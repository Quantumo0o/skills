/**
 * singularity-forum - Personality State Machine + Config Drift（对标 evolver）
 *
 * 持续跟踪进化状态：
 * - iterations / steady_state_cycles
 * - stagnation_threshold 连续 N 次无新 Gene = 停滞
 * - 停滞时自动调整策略
 * - 配置变更检测
 */
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PERSONALITY_FILE = path.join(os.homedir(), '.cache', 'singularity-forum', 'personality.json');
const CONFIG_BASELINE_FILE = path.join(os.homedir(), '.cache', 'singularity-forum', 'config-baseline.json');

export const DEFAULT_PERSONALITY = {
  iterations: 0,
  steady_state_cycles: 0,      // 连续无新 Gene 次数
  stagnation_signals: [],
  stagnation_threshold: 3,       // 连续3次无新 Gene = 停滞
  stagnation_detected: false,
  stagnation_count: 0,
  current_recommendation: null,  // 'innovate' | 'harden' | 'repair_only'
  last_recommendation_change: null,
  last_iteration_at: null,
  average_candidates_per_run: 0,
  total_genes_published: 0,
  total_genes_rejected: 0,
  total_skipped: 0,
  error_rate: 0,
  created_at: new Date().toISOString(),
};

// =============================================================================
// Personality 读写
// =============================================================================

function loadPersonality() {
  if (!fs.existsSync(PERSONALITY_FILE)) return { ...DEFAULT_PERSONALITY };
  try { return { ...DEFAULT_PERSONALITY, ...JSON.parse(fs.readFileSync(PERSONALITY_FILE, 'utf-8')) }; }
  catch { return { ...DEFAULT_PERSONALITY }; }
}

function savePersonality(p) {
  const dir = path.dirname(PERSONALITY_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(PERSONALITY_FILE, JSON.stringify(p, null, 2), 'utf-8');
}

// =============================================================================
// 配置基线
// =============================================================================

export function snapshotConfig() {
  const configPaths = [
    path.join(os.homedir(), '.openclaw', 'openclaw.json'),
    path.join(os.homedir(), '.config', 'singularity-forum', 'credentials.json'),
    path.join(os.homedir(), '.openclaw', 'workspace', 'AGENTS.md'),
  ];
  const snapshot = {};
  for (const fp of configPaths) {
    if (fs.existsSync(fp)) {
      try {
        const raw = fs.readFileSync(fp, 'utf-8');
        snapshot[fp] = hashString(raw);
      } catch {}
    }
  }
  const dir = path.dirname(CONFIG_BASELINE_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CONFIG_BASELINE_FILE, JSON.stringify(snapshot, null, 2), 'utf-8');
  return snapshot;
}

export function detectConfigDrift() {
  const baseline = loadConfigBaseline();
  if (!baseline) return { drifted: false };

  const configPaths = Object.keys(baseline);
  const drifts = [];

  for (const fp of configPaths) {
    if (!fs.existsSync(fp)) {
      drifts.push({ path: fp, type: 'deleted' });
      continue;
    }
    try {
      const raw = fs.readFileSync(fp, 'utf-8');
      const hash = hashString(raw);
      if (hash !== baseline[fp]) {
        drifts.push({ path: fp.replace(os.homedir(), '~'), type: 'changed', before: baseline[fp].slice(0, 8), after: hash.slice(0, 8) });
      }
    } catch {}
  }

  return { drifted: drifts.length > 0, changes: drifts };
}

function loadConfigBaseline() {
  if (!fs.existsSync(CONFIG_BASELINE_FILE)) return null;
  try { return JSON.parse(fs.readFileSync(CONFIG_BASELINE_FILE, 'utf-8')); } catch { return null; }
}

// =============================================================================
// 状态机更新
// =============================================================================

/**
 * 每轮进化结束后调用，更新 personality 状态
 */
export function updatePersonality({ published = 0, candidates = 0, skipped = 0, rejected = 0, newSignals = [] }) {
  const p = loadPersonality();

  p.iterations += 1;
  p.last_iteration_at = new Date().toISOString();
  p.total_genes_published += published;
  p.total_skipped += skipped;
  p.total_genes_rejected += rejected;

  // 更新移动平均
  const n = p.iterations;
  p.average_candidates_per_run = (p.average_candidates_per_run * (n - 1) + candidates) / n;
  p.error_rate = p.total_genes_rejected / Math.max(n, 1);

  // 停滞检测
  if (published === 0 && candidates === 0) {
    p.steady_state_cycles += 1;
    p.stagnation_count += 1;
  } else {
    p.steady_state_cycles = 0;
    p.stagnation_count = 0;
  }

  // 停滞判定
  if (p.stagnation_count >= p.stagnation_threshold && !p.stagnation_detected) {
    p.stagnation_detected = true;
    const rec = recommendFromStagnation(p);
    p.current_recommendation = rec;
    p.last_recommendation_change = new Date().toISOString();
    p.stagnation_signals = newSignals.slice(0, 5);
  }

  // 新信号时重置停滞
  if (newSignals.length > 0 && p.stagnation_detected) {
    p.stagnation_detected = false;
    p.stagnation_count = 0;
  }

  savePersonality(p);
  return p;
}

function recommendFromStagnation(p) {
  // 根据历史数据决定下一步策略
  if (p.error_rate > 0.3) return 'repair_only';
  if (p.average_candidates_per_run < 0.5) return 'innovate';
  if (p.current_recommendation === 'harden') return 'innovate';
  return 'harden';
}

/**
 * 获取当前推荐策略（供进化引擎调用）
 */
export function getRecommendedStrategy(p = null) {
  const personality = p || loadPersonality();
  if (personality.stagnation_detected) {
    return {
      strategy: personality.current_recommendation || 'harden',
      reason: 'stagnation_detected',
      stagnationCount: personality.stagnation_count,
    };
  }
  if (personality.average_candidates_per_run < 1 && personality.iterations > 5) {
    return { strategy: 'innovate', reason: 'low_candidate_rate' };
  }
  return { strategy: 'balanced', reason: 'normal_operation' };
}

export function getPersonality() {
  return loadPersonality();
}

/**
 * 重置 personality（debug 用）
 */
export function resetPersonality() {
  savePersonality({ ...DEFAULT_PERSONALITY });
}

// =============================================================================
// 工具函数
// =============================================================================

function hashString(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) + str.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash).toString(16);
}
