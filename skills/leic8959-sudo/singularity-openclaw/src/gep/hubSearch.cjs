/**
 * singularity Hub Search — Search-first evolution for singularity.mba
 *
 * 对标 capability-evolver/src/gep/hubSearch.js
 * 适配 singularity.mba EvoMap A2A 接口：
 *   POST /api/evomap/a2a/fetch   (信号匹配搜索)
 *   POST /api/evomap/a2a/apply   (应用 Gene)
 *   POST /api/evomap/a2a/report  (回传置信度)
 *
 * 流程: signals → Phase1(search_only) → 选最优 → Phase2(拉取完整 payload) → apply
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const { loadCredentials } = require('../../lib/api.js');
const { appendEventJsonl } = require('./assetStore.cjs');

const FORUM_BASE = 'https://singularity.mba';
const SEARCH_CACHE_TTL_MS = 5 * 60 * 1000;
const SEARCH_CACHE_MAX = 200;
const PAYLOAD_CACHE_MAX = 100;
const MIN_PHASE2_MS = 500;
const SEMANTIC_TIMEOUT_MS = 3000;
const DEFAULT_MIN_SCORE = 0.72;
const MAX_STREAK_CAP = 5;

// --- In-memory caches ---
const _searchCache = new Map();
const _payloadCache = new Map();

function _cacheKey(signals) {
  return signals.slice().sort().join('|');
}
function _getSearch(key) {
  const e = _searchCache.get(key);
  if (!e) return null;
  if (Date.now() - e.ts > SEARCH_CACHE_TTL_MS) { _searchCache.delete(key); return null; }
  return e.v;
}
function _setSearch(key, v) {
  if (_searchCache.size >= SEARCH_CACHE_MAX) {
    const old = _searchCache.keys().next().value;
    _searchCache.delete(old);
  }
  _searchCache.set(key, { ts: Date.now(), v });
}
function _getPayload(assetId) { return _payloadCache.get(assetId) || null; }
function _setPayload(assetId, payload) {
  if (_payloadCache.size >= PAYLOAD_CACHE_MAX) {
    const old = _payloadCache.keys().next().value;
    _payloadCache.delete(old);
  }
  _payloadCache.set(assetId, payload);
}

// --- Build A2A fetch message (singularity 专用格式) ---
function buildFetchMsg(signals, opts = {}) {
  const msg = {
    protocol: 'gep-a2a',
    message_type: 'fetch',
    payload: {
      signals: signals.map(s => typeof s === 'string' ? s : String(s)),
      taskType: 'AUTO_REPLY',
      search_only: !!opts.searchOnly,
      limit: opts.limit || 5,
    },
  };
  return msg;
}

function buildApplyMsg(gene, targetPath) {
  return {
    protocol: 'gep-a2a',
    message_type: 'apply',
    payload: {
      geneId: gene.id || gene.geneId || gene.name,
      geneName: gene.name,
      displayName: gene.displayName,
      strategy: gene.strategy || {},
      signals: gene.signals || [],
      confidence: gene.confidence || 60,
      targetPath: targetPath || '',
      dryRun: false,
      autoPublishCapsule: true,
    },
  };
}

function buildReportMsg(assetId, outcome, confidenceDelta) {
  return {
    protocol: 'gep-a2a',
    message_type: 'report',
    payload: {
      assetId,
      outcome,           // 'success' | 'failure' | 'degraded'
      confidenceDelta,  // -20 ~ +20
      timestamp: new Date().toISOString(),
    },
  };
}

// --- HTTP helper ---
async function apiPost(apiKey, subPath, body, timeoutMs = 8000) {
  const url = `${FORUM_BASE}${subPath}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Accept': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    clearTimeout(timer);
    const text = await resp.text();
    let data;
    try { data = JSON.parse(text); } catch { throw new Error(`parse error: ${text.slice(0, 100)}`); }
    if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${data?.error || data?.message || text.slice(0, 100)}`);
    return data;
  } finally {
    clearTimeout(timer);
  }
}

// --- Scoring ---
function scoreHubResult(asset) {
  const confidence = Number(asset.confidence) || 0;
  const streak = Math.min(Math.max(Number(asset.success_streak || asset.successStreak) || 0, 1), MAX_STREAK_CAP);
  const rep = Number.isFinite(Number(asset.reputation_score || asset.reputation)) ? Number(asset.reputation_score || asset.reputation) : 50;
  return confidence * streak * (rep / 100);
}

function pickBest(results, minScore) {
  if (!Array.isArray(results) || !results.length) return null;
  let best = null, bestScore = 0;
  for (const asset of results) {
    if (asset.status && asset.status !== 'promoted') continue;
    const s = scoreHubResult(asset);
    if (s > bestScore) { bestScore = s; best = asset; }
  }
  if (!best || bestScore < minScore) return null;
  return { match: best, score: Math.round(bestScore * 1000) / 1000 };
}

// --- Semantic query (直接调 singularity /api/search) ---
function buildSemanticQuery(signals) {
  return signals
    .filter(s => !s.startsWith('errsig:'))
    .map(s => { const i = s.indexOf(':'); return i > 0 && i < 30 ? s.slice(i + 1).trim() : s; })
    .filter(Boolean)
    .slice(0, 12)
    .join(' ');
}

async function fetchSemanticResults(apiKey, signalList) {
  const query = buildSemanticQuery(signalList);
  if (!query || query.length < 3) return [];
  const url = `${FORUM_BASE}/api/search?q=${encodeURIComponent(query)}&type=gene&limit=10`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SEMANTIC_TIMEOUT_MS);
  try {
    const resp = await fetch(url, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${apiKey}`, 'Accept': 'application/json' },
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (!resp.ok) return [];
    const data = await resp.json();
    const genes = (data.genes || data.data || []).map(g => ({ ...g, _isSemantic: true }));
    return genes;
  } catch { clearTimeout(timer); return []; }
}

// --- Merge search + semantic ---
function mergeResults(searchResults, semanticResults) {
  const seen = new Set();
  const merged = [];
  for (const a of searchResults) {
    const id = a.asset_id || a.geneId || a.id || '';
    if (id) seen.add(id);
    merged.push(a);
  }
  for (const b of semanticResults) {
    const id = b.asset_id || b.geneId || b.id || '';
    if (id && seen.has(id)) continue;
    if (id) seen.add(id);
    merged.push({ ...b, _isSemantic: true });
  }
  return merged;
}

// --- Log to events.jsonl ---
function logAssetCall(call) {
  try { appendEventJsonl({ type: 'asset_call', ...call }); } catch {}
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * 在 singularity.mba 搜索匹配的 Gene
 * @param {string[]} signals - 信号列表
 * @param {object} opts
 * @param {number} opts.threshold - 最低匹配分数 (default 0.72)
 * @param {number} opts.timeoutMs - 总超时 (default 8000)
 * @returns {Promise<{hit: boolean, match?, score?, asset_id?, signals?, reason?}>}
 */
async function hubSearch(signals, opts = {}) {
  if (!Array.isArray(signals) || !signals.length) return { hit: false, reason: 'no_signals' };

  const threshold = Number(opts.threshold || DEFAULT_MIN_SCORE);
  const timeoutMs = Number(opts.timeoutMs || 8000);
  const deadline = Date.now() + timeoutMs;

  let apiKey;
  try { apiKey = loadCredentials().api_key; } catch { return { hit: false, reason: 'no_credentials' }; }

  const cacheKey = _cacheKey(signals);

  // Phase 1: search_only fetch + semantic (parallel)
  let results = _getSearch(cacheKey);
  let cacheHit = !!results;
  let semanticUsed = false;

  if (!results) {
    const fetchPromise = (async () => {
      const msg = buildFetchMsg(signals, { searchOnly: true });
      try {
        const data = await apiPost(apiKey, '/api/evomap/a2a/fetch', msg, deadline - Date.now());
        return (data.payload && Array.isArray(data.payload.results)) ? data.payload.results : [];
      } catch { return []; }
    })();

    const semanticPromise = fetchSemanticResults(apiKey, signals);

    const settled = await Promise.allSettled([fetchPromise, semanticPromise]);
    const rawSearch = settled[0].status === 'fulfilled' ? settled[0].value : [];
    const semantic = settled[1].status === 'fulfilled' ? settled[1].value : [];

    if (!rawSearch.length && !semantic.length) {
      logAssetCall({ action: 'hub_search_miss', signals, reason: 'no_results', via: 'search' });
      return { hit: false, reason: 'no_results' };
    }

    results = mergeResults(rawSearch, semantic);
    semanticUsed = semantic.length > 0;
    _setSearch(cacheKey, results);
  }

  if (!results.length) {
    logAssetCall({ action: 'hub_search_miss', signals, reason: 'no_results' });
    return { hit: false, reason: 'no_results' };
  }

  const pick = pickBest(results, threshold);
  if (!pick) {
    logAssetCall({ action: 'hub_search_miss', signals, reason: 'below_threshold', candidates: results.length, threshold });
    return { hit: false, reason: 'below_threshold', candidates: results.length };
  }

  const assetId = pick.match.geneId || pick.match.asset_id || pick.match.id;
  const mode = 'reference'; // singularity 基因只支持 reference 模式（apply 到 memory/config）

  // Phase 2: 拉取完整 payload（如果缓存未命中）
  const cachedPayload = _getPayload(assetId);
  if (!cachedPayload && (deadline - Date.now()) > MIN_PHASE2_MS) {
    try {
      const data = await apiPost(apiKey, '/api/evomap/a2a/fetch', buildFetchMsg(signals), deadline - Date.now());
      const fullResults = (data.payload && Array.isArray(data.payload.results)) ? data.payload.results : [];
      if (fullResults.length > 0) {
        _setPayload(assetId, fullResults[0]);
        Object.assign(pick.match, fullResults[0]);
      }
    } catch { /* non-fatal */ }
  } else if (cachedPayload) {
    Object.assign(pick.match, cachedPayload);
  }

  const viaLabel = cacheHit ? 'search_cached' : (semanticUsed ? 'search+semantic' : 'search_only');
  console.log(`[HubSearch] Hit(${viaLabel}): ${assetId} score=${pick.score}`);

  logAssetCall({
    action: 'hub_search_hit',
    asset_id: assetId,
    score: pick.score,
    mode,
    signals,
    via: viaLabel,
  });

  return {
    hit: true,
    match: pick.match,
    score: pick.score,
    mode,
    asset_id: assetId,
    signals,
  };
}

/**
 * Apply 一个 Gene 到本地（写入 memory 或配置文件）
 * @param {object} gene - Gene 对象
 * @param {object} opts
 * @param {string} opts.targetPath - 应用目标路径（可选）
 * @returns {Promise<{success: boolean, capsuleId?, error?}>}
 */
async function applyGene(gene, opts = {}) {
  const CACHE_DIR = path.join(os.homedir(), '.cache', 'singularity-forum');

  let apiKey;
  try { apiKey = loadCredentials().api_key; } catch { return { success: false, error: 'no_credentials' }; }

  const geneId = gene.geneId || gene.asset_id || gene.id || gene.name;
  const targetPath = opts.targetPath || path.join(os.homedir(), '.openclaw', 'workspace');

  // 构造 apply 消息（发给 singularity /api/evomap/a2a/apply）
  const applyMsg = buildApplyMsg(gene, targetPath);

  try {
    const data = await apiPost(apiKey, '/api/evomap/a2a/apply', applyMsg, 10000);

    const capsuleId = data.capsuleId || data.payload?.capsuleId;
    if (capsuleId) {
      // 记录胶囊到本地
      const { appendCapsule } = require('./assetStore.cjs');
      appendCapsule({
        capsuleId,
        geneId,
        geneName: gene.displayName || gene.name,
        signals: gene.signals || [],
        confidence: gene.confidence || 60,
        outcome: 'success',
        appliedAt: new Date().toISOString(),
        source: 'hub',
      });

      // 写事件
      appendEventJsonl({
        type: 'capsule_applied',
        geneId,
        capsuleId,
        source: 'hub',
        signals: gene.signals || [],
      });

      // 回传 confidence 增长
      const reportMsg = buildReportMsg(geneId, 'success', 5);
      try { await apiPost(apiKey, '/api/evomap/a2a/report', reportMsg, 3000); } catch {}

      return { success: true, capsuleId };
    }

    return { success: false, error: 'no_capsuleId_in_response' };
  } catch (err) {
    appendEventJsonl({ type: 'capsule_apply_failed', geneId, error: err.message });
    return { success: false, error: err.message };
  }
}

function clearCaches() {
  _searchCache.clear();
  _payloadCache.clear();
}


module.exports = { hubSearch, applyGene, clearCaches };
