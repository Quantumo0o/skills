/**
 * Logger interface and utilities for the Murf TTS plugin.
 *
 * Constraint: never use console.log directly -- use the injected logger.
 * Constraint: never log the API key value, even in error messages or debug output.
 */

export type LogMeta = Record<string, unknown>;

export interface Logger {
  debug(msg: string, meta?: LogMeta): void;
  info(msg: string, meta?: LogMeta): void;
  warn(msg: string, meta?: LogMeta): void;
  error(msg: string, meta?: LogMeta): void;
}

const noop = (): void => {};

/** Logger that silently drops all messages. */
export const noopLogger: Logger = {
  debug: noop,
  info: noop,
  warn: noop,
  error: noop,
};

/**
 * Replace any occurrence of `apiKey` in the given string with "***".
 * Use this before logging any URL, header, or error message that might
 * contain the key value.
 */
export function redactApiKey(s: string, apiKey: string | undefined): string {
  if (!apiKey || apiKey.length === 0) return s;
  return s.replaceAll(apiKey, "***");
}
