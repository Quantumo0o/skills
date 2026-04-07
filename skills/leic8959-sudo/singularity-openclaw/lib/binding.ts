/**
 * singularity-forum - Identity Binding Module
 * Handles two-way binding between OpenClaw and the Singularity Forum.
 *
 * Binding flow:
 * 1. Forum side: user clicks "Connect OpenClaw" in settings, generates a BIND-XXXXXX code (10 min TTL)
 * 2. OpenClaw side: this skill reads the bind code and completes the pairing
 * 3. Verification: bidirectional ping confirms the link is live
 */

import * as readline from 'readline';
import {
  loadCredentials,
  saveCredentials,
  generateBindCode,
  bindForum,
  getBindStatus,
  unbind,
  log,
} from './api.js';
import type { BindStatusResponse } from './types.js';

// ============================================================================
// Interactive I/O
// ============================================================================

function prompt(question: string): Promise<string> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise(resolve => {
    rl.question(question, ans => {
      rl.close();
      resolve(ans.trim());
    });
  });
}

function promptDefault(question: string, defaultVal: string): Promise<string> {
  return prompt(`${question} [${defaultVal}]: `).then(v => v === '' ? defaultVal : v);
}

// ============================================================================
// Credential init
// ============================================================================

export async function ensureCredentials() {
  try {
    return loadCredentials();
  } catch {
    log('INFO', 'ensureCredentials', 'No credentials found, launching setup...');
    return await interactiveSetup();
  }
}

export async function interactiveSetup() {
  console.log('\n=== Singularity Forum Skill Setup Wizard ===\n');
  console.log('Please provide the following information (press Enter to use defaults):\n');

  const apiKey = await promptDefault('Forum API Key (from singularity.mba settings page)', '');
  if (!apiKey) throw new Error('API Key cannot be empty');

  const username = await promptDefault('Forum username', '');
  if (!username) throw new Error('Username cannot be empty');

  const webhookUrl = await promptDefault('OpenClaw Webhook URL (OpenClaw Gateway address)', 'http://localhost:18789');
  const token = await promptDefault('OpenClaw Token (for signing webhook requests)', '');
  const agentId = await promptDefault('OpenClaw Agent ID (leave blank for default: main)', 'main');

  const cred = {
    api_key: apiKey,
    forum_username: username,
    openclaw_webhook_url: webhookUrl,
    openclaw_token: token,
    openclaw_agent_id: agentId || 'main',
  };

  saveCredentials(cred);
  log('INFO', 'interactiveSetup', 'Credentials saved');
  console.log('\n✅ Credentials saved to ~/.config/singularity/credentials.json\n');
  return cred;
}

// ============================================================================
// Bind flow
// ============================================================================

export interface BindResult {
  success: boolean;
  message: string;
  status?: BindStatusResponse;
}

export async function runBindFlow(): Promise<BindResult> {
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    console.error('Please complete credential setup first: node scripts/setup.js');
    process.exit(1);
  }

  // Step 1: generate bind code
  console.log('\n=== Bind Step 1/2: Generate Bind Code ===\n');
  log('INFO', 'runBindFlow', 'Starting bind flow');
  let bindCode: string;
  let expiresIn = 0;
  try {
    // Use api_key (canonical field) — forum_api_key is an alias in Credentials
    const apiKey = cred.api_key || (cred as Record<string, unknown>).forum_api_key as string;
    const codeResult = await generateBindCode(apiKey);
    bindCode = codeResult.bindCode.toUpperCase();
    expiresIn = codeResult.expiresIn;
    console.log(`\n🔑  Bind code: ${bindCode}`);
    console.log(`⏱   Valid for: ${Math.floor(expiresIn / 60)}m ${expiresIn % 60}s`);
    console.log('\nPlease paste this bind code into the "Connect OpenClaw" field in your forum settings page.\n');
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    if (msg.includes('401')) {
      return { success: false, message: 'API Key invalid. Please check forum_api_key in credentials.' };
    }
    return { success: false, message: `Failed to generate bind code: ${msg}` };
  }

  // Step 2: confirm binding
  const confirm = await promptDefault('\nBind code entered in forum settings? (y/n)', 'n');
  if (confirm.toLowerCase() !== 'y') {
    return { success: false, message: 'Cancelled' };
  }

  console.log('\n=== Bind Step 2/2: Confirm Binding ===\n');
  try {
    const result = await bindForum({
      forum_username: cred.forum_username!,
      bind_code: bindCode,
      openclaw_webhook_url: cred.openclaw_webhook_url!,
      openclaw_token: cred.openclaw_token!,
      openclaw_agent_id: cred.openclaw_agent_id,
    });

    if (!result.success) {
      return { success: false, message: result.error || 'Binding failed' };
    }

    cred.bound = true;
    cred.bound_at = new Date().toISOString();
    saveCredentials(cred as Parameters<typeof saveCredentials>[0]);

    console.log('✅ Binding successful!\n');

    const apiKey = cred.api_key || (cred as Record<string, unknown>).forum_api_key as string;
    const status = await getBindStatus(apiKey);
    console.log(`   Webhook Host: ${status.webhookHost || 'unknown'}`);
    console.log(`   Agent ID: ${status.agentId || 'default'}`);
    console.log(`   Bound at: ${status.boundAt || 'unknown'}`);

    return { success: true, message: 'Binding successful', status };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    if (msg.includes('400')) {
      return { success: false, message: 'Bind code invalid or expired. Please run the bind flow again.' };
    }
    return { success: false, message: `Binding failed: ${msg}` };
  }
}

export async function quickBind(bindCode: string): Promise<BindResult> {
  const CODE_REGEX = /^BIND-[A-Z0-9]{6}$/;
  if (!CODE_REGEX.test(bindCode.toUpperCase())) {
    return { success: false, message: `Invalid bind code format: ${bindCode} (expected: BIND-XXXXXX)` };
  }
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return { success: false, message: 'Credentials not configured. Run setup first.' };
  }

  try {
    const result = await bindForum({
      forum_username: cred.forum_username!,
      bind_code: bindCode,
      openclaw_webhook_url: cred.openclaw_webhook_url!,
      openclaw_token: cred.openclaw_token!,
      openclaw_agent_id: cred.openclaw_agent_id,
    });

    if (!result.success) {
      return { success: false, message: result.error || 'Binding failed' };
    }

    cred.bound = true;
    cred.bound_at = new Date().toISOString();
    saveCredentials(cred as Parameters<typeof saveCredentials>[0]);
    log('INFO', 'quickBind', `Binding successful, bindCode=${bindCode}`);

    return { success: true, message: 'Binding successful' };
  } catch (err) {
    return { success: false, message: err instanceof Error ? err.message : String(err) };
  }
}

// ============================================================================
// Status check
// ============================================================================

export async function checkStatus(): Promise<BindStatusResponse & { configured: boolean }> {
  try {
    const cred = loadCredentials();
    try {
      const apiKey = cred.api_key || (cred as Record<string, unknown>).forum_api_key as string;
      const status = await getBindStatus(apiKey);
      return { ...status, configured: true };
    } catch (err) {
      return { bound: false, configured: true, error: err instanceof Error ? err.message : String(err) };
    }
  } catch {
    return { bound: false, configured: false };
  }
}

// ============================================================================
// Unbind
// ============================================================================

export async function runUnbind(): Promise<{ success: boolean; message: string }> {
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return { success: false, message: 'Credentials file not found' };
  }

  const confirm = await prompt('Confirm unbind? This cannot be undone (yes/no): ');
  if (confirm !== 'yes') return { success: false, message: 'Cancelled' };

  try {
    const apiKey = cred.api_key || (cred as Record<string, unknown>).forum_api_key as string;
    await unbind(apiKey);
    cred.bound = false;
    delete cred.bound_at;
    saveCredentials(cred as Parameters<typeof saveCredentials>[0]);
    log('INFO', 'runUnbind', 'Unbind successful');
    return { success: true, message: 'Unbound. OpenClaw and Forum connection severed.' };
  } catch (err) {
    return { success: false, message: err instanceof Error ? err.message : String(err) };
  }
}

// ============================================================================
// CLI entry point
// ============================================================================

const cmd = process.argv[2];

async function main() {
  switch (cmd) {
    case 'bind':
      await runBindFlow();
      break;
    case 'status': {
      const s = await checkStatus();
      console.log('\n=== Binding Status ===\n');
      if (!s.configured) {
        console.log('❌ Credentials not configured. Run: node scripts/setup.js');
      } else if (s.bound) {
        console.log('✅ Bound');
        console.log(`   Webhook: ${s.webhookHost}`);
        console.log(`   Agent ID: ${s.agentId}`);
        console.log(`   Bound at: ${s.boundAt}`);
      } else {
        console.log('⏳ Not bound');
        if (s.error) console.log(`   Error: ${s.error}`);
        console.log('\nRun node scripts/bind.js bind to start binding.');
      }
      break;
    }
    case 'unbind':
      await runUnbind().then(r => console.log(`\n${r.success ? '✅' : '❌'} ${r.message}`));
      break;
    default:
      console.log('Usage:');
      console.log('  node scripts/bind.js bind    # bind');
      console.log('  node scripts/bind.js status # status');
      console.log('  node scripts/bind.js unbind # unbind');
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(err => {
    console.error('Fatal:', err instanceof Error ? err.message : String(err));
    process.exit(1);
  });
}
