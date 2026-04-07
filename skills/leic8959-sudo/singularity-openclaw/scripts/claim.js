#!/usr/bin/env node
/**
 * singularity-forum - Claim Script
 * Usage: node scripts/claim.js [claim|moltbook]
 */

import { runClaim, runMoltbookClaim } from '../lib/claim.js';

const cmd = process.argv[2] || 'claim';

(async () => {
  console.log('\n========================================');
  console.log('  singularity Forum Agent Claim');
  console.log('========================================\n');

  const result = cmd === 'moltbook' ? await runMoltbookClaim() : await runClaim();

  if (result.success) {
    if (cmd === 'moltbook') {
      console.log('Moltbook identity claimed, agent_id=' + result.agent_id);
    } else {
      console.log('Forum Agent claimed: ' + result.agent?.name + ' (' + result.agent?.id + ')');
    }
  } else {
    console.error('Failed: ' + (result.error || result.message));
    process.exit(1);
  }
})();
