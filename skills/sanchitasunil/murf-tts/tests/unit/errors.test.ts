import { describe, expect, it } from "vitest";
import {
  MurfError,
  MurfAuthError,
  MurfBadRequestError,
  MurfQuotaError,
  MurfRateLimitError,
  MurfTransientError,
} from "../../src/errors.js";

describe("MurfError base class", () => {
  it("sets message and name", () => {
    const err = new MurfError("test");
    expect(err.message).toBe("test");
    expect(err.name).toBe("MurfError");
    expect(err).toBeInstanceOf(Error);
    expect(err).toBeInstanceOf(MurfError);
  });

  it("stores code", () => {
    const err = new MurfError("test", { code: "500" });
    expect(err.code).toBe("500");
  });

  it("stores cause", () => {
    const cause = new Error("underlying");
    const err = new MurfError("test", { cause });
    expect(err.cause).toBe(cause);
  });

  it("defaults code to undefined", () => {
    const err = new MurfError("test");
    expect(err.code).toBeUndefined();
  });
});

describe("MurfAuthError", () => {
  it("is instanceof MurfError and MurfAuthError", () => {
    const err = new MurfAuthError("auth failed");
    expect(err).toBeInstanceOf(MurfError);
    expect(err).toBeInstanceOf(MurfAuthError);
    expect(err).toBeInstanceOf(Error);
    expect(err.name).toBe("MurfAuthError");
  });
});

describe("MurfRateLimitError", () => {
  it("is instanceof MurfError and stores retryAfterMs", () => {
    const err = new MurfRateLimitError("rate limited", {
      retryAfterMs: 5000,
    });
    expect(err).toBeInstanceOf(MurfError);
    expect(err).toBeInstanceOf(MurfRateLimitError);
    expect(err.name).toBe("MurfRateLimitError");
    expect(err.retryAfterMs).toBe(5000);
  });

  it("defaults retryAfterMs to undefined", () => {
    const err = new MurfRateLimitError("rate limited");
    expect(err.retryAfterMs).toBeUndefined();
  });
});

describe("MurfQuotaError", () => {
  it("is instanceof MurfError", () => {
    const err = new MurfQuotaError("quota exceeded");
    expect(err).toBeInstanceOf(MurfError);
    expect(err).toBeInstanceOf(MurfQuotaError);
    expect(err.name).toBe("MurfQuotaError");
  });
});

describe("MurfBadRequestError", () => {
  it("is instanceof MurfError", () => {
    const err = new MurfBadRequestError("bad input");
    expect(err).toBeInstanceOf(MurfError);
    expect(err).toBeInstanceOf(MurfBadRequestError);
    expect(err.name).toBe("MurfBadRequestError");
  });
});

describe("MurfTransientError", () => {
  it("is instanceof MurfError", () => {
    const err = new MurfTransientError("server down");
    expect(err).toBeInstanceOf(MurfError);
    expect(err).toBeInstanceOf(MurfTransientError);
    expect(err.name).toBe("MurfTransientError");
  });
});

describe("error class hierarchy", () => {
  it("all subclasses are instanceof MurfError", () => {
    const errors = [
      new MurfAuthError("a"),
      new MurfRateLimitError("b"),
      new MurfQuotaError("c"),
      new MurfBadRequestError("d"),
      new MurfTransientError("e"),
    ];
    for (const err of errors) {
      expect(err).toBeInstanceOf(MurfError);
      expect(err).toBeInstanceOf(Error);
    }
  });

  it("instanceof correctly distinguishes subclasses", () => {
    const auth = new MurfAuthError("a");
    expect(auth).toBeInstanceOf(MurfAuthError);
    expect(auth).not.toBeInstanceOf(MurfBadRequestError);
    expect(auth).not.toBeInstanceOf(MurfRateLimitError);
  });
});
