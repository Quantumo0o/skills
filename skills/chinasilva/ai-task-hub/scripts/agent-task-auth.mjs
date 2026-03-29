#!/usr/bin/env node

import { fileURLToPath, pathToFileURL } from 'node:url';
import { getDefaultBaseUrl, normalizeBaseUrl } from './base-url.mjs';

const DEFAULT_BASE_URL = getDefaultBaseUrl();
const PUBLIC_HOST_SLUG_PATTERN = /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/;
const ENTRY_HOST_ENV_KEYS = ['PUBLIC_BRIDGE_ENTRY_HOST', 'AI_TASK_HUB_ENTRY_HOST'];
const ENTRY_HOST_PATH_MARKERS = [
  ['/.mobileclaw/', 'mobileclaw'],
  ['/.codex/', 'codex'],
  ['/.claude/', 'claude'],
  ['/.openclaw/', 'openclaw']
];

export const AGENT_TASK_DEFAULT_BASE_URL = DEFAULT_BASE_URL;

export async function resolveAgentTaskAuth(params = {}) {
  const baseUrl = normalizeBaseUrl(params.baseUrl);
  return {
    mode: 'public_bridge',
    baseUrl,
    entryHost: resolveEntryHost(params.entryHost),
    entryUserKey: readToken(params.entryUserKey),
    agentUid: readText(params.agentUid) || 'assistant',
    conversationId: readText(params.conversationId) || createConversationId(),
    source: 'params'
  };
}

function readToken(value) {
  if (typeof value !== 'string') {
    return '';
  }
  return value.trim();
}

function readText(value) {
  if (typeof value !== 'string') {
    return '';
  }
  return value.trim();
}

function resolveEntryHost(value) {
  const explicit = readText(value);
  if (explicit) {
    return assertSupportedEntryHost(explicit);
  }

  const envEntryHost = resolveEntryHostFromEnv(process.env);
  if (envEntryHost) {
    return envEntryHost;
  }

  return resolveEntryHostFromRuntime();
}

function resolveEntryHostFromEnv(env) {
  for (const key of ENTRY_HOST_ENV_KEYS) {
    const value = readText(env?.[key]);
    if (value) {
      return assertSupportedEntryHost(value);
    }
  }
  return '';
}

function resolveEntryHostFromRuntime() {
  const candidates = [fileURLToPath(import.meta.url), process.cwd()];
  for (const candidate of candidates) {
    const normalized = String(candidate).replace(/\\/g, '/').toLowerCase();
    for (const [marker, entryHost] of ENTRY_HOST_PATH_MARKERS) {
      if (normalized.includes(marker)) {
        return entryHost;
      }
    }
  }
  return 'openclaw';
}

function assertSupportedEntryHost(candidate) {
  const normalized = readText(candidate).toLowerCase();
  if (!PUBLIC_HOST_SLUG_PATTERN.test(normalized)) {
    throw createAuthError(
      400,
      'VALIDATION_BAD_REQUEST',
      'entry_host must be a lowercase host slug containing letters, digits, and internal hyphens'
    );
  }
  return normalized;
}

function createConversationId() {
  return `bridge_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
}

function parseCliArgs(args) {
  const first = typeof args[0] === 'string' ? args[0].trim() : '';
  const baseUrl = /^https?:\/\//i.test(first) ? first : DEFAULT_BASE_URL;
  return {
    baseUrl
  };
}

async function main() {
  try {
    const auth = await resolveAgentTaskAuth(parseCliArgs(process.argv.slice(2)));
    console.log(
      JSON.stringify({
        base_url: auth.baseUrl,
        mode: auth.mode,
        source: auth.source,
        agent_task_token_available: false,
        entry_host: auth.entryHost ?? null,
        entry_user_key_available: Boolean(auth.entryUserKey),
        agent_uid: auth.agentUid ?? null,
        conversation_id: auth.conversationId ?? null
      })
    );
  } catch (error) {
    const status = Number.isFinite(error?.status) ? error.status : 500;
    const code = typeof error?.code === 'string' ? error.code : 'SYSTEM_INTERNAL_ERROR';
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`${JSON.stringify({ event: 'agent_task_auth_failed', status, code, message })}\n`);
    process.exit(1);
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  await main();
}

function createAuthError(status, code, message) {
  const error = new Error(message);
  error.status = status;
  error.code = code;
  return error;
}
