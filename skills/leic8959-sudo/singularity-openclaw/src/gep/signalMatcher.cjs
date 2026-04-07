/**
 * singularity Signal Matcher
 * 将 Gene 信号与本地 memory/session 日志匹配，决定本地 vs Hub 优先
 * 对标 capability-evolver/src/gep/signals.js 的匹配逻辑
 *
 * 优先级策略：
 *   1. Hub 优先：信号在 Hub 有高置信度基因（>=0.8），直接 apply
 *   2. 本地优先：信号已被本地成功验证过（capsule 成功率高），用本地
 *   3. 双路并发：两边同时跑，取较优结果
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const { loadGenes } = require('./assetStore.cjs');
const { loadCapsules } = require('./capsuleRecorder.cjs');

const CACHE_DIR = path.join(os.homedir(), '.cache', 'singularity-forum');

// ---------------------------------------------------------------------------
// 本地 Gene 历史置信度
// ---------------------------------------------------------------------------

function getLocalGeneHistory(signal) {
  const capsules = loadCapsules();
  const matching = capsules.filter(c =>
    c.signals && c.signals.some(s => s === signal || s.includes(signal) || signal.includes(s))
  );
  if (!matching.length) return null;
  const latest = matching.sort((a, b) => new Date(b.appliedAt) - new Date(a.appliedAt))[0];
  return {
    geneName: latest.geneName,
    signal,
    localConfidence: latest.newConfidence || latest.confidence,
    outcome: latest.outcome,
    lastApplied: latest.appliedAt,
    totalAttempts: matching.length,
    successRate: getRate(matching),
  };
}

function getRate(capsules) {
  if (!capsules.length) return 0;
  return capsules.filter(c => c.outcome === 'success').length / capsules.length;
}

// ---------------------------------------------------------------------------
// 信号去重/合并
// ---------------------------------------------------------------------------

/** 将原始错误信息列表转换为标准化信号 */
function normalizeSignals(errors) {
  const PATTERNS = [
    { regex: /timeout|超时|timed?out|ETIMEDOUT|ECONNRESET/i, signal: 'network_timeout' },
    { regex: /json.*parse|JSON.*error|SyntaxError|Unexpected token/i, signal: 'json_parse_error' },
    { regex: /401|Unauthorized|unauthorized|token.*invalid|token.*expired/i, signal: 'auth_failure' },
    { regex: /429|rate.?limit|too many requests/i, signal: 'rate_limit' },
    { regex: /Cannot find module|ERR_MODULE_NOT_FOUND/i, signal: 'module_not_found' },
    { regex: /ENOENT|no such file|not found/i, signal: 'file_not_found' },
    { regex: /encoding|UTF-?8|GBK|charset|乱码/i, signal: 'encoding_error' },
    { regex: /loop|iteration|重复|多次.*失败/i, signal: 'repeated_failure' },
    { regex: /SyntaxError|TypeError.*undefined|Cannot read property/i, signal: 'null_reference' },
    { regex: /memory.*leak|heap|OutOfMemory|Maximum call stack/i, signal: 'memory_leak' },
  ];

  const signals = new Set();
  for (const err of errors) {
    for (const p of PATTERNS) {
      if (p.regex.test(err)) signals.add(p.signal);
    }
  }
  return [...signals];
}

// ---------------------------------------------------------------------------
// 核心匹配：决定每个信号用哪条路径
// ---------------------------------------------------------------------------

/**
 * @param {string[]} signals
 * @param {object} hubResults - hubSearch() 返回 { signal, hit, match, score }
 * @returns {object} - 每信号决策 { local, hub, decision }
 */
function matchSignals(signals, hubResults = []) {
  const hubMap = new Map();
  for (const r of hubResults) {
    if (r && r.signals) {
      for (const s of r.signals) hubMap.set(s, r);
    }
    if (r && r.signal) hubMap.set(r.signal, r);
  }

  const decisions = [];
  for (const signal of signals) {
    const local = getLocalGeneHistory(signal);
    const hubRaw = hubMap.get(signal) || null;
    const hub = hubRaw && hubRaw.hit ? { confidence: hubRaw.score * 100, match: hubRaw.match } : null;

    let decision = 'local'; // default

    if (hub && (!local || local.outcome === 'failure')) {
      // Hub 有，本地失败或没有 → Hub 优先
      decision = 'hub';
    } else if (local && local.outcome === 'success' && local.successRate >= 0.8) {
      // 本地已验证成功率高 → 本地优先
      decision = 'local';
    } else if (hub && local) {
      // 都有，比较分数
      decision = (hub.confidence || 0) > (local.localConfidence || 0) ? 'hub' : 'local';
    } else if (hub) {
      decision = 'hub';
    }

    decisions.push({ signal, local, hub, decision });
  }

  return decisions;
}

// ---------------------------------------------------------------------------
// 汇总统计
// ---------------------------------------------------------------------------

function getSignalStats() {
  const capsules = loadCapsules();
  const signals = new Map();

  for (const c of capsules) {
    for (const s of c.signals || []) {
      if (!signals.has(s)) signals.set(s, { total: 0, success: 0, failure: 0 });
      const st = signals.get(s);
      st.total++;
      if (c.outcome === 'success') st.success++;
      else st.failure++;
    }
  }

  return [...signals.entries()]
    .map(([signal, st]) => ({ signal, ...st, rate: st.total ? Math.round((st.success / st.total) * 100) : 0 }))
    .sort((a, b) => b.total - a.total);
}

module.exports = { normalizeSignals, matchSignals, getSignalStats };
