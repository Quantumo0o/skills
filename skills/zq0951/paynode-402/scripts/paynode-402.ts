#!/usr/bin/env bun
import { cac } from 'cac';
import { checkAction } from './commands/check.ts';
import { mintAction } from './commands/mint.ts';
import { requestAction } from './commands/request.ts';
import { EXIT_CODES } from './utils.ts';

const cli = cac('paynode-402');

// Global Options
cli.option('--json', 'Output results in JSON format');
cli.option('--network <name>', 'Network to use: mainnet or testnet/sepolia');
cli.option('--rpc <url>', 'Custom RPC URL');
cli.option('--confirm-mainnet', 'Required flag for mainnet operations (real USDC)');
cli.option('--dry-run', 'Show request details without sending');

// Command: check
cli
  .command('check', 'Check wallet balance (ETH and USDC) on Base L2')
  .action((options) => {
    return checkAction(options);
  });

// Command: mint
cli
  .command('mint', 'Mint USDC on Base Sepolia')
  .option('--amount <amount>', 'Amount to mint (default: 1000)')
  .action((options) => {
    return mintAction(options);
  });

// Command: request
cli
  .command('request <url> [...params]', 'Access protected API and handle x402 payments')
  .option('-X, --method <method>', 'HTTP method (GET, POST, etc.)')
  .option('-d, --data <data>', 'Raw request body data')
  .option('-H, --header [header]', 'HTTP header in "Key: Value" format (can be used multiple times)', { default: [] })
  .option('--background', 'Execute in background, return immediately (AI-friendly)')
  .option('--output <path>', 'Output file path for result (used with --background)')
  .option('--max-age <seconds>', 'Auto-delete task files older than N seconds (default: 3600)')
  .option('--task-dir <path>', 'Task directory for background results (default: <TMPDIR>/paynode-tasks)')
  .option('--task-id <id>', 'Internal: task ID for background worker')
  .action((url, params, options) => {
    return requestAction(url, params, options);
  });

cli.help();
cli.version('2.2.0');

try {
  const result = cli.parse();
  if (result instanceof Promise) {
    result.catch((err) => {
        console.error(`❌ Uncaught Async Error: ${err.message}`);
        process.exit(EXIT_CODES.GENERIC_ERROR);
    });
  }
} catch (error: any) {
  console.error(`❌ Parse Error: ${error.message}`);
  process.exit(EXIT_CODES.INVALID_ARGS);
}
