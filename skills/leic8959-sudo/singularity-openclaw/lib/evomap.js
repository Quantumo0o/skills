/**
 * singularity-forum - EvoMap 同步模块
 */
import { loadCredentials, fetchGenes, fetchCapsules, fetchStats, a2aFetch, a2aReport, a2aApply,
         loadGeneCache, saveGeneCache, loadSyncState, saveSyncState, updateSyncTime, log } from './api.js';

export async function pullGenes(sinceDays = 7) {
  const start = Date.now();
  const errors = [];
  let cred;
  try { cred = loadCredentials(); } catch { return { pulled: 0, pushed: 0, errors: ['凭证未配置'], duration: Date.now() - start }; }

  const syncState = loadSyncState();
  let since;
  if (syncState.lastGeneSync) { since = syncState.lastGeneSync; }
  else { const d = new Date(); d.setDate(d.getDate() - sinceDays); since = d.toISOString(); }

  try {
    const allGenes = [];
    let offset = 0, limit = 50, hasMore = true;
    while (hasMore) {
      const resp = await fetchGenes(cred.api_key, { since, limit, offset });
      allGenes.push(...resp.genes);
      offset += resp.genes.length;
      hasMore = resp.genes.length === limit;
    }
    if (allGenes.length === 0) { updateSyncTime('lastGeneSync'); return { pulled: 0, pushed: 0, errors: [], duration: Date.now() - start }; }

    const oldCache = loadGeneCache();
    const existingMap = new Map((oldCache?.genes || []).map(g => [g.id, g]));
    for (const gene of allGenes) existingMap.set(gene.id, gene);
    const merged = Array.from(existingMap.values());
    saveGeneCache({ genes: merged, lastUpdated: new Date().toISOString() });
    updateSyncTime('lastGeneSync');

    log('INFO', 'pullGenes', '同步完成：新增 ' + allGenes.length + '，缓存共 ' + merged.length + ' 个 Gene');
    return { pulled: allGenes.length, pushed: 0, errors, duration: Date.now() - start };
  } catch (err) { errors.push('拉取 Gene 失败：' + err.message); return { pulled: 0, pushed: 0, errors, duration: Date.now() - start }; }
}

export function getLocalGenes() { const cache = loadGeneCache(); return cache?.genes || []; }

export function matchGenes(taskType, signals) {
  const genes = getLocalGenes();
  const signalSet = new Set(signals);
  return genes.filter(g => g.taskType === taskType)
    .map(g => ({ gene: g, score: new Set(g.signals || []).size > 0 ? [...signalSet].filter(s => new Set(g.signals || []).has(s)).length / new Set(g.signals || []).size : 0 }))
    .filter(x => x.score >= 0.1).sort((a, b) => b.score - a.score).map(x => x.gene);
}

export async function reportCapsule(params) {
  let cred;
  try { cred = loadCredentials(); } catch { return { success: false, error: '凭证未配置' }; }
  try {
    // A2A 上报需要 nodeId + nodeSecret（不支持纯 API Key）
    const nodeId = cred.openclaw_agent_id || 'main';
    const nodeSecret = cred.openclaw_token || process.env.SINGULARITY_NODE_SECRET;
    if (!nodeSecret) {
      log('WARN', 'reportCapsule', 'openclaw_token 未配置，A2A 上报跳过');
      return { success: false, error: 'openclaw_token 未配置' };
    }
    await a2aReport(nodeId, nodeSecret, {
      capsule_id: params.capsuleId,
      outcome: params.outcome,
      execution_time_ms: params.executionTimeMs,
    });
    log('INFO', 'reportCapsule', '已上报 capsule=' + params.capsuleId + ' outcome=' + params.outcome);
    return { success: true };
  } catch (err) { log('ERROR', 'reportCapsule', err.message); return { success: false, error: err.message }; }
}

export async function hubFetch(params) {
  let cred;
  try { cred = loadCredentials(); } catch { return { assets: [], error: '凭证未配置' }; }
  try {
    const resp = await a2aFetch(cred.api_key, { signals: params.signals, task_type: params.taskType, min_confidence: params.minConfidence ?? 0.5 });
    log('INFO', 'hubFetch', '找到 ' + (resp.assets?.length || 0) + ' 个匹配资源');
    return { assets: resp.assets || [] };
  } catch (err) { log('ERROR', 'hubFetch', err.message); return { assets: [], error: err.message }; }
}

export async function hubApply(capsuleId) {
  let cred;
  try { cred = loadCredentials(); } catch { return { success: false, error: '凭证未配置' }; }
  try {
    const nodeId = cred.openclaw_agent_id || 'main';
    const nodeSecret = cred.openclaw_token || process.env.SINGULARITY_NODE_SECRET;
    if (!nodeSecret) {
      log('WARN', 'hubApply', 'openclaw_token 未配置，Hub Apply 跳过');
      return { success: false, error: 'openclaw_token 未配置' };
    }
    await a2aApply(nodeId, nodeSecret, { capsule_id: capsuleId, agent_id: cred.openclaw_agent_id || 'main' });
    log('INFO', 'hubApply', '成功应用 capsule=' + capsuleId);
    return { success: true };
  } catch (err) { log('ERROR', 'hubApply', err.message); return { success: false, error: err.message }; }
}

export async function getStats(period = 'month') {
  let cred;
  try { cred = loadCredentials(); } catch { return null; }
  try { return await fetchStats(cred.api_key, period); } catch { return null; }
}

export async function fullSync() {
  const start = Date.now();
  const geneResult = await pullGenes(7);
  const stats = await getStats('month');
  if (stats) log('INFO', 'fullSync', '统计：' + stats.myGenes.total + ' 个基因，' + stats.appliedGenes.total + ' 次应用');
  return { pulled: geneResult.pulled, pushed: geneResult.pushed, errors: geneResult.errors, duration: Date.now() - start };
}

export function printGeneSummary() {
  const genes = getLocalGenes();
  if (genes.length === 0) { console.log('本地 Gene 缓存为空（请先运行同步）'); return; }
  const cache = loadGeneCache();
  console.log('\n=== Gene 缓存摘要（共 ' + genes.length + ' 个）===\n最后更新：' + (cache?.lastUpdated || '未知') + '\n');
  const byCategory = {};
  for (const g of genes) byCategory[g.category] = (byCategory[g.category] || 0) + 1;
  console.log('按类别：'); for (const [c, n] of Object.entries(byCategory)) console.log('  ' + c + ': ' + n);
  const top = [...genes].sort((a, b) => b.gdiScore - a.gdiScore).slice(0, 5);
  console.log('\nTop 5（GDI）：'); for (const g of top) console.log('  [' + g.gdiScore + '] ' + g.displayName + ' (' + g.taskType + ')');
  console.log('');
}
