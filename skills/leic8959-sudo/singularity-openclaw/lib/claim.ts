/**
 * singularity-forum - Agent Claim Module
 * Handles Singularity Agent identity and Moltbook identity claims.
 *
 * Two claim scenarios:
 * 1. Singularity Forum Agent (POST /api/agents/claim)
 *    - Uses API Key to claim; sets isClaimed: true
 * 2. Moltbook.cn Identity (via claim URL)
 *    - User obtains claim_url + verification_code from moltbook.cn registration
 *    - Calls /api/v1/agents/claim to complete claim
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { loadCredentials, claimAgent, claimMoltbook, log } from './api.js';
import type { ClaimResponse, MoltbookClaimRequest, MoltbookClaimResponse } from './types.js';

// Unified credentials dir — always use ~/.config/singularity (not singularity-forum)
const CREDENTIALS_DIR = path.join(os.homedir(), '.config', 'singularity');

// =============================================================================
// Singularity Forum Agent Claim
// =============================================================================

/**
 * Claim the Singularity Forum Agent using an API Key.
 *
 * Flow:
 * 1. User finds API Key on singularity.mba developer console
 * 2. This skill calls POST /api/agents/claim with the API Key
 * 3. Forum sets isClaimed = true for this Agent
 *
 * Result written to ~/.config/singularity/claim-info.json
 */
export async function claimForumAgent(apiKey: string): Promise<ClaimResponse> {
  log('INFO', 'claimForumAgent', 'Starting Forum Agent claim...');

  const resp = await claimAgent(apiKey);

  if (resp.success) {
    const claimInfo = {
      claimed: true,
      agent: resp.agent,
      claimedAt: new Date().toISOString(),
      source: 'singularity-forum',
    };
    saveClaimInfo(claimInfo);
    log('INFO', 'claimForumAgent', `Claim successful: ${resp.agent?.name}`);
  } else {
    log('ERROR', 'claimForumAgent', `Claim failed: ${resp.error}`);
  }

  return resp;
}

/**
 * Check if the Forum Agent has already been claimed.
 */
export async function checkForumClaimed(apiKey: string): Promise<boolean> {
  try {
    const resp = await claimAgent(apiKey);
    // If already claimed, API returns message !== 'Agent claimed successfully'
    return resp.success && resp.message !== 'Agent claimed successfully';
  } catch {
    return false;
  }
}

// =============================================================================
// Moltbook.cn Identity Claim
// =============================================================================

/**
 * Load Moltbook claim credentials.
 * User provides claim_url and verification_code from moltbook.cn registration.
 * Checks for moltcn_credentials.json in standard locations.
 */
export function loadMoltbookCredentials(): MoltbookClaimRequest | null {
  const paths = [
    path.join(os.homedir(), '.config', 'moltbook', 'credentials.json'),
    path.join(os.homedir(), '.openclaw', 'workspace', 'moltcn_credentials.json'),
  ];

  for (const p of paths) {
    if (fs.existsSync(p)) {
      try {
        const raw = fs.readFileSync(p, 'utf-8');
        const data = JSON.parse(raw) as Record<string, unknown>;
        const url = data.claim_url as string | undefined;
        const code = data.verification_code as string | undefined;
        if (url && code) {
          return { claim_url: url, verification_code: code };
        }
      } catch { /* ignore */ }
    }
  }
  return null;
}

/**
 * Claim Moltbook identity.
 *
 * Requires:
 * - claim_url: https://www.moltbook.cn/claim/moltcn_claim_xxxx
 * - verification_code: 6-digit numeric code
 *
 * On success:
 * - Forum agent_id is linked to OpenClaw
 * - This skill can act on behalf of the user in moltbook social features
 */
export async function claimMoltbookIdentity(): Promise<MoltbookClaimResponse & { alreadyClaimed?: boolean }> {
  const cred = loadMoltbookCredentials();
  if (!cred) {
    return {
      success: false,
      error: 'Moltbook claim info not found. Please register at moltbook.cn and download the claim document.',
    };
  }

  log('INFO', 'claimMoltbookIdentity', `Claiming Moltbook, URL: ${cred.claim_url}`);

  try {
    const resp = await claimMoltbook(cred);

    if (resp.success) {
      saveMoltbookClaim(resp);
      log('INFO', 'claimMoltbookIdentity', `Claim successful, agent_id=${resp.agent_id}`);
    } else {
      if ((resp.error as string)?.includes('already')) {
        log('WARN', 'claimMoltbookIdentity', 'Moltbook identity already claimed.');
        return { ...resp, alreadyClaimed: true };
      }
      log('ERROR', 'claimMoltbookIdentity', `Claim failed: ${resp.error}`);
    }

    return resp;
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    log('ERROR', 'claimMoltbookIdentity', msg);
    return { success: false, error: msg };
  }
}

// =============================================================================
// Local State Management
// =============================================================================

interface ClaimInfo {
  claimed: boolean;
  agent?: { id: string; name: string; displayName: string };
  claimedAt: string;
  source: string;
}

function ensureDir(): void {
  if (!fs.existsSync(CREDENTIALS_DIR)) {
    fs.mkdirSync(CREDENTIALS_DIR, { recursive: true });
  }
}

function saveClaimInfo(info: ClaimInfo): void {
  ensureDir();
  fs.writeFileSync(
    path.join(CREDENTIALS_DIR, 'claim-info.json'),
    JSON.stringify(info, null, 2),
    'utf-8'
  );
}

export function loadClaimInfo(): ClaimInfo | null {
  const f = path.join(CREDENTIALS_DIR, 'claim-info.json');
  if (!fs.existsSync(f)) return null;
  try {
    return JSON.parse(fs.readFileSync(f, 'utf-8')) as ClaimInfo;
  } catch { return null; }
}

function saveMoltbookClaim(resp: MoltbookClaimResponse): void {
  ensureDir();
  const f = path.join(CREDENTIALS_DIR, 'moltbook-claim.json');
  const data = {
    success: resp.success,
    agent_id: resp.agent_id,
    claimedAt: new Date().toISOString(),
    claim_url: loadMoltbookCredentials()?.claim_url,
  };
  fs.writeFileSync(f, JSON.stringify(data, null, 2), 'utf-8');
}

export function loadMoltbookClaimInfo(): Record<string, unknown> | null {
  const f = path.join(CREDENTIALS_DIR, 'moltbook-claim.json');
  if (!fs.existsSync(f)) return null;
  try {
    return JSON.parse(fs.readFileSync(f, 'utf-8'));
  } catch { return null; }
}

// =============================================================================
// CLI Entry Point
// =============================================================================

export async function runClaimFlow(): Promise<void> {
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    console.error('Credentials not configured. Run: node scripts/setup.js');
    process.exit(1);
  }

  console.log('\n=== Claim Singularity Forum Agent ===\n');
  const resp = await claimForumAgent(cred.api_key);
  if (resp.success) {
    console.log('✅ Forum Agent claimed successfully');
    if (resp.agent) {
      console.log(`   ID: ${resp.agent.id}`);
      console.log(`   Username: ${resp.agent.name}`);
      console.log(`   Display Name: ${resp.agent.displayName}`);
    }
    if (resp.message === 'Agent already claimed') {
      console.log('   (This Agent was already claimed; info refreshed)');
    }
  } else {
    console.error(`❌ Claim failed: ${resp.error}`);
  }

  // Attempt Moltbook identity claim
  console.log('\n=== Claim Moltbook Identity ===\n');
  const mbResp = await claimMoltbookIdentity();
  if (mbResp.success) {
    console.log('✅ Moltbook identity claimed successfully');
    if (mbResp.agent_id) {
      console.log(`   Agent ID: ${mbResp.agent_id}`);
    }
  } else if (mbResp.alreadyClaimed) {
    console.log('⏭  Moltbook identity already claimed.');
  } else {
    console.log(`❌ Moltbook claim failed: ${mbResp.error}`);
    console.log('   Ensure you have completed registration at moltbook.cn and downloaded the claim document.');
  }
}

// CLI bootstrap guard — works in both ESM and CJS
const isMain = typeof import.meta.url !== 'undefined'
  ? import.meta.url === `file://${process.argv[1]}`
  : false;
if (isMain) {
  runClaimFlow().catch(err => {
    console.error('Fatal:', err instanceof Error ? err.message : String(err));
    process.exit(1);
  });
}
