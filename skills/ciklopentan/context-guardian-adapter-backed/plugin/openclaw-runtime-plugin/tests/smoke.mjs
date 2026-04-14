import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import plugin from '../dist/index.js';

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'cg-runtime-plugin-'));
const pluginWorkspace = fs.mkdtempSync(path.join(os.tmpdir(), 'cg-runtime-plugin-workspace-'));
const adapterScript = path.resolve(process.cwd(), '..', 'context-guardian-adapter.js');

const hooks = new Map();
const api = {
  pluginConfig: {
    adapterRoot: tempRoot,
    adapterScript,
    taskIdPrefix: 'testcg',
    guardExec: true,
    prependGuidance: true,
  },
  resolvePath(input) {
    return path.resolve(pluginWorkspace, input);
  },
  logger: {
    warn() {},
    info() {},
  },
  on(name, handler) {
    hooks.set(name, handler);
  },
};

plugin.register(api);
assert.ok(hooks.has('session_start'));
assert.ok(hooks.has('before_prompt_build'));
assert.ok(hooks.has('before_tool_call'));
assert.ok(hooks.has('after_tool_call'));

await hooks.get('session_start')({ sessionId: 's1', sessionKey: 'agent:main:test' }, { sessionId: 's1', sessionKey: 'agent:main:test' });
const promptResult = await hooks.get('before_prompt_build')({ prompt: 'Do work', messages: [] }, { sessionId: 's1', sessionKey: 'agent:main:test', toolName: '' });
assert.ok(promptResult.prependSystemContext.includes('Context Guardian runtime is active'));

const approval = await hooks.get('before_tool_call')({ toolName: 'exec', params: { command: 'rm -rf /tmp/demo' } }, { sessionId: 's1', sessionKey: 'agent:main:test', toolName: 'exec' });
assert.ok(approval.requireApproval);

await hooks.get('after_tool_call')({ toolName: 'exec', params: { command: 'echo ok' }, result: { ok: true } }, { sessionId: 's1', sessionKey: 'agent:main:test', toolName: 'exec' });

const statePath = path.join(tempRoot, 'tasks');
assert.ok(fs.existsSync(statePath));
console.log('OK');
