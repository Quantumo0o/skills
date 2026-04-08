import { describe, expect, it } from "vitest";
import { noopLogger, redactApiKey } from "../../src/logger.js";
import type { Logger } from "../../src/logger.js";

describe("noopLogger", () => {
  it("implements the Logger interface", () => {
    const logger: Logger = noopLogger;
    expect(typeof logger.debug).toBe("function");
    expect(typeof logger.info).toBe("function");
    expect(typeof logger.warn).toBe("function");
    expect(typeof logger.error).toBe("function");
  });

  it("does not throw when called", () => {
    expect(() => noopLogger.debug("test")).not.toThrow();
    expect(() => noopLogger.info("test")).not.toThrow();
    expect(() => noopLogger.warn("test")).not.toThrow();
    expect(() => noopLogger.error("test")).not.toThrow();
  });

  it("accepts optional meta parameter", () => {
    expect(() => noopLogger.debug("msg", { key: "val" })).not.toThrow();
  });
});

describe("redactApiKey", () => {
  it("replaces api key with ***", () => {
    const key = "sk-murf-secret-12345";
    const input = `url: https://api.murf.ai/v1?key=${key}`;
    const result = redactApiKey(input, key);
    expect(result).toBe("url: https://api.murf.ai/v1?key=***");
    expect(result).not.toContain(key);
  });

  it("replaces all occurrences", () => {
    const key = "abc";
    const result = redactApiKey("abc-def-abc", key);
    expect(result).toBe("***-def-***");
  });

  it("returns input unchanged when apiKey is undefined", () => {
    expect(redactApiKey("hello", undefined)).toBe("hello");
  });

  it("returns input unchanged when apiKey is empty string", () => {
    expect(redactApiKey("hello", "")).toBe("hello");
  });

  it("handles input string that does not contain the key", () => {
    expect(redactApiKey("safe message", "secret")).toBe("safe message");
  });
});
