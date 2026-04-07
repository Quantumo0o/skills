/**
 * singularity GEP Asset Store
 * 统一管理 genes.json / capsules.json / events.jsonl
 * 与 capability-evolver/src/gep/assetStore.js 接口对齐
 */
const fs = require('fs');
const path = require('path');


// singularity 缓存目录
const CACHE_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.cache', 'singularity-forum');
const ASSETS_DIR = path.join(CACHE_DIR, 'assets');

const GENES_FILE   = path.join(ASSETS_DIR, 'genes.json');
const CAPSULES_FILE = path.join(ASSETS_DIR, 'capsules.json');
const EVENTS_FILE  = path.join(CACHE_DIR, 'evolution-events.jsonl');

function ensureAssetsDir() {
  if (!fs.existsSync(ASSETS_DIR)) fs.mkdirSync(ASSETS_DIR, { recursive: true });
}

function ensureCacheDir() {
  if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
}

// ---------------------------------------------------------------------------
// Genes
// ---------------------------------------------------------------------------

function loadGenes() {
  ensureAssetsDir();
  if (!fs.existsSync(GENES_FILE)) return [];
  try { return JSON.parse(fs.readFileSync(GENES_FILE, 'utf-8')); }
  catch { return []; }
}

function upsertGene(gene) {
  const genes = loadGenes();
  const idx = genes.findIndex(g => g.name === gene.name || g.id === gene.id);
  if (idx >= 0) genes[idx] = { ...genes[idx], ...gene };
  else genes.push(gene);
  ensureAssetsDir();
  fs.writeFileSync(GENES_FILE, JSON.stringify(genes, null, 2), 'utf-8');
  return genes;
}

function findGeneByName(name) {
  return loadGenes().find(g => g.name === name);
}

// ---------------------------------------------------------------------------
// Capsules
// ---------------------------------------------------------------------------

function loadCapsules() {
  ensureAssetsDir();
  if (!fs.existsSync(CAPSULES_FILE)) return [];
  try { return JSON.parse(fs.readFileSync(CAPSULES_FILE, 'utf-8')); }
  catch { return []; }
}

function appendCapsule(capsule) {
  const capsules = loadCapsules();
  capsules.push({ ...capsule, _createdAt: new Date().toISOString() });
  ensureAssetsDir();
  fs.writeFileSync(CAPSULES_FILE, JSON.stringify(capsules, null, 2), 'utf-8');
}

function upsertCapsule(capsule) {
  const capsules = loadCapsules();
  const idx = capsules.findIndex(c => c.capsuleId === capsule.capsuleId || c.name === capsule.name);
  if (idx >= 0) capsules[idx] = { ...capsules[idx], ...capsule };
  else capsules.push({ ...capsule, _createdAt: new Date().toISOString() });
  ensureAssetsDir();
  fs.writeFileSync(CAPSULES_FILE, JSON.stringify(capsules, null, 2), 'utf-8');
}

// ---------------------------------------------------------------------------
// Events (append-only JSONL)
// ---------------------------------------------------------------------------

function appendEventJsonl(event) {
  ensureCacheDir();
  const line = JSON.stringify({ ...event, _ts: new Date().toISOString() }) + '\n';
  fs.appendFileSync(EVENTS_FILE, line, 'utf-8');
}

function readAllEvents() {
  ensureCacheDir();
  if (!fs.existsSync(EVENTS_FILE)) return [];
  try {
    return fs.readFileSync(EVENTS_FILE, 'utf-8')
      .split('\n').filter(Boolean).map(line => JSON.parse(line));
  } catch { return []; }
}

function getLastEventId() {
  const events = readAllEvents();
  return events.length ? events[events.length - 1]._id || null : null;
}

// ---------------------------------------------------------------------------
// Failed capsules (quick in-memory dedup, persists as JSONL marker)
// ---------------------------------------------------------------------------

const FAILED_FILE = path.join(ASSETS_DIR, 'failed-capsules.json');

function readRecentFailedCapsules(sinceMs = 7 * 24 * 3600 * 1000) {
  if (!fs.existsSync(FAILED_FILE)) return [];
  try {
    const all = JSON.parse(fs.readFileSync(FAILED_FILE, 'utf-8'));
    const cutoff = Date.now() - sinceMs;
    return all.filter(c => c._ts && c._ts > cutoff);
  } catch { return []; }
}

function appendFailedCapsule(capsule, reason) {
  ensureAssetsDir();
  const failed = fs.existsSync(FAILED_FILE)
    ? JSON.parse(fs.readFileSync(FAILED_FILE, 'utf-8'))
    : [];
  failed.push({ ...capsule, reason, _ts: Date.now() });
  fs.writeFileSync(FAILED_FILE, JSON.stringify(failed, null, 2), 'utf-8');
}

// ---------------------------------------------------------------------------
// Asset file existence bootstrap
// ---------------------------------------------------------------------------

function ensureAssetFiles() {
  ensureAssetsDir();
  [GENES_FILE, CAPSULES_FILE].forEach(fp => {
    if (!fs.existsSync(fp)) fs.writeFileSync(fp, '[]', 'utf-8');
  });
}
