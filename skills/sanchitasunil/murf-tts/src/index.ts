/**
 * Plugin entry point for the Murf Falcon TTS provider.
 *
 * Contains ONLY definePluginEntry -- no business logic.
 * All logic is delegated to ./synthesize, ./list-voices, ./config, ./errors.
 */

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import type { SpeechProviderPlugin } from "openclaw/plugin-sdk/speech";

import { createFalconClient, MURF_MODELS } from "./falcon-client.js";
import {
  parseMurfDirectiveToken,
  readMurfProviderConfig,
  resolveConfig,
  resolveTalkConfig,
  resolveTalkOverrides,
} from "./config.js";
import { createSynthesizeFn } from "./synthesize.js";
import { createListVoicesFn } from "./list-voices.js";

// ---------------------------------------------------------------------------
// Client factory -- creates a FalconClient per call with the resolved apiKey.
// ---------------------------------------------------------------------------

function getClient(apiKey: string, timeoutMs?: number) {
  return createFalconClient({ apiKey, timeoutMs });
}

// ---------------------------------------------------------------------------
// Provider
// ---------------------------------------------------------------------------

const synthesize = createSynthesizeFn(getClient);
const listVoices = createListVoicesFn(getClient);

const provider: SpeechProviderPlugin = {
  id: "murf",
  label: "Murf",
  autoSelectOrder: 30,
  models: MURF_MODELS,

  resolveConfig,
  parseDirectiveToken: parseMurfDirectiveToken,
  resolveTalkConfig,
  resolveTalkOverrides,

  // Rule 8: isConfigured returns false when neither config.apiKey nor
  // MURF_API_KEY env var is set. It does NOT throw.
  isConfigured: ({ providerConfig }) =>
    Boolean(
      readMurfProviderConfig(providerConfig).apiKey ||
        process.env.MURF_API_KEY,
    ),

  synthesize,
  listVoices,
};

// ---------------------------------------------------------------------------
// Entry
// ---------------------------------------------------------------------------

export default definePluginEntry({
  id: "murf-tts",
  name: "Murf Falcon TTS",
  description:
    "High-quality text-to-speech via Murf AI (FALCON and GEN2 models)",
  register(api) {
    api.registerSpeechProvider(provider);
  },
});
