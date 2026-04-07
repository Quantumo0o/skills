'use strict';

/**
 * gep/index.js — Capability-Evolver 内核统一导出 + singularity 路径适配
 *
 * singularity/moltbook-web 环境专用：
 * - 所有模块从 /opt/moltbook-web/src/lib/evomap/gep/ 加载
 * - 路径指向 /opt/moltbook-web/data/evomap-evolution / evomap-memory
 * - 与 capability-evolver skill 的原始 paths.js 完全兼容
 *
 * 使用方式（engine.ts）：
 *   const gep = require('./gep');
 *   const { extractSignals, getMemoryAdvice, ... } = gep;
 */

const path = require('path');

// ── singularity 环境路径配置 ──────────────────────────────────────────────────
const SINGULARITY_ROOT   = '/opt/moltbook-web';
const SINGULARITY_EVO    = path.join(SINGULARITY_ROOT, 'data', 'evomap-evolution');
const SINGULARITY_MEM    = path.join(SINGULARITY_ROOT, 'data', 'evomap-memory');
const SINGULARITY_ASSETS = path.join(SINGULARITY_ROOT, 'data', 'evomap-assets');
const SINGULARITY_LOGS   = path.join(SINGULARITY_ROOT, 'data', 'evomap-logs');
const GEP_DIR            = path.join(__dirname);

// ── paths.js（内联，兼容原 API） ─────────────────────────────────────────────
function getRepoRoot()         { return SINGULARITY_ROOT; }
function getWorkspaceRoot()    { return SINGULARITY_ROOT; }
function getMemoryDir()        { return SINGULARITY_MEM; }
function getEvolutionDir()     { return SINGULARITY_EVO; }
function getGepAssetsDir()    { return SINGULARITY_ASSETS; }
function getLogsDir()          { return SINGULARITY_LOGS; }
function getEvolverLogPath()   { return path.join(SINGULARITY_LOGS, 'evolver_loop.log'); }
function getSkillsDir()        { return path.join(SINGULARITY_ROOT, 'skills'); }
function getNarrativePath()    { return path.join(SINGULARITY_EVO, 'evolution_narrative.md'); }
function getReflectionLogPath() { return path.join(SINGULARITY_EVO, 'reflection_log.jsonl'); }
function getSessionScope()     { return process.env.EVOLVER_SESSION_SCOPE || null; }

const paths = {
  getRepoRoot, getWorkspaceRoot, getMemoryDir, getEvolutionDir,
  getGepAssetsDir, getLogsDir, getEvolverLogPath, getSkillsDir,
  getNarrativePath, getReflectionLogPath, getSessionScope,
};

// ── 动态 require（延迟加载，避免循环依赖） ───────────────────────────────────
function require_gep(name) {
  try {
    // 先尝试从 gep 目录加载
    return require(path.join(GEP_DIR, name));
  } catch (_) {}
  return null;
}

// ── signals ──────────────────────────────────────────────────────────────────
let _signals = null;
function getSignals() {
  if (!_signals) _signals = require_gep('signals') || require_gep('signals.js');
  return _signals;
}

// ── memoryGraph ───────────────────────────────────────────────────────────────
let _memoryGraph = null;
function getMemoryGraph() {
  if (!_memoryGraph) {
    const mg = require_gep('memoryGraph');
    if (mg) {
      // 注入 singularity 专用路径（覆盖原 module 内的路径逻辑）
      if (mg.memoryGraphPath) {
        const orig = mg.memoryGraphPath;
        mg.memoryGraphPath = function () {
          return path.join(SINGULARITY_EVO, 'memory_graph.jsonl');
        };
      }
      if (mg.memoryGraphStatePath) {
        const orig = mg.memoryGraphStatePath;
        mg.memoryGraphStatePath = function () {
          return path.join(SINGULARITY_EVO, 'memory_graph_state.json');
        };
      }
      // patch: memoryGraph 内部 require('./paths') 的结果要指向 singularity
      // 由于我们已经 patch 了 exported 函数，paths 的其他函数仍需要正常
    }
    _memoryGraph = mg;
  }
  return _memoryGraph;
}

// ── narrativeMemory ──────────────────────────────────────────────────────────
let _narrative = null;
function getNarrative() {
  if (!_narrative) _narrative = require_gep('narrativeMemory') || require_gep('narrativeMemory.js');
  return _narrative;
}

// ── reflection ──────────────────────────────────────────────────────────────
let _reflection = null;
function getReflection() {
  if (!_reflection) _reflection = require_gep('reflection') || require_gep('reflection.js');
  return _reflection;
}

// ── curriculum ──────────────────────────────────────────────────────────────
let _curriculum = null;
function getCurriculum() {
  if (!_curriculum) _curriculum = require_gep('curriculum') || require_gep('curriculum.js');
  return _curriculum;
}

// ── skillDistiller ──────────────────────────────────────────────────────────
let _distiller = null;
function getSkillDistiller() {
  if (!_distiller) _distiller = require_gep('skillDistiller') || require_gep('skillDistiller.js');
  return _distiller;
}

// ── skillPublisher ─────────────────────────────────────────────────────────
let _publisher = null;
function getSkillPublisher() {
  if (!_publisher) _publisher = require_gep('skillPublisher') || require_gep('skillPublisher.js');
  return _publisher;
}

// ── bridge ──────────────────────────────────────────────────────────────────
let _bridge = null;
function getBridge() {
  if (!_bridge) _bridge = require_gep('bridge') || require_gep('bridge.js');
  return _bridge;
}

// ── hubReview ───────────────────────────────────────────────────────────────
let _hubReview = null;
function getHubReview() {
  if (!_hubReview) _hubReview = require_gep('hubReview') || require_gep('hubReview.js');
  return _hubReview;
}

// ── issueReporter ───────────────────────────────────────────────────────────
let _issueReporter = null;
function getIssueReporter() {
  if (!_issueReporter) _issueReporter = require_gep('issueReporter') || require_gep('issueReporter.js');
  return _issueReporter;
}

// ── sanitize ────────────────────────────────────────────────────────────────
let _sanitize = null;
function getSanitize() {
  if (!_sanitize) _sanitize = require_gep('sanitize') || require_gep('sanitize.js');
  return _sanitize;
}

// ── contentHash ─────────────────────────────────────────────────────────────
let _contentHash = null;
function getContentHash() {
  if (!_contentHash) _contentHash = require_gep('contentHash') || require_gep('contentHash.js');
  return _contentHash;
}

// ── deviceId ─────────────────────────────────────────────────────────────────
let _deviceId = null;
function getDeviceId() {
  if (!_deviceId) _deviceId = require_gep('deviceId') || require_gep('deviceId.js');
  return _deviceId;
}

// ── envFingerprint ───────────────────────────────────────────────────────────
let _envFingerprint = null;
function getEnvFingerprint() {
  if (!_envFingerprint) _envFingerprint = require_gep('envFingerprint') || require_gep('envFingerprint.js');
  return _envFingerprint;
}

// ── questionGenerator ───────────────────────────────────────────────────────
let _questionGenerator = null;
function getQuestionGenerator() {
  if (!_questionGenerator) _questionGenerator = require_gep('questionGenerator') || require_gep('questionGenerator.js');
  return _questionGenerator;
}

// ── analyzer ────────────────────────────────────────────────────────────────
let _analyzer = null;
function getAnalyzer() {
  if (!_analyzer) _analyzer = require_gep('analyzer') || require_gep('analyzer.js');
  return _analyzer;
}

// ── mutation ─────────────────────────────────────────────────────────────────
let _mutation = null;
function getMutation() {
  if (!_mutation) _mutation = require_gep('mutation') || require_gep('mutation.js');
  return _mutation;
}

// ── personality ──────────────────────────────────────────────────────────────
let _personality = null;
function getPersonality() {
  if (!_personality) _personality = require_gep('personality') || require_gep('personality.js');
  return _personality;
}

// ── learningSignals ─────────────────────────────────────────────────────────
let _learningSignals = null;
function getLearningSignals() {
  if (!_learningSignals) _learningSignals = require_gep('learningSignals') || require_gep('learningSignals.js');
  return _learningSignals;
}

// ── assetCallLog ────────────────────────────────────────────────────────────
let _assetCallLog = null;
function getAssetCallLog() {
  if (!_assetCallLog) _assetCallLog = require_gep('assetCallLog') || require_gep('assetCallLog.js');
  return _assetCallLog;
}

// ── validationReport ─────────────────────────────────────────────────────────
let _validationReport = null;
function getValidationReport() {
  if (!_validationReport) _validationReport = require_gep('validationReport') || require_gep('validationReport.js');
  return _validationReport;
}

// ── executionTrace ───────────────────────────────────────────────────────────
let _executionTrace = null;
function getExecutionTrace() {
  if (!_executionTrace) _executionTrace = require_gep('executionTrace') || require_gep('executionTrace.js');
  return _executionTrace;
}

// ── 统一导出 ─────────────────────────────────────────────────────────────────
module.exports = {
  // paths
  ...paths,

  // signals（最强信号提取引擎）
  extractSignals: (...args) => { const m = getSignals(); return m ? m.extractSignals(...args) : []; },
  hasOpportunitySignal: (...args) => { const m = getSignals(); return m ? m.hasOpportunitySignal(...args) : false; },

  // memoryGraph（进化记忆知识图谱）
  getMemoryAdvice: (...args) => { const m = getMemoryGraph(); return m ? m.getMemoryAdvice(...args) : null; },
  recordSignalSnapshot: (...args) => { const m = getMemoryGraph(); return m ? m.recordSignalSnapshot(...args) : null; },
  recordHypothesis: (...args) => { const m = getMemoryGraph(); return m ? m.recordHypothesis(...args) : null; },
  recordAttempt: (...args) => { const m = getMemoryGraph(); return m ? m.recordAttempt(...args) : null; },
  recordOutcomeFromState: (...args) => { const m = getMemoryGraph(); return m ? m.recordOutcomeFromState(...args) : null; },
  recordExternalCandidate: (...args) => { const m = getMemoryGraph(); return m ? m.recordExternalCandidate(...args) : null; },
  tryReadMemoryGraphEvents: (...args) => { const m = getMemoryGraph(); return m ? m.tryReadMemoryGraphEvents(...args) : []; },
  computeSignalKey: (...args) => { const m = getMemoryGraph(); return m ? m.computeSignalKey(...args) : ''; },

  // narrativeMemory
  recordNarrative: (...args) => { const m = getNarrative(); return m ? m.recordNarrative(...args) : null; },
  loadNarrativeSummary: (...args) => { const m = getNarrative(); return m ? m.loadNarrativeSummary(...args) : ''; },

  // reflection
  shouldReflect: (...args) => { const m = getReflection(); return m ? m.shouldReflect(...args) : false; },
  buildReflectionContext: (...args) => { const m = getReflection(); return m ? m.buildReflectionContext(...args) : ''; },
  recordReflection: (...args) => { const m = getReflection(); return m ? m.recordReflection(...args) : null; },
  loadRecentReflections: (...args) => { const m = getReflection(); return m ? m.loadRecentReflections(...args) : []; },
  buildSuggestedMutations: (...args) => { const m = getReflection(); return m ? m.buildSuggestedMutations(...args) : []; },

  // curriculum
  generateCurriculumSignals: (...args) => { const m = getCurriculum(); return m ? m.generateCurriculumSignals(...args) : []; },
  markCurriculumProgress: (...args) => { const m = getCurriculum(); return m ? m.markCurriculumProgress(...args) : null; },
  loadCurriculumState: (...args) => { const m = getCurriculum(); return m ? m.loadCurriculumState(...args) : null; },

  // skillDistiller
  collectDistillationData: (...args) => { const m = getSkillDistiller(); return m ? m.collectDistillationData(...args) : null; },
  analyzePatterns: (...args) => { const m = getSkillDistiller(); return m ? m.analyzePatterns(...args) : null; },
  runDistillation: (...args) => { const m = getSkillDistiller(); return m ? m.runDistillation(...args) : null; },
  autoDistillFromFailures: (...args) => { const m = getSkillDistiller(); return m ? m.autoDistillFromFailures(...args) : null; },

  // skillPublisher
  publishSkillToHub: (...args) => { const m = getSkillPublisher(); return m ? m.publishSkillToHub(...args) : null; },
  checkSkillStatus: (...args) => { const m = getSkillPublisher(); return m ? m.checkSkillStatus(...args) : null; },

  // bridge
  renderSessionsSpawnCall: (...args) => { const m = getBridge(); return m ? m.renderSessionsSpawnCall(...args) : null; },
  writePromptArtifact: (...args) => { const m = getBridge(); return m ? m.writePromptArtifact(...args) : null; },

  // hubReview
  runHubReview: (...args) => { const m = getHubReview(); return m ? m.runHubReview(...args) : null; },

  // issueReporter
  maybeReportIssue: (...args) => { const m = getIssueReporter(); return m ? m.maybeReportIssue(...args) : null; },

  // sanitize
  sanitizeForReport: (...args) => { const m = getSanitize(); return m ? m.sanitizeForReport(...args) : ''; },

  // contentHash
  computeContentHash: (...args) => { const m = getContentHash(); return m ? m.computeContentHash(...args) : ''; },

  // deviceId
  getOrCreateDeviceId: (...args) => { const m = getDeviceId(); return m ? m.getOrCreateDeviceId(...args) : null; },

  // envFingerprint
  getEnvFingerprint: (...args) => { const m = getEnvFingerprint(); return m ? m.getEnvFingerprint(...args) : null; },

  // questionGenerator
  generateQuestions: (...args) => { const m = getQuestionGenerator(); return m ? m.generateQuestions(...args) : []; },

  // analyzer
  analyzeFailures: (...args) => { const m = getAnalyzer(); return m ? m.analyzeFailures(...args) : null; },

  // mutation
  normalizeMutation: (...args) => { const m = getMutation(); return m ? m.normalizeMutation(...args) : null; },
  isValidMutation: (...args) => { const m = getMutation(); return m ? m.isValidMutation(...args) : false; },

  // personality
  normalizePersonalityState: (...args) => { const m = getPersonality(); return m ? m.normalizePersonalityState(...args) : null; },
  isValidPersonalityState: (...args) => { const m = getPersonality(); return m ? m.isValidPersonalityState(...args) : false; },

  // learningSignals
  computeLearningSignals: (...args) => { const m = getLearningSignals(); return m ? m.computeLearningSignals(...args) : null; },

  // assetCallLog
  logAssetCall: (...args) => { const m = getAssetCallLog(); return m ? m.logAssetCall(...args) : null; },

  // validationReport
  buildValidationReport: (...args) => { const m = getValidationReport(); return m ? m.buildValidationReport(...args) : null; },

  // executionTrace
  startTrace: (...args) => { const m = getExecutionTrace(); return m ? m.startTrace(...args) : null; },
  endTrace: (...args) => { const m = getExecutionTrace(); return m ? m.endTrace(...args) : null; },

  // raw modules（高级用法）
  modules: {
    get signals()        { return getSignals(); },
    get memoryGraph()    { return getMemoryGraph(); },
    get narrative()      { return getNarrative(); },
    get reflection()     { return getReflection(); },
    get curriculum()    { return getCurriculum(); },
    get distiller()     { return getSkillDistiller(); },
    get publisher()      { return getSkillPublisher(); },
    get bridge()        { return getBridge(); },
    get mutation()       { return getMutation(); },
    get personality()    { return getPersonality(); },
  },

  // 版本信息
  VERSION: '1.0.0-capability-evolver',
  GEP_DIR,
  SINGULARITY_ROOT,
  SINGULARITY_EVO,
  SINGULARITY_MEM,
};
