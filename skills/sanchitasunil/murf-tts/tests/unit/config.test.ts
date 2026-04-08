import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { SpeechModelOverridePolicy } from "openclaw/plugin-sdk/speech";
import {
  normalizeMurfProviderConfig,
  readMurfProviderConfig,
  resolveConfig,
  resolveTalkConfig,
  resolveTalkOverrides,
  parseMurfDirectiveToken,
  isConfigured,
  DEFAULT_VOICE_ID,
  DEFAULT_MODEL,
  DEFAULT_LOCALE,
  DEFAULT_STYLE,
  DEFAULT_REGION,
  DEFAULT_FORMAT,
  DEFAULT_RATE,
  DEFAULT_PITCH,
} from "../../src/config.js";
import type { MurfConfig } from "../../src/config.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const ALLOW_ALL_POLICY: SpeechModelOverridePolicy = {
  enabled: true,
  allowText: true,
  allowProvider: true,
  allowVoice: true,
  allowModelId: true,
  allowVoiceSettings: true,
  allowNormalization: true,
  allowSeed: true,
};

// ---------------------------------------------------------------------------
// Default values
// ---------------------------------------------------------------------------

describe("config defaults", () => {
  it("exports correct defaults from source reference", () => {
    expect(DEFAULT_VOICE_ID).toBe("en-US-natalie");
    expect(DEFAULT_MODEL).toBe("FALCON");
    expect(DEFAULT_LOCALE).toBe("en-US");
    expect(DEFAULT_STYLE).toBe("Conversation");
    expect(DEFAULT_REGION).toBe("global");
    expect(DEFAULT_FORMAT).toBe("MP3");
    expect(DEFAULT_RATE).toBe(0);
    expect(DEFAULT_PITCH).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// normalizeMurfProviderConfig
// ---------------------------------------------------------------------------

describe("normalizeMurfProviderConfig", () => {
  it("returns all defaults for empty rawConfig", () => {
    const config = normalizeMurfProviderConfig({});
    expect(config).toMatchObject({
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
  });

  it("reads from rawConfig.murf (flat shorthand)", () => {
    const config = normalizeMurfProviderConfig({
      murf: { voiceId: "en-US-jackson", model: "gen2" },
    });
    expect(config.voiceId).toBe("en-US-jackson");
    expect(config.model).toBe("GEN2");
    expect(config.sampleRate).toBe(44_100);
  });

  it("reads from rawConfig.providers.murf (nested)", () => {
    const config = normalizeMurfProviderConfig({
      providers: { murf: { voiceId: "Matthew", model: "gen2" } },
    });
    expect(config.voiceId).toBe("Matthew");
    expect(config.model).toBe("GEN2");
    expect(config.sampleRate).toBe(44_100);
  });

  it("coerces numeric strings for sampleRate", () => {
    const config = normalizeMurfProviderConfig({
      murf: { sampleRate: "48000" },
    });
    expect(config.sampleRate).toBe(48_000);
  });

  it("uses FALCON default sample rate (24000)", () => {
    const config = normalizeMurfProviderConfig({ murf: { model: "FALCON" } });
    expect(config.sampleRate).toBe(24_000);
  });

  it("uses GEN2 default sample rate (44100)", () => {
    const config = normalizeMurfProviderConfig({ murf: { model: "GEN2" } });
    expect(config.sampleRate).toBe(44_100);
  });
});

// ---------------------------------------------------------------------------
// readMurfProviderConfig
// ---------------------------------------------------------------------------

describe("readMurfProviderConfig", () => {
  it("reads apiKey from providerConfig", () => {
    const config = readMurfProviderConfig({ apiKey: "config-key" });
    expect(config.apiKey).toBe("config-key");
  });

  it("applies defaults for missing fields", () => {
    const config = readMurfProviderConfig({});
    expect(config.voiceId).toBe("en-US-natalie");
    expect(config.model).toBe("FALCON");
  });

  it("normalizes model casing", () => {
    const config = readMurfProviderConfig({ model: "gen2" });
    expect(config.model).toBe("GEN2");
  });
});

// ---------------------------------------------------------------------------
// resolveConfig (SpeechProviderPlugin hook)
// ---------------------------------------------------------------------------

describe("resolveConfig", () => {
  it("normalizes raw config with defaults", () => {
    const resolved = resolveConfig({
      cfg: {} as never,
      rawConfig: { murf: { voiceId: "Matthew" } },
      timeoutMs: 10_000,
    });
    expect(resolved).toMatchObject({
      voiceId: "Matthew",
      model: "FALCON",
      locale: "en-US",
      format: "MP3",
      sampleRate: 24_000,
    });
  });
});

// ---------------------------------------------------------------------------
// isConfigured
// ---------------------------------------------------------------------------

describe("isConfigured", () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    delete process.env.MURF_API_KEY;
  });

  afterEach(() => {
    process.env = { ...originalEnv };
  });

  it("returns true when apiKey is in config", () => {
    expect(isConfigured({ apiKey: "my-key" })).toBe(true);
  });

  it("returns true when MURF_API_KEY env var is set", () => {
    expect(
      isConfigured(undefined, { MURF_API_KEY: "env-key" }),
    ).toBe(true);
  });

  it("returns false when neither is set", () => {
    expect(isConfigured(undefined, {})).toBe(false);
    expect(isConfigured({}, {})).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// parseMurfDirectiveToken
// ---------------------------------------------------------------------------

describe("parseMurfDirectiveToken", () => {
  it("handles voiceid key", () => {
    const result = parseMurfDirectiveToken({
      key: "voiceid",
      value: "en-US-jackson",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(true);
    expect(result.overrides).toMatchObject({ voiceId: "en-US-jackson" });
  });

  it("handles murf_voice alias", () => {
    const result = parseMurfDirectiveToken({
      key: "murf_voice",
      value: "en-UK-harry",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(true);
    expect(result.overrides).toMatchObject({ voiceId: "en-UK-harry" });
  });

  it("handles model key", () => {
    const result = parseMurfDirectiveToken({
      key: "model",
      value: "GEN2",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(true);
    expect(result.overrides).toMatchObject({ model: "GEN2" });
  });

  it("handles rate with validation", () => {
    const ok = parseMurfDirectiveToken({
      key: "rate",
      value: "25",
      policy: ALLOW_ALL_POLICY,
    });
    expect(ok.handled).toBe(true);
    expect(ok.overrides).toMatchObject({ rate: 25 });

    const bad = parseMurfDirectiveToken({
      key: "rate",
      value: "999",
      policy: ALLOW_ALL_POLICY,
    });
    expect(bad.handled).toBe(true);
    expect(bad.warnings).toBeDefined();
    expect(bad.overrides).toBeUndefined();
  });

  it("handles pitch with validation", () => {
    const ok = parseMurfDirectiveToken({
      key: "pitch",
      value: "-10",
      policy: ALLOW_ALL_POLICY,
    });
    expect(ok.handled).toBe(true);
    expect(ok.overrides).toMatchObject({ pitch: -10 });
  });

  it("handles style", () => {
    const result = parseMurfDirectiveToken({
      key: "style",
      value: "Newscast",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(true);
    expect(result.overrides).toMatchObject({ style: "Newscast" });
  });

  it("handles format with validation", () => {
    const ok = parseMurfDirectiveToken({
      key: "format",
      value: "wav",
      policy: ALLOW_ALL_POLICY,
    });
    expect(ok.handled).toBe(true);
    expect(ok.overrides).toMatchObject({ format: "WAV" });

    const bad = parseMurfDirectiveToken({
      key: "format",
      value: "aac",
      policy: ALLOW_ALL_POLICY,
    });
    expect(bad.handled).toBe(true);
    expect(bad.warnings).toBeDefined();
  });

  it("handles locale", () => {
    const result = parseMurfDirectiveToken({
      key: "locale",
      value: "es-ES",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(true);
    expect(result.overrides).toMatchObject({ locale: "es-ES" });
  });

  it("respects policy restrictions", () => {
    const deniedPolicy: SpeechModelOverridePolicy = {
      ...ALLOW_ALL_POLICY,
      allowVoice: false,
    };
    const result = parseMurfDirectiveToken({
      key: "voiceid",
      value: "en-US-jackson",
      policy: deniedPolicy,
    });
    expect(result.handled).toBe(true);
    expect(result.overrides).toBeUndefined();
  });

  it("returns unhandled for unknown keys", () => {
    const result = parseMurfDirectiveToken({
      key: "unknown_key",
      value: "anything",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(false);
  });

  it("returns invalid rate value warning for non-numeric rate", () => {
    const result = parseMurfDirectiveToken({
      key: "rate",
      value: "abc",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(true);
    expect(result.warnings).toContain("invalid rate value");
  });

  it("returns invalid pitch value warning for non-numeric pitch", () => {
    const result = parseMurfDirectiveToken({
      key: "pitch",
      value: "abc",
      policy: ALLOW_ALL_POLICY,
    });
    expect(result.handled).toBe(true);
    expect(result.warnings).toContain("invalid pitch value");
  });
});

// ---------------------------------------------------------------------------
// resolveTalkConfig
// ---------------------------------------------------------------------------

describe("resolveTalkConfig", () => {
  it("merges talk provider config over base", () => {
    const result = resolveTalkConfig({
      cfg: {} as never,
      baseTtsConfig: { murf: { voiceId: "en-US-natalie", model: "FALCON" } },
      talkProviderConfig: { voiceId: "en-US-jackson", style: "Newscast" },
      timeoutMs: 10_000,
    });
    expect(result).toMatchObject({
      voiceId: "en-US-jackson",
      style: "Newscast",
      model: "FALCON",
    });
  });

  it("preserves base when talk config has no overrides", () => {
    const result = resolveTalkConfig({
      cfg: {} as never,
      baseTtsConfig: { murf: { voiceId: "en-US-natalie", model: "GEN2" } },
      talkProviderConfig: {},
      timeoutMs: 10_000,
    });
    expect(result).toMatchObject({
      voiceId: "en-US-natalie",
      model: "GEN2",
    });
  });
});

// ---------------------------------------------------------------------------
// resolveTalkOverrides
// ---------------------------------------------------------------------------

describe("resolveTalkOverrides", () => {
  it("extracts supported params", () => {
    const result = resolveTalkOverrides({
      talkProviderConfig: {},
      params: {
        voiceId: "en-US-jackson",
        model: "gen2",
        style: "Newscast",
        rate: 10,
        pitch: -5,
        format: "wav",
      },
    });
    expect(result).toMatchObject({
      voiceId: "en-US-jackson",
      model: "GEN2",
      style: "Newscast",
      rate: 10,
      pitch: -5,
      format: "WAV",
    });
  });

  it("returns empty object for no matching params", () => {
    const result = resolveTalkOverrides({
      talkProviderConfig: {},
      params: { unknownParam: "value" },
    });
    expect(result).toEqual({});
  });
});
