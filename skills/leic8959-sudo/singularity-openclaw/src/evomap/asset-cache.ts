/**
 * EvoMap Asset Cache
 * 本地文件缓存层：genes.json / capsules.json
 * 查找顺序：文件缓存 → 本地 DB → Hub
 */

import fs from 'fs';
import path from 'path';

const CACHE_DIR = process.env.EVOMAP_CACHE_PATH || path.join(process.cwd(), '.evomap_cache');
const CACHE_TTL_MS = parseInt(process.env.EVOMAP_CACHE_TTL_MS || '3600000', 10); // default 1h
const GENES_FILE = path.join(CACHE_DIR, 'genes.json');
const CAPSULES_FILE = path.join(CACHE_DIR, 'capsules.json');

export interface CachedGene {
  id: string;
  name: string;
  displayName: string;
  taskType: string;
  signals: string[];
  execMode: string;
  strategy: unknown;
  constraints?: unknown;
  minConfidence: number;
  isActive: boolean;
  cachedAt: string;
}

export interface CachedCapsule {
  id: string;
  name: string;
  taskType: string;
  geneId: string;           // primary gene
  geneIds: string[];        // all genes (multi-gene)
  payload: unknown;
  confidence: number;
  triggerSignals: string[];
  inheritedFrom?: string;   // original Hub capsuleId
  cachedAt: string;
}

type GeneStore = Record<string, CachedGene>;
type CapsuleStore = Record<string, CachedCapsule>;

function ensureCacheDir(): void {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }
}

function readStore<T>(filePath: string): Record<string, T> {
  try {
    if (!fs.existsSync(filePath)) return {};
    const raw = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(raw) as Record<string, T>;
  } catch {
    return {};
  }
}

function writeStore<T>(filePath: string, store: Record<string, T>): void {
  ensureCacheDir();
  fs.writeFileSync(filePath, JSON.stringify(store, null, 2), 'utf-8');
}

export function pruneExpiredCache(): void {
  const now = Date.now();

  const geneStore = readStore<CachedGene>(GENES_FILE);
  const prunedGenes = Object.fromEntries(
    Object.entries(geneStore).filter(([, g]) => now - new Date(g.cachedAt).getTime() <= CACHE_TTL_MS)
  );
  if (Object.keys(prunedGenes).length !== Object.keys(geneStore).length) {
    writeStore(GENES_FILE, prunedGenes);
  }

  const capsuleStore = readStore<CachedCapsule>(CAPSULES_FILE);
  const prunedCapsules = Object.fromEntries(
    Object.entries(capsuleStore).filter(([, c]) => now - new Date(c.cachedAt).getTime() <= CACHE_TTL_MS)
  );
  if (Object.keys(prunedCapsules).length !== Object.keys(capsuleStore).length) {
    writeStore(CAPSULES_FILE, prunedCapsules);
  }
}



export function cacheGene(gene: CachedGene): void {
  const store = readStore<CachedGene>(GENES_FILE);
  store[gene.id] = { ...gene, cachedAt: new Date().toISOString() };
  writeStore(GENES_FILE, store);
}

export function getCachedGene(geneId: string): CachedGene | null {
  const store = readStore<CachedGene>(GENES_FILE);
  const entry = store[geneId];
  if (!entry) return null;
  if (Date.now() - new Date(entry.cachedAt).getTime() > CACHE_TTL_MS) return null;
  return entry;
}

export function getAllCachedGenes(): CachedGene[] {
  const store = readStore<CachedGene>(GENES_FILE);
  const now = Date.now();
  return Object.values(store).filter(g => now - new Date(g.cachedAt).getTime() <= CACHE_TTL_MS);
}

// ─── Capsule cache ───────────────────────────────────────────────────────────

export function cacheCapsule(capsule: CachedCapsule): void {
  const store = readStore<CachedCapsule>(CAPSULES_FILE);
  store[capsule.id] = { ...capsule, cachedAt: new Date().toISOString() };
  writeStore(CAPSULES_FILE, store);
}

export function getCachedCapsule(capsuleId: string): CachedCapsule | null {
  const store = readStore<CachedCapsule>(CAPSULES_FILE);
  const entry = store[capsuleId];
  if (!entry) return null;
  if (Date.now() - new Date(entry.cachedAt).getTime() > CACHE_TTL_MS) return null;
  return entry;
}

/**
 * 按 signals 快速匹配本地缓存的 Capsule
 * 返回置信度最高且信号重叠最多的 Capsule
 */
export function findCachedCapsuleBySignals(
  signals: string[],
  taskType?: string,
  minConfidence = 0.5,
): CachedCapsule | null {
  const store = readStore<CachedCapsule>(CAPSULES_FILE);
  const signalSet = new Set(signals);

  let best: CachedCapsule | null = null;
  let bestScore = -1;

  for (const capsule of Object.values(store)) {
    if (Date.now() - new Date(capsule.cachedAt).getTime() > CACHE_TTL_MS) continue;
    if (capsule.confidence < minConfidence) continue;
    if (taskType && capsule.taskType !== taskType) continue;

    const overlap = capsule.triggerSignals.filter(s => signalSet.has(s)).length;
    const total = capsule.triggerSignals.length || 1;
    const score = (overlap / total) * capsule.confidence;

    if (score > bestScore) {
      bestScore = score;
      best = capsule;
    }
  }

  return best;
}
