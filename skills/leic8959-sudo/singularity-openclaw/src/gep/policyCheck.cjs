/**
 * singularity GEP PolicyCheck
 * Blast radius 计算 + 约束校验 + 验证命令执行
 *
 * 对标 capability-evolver/src/gep/policyCheck.js
 */
const fs = require('fs');
const path = require('path');
const { getRepoRoot } = require('./paths.cjs');
const { tryRunCmd, normalizeRelPath, gitListChangedFiles, isCriticalProtectedPath } = require('./gitOps.cjs');
const { BLAST_HARD_CAP_FILES, BLAST_HARD_CAP_LINES, BLAST_WARN_RATIO,
  BLAST_CRITICAL_RATIO, CONSTRAINT_MAX_FILES,
  VALIDATION_ALLOWED_PREFIXES, VALIDATION_TIMEOUT_MS, SOLIDIFY_MAX_RETRIES,
  SOLIDIFY_RETRY_INTERVAL_MS, CANARY_TIMEOUT_MS } = require('./config.cjs');

// ---------------------------------------------------------------------------
// Blast radius
// ---------------------------------------------------------------------------

function parseNumstatRows(text) {
  const rows = [];
  const lines = String(text || '').split('\n').map(l => l.trim()).filter(Boolean);
  for (const line of lines) {
    const parts = line.split('\t');
    if (parts.length < 3) continue;
    const added = Number(parts[0]);
    const deleted = Number(parts[1]);
    let file = normalizeRelPath(parts.slice(2).join('\t'));
    if (file.includes('=>')) {
      file = normalizeRelPath(String(file.split('=>').pop()).replace(/[{}]/g, '').trim());
    }
    rows.push({ file, added: Number.isFinite(added) ? added : 0, deleted: Number.isFinite(deleted) ? deleted : 0 });
  }
  return rows;
}

function computeBlastRadius(repoRoot) {
  const policy = readConstraintPolicy();
  let changedFiles = gitListChangedFiles(repoRoot).map(normalizeRelPath).filter(Boolean);

  // 过滤忽略的文件
  const countedFiles = changedFiles.filter(f => isConstraintCountedPath(f, policy));
  const ignoredFiles = changedFiles.filter(f => !isConstraintCountedPath(f, policy));

  // 解析 numstat 获取行数
  const u = tryRunCmd('git diff --numstat', repoRoot, 60000);
  const c = tryRunCmd('git diff --cached --numstat', repoRoot, 60000);
  const unstagedRows = u.ok ? parseNumstatRows(u.out) : [];
  const stagedRows = c.ok ? parseNumstatRows(c.out) : [];
  let churn = 0;
  for (const row of [...unstagedRows, ...stagedRows]) {
    if (!isConstraintCountedPath(row.file, policy)) continue;
    churn += row.added + row.deleted;
  }

  // 新增未追踪文件行数
  const untracked = tryRunCmd('git ls-files --others --exclude-standard', repoRoot, 60000);
  if (untracked.ok) {
    const rels = String(untracked.out).split('\n').map(normalizeRelPath).filter(Boolean);
    for (const rel of rels) {
      if (!isConstraintCountedPath(rel, policy)) continue;
      churn += countFileLines(path.join(repoRoot, rel));
    }
  }

  return {
    files: countedFiles.length,
    lines: churn,
    changed_files: countedFiles,
    ignored_files: ignoredFiles,
    all_changed_files: changedFiles,
  };
}

function countFileLines(absPath) {
  try {
    if (!fs.existsSync(absPath)) return 0;
    const buf = fs.readFileSync(absPath);
    if (!buf || buf.length === 0) return 0;
    let n = 1;
    for (let i = 0; i < buf.length; i++) if (buf[i] === 10) n++;
    return n;
  } catch { return 0; }
}

// ---------------------------------------------------------------------------
// Constraint policy
// ---------------------------------------------------------------------------

function readConstraintPolicy() {
  return {
    excludePrefixes:  ['logs/', 'memory/', 'assets/', 'out/', 'temp/', 'node_modules/', 'dist/'],
    excludeExact:     ['event.json', 'temp_gep_output.json', 'evolution_error.log'],
    excludeRegex:     [/capsules?\.jsonl?$/i],
    includePrefixes:  ['src/', 'scripts/', 'config/'],
    includeExact:     ['index.js', 'package.json', 'SKILL.md'],
    includeExtensions: ['.js', '.cjs', '.mjs', '.ts', '.tsx', '.json', '.yaml', '.yml', '.sh'],
  };
}

function matchAnyPrefix(rel, prefixes) {
  for (const p of (prefixes || [])) {
    const n = normalizeRelPath(p).replace(/\/+$/, '');
    if (!n) continue;
    if (rel === n || rel.startsWith(n + '/')) return true;
  }
  return false;
}

function matchAnyExact(rel, exacts) {
  return new Set((exacts || []).map(normalizeRelPath)).has(rel);
}

function matchAnyRegex(rel, regexList) {
  for (const raw of (regexList || [])) {
    try {
      if (new RegExp(raw, 'i').test(rel)) return true;
    } catch {}
  }
  return false;
}

function isConstraintCountedPath(relPath, policy) {
  const rel = normalizeRelPath(relPath);
  if (!rel) return false;
  if (matchAnyExact(rel, policy.excludeExact)) return false;
  if (matchAnyPrefix(rel, policy.excludePrefixes)) return false;
  if (matchAnyRegex(rel, policy.excludeRegex)) return false;
  if (matchAnyExact(rel, policy.includeExact)) return true;
  if (matchAnyPrefix(rel, policy.includePrefixes)) return true;
  const lower = rel.toLowerCase();
  for (const ext of (policy.includeExtensions || [])) {
    if (lower.endsWith(String(ext).toLowerCase())) return true;
  }
  return false;
}

function isForbiddenPath(relPath, forbiddenPaths) {
  const rel = normalizeRelPath(relPath);
  for (const fp of (forbiddenPaths || [])) {
    const f = normalizeRelPath(fp);
    if (rel === f || rel.startsWith(f + '/')) return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
// Blast severity classification
// ---------------------------------------------------------------------------

function classifyBlastSeverity(blast, maxFiles) {
  const files = Number(blast.files) || 0;
  const lines = Number(blast.lines) || 0;

  if (files > BLAST_HARD_CAP_FILES || lines > BLAST_HARD_CAP_LINES) {
    return {
      severity: 'hard_cap_breach',
      message: `HARD CAP BREACH: ${files} files / ${lines} lines exceeds system limit (${BLAST_HARD_CAP_FILES} files / ${BLAST_HARD_CAP_LINES} lines)`,
    };
  }
  const mF = Number.isFinite(maxFiles) && maxFiles > 0 ? maxFiles : CONSTRAINT_MAX_FILES;
  if (files > mF * BLAST_CRITICAL_RATIO) {
    return {
      severity: 'critical_overrun',
      message: `CRITICAL OVERRUN: ${files} files > ${mF * BLAST_CRITICAL_RATIO} (${BLAST_CRITICAL_RATIO}x limit of ${mF})`,
    };
  }
  if (files > mF) {
    return { severity: 'exceeded', message: `max_files exceeded: ${files} > ${mF}` };
  }
  if (files > mF * BLAST_WARN_RATIO) {
    return { severity: 'approaching_limit', message: `approaching limit: ${files} / ${mF} files (${Math.round((files / mF) * 100)}%)` };
  }
  return { severity: 'within_limit', message: `${files} / ${mF} files` };
}

function analyzeBlastRadiusBreakdown(changedFiles, topN = 5) {
  const dirCount = {};
  for (const f of (changedFiles || [])) {
    const rel = normalizeRelPath(f);
    if (!rel) continue;
    const parts = rel.split('/');
    const key = parts.length >= 2 ? parts.slice(0, 2).join('/') : parts[0];
    dirCount[key] = (dirCount[key] || 0) + 1;
  }
  return Object.entries(dirCount).sort((a, b) => b[1] - a[1]).slice(0, topN)
    .map(([dir, files]) => ({ dir, files }));
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

function isValidationCommandAllowed(cmd) {
  const c = String(cmd || '').trim();
  if (!c) return false;
  if (!VALIDATION_ALLOWED_PREFIXES.some(p => c.startsWith(p))) return false;
  if (/`|\$\(/.test(c)) return false;
  const stripped = c.replace(/"[^"]*"/g, '').replace(/'[^']*'/g, '');
  if (/[;&|><]/.test(stripped)) return false;
  if (/^node\s+(-e|--eval|--print|-p)\b/.test(c)) return false;
  return true;
}

function runValidationsOnce(gene, repoRoot, timeoutMs) {
  const validation = Array.isArray(gene && gene.validation) ? gene.validation : [];
  const results = [];
  for (const cmd of validation) {
    const c = String(cmd || '').trim();
    if (!c) continue;
    if (!isValidationCommandAllowed(c)) {
      results.push({ cmd: c, ok: false, err: 'BLOCKED: validation command rejected (allowed: node/npm/npx; shell operators prohibited)' });
      return { ok: false, results, startedAt: Date.now(), finishedAt: Date.now() };
    }
    const r = tryRunCmd(c, repoRoot, timeoutMs || VALIDATION_TIMEOUT_MS);
    results.push({ cmd: c, ok: r.ok, out: String(r.out || ''), err: String(r.err || '') });
    if (!r.ok) return { ok: false, results, startedAt: Date.now(), finishedAt: Date.now() };
  }
  return { ok: true, results, startedAt: Date.now(), finishedAt: Date.now() };
}

function sleepSync(ms) {
  try {
    const arr = new Int32Array(new SharedArrayBuffer(4));
    Atomics.wait(arr, 0, 0, Math.max(0, ms));
  } catch {
    require('child_process').execSync('sleep ' + Math.max(0, ms / 1000), { windowsHide: true });
  }
}

function runValidations(gene, repoRoot) {
  let attempt = 0;
  let result;
  while (attempt <= SOLIDIFY_MAX_RETRIES) {
    result = runValidationsOnce(gene, repoRoot, VALIDATION_TIMEOUT_MS);
    if (result.ok) {
      if (attempt > 0) console.log('[PolicyCheck] Validation passed on retry ' + attempt);
      result.retries_attempted = attempt;
      return result;
    }
    const blocked = result.results && result.results.some(r => r.err && r.err.startsWith('BLOCKED:'));
    if (blocked) break;
    attempt++;
    if (attempt <= SOLIDIFY_MAX_RETRIES) {
      console.log('[PolicyCheck] Validation failed (attempt ' + attempt + '/' + (SOLIDIFY_MAX_RETRIES + 1) + '), retrying...');
      sleepSync(SOLIDIFY_RETRY_INTERVAL_MS);
    }
  }
  result.retries_attempted = attempt > 0 ? attempt - 1 : 0;
  return result;
}

function runCanaryCheck(repoRoot) {
  const canaryScript = path.join(repoRoot, 'src', 'canary.js');
  if (!fs.existsSync(canaryScript)) {
    return { ok: true, skipped: true, reason: 'canary.js not found' };
  }
  const r = tryRunCmd('node "' + canaryScript + '"', repoRoot, CANARY_TIMEOUT_MS);
  return { ok: r.ok, skipped: false, out: String(r.out || ''), err: String(r.err || '') };
}

// ---------------------------------------------------------------------------
// Full constraint check
// ---------------------------------------------------------------------------

function checkConstraints(gene, blast, repoRoot) {
  const violations = [];
  const warnings = [];
  if (!gene || gene.type !== 'Gene') return { ok: true, violations, warnings };

  const constraints = gene.constraints || {};
  const maxFiles = Number(constraints.max_files) > 0 ? Number(constraints.max_files) : CONSTRAINT_MAX_FILES;

  const blastSev = classifyBlastSeverity(blast, maxFiles);
  if (blastSev.severity === 'hard_cap_breach') violations.push(blastSev.message);
  else if (blastSev.severity === 'critical_overrun') {
    violations.push(blastSev.message);
    const breakdown = analyzeBlastRadiusBreakdown(blast.all_changed_files || []);
    console.error('[PolicyCheck] Top dirs: ' + breakdown.map(d => d.dir + ' (' + d.files + ')').join(', '));
  } else if (blastSev.severity === 'exceeded') {
    violations.push(blastSev.message);
  } else if (blastSev.severity === 'approaching_limit') {
    warnings.push(blastSev.message);
  }

  const forbidden = Array.isArray(constraints.forbidden_paths) ? constraints.forbidden_paths : [];
  for (const f of (blast.all_changed_files || [])) {
    if (isForbiddenPath(f, forbidden)) violations.push('forbidden_path touched: ' + f);
    if (isCriticalProtectedPath(f)) {
      violations.push('critical_path_modified: ' + normalizeRelPath(f));
    }
  }

  // Ethics check
  const ethicsText = [
    ...(Array.isArray(gene.strategy) ? gene.strategy : []),
    gene.description || '',
    gene.summary || '',
  ].join(' ');
  const ethicsPatterns = [
    { re: /bypass|disable|circumvent|remove\s+(?:safety|guardrail|security|ethic|constraint|protection)/i, msg: 'ethics: strategy attempts to bypass safety mechanisms' },
    { re: /keylogger|screen\s*capture|webcam\s*hijack/i, msg: 'ethics: covert monitoring tool' },
    { re: /hide|conceal|obfuscat\w*\s+(?:action|behavior|intent|log)/i, msg: 'ethics: strategy conceals actions' },
  ];
  for (const p of ethicsPatterns) {
    if (p.re.test(ethicsText)) violations.push(p.msg);
  }

  return { ok: violations.length === 0, violations, warnings };
}

// ---------------------------------------------------------------------------
// Destructive change detection
// ---------------------------------------------------------------------------

function detectDestructiveChanges(repoRoot, baselineUntracked = []) {
  const violations = [];
  const baselineSet = new Set(baselineUntracked.map(String));
  const changed = gitListChangedFiles(repoRoot);
  for (const rel of changed) {
    if (!isCriticalProtectedPath(rel)) continue;
    const abs = path.join(repoRoot, rel);
    if (!fs.existsSync(abs)) violations.push('CRITICAL_FILE_DELETED: ' + rel);
  }
  return violations;
}

// ---------------------------------------------------------------------------
// Failure reason builder
// ---------------------------------------------------------------------------

function buildFailureReason(constraintCheck, validation, canary) {
  const reasons = [];
  if (constraintCheck && Array.isArray(constraintCheck.violations)) {
    for (const v of constraintCheck.violations) reasons.push('constraint: ' + v);
  }
  if (validation && Array.isArray(validation.results)) {
    for (const r of validation.results) {
      if (!r.ok) reasons.push('validation_failed: ' + String(r.cmd || '').slice(0, 80) + ' => ' + String(r.err || '').slice(0, 200));
    }
  }
  if (canary && !canary.ok && !canary.skipped) {
    reasons.push('canary_failed: ' + String(canary.err || '').slice(0, 200));
  }
  return reasons.join('; ').slice(0, 2000) || 'unknown';
}

module.exports = {
  computeBlastRadius,
  isConstraintCountedPath,
  isForbiddenPath,
  classifyBlastSeverity,
  analyzeBlastRadiusBreakdown,
  runValidations,
  runCanaryCheck,
  checkConstraints,
  detectDestructiveChanges,
  isValidationCommandAllowed,
  buildFailureReason,
  BLAST_HARD_CAP_FILES,
  BLAST_HARD_CAP_LINES,
};
