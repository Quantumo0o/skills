import { describe, expect, it, vi } from "vitest";

describe("plugin entry", { timeout: 30_000 }, () => {
  it("default export has correct plugin entry shape", async () => {
    const mod = await import("../../src/index.js");
    const entry = mod.default;

    expect(entry.id).toBe("murf-tts");
    expect(entry.name).toBe("Murf Falcon TTS");
    expect(typeof entry.description).toBe("string");
    expect(typeof entry.register).toBe("function");
  });

  it("register() calls registerSpeechProvider with provider id 'murf'", async () => {
    const mod = await import("../../src/index.js");
    const entry = mod.default;

    const registerSpeechProvider = vi.fn();
    const api = { registerSpeechProvider } as never;

    entry.register(api);

    expect(registerSpeechProvider).toHaveBeenCalledTimes(1);
    const provider = registerSpeechProvider.mock.calls[0]![0];
    expect(provider.id).toBe("murf");
    expect(provider.label).toBe("Murf");
    expect(provider.models).toContain("FALCON");
    expect(provider.models).toContain("GEN2");
    expect(typeof provider.isConfigured).toBe("function");
    expect(typeof provider.synthesize).toBe("function");
    expect(typeof provider.listVoices).toBe("function");
    expect(typeof provider.parseDirectiveToken).toBe("function");
    expect(typeof provider.resolveConfig).toBe("function");
    expect(typeof provider.resolveTalkConfig).toBe("function");
    expect(typeof provider.resolveTalkOverrides).toBe("function");
  });

  it("isConfigured returns false when no key is set", async () => {
    const originalKey = process.env.MURF_API_KEY;
    delete process.env.MURF_API_KEY;

    try {
      const mod = await import("../../src/index.js");
      const entry = mod.default;

      const registerSpeechProvider = vi.fn();
      entry.register({ registerSpeechProvider } as never);

      const provider = registerSpeechProvider.mock.calls[0]![0];
      const result = provider.isConfigured({
        providerConfig: {},
        timeoutMs: 10_000,
      });
      expect(result).toBe(false);
    } finally {
      if (originalKey !== undefined) {
        process.env.MURF_API_KEY = originalKey;
      }
    }
  });

  it("isConfigured returns true when apiKey is in providerConfig", async () => {
    const mod = await import("../../src/index.js");
    const entry = mod.default;

    const registerSpeechProvider = vi.fn();
    entry.register({ registerSpeechProvider } as never);

    const provider = registerSpeechProvider.mock.calls[0]![0];
    const result = provider.isConfigured({
      providerConfig: { apiKey: "some-key" },
      timeoutMs: 10_000,
    });
    expect(result).toBe(true);
  });
});
