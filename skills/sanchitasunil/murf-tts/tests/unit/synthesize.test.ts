import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createSynthesizeFn } from "../../src/synthesize.js";
import { MurfAuthError } from "../../src/errors.js";
import type { FalconClient, FalconSynthesizeRequest } from "../../src/falcon-client.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function mockClient(overrides?: Partial<FalconClient>): FalconClient {
  return {
    synthesize: vi.fn(async () => ({
      audioBuffer: Buffer.from([1, 2, 3]),
    })),
    listVoices: vi.fn(async () => []),
    ...overrides,
  };
}

function makeGetClient(client: FalconClient) {
  return vi.fn((_apiKey: string, _timeoutMs?: number) => client);
}

function baseSynthReq(overrides?: Record<string, unknown>) {
  return {
    text: "Hello world",
    cfg: {} as never,
    providerConfig: {},
    target: "audio-file" as const,
    timeoutMs: 10_000,
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("createSynthesizeFn", () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    delete process.env.MURF_API_KEY;
  });

  afterEach(() => {
    process.env = { ...originalEnv };
  });

  it("throws MurfAuthError when no API key is available", async () => {
    const client = mockClient();
    const synthesize = createSynthesizeFn(makeGetClient(client));

    await expect(synthesize(baseSynthReq())).rejects.toThrow(MurfAuthError);
  });

  it("uses apiKey from providerConfig", async () => {
    const client = mockClient();
    const getClient = makeGetClient(client);
    const synthesize = createSynthesizeFn(getClient);

    await synthesize(
      baseSynthReq({ providerConfig: { apiKey: "config-key" } }),
    );

    expect(getClient).toHaveBeenCalledWith("config-key", 10_000);
  });

  it("falls back to MURF_API_KEY env var", async () => {
    process.env.MURF_API_KEY = "env-key";
    const client = mockClient();
    const getClient = makeGetClient(client);
    const synthesize = createSynthesizeFn(getClient);

    await synthesize(baseSynthReq());

    expect(getClient).toHaveBeenCalledWith("env-key", 10_000);
  });

  it("returns correct format metadata for audio-file target", async () => {
    process.env.MURF_API_KEY = "test-key";
    const client = mockClient();
    const synthesize = createSynthesizeFn(makeGetClient(client));

    const result = await synthesize(
      baseSynthReq({ providerConfig: { format: "WAV" } }),
    );

    expect(result.outputFormat).toBe("wav");
    expect(result.fileExtension).toBe(".wav");
    expect(result.voiceCompatible).toBe(false);
  });

  // Voice-note format: FALCON->MP3, GEN2->OGG

  it("requests MP3 for FALCON voice-note target", async () => {
    process.env.MURF_API_KEY = "test-key";
    const synthesizeMock = vi.fn(async () => ({
      audioBuffer: Buffer.from([1]),
    }));
    const client = mockClient({ synthesize: synthesizeMock });
    const synthesize = createSynthesizeFn(makeGetClient(client));

    const result = await synthesize(
      baseSynthReq({
        providerConfig: { format: "WAV", model: "FALCON" },
        target: "voice-note",
      }),
    );

    const req = synthesizeMock.mock.calls[0]![0] as FalconSynthesizeRequest;
    expect(req.format).toBe("MP3");
    expect(result.outputFormat).toBe("mp3");
    expect(result.fileExtension).toBe(".mp3");
    expect(result.voiceCompatible).toBe(true);
  });

  it("requests OGG for GEN2 voice-note target", async () => {
    process.env.MURF_API_KEY = "test-key";
    const synthesizeMock = vi.fn(async () => ({
      audioBuffer: Buffer.from([1]),
    }));
    const client = mockClient({ synthesize: synthesizeMock });
    const synthesize = createSynthesizeFn(makeGetClient(client));

    const result = await synthesize(
      baseSynthReq({
        providerConfig: { model: "GEN2" },
        target: "voice-note",
      }),
    );

    const req = synthesizeMock.mock.calls[0]![0] as FalconSynthesizeRequest;
    expect(req.format).toBe("OGG");
    expect(result.outputFormat).toBe("ogg");
    expect(result.fileExtension).toBe(".ogg");
    expect(result.voiceCompatible).toBe(true);
  });

  it("applies providerOverrides over providerConfig", async () => {
    process.env.MURF_API_KEY = "test-key";
    const synthesizeMock = vi.fn(async () => ({
      audioBuffer: Buffer.from([1]),
    }));
    const client = mockClient({ synthesize: synthesizeMock });
    const synthesize = createSynthesizeFn(makeGetClient(client));

    await synthesize(
      baseSynthReq({
        providerConfig: { voiceId: "en-US-natalie", model: "FALCON" },
        providerOverrides: { voiceId: "en-US-jackson", model: "GEN2" },
      }),
    );

    const req = synthesizeMock.mock.calls[0]![0] as FalconSynthesizeRequest;
    expect(req.voiceId).toBe("en-US-jackson");
    expect(req.model).toBe("GEN2");
  });

  it("returns audioBuffer from the falcon client", async () => {
    process.env.MURF_API_KEY = "test-key";
    const audio = Buffer.from([10, 20, 30, 40]);
    const client = mockClient({
      synthesize: vi.fn(async () => ({ audioBuffer: audio })),
    });
    const synthesize = createSynthesizeFn(makeGetClient(client));

    const result = await synthesize(baseSynthReq());
    expect(result.audioBuffer).toBe(audio);
  });
});
