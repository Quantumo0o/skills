/**
 * Live integration tests for the Murf TTS provider.
 *
 * Skipped unless both MURF_LIVE_TEST=1 and a non-empty MURF_API_KEY are set.
 * Example:
 *
 *   MURF_LIVE_TEST=1 MURF_API_KEY=your_key pnpm exec vitest run tests/live/murf.live.test.ts
 */
import { describe, expect, it } from "vitest";
import { createFalconClient } from "../../src/falcon-client.js";

const MURF_API_KEY = process.env.MURF_API_KEY ?? "";
const liveEnabled =
  process.env.MURF_LIVE_TEST === "1" && MURF_API_KEY.trim().length > 0;
const describeLive = liveEnabled ? describe : describe.skip;

describeLive("murf live integration", () => {
  it("synthesizes audio via the real Murf API", async () => {
    const client = createFalconClient({
      apiKey: MURF_API_KEY,
      timeoutMs: 30_000,
    });

    const result = await client.synthesize({
      text: "Hello from OpenClaw integration test.",
      voiceId: "en-US-natalie",
      model: "FALCON",
      locale: "en-US",
      style: "Conversation",
      rate: 0,
      pitch: 0,
      region: "global",
      format: "MP3",
      sampleRate: 24_000,
    });

    expect(result.audioBuffer).toBeInstanceOf(Buffer);
    expect(result.audioBuffer.length).toBeGreaterThan(100);
  });

  it("lists voices via the real Murf API", async () => {
    const client = createFalconClient({
      apiKey: MURF_API_KEY,
      timeoutMs: 30_000,
    });

    const voices = await client.listVoices();

    expect(Array.isArray(voices)).toBe(true);
    expect(voices.length).toBeGreaterThan(0);
    for (const voice of voices) {
      expect(voice.id.length).toBeGreaterThan(0);
    }
  });

  it("returns a clear error for invalid API key", async () => {
    const client = createFalconClient({
      apiKey: "invalid-key-12345",
      timeoutMs: 15_000,
    });

    await expect(
      client.synthesize({
        text: "This should fail.",
        voiceId: "en-US-natalie",
        model: "FALCON",
        locale: "en-US",
        style: "Conversation",
        rate: 0,
        pitch: 0,
        region: "global",
        format: "MP3",
        sampleRate: 24_000,
      }),
    ).rejects.toThrow("Murf");
  });
}, 60_000);
