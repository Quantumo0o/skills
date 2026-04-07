/**
 * singularity - Local Cache Management
 * Handles persistent state for EvoMap Gene/Capsule sync.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { CREDENTIALS_PATH } from './api.js';

const CACHE_DIR = path.join(os.homedir(), '.cache', 'singularity');

function ensureCacheDir(): void {
  if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
}

// ---------------------------------------------------------------------------
// Gene cache
// ---------------------------------------------------------------------------

export interface GeneCache {
  genes: unknown[];
  lastUpdated: string | null;
}

export function getGeneCachePath(): string {
  return path.join(CACHE_DIR, 'genes.json');
}

export function loadGeneCache(): GeneCache {
  ensureCacheDir();
  const f = getGeneCachePath();
  if (!fs.existsSync(f)) return { genes: [], lastUpdated: null };
  try {
    return JSON.parse(fs.readFileSync(f, 'utf-8')) as GeneCache;
  } catch { return { genes: [], lastUpdated: null }; }
}

export function saveGeneCache(cache: GeneCache): void {
  ensureCacheDir();
  fs.writeFileSync(getGeneCachePath(), JSON.stringify(cache, null, 2), 'utf-8');
}

// ---------------------------------------------------------------------------
// Capsule cache
// ---------------------------------------------------------------------------

export interface CapsuleCache {
  capsules: unknown[];
  lastUpdated: string | null;
}

export function getCapsuleCachePath(): string {
  return path.join(CACHE_DIR, 'capsules.json');
}

export function loadCapsuleCache(): CapsuleCache {
  ensureCacheDir();
  const f = getCapsuleCachePath();
  if (!fs.existsSync(f)) return { capsules: [], lastUpdated: null };
  try {
    return JSON.parse(fs.readFileSync(f, 'utf-8')) as CapsuleCache;
  } catch { return { capsules: [], lastUpdated: null }; }
}

export function saveCapsuleCache(cache: CapsuleCache): void {
  ensureCacheDir();
  fs.writeFileSync(getCapsuleCachePath(), JSON.stringify(cache, null, 2), 'utf-8');
}

// ---------------------------------------------------------------------------
// Sync state
// ---------------------------------------------------------------------------

export interface SyncState {
  lastGeneSync: string | null;
  lastCapsuleSync: string | null;
  lastStatsSync: string | null;
}

export function getSyncStatePath(): string {
  return path.join(CACHE_DIR, 'sync-state.json');
}

export function loadSyncState(): SyncState {
  ensureCacheDir();
  const f = getSyncStatePath();
  if (!fs.existsSync(f)) return { lastGeneSync: null, lastCapsuleSync: null, lastStatsSync: null };
  try {
    return JSON.parse(fs.readFileSync(f, 'utf-8')) as SyncState;
  } catch { return { lastGeneSync: null, lastCapsuleSync: null, lastStatsSync: null }; }
}

export function saveSyncState(state: Partial<SyncState>): void {
  ensureCacheDir();
  const current = loadSyncState();
  const f = getSyncStatePath();
  fs.writeFileSync(f, JSON.stringify({ ...current, ...state }, null, 2), 'utf-8');
}

export function updateSyncTime(field: keyof SyncState): void {
  saveSyncState({ [field]: new Date().toISOString() });
}
