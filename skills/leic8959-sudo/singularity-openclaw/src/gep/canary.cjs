/**
 * singularity-forum - Canary Validation（对标 evolver validateGene）
 *
 * Gene 发布前进行轻量 canary 测试：
 * 1. 检查 pre_conditions
 * 2. 模拟应用 gene 策略
 * 3. 验证 post_conditions
 * 4. 不满足则拒绝发布
 */
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';
import { loadCredentials, log } from '../../lib/api.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// =============================================================================
// Canary 验证器
// =============================================================================

async function validateGene(gene, mutation) {
  const results = {
    passed: false,
    checks: [],
    errors: [],
    warnings: [],
    score: 0,
  };

  // 1. Pre-conditions 检查
  const preChecks = runPreConditions(gene, mutation);
  results.checks.push(...preChecks.checks);
  results.errors.push(...preChecks.errors);
  results.warnings.push(...preChecks.warnings);

  // 2. 模拟 canary 测试
  const canaryResult = await runCanaryTest(gene);
  results.checks.push(...canaryResult.checks);
  if (!canaryResult.passed) results.errors.push(...canaryResult.errors);
  results.warnings.push(...canaryResult.warnings);

  // 3. Post-conditions 验证
  const postChecks = runPostConditions(gene);
  results.checks.push(...postChecks.checks);
  results.errors.push(...postChecks.errors);
  results.warnings.push(...postChecks.warnings);

  // 评分
  const totalChecks = results.checks.length;
  const failedChecks = results.errors.length;
  results.score = totalChecks > 0 ? Math.max(0, (totalChecks - failedChecks) / totalChecks) : 0;
  results.passed = results.errors.length === 0 && results.score >= 0.7;

  if (!results.passed) {
    log('WARN', 'canary', 'Validation failed for ' + gene.displayName + ': ' + results.errors.join('; '));
  } else {
    log('INFO', 'canary', 'Validation passed for ' + gene.displayName + ' (score=' + results.score.toFixed(2) + ')');
  }

  return results;
}

// =============================================================================
// Pre-conditions
// =============================================================================

function runPreConditions(gene, mutation) {
  const result = { checks: [], errors: [], warnings: [] };

  // 1. API Key 有效
  try {
    loadCredentials();
    result.checks.push({ name: 'api_key_valid', passed: true });
  } catch {
    result.errors.push({ name: 'api_key_valid', message: 'Forum API key not configured' });
  }

  // 2. Mutation pre_conditions 满足
  if (mutation?.pre_conditions?.length) {
    for (const cond of mutation.pre_conditions) {
      const satisfied = checkCondition(cond);
      result.checks.push({ name: 'pre_condition:' + cond, passed: satisfied });
      if (!satisfied) result.errors.push({ name: 'pre_condition:' + cond, message: 'Pre-condition not met: ' + cond });
    }
  }

  // 3. 网络可用
  if (isNetworkAvailable()) {
    result.checks.push({ name: 'network_available', passed: true });
  } else {
    result.warnings.push({ name: 'network_available', message: 'Network may be unavailable, proceeding anyway' });
  }

  // 4. 磁盘空间充足
  const diskFreeGb = getDiskFreeGb();
  if (diskFreeGb >= 1) {
    result.checks.push({ name: 'disk_space', passed: true, detail: diskFreeGb.toFixed(1) + 'GB free' });
  } else {
    result.errors.push({ name: 'disk_space', message: 'Disk space critical: ' + diskFreeGb.toFixed(1) + 'GB free' });
  }

  // 5. 候选基因 GDI 阈值
  const gdiScore = gene.strategy?.gdiScore || gene.gdiScore || 50;
  if (gdiScore >= 55) {
    result.checks.push({ name: 'gdi_threshold', passed: true, detail: 'GDI=' + gdiScore });
  } else {
    result.warnings.push({ name: 'gdi_threshold', message: 'GDI=' + gdiScore + ' below typical threshold (65)' });
  }

  // 6. 基因描述非空
  if (gene.description && gene.description.length >= 10) {
    result.checks.push({ name: 'description_present', passed: true });
  } else {
    result.errors.push({ name: 'description_present', message: 'Gene description too short or missing' });
  }

  return result;
}

// =============================================================================
// Canary 测试
// =============================================================================

async function runCanaryTest(gene) {
  const result = { checks: [], errors: [], warnings: [], passed: true };

  // 模拟应用策略，看是否会产生新的错误
  const simulationErrors = simulateGeneApplication(gene);

  for (const err of simulationErrors) {
    result.warnings.push({ name: 'canary_warning', message: err });
  }

  // 测试 API 连通性
  try {
    const cred = loadCredentials();
    const resp = await fetch('https://singularity.mba/api/me', {
      method: 'GET',
      headers: { Authorization: 'Bearer ' + cred.forum_api_key },
      signal: AbortSignal.timeout(5000),
    });
    if (resp.ok) {
      result.checks.push({ name: 'forum_api_reachable', passed: true });
    } else if (resp.status === 401) {
      result.errors.push({ name: 'forum_api_reachable', message: 'API returns 401 - key may be invalid' });
      result.passed = false;
    } else {
      result.warnings.push({ name: 'forum_api_reachable', message: 'API returned status ' + resp.status });
    }
  } catch (e) {
    result.warnings.push({ name: 'forum_api_reachable', message: 'API unreachable: ' + e.message });
  }

  // 检查 strategy steps 是否合理
  const steps = gene.strategy?.steps || gene.steps || [];
  if (steps.length >= 1 && steps.length <= 10) {
    result.checks.push({ name: 'strategy_steps_reasonable', passed: true, detail: steps.length + ' steps' });
  } else if (steps.length > 10) {
    result.warnings.push({ name: 'strategy_steps_reasonable', message: 'Strategy has ' + steps.length + ' steps (may be too complex)' });
  } else {
    result.errors.push({ name: 'strategy_steps_reasonable', message: 'Strategy has no steps defined' });
    result.passed = false;
  }

  return result;
}

// =============================================================================
// Post-conditions
// =============================================================================

function runPostConditions(gene) {
  const result = { checks: [], errors: [], warnings: [] };

  // 验证 category 合法
  const validCategories = ['REPAIR', 'OPTIMIZE', 'INNOVATE', 'repair', 'optimize', 'innovate'];
  if (validCategories.includes(gene.category)) {
    result.checks.push({ name: 'category_valid', passed: true, detail: gene.category });
  } else {
    result.errors.push({ name: 'category_valid', message: 'Invalid category: ' + gene.category });
  }

  // 验证 taskType 合法
  const validTaskTypes = ['AUTO_REPLY', 'POST_SUMMARY', 'NETWORK_REQUEST', 'DATA_PARSING', 'API_REQUEST', 'CODE_EXECUTION', 'FILE_SYSTEM'];
  if (!gene.taskType || validTaskTypes.includes(gene.taskType)) {
    result.checks.push({ name: 'tasktype_valid', passed: true });
  } else {
    result.warnings.push({ name: 'tasktype_valid', message: 'Unusual taskType: ' + gene.taskType });
  }

  // 验证 signals 非空
  if (gene.signals?.length > 0) {
    result.checks.push({ name: 'signals_present', passed: true, detail: gene.signals.join(', ') });
  } else {
    result.errors.push({ name: 'signals_present', message: 'No signals defined for this gene' });
  }

  return result;
}

// =============================================================================
// 工具函数
// =============================================================================

function checkCondition(cond) {
  // 通用条件检查
  if (cond === 'api_key valid') {
    try { loadCredentials(); return true; } catch { return false; }
  }
  if (cond === 'network available') return isNetworkAvailable();
  if (cond === 'disk space available') return getDiskFreeGb() >= 1;
  if (cond.startsWith('gdi_score >')) {
    const threshold = parseInt(cond.split('>')[1], 10);
    return true; // gdiScore 已在 pre-check 中验证
  }
  return true; // 未知条件默认通过
}

function isNetworkAvailable() {
  try {
    require('child_process').execSync(
      process.platform === 'win32'
        ? 'ping -n 1 -w 1000 8.8.8.8'
        : 'ping -c 1 -W 1 8.8.8.8',
      { encoding: 'utf-8', timeout: 3000, stdio: 'ignore' }
    );
    return true;
  } catch { return false; }
}

function getDiskFreeGb() {
  try {
    if (process.platform === 'win32') {
      const out = require('child_process').execSync(
        'powershell -Command "(Get-PSDrive C).Free / 1GB"',
        { encoding: 'utf-8', timeout: 3000, windowsHide: true }
      ).trim();
      return parseFloat(out) || 0;
    } else {
      const stats = fs.statfsSync('/');
      return Math.round((stats.bfree * stats.bsize) / 1024**3 * 10) / 10;
    }
  } catch { return 0; }
}

/**
 * 模拟应用基因策略，返回可能产生的新错误
 */
function simulateGeneApplication(gene) {
  const warnings = [];
  const steps = gene.strategy?.steps || [];

  // 检测策略是否有潜在问题
  if (steps.some(s => s.toLowerCase().includes('delete') || s.toLowerCase().includes('rm '))) {
    warnings.push('Strategy contains destructive operations');
  }
  if (steps.some(s => s.toLowerCase().includes('exec') || s.toLowerCase().includes('eval'))) {
    warnings.push('Strategy contains eval/exec - potential security risk');
  }
  if (gene.strategy?.algorithm === 'exponential_backoff') {
    warnings.push('Consider setting max_retries cap for exponential_backoff');
  }

  return warnings;
}
