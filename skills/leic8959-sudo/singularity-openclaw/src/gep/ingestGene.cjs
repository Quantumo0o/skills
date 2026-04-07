/**
 * singularity Gene Ingestion
 * 将 Hub Gene 引入本地闭环
 *
 * 三个步骤：
 * 1. upsertGene — 写入 assets/gep/genes.json
 * 2. updateMemory — 追加到 memory/ 信号日志
 * 3. scheduleApply — 决定是否立即 apply
 */

const fs = require('fs');
const path = require('path');
const os = require('os');


const { upsertGene }      = require('./assetStore.cjs');
const { recordHubCapsule } = require('./capsuleRecorder.cjs');
const { hubSearch }       = require('./hubSearch.cjs');

// singularity skill 本地路径
const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const ASSETS_DIR = path.join(os.homedir(), '.cache', 'singularity-forum', 'assets');

// ---------------------------------------------------------------------------
// Gene 字段标准化（抹平 Hub 返回格式差异）
// ---------------------------------------------------------------------------

function normalizeGene(raw) {
  return {
    id:       raw.geneId || raw.asset_id || raw.id || raw.name || ('gene_' + Date.now()),
    name:     raw.name   || raw.geneName  || raw.displayName || 'unknown',
    displayName: raw.displayName || raw.geneName || raw.name || 'unknown',
    description: raw.description || raw.summary || '',
    category: (raw.category || 'REPAIR').toUpperCase(),
    signals:  Array.isArray(raw.signals) ? raw.signals
              : typeof raw.signals === 'string' ? raw.signals.split(',').map(s => s.trim())
              : [],
    strategy: raw.strategy || raw.payload?.strategy || {},
    algorithm: raw.strategy?.algorithm || raw.algorithm || '',
    confidence: Number(raw.confidence) || 60,
    reputation: Number(raw.reputation_score || raw.reputation) || 50,
    success_streak: Number(raw.success_streak || raw.successStreak) || 0,
    usageCount: Number(raw.usageCount || raw.usage_count || 0),
    source:   'hub',
    sourceNodeId: raw.source_node_id || raw.nodeId || null,
    chainId:  raw.chain_id || raw.chainId || null,
    ingestedAt: new Date().toISOString(),
    version:  raw.version || '1.0.0',
    gdiScore: Number(raw.gdiScore || raw.gdi_score || 70),
    // 标记来自 Hub，用于后续 distinguish local vs hub
    _fromHub: true,
  };
}

// ---------------------------------------------------------------------------
// Ingest：写入本地 gene 库
// ---------------------------------------------------------------------------

/**
 * 将 Hub 基因写入本地资产库
 * @param {object} hubGene - hubSearch 返回的 match
 * @returns {object} 标准化后的 gene
 */
function ingestGene(hubGene) {
  const gene = normalizeGene(hubGene);

  // 写入 assets/gep/genes.json（去重：同 name 覆盖）
  upsertGene(gene);

  // 写 memory 日志
  _appendToMemoryLog(gene);

  // 写事件
  const { appendEventJsonl } = require('./assetStore.cjs');
  appendEventJsonl({
    type: 'gene_ingested',
    geneId: gene.id,
    geneName: gene.name,
    signal: gene.signals[0] || '',
    source: 'hub',
    confidence: gene.confidence,
    ingestedAt: gene.ingestedAt,
  });

  console.log(`[Ingest] ${gene.displayName} (signal=${gene.signals[0]}, conf=${gene.confidence})`);
  return gene;
}

// ---------------------------------------------------------------------------
// Ingest 多个基因
// ---------------------------------------------------------------------------

/**
 * 批量 ingest 基因，返回成功数
 */
function ingestGenes(hubGenes) {
  if (!Array.isArray(hubGenes)) return 0;
  let count = 0;
  for (const g of hubGenes) {
    try { ingestGene(g); count++; } catch (e) { console.log(`[Ingest] Skip ${g.name}: ${e.message}`); }
  }
  return count;
}

// ---------------------------------------------------------------------------
// Check：是否需要 ingest（已有则跳过）
// ---------------------------------------------------------------------------

/**
 * 检查某信号是否已在本地有足够好的基因
 */
function hasLocalGene(signal, minConfidence = 60) {
  try {
    const { loadGenes } = require('./assetStore.cjs');
    const genes = loadGenes();
    return genes.some(g =>
      g.source === 'local' &&
      g.signals &&
      (g.signals.includes(signal) || signal.includes(g.signals[0])) &&
      (g.confidence || 0) >= minConfidence
    );
  } catch { return false; }
}

// ---------------------------------------------------------------------------
// memory 日志
// ---------------------------------------------------------------------------

function _todayMemoryFile() {
  if (!fs.existsSync(MEMORY_DIR)) return null;
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const candidates = [
    path.join(MEMORY_DIR, today + '.md'),
    path.join(MEMORY_DIR, 'recent.md'),
    path.join(MEMORY_DIR, 'signals.md'),
  ];
  for (const fp of candidates) { if (fs.existsSync(fp)) return fp; }
  return candidates[0]; // fallback：写在今天文件里
}

function _appendToMemoryLog(gene) {
  try {
    const fp = _todayMemoryFile();
    if (!fp) return;
    const entry = `\n## [Ingest] Gene: ${gene.displayName} (${gene.category})\n` +
      `- Signal: ${gene.signals.join(', ') || 'unknown'}\n` +
      `- Confidence: ${gene.confidence} (from Hub, source=${gene.sourceNodeId || 'singularity.mba'})\n` +
      `- Algorithm: ${gene.algorithm || gene.strategy?.algorithm || 'N/A'}\n` +
      `- Ingested: ${gene.ingestedAt}\n` +
      `- Description: ${gene.description}\n`;
    fs.appendFileSync(fp, entry, 'utf-8');
  } catch { /* non-critical */ }
}

module.exports = { ingestGene, ingestGenes, hasLocalGene };
