/**
 * singularity GEP Idle Scheduler + Preflight Guards
 *
 * 对标 capability-evolver evolve.js 里的：
 *   - runPreflightChecks()（系统负载、活跃会话、loop gating）
 *   - shouldSkipHubCalls()（idle 节流）
 *   - checkRepairLoopCircuitBreaker()
 *   - getSystemLoad() / getActiveSessionCount()
 */
const os = require('os');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { getRepoRoot, getGepAssetsDir } = require('./paths.cjs');
const { readAllEvents } = require('./assetStore.cjs');

// --- Config ---
const LOAD_MAX = parseFloat(process.env.EVOLVER_LOAD_MAX || String(Math.min(os.cpus().length * 0.9, 4)));
const QUEUE_MAX = parseInt(process.env.EVOLVE_AGENT_QUEUE_MAX || '10', 10);
const QUEUE_BACKOFF_MS = parseInt(process.env.EVOLVE_AGENT_QUEUE_BACKOFF_MS || '60000', 10);
const IDLE_FETCH_INTERVAL_MS = parseInt(process.env.EVOLVER_IDLE_FETCH_INTERVAL_MS || (30 * 60 * 1000).toString(), 10);
const REPAIR_LOOP_THRESHOLD = 5;
const DORMANT_TTL_MS = parseInt(process.env.EVOLVER_DORMANT_TTL_MS || (60 * 60 * 1000).toString(), 10);
const MIN_CYCLE_INTERVAL_MS = parseInt(process.env.EVOLVE_MIN_INTERVAL || '120000', 10);

// --- Paths ---
const CACHE_DIR = path.join(os.homedir(), '.cache', 'singularity-forum');
const DORMANT_FILE = path.join(CACHE_DIR, 'dormant-hypothesis.json');
const STATE_FILE = path.join(getGepAssetsDir(), 'solidify_state.json');

// ============================================================================
// System load
// ============================================================================

function getSystemLoad() {
  try {
    if (process.platform === 'win32') {
      try {
        const out = execSync(
          'powershell -Command "(Get-Counter \'\\Processor(_Total)\\% Processor Time\' -ErrorAction SilentlyContinue).CounterSamples.CookedValue"',
          { encoding: 'utf-8', timeout: 5000, windowsHide: true }
        ).trim();
        const pct = parseFloat(out);
        if (!isNaN(pct)) return pct / 100;
      } catch {}
      return 0.5;
    } else {
      const out = fs.readFileSync('/proc/loadavg', 'utf-8');
      return parseFloat(out.split(' ')[0]) / os.cpus().length;
    }
  } catch { return 0; }
}

function getDefaultLoadMax() {
  const cores = os.cpus().length;
  return cores === 1 ? 0.9 : cores * 0.9;
}

// ============================================================================
// Active session detection
// ============================================================================

const AGENT_SESSIONS_DIR = path.join(os.homedir(), '.openclaw', 'agents', (process.env.AGENT_NAME || 'main'), 'sessions');

function getRecentActiveSessionCount(windowMs = 10 * 60 * 1000) {
  try {
    if (!fs.existsSync(AGENT_SESSIONS_DIR)) return 0;
    const now = Date.now();
    const w = Number.isFinite(windowMs) ? windowMs : 10 * 60 * 1000;
    return fs.readdirSync(AGENT_SESSIONS_DIR)
      .filter(f => f.endsWith('.jsonl') && !f.includes('.lock') && !f.startsWith('evolver_hand_'))
      .filter(f => {
        try { return (now - fs.statSync(path.join(AGENT_SESSIONS_DIR, f)).mtimeMs) < w; }
        catch { return false; }
      }).length;
  } catch { return 0; }
}

// ============================================================================
// Dormant hypothesis
// ============================================================================

function writeDormantHypothesis(data) {
  try {
    if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
    fs.writeFileSync(DORMANT_FILE, JSON.stringify({
      createdAt: Date.now(),
      ttl: DORMANT_TTL_MS,
      ...data,
    }, null, 2), 'utf-8');
  } catch (e) {
    console.warn('[DormantHypothesis] Write failed: ' + e.message);
  }
}

function readDormantHypothesis() {
  try {
    if (!fs.existsSync(DORMANT_FILE)) return null;
    const h = JSON.parse(fs.readFileSync(DORMANT_FILE, 'utf-8'));
    if (!h.createdAt) return null;
    if (Date.now() - h.createdAt > h.ttl) {
      try { fs.unlinkSync(DORMANT_FILE); } catch {}
      return null;
    }
    return h;
  } catch { return null; }
}

function clearDormantHypothesis() {
  try { if (fs.existsSync(DORMANT_FILE)) fs.unlinkSync(DORMANT_FILE); } catch {}
}

// ============================================================================
// Loop gating state
// ============================================================================

function readSolidifyState() {
  try {
    if (!fs.existsSync(STATE_FILE)) return null;
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  } catch { return null; }
}

/**
 * 检查是否需要等待上一次 solidify 完成
 */
function shouldWaitForSolidify() {
  try {
    const st = readSolidifyState();
    const lastRun = st && st.last_run ? st.last_run : null;
    const lastSolid = st && st.last_solidify ? st.last_solidify : null;
    if (!lastRun || !lastRun.run_id) return false;
    const pending = !lastSolid || !lastSolid.run_id || String(lastSolid.run_id) !== String(lastRun.run_id);
    return pending;
  } catch { return false; }
}

// ============================================================================
// Saturation detection (Hub fetch gating)
// ============================================================================

const SATURATION_SIGNALS = ['force_steady_state', 'evolution_saturation', 'empty_cycle_loop_detected'];
const ACTIONABLE_PATTERNS = [
  'log_error', 'recurring_error', 'capability_gap', 'perf_bottleneck',
  'external_task', 'bounty_task', 'overdue_task', 'urgent',
  'unsupported_input_type', 'errsig:',
];

let _lastHubFetchTs = 0;

function shouldSkipHubCalls(signals) {
  if (!Array.isArray(signals)) return false;

  // Check for saturation signals
  let hasSaturation = false;
  for (const s of SATURATION_SIGNALS) {
    if (signals.includes(s)) { hasSaturation = true; break; }
  }
  if (!hasSaturation) return false;

  // Are there actionable signals mixed in?
  for (const s of signals) {
    if (s.indexOf('errsig:') === 0) return false;
    for (const ap of ACTIONABLE_PATTERNS) {
      if (s.indexOf(ap) >= 0) return false;
    }
  }
  return true;
}

// Last Hub fetch throttle
function recordHubFetch() { _lastHubFetchTs = Date.now(); }

function shouldThrottleHubFetch() {
  if (_lastHubFetchTs === 0) return false;
  return Date.now() - _lastHubFetchTs < IDLE_FETCH_INTERVAL_MS;
}

// ============================================================================
// Repair loop circuit breaker
// ============================================================================

function checkRepairLoopCircuitBreaker() {
  try {
    const events = readAllEvents();
    if (!Array.isArray(events) || events.length < REPAIR_LOOP_THRESHOLD) return;
    const recent = events.slice(-REPAIR_LOOP_THRESHOLD);
    const allRepairFailed = recent.every(e =>
      e && e.intent === 'repair' &&
      e.outcome && (e.outcome.status === 'failed' || e.outcome === 'failure')
    );
    if (allRepairFailed) {
      const geneIds = recent
        .map(e => (e.genes_used && e.genes_used[0]) || e.geneId || 'unknown')
        .filter(Boolean);
      const sameGene = geneIds.every(id => id === geneIds[0]);
      console.warn(`[CircuitBreaker] ${REPAIR_LOOP_THRESHOLD} consecutive failed repairs${sameGene ? ' (gene: ' + geneIds[0] + ')' : ''}. Forcing innovation.`);
      process.env.FORCE_INNOVATION = 'true';
    }
  } catch (e) {
    console.warn('[CircuitBreaker] Check failed: ' + e.message);
  }
}

// ============================================================================
// Main preflight
// ============================================================================

/**
 * 运行前置检查，返回 { abort: boolean, reason?: string, backoffMs?: number }
 */
async function runPreflightChecks() {
  // 1. Singleton: another evolver running?
  const lockFile = path.join(CACHE_DIR, 'evolver.pid');
  try {
    if (fs.existsSync(lockFile)) {
      const pid = parseInt(fs.readFileSync(lockFile, 'utf-8').trim(), 10);
      if (Number.isFinite(pid) && pid > 0) {
        try { process.kill(pid, 0); return { abort: true, reason: 'another_evolver_running', backoffMs: 300000 }; }
        catch {}
      }
    }
  } catch {}

  // 2. Agent busy with user conversations?
  const activeSessions = getRecentActiveSessionCount(10 * 60 * 1000);
  const queueMax = parseInt(process.env.EVOLVE_AGENT_QUEUE_MAX || String(QUEUE_MAX), 10);
  if (activeSessions > queueMax) {
    console.log(`[Preflight] ${activeSessions} active sessions (max ${queueMax}). Backing off ${QUEUE_BACKOFF_MS}ms.`);
    writeDormantHypothesis({ backoff_reason: 'active_sessions_exceeded', active_sessions: activeSessions, queue_max: queueMax });
    return { abort: true, reason: 'active_sessions_exceeded', backoffMs: QUEUE_BACKOFF_MS };
  }

  // 3. System load too high?
  const loadMax = parseFloat(process.env.EVOLVER_LOAD_MAX || String(Math.min(getDefaultLoadMax(), 4)));
  const sysLoad = getSystemLoad();
  if (sysLoad > loadMax) {
    console.log(`[Preflight] System load ${sysLoad.toFixed(2)} > ${loadMax.toFixed(1)}. Backing off ${QUEUE_BACKOFF_MS}ms.`);
    writeDormantHypothesis({ backoff_reason: 'system_load_exceeded', system_load: sysLoad, load_max: loadMax });
    return { abort: true, reason: 'system_load_exceeded', backoffMs: QUEUE_BACKOFF_MS };
  }

  // 4. Loop gating: previous solidify not done?
  if (shouldWaitForSolidify()) {
    const dormant = readDormantHypothesis();
    if (dormant && dormant.backoff_reason === 'loop_gating_pending_solidify') {
      const waited = Date.now() - (dormant.createdAt || 0);
      if (waited < MIN_CYCLE_INTERVAL_MS) {
        const remaining = MIN_CYCLE_INTERVAL_MS - waited;
        console.log(`[Preflight] Previous solidify pending. Waiting ${Math.round(remaining / 1000)}s...`);
        return { abort: true, reason: 'loop_gating', backoffMs: remaining };
      }
    }
    writeDormantHypothesis({ backoff_reason: 'loop_gating_pending_solidify' });
    return { abort: true, reason: 'loop_gating', backoffMs: MIN_CYCLE_INTERVAL_MS };
  }

  return { abort: false };
}

// ============================================================================
// Cycle info
// ============================================================================

const CYCLE_COUNTER_FILE = path.join(CACHE_DIR, 'cycle-counter.json');

function getNextCycleId() {
  try {
    if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
    let counter = { cycle: 0 };
    if (fs.existsSync(CYCLE_COUNTER_FILE)) {
      try { counter = JSON.parse(fs.readFileSync(CYCLE_COUNTER_FILE, 'utf-8')); } catch {}
    }
    counter.cycle = (counter.cycle || 0) + 1;
    fs.writeFileSync(CYCLE_COUNTER_FILE, JSON.stringify(counter, null, 2));
    return counter.cycle;
  } catch { return 0; }
}

module.exports = {
  runPreflightChecks,
  checkRepairLoopCircuitBreaker,
  shouldSkipHubCalls,
  shouldThrottleHubFetch,
  recordHubFetch,
  writeDormantHypothesis,
  readDormantHypothesis,
  clearDormantHypothesis,
  getSystemLoad,
  getRecentActiveSessionCount,
  getNextCycleId,
  getDefaultLoadMax,
  LOAD_MAX,
  QUEUE_MAX,
  IDLE_FETCH_INTERVAL_MS,
};
