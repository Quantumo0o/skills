/**
 * Pure HTTP client for the Murf Falcon / GEN2 TTS API.
 *
 * ZERO OpenClaw imports -- testable in isolation by mocking globalThis.fetch.
 *
 * PRODUCTION ERROR HANDLING RULES (non-negotiable):
 * 1. Every fetch call has an AbortController with config.timeoutMs (default 30000).
 * 2. Network errors and 5xx responses retry with exponential backoff:
 *    max 3 attempts, base delay 500ms, factor 2, jitter 0-200ms.
 * 3. 4xx (non-429) responses do NOT retry -- throw immediately.
 * 4. 429 responses respect Retry-After header if present (parse seconds OR HTTP
 *    date), otherwise use the backoff schedule.
 * 5. Auth errors (401, 403) throw MurfAuthError with message:
 *    "Murf API rejected the credentials. Check that MURF_API_KEY is set correctly."
 *    -- DO NOT include the key value, even partially.
 * 6. Empty text input throws MurfBadRequestError("Text cannot be empty").
 * 7. Text over maxTextLength (default 4000) throws
 *    MurfBadRequestError("Text exceeds maximum length of N characters").
 * 8. isConfigured() returns false when neither config.apiKey nor MURF_API_KEY env
 *    var is set. It does NOT throw.
 */

import {
  MurfAuthError,
  MurfBadRequestError,
  MurfQuotaError,
  MurfRateLimitError,
  MurfTransientError,
} from "./errors.js";
import type { Logger } from "./logger.js";
import { noopLogger, redactApiKey } from "./logger.js";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MAX_RETRIES = 3;
const BASE_DELAY_MS = 500;
const BACKOFF_FACTOR = 2;
const MAX_JITTER_MS = 200;
const DEFAULT_TIMEOUT_MS = 30_000;
const DEFAULT_MAX_TEXT_LENGTH = 4_000;

/** Subdomain for `https://<id>.api.murf.ai` (see Murf Stream Speech API regional URLs). */
export const MURF_API_REGIONS = [
  "au",
  "ca",
  "eu-central",
  "global",
  "in",
  "jp",
  "kr",
  "me",
  "sa-east",
  "uk",
  "us-east",
  "us-west",
] as const;

const MURF_REGIONS = new Set<string>(MURF_API_REGIONS);

export const MURF_MODELS = ["FALCON", "GEN2"] as const;
const MURF_MODEL_SET = new Set<string>(MURF_MODELS);

const MURF_FORMATS = new Set(["MP3", "WAV", "OGG", "FLAC"]);
const MURF_SAMPLE_RATES = new Set([8000, 16000, 24000, 44100, 48000]);

/** Base URL for non-regional Murf API endpoints (e.g. voice listing). */
const MURF_API_BASE_URL = "https://api.murf.ai";

// ---------------------------------------------------------------------------
// Local utility reimplementations (falcon-client has zero OpenClaw imports).
//
// These mirror the SDK-safe utilities from openclaw/plugin-sdk/speech
// (see audit.md section 2, "Import Classification" -- all classified as
// sdk-safe). We reimplement them here so falcon-client.ts is testable in
// complete isolation without any openclaw dependency.
// ---------------------------------------------------------------------------

/** Mirrors `trimToUndefined` from openclaw/plugin-sdk/speech (audit.md lines 44,58). */
function trimToUndefined(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

/** Mirrors `asObject` from openclaw/plugin-sdk/speech (audit.md lines 42,57). */
function asObject(value: unknown): Record<string, unknown> | undefined {
  if (value !== null && typeof value === "object" && !Array.isArray(value)) {
    return value as Record<string, unknown>;
  }
  return undefined;
}

/** Mirrors `truncateErrorDetail` from openclaw/plugin-sdk/speech (audit.md line 45). */
function truncateErrorDetail(detail: string, limit = 500): string {
  if (detail.length <= limit) return detail;
  return detail.slice(0, limit) + "...";
}

/** Mirrors `readResponseTextLimited` from openclaw/plugin-sdk/speech (audit.md line 43). */
async function readResponseTextLimited(
  response: Response,
  limitBytes = 4096,
): Promise<string> {
  try {
    const reader = response.body?.getReader();
    if (!reader) return "";
    const chunks: Uint8Array[] = [];
    let totalBytes = 0;
    while (totalBytes < limitBytes) {
      const { done, value } = await reader.read();
      if (done || !value) break;
      chunks.push(value);
      totalBytes += value.length;
    }
    reader.releaseLock();
    const merged = new Uint8Array(totalBytes);
    let offset = 0;
    for (const chunk of chunks) {
      merged.set(chunk, offset);
      offset += chunk.length;
    }
    return new TextDecoder().decode(merged.slice(0, limitBytes));
  } catch {
    return "";
  }
}

/** Strip control characters except tab (\t), newline (\n), carriage return (\r). */
function stripControlChars(input: string): string {
  let result = "";
  for (const ch of input) {
    const code = ch.codePointAt(0) ?? 0;
    if (code >= 0x20 || code === 9 || code === 10 || code === 13) {
      if (code !== 0x7f) {
        result += ch;
      }
    }
  }
  return result;
}

// ---------------------------------------------------------------------------
// Public helpers (exported for testing and config module)
// ---------------------------------------------------------------------------

export function normalizeMurfRegion(region?: string): string {
  const trimmed = region?.trim().toLowerCase();
  return trimmed && MURF_REGIONS.has(trimmed) ? trimmed : "global";
}

export function normalizeMurfModel(raw: unknown): string {
  const v = trimToUndefined(raw);
  if (v === undefined) return "FALCON";
  const upper = v.trim().toUpperCase();
  return MURF_MODEL_SET.has(upper) ? upper : v.trim();
}

export function normalizeFormat(value: unknown): string | undefined {
  const trimmed = trimToUndefined(value)?.toUpperCase();
  return trimmed && MURF_FORMATS.has(trimmed) ? trimmed : undefined;
}

export function isValidSampleRate(rate: number): boolean {
  return MURF_SAMPLE_RATES.has(rate);
}

// ---------------------------------------------------------------------------
// Error parsing (ported from murf/tts.ts)
// ---------------------------------------------------------------------------

/**
 * Parse a structured Murf API error payload, extracting the most useful
 * human-readable detail string.
 */
export function formatMurfErrorPayload(payload: unknown): string | undefined {
  const root = asObject(payload);
  if (!root) return undefined;

  const detailObject = asObject(root.detail);
  const message =
    trimToUndefined(root.error_message) ??
    trimToUndefined(root.message) ??
    trimToUndefined(detailObject?.message) ??
    trimToUndefined(detailObject?.detail) ??
    trimToUndefined(root.error);
  const rawCode = root.error_code ?? root.code ?? detailObject?.code ?? detailObject?.status;
  const code =
    typeof rawCode === "number"
      ? String(rawCode)
      : trimToUndefined(rawCode);
  if (message && code) return `${truncateErrorDetail(message)} [code=${code}]`;
  if (message) return truncateErrorDetail(message);
  if (code) return `[code=${code}]`;
  return undefined;
}

/** Extract human-readable error detail from a Murf API error response. */
async function extractMurfErrorDetail(
  response: Response,
): Promise<string | undefined> {
  const rawBody = trimToUndefined(await readResponseTextLimited(response));
  if (!rawBody) return undefined;
  try {
    return (
      formatMurfErrorPayload(JSON.parse(rawBody)) ??
      truncateErrorDetail(rawBody)
    );
  } catch {
    return truncateErrorDetail(rawBody);
  }
}

/** Extract request/trace ID from Murf API response headers. */
function extractMurfRequestId(response: Response): string | undefined {
  return (
    trimToUndefined(response.headers.get("x-request-id")) ??
    trimToUndefined(response.headers.get("request-id"))
  );
}

// ---------------------------------------------------------------------------
// Retry-After parsing
// ---------------------------------------------------------------------------

/**
 * Parse a Retry-After header value. Supports both delta-seconds and HTTP-date.
 * Returns milliseconds to wait, or undefined if unparseable.
 */
function parseRetryAfter(header: string | null): number | undefined {
  if (!header) return undefined;
  const trimmed = header.trim();
  const asSeconds = Number(trimmed);
  if (Number.isFinite(asSeconds) && asSeconds >= 0) {
    return asSeconds * 1000;
  }
  const date = Date.parse(trimmed);
  if (Number.isFinite(date)) {
    const delta = date - Date.now();
    return delta > 0 ? delta : 0;
  }
  return undefined;
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type FalconSynthesizeRequest = {
  text: string;
  voiceId: string;
  model: string;
  locale: string;
  style: string;
  rate: number;
  pitch: number;
  region: string;
  format: string;
  sampleRate: number;
  channelType?: string;
};

export type FalconSynthesizeResult = {
  audioBuffer: Buffer;
};

export type FalconVoice = {
  id: string;
  name?: string;
  locale?: string;
  gender?: string;
  description?: string;
};

export type FalconClientOptions = {
  apiKey: string;
  timeoutMs?: number;
  maxTextLength?: number;
  logger?: Logger;
};

export type FalconClient = {
  synthesize(req: FalconSynthesizeRequest): Promise<FalconSynthesizeResult>;
  listVoices(model?: string): Promise<FalconVoice[]>;
};

// ---------------------------------------------------------------------------
// Backoff helper
// ---------------------------------------------------------------------------

function backoffDelay(attempt: number): number {
  const base = BASE_DELAY_MS * BACKOFF_FACTOR ** attempt;
  const jitter = Math.random() * MAX_JITTER_MS;
  return base + jitter;
}

// ---------------------------------------------------------------------------
// Classify HTTP status into typed errors
// ---------------------------------------------------------------------------

async function throwForStatus(
  response: Response,
  logger: Logger,
  apiKey: string,
): Promise<never> {
  const detail = await extractMurfErrorDetail(response);
  const requestId = extractMurfRequestId(response);
  const suffix =
    (detail ? `: ${detail}` : "") +
    (requestId ? ` [request_id=${requestId}]` : "");

  const safeMsg = redactApiKey(
    `Murf TTS API error (${response.status})${suffix}`,
    apiKey,
  );

  logger.warn(safeMsg);

  switch (response.status) {
    case 401:
    case 403:
      // Rule 5: DO NOT include the key value, even partially.
      throw new MurfAuthError(
        "Murf API rejected the credentials. Check that MURF_API_KEY is set correctly.",
        { code: String(response.status) },
      );
    case 402:
      throw new MurfQuotaError(safeMsg, { code: String(response.status) });
    case 429: {
      const retryAfterMs = parseRetryAfter(
        response.headers.get("retry-after"),
      );
      throw new MurfRateLimitError(safeMsg, {
        code: "429",
        retryAfterMs,
      });
    }
    default:
      if (response.status >= 400 && response.status < 500) {
        throw new MurfBadRequestError(safeMsg, {
          code: String(response.status),
        });
      }
      throw new MurfTransientError(safeMsg, {
        code: String(response.status),
      });
  }
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

export function createFalconClient(opts: FalconClientOptions): FalconClient {
  const {
    apiKey,
    timeoutMs = DEFAULT_TIMEOUT_MS,
    maxTextLength = DEFAULT_MAX_TEXT_LENGTH,
    logger = noopLogger,
  } = opts;

  // -- synthesize -----------------------------------------------------------

  async function synthesize(
    req: FalconSynthesizeRequest,
  ): Promise<FalconSynthesizeResult> {
    // Rule 6: Empty text input throws MurfBadRequestError.
    const text = stripControlChars(req.text).trim();
    if (!text) {
      throw new MurfBadRequestError("Text cannot be empty");
    }

    // Rule 7: Text over maxTextLength throws MurfBadRequestError.
    if (text.length > maxTextLength) {
      throw new MurfBadRequestError(
        `Text exceeds maximum length of ${maxTextLength} characters`,
      );
    }

    const modelNorm = req.model.trim().toUpperCase();
    if (!MURF_MODEL_SET.has(modelNorm)) {
      throw new MurfBadRequestError(
        `Unsupported model "${req.model}" (expected FALCON or GEN2)`,
      );
    }

    if (!MURF_FORMATS.has(req.format)) {
      throw new MurfBadRequestError(
        `Unsupported format "${req.format}" (expected MP3, WAV, OGG, or FLAC)`,
      );
    }
    if (!MURF_SAMPLE_RATES.has(req.sampleRate)) {
      throw new MurfBadRequestError(
        `Unsupported sampleRate ${req.sampleRate} (expected 8000, 16000, 24000, 44100, or 48000)`,
      );
    }
    if (req.rate < -50 || req.rate > 50) {
      throw new MurfBadRequestError("rate must be between -50 and 50");
    }
    if (req.pitch < -50 || req.pitch > 50) {
      throw new MurfBadRequestError("pitch must be between -50 and 50");
    }

    const region = normalizeMurfRegion(req.region);
    const url = `https://${region}.api.murf.ai/v1/speech/stream`;
    const body = JSON.stringify({
      text,
      voiceId: req.voiceId,
      model: modelNorm,
      format: req.format,
      locale: req.locale,
      style: req.style,
      rate: req.rate,
      pitch: req.pitch,
      sampleRate: req.sampleRate,
      channelType: req.channelType ?? "MONO",
    });

    logger.debug(
      `Murf synthesize: ${redactApiKey(url, apiKey)} model=${modelNorm} voice=${req.voiceId}`,
    );

    let lastError: Error | undefined;

    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      // Rule 1: Every fetch call has an AbortController with timeoutMs.
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), timeoutMs);

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "api-key": apiKey,
            "Content-Type": "application/json",
          },
          body,
          signal: controller.signal,
        });

        if (response.ok) {
          const buffer = Buffer.from(await response.arrayBuffer());
          if (buffer.length === 0) {
            throw new MurfTransientError(
              "Murf TTS: received empty audio response",
            );
          }
          return { audioBuffer: buffer };
        }

        // Rule 3 & 5: 4xx (non-429) responses do NOT retry -- throw immediately.
        if (
          response.status >= 400 &&
          response.status < 500 &&
          response.status !== 429
        ) {
          await throwForStatus(response, logger, apiKey);
        }

        // Rule 4: 429 responses respect Retry-After header.
        if (response.status === 429) {
          const retryAfterMs = parseRetryAfter(
            response.headers.get("retry-after"),
          );
          if (retryAfterMs !== undefined && attempt < MAX_RETRIES - 1) {
            logger.info(
              `Murf rate limited (429), retrying after ${retryAfterMs}ms (attempt ${attempt + 1}/${MAX_RETRIES})`,
            );
            await new Promise((resolve) => setTimeout(resolve, retryAfterMs));
            continue;
          }
          // No Retry-After or last attempt -- fall through to backoff/throw
        }

        // Rule 2: 5xx and 429 without Retry-After retry with backoff.
        const detail = await extractMurfErrorDetail(response);
        const requestId = extractMurfRequestId(response);
        const suffix =
          (detail ? `: ${detail}` : "") +
          (requestId ? ` [request_id=${requestId}]` : "");
        lastError = new MurfTransientError(
          redactApiKey(
            `Murf TTS API error (${response.status})${suffix}`,
            apiKey,
          ),
          { code: String(response.status) },
        );

        logger.warn(
          `Murf transient error (${response.status}), attempt ${attempt + 1}/${MAX_RETRIES}`,
        );
      } catch (err) {
        if (
          err instanceof MurfAuthError ||
          err instanceof MurfBadRequestError ||
          err instanceof MurfQuotaError
        ) {
          throw err;
        }

        if (err instanceof MurfRateLimitError) {
          // On last attempt, throw; otherwise continue to backoff.
          if (attempt === MAX_RETRIES - 1) throw err;
          const delay = err.retryAfterMs ?? backoffDelay(attempt);
          logger.info(
            `Murf rate limited (429), retrying after ${delay}ms (attempt ${attempt + 1}/${MAX_RETRIES})`,
          );
          await new Promise((resolve) => setTimeout(resolve, delay));
          continue;
        }

        // Abort or network error -- retryable (rule 2).
        const isAbort =
          err instanceof DOMException && err.name === "AbortError";
        lastError = new MurfTransientError(
          isAbort
            ? `Murf TTS: request timed out after ${timeoutMs}ms`
            : `Murf TTS: network error: ${err instanceof Error ? err.message : String(err)}`,
          { cause: err },
        );
        logger.warn(
          `Murf network/timeout error, attempt ${attempt + 1}/${MAX_RETRIES}: ${lastError.message}`,
        );
      } finally {
        clearTimeout(timeout);
      }

      // Exponential backoff before next attempt (rule 2).
      if (attempt < MAX_RETRIES - 1) {
        const delay = backoffDelay(attempt);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }

    throw lastError ?? new MurfTransientError("Murf TTS: all retries exhausted");
  }

  // -- listVoices -----------------------------------------------------------

  async function listVoices(model?: string): Promise<FalconVoice[]> {
    // The voices endpoint uses the non-regional base URL because the
    // voice catalog is not region-scoped (see audit.md section on
    // speech-provider.ts, line 115-116: MURF_API_BASE_URL = "https://api.murf.ai").
    const url = new URL(`${MURF_API_BASE_URL}/v1/speech/voices`);
    if (model) {
      url.searchParams.set("model", model);
    }

    logger.debug(
      `Murf listVoices: ${redactApiKey(url.toString(), apiKey)}`,
    );

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const res = await fetch(url.toString(), {
        headers: { "api-key": apiKey },
        signal: controller.signal,
      });

      if (!res.ok) {
        await throwForStatus(res, logger, apiKey);
      }

      // The Murf API returns an array of voice objects directly (or wrapped
      // in a `voices` field depending on version). Handle both defensively.
      const json: unknown = await res.json();
      const voiceArray: Array<Record<string, unknown>> = Array.isArray(json)
        ? json
        : Array.isArray(
              (json as Record<string, unknown>).voices,
            )
          ? ((json as Record<string, unknown>).voices as Array<
              Record<string, unknown>
            >)
          : [];

      return voiceArray
        .map((v) => ({
          id: (
            typeof v.voiceId === "string" ? v.voiceId.trim() : ""
          ) as string,
          name:
            (typeof v.displayName === "string"
              ? v.displayName.trim()
              : undefined) ||
            (typeof v.name === "string" ? v.name.trim() : undefined) ||
            undefined,
          locale:
            (typeof v.locale === "string" ? v.locale.trim() : undefined) ||
            undefined,
          gender:
            (typeof v.gender === "string" ? v.gender.trim() : undefined) ||
            undefined,
          description:
            (typeof v.description === "string"
              ? v.description.trim()
              : undefined) || undefined,
        }))
        .filter((v) => v.id.length > 0);
    } catch (err) {
      if (
        err instanceof MurfAuthError ||
        err instanceof MurfBadRequestError ||
        err instanceof MurfQuotaError ||
        err instanceof MurfRateLimitError ||
        err instanceof MurfTransientError
      ) {
        throw err;
      }
      const isAbort =
        err instanceof DOMException && err.name === "AbortError";
      throw new MurfTransientError(
        isAbort
          ? `Murf voices: request timed out after ${timeoutMs}ms`
          : `Murf voices: network error: ${err instanceof Error ? err.message : String(err)}`,
        { cause: err },
      );
    } finally {
      clearTimeout(timeout);
    }
  }

  return { synthesize, listVoices };
}
