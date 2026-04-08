import { afterEach, describe, expect, it, vi } from "vitest";
import {
  createFalconClient,
  MURF_API_REGIONS,
  MURF_MODELS,
  normalizeMurfRegion,
  normalizeMurfModel,
  normalizeFormat,
  formatMurfErrorPayload,
} from "../../src/falcon-client.js";
import {
  MurfAuthError,
  MurfBadRequestError,
  MurfQuotaError,
  MurfRateLimitError,
  MurfTransientError,
} from "../../src/errors.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function baseParams() {
  return {
    text: "hello",
    voiceId: "en-US-natalie",
    model: "FALCON",
    locale: "en-US",
    style: "Conversation",
    rate: 0,
    pitch: 0,
    region: "global",
    format: "MP3",
    sampleRate: 24_000,
  };
}

function okAudioResponse(bytes: number[] = [1, 2, 3]) {
  return new Response(new Uint8Array(bytes), { status: 200 });
}

function stubFetch(fn: (...args: unknown[]) => Promise<Response>) {
  vi.stubGlobal("fetch", vi.fn(fn));
}

function getLastFetchCall() {
  const mock = vi.mocked(globalThis.fetch);
  const calls = mock.mock.calls;
  return calls[calls.length - 1] as [string, RequestInit];
}

// ---------------------------------------------------------------------------
// Region normalization
// ---------------------------------------------------------------------------

describe("normalizeMurfRegion", () => {
  it("exposes all 12 documented regional host ids", () => {
    expect(MURF_API_REGIONS).toContain("eu-central");
    expect(MURF_API_REGIONS).toContain("us-west");
    expect(MURF_API_REGIONS).toHaveLength(12);
  });

  it("accepts valid region ids case-insensitively", () => {
    expect(normalizeMurfRegion("us-west")).toBe("us-west");
    expect(normalizeMurfRegion("EU-CENTRAL")).toBe("eu-central");
  });

  it("maps unknown regions to global", () => {
    expect(normalizeMurfRegion("nope")).toBe("global");
    expect(normalizeMurfRegion(undefined)).toBe("global");
    expect(normalizeMurfRegion("")).toBe("global");
    expect(normalizeMurfRegion("  ")).toBe("global");
  });
});

// ---------------------------------------------------------------------------
// Model normalization
// ---------------------------------------------------------------------------

describe("normalizeMurfModel", () => {
  it("defaults to FALCON for undefined/empty", () => {
    expect(normalizeMurfModel(undefined)).toBe("FALCON");
    expect(normalizeMurfModel("")).toBe("FALCON");
    expect(normalizeMurfModel("  ")).toBe("FALCON");
  });

  it("uppercases valid models", () => {
    expect(normalizeMurfModel("falcon")).toBe("FALCON");
    expect(normalizeMurfModel("gen2")).toBe("GEN2");
  });

  it("passes through unknown models trimmed", () => {
    expect(normalizeMurfModel("gen3")).toBe("gen3");
  });

  it("exports both FALCON and GEN2 in MURF_MODELS", () => {
    expect(MURF_MODELS).toContain("FALCON");
    expect(MURF_MODELS).toContain("GEN2");
  });
});

// ---------------------------------------------------------------------------
// Format normalization
// ---------------------------------------------------------------------------

describe("normalizeFormat", () => {
  it("normalizes valid formats to uppercase", () => {
    expect(normalizeFormat("mp3")).toBe("MP3");
    expect(normalizeFormat("wav")).toBe("WAV");
    expect(normalizeFormat("ogg")).toBe("OGG");
    expect(normalizeFormat("flac")).toBe("FLAC");
  });

  it("returns undefined for invalid formats", () => {
    expect(normalizeFormat("aac")).toBeUndefined();
    expect(normalizeFormat(undefined)).toBeUndefined();
    expect(normalizeFormat("")).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------
// formatMurfErrorPayload
// ---------------------------------------------------------------------------

describe("formatMurfErrorPayload", () => {
  it("extracts message and code from flat object", () => {
    expect(
      formatMurfErrorPayload({ message: "Bad request", code: "ERR_BAD" }),
    ).toBe("Bad request [code=ERR_BAD]");
  });

  it("extracts error_message and error_code from Murf API error shape", () => {
    expect(
      formatMurfErrorPayload({ error_message: "Internal server error", error_code: 500 }),
    ).toBe("Internal server error [code=500]");
  });

  it("prefers error_message over message", () => {
    expect(
      formatMurfErrorPayload({ error_message: "specific", message: "generic", error_code: 400 }),
    ).toBe("specific [code=400]");
  });

  it("extracts message from nested detail object", () => {
    expect(
      formatMurfErrorPayload({
        detail: { message: "Quota exceeded", status: "quota_exceeded" },
      }),
    ).toBe("Quota exceeded [code=quota_exceeded]");
  });

  it("extracts error field as fallback", () => {
    expect(
      formatMurfErrorPayload({ error: "Something went wrong" }),
    ).toBe("Something went wrong");
  });

  it("returns undefined for non-object input", () => {
    expect(formatMurfErrorPayload("string")).toBeUndefined();
    expect(formatMurfErrorPayload(null)).toBeUndefined();
    expect(formatMurfErrorPayload(undefined)).toBeUndefined();
  });

  it("returns undefined for object with no recognized fields", () => {
    expect(formatMurfErrorPayload({ foo: "bar" })).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------
// falcon-client.synthesize
// ---------------------------------------------------------------------------

describe("createFalconClient().synthesize", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  // --- Input validation (rules 6, 7) ---

  it("rejects empty text (rule 6)", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), text: "" }),
    ).rejects.toThrow(MurfBadRequestError);
    await expect(
      client.synthesize({ ...baseParams(), text: "" }),
    ).rejects.toThrow("Text cannot be empty");
  });

  it("rejects whitespace-only text (rule 6)", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), text: "   \n\t  " }),
    ).rejects.toThrow("Text cannot be empty");
  });

  it("rejects text exceeding maxTextLength (rule 7, default 4000)", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), text: "a".repeat(4001) }),
    ).rejects.toThrow("Text exceeds maximum length of 4000 characters");
  });

  it("accepts text at exactly maxTextLength", async () => {
    stubFetch(() => Promise.resolve(okAudioResponse()));
    const client = createFalconClient({ apiKey: "test-key" });
    const result = await client.synthesize({
      ...baseParams(),
      text: "a".repeat(4000),
    });
    expect(result.audioBuffer.length).toBe(3);
  });

  it("respects custom maxTextLength", async () => {
    const client = createFalconClient({
      apiKey: "test-key",
      maxTextLength: 100,
    });
    await expect(
      client.synthesize({ ...baseParams(), text: "a".repeat(101) }),
    ).rejects.toThrow("Text exceeds maximum length of 100 characters");
  });

  it("rejects unsupported models", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), model: "GEN3" }),
    ).rejects.toThrow(MurfBadRequestError);
  });

  it("rejects unsupported format", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), format: "AAC" }),
    ).rejects.toThrow(MurfBadRequestError);
  });

  it("rejects unsupported sampleRate", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), sampleRate: 22050 }),
    ).rejects.toThrow(MurfBadRequestError);
  });

  it("rejects rate out of range", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), rate: 51 }),
    ).rejects.toThrow("rate must be between -50 and 50");
    await expect(
      client.synthesize({ ...baseParams(), rate: -51 }),
    ).rejects.toThrow("rate must be between -50 and 50");
  });

  it("rejects pitch out of range", async () => {
    const client = createFalconClient({ apiKey: "test-key" });
    await expect(
      client.synthesize({ ...baseParams(), pitch: 51 }),
    ).rejects.toThrow("pitch must be between -50 and 50");
  });

  // --- Request construction ---

  it("normalizes model casing in the JSON payload", async () => {
    stubFetch(() => Promise.resolve(okAudioResponse()));
    const client = createFalconClient({ apiKey: "test-key" });

    await client.synthesize({ ...baseParams(), model: "falcon" });

    const [, init] = getLastFetchCall();
    const body = JSON.parse(String(init.body));
    expect(body.model).toBe("FALCON");
  });

  it("constructs the correct regional URL", async () => {
    stubFetch(() => Promise.resolve(okAudioResponse()));
    const client = createFalconClient({ apiKey: "test-key" });

    await client.synthesize({ ...baseParams(), region: "us-east" });

    const [url] = getLastFetchCall();
    expect(url).toBe("https://us-east.api.murf.ai/v1/speech/stream");
  });

  it("falls back to global region URL for unknown regions", async () => {
    stubFetch(() => Promise.resolve(okAudioResponse()));
    const client = createFalconClient({ apiKey: "test-key" });

    await client.synthesize({ ...baseParams(), region: "unknown-region" });

    const [url] = getLastFetchCall();
    expect(url).toBe("https://global.api.murf.ai/v1/speech/stream");
  });

  it("sends api-key header (not Authorization)", async () => {
    stubFetch(() => Promise.resolve(okAudioResponse()));
    const client = createFalconClient({ apiKey: "my-secret-key" });

    await client.synthesize(baseParams());

    const [, init] = getLastFetchCall();
    const headers = init.headers as Record<string, string>;
    expect(headers["api-key"]).toBe("my-secret-key");
    expect(headers["Authorization"]).toBeUndefined();
  });

  // --- Error handling ---

  it("throws MurfAuthError on 401 (rule 5)", async () => {
    stubFetch(() => Promise.resolve(new Response("unauthorized", { status: 401 })));
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(MurfAuthError);
    await expect(client.synthesize(baseParams())).rejects.toThrow(
      "Murf API rejected the credentials",
    );
    // Verify no retry -- only 1 call per attempt
    expect(vi.mocked(globalThis.fetch)).toHaveBeenCalledTimes(2); // 2 assertions = 2 calls
  });

  it("throws MurfAuthError on 403 (rule 5)", async () => {
    stubFetch(() => Promise.resolve(new Response("forbidden", { status: 403 })));
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(MurfAuthError);
  });

  it("does NOT include api key in MurfAuthError message (rule 5)", async () => {
    const secretKey = "sk-murf-secret-12345";
    stubFetch(() => Promise.resolve(new Response("denied", { status: 401 })));
    const client = createFalconClient({ apiKey: secretKey });

    try {
      await client.synthesize(baseParams());
    } catch (err) {
      expect((err as Error).message).not.toContain(secretKey);
    }
  });

  it("throws MurfQuotaError on 402", async () => {
    stubFetch(() =>
      Promise.resolve(new Response("payment required", { status: 402 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(MurfQuotaError);
  });

  it("throws MurfBadRequestError on 400 (rule 3, no retry)", async () => {
    stubFetch(() =>
      Promise.resolve(new Response("bad request", { status: 400 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(
      MurfBadRequestError,
    );
    expect(vi.mocked(globalThis.fetch)).toHaveBeenCalledTimes(1);
  });

  it("parses JSON error body with message and code", async () => {
    stubFetch(() =>
      Promise.resolve(
        new Response(
          JSON.stringify({
            message: "Invalid voice ID",
            code: "INVALID_VOICE",
          }),
          {
            status: 400,
            headers: { "x-request-id": "murf_req_123" },
          },
        ),
      ),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(
      /Invalid voice ID.*INVALID_VOICE.*murf_req_123/,
    );
  });

  it("falls back to raw body text when error body is non-JSON", async () => {
    stubFetch(() =>
      Promise.resolve(new Response("service unavailable", { status: 400 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(
      /service unavailable/,
    );
  });

  it("throws MurfTransientError on empty audio response", async () => {
    vi.spyOn(Math, "random").mockReturnValue(0); // zero jitter for speed
    stubFetch(() =>
      Promise.resolve(new Response(new Uint8Array([]), { status: 200 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    // Empty audio is retried (transient), so this will exhaust retries
    await expect(client.synthesize(baseParams())).rejects.toThrow(
      "received empty audio response",
    );
  }, 15_000);

  // --- Retry behavior (rule 2) ---
  // These tests mock Math.random to eliminate jitter and use real timers
  // to avoid timing issues with Response body reading + fake timers.

  it("retries on 503 then succeeds", async () => {
    vi.spyOn(Math, "random").mockReturnValue(0); // zero jitter
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(new Response(null, { status: 503 }))
      .mockResolvedValueOnce(okAudioResponse());
    vi.stubGlobal("fetch", fetchMock);

    // Use real timers but tiny timeout so backoff waits are real but short
    // We can't easily shorten the backoff constants, so instead we just let
    // the real backoff run (500ms base + 0 jitter = 500ms).
    const client = createFalconClient({ apiKey: "test-key" });
    const result = await client.synthesize(baseParams());

    expect(result.audioBuffer.length).toBe(3);
    expect(fetchMock).toHaveBeenCalledTimes(2);
  }, 10_000);

  it("retries on 429 without Retry-After using backoff (rule 4)", async () => {
    vi.spyOn(Math, "random").mockReturnValue(0);
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(new Response("rate limited", { status: 429 }))
      .mockResolvedValueOnce(okAudioResponse());
    vi.stubGlobal("fetch", fetchMock);

    const client = createFalconClient({ apiKey: "test-key" });
    const result = await client.synthesize(baseParams());

    expect(result.audioBuffer.length).toBe(3);
    expect(fetchMock).toHaveBeenCalledTimes(2);
  }, 10_000);

  it("does not retry 400 errors (rule 3)", async () => {
    stubFetch(() =>
      Promise.resolve(new Response("bad", { status: 400 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(
      MurfBadRequestError,
    );
    expect(vi.mocked(globalThis.fetch)).toHaveBeenCalledTimes(1);
  });

  it("exhausts all retries on persistent 5xx", async () => {
    vi.spyOn(Math, "random").mockReturnValue(0); // zero jitter
    const fetchMock = vi
      .fn()
      .mockResolvedValue(new Response(null, { status: 500 }));
    vi.stubGlobal("fetch", fetchMock);

    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.synthesize(baseParams())).rejects.toThrow(
      MurfTransientError,
    );
    expect(fetchMock).toHaveBeenCalledTimes(3);
  }, 15_000);

  // --- AbortController timeout (rule 1) ---

  it("passes an AbortSignal to every fetch call", async () => {
    stubFetch(() => Promise.resolve(okAudioResponse()));
    const client = createFalconClient({ apiKey: "test-key", timeoutMs: 5000 });

    await client.synthesize(baseParams());

    const [, init] = getLastFetchCall();
    expect(init.signal).toBeInstanceOf(AbortSignal);
  });
});

// ---------------------------------------------------------------------------
// falcon-client.listVoices
// ---------------------------------------------------------------------------

describe("createFalconClient().listVoices", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("calls the non-regional base URL", async () => {
    stubFetch(() =>
      Promise.resolve(new Response(JSON.stringify([]), { status: 200 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await client.listVoices();

    const [url] = getLastFetchCall();
    expect(url).toBe("https://api.murf.ai/v1/speech/voices");
  });

  it("appends model query param when provided", async () => {
    stubFetch(() =>
      Promise.resolve(new Response(JSON.stringify([]), { status: 200 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await client.listVoices("FALCON");

    const [url] = getLastFetchCall();
    expect(url).toContain("model=FALCON");
  });

  it("sends api-key header", async () => {
    stubFetch(() =>
      Promise.resolve(new Response(JSON.stringify([]), { status: 200 })),
    );
    const client = createFalconClient({ apiKey: "my-key" });

    await client.listVoices();

    const [, init] = getLastFetchCall();
    const headers = init.headers as Record<string, string>;
    expect(headers["api-key"]).toBe("my-key");
  });

  it("parses voices array response", async () => {
    stubFetch(() =>
      Promise.resolve(
        new Response(
          JSON.stringify([
            {
              voiceId: "en-US-natalie",
              name: "Natalie",
              locale: "en-US",
              gender: "Female",
            },
            {
              voiceId: "en-US-jackson",
              displayName: "Jackson",
              locale: "en-US",
              gender: "Male",
            },
          ]),
          { status: 200 },
        ),
      ),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    const voices = await client.listVoices();

    expect(voices).toHaveLength(2);
    expect(voices[0]).toMatchObject({
      id: "en-US-natalie",
      name: "Natalie",
      gender: "Female",
    });
    expect(voices[1]).toMatchObject({
      id: "en-US-jackson",
      name: "Jackson",
    });
  });

  it("parses voices wrapped in a voices field", async () => {
    stubFetch(() =>
      Promise.resolve(
        new Response(
          JSON.stringify({
            voices: [
              { voiceId: "en-US-natalie", name: "Natalie" },
              { voiceId: "", name: "Bad" },
            ],
          }),
          { status: 200 },
        ),
      ),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    const voices = await client.listVoices();

    expect(voices).toHaveLength(1);
    expect(voices[0].id).toBe("en-US-natalie");
  });

  it("throws MurfAuthError on 403", async () => {
    stubFetch(() =>
      Promise.resolve(new Response("Forbidden", { status: 403 })),
    );
    const client = createFalconClient({ apiKey: "bad-key" });

    await expect(client.listVoices()).rejects.toThrow(MurfAuthError);
  });

  it("throws MurfTransientError on 500", async () => {
    stubFetch(() =>
      Promise.resolve(new Response("error", { status: 500 })),
    );
    const client = createFalconClient({ apiKey: "test-key" });

    await expect(client.listVoices()).rejects.toThrow(MurfTransientError);
  });
});
