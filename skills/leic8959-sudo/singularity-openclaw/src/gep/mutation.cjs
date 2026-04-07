/**
 * singularity-forum - Gene Mutation 对象（对标 evolver mutation.js）
 *
 * 每个 Gene 发布都对应一个结构化 Mutation 记录：
 * - 发布前：描述预期效果
 * - 发布后：填充实际结果
 * - 闭环：actual_outcome → verdict → 下一次选择的依据
 */
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';
import { loadCredentials } from '../../lib/api.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MUTATION_DB = path.join(os.homedir(), '.cache', 'singularity-forum', 'mutation-db.jsonl');

function ensureDir() {
  const dir = path.dirname(MUTATION_DB);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function nowISO() { return new Date().toISOString(); }

// =============================================================================
// Mutation 对象结构
// =============================================================================

export function createMutation({ geneId, geneName, signal, category, changeDescription, changeType, blastRadius, validationMethod, preConditions, expectedOutcome, selectedGene }) {
  return {
    id: 'mut_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7),
    gene_id: geneId || null,
    gene_name: geneName,
    signal,
    category,                          // 'repair' | 'optimize' | 'innovate'
    type: changeType || 'strategy_modification',
    change_description: changeDescription,
    blast_radius: blastRadius || 'local_only',
    validation_method: validationMethod || 'observation',
    pre_conditions: preConditions || [],
    expected_outcome: expectedOutcome || '',
    actual_outcome: null,
    outcome_verdict: null,            // 'success' | 'partial' | 'failed' | null
    selected_gene_id: selectedGene?.id || null,
    selected_gene_name: selectedGene?.displayName || null,
    created_at: nowISO(),
    published_at: null,
    outcome_recorded_at: null,
    status: 'pending',               // 'pending' | 'published' | 'verified' | 'rejected'
  };
}

// =============================================================================
// Mutation 生命周期
// =============================================================================

/** 追加 mutation 记录（publish 前） */
export function appendMutation(mutation) {
  ensureDir();
  const line = JSON.stringify(mutation) + '\n';
  fs.appendFileSync(MUTATION_DB, line, 'utf-8');
  return mutation;
}

/** 标记 mutation 为已发布 */
export function markPublished(mutationId, geneId) {
  const mutations = loadMutations();
  const idx = mutations.findIndex(m => m.id === mutationId);
  if (idx >= 0) {
    mutations[idx].status = 'published';
    mutations[idx].published_at = nowISO();
    if (geneId) mutations[idx].gene_id = geneId;
    saveMutations(mutations);
  }
}

/** 记录实际结果（outcome），发布后调用 */
export function recordOutcome(mutationId, actualOutcome, verdict) {
  const mutations = loadMutations();
  const idx = mutations.findIndex(m => m.id === mutationId);
  if (idx >= 0) {
    mutations[idx].actual_outcome = actualOutcome;
    mutations[idx].outcome_verdict = verdict; // 'success' | 'partial' | 'failed'
    mutations[idx].outcome_recorded_at = nowISO();
    mutations[idx].status = verdict === 'success' ? 'verified' : verdict === 'partial' ? 'published' : 'rejected';
    saveMutations(mutations);
  }
}

/** 获取最近的 mutation */
export function getRecentMutations(limit = 20) {
  return loadMutations().slice(-limit);
}

/** 获取某 signal 的历史 mutation（用于判断是否要再次发布） */
export function getMutationHistory(signal, limit = 5) {
  const all = loadMutations();
  return all.filter(m => m.signal === signal).slice(-limit);
}

/** 判断某 signal 是否最近验证失败（避免重复发布失败策略） */
export function wasRecentlyRejected(signal, maxAgeMs = 24 * 3600000) {
  const history = getMutationHistory(signal, 10);
  const cutoff = Date.now() - maxAgeMs;
  return history.some(m =>
    m.signal === signal &&
    m.outcome_verdict === 'failed' &&
    m.outcome_recorded_at &&
    new Date(m.outcome_recorded_at).getTime() > cutoff
  );
}

// =============================================================================
// Outcome 报告（供外部调用：发布后告知实际效果）
// =============================================================================

/**
 * 向论坛报告 Gene 应用效果（如果 API 支持）
 */
export async function reportOutcomeToHub(geneId, outcome) {
  try {
    const cred = loadCredentials();
    const resp = await fetch('https://singularity.mba/api/evolution/mutations', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + cred.forum_api_key, 'Content-Type': 'application/json' },
      body: JSON.stringify({ gene_id: geneId, outcome }),
    });
    return { success: resp.ok };
  } catch { return { success: false }; }
}

// =============================================================================
// Change Description 生成（对标 evolver）
// =============================================================================

/**
 * 根据错误 signal 和选中的 Gene 生成人类可读的变更描述
 */
export function generateChangeDescription(signal, gene, category) {
  const descriptions = {
    network_timeout: '将网络请求从单次失败改为指数退避重试策略（base=1s, max=30s, factor=2）',
    json_parse_error: 'JSON 解析增加 try-catch 容错，解析失败时返回空数组而非抛出异常',
    auth_failure: '认证失败后清除缓存 Token 并重试一次，仍失败则返回友好错误',
    rate_limit: '检测到 429 响应后读取 Retry-After 头，等待冷却时间后再重试',
    module_not_found: '模块加载失败时使用内联实现作为降级方案',
    file_not_found: '文件不存在时尝试常见路径变体，返回清晰错误而非 ENOENT',
    encoding_error: '强制使用 UTF-8 解码，对中文路径特殊处理',
    repeated_failure: '同一任务失败 3 次后启用熔断器，返回缓存结果',
    null_reference: '添加防御性空值检查，提供 undefined 时的默认值',
    memory_leak: '添加资源清理逻辑，对长时间运行任务设置内存上限',
  };
  const base = descriptions[signal] || '优化策略以提高稳定性';
  return category === 'innovate'
    ? '[创新] 探索新策略组合: ' + base
    : category === 'optimize'
    ? '[优化] 改进现有策略: ' + base
    : '[修复] ' + base;
}

// =============================================================================
// 数据库读写
// =============================================================================

function loadMutations() {
  ensureDir();
  if (!fs.existsSync(MUTATION_DB)) return [];
  try {
    return fs.readFileSync(MUTATION_DB, 'utf-8')
      .split('\n').filter(Boolean)
      .map(line => JSON.parse(line));
  } catch { return []; }
}

function saveMutations(mutations) {
  ensureDir();
  fs.writeFileSync(MUTATION_DB, mutations.map(m => JSON.stringify(m)).join('\n') + '\n', 'utf-8');
}
