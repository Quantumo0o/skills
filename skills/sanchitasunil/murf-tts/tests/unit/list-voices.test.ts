import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createListVoicesFn } from "../../src/list-voices.js";
import { MurfAuthError } from "../../src/errors.js";
import type { FalconClient } from "../../src/falcon-client.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function mockClient(overrides?: Partial<FalconClient>): FalconClient {
  return {
    synthesize: vi.fn(async () => ({
      audioBuffer: Buffer.from([1]),
    })),
    listVoices: vi.fn(async () => [
      { id: "en-US-natalie", name: "Natalie", locale: "en-US", gender: "Female" },
      { id: "en-US-jackson", name: "Jackson", locale: "en-US", gender: "Male" },
    ]),
    ...overrides,
  };
}

function makeGetClient(client: FalconClient) {
  return vi.fn((_apiKey: string, _timeoutMs?: number) => client);
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("createListVoicesFn", () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    delete process.env.MURF_API_KEY;
  });

  afterEach(() => {
    process.env = { ...originalEnv };
  });

  it("throws MurfAuthError when no API key is available", async () => {
    const client = mockClient();
    const listVoices = createListVoicesFn(makeGetClient(client));

    await expect(listVoices({ providerConfig: {} })).rejects.toThrow(
      MurfAuthError,
    );
  });

  it("uses apiKey from request", async () => {
    const client = mockClient();
    const getClient = makeGetClient(client);
    const listVoices = createListVoicesFn(getClient);

    await listVoices({ apiKey: "req-key" });

    expect(getClient).toHaveBeenCalledWith("req-key");
  });

  it("uses apiKey from providerConfig", async () => {
    const client = mockClient();
    const getClient = makeGetClient(client);
    const listVoices = createListVoicesFn(getClient);

    await listVoices({ providerConfig: { apiKey: "config-key" } });

    expect(getClient).toHaveBeenCalledWith("config-key");
  });

  it("falls back to MURF_API_KEY env var", async () => {
    process.env.MURF_API_KEY = "env-key";
    const client = mockClient();
    const getClient = makeGetClient(client);
    const listVoices = createListVoicesFn(getClient);

    await listVoices({});

    expect(getClient).toHaveBeenCalledWith("env-key");
  });

  it("returns SpeechVoiceOption[] from falcon client", async () => {
    process.env.MURF_API_KEY = "test-key";
    const client = mockClient();
    const listVoices = createListVoicesFn(makeGetClient(client));

    const voices = await listVoices({});

    expect(voices).toHaveLength(2);
    expect(voices[0]).toMatchObject({
      id: "en-US-natalie",
      name: "Natalie",
      locale: "en-US",
      gender: "Female",
    });
  });

  it("prefers request apiKey over config apiKey over env", async () => {
    process.env.MURF_API_KEY = "env-key";
    const client = mockClient();
    const getClient = makeGetClient(client);
    const listVoices = createListVoicesFn(getClient);

    await listVoices({
      apiKey: "req-key",
      providerConfig: { apiKey: "config-key" },
    });

    expect(getClient).toHaveBeenCalledWith("req-key");
  });
});
