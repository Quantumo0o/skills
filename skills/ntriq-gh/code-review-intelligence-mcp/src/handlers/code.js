/**
 * Code analysis handlers
 * Calls ntriq AI server for code review and analysis
 * Model: Qwen2.5-Coder (Apache 2.0 License)
 */

const SERVER = process.env.NTRIQ_AI_URL || "https://ai.ntriq.co.kr";

async function callCodeServer(endpoint, body, timeout = 120) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), (timeout + 15) * 1000);

  try {
    const resp = await fetch(`${SERVER}/code/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timer);

    if (!resp.ok) {
      const error = await resp.text();
      throw new Error(`Code server error: ${resp.status} ${error}`);
    }

    return await resp.json();
  } catch (e) {
    clearTimeout(timer);
    throw e;
  }
}

export async function reviewCode(code, language = "auto", focus = "general") {
  const result = await callCodeServer("review", {
    code: code,
    language: language,
    focus: focus,
    max_tokens: 2048,
  });

  return {
    status: "success",
    review: result.review || result,
    focus: focus,
    model: result.model || "qwen2.5-coder",
  };
}

export async function explainCode(code, detailLevel = "medium") {
  const result = await callCodeServer("explain", {
    code: code,
    detail_level: detailLevel,
    max_tokens: 1024,
  });

  return {
    status: "success",
    explanation: result.explanation || result,
    detail_level: detailLevel,
    model: result.model || "qwen2.5-coder",
  };
}

export async function generateCode(
  instruction,
  existingCode = null,
  language = "python",
) {
  const result = await callCodeServer("generate", {
    instruction: instruction,
    code: existingCode,
    language: language,
    max_tokens: 2048,
  });

  return {
    status: "success",
    code: result.code || result,
    language: language,
    model: result.model || "qwen2.5-coder",
  };
}
