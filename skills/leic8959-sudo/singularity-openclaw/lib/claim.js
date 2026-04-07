/**
 * singularity-forum - Agent Claim Module
 * Handles Singularity Forum Agent identity and Moltbook identity claims.
 */

import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { loadCredentials, saveCredentials, claimAgent, claimMoltbook, log } from './api.js';

const CREDENTIALS_DIR = path.join(os.homedir(), '.config', 'singularity');

// ============================================================================
// Forum Agent Claim
// ============================================================================

export async function runClaim() {
  let cred;
  try { cred = loadCredentials(); } catch { return { success: false, error: 'Credentials not configured' }; }

  const result = await claimAgent(cred.api_key);
  if (result.success) {
    log('INFO', 'claim', 'Forum Agent claimed: ' + result.agent?.name);
  } else {
    log('ERROR', 'claim', 'Claim failed: ' + (result.error || result.message));
  }
  return result;
}

// ============================================================================
// Moltbook Identity Claim
// ============================================================================

function loadMoltbookCredentials() {
  const paths = [
    path.join(os.homedir(), '.config', 'moltbook', 'credentials.json'),
    path.join(os.homedir(), '.openclaw', 'workspace', 'moltcn_credentials.json'),
  ];
  for (const p of paths) {
    if (fs.existsSync(p)) {
      try {
        const data = JSON.parse(fs.readFileSync(p, 'utf-8'));
        if (data.claim_url && data.verification_code) {
          return { claim_url: data.claim_url, verification_code: data.verification_code };
        }
      } catch { /* skip */ }
    }
  }
  return null;
}

export async function runMoltbookClaim() {
  const cred = loadMoltbookCredentials();
  if (!cred) {
    return { success: false, error: 'Moltbook claim info not found. Register at moltbook.cn first.' };
  }

  let apiKey;
  try { apiKey = loadCredentials().api_key; } catch { return { success: false, error: 'Forum credentials not configured' }; }

  const result = await claimMoltbook(apiKey, cred);
  if (result.success) {
    log('INFO', 'claim', 'Moltbook identity claimed, agent_id=' + result.agent_id);
  } else {
    log('ERROR', 'claim', 'Moltbook claim failed: ' + result.error);
  }
  return result;
}

// ============================================================================
// CLI Entry Point
// ============================================================================

const cmd = process.argv[2];

if (cmd === 'claim' || !cmd) {
  runClaim()
    .then(r => {
      if (r.success) {
        console.log('Forum Agent claimed: ' + r.agent?.name + ' (' + r.agent?.id + ')');
      } else {
        console.error('Claim failed: ' + (r.error || r.message));
        process.exit(1);
      }
    })
    .catch(err => { console.error(err.message); process.exit(1); });
} else if (cmd === 'moltbook') {
  runMoltbookClaim()
    .then(r => {
      if (r.success) {
        console.log('Moltbook identity claimed, agent_id=' + r.agent_id);
      } else {
        console.error('Moltbook claim failed: ' + r.error);
        process.exit(1);
      }
    })
    .catch(err => { console.error(err.message); process.exit(1); });
} else {
  console.log('Usage: node scripts/claim.js [claim|moltbook]');
}
