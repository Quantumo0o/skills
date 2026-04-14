import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pluginRoot = path.resolve(__dirname, '..');
const defaultAdapterScript = path.resolve(pluginRoot, '..', 'context-guardian-adapter.js');
const DEFAULT_GUIDANCE = [
  'Context Guardian runtime is active in adapter-backed mode.',
  'Before major actions, rely on durable state and latest summary rather than chat history alone.',
  'For risky or destructive work, checkpoint first and continue one major action at a time.',
  'If continuity state is missing or pressure is critical, stop and recover from persistent state instead of guessing.'
].join(' ');

function safeTaskId(value, prefix = 'cg') {
  const base = String(value || 'default').replace(/[^a-zA-Z0-9._-]+/g, '-').replace(/^-+|-+$/g, '');
  return `${prefix}-${base || 'default'}`;
}

function adapterConfig(api) {
  const cfg = api.pluginConfig || {};
  return {
    enabled: cfg.enabled !== false,
    adapterRoot: cfg.adapterRoot || path.join(api.resolvePath('.'), '.context-guardian-runtime'),
    adapterScript: cfg.adapterScript || defaultAdapterScript,
    taskIdPrefix: cfg.taskIdPrefix || 'cg',
    criticalThreshold: typeof cfg.criticalThreshold === 'number' ? cfg.criticalThreshold : 0.85,
    guardExec: cfg.guardExec !== false,
    prependGuidance: cfg.prependGuidance !== false,
  };
}

function deriveTaskContext(ctx, cfg) {
  const sessionKey = ctx?.sessionKey || ctx?.sessionId || 'default-session';
  return {
    taskId: safeTaskId(sessionKey, cfg.taskIdPrefix),
    sessionId: ctx?.sessionId || 'unknown-session',
    sessionKey,
  };
}

function runAdapter(api, cfg, args, { tolerateFailure = true } = {}) {
  try {
    const out = execFileSync(process.execPath, [cfg.adapterScript, ...args], {
      encoding: 'utf8',
      env: {
        ...process.env,
        CG_ADAPTER_ROOT: cfg.adapterRoot,
      },
      cwd: api.resolvePath('.'),
      timeout: 20000,
    }).trim();
    return out ? JSON.parse(out) : { ok: true };
  } catch (error) {
    api.logger?.warn?.(`context-guardian-runtime adapter call failed: ${String(error?.message || error)}`);
    if (!tolerateFailure) throw error;
    return null;
  }
}

function buildEnsureArgs(task, event, cfg) {
  return [
    'ensure',
    '--root', cfg.adapterRoot,
    '--task', task.taskId,
    '--session', task.sessionId,
    '--goal', event?.prompt || 'OpenClaw session continuity',
    '--next-action', 'Continue from the latest durable state',
  ];
}

function maybeCheckpoint(api, cfg, task, patch = {}, extraArgs = []) {
  const args = [
    'checkpoint',
    '--root', cfg.adapterRoot,
    '--task', task.taskId,
    '--patch-json', JSON.stringify(patch),
    ...extraArgs,
  ];
  return runAdapter(api, cfg, args);
}

const plugin = {
  id: 'context-guardian-runtime',
  name: 'Context Guardian Runtime',
  description: 'Hook-only runtime plugin that wires external adapter-backed continuity into OpenClaw without patching core.',
  register(api) {
    const cfg = adapterConfig(api);
    if (!cfg.enabled) return;

    api.on('session_start', async (event, ctx) => {
      const task = deriveTaskContext(ctx, cfg);
      runAdapter(api, cfg, buildEnsureArgs(task, { prompt: `Session start: ${event.sessionKey || event.sessionId}` }, cfg));
    });

    api.on('before_prompt_build', async (event, ctx) => {
      const task = deriveTaskContext(ctx, cfg);
      runAdapter(api, cfg, buildEnsureArgs(task, event, cfg));
      const resume = runAdapter(api, cfg, ['resume', '--root', cfg.adapterRoot, '--task', task.taskId]);
      const nextAction = resume?.next_action || 'Continue from durable state';
      const status = resume?.status || 'running';
      const currentPhase = resume?.current_phase || 'unknown';
      const append = cfg.prependGuidance
        ? `${DEFAULT_GUIDANCE}\nCurrent durable phase: ${currentPhase}. Durable status: ${status}. Next action: ${nextAction}.`
        : `Current durable phase: ${currentPhase}. Next action: ${nextAction}.`;
      return { prependSystemContext: append };
    });

    api.on('before_tool_call', async (event, ctx) => {
      const task = deriveTaskContext(ctx, cfg);
      const toolName = event.toolName || ctx.toolName;
      const patch = {
        status: 'running',
        current_phase: `before-tool:${toolName}`,
        next_action: `Run tool ${toolName} and persist result`,
        last_action: null,
      };
      maybeCheckpoint(api, cfg, task, patch, [
        '--event-summary', `before tool call: ${toolName}`,
        '--last-action-summary', `Preparing tool call ${toolName}`,
        '--last-action-type', 'before_tool_call',
      ]);

      if (cfg.guardExec && toolName === 'exec') {
        const command = typeof event.params?.command === 'string' ? event.params.command : '';
        const dangerous = /\b(rm\s+-rf|mkfs|dd\s+if=|shutdown|reboot|poweroff|killall|iptables|ufw\s+reset)\b/.test(command);
        if (dangerous) {
          maybeCheckpoint(api, cfg, task, {
            status: 'halted',
            current_phase: 'awaiting-approval',
            next_action: 'Wait for explicit operator approval before destructive exec',
            open_issues: ['destructive exec pending approval'],
          }, [
            '--event-summary', 'destructive exec requires approval',
            '--last-action-summary', `Guarded destructive exec: ${command}`,
            '--last-action-type', 'guard',
          ]);
          return {
            requireApproval: {
              title: 'Context Guardian: destructive exec approval',
              description: command,
              severity: 'warning',
              timeoutMs: 300000,
              timeoutBehavior: 'deny',
            },
          };
        }
      }
      return undefined;
    });

    api.on('after_tool_call', async (event, ctx) => {
      const task = deriveTaskContext(ctx, cfg);
      const toolName = event.toolName || ctx.toolName;
      const ok = !event.error;
      const patch = {
        status: ok ? 'running' : 'halted',
        current_phase: `after-tool:${toolName}`,
        next_action: ok ? 'Continue with the next checkpointable action' : 'Recover from latest durable state before continuing',
        state_confidence: ok ? 0.92 : 0.45,
        open_issues: ok ? [] : [`tool failed: ${toolName}`],
      };
      maybeCheckpoint(api, cfg, task, patch, [
        '--event-summary', ok ? `after tool call success: ${toolName}` : `after tool call failure: ${toolName}`,
        '--last-action-summary', ok ? `Tool ${toolName} completed` : `Tool ${toolName} failed: ${event.error || 'unknown error'}`,
        '--last-action-type', 'after_tool_call',
        '--last-action-outcome', ok ? 'success' : 'error',
      ]);
    });

    api.on('before_compaction', async (_event, ctx) => {
      const task = deriveTaskContext(ctx, cfg);
      maybeCheckpoint(api, cfg, task, {
        status: 'running',
        current_phase: 'before-compaction',
        next_action: 'Resume after compaction from durable state',
      }, [
        '--event-summary', 'checkpoint before compaction',
        '--last-action-summary', 'Preparing for compaction',
        '--last-action-type', 'before_compaction',
      ]);
    });

    api.on('session_end', async (_event, ctx) => {
      const task = deriveTaskContext(ctx, cfg);
      maybeCheckpoint(api, cfg, task, {
        status: 'idle',
        current_phase: 'session-ended',
        next_action: 'Wait for next session resume',
      }, [
        '--event-summary', 'session ended checkpoint',
        '--last-action-summary', 'Session ended',
        '--last-action-type', 'session_end',
      ]);
    });
  },
};

export default plugin;
