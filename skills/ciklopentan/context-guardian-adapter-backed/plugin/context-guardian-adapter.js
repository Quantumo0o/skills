#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

const SCHEMA_VERSION = '2.1';

function isoNow() {
  return new Date().toISOString();
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (next == null || next.startsWith('--')) {
      if (args[key] === undefined) {
        args[key] = true;
      } else if (Array.isArray(args[key])) {
        args[key].push(true);
      } else {
        args[key] = [args[key], true];
      }
      continue;
    }
    i += 1;
    if (args[key] === undefined) {
      args[key] = next;
    } else if (Array.isArray(args[key])) {
      args[key].push(next);
    } else {
      args[key] = [args[key], next];
    }
  }
  return args;
}

function asArray(value) {
  if (value === undefined) return [];
  return Array.isArray(value) ? value : [value];
}

function requireString(args, key, fallback) {
  const value = args[key] !== undefined ? args[key] : fallback;
  if (typeof value !== 'string' || value.trim() === '') {
    throw new Error(`Missing required --${key}`);
  }
  return value;
}

function resolveRoot(args) {
  const value = args.root || process.env.CG_ADAPTER_ROOT || process.env.CG_ROOT;
  if (!value || typeof value !== 'string') {
    throw new Error('Missing storage root. Pass --root or set CG_ADAPTER_ROOT.');
  }
  return path.resolve(value);
}

function resolveLayout(root) {
  return {
    root,
    configPath: path.join(root, 'config.yaml'),
    tasksDir: path.join(root, 'tasks'),
    summariesDir: path.join(root, 'summaries'),
    snapshotsDir: path.join(root, 'snapshots'),
    logsDir: path.join(root, 'logs'),
    testsDir: path.join(root, 'tests'),
    latestSummaryPath: path.join(root, 'summaries', 'latest-summary.md'),
    eventsPath: path.join(root, 'logs', 'events.ndjson'),
  };
}

function ensureDirs(layout) {
  for (const dirPath of [layout.root, layout.tasksDir, layout.summariesDir, layout.snapshotsDir, layout.logsDir, layout.testsDir]) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function atomicWrite(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const tempPath = path.join(path.dirname(filePath), `.tmp-${path.basename(filePath)}-${process.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}`);
  fs.writeFileSync(tempPath, content, 'utf8');
  fs.renameSync(tempPath, filePath);
}

function readJsonIfExists(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function readTextIfExists(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return fs.readFileSync(filePath, 'utf8');
}

function appendEvent(layout, event) {
  ensureDirs(layout);
  fs.appendFileSync(layout.eventsPath, `${JSON.stringify(event)}\n`, 'utf8');
}

function taskStatePath(layout, taskId) {
  return path.join(layout.tasksDir, `${taskId}.state.json`);
}

function taskSummaryPath(layout, taskId) {
  return path.join(layout.summariesDir, `${taskId}.summary.md`);
}

function snapshotPath(layout, taskId) {
  const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
  return path.join(layout.snapshotsDir, `${taskId}-${stamp}.json`);
}

function defaultState({ taskId, sessionId, goal, status = 'idle', phase = 'initial', nextAction = 'START' }) {
  return {
    schema_version: SCHEMA_VERSION,
    task_id: taskId,
    session_id: sessionId,
    goal,
    status,
    current_phase: phase,
    plan: [],
    completed_steps: [],
    open_issues: [],
    decisions: [],
    constraints: [],
    important_facts: [],
    artifacts: [],
    last_action: null,
    next_action: nextAction,
    recovery_instructions: [
      'Read the latest durable task state.',
      'Read the latest durable summary.',
      'Verify files before editing.',
      'Resume from next_action only if constraints still hold.',
    ],
    state_confidence: 0.0,
    updated_at: isoNow(),
  };
}

function summarizeState(state) {
  const completed = (state.completed_steps || []).map((item) => `- ${item}`).join('\n') || '- none';
  const decisions = (state.decisions || []).map((item) => `- Decision: ${item.decision || ''}\n  Reason: ${item.reason || ''}`).join('\n') || '- none';
  const constraints = (state.constraints || []).map((item) => `- ${item}`).join('\n') || '- none';
  const artifacts = (state.artifacts || []).map((item) => `- path: ${item.path}\n  role: ${item.kind || 'file'}`).join('\n') || '- none';
  const issues = (state.open_issues || []).map((item) => `- ${item}`).join('\n') || '- none';
  const lastAction = state.last_action && state.last_action.summary ? state.last_action.summary : 'none';
  const nextAction = state.next_action || 'none';
  return [
    '# Context Guardian Summary',
    '',
    '## Goal',
    state.goal || 'none',
    '',
    '## Current Phase',
    state.current_phase || 'initial',
    '',
    '## Completed',
    completed,
    '',
    '## Decisions',
    decisions,
    '',
    '## Constraints',
    constraints,
    '',
    '## Artifacts',
    artifacts,
    '',
    '## Open Issues',
    issues,
    '',
    '## Last Successful Action',
    lastAction,
    '',
    '## Next Action',
    nextAction,
    '',
    '## Recovery Notes',
    '- Resume from the latest durable state.',
    '- Re-check important files before editing.',
    '- Do not redo completed work without validation.',
    '- Do not overwrite durable state without a fresh checkpoint.',
    '',
  ].join('\n');
}

function writeStateArtifacts(layout, state, summaryText, filesTouched, eventType, eventSummary) {
  ensureDirs(layout);
  const statePath = taskStatePath(layout, state.task_id);
  const summaryPath = taskSummaryPath(layout, state.task_id);
  const snapPath = snapshotPath(layout, state.task_id);
  const snapshot = {
    timestamp: isoNow(),
    schema_version: state.schema_version || SCHEMA_VERSION,
    task_id: state.task_id,
    session_id: state.session_id,
    goal: state.goal,
    status: state.status,
    current_phase: state.current_phase,
    next_action: state.next_action,
    state_confidence: state.state_confidence,
    files_touched: filesTouched,
    summary: summaryText,
  };
  atomicWrite(statePath, `${JSON.stringify(state, null, 2)}\n`);
  atomicWrite(summaryPath, summaryText);
  atomicWrite(layout.latestSummaryPath, summaryText);
  atomicWrite(snapPath, `${JSON.stringify(snapshot, null, 2)}\n`);
  appendEvent(layout, {
    timestamp: isoNow(),
    task_id: state.task_id,
    event_type: eventType,
    summary: eventSummary,
    files_changed: filesTouched,
    success: true,
    confidence: state.state_confidence,
  });
  return { statePath, summaryPath, snapshotPath: snapPath };
}

function mergeState(baseState, patch) {
  const state = { ...baseState, ...patch };
  state.schema_version = SCHEMA_VERSION;
  state.updated_at = isoNow();
  if (patch.last_action === null) {
    state.last_action = null;
  }
  return state;
}

function safeReadFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    return `[missing or unreadable: ${filePath}]`;
  }
}

function normalizeArtifacts(values) {
  return values.map((value) => {
    try {
      const parsed = JSON.parse(value);
      return {
        path: parsed.path,
        kind: parsed.kind || 'file',
        description: parsed.description || '',
      };
    } catch {
      return {
        path: value,
        kind: 'file',
        description: 'explicit artifact',
      };
    }
  });
}

function buildBundle({ systemInstructions, state, summary, filePaths }) {
  const fileSections = [];
  for (const filePath of filePaths) {
    fileSections.push(`### ${filePath}`);
    fileSections.push('```text');
    fileSections.push(safeReadFile(filePath));
    fileSections.push('```');
    fileSections.push('');
  }
  return [
    '# Working Context Bundle',
    '',
    '## System Instructions',
    systemInstructions || 'none',
    '',
    '## Goal',
    state.goal || 'none',
    '',
    '## Current Phase',
    state.current_phase || 'initial',
    '',
    '## Next Action',
    state.next_action || 'none',
    '',
    '## Last Successful Action',
    state.last_action && state.last_action.summary ? state.last_action.summary : 'none',
    '',
    '## Constraints',
    (state.constraints || []).map((item) => `- ${item}`).join('\n') || '- none',
    '',
    '## Relevant Artifacts',
    filePaths.map((item) => `- ${item}`).join('\n') || '- none',
    '',
    '## Latest Structured Summary',
    summary || 'none',
    '',
    '## File Contents',
    fileSections.join('\n') || 'none',
  ].join('\n');
}

function parsePressure(args) {
  if (args.pressure === undefined || args.pressure === true) return null;
  const value = Number(args.pressure);
  if (!Number.isFinite(value) || value < 0 || value > 1) {
    throw new Error('Invalid --pressure. Expected numeric value between 0.0 and 1.0.');
  }
  return value;
}

function criticalThreshold(args) {
  const raw = args['critical-threshold'];
  if (raw === undefined || raw === true) return 0.85;
  const value = Number(raw);
  if (!Number.isFinite(value) || value <= 0 || value > 1) {
    throw new Error('Invalid --critical-threshold. Expected numeric value between 0.0 and 1.0.');
  }
  return value;
}

function writeJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function loadState(layout, taskId) {
  const state = readJsonIfExists(taskStatePath(layout, taskId));
  if (!state) {
    throw new Error(`Task state not found for ${taskId}`);
  }
  return state;
}

function commandStatus(args) {
  const root = resolveRoot(args);
  const layout = resolveLayout(root);
  const taskId = requireString(args, 'task');
  const statePath = taskStatePath(layout, taskId);
  const summaryPath = taskSummaryPath(layout, taskId);
  const state = readJsonIfExists(statePath);
  const summaryText = readTextIfExists(summaryPath) || readTextIfExists(layout.latestSummaryPath);
  writeJson({
    ok: true,
    command: 'status',
    root,
    task_id: taskId,
    state_exists: !!state,
    summary_exists: !!summaryText,
    resumable: !!(state && state.next_action),
    state_path: statePath,
    summary_path: summaryPath,
    latest_summary_path: layout.latestSummaryPath,
    status: state ? state.status : null,
    current_phase: state ? state.current_phase : null,
    next_action: state ? state.next_action : null,
    updated_at: state ? state.updated_at : null,
  });
}

function commandEnsure(args) {
  const root = resolveRoot(args);
  const layout = resolveLayout(root);
  ensureDirs(layout);
  const taskId = requireString(args, 'task');
  const sessionId = requireString(args, 'session', `session-${taskId}`);
  const goal = requireString(args, 'goal');
  const existing = readJsonIfExists(taskStatePath(layout, taskId));
  const state = existing || defaultState({
    taskId,
    sessionId,
    goal,
    status: typeof args.status === 'string' ? args.status : 'idle',
    phase: typeof args.phase === 'string' ? args.phase : 'initial',
    nextAction: typeof args['next-action'] === 'string' ? args['next-action'] : 'START',
  });
  const summaryText = summarizeState(state);
  const written = writeStateArtifacts(layout, state, summaryText, [], existing ? 'ensure-noop' : 'ensure', existing ? 'state already existed' : 'initial durable state created');
  writeJson({ ok: true, command: 'ensure', created: !existing, root, task_id: taskId, ...written });
}

function commandCheckpoint(args) {
  const root = resolveRoot(args);
  const layout = resolveLayout(root);
  const taskId = requireString(args, 'task');
  const pressure = parsePressure(args);
  const threshold = criticalThreshold(args);
  const baseState = loadState(layout, taskId);
  const patch = args['patch-json'] ? JSON.parse(args['patch-json']) : {};
  const state = mergeState(baseState, patch);
  if (pressure !== null) {
    state.adapter_pressure = pressure;
  }
  const filesTouched = asArray(args.file);
  const constraints = asArray(args.constraint);
  const issues = asArray(args.issue);
  const completedSteps = asArray(args['completed-step']);
  const decisionJson = asArray(args['decision-json']).map((value) => JSON.parse(value));
  const artifactValues = normalizeArtifacts(asArray(args['artifact-json']).concat(asArray(args.artifact)));
  if (constraints.length) state.constraints = constraints;
  if (issues.length) state.open_issues = issues;
  if (completedSteps.length) state.completed_steps = completedSteps;
  if (decisionJson.length) state.decisions = decisionJson;
  if (artifactValues.length) state.artifacts = artifactValues;
  if (typeof args['next-action'] === 'string') state.next_action = args['next-action'];
  if (typeof args.phase === 'string') state.current_phase = args.phase;
  if (typeof args.status === 'string') state.status = args.status;
  if (typeof args['state-confidence'] === 'string') state.state_confidence = Number(args['state-confidence']);
  if (typeof args['last-action-summary'] === 'string') {
    state.last_action = {
      timestamp: isoNow(),
      type: typeof args['last-action-type'] === 'string' ? args['last-action-type'] : 'adapter',
      summary: args['last-action-summary'],
      outcome: typeof args['last-action-outcome'] === 'string' ? args['last-action-outcome'] : 'success',
    };
  }
  const critical = pressure !== null && pressure >= threshold;
  if (critical) {
    state.status = 'halted';
    state.open_issues = Array.from(new Set([...(state.open_issues || []), 'critical context pressure']));
  }
  const summaryText = summarizeState(state);
  const eventSummary = typeof args['event-summary'] === 'string'
    ? args['event-summary']
    : (critical ? 'checkpoint + halt due to critical pressure' : 'checkpoint persisted');
  const written = writeStateArtifacts(layout, state, summaryText, filesTouched, critical ? 'halt' : 'checkpoint', eventSummary);
  writeJson({ ok: true, command: 'checkpoint', critical, pressure, threshold, root, task_id: taskId, ...written });
}

function commandBundle(args) {
  const root = resolveRoot(args);
  const layout = resolveLayout(root);
  const taskId = requireString(args, 'task');
  const state = loadState(layout, taskId);
  const summaryText = readTextIfExists(taskSummaryPath(layout, taskId)) || readTextIfExists(layout.latestSummaryPath) || '';
  const artifactPaths = state.artifacts ? state.artifacts.map((item) => item.path).filter(Boolean) : [];
  const explicitFiles = asArray(args.file);
  const combined = Array.from(new Set([...artifactPaths, ...explicitFiles]));
  const bundle = buildBundle({
    systemInstructions: typeof args['system-instructions'] === 'string' ? args['system-instructions'] : '',
    state,
    summary: summaryText,
    filePaths: combined,
  });
  if (args.json) {
    writeJson({ ok: true, command: 'bundle', task_id: taskId, root, bundle, files: combined });
    return;
  }
  process.stdout.write(`${bundle}\n`);
}

function commandHalt(args) {
  const root = resolveRoot(args);
  const layout = resolveLayout(root);
  const taskId = requireString(args, 'task');
  const state = loadState(layout, taskId);
  const reason = requireString(args, 'reason');
  state.status = 'halted';
  state.updated_at = isoNow();
  state.open_issues = Array.from(new Set([...(state.open_issues || []), reason]));
  if (typeof args['next-action'] === 'string') state.next_action = args['next-action'];
  state.last_action = {
    timestamp: isoNow(),
    type: 'halt',
    summary: reason,
    outcome: 'halted',
  };
  const summaryText = summarizeState(state);
  const written = writeStateArtifacts(layout, state, summaryText, asArray(args.file), 'halt', reason);
  writeJson({ ok: true, command: 'halt', root, task_id: taskId, reason, ...written });
}

function commandResume(args) {
  const root = resolveRoot(args);
  const layout = resolveLayout(root);
  const taskId = requireString(args, 'task');
  const state = loadState(layout, taskId);
  const summaryText = readTextIfExists(taskSummaryPath(layout, taskId)) || readTextIfExists(layout.latestSummaryPath) || '';
  writeJson({
    ok: true,
    command: 'resume',
    root,
    task_id: taskId,
    next_action: state.next_action,
    status: state.status,
    current_phase: state.current_phase,
    resumable: !!state.next_action,
    state_path: taskStatePath(layout, taskId),
    summary_path: taskSummaryPath(layout, taskId),
    summary: summaryText,
    state,
  });
}

function printHelp() {
  const text = `Context Guardian Adapter CLI\n\nCommands:\n  status --root <path> --task <id>\n  ensure --root <path> --task <id> --session <id> --goal <text> [--next-action <text>]\n  checkpoint --root <path> --task <id> [--patch-json <json>] [--pressure <0..1>] [--file <path>]...\n  bundle --root <path> --task <id> [--system-instructions <text>] [--file <path>]... [--json]\n  halt --root <path> --task <id> --reason <text> [--next-action <text>]\n  resume --root <path> --task <id>\n\nEnvironment:\n  CG_ADAPTER_ROOT or CG_ROOT can provide the storage root.\n`;
  process.stdout.write(text);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  if (!command || command === 'help' || args.help) {
    printHelp();
    return;
  }
  switch (command) {
    case 'status':
      commandStatus(args);
      return;
    case 'ensure':
      commandEnsure(args);
      return;
    case 'checkpoint':
      commandCheckpoint(args);
      return;
    case 'bundle':
      commandBundle(args);
      return;
    case 'halt':
      commandHalt(args);
      return;
    case 'resume':
      commandResume(args);
      return;
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}

try {
  main();
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
}
