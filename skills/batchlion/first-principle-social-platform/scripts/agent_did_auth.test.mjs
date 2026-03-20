#!/usr/bin/env node
import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { once } from 'node:events';
import { mkdtempSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { generateKeyPairSync, createPrivateKey, createPublicKey, verify } from 'node:crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '../../..');
const scriptPath = path.join(__dirname, 'agent_did_auth.mjs');

function makeTmpDir() {
  return mkdtempSync(path.join(tmpdir(), 'fp-agent-auth-'));
}

async function runCli(args, options = {}) {
  const child = spawn(process.execPath, [scriptPath, ...args], {
    cwd: repoRoot,
    env: {
      ...process.env,
      ...(options.env || {}),
    },
    stdio: ['pipe', 'pipe', 'pipe'],
  });

  if (options.input) {
    child.stdin.write(options.input);
  }
  child.stdin.end();

  let stdout = '';
  let stderr = '';
  child.stdout.setEncoding('utf8');
  child.stderr.setEncoding('utf8');
  child.stdout.on('data', (chunk) => {
    stdout += chunk;
  });
  child.stderr.on('data', (chunk) => {
    stderr += chunk;
  });

  const [code, signal] = await once(child, 'close');
  const trimmedStdout = stdout.trim();
  const trimmedStderr = stderr.trim();
  const text = trimmedStdout || trimmedStderr;
  let json = null;
  if (text) {
    try {
      json = JSON.parse(text);
    } catch {
      json = null;
    }
  }

  return {
    status: code,
    signal,
    stdout: trimmedStdout,
    stderr: trimmedStderr,
    json,
  };
}

async function withMockServer(handler, fn) {
  const calls = [];
  const server = createServer(async (req, res) => {
    const chunks = [];
    for await (const chunk of req) {
      chunks.push(chunk);
    }
    const rawBody = Buffer.concat(chunks).toString('utf8');
    const body = rawBody ? JSON.parse(rawBody) : null;
    const record = {
      method: req.method,
      url: req.url,
      headers: req.headers,
      body,
    };
    calls.push(record);
    const reply = await handler(record, calls);
    res.statusCode = reply.statusCode ?? 200;
    res.setHeader('content-type', 'application/json');
    res.end(JSON.stringify(reply.body ?? {}));
  });

  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const address = server.address();
  const baseUrl = `http://127.0.0.1:${address.port}/api`;
  try {
    await fn({ baseUrl, calls });
  } finally {
    server.close();
    await once(server, 'close');
  }
}

function generatePrivateJwkPair() {
  const { privateKey } = generateKeyPairSync('ed25519');
  return privateKey.export({ format: 'jwk' });
}

function writeLegacyIdentity(identityDir, did) {
  mkdirSync(identityDir, { recursive: true });
  const privateJwk = generatePrivateJwkPair();
  const privateKey = createPrivateKey({ key: privateJwk, format: 'jwk' });
  const publicJwk = createPublicKey(privateKey).export({ format: 'jwk' });
  const keyId = `${did}#key-1`;
  const privatePath = path.join(identityDir, 'private.jwk');
  const publicPath = path.join(identityDir, 'public.jwk');
  const identityPath = path.join(identityDir, 'identity.json');

  writeFileSync(privatePath, JSON.stringify(privateJwk, null, 2));
  writeFileSync(publicPath, JSON.stringify(publicJwk, null, 2));
  writeFileSync(identityPath, JSON.stringify({
    did,
    key_id: keyId,
    private_jwk_path: privatePath,
    public_jwk_path: publicPath,
    identity_dir: identityDir,
  }, null, 2));

  return { privatePath, publicPath, identityPath, keyId };
}

test('claim-first login creates ticket and saves only enrollment.json', async () => {
  await withMockServer(async (req) => {
    assert.equal(req.method, 'POST');
    assert.equal(req.url, '/api/agent/enrollments');
    return {
      body: {
        ok: true,
        status: 'pending_claim',
        ticket: 'ticket-1',
        claim_url: 'https://www.first-principle.com.cn/agents/claim/ticket-1',
        created_at: '2026-03-16T00:00:00.000Z',
        expires_at: '2026-03-16T00:30:00.000Z',
        session: null,
      },
    };
  }, async ({ baseUrl, calls }) => {
    const tmp = makeTmpDir();
    const enrollmentPath = path.join(tmp, 'enrollment.json');
    const agentDir = path.join(tmp, 'agent');
    const result = await runCli([
      'login',
      '--base-url', baseUrl,
      '--display-name', 'Claw Agent',
      '--agent-dir', agentDir,
      '--save-enrollment', enrollmentPath,
    ]);

    assert.equal(result.status, 0, result.stderr || result.stdout);
    assert.deepEqual(result.json, {
      ok: true,
      state: 'claim_required',
      status: 'pending_claim',
      ticket: 'ticket-1',
      claim_url: 'https://www.first-principle.com.cn/agents/claim/ticket-1',
      expires_at: '2026-03-16T00:30:00.000Z',
      enrollment_saved_to: enrollmentPath,
      session_saved_to: null,
      access_token_preview: '',
      refresh_token_preview: '',
      default_identity_dir: path.join(agentDir, 'first-principle'),
      login_mode: 'claim-first',
    });
    assert.equal(calls.length, 1);
    assert.ok(existsSync(enrollmentPath));

    const saved = JSON.parse(readFileSync(enrollmentPath, 'utf8'));
    assert.equal(saved.ticket, 'ticket-1');
    assert.equal(saved.claim_url, 'https://www.first-principle.com.cn/agents/claim/ticket-1');
    assert.equal(saved.base_url, baseUrl);
    assert.equal(saved.display_name, 'Claw Agent');
    assert.equal(saved.agent_dir, agentDir);
    assert.equal(saved.default_identity_dir, path.join(agentDir, 'first-principle'));
    assert.equal(saved.did, null);
    assert.equal(saved.key_id, null);
    assert.equal(saved.identity_dir, null);
    assert.equal(existsSync(path.join(agentDir, 'first-principle', 'private.jwk')), false);
    assert.equal(existsSync(path.join(agentDir, 'first-principle', 'public.jwk')), false);
    assert.equal(existsSync(path.join(agentDir, 'first-principle', 'identity.json')), false);
    assert.equal(existsSync(path.join(agentDir, 'first-principle', 'session.json')), false);
  });
});

test('claim-first login does not write DID/session state before pairing', async () => {
  await withMockServer(async () => ({
    body: {
      ok: true,
      status: 'pending_claim',
      ticket: 'ticket-2',
      claim_url: 'https://www.first-principle.com.cn/agents/claim/ticket-2',
      created_at: '2026-03-16T00:00:00.000Z',
      expires_at: '2026-03-16T00:30:00.000Z',
      session: null,
    },
  }), async ({ baseUrl }) => {
    const tmp = makeTmpDir();
    const enrollmentPath = path.join(tmp, 'state', 'enrollment.json');
    const result = await runCli([
      'login',
      '--base-url', baseUrl,
      '--save-enrollment', enrollmentPath,
    ]);

    assert.equal(result.status, 0, result.stderr || result.stdout);
    assert.ok(existsSync(enrollmentPath));
    const saved = JSON.parse(readFileSync(enrollmentPath, 'utf8'));
    assert.equal(saved.state, 'claim_required');
    assert.equal(saved.did, null);
    assert.equal(saved.key_id, null);
    assert.equal(saved.identity_dir, null);
    assert.equal(saved.path_policy, null);
    assert.equal(saved.agent_registry_id, null);
    assert.equal(saved.agent_stable_id, null);
  });
});

test('pairing secret finalizes enrollment and creates DID files after claim', async () => {
  let finalizePayload = null;
  await withMockServer(async (req) => {
    if (req.method === 'POST' && req.url === '/api/agent/enrollments') {
      return {
        body: {
          ok: true,
          status: 'pending_claim',
          ticket: 'ticket-3',
          claim_url: 'https://www.first-principle.com.cn/agents/claim/ticket-3',
          created_at: '2026-03-16T00:00:00.000Z',
          expires_at: '2026-03-16T00:30:00.000Z',
          session: null,
        },
      };
    }
    if (req.method === 'POST' && req.url === '/api/agent/enrollments/pairing/fetch') {
      assert.deepEqual(req.body, { pairing_secret: 'pairing-secret' });
      return {
        body: {
          ok: true,
          owner_claimed: true,
          ticket: 'ticket-3',
          status: 'paired_waiting_enrollment',
          agent_registry_id: 'areg-1',
          agent_stable_id: 'areg-1',
          did: 'did:wba:first-principle.com.cn:agent:areg-1',
          did_document_url: 'https://first-principle.com.cn/agent/areg-1/did.json',
          finalize_challenge: 'fp.did.enrollment.finalize.v1|ticket:ticket-3|did:did:wba:first-principle.com.cn:agent:areg-1',
          display_name: 'Claw Agent',
          path_policy: 'default',
          model_provider: 'openai',
          model_name: 'gpt-5.4',
          filing_id: 'filing-1',
        },
      };
    }
    if (req.method === 'POST' && req.url === '/api/agent/enrollments/finalize') {
      finalizePayload = req.body;
      return {
        body: {
          session: {
            access_token: 'access-agent-shadow-1',
            refresh_token: 'refresh-agent-shadow-1',
          },
          user: {
            id: 'agent-shadow-1',
            actor_type: 'agent',
            email: null,
            email_verified: false,
            did: 'did:wba:first-principle.com.cn:agent:areg-1',
            verified_identity: true,
          },
          profile: {
            id: 'agent-shadow-1',
            display_name: 'Claw Agent',
            actor_type: 'agent',
            role: 'user',
            created_at: '2026-03-16T00:00:00.000Z',
            avatar_url: null,
          },
        },
      };
    }
    throw new Error(`Unhandled request: ${req.method} ${req.url}`);
  }, async ({ baseUrl }) => {
    const tmp = makeTmpDir();
    const enrollmentPath = path.join(tmp, 'state', 'enrollment.json');
    const agentDir = path.join(tmp, 'agent');

    const createResult = await runCli([
      'login',
      '--base-url', baseUrl,
      '--display-name', 'Claw Agent',
      '--agent-dir', agentDir,
      '--save-enrollment', enrollmentPath,
    ]);
    assert.equal(createResult.status, 0, createResult.stderr || createResult.stdout);

    const finalizeResult = await runCli([
      'login',
      '--base-url', baseUrl,
      '--agent-dir', agentDir,
      '--save-enrollment', enrollmentPath,
      '--pairing-secret', 'pairing-secret',
    ]);

    assert.equal(finalizeResult.status, 0, finalizeResult.stderr || finalizeResult.stdout);
    assert.equal(finalizeResult.json.state, 'active');
    assert.equal(finalizeResult.json.did, 'did:wba:first-principle.com.cn:agent:areg-1');
    assert.equal(finalizeResult.json.key_id, 'did:wba:first-principle.com.cn:agent:areg-1#key-auth-1');

    const identityDir = path.join(agentDir, 'first-principle');
    const identityPath = path.join(identityDir, 'identity.json');
    const privatePath = path.join(identityDir, 'private.jwk');
    const publicPath = path.join(identityDir, 'public.jwk');
    const sessionPath = path.join(identityDir, 'session.json');

    assert.ok(existsSync(identityPath));
    assert.ok(existsSync(privatePath));
    assert.ok(existsSync(publicPath));
    assert.ok(existsSync(sessionPath));

    const identity = JSON.parse(readFileSync(identityPath, 'utf8'));
    assert.equal(identity.did, 'did:wba:first-principle.com.cn:agent:areg-1');
    assert.equal(identity.key_id, 'did:wba:first-principle.com.cn:agent:areg-1#key-auth-1');
    assert.equal(identity.identity_dir, identityDir);

    const session = JSON.parse(readFileSync(sessionPath, 'utf8'));
    assert.equal(session.session.access_token, 'access-agent-shadow-1');
    assert.equal(session.session.refresh_token, 'refresh-agent-shadow-1');

    const enrollment = JSON.parse(readFileSync(enrollmentPath, 'utf8'));
    assert.equal(enrollment.state, 'active');
    assert.equal(enrollment.status, 'active');
    assert.equal(enrollment.agent_registry_id, 'areg-1');
    assert.equal(enrollment.agent_stable_id, 'areg-1');
    assert.equal(enrollment.did, 'did:wba:first-principle.com.cn:agent:areg-1');
    assert.equal(enrollment.identity_dir, identityDir);

    assert.equal(finalizePayload.ticket, 'ticket-3');
    assert.equal(finalizePayload.did, 'did:wba:first-principle.com.cn:agent:areg-1');
    assert.equal(finalizePayload.did_key_id, 'did:wba:first-principle.com.cn:agent:areg-1#key-auth-1');
    assert.equal(finalizePayload.did_document.id, 'did:wba:first-principle.com.cn:agent:areg-1');
    assert.deepEqual(finalizePayload.did_document.authentication, ['did:wba:first-principle.com.cn:agent:areg-1#key-auth-1']);
    assert.ok(typeof finalizePayload.signature === 'string' && finalizePayload.signature.length > 10);
    const verifyKey = createPublicKey({ key: finalizePayload.did_document.verificationMethod[0].publicKeyJwk, format: 'jwk' });
    const signature = Buffer.from(finalizePayload.signature, 'base64url');
    const challenge = 'fp.did.enrollment.finalize.v1|ticket:ticket-3|did:did:wba:first-principle.com.cn:agent:areg-1';
    assert.equal(verify(null, Buffer.from(challenge, 'utf8'), verifyKey, signature), true);
  });
});

test('reuse identity login refreshes session without creating claim', async () => {
  await withMockServer(async (req, calls) => {
    if (req.method === 'POST' && req.url === '/api/agent/auth/didwba/verify') {
      return {
        body: {
          ok: true,
          session: {
            access_token: 'access-reuse-1',
            refresh_token: 'refresh-reuse-1',
          },
          user: { id: 'agent-reuse-1' },
          profile: { id: 'agent-reuse-1' },
        },
      };
    }
    assert.fail(`reuse login should not call ${req.method} ${req.url}; calls so far: ${calls.map((call) => `${call.method} ${call.url}`).join(', ')}`);
  }, async ({ baseUrl }) => {
    const tmp = makeTmpDir();
    const identityDir = path.join(tmp, 'identity');
    const did = 'did:wba:first-principle.com.cn:agent:reuse-agent';
    writeLegacyIdentity(identityDir, did);

    const result = await runCli([
      'login',
      '--base-url', baseUrl,
      '--identity-dir', identityDir,
    ]);

    assert.equal(result.status, 0, result.stderr || result.stdout);
    assert.equal(result.json.login_mode, 'reuse-identity');
    assert.equal(result.json.did, did);
    assert.equal(result.json.session_saved_to, null);
  });
});
