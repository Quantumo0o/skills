/**
 * singularity GEP Config
 * 所有可调参数集中管理
 */
module.exports = {
  // --- Git ---
  GIT_ROLLBACK_MODE: String(process.env.GIT_ROLLBACK_MODE || 'hard').toLowerCase(),

  // --- Validation ---
  VALIDATION_TIMEOUT_MS:      Number(process.env.VALIDATION_TIMEOUT_MS)      || 60000,
  CANARY_TIMEOUT_MS:          Number(process.env.CANARY_TIMEOUT_MS)          || 30000,
  SOLIDIFY_MAX_RETRIES:       Number(process.env.SOLIDIFY_MAX_RETRIES)       || 2,
  SOLIDIFY_RETRY_INTERVAL_MS: Number(process.env.SOLIDIFY_RETRY_INTERVAL_MS) || 5000,

  // --- Blast radius ---
  BLAST_HARD_CAP_FILES: Number(process.env.EVOLVER_HARD_CAP_FILES) || 60,
  BLAST_HARD_CAP_LINES: Number(process.env.EVOLVER_HARD_CAP_LINES) || 20000,
  BLAST_WARN_RATIO: 0.8,
  BLAST_CRITICAL_RATIO: 2.0,

  // --- Constraint policy ---
  CONSTRAINT_MAX_FILES: Number(process.env.EVOLVER_MAX_FILES) || 20,

  // --- LLM Review ---
  LLM_REVIEW_ENABLED: String(process.env.EVOLVER_LLM_REVIEW || '0') === '1',

  // --- Self-modify ---
  ALLOW_SELF_MODIFY: String(process.env.EVOLVE_ALLOW_SELF_MODIFY || 'false') === 'true',

  // --- Distiller ---
  DISTILLER_MIN_CAPSULES:      Number(process.env.DISTILLER_MIN_CAPSULES)      || 10,
  DISTILLER_INTERVAL_HOURS:    Number(process.env.DISTILLER_INTERVAL_HOURS)    || 24,
  DISTILLER_MIN_SUCCESS_RATE:  Float(process.env.DISTILLER_MIN_SUCCESS_RATE)  || 0.7,

  // --- Hub search ---
  HUB_SEARCH_TIMEOUT_MS:  Number(process.env.HUB_SEARCH_TIMEOUT_MS)  || 8000,
  HUB_MIN_REUSE_SCORE:   Float(process.env.HUB_MIN_REUSE_SCORE)   || 0.72,

  // --- Validation commands ---
  VALIDATION_ALLOWED_PREFIXES: ['node ', 'npm ', 'npx '],
};

function Float(v) {
  const n = Number(v);
  return Number.isFinite(n) ? n : undefined;
}
