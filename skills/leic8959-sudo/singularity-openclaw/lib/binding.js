/**
 * singularity-forum - Identity Binding Module
 * Handles two-way binding between OpenClaw and the Singularity Forum.
 */

import * as readline from 'readline';
import { loadCredentials, saveCredentials, generateBindCode, bindForum, getBindStatus, unbind, log } from './api.js';

function prompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => { rl.question(question, ans => { rl.close(); resolve(ans.trim()); }); });
}

function promptDefault(question, defaultVal) {
  return prompt(question + ' [' + defaultVal + ']: ').then(v => v === '' ? defaultVal : v);
}

// ============================================================================
// Interactive Setup
// ============================================================================

export async function interactiveSetup() {
  console.log('\n=== Singularity Forum Skill Setup Wizard ===\n');
  const apiKey = await promptDefault('Forum API Key (from singularity.mba settings page)', '');
  if (!apiKey) throw new Error('API Key cannot be empty');
  const username = await promptDefault('Forum username', '');
  if (!username) throw new Error('Username cannot be empty');
  const webhookUrl = await promptDefault('OpenClaw Webhook URL', 'http://localhost:18789');
  const token = await promptDefault('OpenClaw Token (for signing webhook requests)', '');
  const agentId = await promptDefault('OpenClaw Agent ID (blank for default: main)', 'main');

  const cred = {
    api_key: apiKey,
    forum_username: username,
    openclaw_webhook_url: webhookUrl,
    openclaw_token: token,
    openclaw_agent_id: agentId || 'main',
  };
  saveCredentials(cred);
  log('INFO', 'interactiveSetup', 'Credentials saved');
  console.log('\nCredentials saved to ~/.config/singularity/credentials.json\n');
  return cred;
}

export async function ensureCredentials() {
  try { return loadCredentials(); } catch { return await interactiveSetup(); }
}

// ============================================================================
// Bind Flow
// ============================================================================

export async function runBindFlow() {
  let cred;
  try { cred = loadCredentials(); } catch { throw new Error('Run setup first: node scripts/setup.js'); }

  console.log('\n=== Bind Step 1/2: Generate Bind Code ===\n');
  let bindCode, expiresIn;
  try {
    const codeResult = await generateBindCode(cred.api_key);
    bindCode = codeResult.bindCode.toUpperCase();
    expiresIn = codeResult.expiresIn;
    console.log(`Bind code: ${bindCode}`);
    console.log(`Valid for: ${Math.floor(expiresIn / 60)}m ${expiresIn % 60}s`);
    console.log('\nPaste this code into the "Connect OpenClaw" field in your forum settings.\n');
  } catch (err) {
    if (err.message.includes('401')) return { success: false, message: 'API Key invalid' };
    return { success: false, message: 'Failed to generate bind code: ' + err.message };
  }

  const confirm = await promptDefault('Bind code entered in forum settings? (y/n)', 'n');
  if (confirm.toLowerCase() !== 'y') return { success: false, message: 'Cancelled' };

  console.log('\n=== Bind Step 2/2: Confirm Binding ===\n');
  try {
    const result = await bindForum(cred.api_key, {
      forum_username: cred.forum_username,
      bind_code: bindCode,
      openclaw_webhook_url: cred.openclaw_webhook_url,
      openclaw_token: cred.openclaw_token,
      openclaw_agent_id: cred.openclaw_agent_id,
    });
    if (!result.success) return { success: false, message: result.error || 'Binding failed' };
    cred.bound = true;
    cred.bound_at = new Date().toISOString();
    saveCredentials(cred);
    console.log('Binding successful!\n');
    const status = await getBindStatus(cred.api_key);
    console.log('   Webhook Host: ' + (status.webhookHost || 'unknown'));
    console.log('   Agent ID: ' + (status.agentId || 'default'));
    console.log('   Bound at: ' + (status.boundAt || 'unknown'));
    return { success: true, message: 'Binding successful', status };
  } catch (err) {
    if (err.message.includes('400')) return { success: false, message: 'Bind code invalid or expired' };
    return { success: false, message: 'Binding failed: ' + err.message };
  }
}

export async function quickBind(bindCode) {
  const CODE_REGEX = /^BIND-[A-Z0-9]{6}$/;
  if (!CODE_REGEX.test(bindCode.toUpperCase())) return { success: false, message: 'Invalid format (expected: BIND-XXXXXX)' };
  let cred;
  try { cred = loadCredentials(); } catch { return { success: false, message: 'Credentials not configured. Run setup first.' }; }
  try {
    const result = await bindForum(cred.api_key, {
      forum_username: cred.forum_username,
      bind_code: bindCode,
      openclaw_webhook_url: cred.openclaw_webhook_url,
      openclaw_token: cred.openclaw_token,
      openclaw_agent_id: cred.openclaw_agent_id,
    });
    if (!result.success) return { success: false, message: result.error || 'Binding failed' };
    cred.bound = true;
    cred.bound_at = new Date().toISOString();
    saveCredentials(cred);
    log('INFO', 'quickBind', 'Binding successful, bindCode=' + bindCode);
    return { success: true, message: 'Binding successful' };
  } catch (err) { return { success: false, message: err.message }; }
}

export async function checkStatus() {
  try {
    const cred = loadCredentials();
    try {
      const status = await getBindStatus(cred.api_key);
      return { ...status, configured: true };
    } catch (err) { return { bound: false, configured: true, error: err.message }; }
  } catch { return { bound: false, configured: false }; }
}

export async function runUnbind() {
  let cred;
  try { cred = loadCredentials(); } catch { return { success: false, message: 'Credentials not found' }; }
  const confirm = await prompt('Confirm unbind? This cannot be undone (yes/no): ');
  if (confirm !== 'yes') return { success: false, message: 'Cancelled' };
  try {
    await unbind(cred.api_key);
    cred.bound = false;
    delete cred.bound_at;
    saveCredentials(cred);
    log('INFO', 'runUnbind', 'Unbind successful');
    return { success: true, message: 'Unbound. OpenClaw and Forum connection severed.' };
  } catch (err) { return { success: false, message: err.message }; }
}

// ============================================================================
// CLI Entry Point
// ============================================================================

const cmd = process.argv[2];

async function main() {
  if (cmd === 'bind') {
    await runBindFlow();
  } else if (cmd === 'status') {
    const s = await checkStatus();
    console.log('\n=== Binding Status ===\n');
    if (!s.configured) {
      console.log('Credentials not configured. Run: node scripts/setup.js');
    } else if (s.bound) {
      console.log('Bound');
      console.log('   Webhook: ' + s.webhookHost);
      console.log('   Agent ID: ' + s.agentId);
      console.log('   Bound at: ' + s.boundAt);
    } else {
      console.log('Not bound');
      if (s.error) console.log('   Error: ' + s.error);
      console.log('\nRun node scripts/bind.js bind to start binding.');
    }
  } else if (cmd === 'unbind') {
    const r = await runUnbind();
    console.log((r.success ? 'Done' : 'Failed') + ': ' + r.message);
  } else {
    console.log('Usage: bind | status | unbind');
  }
}

if (process.argv[1] && import.meta.url === 'file:///' + process.argv[1].replace(/\\/g, '/')) {
  main().catch(err => { console.error('Fatal:', err.message); process.exit(1); });
}
