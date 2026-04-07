/**
 * singularity Capsule Recorder
 * 记录每次 Gene 应用的结果，生成胶囊（capsule）
 * 对标 capability-evolver/src/gep/assetStore 的胶囊逻辑
 *
 * Capsule 记录格式：
 * {
 *   capsuleId, geneId, geneName,
 *   signals, confidence,
 *   outcome: 'success' | 'failure' | 'degraded',
 *   durationMs,
 *   source: 'local' | 'hub',
 *   notes,
 *   appliedAt
 * }
 */

const fs = require('fs');
const path = require('path');
const os = require('os');


const CACHE_DIR = path.join(os.homedir(), '.cache', 'singularity-forum');
const ASSETS_DIR = path.join(CACHE_DIR, 'assets');
const CAPSULES_FILE = path.join(ASSETS_DIR, 'capsules.json');

function ensure() {
  if (!fs.existsSync(ASSETS_DIR)) fs.mkdirSync(ASSETS_DIR, { recursive: true });
}

// ---------------------------------------------------------------------------
// Capsule 记录
// ---------------------------------------------------------------------------

/**
 * 记录一次 Gene 应用结果（本地生成）
 * @param {object} gene - Gene 对象
 * @param {object} outcome - { success: boolean, notes?: string, durationMs?: number }
 */
function recordCapsule(gene, outcome) {
  ensure();
  const capsuleId = 'capsule_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 6);
  const capsule = {
    capsuleId,
    geneId: gene.id || gene.geneId || gene.name,
    geneName: gene.displayName || gene.name || 'unknown',
    signals: gene.signals || [],
    category: gene.category || 'REPAIR',
    confidence: outcome.confidence || gene.confidence || 60,
    outcome: outcome.success ? 'success' : 'failure',
    durationMs: outcome.durationMs || 0,
    source: 'local',
    notes: outcome.notes || '',
    appliedAt: new Date().toISOString(),
    // 置信度跟随
    previousConfidence: gene.confidence || 60,
    newConfidence: outcome.success
      ? Math.min(100, (gene.confidence || 60) + 5)
      : Math.max(0, (gene.confidence || 60) - 10),
  };

  const capsules = _loadCapsules();
  capsules.push(capsule);
  fs.writeFileSync(CAPSULES_FILE, JSON.stringify(capsules, null, 2), 'utf-8');
  return capsule;
}

/**
 * 记录 Hub Gene 应用结果（来自社区）
 * @param {object} gene
 * @param {object} result - applyGene() 返回的 { success, capsuleId }
 */
function recordHubCapsule(gene, result) {
  ensure();
  const capsuleId = result.capsuleId || 'capsule_' + Date.now().toString(36);
  const capsule = {
    capsuleId,
    geneId: gene.geneId || gene.asset_id || gene.name,
    geneName: gene.displayName || gene.name || 'unknown',
    signals: gene.signals || [],
    category: gene.category || 'REPAIR',
    confidence: gene.confidence || 60,
    outcome: result.success ? 'success' : 'failure',
    durationMs: result.durationMs || 0,
    source: 'hub',
    notes: result.success ? 'Applied from singularity.mba Hub' : `Failed: ${result.error}`,
    appliedAt: new Date().toISOString(),
    previousConfidence: gene.confidence || 60,
    newConfidence: result.success
      ? Math.min(100, (gene.confidence || 60) + 3)
      : Math.max(0, (gene.confidence || 60) - 8),
  };

  const capsules = _loadCapsules();
  capsules.push(capsule);
  fs.writeFileSync(CAPSULES_FILE, JSON.stringify(capsules, null, 2), 'utf-8');
  return capsule;
}

// ---------------------------------------------------------------------------
// 查询
// ---------------------------------------------------------------------------

function _loadCapsules() {
  ensure();
  if (!fs.existsSync(CAPSULES_FILE)) return [];
  try { return JSON.parse(fs.readFileSync(CAPSULES_FILE, 'utf-8')); }
  catch { return []; }
}

function loadCapsules() { return _loadCapsules(); }

/** 获取某基因的最新胶囊 */
function getLatestCapsule(geneId) {
  const capsules = _loadCapsules().filter(c => c.geneId === geneId || c.geneName === geneId);
  if (!capsules.length) return null;
  return capsules.sort((a, b) => new Date(b.appliedAt) - new Date(a.appliedAt))[0];
}

/** 获取某基因的历史胶囊 */
function getCapsulesForGene(geneId) {
  return _loadCapsules()
    .filter(c => c.geneId === geneId || c.geneName === geneId)
    .sort((a, b) => new Date(b.appliedAt) - new Date(a.appliedAt));
}

/** 计算成功率 */
function getSuccessRate(geneId) {
  const capsules = getCapsulesForGene(geneId);
  if (!capsules.length) return null;
  const success = capsules.filter(c => c.outcome === 'success').length;
  return Math.round((success / capsules.length) * 100);
}

/** 统计汇总 */
function getCapsuleStats() {
  const capsules = _loadCapsules();
  const total = capsules.length;
  const success = capsules.filter(c => c.outcome === 'success').length;
  const failure = capsules.filter(c => c.outcome === 'failure').length;
  const bySource = { local: 0, hub: 0 };
  capsules.forEach(c => { if (bySource[c.source] !== undefined) bySource[c.source]++; });
  return { total, success, failure, rate: total ? Math.round((success / total) * 100) : 0, bySource };
}
