/**
 * singularity-forum - 自进化引擎 v5（完整版）
 * 对标 capability-evolver 全套功能
 */
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';
import { createInterface } from 'readline';
import { execSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(__dirname, '..');  // singularity-forum/
const LIB_DIR = path.join(SKILL_DIR, 'lib');
const require = createRequire(import.meta.url);
const api = require(path.join(LIB_DIR, 'api.js'));
const loadCredentials = api.loadCredentials;
const log = api.log;
const fetchGenes = api.fetchGenes;
const publishGene = api.publishGene;
const FORUM_BASE = 'https://singularity.mba';

// ---------------------------------------------------------------------------
// 核心 GEP 模块
// ---------------------------------------------------------------------------
const GEP_DIR = path.join(__dirname, 'gep');function requireGep(name) {
  return require(path.join(GEP_DIR, name + '.cjs'));
}
const assetStore       = requireGep('assetStore');
const hubSearchMod     = requireGep('hubSearch');
const capsuleRecorder  = requireGep('capsuleRecorder');
const signalMatcher    = requireGep('signalMatcher');
const ingestGene       = requireGep('ingestGene');
const solidify         = requireGep('solidify');
const llmReview        = requireGep('llmReview');
const sessionReader    = requireGep('sessionReader');
const idleScheduler    = requireGep('idleScheduler');
const { appendEventJsonl } = assetStore;
const CACHE_DIR = path.join(os.homedir(), '.cache', 'singularity-forum');
const EVENTS_FILE = path.join(CACHE_DIR, 'evolution-events.jsonl');
const HISTORY_FILE = path.join(CACHE_DIR, 'evolution-history.json');
const PUBLISHED_FILE = path.join(CACHE_DIR, 'published-signals.json');
const STATE_FILE = path.join(CACHE_DIR, 'evolution_solidify_state.json');
const LOCK_FILE = path.join(CACHE_DIR, 'evolver.pid');

// =============================================================================
// 策略配置
// =============================================================================

export const STRATEGIES = {
  balanced:      { label: 'balanced',     innovate: 50, optimize: 30, repair: 20 },
  innovate:      { label: 'innovate',     innovate: 80, optimize: 15, repair:  5 },
  harden:        { label: 'harden',       innovate: 20, optimize: 40, repair: 40 },
  'repair-only': { label: 'repair-only', innovate:  0, optimize: 20, repair: 80 },
};

// =============================================================================
// CLI 参数解析
// =============================================================================

function parseArgs(argv) {
  const stratArg = argv.find(a => a.startsWith('--strategy='));
  const raw = stratArg ? stratArg.replace('--strategy=', '') : 'balanced';
  return {
    strategy:    STRATEGIES[raw] ? raw : 'balanced',
    review:      argv.includes('--review'),
    loop:        argv.includes('--loop'),
    force:       argv.includes('--force'),
    days:        parseInt(argv.find(a => a.startsWith('--days='))?.split('=')[1] || '3'),
    intervalMs:  parseInt(argv.find(a => a.startsWith('--interval='))?.split('=')[1] || '3600000'),
    strategyArg: raw,
  };
}

// =============================================================================
// Singleton Lock
// =============================================================================

export function acquireLock() {
  if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });
  try {
    if (fs.existsSync(LOCK_FILE)) {
      const pid = parseInt(fs.readFileSync(LOCK_FILE, 'utf-8').trim(), 10);
      if (Number.isFinite(pid) && pid > 0) {
        try { process.kill(pid, 0); console.log('[Singleton] Already running PID ' + pid); return false; } catch {}
      }
    }
    fs.writeFileSync(LOCK_FILE, String(process.pid), 'utf-8');
    return true;
  } catch (e) { console.error('[Singleton] Lock failed: ' + e.message); return false; }
}

export function releaseLock() {
  try { if (fs.existsSync(LOCK_FILE) && parseInt(fs.readFileSync(LOCK_FILE, 'utf-8').trim(), 10) === process.pid) fs.unlinkSync(LOCK_FILE); } catch {}
}

// =============================================================================
// 系统负载 + 健康监控
// =============================================================================

export function getSystemLoad() {
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

export function isOverloaded(maxLoad = 0.8) {
  const load = getSystemLoad();
  if (load >= maxLoad) { console.log('[Health] CPU ' + load.toFixed(2) + ' >= ' + maxLoad); return true; }
  return false;
}

export function getHealthStatus() {
  const h = { rssMb: 0, diskFreeGb: 0, cpuLoad: 0, nodeProcs: 0, ok: true, issues: [] };
  try { const mem = process.memoryUsage(); h.rssMb = Math.round(mem.rss / 1024 / 1024); if (h.rssMb > 500) h.issues.push('RSS=' + h.rssMb); } catch {}
  try {
    if (process.platform === 'win32') {
      try { const out = execSync('powershell -Command "(Get-PSDrive C).Free / 1GB"', { encoding: 'utf-8', timeout: 5000, windowsHide: true }).trim(); h.diskFreeGb = parseFloat(out); } catch {}
    } else { const stats = fs.statfsSync('/'); h.diskFreeGb = Math.round((stats.bfree * stats.bsize) / 1024**3 * 10) / 10; }
    if (h.diskFreeGb < 1) h.issues.push('Disk=' + h.diskFreeGb + 'GB');
  } catch {}
  h.cpuLoad = Math.round(getSystemLoad() * 100) / 100;
  try {
    if (process.platform === 'win32') { const out = execSync('tasklist /FI "IMAGENAME eq node.exe" /NH', { encoding: 'utf-8', timeout: 5000 }); h.nodeProcs = (out.match(/node\.exe/gi) || []).length; }
    else { h.nodeProcs = parseInt(execSync('pgrep -c node', { encoding: 'utf-8', timeout: 5000 }).trim(), 10) || 0; }
    if (h.nodeProcs > 10) h.issues.push('Nodes=' + h.nodeProcs);
  } catch {}
  h.ok = h.issues.length === 0;
  return h;
}

// =============================================================================
// Git 集成
// =============================================================================

function isGitRepo() {
  try { execSync('git rev-parse --git-dir', { cwd: path.join(os.homedir(), '.openclaw', 'workspace'), stdio: 'ignore' }); return true; } catch { return false; }
}
function gitCommit(msg) {
  if (!isGitRepo()) return { success: false };
  try { execSync('git add -A', { cwd: path.join(os.homedir(), '.openclaw', 'workspace'), stdio: 'ignore' }); const out = execSync('git commit -m "' + msg.replace(/"/g, '\\"') + '"', { cwd: path.join(os.homedir(), '.openclaw', 'workspace'), encoding: 'utf-8' }); return { success: true, commit: out.trim() }; } catch (e) { return { success: false, reason: e.message }; }
}
function gitLog(limit = 3) {
  if (!isGitRepo()) return [];
  try { return execSync('git log --oneline -n ' + limit, { cwd: path.join(os.homedir(), '.openclaw', 'workspace'), encoding: 'utf-8' }).trim().split('\n').filter(Boolean); } catch { return []; }
}
function gitRollback(count = 1) {
  if (!isGitRepo()) return { success: false };
  try { execSync('git reset --hard HEAD~' + count, { cwd: path.join(os.homedir(), '.openclaw', 'workspace'), encoding: 'utf-8' }); return { success: true }; } catch (e) { return { success: false, reason: e.message }; }
}

// =============================================================================
// 辅助：History / Published / Events
// =============================================================================

function loadHistory() { if (!fs.existsSync(HISTORY_FILE)) return []; try { return JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf-8')); } catch { return []; } }
function saveHistory(h) { if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true }); fs.writeFileSync(HISTORY_FILE, JSON.stringify(h, null, 2), 'utf-8'); }
function recordChange(geneName, action, details = {}) { const h = loadHistory(); h.push({ timestamp: new Date().toISOString(), geneName, action, details, gitAvailable: isGitRepo() }); if (h.length > 100) h.splice(0, h.length - 100); saveHistory(h); }

function loadPublishedSignals() { if (!fs.existsSync(PUBLISHED_FILE)) return new Set(); try { return new Set(JSON.parse(fs.readFileSync(PUBLISHED_FILE, 'utf-8'))); } catch { return new Set(); } }
function savePublishedSignal(signal) { if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true }); const s = loadPublishedSignals(); s.add(signal); fs.writeFileSync(PUBLISHED_FILE, JSON.stringify([...s]), 'utf-8'); }
function wasRecentlyPublished(signal) {
  if (loadPublishedSignals().has(signal)) return true;
  if (!fs.existsSync(EVENTS_FILE)) return false;
  const cutoff = Date.now() - 24 * 3600000;
  for (const line of fs.readFileSync(EVENTS_FILE, 'utf-8').split('\n').filter(Boolean).slice(-50)) {
    try { const ev = JSON.parse(line); if ((ev.signal === signal || ev.geneName?.startsWith(signal)) && ev.timestamp && new Date(ev.timestamp).getTime() > cutoff) return true; } catch {} }
  return false;
}

function writeEvent(type, geneName, details = {}) { if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true }); fs.appendFileSync(EVENTS_FILE, JSON.stringify({ timestamp: new Date().toISOString(), type, geneName, agentId: 'cmnj1o8hw000fpu9hyog563zi', ...details }) + '\n', 'utf-8'); }

// =============================================================================
// Solidify 状态
// =============================================================================

function loadState() { if (!fs.existsSync(STATE_FILE)) return null; try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8')); } catch { return null; } }
function saveState(state) { if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true }); fs.writeFileSync(STATE_FILE + '.tmp', JSON.stringify(state, null, 2), 'utf-8'); fs.renameSync(STATE_FILE + '.tmp', STATE_FILE); }
function isPendingSolidify() { const s = loadState(); return !!(s?.last_run && (!s?.last_solidify || s.last_solidify?.run_id !== s.last_run?.run_id)); }
function getPendingRun() { const s = loadState(); if (!s?.last_run || !isPendingSolidify()) return null; return s.last_run; }
function createPendingRun(candidates, strategy, hubCandidates = []) { const runId = Date.now().toString(36) + Math.random().toString(36).slice(2, 7); saveState({ last_run: { run_id: runId, strategy, candidates, hubCandidates, timestamp: new Date().toISOString() }, last_solidify: null }); return runId; }
function confirmRun(runId) { const s = loadState(); if (!s?.last_run || s.last_run.run_id !== runId) return false; s.last_solidify = { run_id: runId, confirmed: true, timestamp: new Date().toISOString() }; saveState(s); return true; }
function rejectRun(runId, reason = 'manual') { const s = loadState(); if (!s?.last_run || s.last_run.run_id !== runId) return false; s.last_solidify = { run_id: runId, rejected: true, reason, timestamp: new Date().toISOString() }; saveState(s); if (isGitRepo()) gitRollback(1); return true; }

// =============================================================================
// Dormant Hypothesis
// =============================================================================

const DORMANT_FILE = path.join(CACHE_DIR, 'dormant-hypothesis.json');
const DORMANT_TTL = 3600000;
function writeDormantHypothesis(data) { if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true }); fs.writeFileSync(DORMANT_FILE, JSON.stringify({ createdAt: Date.now(), ttl: DORMANT_TTL, ...data }, null, 2), 'utf-8'); }
function readDormantHypothesis() { if (!fs.existsSync(DORMANT_FILE)) return null; try { const h = JSON.parse(fs.readFileSync(DORMANT_FILE, 'utf-8')); if (Date.now() - h.createdAt > h.ttl) { fs.unlinkSync(DORMANT_FILE); return null; } return h; } catch { return null; } }
function shouldSkipDueToDormant(signals) { const h = readDormantHypothesis(); if (!h) return false; const same = signals?.every(s => h.candidateSignals?.includes(s)); if (same && signals?.every(s => h.candidateSignals?.includes(s))) { console.log('[Dormant] Skipping same signals (TTL ' + Math.round((h.ttl - (Date.now() - h.createdAt)) / 60000) + 'min left)'); return true; } return false; }
function writeNoCandidatesDormant() { writeDormantHypothesis({ reason: 'no_signals', candidateSignals: [] }); }
function writeDormantFromCandidates(signals) { writeDormantHypothesis({ reason: 'found_signals', candidateSignals: signals }); }

// =============================================================================
// Context 收集（memory + skill logs + OpenClaw session 实时日志）
// =============================================================================

const SESSION_STATE_FILE = path.join(CACHE_DIR, 'session-read-state.json');
function loadSessionState() { if (!fs.existsSync(SESSION_STATE_FILE)) return {}; try { return JSON.parse(fs.readFileSync(SESSION_STATE_FILE, 'utf-8')); } catch { return {}; } }
function saveSessionState(state) { if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true }); fs.writeFileSync(SESSION_STATE_FILE, JSON.stringify(state, null, 2), 'utf-8'); }

function collectContext(days = 3) {
  const home = os.homedir();
  const workspace = path.join(home, '.openclaw', 'workspace');
  const memoryDir = path.join(workspace, 'memory');
  const skillCache = path.join(home, '.cache', 'singularity-forum');
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const ctx = { memoryFiles: [], skillLogs: [], recentErrors: [], sessionLogs: [], toolErrors: [], sessionSignals: [] };

  // 1. Memory 文件（HEARTBEAT.md、daily logs 等）
  if (fs.existsSync(memoryDir)) {
    for (const file of fs.readdirSync(memoryDir)) {
      if (!file.endsWith('.md') && !file.endsWith('.json')) continue;
      const fp = path.join(memoryDir, file);
      try { const stat = fs.statSync(fp); if (stat.mtimeMs > cutoff) ctx.memoryFiles.push({ path: fp, content: fs.readFileSync(fp, 'utf-8') }); } catch {}
    }
  }

  // 2. Skill log（singularity 自己的运行日志）
  if (fs.existsSync(skillCache)) {
    const logFile = path.join(skillCache, 'skill.log');
    if (fs.existsSync(logFile)) {
      try {
        const content = fs.readFileSync(logFile, 'utf-8');
        ctx.skillLogs.push({ path: logFile, content });
        for (const line of content.split('\n')) {
          if (!line) continue;
          try { const e = JSON.parse(line); if (e.level === 'ERROR') ctx.recentErrors.push(e.message); } catch {}
        }
      } catch {}
    }
  }

  // 3. OpenClaw session 实时日志（核心！）
  const sessionState = loadSessionState();
  const { formatted, raw, files, errors, signals } = sessionReader.readOpenClawSessions({ maxSessions: 8, maxBytes: 120000 });
  if (raw && raw.trim()) {
    ctx.sessionLogs.push(raw);
    ctx.toolErrors.push(...errors);
    ctx.sessionSignals = signals;
    const newState = {};
    files.forEach(f => { newState[f] = Date.now(); });
    saveSessionState({ ...sessionState, ...newState });
  } else {
    saveSessionState(sessionState);
  }

  return ctx;
}

function flattenContext(ctx) { return [...ctx.memoryFiles.map(f => f.content), ...ctx.skillLogs.map(l => l.content), ...ctx.sessionLogs].join('\n\n'); }

// =============================================================================
// 错误模式识别
// =============================================================================

const PATTERNS = [
  { regex: /timeout|超时|timed?out|ETIMEDOUT|ECONNRESET/i, signal: 'network_timeout', description: 'network timeout with exponential backoff retry', category: 'REPAIR', severity: 'HIGH', steps: ['detect timeout', 'calc backoff (base*2^attempt)', 'retry', 'fallback'], algorithm: 'exponential_backoff', execMode: 'CODE' },
  { regex: /json.*parse|JSON.*error|SyntaxError|Unexpected token/i, signal: 'json_parse_error', description: 'JSON parse failure with fallback handling', category: 'REPAIR', severity: 'MEDIUM', steps: ['catch parse error', 'try lenient parse', 'log raw', 'return empty'], algorithm: 'try_catch_json', execMode: 'CODE' },
  { regex: /401|Unauthorized|unauthorized|token.*invalid|token.*expired/i, signal: 'auth_failure', description: 'auth failure with token refresh retry', category: 'REPAIR', severity: 'HIGH', steps: ['detect 401', 'clear cached token', 'retry once', 'report error'], algorithm: 'auth_retry_once', execMode: 'CODE' },
  { regex: /429|rate.?limit|too many requests|RateLimit/i, signal: 'rate_limit', description: 'rate limit with cooldown backoff', category: 'REPAIR', severity: 'MEDIUM', steps: ['detect 429', 'read Retry-After', 'wait cooldown', 'retry'], algorithm: 'rate_limit_backoff', execMode: 'CODE' },
  { regex: /Cannot find module|ERR_MODULE_NOT_FOUND|import.*failed/i, signal: 'module_not_found', description: 'module not found with inline fallback', category: 'REPAIR', severity: 'HIGH', steps: ['catch module error', 'check name/path', 'inline fallback', 'friendly error'], algorithm: 'module_fallback', execMode: 'CODE' },
  { regex: /ENOENT|no such file|not found|does not exist/i, signal: 'file_not_found', description: 'file not found with path fallback', category: 'REPAIR', severity: 'MEDIUM', steps: ['check file exists', 'try common paths', 'friendly error'], algorithm: 'file_exists_check', execMode: 'CODE' },
  { regex: /encoding|UTF-?8|GBK|charset|乱码/i, signal: 'encoding_error', description: 'encoding error forced UTF-8', category: 'REPAIR', severity: 'MEDIUM', steps: ['detect encoding', 'force UTF-8 decode', 'verify result'], algorithm: 'force_utf8', execMode: 'CODE' },
  { regex: /loop|iteration|重复|多次.*失败/i, signal: 'repeated_failure', description: 'repeated failure with circuit breaker', category: 'OPTIMIZE', severity: 'MEDIUM', steps: ['count failures', 'trip breaker threshold', 'return cached'], algorithm: 'circuit_breaker', execMode: 'WORKFLOW' },
  { regex: /SyntaxError|TypeError.*undefined|Cannot read property/i, signal: 'null_reference', description: 'null reference with defensive checks', category: 'REPAIR', severity: 'HIGH', steps: ['locate null ref', 'add undefined check', 'provide default'], algorithm: 'null_check', execMode: 'CODE' },
  { regex: /memory.*leak|heap|OutOfMemory|Maximum call stack/i, signal: 'memory_leak', description: 'memory leak with resource cleanup', category: 'REPAIR', severity: 'HIGH', steps: ['detect memory error', 'add cleanup', 'set limits'], algorithm: 'resource_cleanup', execMode: 'CODE' },
];

function detectSignal(text) { for (const p of PATTERNS) { if (p.regex.test(text)) return p.signal; } return null; }

function analyzeAndGenerateGenes(ctx, strategy) {
  const text = flattenContext(ctx);
  return PATTERNS
    .filter(p => p.regex.test(text))
    .filter(p => strategy === 'repair-only' ? p.category === 'REPAIR' : true)
    .filter(p => strategy === 'innovate' ? (p.category === 'REPAIR' && p.severity === 'HIGH') || p.category !== 'REPAIR' : true)
    .map(p => ({
      signal: p.signal, taskType: 'AUTO_REPLY',
      displayName: p.signal.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
      description: p.description, category: p.category,
      strategy: { steps: p.steps, algorithm: p.algorithm, execMode: p.execMode, gdiScore: { HIGH: 75, MEDIUM: 65, LOW: 55 }[p.severity] || 65 },
      confidence: { HIGH: 80, MEDIUM: 60, LOW: 40 }[p.severity] || 60,
      usageCount: 0, signals: [p.signal],
    }));
}

// =============================================================================
// Gene Selector（TF-IDF 语义相似度）
// =============================================================================

function loadLocalGenes() { const f = path.join(CACHE_DIR, 'assets', 'genes.json'); if (!fs.existsSync(f)) return []; try { return JSON.parse(fs.readFileSync(f, 'utf-8')); } catch { return []; } }
function saveLocalGenes(genes) { const dir = path.join(CACHE_DIR, 'assets'); if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true }); fs.writeFileSync(path.join(dir, 'genes.json'), JSON.stringify(genes, null, 2), 'utf-8'); }

const STOP_WORDS = new Set(['the','and','for','with','from','that','this','into','when','are','was','has','had','not','but','its','can','will','all','any','use','may','also','should','would','could']);
function tokenize(text) { return String(text||'').toLowerCase().replace(/[^a-z0-9_\-]+/g,' ').split(/\s+/).filter(w=>w.length>=2&&!STOP_WORDS.has(w)); }
function tf(tokens) { const m={}; for (const t of tokens) m[t]=(m[t]||0)+1; return m; }
function cosine(a,b) { const keys=new Set([...Object.keys(a),...Object.keys(b)]); let dot=0,nA=0,nB=0; for(const k of keys){dot+=(a[k]||0)*(b[k]||0);nA+=(a[k]||0)**2;nB+=(b[k]||0)**2;} return nA&&nB?dot/(Math.sqrt(nA)*Math.sqrt(nB)):0; }

function scoreGene(signals, gene) {
  const sigTokens = tokenize(signals.join(' '));
  const geneTokens = tokenize([...(gene.signals||[]),...(gene.signals_match||[]),gene.summary||'',gene.displayName||'',gene.name||''].join(' '));
  if (!sigTokens.length||!geneTokens.length) return 0;
  return cosine(tf(sigTokens), tf(geneTokens));
}

function selectGenes(signals, category, options = {}) {
  const { minScore=0.2, maxResults=3 } = options;
  const genes = loadLocalGenes();
  if (!genes.length) return [];
  return genes
    .filter(g=>!category||g.category===category||(category==='optimize'&&!g.category)||(category==='repair'&&g.category==='REPAIR'))
    .map(g=>({ gene:g, score: scoreGene(signals,g) }))
    .filter(r=>r.score>=minScore)
    .sort((a,b)=>b.score-a.score)
    .slice(0,maxResults);
}

// =============================================================================
// Canary Validation
// =============================================================================

async function validateGene(gene) {
  const checks=[], errors=[], warnings=[];
  try { loadCredentials(); checks.push({ name:'api_key_valid', passed:true }); } catch { errors.push({ name:'api_key_valid', message:'API key not configured' }); }
  if (!gene.description||gene.description.length<10) errors.push({ name:'description', message:'Gene description too short' });
  else checks.push({ name:'description', passed:true });
  const steps=gene.strategy?.steps||[];
  if (!steps.length) errors.push({ name:'strategy_steps', message:'No steps defined' });
  else if (steps.length<=10) checks.push({ name:'strategy_steps', passed:true, detail:steps.length+' steps' });
  try { const r=await fetch('https://singularity.mba/api/me',{method:'GET',headers:{Authorization:'Bearer '+loadCredentials().forum_api_key},signal:AbortSignal.timeout(5000)}); if(!r.ok&&r.status===401) errors.push({name:'api_reachable',message:'API 401'}); else checks.push({name:'api_reachable',passed:true}); } catch(e){warnings.push({name:'api_reachable',message:e.message});}
  const score=checks.length?(checks.length-errors.length)/checks.length:0;
  return { passed:errors.length===0&&score>=0.7, score, checks, errors, warnings };
}

// =============================================================================
// Personality 状态机
// =============================================================================

const PERS_FILE=path.join(CACHE_DIR,'personality.json');
function loadPersonality() { if(!fs.existsSync(PERS_FILE)) return defaultPersonality(); try{return{...defaultPersonality(),...JSON.parse(fs.readFileSync(PERS_FILE,'utf-8'))};}catch{return defaultPersonality();} }
function defaultPersonality() { return{iterations:0,steady_state_cycles:0,stagnation_threshold:3,stagnation_detected:false,stagnation_count:0,current_recommendation:null,last_recommendation_change:null,avg_candidates:0,total_published:0,total_rejected:0,total_skipped:0,created_at:new Date().toISOString()}; }
function savePersonality(p){if(!fs.existsSync(CACHE_DIR))fs.mkdirSync(CACHE_DIR,{recursive:true});fs.writeFileSync(PERS_FILE,JSON.stringify(p,null,2),'utf-8');}
function updatePersonality({published=0,candidates=0,skipped=0,rejected=0,signals=[]}){const p=loadPersonality();p.iterations++;p.total_published+=published;p.total_skipped+=skipped;p.total_rejected+=rejected;p.avg_candidates=(p.avg_candidates*(p.iterations-1)+candidates)/p.iterations;if(!published&&!candidates){p.steady_state_cycles++;p.stagnation_count++;}else{p.steady_state_cycles=0;p.stagnation_count=0;}if(p.stagnation_count>=p.stagnation_threshold&&!p.stagnation_detected){p.stagnation_detected=true;p.current_recommendation=p.avg_candidates<1?'innovate':'harden';p.last_recommendation_change=new Date().toISOString();p.stagnation_signals=signals.slice(0,5);}if(signals.length>0&&p.stagnation_detected){p.stagnation_detected=false;p.stagnation_count=0;}savePersonality(p);return p;}
function getRecommendedStrategy(){const p=loadPersonality();if(p.stagnation_detected)return{strategy:p.current_recommendation||'harden',reason:'stagnation',count:p.stagnation_count};if(p.avg_candidates<1&&p.iterations>5)return{strategy:'innovate',reason:'low_rate'};return{strategy:'balanced',reason:'normal'};}

// =============================================================================
// Config Drift
// =============================================================================

const CONFIG_BASE=path.join(CACHE_DIR,'config-baseline.json');
function hashStr(s){let h=5381;for(let i=0;i<s.length;i++){h=((h<<5)+h)+s.charCodeAt(i);h=h&h;}return Math.abs(h).toString(16);}
function snapshotConfig(){const paths=[path.join(os.homedir(),'.openclaw','openclaw.json'),path.join(os.homedir(),'.config','singularity-forum','credentials.json')];const snap={};for(const fp of paths){if(fs.existsSync(fp))try{snap[fp]=hashStr(fs.readFileSync(fp,'utf-8'));}catch{}}if(!fs.existsSync(CACHE_DIR))fs.mkdirSync(CACHE_DIR,{recursive:true});fs.writeFileSync(CONFIG_BASE,JSON.stringify(snap,null,2),'utf-8');}
function detectConfigDrift(){if(!fs.existsSync(CONFIG_BASE))return{drifted:false};try{const base=JSON.parse(fs.readFileSync(CONFIG_BASE,'utf-8'));const paths=Object.keys(base);const changes=[];for(const fp of paths){if(!fs.existsSync(fp)){changes.push({path:fp,type:'deleted'});continue;}try{const h=hashStr(fs.readFileSync(fp,'utf-8'));if(h!==base[fp])changes.push({path:fp,type:'changed'});}catch{}}return{drifted:changes.length>0,changes};}catch{return{drifted:false};}}

// =============================================================================
// Forum Skill Update
// =============================================================================

const SKILL_META=path.join(CACHE_DIR,'skill-meta.json');
function getSkillMeta(){if(!fs.existsSync(SKILL_META))return{version:'0.0.0',lastCheck:null};try{return JSON.parse(fs.readFileSync(SKILL_META,'utf-8'));}catch{return{version:'0.0.0',lastCheck:null};}}
function saveSkillMeta(m){if(!fs.existsSync(CACHE_DIR))fs.mkdirSync(CACHE_DIR,{recursive:true});fs.writeFileSync(SKILL_META,JSON.stringify(m,null,2),'utf-8');}
async function checkForumSkillUpdate(apiKey){const meta=getSkillMeta();const now=Date.now();if(meta.lastCheck&&now-meta.lastCheck<6*3600000)return{checked:false,hasUpdate:false};try{const resp=await fetch(FORUM_BASE+'/api/skills?name=singularity-forum&limit=5',{headers:{Authorization:'Bearer '+apiKey}});const data=await resp.json();const skill=(data.data||[]).find(s=>s.name==='singularity-forum');if(!skill){saveSkillMeta({...meta,lastCheck:now});return{checked:true,hasUpdate:false};}const cmp=(a,b)=>{const p=a.split('.').map(Number),q=b.split('.').map(Number);for(let i=0;i<Math.max(p.length,q.length);i++){if((p[i]||0)>(q[i]||0))return 1;if((p[i]||0)<(q[i]||0))return-1;}return 0;};const hasUpdate=skill.version&&cmp(skill.version,meta.version)>0;saveSkillMeta({version:skill.version||meta.version,lastCheck:now,skillId:skill.id});return{checked:true,hasUpdate,latestVersion:skill.version,currentVersion:meta.version,skillId:skill.id};}catch(e){return{checked:true,hasUpdate:false,error:e.message};}}

// =============================================================================
// Hub 心跳
// =============================================================================

async function sendHeartbeat(cred,status='idle'){try{const resp=await fetch(FORUM_BASE+'/api/evomap/a2a/heartbeat',{method:'POST',headers:{Authorization:'Bearer '+cred.forum_api_key,'Content-Type':'application/json'},body:JSON.stringify({node_status:status,agent_id:cred.openclaw_agent_id})});const data=await resp.json();return{success:resp.ok,tasks:data.tasks||[]};}catch(e){return{success:false,tasks:[]};}}

// =============================================================================
// Gene 发布
// =============================================================================

async function publishCandidate(candidate,apiKey,agentId){
  const name=candidate.signal+'_v'+Date.now();
  try{
    const result=await publishGene(apiKey,{name,displayName:candidate.displayName||candidate.signal,description:candidate.description||candidate.signal,taskType:candidate.taskType||'AUTO_REPLY',category:candidate.category||'REPAIR',signals:candidate.signals||[candidate.signal],execMode:candidate.strategy?.execMode||'CODE',strategy:{description:candidate.description||candidate.signal,steps:candidate.strategy?.steps||[],algorithm:candidate.strategy?.algorithm},gdiScore:candidate.strategy?.gdiScore||candidate.gdiScore||70,confidence:candidate.confidence||60,usageCount:0,sourceAgentId:agentId,version:'1.0.0'});
    log('INFO','evolver','Published: '+candidate.displayName);
    savePublishedSignal(candidate.signal);
    recordChange(candidate.displayName,'published',{geneId:result.id,signal:candidate.signal});
    writeEvent('gene_published',candidate.displayName,{geneId:result.id,signal:candidate.signal});
    return{success:true,geneId:result.id};
  }catch(err){log('ERROR','evolver','Failed: '+candidate.displayName+' - '+err.message);writeEvent('gene_failed',candidate.displayName,{signal:candidate.signal,error:err.message});return{success:false,error:err.message};}
}
async function checkGeneExists(signal,apiKey){try{const resp=await fetchGenes(apiKey,{limit:50});return resp.genes.some(g=>g.signals?.includes(signal));}catch{return false;}}

// =============================================================================
// Review 模式
// =============================================================================

async function promptReview(q){const rl=createInterface({input:process.stdin,output:process.stdout});return new Promise(res=>{rl.question(q,ans=>{rl.close();res(ans.trim());});});}
async function reviewCandidates(candidates){
  console.log('\n=== Review Mode: Pending Genes ===\n');
  for(const[i,c]of candidates.entries()){const gene=c.gene||c;console.log(`${i+1}. ${gene.displayName} [${gene.category}] [GDI=${gene.strategy?.gdiScore||'?'}]`);console.log(`   Signal: ${gene.signal}  Algorithm: ${gene.strategy?.algorithm||'N/A'}`);console.log(`   Steps: ${(gene.strategy?.steps||[]).join(' -> ')}`);console.log('');}
  const answer=await promptReview('Publish all? (y/n/p[ublish num]): ');
  if(answer.toLowerCase()==='y')return candidates;
  if(answer.toLowerCase()==='n')return[];
  if(answer.toLowerCase().startsWith('p')){const nums=answer.substring(1).split(',').map(n=>parseInt(n.trim())-1).filter(n=>n>=0&&n<candidates.length);return nums.map(i=>candidates[i]).filter(Boolean);}
  return[];
}

// =============================================================================
// Phase 1: 分析 + 选择 + Canary
// =============================================================================

export async function prepareEvolution(opts={}){
  const{strategy='balanced',force=false,days=3}=opts;
  const start=Date.now();
  let cred;try{cred=loadCredentials();}catch{return{phase:'prepare',error:'credentials missing',duration:Date.now()-start};}
  log('INFO','evolver','Phase1: analysis [strategy='+strategy+']');
  const ctx=collectContext(days);
  const toolErrors=ctx.toolErrors?.length||0;
  log('INFO','evolver','Context: '+ctx.memoryFiles.length+' files, '+ctx.recentErrors.length+' errors, '+toolErrors+' tool errors');

  // Config drift
  try{const d=detectConfigDrift();if(d.drifted)console.log('[Config] Drift:',d.changes.map(c=>c.path).join(','));}catch{}

  // Personality 推荐策略
  let effectiveStrategy=strategy;
  try{const rec=getRecommendedStrategy();if(rec.reason==='stagnation'&&strategy==='balanced'){effectiveStrategy=rec.strategy;console.log('[Personality] Stagnation, switching to: '+effectiveStrategy);}}catch{}

  // Emergency 自适应
  const emerg=['network_timeout','auth_failure','rate_limit','null_reference','memory_leak'];
  if(ctx.recentErrors.some(e=>emerg.some(s=>e.toLowerCase().includes(s)))&&effectiveStrategy==='balanced'){effectiveStrategy='repair-only';console.log('[Evo] Emergency, auto-switch to repair-only');}

  // 从工具错误提取信号
  const toolSigs=ctx.toolErrors.map(e=>{for(const p of PATTERNS){if(p.regex.test(e))return p.signal;}return null;}).filter(Boolean);
  const allSigs=[...new Set([...ctx.recentErrors.map(detectSignal).filter(Boolean),...toolSigs])];

  if(allSigs.length===0){
    writeEvent('no_candidates','',{phase:1,toolErrors});
    return{phase:'prepare',analyzed:ctx.memoryFiles.length,toolErrors,candidates:0,pending:false,duration:Date.now()-start};
  }

  // Selector + 新基因候选
  const generated=analyzeAndGenerateGenes(ctx,effectiveStrategy);
  let selected=[];
  try{selected=selectGenes(allSigs,effectiveStrategy,{minScore:0,maxResults:3});log('INFO','evolver','Selector: '+selected.length+' local, generated: '+generated.length+' total');}catch(e){console.log('[DEBUG] selector error:',e.message);}
  console.log('[DEBUG] selected:', selected.length, 'generated:', generated.length);
  console.log('[DEBUG] generated signals:', generated.map(g=>g.signal).join(','));
  const unique=[];
  for(const sel of selected){if(!wasRecentlyPublished(sel.gene?.signal))unique.push(sel);}
  console.log('[DEBUG] after selected loop, unique:', unique.length);
  for(const c of generated){const sig=c.signal||'';if(unique.some(s=>(s.gene?.signal||s.signal||'')===sig)){console.log('[DEBUG] skip duplicate signal:',sig);continue;}if(!force&&wasRecentlyPublished(sig)){console.log('[DEBUG] skip recently published:',sig);continue;}console.log('[DEBUG] checking gene exists:',sig);const exists=await checkGeneExists(sig,cred.forum_api_key);console.log('[DEBUG] exists:',exists);if(!exists)unique.push({gene:c,score:(c.strategy?.gdiScore||70)/100,selected:false});}
  console.log('[DEBUG] unique candidates:', unique.length, '|', unique.map(u=>(u.gene?.displayName||u.gene?.signal||'?')).join(' | '));

  // ========================================================================
  // 【新增】Hub 搜索：内部闭环第二步 — 从 singularity.mba 拉取匹配基因
  // ========================================================================
  const hubCandidates = [];
  const signalsForHub = allSigs.filter(s => !wasRecentlyPublished(s));
  if (signalsForHub.length > 0 && signalsForHub.length <= 10) {
    console.log('[Hub] Searching singularity.mba for signals:', signalsForHub.join(', '));
    try {
      const hubResults = [];
      // 并发搜索所有信号（分批，每批3个避免超限）
      for (let i = 0; i < signalsForHub.length; i += 3) {
        const batch = signalsForHub.slice(i, i + 3);
        const results = await Promise.allSettled(
          batch.map(s => hubSearchMod.hubSearch([s], { threshold: 0.6, timeoutMs: 6000 }))
        );
        for (const r of results) {
          if (r.status === 'fulfilled' && r.value && r.value.hit) {
            hubResults.push({ ...r.value, signal: r.value.signals?.[0] || batch[0] });
          }
        }
        await new Promise(r => setTimeout(r, 300));
      }

      for (const hr of hubResults) {
        if (!hr.hit || !hr.match) continue;
        // 判断该 Hub 基因是否值得 ingest
        const localHist = signalMatcher.getLocalGeneHistory(hr.signal);
        if (localHist && localHist.outcome === 'success' && (localHist.localConfidence || 0) >= (hr.score * 100 || 0)) {
          console.log('[Hub] Skip (local better): ' + hr.signal);
          continue;
        }
        // Ingest 到本地基因库
        try {
          const ingested = ingestGene.ingestGene(hr.match);
          hubCandidates.push({
            gene: ingested,
            score: hr.score || 0.7,
            selected: false,
            fromHub: true,
          });
          console.log('[Hub] Ingested: ' + ingested.displayName + ' (score=' + hr.score + ')');
        } catch (e) {
          console.log('[Hub] Ingest error: ' + e.message);
        }
      }
      if (hubCandidates.length > 0) {
        log('INFO', 'evolver', 'Hub: ingested ' + hubCandidates.length + ' genes from singularity.mba');
        appendEventJsonl({ type: 'hub_ingestion', count: hubCandidates.length, signals: signalsForHub });
      }
    } catch (e) {
      console.log('[Hub] Search failed (non-fatal): ' + e.message);
    }
  }

  if(unique.length===0){
    writeEvent('no_candidates','',{phase:1,toolErrors});
    return{phase:'prepare',analyzed:ctx.memoryFiles.length,toolErrors,candidates:0,pending:false,duration:Date.now()-start};
  }

  // Canary 验证
  console.log('[DEBUG] unique candidates:', unique.length, unique.map(u=>(u.gene?.displayName||u.displayName||'?')+(u.gene?.signal||u.signal?' ['+u.gene?.signal+']':'')));
  const canaryResults=[];let passedGenes=[];
  for(const sel of unique){
    const gene=sel.gene||sel;
    try{const vr=await validateGene(gene);canaryResults.push({gene,result:vr});if(vr.passed){passedGenes.push(sel);log('INFO','evolver','Canary PASSED: '+gene.displayName+' (score='+vr.score.toFixed(2)+')');}else{log('WARN','evolver','Canary FAILED: '+gene.displayName);}}catch(e){log('ERROR','evolver','Canary error: '+e.message);passedGenes.push(sel);}
  }

  if(passedGenes.length===0){
    log('INFO','evolver','All genes failed canary');
    updatePersonality({published:0,candidates:unique.length,skipped:unique.length,rejected:unique.length,signals:allSigs});
    return{phase:'prepare',analyzed:ctx.memoryFiles.length,toolErrors,candidates:0,canaryFailed:true,duration:Date.now()-start};
  }

  const toPublish=force?passedGenes:passedGenes.filter(s=>(s.score||0)>=0.2);
  const runId=createPendingRun(toPublish.map(s=>({...s.gene||s,_score:s.score||0})),effectiveStrategy,hubCandidates);
  log('INFO','evolver','Phase1 done: runId='+runId+', '+toPublish.length+' genes (local='+toPublish.length+', hub='+hubCandidates.length+')');

  return{phase:'prepare',runId,analyzed:ctx.memoryFiles.length,toolErrors,candidates:toPublish.length,pending:true,candidatesList:passedGenes,hubCandidates,canaryResults,strategy:effectiveStrategy,force,duration:Date.now()-start,gitAvailable:isGitRepo()};
}

// =============================================================================
// Phase 2: Solidify
// =============================================================================

export async function solidifyRun(runId=null,opts={}){
  const{confirm=true,reason=null, hubCandidates=[]}=opts;
  const start=Date.now();
  const pending=getPendingRun();
  if(!pending)return{phase:'solidify',error:'no pending run',duration:Date.now()-start};
  const activeRunId=runId||pending.run_id;
  if(!confirm){rejectRun(activeRunId,reason||'manual');log('INFO','evolver','Rejected runId='+activeRunId);return{phase:'solidify',runId:activeRunId,confirmed:false,reason,duration:Date.now()-start};}
  let cred;try{cred=loadCredentials();}catch{return{phase:'solidify',error:'credentials missing'};}
  let agentId='cmnj1o8hw000fpu9hyog563zi';
  try{const r=await fetch(FORUM_BASE+'/api/me',{headers:{Authorization:'Bearer '+cred.forum_api_key}});const d=await r.json();if(d?.id)agentId=d.id;}catch{}
  const candidates=pending.candidates||[];
  log('INFO','evolver','Phase2: publishing '+candidates.length+' local candidates');

  // ========================================================================
  // 【升级】Solidify 门控：blast radius + 约束检查 + LLM review
  // ========================================================================
  let preSolidifyOk = true;
  try {
    // 先做一次全局 blast radius 预检（不对应具体 gene，只是看当前工作区状态）
    const preBlast = solidify.computeBlastRadius(path.join(os.homedir(), 'Desktop', 'singularity'));
    console.log('[Solidify] Pre-check blast: ' + preBlast.files + ' files, ' + preBlast.lines + ' lines');
  } catch (e) {
    console.warn('[Solidify] Pre-check failed (non-fatal): ' + e.message);
  }

  let published=0,skipped=0,rejected=0;
  const publishedSigs=new Set();
  for(const c of candidates){
    if(publishedSigs.has(c.signal)){skipped++;continue;}
    const gene = c;

    // --- Solidify gate ---
    let gatePassed = true;
    try {
      // Blast + constraint check
      const blastReport = solidify.solidifyGene(gene, { skipValidation: false, dryRun: true });
      if (!blastReport.overall) {
        console.log('[Solidify] ❌ REJECTED: ' + (gene.displayName||gene.signal) + ' — ' + (blastReport.failureReason||'constraint/validation failed'));
        rejected++;
        gatePassed = false;
        // 写失败事件
        writeEvent('gene_rejected', gene.displayName||gene.signal, { reason: blastReport.failureReason });
        continue;
      }
      console.log('[Solidify] ✅ PASSED: ' + (gene.displayName||gene.signal));
    } catch (e) {
      console.warn('[Solidify] Gate error (allow through): ' + e.message);
    }

    // --- LLM Review（可选）---
    if (gatePassed) {
      try {
        const llmResult = await llmReview.runLlmReview(gene);
        if (llmResult.ok && llmResult.safe === false) {
          console.log('[Solidify] ❌ LLM REJECTED: ' + (gene.displayName||gene.signal) + ' — ' + llmResult.reason);
          rejected++;
          gatePassed = false;
          writeEvent('gene_llm_rejected', gene.displayName||gene.signal, { reason: llmResult.reason });
          continue;
        }
        if (!llmResult.ok) {
          console.warn('[Solidify] LLM review error (allow through): ' + llmResult.reason);
        } else {
          console.log('[Solidify] 🤖 LLM: ' + llmResult.reason);
        }
      } catch (e) {
        console.warn('[Solidify] LLM review failed (allow through): ' + e.message);
      }
    }

    if (!gatePassed) continue;

    // --- Publish ---
    const result=await publishCandidate(gene,cred.forum_api_key,agentId);
    if(result.success){publishedSigs.add(gene.signal);published++;if(isGitRepo()){const r=gitCommit('evo.solidify: '+(gene.displayName||gene.signal)+' signal='+gene.signal);if(r.success)log('INFO','evolver','Git: '+r.commit);}}
    await new Promise(r=>setTimeout(r,500));
  }

  // ========================================================================
  // 【新增】Hub 基因 Apply — 内部闭环第三步
  // ========================================================================
  let hubApplied = 0, hubFailed = 0;
  const pendingHubCandidates = pending.hubCandidates || hubCandidates;
  if (pendingHubCandidates && pendingHubCandidates.length > 0) {
    log('INFO', 'evolver', 'Phase2b: applying ' + pendingHubCandidates.length + ' Hub genes');
    for (const item of pendingHubCandidates) {
      const gene = item.gene || item;
      if (!gene || !gene.id) continue;
      try {
        const result = await hubSearchMod.applyGene(gene, { targetPath: os.homedir() + '/.openclaw/workspace' });
        if (result.success) {
          hubApplied++;
          // 记录本地胶囊
          capsuleRecorder.recordHubCapsule(gene, { success: true, capsuleId: result.capsuleId });
          writeEvent('hub_capsule_applied', gene.displayName, { geneId: gene.id, capsuleId: result.capsuleId });
          console.log('[HubApply] Success: ' + gene.displayName + ' -> capsule=' + result.capsuleId);
        } else {
          hubFailed++;
          capsuleRecorder.recordHubCapsule(gene, { success: false, error: result.error });
          console.log('[HubApply] Failed: ' + gene.displayName + ' -> ' + result.error);
        }
      } catch (e) {
        hubFailed++;
        console.log('[HubApply] Error: ' + gene.displayName + ' -> ' + e.message);
      }
      await new Promise(r => setTimeout(r, 800));
    }
    log('INFO', 'evolver', 'Phase2b done: applied=' + hubApplied + ', failed=' + hubFailed);
  }

  updatePersonality({published,candidates:candidates.length,skipped,rejected,signals:candidates.map(c=>c.signal)});
  confirmRun(activeRunId);
  const duration=Date.now()-start;
  writeEvent('solidified','',{runId:activeRunId,published,skipped,rejected,duration,hubApplied,hubFailed});
  log('INFO','evolver','Phase2 done: published='+published+' skipped='+skipped+' rejected='+rejected+' | Hub: applied='+hubApplied+' failed='+hubFailed);
  return{phase:'solidify',runId:activeRunId,confirmed:true,published,skipped,rejected,hubApplied,hubFailed,duration};
}

// =============================================================================
// 合并运行
// =============================================================================

export async function runEvolution(opts={}){
  const{strategy='balanced',review=false,force=false,days=3,autoSolidify=true}=opts;
  const prep=await prepareEvolution({strategy,force,days});
  if(prep.error)return prep;
  if(!prep.pending)return{...prep,phase:'complete'};
  let toPublish=prep.candidatesList;
  if(review){
    if(!process.stdin.isTTY){console.error('Review requires TTY');return{...prep,phase:'prepare',reviewAborted:true};}
    toPublish=await reviewCandidates(prep.candidatesList);
    if(!toPublish.length){rejectRun(prep.runId,'review_aborted');return{...prep,phase:'review_aborted',candidates:0};}
  }
  if(!autoSolidify)return{...prep,phase:'ready',awaitingSolidify:true,runId:prep.runId};
  return await solidifyRun(prep.runId, { hubCandidates: prep.hubCandidates || [] });
}

// =============================================================================
// Daemon Loop（带 Preflight Guards + Circuit Breaker + Idle Gating）
// =============================================================================

let SHUTDOWN=false;let LAST_HB=0;const HB_INT=6*60*1000;const MIN_SLEEP=5000;const MAX_SLEEP=4*3600000;

async function sleepFor(ms){for(let e=0;e<ms&&!SHUTDOWN;e+=30000)await new Promise(r=>setTimeout(r,Math.min(30000,ms-e)));}

async function daemonLoop(intervalMs=3600000){
  let iterations=0;let curSleep=Math.max(MIN_SLEEP,intervalMs);
  if(!acquireLock()){console.error('[Daemon] Already running. Exiting.');process.exitCode=1;return;}
  process.on('exit',()=>releaseLock());
  process.on('SIGINT',()=>{SHUTDOWN=true;releaseLock();});
  process.on('SIGTERM',()=>{SHUTDOWN=true;releaseLock();});

  const cycleNum = idleScheduler.getNextCycleId();
  console.log('\n=== Evolver Daemon v7 ===');
  console.log('Interval: '+Math.round(intervalMs/60000)+'min  Git: '+(isGitRepo()?'yes':'no')+'  Health: active  Dormant: active  SkillUpdate: active');
  console.log('SessionReader: '+sessionReader.SESSIONS_DIR+'  Active sessions: '+sessionReader.getActiveSessionCount()+'\n');

  while(!SHUTDOWN){
    iterations++;
    const now=Date.now();
    console.log('\n--- #'+iterations+' ['+new Date().toLocaleTimeString()+'] ---');

    // ====================================================================
    // Preflight Guards（系统负载 / 活跃会话 / Loop Gating）
    // ====================================================================
    const preflight = await idleScheduler.runPreflightChecks();
    if (preflight.abort) {
      console.log('[Preflight] Abort: ' + preflight.reason + ' — backing off ' + Math.round((preflight.backoffMs||0)/60000) + 'min');
      await sleepFor(preflight.backoffMs || 60000);
      continue;
    }

    // Circuit breaker（连续 repair 失败 → 强制 innovate）
    idleScheduler.checkRepairLoopCircuitBreaker();

    const health=getHealthStatus();
    if(!health.ok)console.log('[Health] '+health.issues.join(', '));
    if(isOverloaded(0.8)||health.rssMb>500||health.diskFreeGb<1){curSleep=Math.min(MAX_SLEEP,curSleep*2);console.log('[Health] Resource pressure, back off '+Math.round(curSleep/60000)+'min');await sleepFor(curSleep);continue;}

    // Solidify pending run from previous cycle
    if(isPendingSolidify()){
      const p=getPendingRun();
      console.log('[Pending] Run from '+p?.timestamp+', solidifying...');
      const sr=await solidifyRun();
      console.log('[Pending] Done: published='+sr.published+' rejected='+sr.rejected);
    }

    // Skill update check + Hub heartbeat
    try{
      const cred=loadCredentials();
      const meta=getSkillMeta();
      const skillUpdateDue=!meta.lastCheck||(Date.now()-meta.lastCheck>3600000);
      if(skillUpdateDue){
        const upd=await checkForumSkillUpdate(cred.apiKey);
        if(upd.checked&&upd.hasUpdate)console.log('[Update] v'+upd.latestVersion+' available, current: '+upd.currentVersion);
      }
      if(now-LAST_HB>HB_INT){
        const hb=await sendHeartbeat(cred,'evolving');
        LAST_HB=now;
        console.log('[Hub] heartbeat '+(hb.success?'ok':'failed')+(hb.tasks?.length?' ('+hb.tasks.length+' tasks)':''));
      }
    }catch(e){console.log('[Error] '+e.message);}

    // ====================================================================
    // 主循环：收集 session 信号 → 运行进化
    // ====================================================================
    const t0=Date.now();
    let result=null;
    try{
      result=await runEvolution({strategy:'balanced',review:false,force:false,days:3});
      const dt=Date.now()-t0;
      const cycleId = '#' + (iterations);

      // 检查结果，决定下次休眠时长
      if((result.candidates??-1)===0){
        idleScheduler.writeDormantHypothesis({ reason: 'no_signals', candidateSignals: [] });
        curSleep=Math.min(MAX_SLEEP,curSleep*2);
        console.log('[Dormant] No candidates, back off '+Math.round(curSleep/60000)+'min');
      } else if(result.phase==='prepare'&&result.pending){
        idleScheduler.writeDormantHypothesis({ reason: 'found_signals', candidateSignals: result.candidatesList?.map(c=>c.signal)||[] });
        curSleep=Math.max(MIN_SLEEP,Math.floor(intervalMs/2));
      } else {
        curSleep=Math.max(MIN_SLEEP,Math.floor(intervalMs/2));
      }

      // Hub fetch 节流记录
      idleScheduler.recordHubFetch();

      console.log('Result: phase='+result.phase+' published='+result.published+' skipped='+result.skipped+' rejected='+result.rejected+' candidates='+result.candidates+' ['+dt+'ms]');
    }catch(e){
      console.error('[Error] '+e.message);
      curSleep=Math.min(MAX_SLEEP,curSleep*2);
    }

    await sleepFor(Math.min(curSleep,intervalMs));
  }
  releaseLock();console.log('Daemon stopped.');process.exitCode=0;
}

// =============================================================================
// CLI
// =============================================================================

function printResult(r){console.log('\n=== Evolution Result ===');console.log('Phase: '+(r.phase||'?'));if(r.phase==='prepare'&&!r.pending)console.log('Status: No new genes');else if(r.phase==='prepare'&&r.pending)console.log('Run ID: '+r.runId+' | Candidates: '+r.candidates+' | Strategy: '+r.strategy);else if(r.phase==='solidify'){console.log('Run ID: '+r.runId+' | Confirmed: '+r.confirmed);if(r.confirmed)console.log('Published: '+r.published+' | Skipped: '+r.skipped);}else if(r.phase==='complete'){console.log('Published: '+(r.published||0)+' | Candidates: '+(r.candidates||0));}console.log('Duration: '+(r.duration||0)+'ms  Git: '+(r.gitAvailable?'yes':'no'));if(r.errors?.length)console.log('Errors: '+r.errors.join(', '));}

const argv=process.argv.slice(2);
const ctx=parseArgs(argv);

async function main(){
  if(argv.includes('--help')||argv.includes('-h')){console.log('Usage: node src/evolver.js [options]');console.log('');console.log('  --strategy=<name>  Strategy: balanced| innovate| harden| repair-only');console.log('  --review           Human-in-the-loop review');console.log('  --auto            Fully automated (Phase1+2)');console.log('  --solidify [id]   Solidify pending run');console.log('  --reject [id]      Reject pending run');console.log('  --status           Show pending run');console.log('  --loop [--interval=N]  Daemon mode');console.log('  --days=N           Memory range (default 3)');console.log('  --force            Skip GDI threshold');console.log('  --help, -h         Show help');process.exitCode=0;return;}
  if(ctx.loop){await daemonLoop(ctx.intervalMs);return;}
  if(argv.includes('--status')){const p=getPendingRun();console.log(p?'Pending: ID='+p.run_id+' candidates='+(p.candidates?.length||0)+' ts='+p.timestamp:'No pending run.');process.exitCode=0;return;}
  if(argv.includes('--solidify')){const rid=argv.find(a=>!a.startsWith('--'));const r=await solidifyRun(rid);printResult(r);process.exitCode=r.confirmed!==false?0:1;return;}
  if(argv.includes('--reject')){const rid=argv.find(a=>!a.startsWith('--'));const r=await solidifyRun(rid,{confirm:false,reason:'manual'});printResult(r);process.exitCode=0;return;}
  const autoSolidify=argv.includes('--auto');
  const result=await runEvolution({strategy:ctx.strategy,review:ctx.review,force:ctx.force,days:ctx.days,autoSolidify});
  printResult(result);process.exitCode=result.error?1:0;
}
main().catch(err=>{console.error('Fatal: '+err.message);process.exitCode=1;});