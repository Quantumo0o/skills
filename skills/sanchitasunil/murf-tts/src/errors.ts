/**
 * Typed error classes for the Murf TTS plugin.
 *
 * Retry logic uses `instanceof` checks to distinguish error categories.
 * Each class sets `name` in the constructor so it survives bundle boundaries
 * and appears correctly in stack traces.
 */

export type MurfErrorOptions = {
  cause?: unknown;
  code?: string;
};

/** Base error for all Murf plugin errors. */
export class MurfError extends Error {
  readonly code: string | undefined;

  constructor(message: string, opts?: MurfErrorOptions) {
    super(message, opts?.cause !== undefined ? { cause: opts.cause } : undefined);
    this.name = "MurfError";
    this.code = opts?.code;
  }
}

/** 401 / 403 -- credentials rejected. */
export class MurfAuthError extends MurfError {
  constructor(message: string, opts?: MurfErrorOptions) {
    super(message, opts);
    this.name = "MurfAuthError";
  }
}

/** 429 -- rate limited. */
export class MurfRateLimitError extends MurfError {
  readonly retryAfterMs: number | undefined;

  constructor(
    message: string,
    opts?: MurfErrorOptions & { retryAfterMs?: number },
  ) {
    super(message, opts);
    this.name = "MurfRateLimitError";
    this.retryAfterMs = opts?.retryAfterMs;
  }
}

/** 402 or quota-specific 4xx. */
export class MurfQuotaError extends MurfError {
  constructor(message: string, opts?: MurfErrorOptions) {
    super(message, opts);
    this.name = "MurfQuotaError";
  }
}

/** 400 and other non-auth, non-quota 4xx errors. */
export class MurfBadRequestError extends MurfError {
  constructor(message: string, opts?: MurfErrorOptions) {
    super(message, opts);
    this.name = "MurfBadRequestError";
  }
}

/** 5xx, network, timeout -- retryable transient failures. */
export class MurfTransientError extends MurfError {
  constructor(message: string, opts?: MurfErrorOptions) {
    super(message, opts);
    this.name = "MurfTransientError";
  }
}
