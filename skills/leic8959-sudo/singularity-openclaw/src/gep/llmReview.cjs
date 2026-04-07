/**
 * singularity GEP LLM Review
 * 在 solidify 前，用 LLM 判断改动是否合理
 *
 * 对标 capability-evolver/src/gep/llmReview.js
 */
const { LLM_REVIEW_ENABLED } = require('./config.cjs');
const { getRepoRoot } = require('./paths.cjs');
const { captureDiffSnapshot, isGitRepo } = require('./gitOps.cjs');

// ---------------------------------------------------------------------------
// Build review prompt
// ---------------------------------------------------------------------------

function buildLlmReviewPrompt({ gene, diff, context }) {
  const geneSummary = gene
    ? [
        'Gene ID: ' + (gene.id || gene.name || 'unknown'),
        'Category: ' + (gene.category || 'unknown'),
        'Summary: ' + (gene.summary || gene.description || 'N/A'),
        'Strategy: ' + (Array.isArray(gene.strategy) ? gene.strategy.join(' | ') : gene.strategy || 'N/A'),
        'Signals: ' + (Array.isArray(gene.signals) ? gene.signals.join(', ') : gene.signals || 'N/A'),
      ].join('\n')
    : 'No gene context';

  return [
    'You are a code safety reviewer for an AI agent evolution engine.',
    'The agent wants to apply the following Gene and has made these code changes:',
    '',
    '## Gene Context',
    geneSummary,
    '',
    '## Code Changes (git diff)',
    diff || '(no diff available — dry run or no files changed)',
    '',
    '## Your Task',
    'Answer: Is this change SAFE and REASONABLE for the stated Gene purpose?',
    '',
    'Respond with ONLY a JSON object (no markdown, no explanation):',
    '{ "safe": true|false, "reason": "<one sentence>", "concerns": ["<concern 1>", ...] }',
  ].join('\n');
}

// ---------------------------------------------------------------------------
// Call LLM (uses OpenAI-compatible API via env vars)
// ---------------------------------------------------------------------------

async function callLlm(prompt, timeoutMs = 30000) {
  const apiKey = process.env.OPENAI_API_KEY || process.env.LLM_API_KEY;
  const baseUrl = process.env.LLM_API_BASE || 'https://api.openai.com/v1';
  const model = process.env.LLM_MODEL || 'gpt-4o-mini';

  if (!apiKey) return { error: 'no_api_key' };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const resp = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.1,
        max_tokens: 400,
      }),
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (!resp.ok) return { error: 'http_' + resp.status };
    const data = await resp.json();
    const text = data.choices?.[0]?.message?.content || '';
    return parseLlmResponse(text);
  } catch (e) {
    clearTimeout(timer);
    return { error: e.name === 'AbortError' ? 'timeout' : e.message };
  }
}

function parseLlmResponse(text) {
  try {
    // Try direct JSON
    return JSON.parse(text.trim());
  } catch {
    // Try extracting from markdown fences
    const m = text.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
    if (m) {
      try { return JSON.parse(m[1].trim()); }
      catch { /* fall through */ }
    }
    return { safe: null, reason: 'parse_error', raw: text.slice(0, 100) };
  }
}

// ---------------------------------------------------------------------------
// Main review function
// ---------------------------------------------------------------------------

/**
 * @param {object} gene - Gene 对象
 * @param {object} opts
 * @param {string} opts.diff - 可选，手动传入 diff（否则自动抓取）
 * @returns {Promise<{ok: boolean, safe: boolean, reason: string, concerns: string[]}>}
 */
async function runLlmReview(gene, opts = {}) {
  if (!LLM_REVIEW_ENABLED) {
    return { ok: true, safe: true, reason: 'llm_review_disabled', concerns: [] };
  }

  let diff;
  if (opts.diff) {
    diff = opts.diff;
  } else {
    const repoRoot = getRepoRoot();
    diff = isGitRepo(repoRoot) ? captureDiffSnapshot(repoRoot) : '(not a git repo)';
  }

  const prompt = buildLlmReviewPrompt({ gene, diff, context: opts.context || '' });
  const result = await callLlm(prompt);

  if (result.error) {
    console.warn('[LlmReview] LLM call failed: ' + result.error + ' — proceeding without review');
    return { ok: false, safe: null, reason: 'llm_error: ' + result.error, concerns: [] };
  }

  const safe = result.safe !== false;
  if (!safe && Array.isArray(result.concerns) && result.concerns.length > 0) {
    console.warn('[LlmReview] ⚠️ LLM concerns: ' + result.concerns.join('; '));
  }

  return {
    ok: true,
    safe,
    reason: result.reason || 'unknown',
    concerns: Array.isArray(result.concerns) ? result.concerns : [],
  };
}

module.exports = {
  runLlmReview,
  buildLlmReviewPrompt,
  isLlmReviewEnabled: () => LLM_REVIEW_ENABLED,
};
