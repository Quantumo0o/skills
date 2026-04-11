#!/usr/bin/env node
/**
 * 离线参数校验烟测：不依赖真实魔方服务（BASE_URL 指向无效地址即可）。
 * 用法：node scripts/smoke-cli-validation.mjs
 * 全链路联调：配置有效 .env 后另行执行各 mofang_* 命令。
 */

import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const cli = join(root, 'cli.mjs');

const env = {
  ...process.env,
  BASE_URL: 'http://127.0.0.1:9',
  USERNAME: 'smoke',
  PASSWORD: 'smoke',
};

function run(args, expectSuccess = false) {
  const r = spawnSync(process.execPath, [cli, ...args], {
    encoding: 'utf-8',
    env,
    cwd: root,
  });
  const out = (r.stdout || '').trim();
  let j;
  try {
    j = JSON.parse(out);
  } catch {
    console.error('FAIL non-JSON:', args[0], out || r.stderr);
    process.exit(1);
  }
  if (expectSuccess && !j.success) {
    console.error('FAIL expected success:', args[0], j);
    process.exit(1);
  }
  if (!expectSuccess && j.success) {
    console.error('FAIL expected failure:', args[0], j);
    process.exit(1);
  }
  return j;
}

const cases = [
  [['mofang_bpm_get_task', '{}'], '需要 taskId'],
  [['mofang_bpm_jump_task', '{"taskId":"1"}'], 'kind'],
  [['mofang_bpm_delegate_task', '{"taskId":"1"}'], 'assignee'],
  [['mofang_bpm_open_transaction', '{}'], 'taskAction'],
  [['mofang_bpm_close_transaction', '{}'], 'transactionId'],
  [['mofang_bpm_query_tasks', '{"recordId":"1"}'], 'formHint'],
  [['mofang_bpm_list_tasks', '{"mode":"nope"}'], 'mode'],
  [['mofang_bpm_complete_task', '{"taskId":"1","simple":true}'], 'variables'],
];

console.log('smoke-cli-validation: param checks');
for (const [[cmd, json], needle] of cases) {
  const j = run([cmd, json]);
  if (!j.message || !String(j.message).includes(needle)) {
    console.error('FAIL message mismatch', cmd, j.message, 'expected contains:', needle);
    process.exit(1);
  }
  console.log('  ok', cmd);
}

const badJson = spawnSync(process.execPath, [cli, 'mofang_bpm_get_task', '{x}'], {
  encoding: 'utf-8',
  env,
  cwd: root,
});
const badOut = (badJson.stdout || '').trim();
if (!badOut.includes('Invalid JSON')) {
  console.error('FAIL invalid JSON handling', badOut);
  process.exit(1);
}
console.log('  ok invalid JSON');

console.log('all param-validation checks passed.');
