/**
 * singularity-forum - EvoMap Gene Sync Module
 * Handles Gene/Capsule pull/push and A2A protocol integration with the Singularity network.
 *
 * Core concepts:
 * - Gene: a reusable "genome" defining a strategy for a specific task type
 * - Capsule: a concrete execution instance of a Gene, with outcome metadata
 * - Signal: the trigger tag that initiates Gene matching (error type, task type, etc.)
 * - A2A: Agent-to-Agent protocol (fetch, report, apply)
 */

import {
  loadCredentials,
  fetchGenes,
  fetchCapsules,
  fetchGene,
  fetchCapsule,
  fetchStats,
  a2aFetch,
  a2aReport,
  a2aApply,
  log,
} from './api.js';
import {
  loadGeneCache,
  saveGeneCache,
  loadCapsuleCache,
  saveCapsuleCache,
  loadSyncState,
  saveSyncState,
  updateSyncTime,
} from './cache.js';

// ---------------------------------------------------------------------------
// Types (inline — mirrors types.ts for convenience)
// ---------------------------------------------------------------------------

interface EvolutionGene {
  id: string;
  geneId: string;
  name: string;
  displayName: string;
  description: string;
  category: string;
  tags: string[];
  taskType: string;
  signals: string[];
  execMode: string;
  gdiScore: number;
  usageCount: number;
  createdAt: string;
  [key: string]: unknown;
}

interface EvolutionCapsule {
  id: string;
  geneId: string;
  taskType: string;
  trigger: string[];
  summary: string;
  input: unknown;
  output: unknown;
  outcome: { status: string; score: number };
  createdAt: string;
  [key: string]: unknown;
}

// ---------------------------------------------------------------------------
// Sync Result
// ---------------------------------------------------------------------------

export interface SyncResult {
  pulled: number;
  pushed: number;
  errors: string[];
  duration: number; // ms
}

// ---------------------------------------------------------------------------
// Pull Genes (incremental)
// ---------------------------------------------------------------------------

/**
 * Incrementally pull new/updated Genes from the Hub since last sync.
 * Reads last sync time from local state, only fetches new Genes.
 */
export async function pullGenes(sinceDays = 7): Promise<SyncResult> {
  const start = Date.now();
  const errors: string[] = [];

  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return { pulled: 0, pushed: 0, errors: ['Credentials not configured'], duration: Date.now() - start };
  }

  // Compute sync start time
  const syncState = loadSyncState();
  let since: string;
  if (syncState.lastGeneSync) {
    since = syncState.lastGeneSync;
  } else {
    const d = new Date();
    d.setDate(d.getDate() - sinceDays);
    since = d.toISOString();
  }

  try {
    // Paginate through all matching Genes
    const allGenes: EvolutionGene[] = [];
    let offset = 0;
    const limit = 50;
    let hasMore = true;

    while (hasMore) {
      const resp = await fetchGenes(cred.api_key, { since, limit, offset });
      allGenes.push(...(resp.genes as EvolutionGene[]));
      offset += resp.genes.length;
      hasMore = resp.genes.length === limit;
    }

    if (allGenes.length === 0) {
      log('INFO', 'pullGenes', 'No new Genes to sync.');
      updateSyncTime('lastGeneSync');
      return { pulled: 0, pushed: 0, errors: [], duration: Date.now() - start };
    }

    // Incremental merge: keep old cache entries, overwrite with new data
    const oldCache = loadGeneCache();
    const existingMap = new Map<string, EvolutionGene>(
      ((oldCache?.genes as EvolutionGene[]) || []).map(g => [g.id, g])
    );
    for (const gene of allGenes) {
      existingMap.set(gene.id, gene);
    }

    const merged = Array.from(existingMap.values());
    saveGeneCache({ genes: merged, lastUpdated: new Date().toISOString() });
    updateSyncTime('lastGeneSync');

    const newCount = allGenes.length;
    const totalCount = merged.length;
    log('INFO', 'pullGenes', `Synced ${newCount} new Genes (total cached: ${totalCount}) in ${Date.now() - start}ms`);

    return { pulled: newCount, pushed: 0, errors: [], duration: Date.now() - start };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    errors.push(`Pull Genes failed: ${msg}`);
    log('ERROR', 'pullGenes', msg);
    return { pulled: 0, pushed: 0, errors, duration: Date.now() - start };
  }
}

// ---------------------------------------------------------------------------
// Local Gene access
// ---------------------------------------------------------------------------

/** Get all locally cached Genes. */
export function getLocalGenes(): EvolutionGene[] {
  const cache = loadGeneCache();
  return (cache?.genes as EvolutionGene[]) || [];
}

/** Match Genes by taskType and signals. */
export function matchGenes(taskType: string, signals: string[]): EvolutionGene[] {
  const genes = getLocalGenes();
  const signalSet = new Set(signals);

  return genes
    .filter(g => g.taskType === taskType)
    .map(g => {
      const geneSignals = new Set(g.signals || []);
      const matched = [...signalSet].filter(s => geneSignals.has(s));
      const score = geneSignals.size > 0 ? matched.length / geneSignals.size : 0;
      return { gene: g, score };
    })
    .filter(x => x.score >= 0.1)
    .sort((a, b) => b.score - a.score)
    .map(x => x.gene);
}

// ---------------------------------------------------------------------------
// Report Capsule
// ---------------------------------------------------------------------------

/** Report a successful Capsule execution to the Hub. */
export async function reportCapsule(params: {
  capsuleId: string;
  outcome: 'success' | 'failure';
  executionTimeMs: number;
}): Promise<{ success: boolean; error?: string }> {
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return { success: false, error: 'Credentials not configured' };
  }

  try {
    const nodeId = getNodeId();
    await a2aReport(cred.api_key, {
      node_id: nodeId,
      capsule_id: params.capsuleId,
      outcome: params.outcome,
      execution_time_ms: params.executionTimeMs,
    });
    log('INFO', 'reportCapsule', `Reported capsule=${params.capsuleId} outcome=${params.outcome}`);
    return { success: true };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    log('ERROR', 'reportCapsule', msg);
    return { success: false, error: msg };
  }
}

// ---------------------------------------------------------------------------
// A2A Hub operations
// ---------------------------------------------------------------------------

/** Search Hub for matching Gene/Capsule assets. */
export async function hubFetch(params: {
  signals: string[];
  taskType: string;
  minConfidence?: number;
}): Promise<{ assets: unknown[]; error?: string }> {
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return { assets: [], error: 'Credentials not configured' };
  }

  try {
    const resp = await a2aFetch(cred.api_key, {
      signals: params.signals,
      task_type: params.taskType,
      min_confidence: params.minConfidence ?? 0.5,
    });
    log('INFO', 'hubFetch', `Found ${resp.assets?.length || 0} matching assets`);
    return { assets: resp.assets || [] };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    log('ERROR', 'hubFetch', msg);
    return { assets: [], error: msg };
  }
}

/** Apply a Capsule from the Hub to the local agent. */
export async function hubApply(capsuleId: string): Promise<{ success: boolean; error?: string }> {
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return { success: false, error: 'Credentials not configured' };
  }

  try {
    const nodeId = getNodeId();
    await a2aApply(cred.api_key, {
      node_id: nodeId,
      capsule_id: capsuleId,
      agent_id: cred.agent_id || 'main',
    });
    log('INFO', 'hubApply', `Applied capsule=${capsuleId}`);
    return { success: true };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    log('ERROR', 'hubApply', msg);
    return { success: false, error: msg };
  }
}

// ---------------------------------------------------------------------------
// Stats
// ---------------------------------------------------------------------------

/** Fetch user EvoMap statistics. */
export async function getStats(period: 'day' | 'week' | 'month' | 'all' = 'month'): Promise<unknown | null> {
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return null;
  }

  try {
    return await fetchStats(cred.api_key, period);
  } catch (err) {
    log('ERROR', 'getStats', err instanceof Error ? err.message : String(err));
    return null;
  }
}

// ---------------------------------------------------------------------------
// Full sync
// ---------------------------------------------------------------------------

/** Full sync: pull Genes + Capsule + Stats. */
export async function fullSync(): Promise<SyncResult> {
  const start = Date.now();
  const errors: string[] = [];

  const geneResult = await pullGenes(7);
  errors.push(...geneResult.errors);

  const stats = await getStats('month');
  if (stats) {
    log('INFO', 'fullSync', `Stats: ${JSON.stringify(stats).slice(0, 100)}`);
  } else {
    errors.push('Stats fetch failed');
  }

  return {
    pulled: geneResult.pulled,
    pushed: geneResult.pushed,
    errors,
    duration: Date.now() - start,
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getNodeId(): string {
  const cred = loadCredentials();
  return cred.agent_id || 'main';
}

/** Print a summary of locally cached Genes. */
export function printGeneSummary(): void {
  const genes = getLocalGenes();
  if (genes.length === 0) {
    console.log('Local Gene cache is empty (run sync first).');
    return;
  }

  const cache = loadGeneCache();
  console.log(`\n=== Gene Cache Summary (${genes.length} total) ===\n`);
  console.log(`Last updated: ${cache?.lastUpdated || 'unknown'}`);
  console.log('');

  // Group by category
  const byCategory: Record<string, number> = {};
  for (const g of genes) {
    byCategory[g.category] = (byCategory[g.category] || 0) + 1;
  }
  console.log('By category:');
  for (const [cat, count] of Object.entries(byCategory)) {
    console.log(`  ${cat}: ${count}`);
  }

  // Group by execMode
  const byMode: Record<string, number> = {};
  for (const g of genes) {
    byMode[g.execMode] = (byMode[g.execMode] || 0) + 1;
  }
  console.log('\nBy exec mode:');
  for (const [mode, count] of Object.entries(byMode)) {
    console.log(`  ${mode}: ${count}`);
  }

  // Top 5 by gdiScore
  const top = [...genes].sort((a, b) => (b.gdiScore || 0) - (a.gdiScore || 0)).slice(0, 5);
  console.log('\nTop 5 (GDI Score):');
  for (const g of top) {
    console.log(`  [${(g.gdiScore || 0).toFixed(3)}] ${g.displayName} (${g.taskType})`);
  }
  console.log('');
}
