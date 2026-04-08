/**
 * Bridge between OpenClaw's SpeechProviderPlugin.listVoices and the
 * Falcon client's voice listing endpoint.
 *
 * Ported from murf/speech-provider.ts:listVoices (lines 124-162).
 */

import type {
  SpeechListVoicesRequest,
  SpeechVoiceOption,
} from "openclaw/plugin-sdk/speech";

import type { FalconClient } from "./falcon-client.js";
import { readMurfProviderConfig } from "./config.js";
import { MurfAuthError } from "./errors.js";

/**
 * Create a listVoices function that satisfies SpeechProviderPlugin.listVoices.
 */
export function createListVoicesFn(
  getClient: (apiKey: string, timeoutMs?: number) => FalconClient,
) {
  return async function listVoices(
    req: SpeechListVoicesRequest,
  ): Promise<SpeechVoiceOption[]> {
    const config = req.providerConfig
      ? readMurfProviderConfig(req.providerConfig)
      : undefined;
    const apiKey = req.apiKey || config?.apiKey || process.env.MURF_API_KEY;

    if (!apiKey) {
      throw new MurfAuthError(
        "Murf TTS is not configured. Set MURF_API_KEY in your environment " +
          "or add apiKey under messages.tts.providers.murf in your OpenClaw " +
          "config. See openclaw.config.example.json5 for a complete example.",
      );
    }

    const client = getClient(apiKey);
    const voices = await client.listVoices(config?.model);

    return voices.map((v) => ({
      id: v.id,
      name: v.name,
      locale: v.locale,
      gender: v.gender,
      description: v.description,
    }));
  };
}
