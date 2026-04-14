#!/usr/bin/env node
'use strict';

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const adapterPath = path.join(__dirname, 'context-guardian-adapter.js');

function tmpRoot() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'cg-adapter-test-'));
}

function run(args, root) {
  const output = execFileSync(process.execPath, [adapterPath, ...args], {
    encoding: 'utf8',
    env: { ...process.env, CG_ADAPTER_ROOT: root },
  });
  return output.trim() ? JSON.parse(output) : null;
}

(function testEnsureAndStatus() {
  const root = tmpRoot();
  const ensured = run(['ensure', '--task', 'task-1', '--session', 'session-1', '--goal', 'Preserve continuity'], root);
  assert.equal(ensured.ok, true);
  assert.equal(ensured.created, true);
  const status = run(['status', '--task', 'task-1'], root);
  assert.equal(status.state_exists, true);
  assert.equal(status.summary_exists, true);
})();

(function testCheckpointAndResume() {
  const root = tmpRoot();
  run(['ensure', '--task', 'task-2', '--session', 'session-2', '--goal', 'Checkpoint state'], root);
  const checkpoint = run([
    'checkpoint',
    '--task', 'task-2',
    '--phase', 'implementation',
    '--status', 'running',
    '--next-action', 'Run validation',
    '--last-action-summary', 'Patched adapter',
    '--state-confidence', '0.9',
    '--file', 'plugin/context-guardian-adapter.js'
  ], root);
  assert.equal(checkpoint.ok, true);
  const resumed = run(['resume', '--task', 'task-2'], root);
  assert.equal(resumed.next_action, 'Run validation');
  assert.equal(resumed.current_phase, 'implementation');
})();

(function testCriticalCheckpointHalts() {
  const root = tmpRoot();
  run(['ensure', '--task', 'task-3', '--session', 'session-3', '--goal', 'Halt on pressure'], root);
  const result = run([
    'checkpoint',
    '--task', 'task-3',
    '--pressure', '0.91',
    '--critical-threshold', '0.85',
    '--event-summary', 'Pressure too high'
  ], root);
  assert.equal(result.critical, true);
  const resumed = run(['resume', '--task', 'task-3'], root);
  assert.equal(resumed.status, 'halted');
})();

(function testBundleIncludesSummaryAndFiles() {
  const root = tmpRoot();
  const sampleFile = path.join(root, 'sample.txt');
  fs.writeFileSync(sampleFile, 'hello bundle\n', 'utf8');
  run(['ensure', '--task', 'task-4', '--session', 'session-4', '--goal', 'Bundle context'], root);
  run([
    'checkpoint',
    '--task', 'task-4',
    '--artifact-json', JSON.stringify({ path: sampleFile, kind: 'file', description: 'sample file' }),
    '--next-action', 'Read bundle'
  ], root);
  const bundled = run(['bundle', '--task', 'task-4', '--system-instructions', 'Follow the task', '--json'], root);
  assert.equal(bundled.ok, true);
  assert.ok(bundled.bundle.includes('# Working Context Bundle'));
  assert.ok(bundled.bundle.includes('hello bundle'));
})();

(function testHaltWritesReason() {
  const root = tmpRoot();
  run(['ensure', '--task', 'task-5', '--session', 'session-5', '--goal', 'Explicit halt'], root);
  run(['halt', '--task', 'task-5', '--reason', 'manual stop', '--next-action', 'Wait for operator'], root);
  const resumed = run(['resume', '--task', 'task-5'], root);
  assert.equal(resumed.status, 'halted');
  assert.equal(resumed.next_action, 'Wait for operator');
})();

console.log('OK');
