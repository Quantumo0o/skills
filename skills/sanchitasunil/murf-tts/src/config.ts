/**
 * Configuration types and resolution for the Murf TTS plugin.
 *
 * Uses the field list from audit.md section 6 as the source of truth.
 * SDK utility imports are from openclaw/plugin-sdk/speech and
 * openclaw/plugin-sdk/secret-input (all classified sdk-safe in audit.md
 * section 2).
 */

import { normalizeResolvedSecretInputString } from "openclaw/plugin-sdk/secret-input";
import type {
  SpeechDirectiveTokenParseContext,
  SpeechDirectiveTokenParseResult,
  SpeechProviderConfig,
  SpeechProviderResolveConfigContext,
  SpeechProviderResolveTalkConfigContext,
  SpeechProviderResolveTalkOverridesContext,
} from "openclaw/plugin-sdk/speech";
import {
  asObject,
  requireInRange,
  trimToUndefined,
} from "openclaw/plugin-sdk/speech";

import {
  normalizeFormat,
  normalizeMurfModel,
  normalizeMurfRegion,
} from "./falcon-client.js";

// ---------------------------------------------------------------------------
// Defaults (preserved from murf/speech-provider.ts, murf/tts.ts)
// ---------------------------------------------------------------------------

export const DEFAULT_VOICE_ID = "en-US-natalie";
export const DEFAULT_MODEL = "FALCON";
export const DEFAULT_LOCALE = "en-US";
export const DEFAULT_STYLE = "Conversation";
export const DEFAULT_REGION = "global";
export const DEFAULT_FORMAT = "MP3";
export const DEFAULT_RATE = 0;
export const DEFAULT_PITCH = 0;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Resolved configuration for the Murf provider.
 * Matches audit.md section 6 field list.
 */
export type MurfConfig = {
  apiKey?: string;
  voiceId: string;
  model: string;
  locale: string;
  style: string;
  rate: number;
  pitch: number;
  region: string;
  format: string;
  sampleRate: number;
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function asNumber(value: unknown): number | undefined {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string") {
    const t = value.trim();
    if (!t) return undefined;
    const n = Number(t);
    return Number.isFinite(n) ? n : undefined;
  }
  return undefined;
}

/** Murf defaults: 24 kHz (Falcon) vs 44.1 kHz (Gen2) per API schema notes. */
function defaultSampleRateForModel(model: string): number {
  return model === "GEN2" ? 44_100 : 24_000;
}

// ---------------------------------------------------------------------------
// Config normalization (from rawConfig)
// ---------------------------------------------------------------------------

/**
 * Normalize a raw config object into a resolved MurfConfig.
 * Supports both `rawConfig.providers.murf` (nested) and `rawConfig.murf` (flat).
 */
export function normalizeMurfProviderConfig(
  rawConfig: Record<string, unknown>,
): MurfConfig {
  const providers = asObject(rawConfig.providers);
  const raw = asObject(providers?.murf) ?? asObject(rawConfig.murf) ?? {};
  const model = normalizeMurfModel(raw.model);
  return {
    apiKey: normalizeResolvedSecretInputString({
      value: raw.apiKey,
      path: "messages.tts.providers.murf.apiKey",
    }),
    voiceId: trimToUndefined(raw.voiceId) ?? DEFAULT_VOICE_ID,
    model,
    locale: trimToUndefined(raw.locale) ?? DEFAULT_LOCALE,
    style: trimToUndefined(raw.style) ?? DEFAULT_STYLE,
    rate: asNumber(raw.rate) ?? DEFAULT_RATE,
    pitch: asNumber(raw.pitch) ?? DEFAULT_PITCH,
    region: normalizeMurfRegion(
      trimToUndefined(raw.region) ?? DEFAULT_REGION,
    ),
    format: normalizeFormat(raw.format) ?? DEFAULT_FORMAT,
    sampleRate: asNumber(raw.sampleRate) ?? defaultSampleRateForModel(model),
  };
}

// ---------------------------------------------------------------------------
// Config resolution (from providerConfig)
// ---------------------------------------------------------------------------

/**
 * Read a MurfConfig from the resolved providerConfig passed to synthesize/isConfigured.
 */
export function readMurfProviderConfig(
  config: SpeechProviderConfig,
): MurfConfig {
  const defaults = normalizeMurfProviderConfig({});
  const model = normalizeMurfModel(config.model ?? defaults.model);
  return {
    apiKey: trimToUndefined(config.apiKey) ?? defaults.apiKey,
    voiceId: trimToUndefined(config.voiceId) ?? defaults.voiceId,
    model,
    locale: trimToUndefined(config.locale) ?? defaults.locale,
    style: trimToUndefined(config.style) ?? defaults.style,
    rate: asNumber(config.rate) ?? defaults.rate,
    pitch: asNumber(config.pitch) ?? defaults.pitch,
    region: normalizeMurfRegion(
      trimToUndefined(config.region) ?? defaults.region,
    ),
    format: normalizeFormat(config.format) ?? defaults.format,
    sampleRate:
      asNumber(config.sampleRate) ?? defaultSampleRateForModel(model),
  };
}

// ---------------------------------------------------------------------------
// resolveConfig hook (used by SpeechProviderPlugin.resolveConfig)
// ---------------------------------------------------------------------------

export function resolveConfig(
  ctx: SpeechProviderResolveConfigContext,
): SpeechProviderConfig {
  return normalizeMurfProviderConfig(ctx.rawConfig);
}

// ---------------------------------------------------------------------------
// Talk mode config resolution (ported from murf/speech-provider.ts)
// ---------------------------------------------------------------------------

export function resolveTalkConfig(
  ctx: SpeechProviderResolveTalkConfigContext,
): SpeechProviderConfig {
  const base = normalizeMurfProviderConfig(ctx.baseTtsConfig);
  const tp = ctx.talkProviderConfig;

  const resolvedTalkApiKey =
    tp.apiKey === undefined
      ? undefined
      : normalizeResolvedSecretInputString({
          value: tp.apiKey,
          path: "talk.providers.murf.apiKey",
        });

  return {
    ...base,
    ...(resolvedTalkApiKey === undefined ? {} : { apiKey: resolvedTalkApiKey }),
    ...(trimToUndefined(tp.voiceId) == null
      ? {}
      : { voiceId: trimToUndefined(tp.voiceId) }),
    ...(trimToUndefined(tp.model) == null
      ? {}
      : { model: normalizeMurfModel(trimToUndefined(tp.model)) }),
    ...(trimToUndefined(tp.locale) == null
      ? {}
      : { locale: trimToUndefined(tp.locale) }),
    ...(trimToUndefined(tp.style) == null
      ? {}
      : { style: trimToUndefined(tp.style) }),
    ...(asNumber(tp.rate) == null ? {} : { rate: asNumber(tp.rate) }),
    ...(asNumber(tp.pitch) == null ? {} : { pitch: asNumber(tp.pitch) }),
    ...(trimToUndefined(tp.region) == null
      ? {}
      : { region: normalizeMurfRegion(trimToUndefined(tp.region)) }),
    ...(normalizeFormat(tp.format) == null
      ? {}
      : { format: normalizeFormat(tp.format) }),
    ...(asNumber(tp.sampleRate) == null
      ? {}
      : { sampleRate: asNumber(tp.sampleRate) }),
  };
}

export function resolveTalkOverrides(
  ctx: SpeechProviderResolveTalkOverridesContext,
): SpeechProviderConfig | undefined {
  const p = ctx.params;
  return {
    ...(trimToUndefined(p.voiceId) == null
      ? {}
      : { voiceId: trimToUndefined(p.voiceId) }),
    ...(trimToUndefined(p.model) == null
      ? {}
      : { model: normalizeMurfModel(trimToUndefined(p.model)) }),
    ...(trimToUndefined(p.style) == null
      ? {}
      : { style: trimToUndefined(p.style) }),
    ...(asNumber(p.rate) == null ? {} : { rate: asNumber(p.rate) }),
    ...(asNumber(p.pitch) == null ? {} : { pitch: asNumber(p.pitch) }),
    ...(trimToUndefined(p.locale) == null
      ? {}
      : { locale: trimToUndefined(p.locale) }),
    ...(normalizeFormat(p.format) == null
      ? {}
      : { format: normalizeFormat(p.format) }),
  };
}

// ---------------------------------------------------------------------------
// Directive token parsing (ported from murf/speech-provider.ts)
// ---------------------------------------------------------------------------

function parseNumberValue(value: string): number | undefined {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : undefined;
}

export function parseMurfDirectiveToken(
  ctx: SpeechDirectiveTokenParseContext,
): SpeechDirectiveTokenParseResult {
  try {
    switch (ctx.key) {
      case "voiceid":
      case "voice_id":
      case "murf_voice":
      case "murfvoice":
        if (!ctx.policy.allowVoice) return { handled: true };
        return {
          handled: true,
          overrides: { ...(ctx.currentOverrides ?? {}), voiceId: ctx.value },
        };
      case "model":
      case "modelid":
      case "model_id":
      case "murf_model":
      case "murfmodel":
        if (!ctx.policy.allowModelId) return { handled: true };
        return {
          handled: true,
          overrides: { ...(ctx.currentOverrides ?? {}), model: ctx.value },
        };
      case "style":
      case "murf_style":
      case "murfstyle":
        if (!ctx.policy.allowVoiceSettings) return { handled: true };
        return {
          handled: true,
          overrides: { ...(ctx.currentOverrides ?? {}), style: ctx.value },
        };
      case "rate":
      case "murf_rate":
      case "murfrate": {
        if (!ctx.policy.allowVoiceSettings) return { handled: true };
        const value = parseNumberValue(ctx.value);
        if (value == null)
          return { handled: true, warnings: ["invalid rate value"] };
        requireInRange(value, -50, 50, "rate");
        return {
          handled: true,
          overrides: { ...(ctx.currentOverrides ?? {}), rate: value },
        };
      }
      case "pitch":
      case "murf_pitch":
      case "murfpitch": {
        if (!ctx.policy.allowVoiceSettings) return { handled: true };
        const value = parseNumberValue(ctx.value);
        if (value == null)
          return { handled: true, warnings: ["invalid pitch value"] };
        requireInRange(value, -50, 50, "pitch");
        return {
          handled: true,
          overrides: { ...(ctx.currentOverrides ?? {}), pitch: value },
        };
      }
      case "locale":
      case "murf_locale":
      case "murflocale":
        if (!ctx.policy.allowNormalization) return { handled: true };
        return {
          handled: true,
          overrides: { ...(ctx.currentOverrides ?? {}), locale: ctx.value },
        };
      case "format":
      case "murf_format":
      case "murfformat": {
        if (!ctx.policy.allowVoiceSettings) return { handled: true };
        const normalized = normalizeFormat(ctx.value);
        if (!normalized)
          return {
            handled: true,
            warnings: [`invalid format "${ctx.value}"`],
          };
        return {
          handled: true,
          overrides: { ...(ctx.currentOverrides ?? {}), format: normalized },
        };
      }
      default:
        return { handled: false };
    }
  } catch (error) {
    return {
      handled: true,
      warnings: [error instanceof Error ? error.message : String(error)],
    };
  }
}

export function isConfigured(config: Partial<MurfConfig> | undefined, env = process.env): boolean {
  return Boolean(config?.apiKey || env.MURF_API_KEY);
}
