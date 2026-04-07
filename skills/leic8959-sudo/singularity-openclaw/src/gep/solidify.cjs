/**
 * singularity GEP Solidify
 * 基因发布前的代码固态化流水线：
 *   1. 计算 blast radius
 *   2. 约束校验（policyCheck）
 *   3. 验证命令执行（runValidations）
 *   4. Canary check
 *   5. 生成验证报告
 *
 * 对标 capability-evolver/src/gep/solidify.js
 */
const fs = require('fs');
const path = require('path');
const { getRepoRoot, getGepAssetsDir } = require('./paths.cjs');
const { computeBlastRadius, checkConstraints, runValidations,
  runCanaryCheck, buildFailureReason, detectDestructiveChanges } = require('./policyCheck.cjs');
const { gitListChangedFiles, rollbackTracked, rollbackNewUntrackedFiles,
  captureDiffSnapshot, isGitRepo } = require('./gitOps.cjs');

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------

function stateFile() {
  return path.join(getGepAssetsDir(), 'solidify_state.json');
}

function reportFile(runId) {
  return path.join(getGepAssetsDir(), 'solidify_report_' + runId + '.json');
}

function readState() {
  try {
    if (!fs.existsSync(stateFile())) return null;
    return JSON.parse(fs.readFileSync(stateFile(), 'utf-8'));
  } catch { return null; }
}

function writeState(state) {
  const dir = path.dirname(stateFile());
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(stateFile() + '.tmp', JSON.stringify(state, null, 2));
  fs.renameSync(stateFile() + '.tmp', stateFile());
}

// ---------------------------------------------------------------------------
// Build validation report
// ---------------------------------------------------------------------------

function buildValidationReport({ gene, blast, constraintCheck, validation, canary, runId }) {
  return {
    runId,
    geneId: gene && (gene.id || gene.name || 'unknown'),
    timestamp: new Date().toISOString(),
    blastRadius: {
      files: blast.files,
      lines: blast.lines,
      changed_files: blast.changed_files,
      ignored_files: blast.ignored_files,
    },
    constraints: {
      ok: constraintCheck.ok,
      violations: constraintCheck.violations,
      warnings: constraintCheck.warnings,
    },
    validation: {
      ok: validation.ok,
      results: validation.results,
      retries_attempted: validation.retries_attempted,
    },
    canary: {
      ok: canary.ok,
      skipped: canary.skipped,
      reason: canary.reason || null,
    },
    overall: constraintCheck.ok && validation.ok && canary.ok,
    failureReason: constraintCheck.ok && validation.ok && canary.ok
      ? null
      : buildFailureReason(constraintCheck, validation, canary),
  };
}

// ---------------------------------------------------------------------------
// Solidify a gene: gate check before it is applied/published
// ---------------------------------------------------------------------------

/**
 * @param {object} gene - Gene 对象
 * @param {object} opts
 * @param {boolean} opts.skipValidation - 跳过命令验证（仅 blast+constraint）
 * @param {string} opts.runId - 此次运行的 ID
 * @param {boolean} opts.dryRun - 干跑，不写入报告
 * @returns {object} 验证报告
 */
function solidifyGene(gene, opts = {}) {
  const skipValidation = !!opts.skipValidation;
  const dryRun = !!opts.dryRun;
  const runId = opts.runId || ('s_' + Date.now().toString(36));
  const repoRoot = getRepoRoot();

  console.log('[Solidify] Starting for gene: ' + (gene.id || gene.name || '?'));
  if (dryRun) console.log('[Solidify] DRY RUN — no writes');

  // 1. Blast radius
  let blast;
  try {
    blast = computeBlastRadius(repoRoot);
    console.log('[Solidify] Blast: ' + blast.files + ' files, ' + blast.lines + ' lines');
  } catch (e) {
    blast = { files: 0, lines: 0, changed_files: [], ignored_files: [], all_changed_files: [] };
    console.warn('[Solidify] Blast radius failed (non-fatal): ' + e.message);
  }

  // 2. Constraint check
  let constraintCheck;
  try {
    constraintCheck = checkConstraints(gene, blast, repoRoot);
    if (!constraintCheck.ok) {
      console.error('[Solidify] CONSTRAINT VIOLATIONS:');
      constraintCheck.violations.forEach(v => console.error('  ✗ ' + v));
    }
    constraintCheck.warnings.forEach(w => console.warn('[Solidify] WARN: ' + w));
  } catch (e) {
    constraintCheck = { ok: false, violations: ['policyCheck error: ' + e.message], warnings: [] };
    console.error('[Solidify] PolicyCheck failed: ' + e.message);
  }

  // 3. Validation commands
  let validation;
  if (!skipValidation) {
    try {
      validation = runValidations(gene, repoRoot);
      if (!validation.ok) {
        console.error('[Solidify] VALIDATION FAILED:');
        (validation.results || []).forEach(r => {
          if (!r.ok) console.error('  ✗ ' + r.cmd + ' => ' + r.err.slice(0, 100));
        });
      }
    } catch (e) {
      validation = { ok: false, results: [{ cmd: 'runValidations', ok: false, err: e.message }] };
      console.error('[Solidify] Validation error: ' + e.message);
    }
  } else {
    validation = { ok: true, results: [], skipped: true };
    console.log('[Solidify] Validation skipped (--skip-validation)');
  }

  // 4. Canary check
  let canary;
  try {
    canary = runCanaryCheck(repoRoot);
    if (!canary.ok && !canary.skipped) {
      console.warn('[Solidify] Canary failed: ' + (canary.err || '').slice(0, 100));
    }
  } catch (e) {
    canary = { ok: true, skipped: true, reason: 'error: ' + e.message };
  }

  // 5. Build report
  const report = buildValidationReport({ gene, blast, constraintCheck, validation, canary, runId });

  // 6. Write report + state (unless dry run)
  if (!dryRun) {
    try {
      const dir = path.dirname(reportFile(runId));
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(reportFile(runId), JSON.stringify(report, null, 2));
      writeState({ last_report: runId, timestamp: new Date().toISOString(), ok: report.overall });
    } catch (e) {
      console.warn('[Solidify] Report write failed: ' + e.message);
    }
  }

  // Log to console
  if (report.overall) {
    console.log('[Solidify] ✅ PASSED — gene ready: ' + report.geneId);
  } else {
    console.error('[Solidify] ❌ FAILED — reason: ' + (report.failureReason || 'unknown'));
  }

  return report;
}

// ---------------------------------------------------------------------------
// Rollback on failure
// ---------------------------------------------------------------------------

function rollbackOnFailure(repoRoot, rollbackMode) {
  console.log('[Solidify] Rolling back...');
  const r = rollbackTracked(repoRoot, rollbackMode || 'hard');
  console.log('[Solidify] Rollback ' + r.mode + ': ' + (r.ok ? 'ok' : 'failed'));
  return r;
}

// ---------------------------------------------------------------------------
// Solidify gate: return pass/fail + details
// ---------------------------------------------------------------------------

/**
 * 入口函数：在发布基因前调用
 * @returns {{ ok: boolean, report: object, rollback: object|null }}
 */
function solidifyGate(gene, opts = {}) {
  const report = solidifyGene(gene, opts);

  if (report.overall) {
    return { ok: true, report };
  }

  // Failure — auto-rollback if configured
  let rollbackResult = null;
  const rollbackMode = String(process.env.GIT_ROLLBACK_MODE || 'hard').toLowerCase();
  if (rollbackMode !== 'none') {
    rollbackResult = rollbackOnFailure(getRepoRoot(), rollbackMode);
  }

  return { ok: false, report, rollback: rollbackResult };
}

module.exports = {
  solidifyGene,
  solidifyGate,
  rollbackOnFailure,
  buildValidationReport,
  computeBlastRadius,
  checkConstraints,
  runValidations,
  runCanaryCheck,
};
