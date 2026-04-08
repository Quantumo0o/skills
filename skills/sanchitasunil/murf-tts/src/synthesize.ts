/**
 * Bridge between OpenClaw's SpeechProvider.synthesize contract and the
 * Falcon client.
 *
 * Translates OpenClaw's SpeechSynthesisRequest into FalconSynthesizeRequest,
 * and Falcon's response into OpenClaw's SpeechSynthesisResult.
 *
 * Voice-note format logic (non-negotiable):
 *   FALCON uses MP3 (FALCON returns HTTP 500 for OGG).
 *   GEN2 uses OGG.
 *   const voiceNoteFormat = effectiveModel === "FALCON" ? "MP3" : "OGG";
 *   const format = isVoiceNote ? voiceNoteFormat : requestedFormat;
 */

import type { SpeechSynthesisRequest } from "openclaw/plugin-sdk/speech";
import { asObject, trimToUndefined } from "openclaw/plugin-sdk/speech";

import type { FalconClient } from "./falcon-client.js";
import { normalizeFormat, normalizeMurfModel, normalizeMurfRegion } from "./falcon-client.js";
import { readMurfProviderConfig } from "./config.js";
import { MurfAuthError } from "./errors.js";

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

function formatToExtension(format: string): string {
  return `.${format.toLowerCase()}`;
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type SpeechSynthesisResult = {
  audioBuffer: Buffer;
  outputFormat: string;
  fileExtension: string;
  voiceCompatible: boolean;
};

// ---------------------------------------------------------------------------
// Synthesize bridge
// ---------------------------------------------------------------------------

/**
 * Create a synthesize function that satisfies SpeechProviderPlugin.synthesize.
 *
 * @param getClient - factory that returns a FalconClient for the given apiKey.
 *   The client is created per-call so the apiKey from config/env can be resolved
 *   at synthesis time.
 */
export function createSynthesizeFn(
  getClient: (apiKey: string, timeoutMs: number) => FalconClient,
) {
  return async function synthesize(
    req: SpeechSynthesisRequest,
  ): Promise<SpeechSynthesisResult> {
    const config = readMurfProviderConfig(req.providerConfig);
    const overrides = (req.providerOverrides ?? {}) as Record<string, unknown>;

    const apiKey = config.apiKey || process.env.MURF_API_KEY;
    if (!apiKey) {
      throw new MurfAuthError(
        "Murf TTS is not configured. Set MURF_API_KEY in your environment " +
          "or add apiKey under messages.tts.providers.murf in your OpenClaw " +
          "config. See openclaw.config.example.json5 for a complete example.",
      );
    }

    const modelOverride = trimToUndefined(overrides.model);
    const effectiveModel = normalizeMurfModel(modelOverride ?? config.model);

    // Voice-note format logic: FALCON->MP3 (FALCON returns HTTP 500 for OGG), GEN2->OGG.
    const isVoiceNote = req.target === "voice-note";
    const requestedFormat =
      normalizeFormat(overrides.format) ?? config.format;
    const voiceNoteFormat = effectiveModel === "FALCON" ? "MP3" : "OGG";
    const format = isVoiceNote ? voiceNoteFormat : requestedFormat;

    const client = getClient(apiKey, req.timeoutMs);
    const result = await client.synthesize({
      text: req.text,
      voiceId: trimToUndefined(overrides.voiceId) ?? config.voiceId,
      model: effectiveModel,
      locale: trimToUndefined(overrides.locale) ?? config.locale,
      style: trimToUndefined(overrides.style) ?? config.style,
      rate: asNumber(overrides.rate) ?? config.rate,
      pitch: asNumber(overrides.pitch) ?? config.pitch,
      region: normalizeMurfRegion(
        trimToUndefined(overrides.region) ?? config.region,
      ),
      format,
      sampleRate: asNumber(overrides.sampleRate) ?? config.sampleRate,
    });

    return {
      audioBuffer: result.audioBuffer,
      outputFormat: format.toLowerCase(),
      fileExtension: formatToExtension(format),
      voiceCompatible: isVoiceNote,
    };
  };
}
