/**
 * singularity-forum - Gene Selector（对标 evolver selector.js）
 *
 * 两种评分算法并行，选出最优 Gene：
 * 1. 精确匹配：signals_match 数组交集
 * 2. 语义相似度：TF-IDF 余弦相似度（bag-of-words），权重 0.4
 *
 * 最终得分 = exact_score * 0.6 + semantic_score * 0.4
 */
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';
import { loadCredentials } from '../../lib/api.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ASSETS_DIR = path.join(os.homedir(), '.cache', 'singularity-forum', 'assets');
const GENES_FILE = path.join(ASSETS_DIR, 'genes.json');
const CAPSULES_FILE = path.join(ASSETS_DIR, 'capsules.json');

// =============================================================================
// 语义相似度：Bag-of-Words TF-IDF + 余弦相似度
// =============================================================================

const SEMANTIC_WEIGHT = 0.4;
const EXACT_WEIGHT = 0.6;
const STOP_WORDS = new Set([
  'the', 'and', 'for', 'with', 'from', 'that', 'this', 'into', 'when',
  'are', 'was', 'has', 'had', 'not', 'but', 'its', 'can', 'will', 'all',
  'any', 'use', 'may', 'also', 'should', 'would', 'could', 'from', 'into',
]);

function tokenize(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9_\-]+/g, ' ')
    .split(/\s+/)
    .filter(w => w.length >= 2 && !STOP_WORDS.has(w));
}

function buildTermFrequency(tokens) {
  const tf = {};
  for (const t of tokens) tf[t] = (tf[t] || 0) + 1;
  return tf;
}

function cosineSimilarity(tfA, tfB) {
  const keys = new Set([...Object.keys(tfA), ...Object.keys(tfB)]);
  let dotProduct = 0, normA = 0, normB = 0;
  for (const k of keys) {
    const a = tfA[k] || 0, b = tfB[k] || 0;
    dotProduct += a * b;
    normA += a * a;
    normB += b * b;
  }
  if (normA === 0 || normB === 0) return 0;
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

function tokenizeGene(gene) {
  const tokens = [];
  if (Array.isArray(gene.signals_match)) tokens.push(...gene.signals_match);
  if (Array.isArray(gene.signals)) tokens.push(...gene.signals);
  if (gene.summary) tokens.push(gene.summary);
  if (gene.description) tokens.push(gene.description);
  if (gene.displayName) tokens.push(gene.displayName);
  if (gene.name) tokens.push(gene.name);
  return tokenize(tokens.join(' '));
}

/** 语义相似度：signals 文本 vs 单个 gene */
function semanticScore(signals, gene) {
  const signalTokens = tokenize(signals.join(' '));
  if (signalTokens.length === 0) return 0;
  const geneTokens = tokenizeGene(gene);
  if (geneTokens.length === 0) return 0;
  return cosineSimilarity(buildTermFrequency(signalTokens), buildTermFrequency(geneTokens));
}

// =============================================================================
// 精确匹配
// =============================================================================

/**
 * 判断 gene.signals_match 是否与 signals 有交集
 * 支持：
 *   - 普通字符串：substring 包含
 *   - 正则表达式：/pattern/flags
 *   - 多语言别名：en_term|zh_term|ja_term
 */
function matchPatternToSignal(pattern, signal) {
  const p = String(pattern || '');
  const s = String(signal || '').toLowerCase();

  // Regex: /body/flags
  if (p.length >= 2 && p.startsWith('/') && p.indexOf('/', 1) > 0) {
    try {
      const lastSlash = p.lastIndexOf('/');
      const body = p.slice(1, lastSlash);
      const flags = p.slice(lastSlash + 1);
      return new RegExp(body, flags || 'i').test(s);
    } catch {}
  }

  // Multi-language alias: "en|zh|ja"
  if (p.includes('|')) {
    return p.split('|').some(b => s.includes(b.trim().toLowerCase()));
  }

  return s.includes(p.toLowerCase());
}

function exactMatchScore(signals, gene) {
  const geneSignals = gene.signals_match || gene.signals || [];
  if (!geneSignals.length) {
    // fallback: 用 name/displayName/description 做模糊匹配
    const text = [gene.name, gene.displayName, gene.description].filter(Boolean).join(' ');
    if (!text || !signals.length) return 0;
    const sig = signals[0]?.toLowerCase() || '';
    return sig.length > 3 && text.toLowerCase().includes(sig) ? 0.5 : 0;
  }
  const hits = geneSignals.filter(gs => signals.some(s => matchPatternToSignal(gs, s)));
  return hits.length / geneSignals.length;
}

// =============================================================================
// Signal 扩展（对标 evolver learningSignals.js）
// =============================================================================

const OPPORTUNITY_SIGNALS = new Set([
  'user_feature_request', 'user_improvement_suggestion', 'perf_bottleneck',
  'capability_gap', 'stable_success_plateau', 'external_opportunity',
  'empty_cycle_loop_detected', 'issue_already_resolved', 'openclaw_self_healed',
]);

function hasOpportunitySignal(signals) {
  return signals.some(s => {
    const str = String(s).toLowerCase();
    return OPPORTUNITY_SIGNALS.has(str) ||
      [...OPPORTUNITY_SIGNALS].some(os => str.startsWith(os + ':'));
  });
}

function hasErrorSignal(signals) {
  return signals.some(s => {
    const str = String(s).toLowerCase();
    return str.includes('error') || str.includes('exception') || str.includes('failed') ||
      str.includes('log_error') || str.includes('unstable') || str.includes('runtime');
  });
}

export function expandSignals(signals) {
  const tags = [];
  const raw = signals.map(s => String(s));

  for (const s of raw) {
    tags.push(s);
    const base = s.split(':')[0];
    if (base && base !== s) tags.push(base);
  }

  const text = raw.join(' ').toLowerCase();

  if (/(error|exception|failed|unstable|log_error|runtime|429)/.test(text)) {
    tags.push('problem:reliability', 'action:repair');
  }
  if (/(protocol|prompt|audit|drift|schema)/.test(text)) {
    tags.push('problem:protocol', 'action:optimize', 'area:prompt');
  }
  if (/(perf|performance|bottleneck|latency|slow|throughput)/.test(text)) {
    tags.push('problem:performance', 'action:optimize');
  }
  if (/(feature|capability_gap|user_feature_request|external_opportunity)/.test(text)) {
    tags.push('problem:capability', 'action:innovate');
  }
  if (/(stagnation|plateau|steady_state|saturation|empty_cycle|recurring)/.test(text)) {
    tags.push('problem:stagnation', 'action:innovate');
  }
  if (/(task|worker|heartbeat|hub|orchestration)/.test(text)) {
    tags.push('area:orchestration');
  }
  if (/(memory|narrative|reflection)/.test(text)) {
    tags.push('area:memory');
  }
  if (/(validation|canary|rollback|constraint|blast)/.test(text)) {
    tags.push('risk:validation');
  }

  return [...new Set(tags)];
}

function signalTagScore(signals, gene) {
  const tags = new Set(expandSignals(signals));
  const geneTags = new Set([
    ...(gene.signals_match || []),
    ...(gene.signals || []),
    'category:' + (gene.category || ''),
  ].filter(Boolean));

  if (tags.size === 0 || geneTags.size === 0) return 0;
  let hits = 0;
  for (const t of tags) if (geneTags.has(t)) hits++;
  return hits / Math.max(tags.size, geneTags.size);
}

// =============================================================================
// Gene 评分 + 选择（主函数）
// =============================================================================

/**
 * 从本地基因库中选出最匹配的 Gene
 * @param {string[]} signals - 当前错误信号列表
 * @param {string} category - 期望类别 repair/optimize/innovate
 * @param {object} options - { minScore: 0.3, maxResults: 3 }
 * @returns {object[]} 排序后的 Gene 列表（附评分）
 */
export function selectGenes(signals, category = null, options = {}) {
  const { minScore = 0.0, maxResults = 3 } = options;
  const genes = loadLocalGenes();

  if (!genes.length) return [];

  const scores = genes
    .filter(g => {
      if (!category) return true;
      return g.category === category ||
        (category === 'optimize' && !g.category) ||
        (category === 'repair' && g.category === 'REPAIR');
    })
    .map(gene => {
      const exact = exactMatchScore(signals, gene);
      const semantic = semanticScore(signals, gene);
      const tagScore = signalTagScore(signals, gene);
      const finalScore = exact * EXACT_WEIGHT + semantic * SEMANTIC_WEIGHT + tagScore * 0.0; // tag 辅助，不独立计分

      return {
        gene,
        exact,
        semantic,
        finalScore,
        selected: false,
      };
    })
    .filter(r => r.finalScore >= minScore)
    .sort((a, b) => b.finalScore - a.finalScore)
    .slice(0, maxResults);

  if (scores.length > 0) scores[0].selected = true;
  return scores;
}

/**
 * 根据 signals 判断应选择哪种 category
 */
export function inferCategory(signals) {
  if (hasErrorSignal(signals)) return 'repair';
  if (hasOpportunitySignal(signals)) return 'innovate';
  return 'optimize';
}

// =============================================================================
// 本地 Gene 资产库管理
// =============================================================================

function ensureAssetsDir() {
  if (!fs.existsSync(ASSETS_DIR)) fs.mkdirSync(ASSETS_DIR, { recursive: true });
}

export function loadLocalGenes() {
  ensureAssetsDir();
  if (!fs.existsSync(GENES_FILE)) return [];
  try { return JSON.parse(fs.readFileSync(GENES_FILE, 'utf-8')); } catch { return []; }
}

export function saveLocalGenes(genes) {
  ensureAssetsDir();
  fs.writeFileSync(GENES_FILE, JSON.stringify(genes, null, 2), 'utf-8');
}

/** 追加 gene 到本地资产库（发布成功后调用） */
export function addLocalGene(gene) {
  const genes = loadLocalGenes();
  const exists = genes.find(g => g.id === gene.id || g.name === gene.name);
  if (!exists) {
    genes.push({ ...gene, addedAt: new Date().toISOString() });
    saveLocalGenes(genes);
  }
  return genes;
}

export function loadLocalCapsules() {
  ensureAssetsDir();
  if (!fs.existsSync(CAPSULES_FILE)) return [];
  try { return JSON.parse(fs.readFileSync(CAPSULES_FILE, 'utf-8')); } catch { return []; }
}

export function saveLocalCapsules(capsules) {
  ensureAssetsDir();
  fs.writeFileSync(CAPSULES_FILE, JSON.stringify(capsules, null, 2), 'utf-8');
}

/** 根据 signals 从本地 capsules 中选最优 */
export function selectCapsules(signals, options = {}) {
  const { minScore = 0.2, maxResults = 3 } = options;
  const capsules = loadLocalCapsules();
  if (!capsules.length) return [];

  return capsules
    .map(cap => {
      const semantic = semanticScore(signals, cap);
      return { capsule: cap, semantic, selected: false };
    })
    .filter(r => r.semantic >= minScore)
    .sort((a, b) => b.semantic - a.semantic)
    .slice(0, maxResults);
}
