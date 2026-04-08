/**
 * Barrel re-export for external test consumers.
 * Mirrors the ElevenLabs pattern from murf/test-api.ts.
 */

export {
  createFalconClient,
  MURF_API_REGIONS,
  MURF_MODELS,
  normalizeMurfRegion,
  normalizeMurfModel,
  normalizeFormat,
  formatMurfErrorPayload,
} from "./falcon-client.js";

export type {
  FalconClient,
  FalconClientOptions,
  FalconSynthesizeRequest,
  FalconSynthesizeResult,
  FalconVoice,
} from "./falcon-client.js";

export {
  normalizeMurfProviderConfig,
  readMurfProviderConfig,
  resolveConfig,
  resolveTalkConfig,
  resolveTalkOverrides,
  parseMurfDirectiveToken,
  DEFAULT_VOICE_ID,
  DEFAULT_MODEL,
  DEFAULT_LOCALE,
  DEFAULT_STYLE,
  DEFAULT_REGION,
  DEFAULT_FORMAT,
  DEFAULT_RATE,
  DEFAULT_PITCH,
} from "./config.js";

export type { MurfConfig } from "./config.js";

export { createSynthesizeFn } from "./synthesize.js";
export { createListVoicesFn } from "./list-voices.js";

export {
  MurfError,
  MurfAuthError,
  MurfBadRequestError,
  MurfQuotaError,
  MurfRateLimitError,
  MurfTransientError,
} from "./errors.js";

export { noopLogger, redactApiKey } from "./logger.js";
export type { Logger, LogMeta } from "./logger.js";
