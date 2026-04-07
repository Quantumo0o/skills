/**
 * singularity-forum - 自进化模块 v1.2.0
 * 分析运行历史，主动发现问题并发布 Gene 到 EvoMap
 *
 * 相比 v1.1.0 新增：
 * - GitOps 版本控制 + stash/rollback
 * - 完整 A2A 协议（hello/heartbeat/fetch/publish/review/report）
 * - MemoryGraph 知识图谱集成
 * - LLM Review 二次验证
 * - 负载感知自动退让
 * - Review 模式（人类确认）
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';
import {
  loadCredentials,
  log,
  loadSyncState,
  saveSyncState,
} from '../lib/api.js';
import { publishGene, fetchGene } from '../lib/api.js';
import type { EvolutionGene } from '../lib/types.js';

// 新增模块
import * as GitOps from './gep/gitops.js';
import * as A2A from './gep/a2aProtocol.js';
import * as MemoryGraph from './gep/memoryGraph.js';
import { reviewGene, needsReview } from './gep/llmReview.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// =============================================================================
// 错误模式识别（保留原有 8 个，新增更多）
// =============================================================================

interface ErrorPattern {
  signal: string;
  taskType: string;
  description: string;
  strategy: {
    steps: string[];
    algorithm?: string;
    execMode: 'PROMPT' | 'CODE' | 'WORKFLOW';
  };
  category: 'REPAIR' | 'OPTIMIZE' | 'INNOVATE';
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
}

function extractErrorPatterns(text: string): ErrorPattern[] {
  const patterns: ErrorPattern[] = [];

  if (/timeout|超时|timed?out|ETIMEDOUT|ECONNRESET/i.test(text)) {
    patterns.push({
      signal: 'network_timeout',
      taskType: 'NETWORK_REQUEST',
      description: '网络请求超时，使用指数退避重试',
      strategy: {
        steps: ['检测超时错误', '计算退避时间（base*2^attempt）', '重试请求', '超限后降级'],
        algorithm: 'exponential_backoff',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'HIGH',
    });
  }

  if (/json.*parse|JSON.*error|SyntaxError|Unexpected token/i.test(text)) {
    patterns.push({
      signal: 'json_parse_error',
      taskType: 'DATA_PARSING',
      description: 'JSON 解析失败，尝试容错处理',
      strategy: {
        steps: ['捕获解析异常', '尝试宽松解析', '记录原始内容', '降级返回空数据'],
        algorithm: 'try_catch_json',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'MEDIUM',
    });
  }

  if (/401|Unauthorized|unauthorized|token.*invalid|token.*expired/i.test(text)) {
    patterns.push({
      signal: 'auth_failure',
      taskType: 'API_REQUEST',
      description: '认证失败，刷新 Token 或提示重新配置',
      strategy: {
        steps: ['检测 401 响应', '清除缓存的 Token', '重试请求一次', '失败后报告认证错误'],
        algorithm: 'auth_retry_once',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'HIGH',
    });
  }

  if (/429|rate.?limit|too many requests|RateLimit/i.test(text)) {
    patterns.push({
      signal: 'rate_limit',
      taskType: 'API_REQUEST',
      description: '触发速率限制，等待冷却后重试',
      strategy: {
        steps: ['检测 429 响应', '读取 Retry-After 头', '等待冷却时间', '重试请求'],
        algorithm: 'rate_limit_backoff',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'MEDIUM',
    });
  }

  if (/Cannot find module|ERR_MODULE_NOT_FOUND|import.*failed/i.test(text)) {
    patterns.push({
      signal: 'module_not_found',
      taskType: 'CODE_EXECUTION',
      description: '模块未找到，建议使用 require() 而非 import 或检查路径',
      strategy: {
        steps: ['捕获模块加载异常', '检查模块名称拼写', '尝试相对路径', '降级到内联实现'],
        algorithm: 'module_fallback',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'HIGH',
    });
  }

  if (/ENOENT|no such file|not found|does not exist/i.test(text)) {
    patterns.push({
      signal: 'file_not_found',
      taskType: 'FILE_SYSTEM',
      description: '文件不存在，提供清晰的错误提示',
      strategy: {
        steps: ['检查文件路径是否存在', '尝试常见路径变体', '返回友好错误信息', '记录缺失文件路径'],
        algorithm: 'file_exists_check',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'MEDIUM',
    });
  }

  if (/encoding|UTF-?8|GBK|charset|乱码/i.test(text)) {
    patterns.push({
      signal: 'encoding_error',
      taskType: 'DATA_PROCESSING',
      description: '字符编码问题，强制使用 UTF-8',
      strategy: {
        steps: ['检测编码头', '强制使用 UTF-8 解码', '对中文路径特殊处理', '验证解码结果'],
        algorithm: 'force_utf8',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'MEDIUM',
    });
  }

  if (/loop|iteration|重复|多次.*失败/i.test(text)) {
    patterns.push({
      signal: 'repeated_failure',
      taskType: 'TASK_ORCHESTRATION',
      description: '同一任务反复失败，启用熔断器',
      strategy: {
        steps: ['记录失败次数', '超过阈值后熔断', '返回缓存结果或空数据', '通知人工介入'],
        algorithm: 'circuit_breaker',
        execMode: 'WORKFLOW',
      },
      category: 'OPTIMIZE',
      severity: 'MEDIUM',
    });
  }

  // 新增模式
  if (/heap|out of memory|OOM|Memory.*exhaust/i.test(text)) {
    patterns.push({
      signal: 'memory_exhaustion',
      taskType: 'RESOURCE_MANAGEMENT',
      description: '内存耗尽，使用流式处理或分批处理',
      strategy: {
        steps: ['监控内存使用', '单次处理量降低', '及时释放引用', '使用流替代全量加载'],
        algorithm: 'streaming_chunked',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'HIGH',
    });
  }

  if (/permission denied|EPERM|access denied|EACCES/i.test(text)) {
    patterns.push({
      signal: 'permission_error',
      taskType: 'FILE_SYSTEM',
      description: '权限不足，降级或请求管理员权限',
      strategy: {
        steps: ['检查文件权限', '尝试降级到用户目录', '记录权限错误', '提示配置路径'],
        algorithm: 'permission_fallback',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'HIGH',
    });
  }

  if (/disk full|ENOSPC|no space/i.test(text)) {
    patterns.push({
      signal: 'disk_full',
      taskType: 'RESOURCE_MANAGEMENT',
      description: '磁盘空间不足，清理缓存或报错',
      strategy: {
        steps: ['检查磁盘剩余空间', '清理临时文件', '清理过期缓存', '返回友好错误'],
        algorithm: 'disk_cleanup',
        execMode: 'CODE',
      },
      category: 'REPAIR',
      severity: 'HIGH',
    });
  }

  return patterns;
}

// =============================================================================
// 上下文收集
// =============================================================================

interface RuntimeContext {
  memoryFiles: Array<{ path: string; content: string; mtime: Date }>;
  skillLogs: Array<{ path: string; content: string }>;
  recentErrors: string[];
  sessionLogs: string[];
}

function collectContext(days = 3): RuntimeContext {
  const home = os.homedir();
  const workspace = path.join(home, '.openclaw', 'workspace');
  const memoryDir = path.join(workspace, 'memory');
  const cacheDir = path.join(home, '.cache', 'singularity-forum');
  const now = Date.now();
  const cutoff = now - days * 24 * 60 * 60 * 1000;

  const context: RuntimeContext = {
    memoryFiles: [],
    skillLogs: [],
    recentErrors: [],
    sessionLogs: [],
  };

  if (fs.existsSync(memoryDir)) {
    for (const file of fs.readdirSync(memoryDir)) {
      if (!file.endsWith('.md') && !file.endsWith('.json')) continue;
      const fp = path.join(memoryDir, file);
      try {
        const stat = fs.statSync(fp);
        if (stat.mtimeMs > cutoff) {
          const content = fs.readFileSync(fp, 'utf-8');
          context.memoryFiles.push({ path: fp, content, mtime: stat.mtime });
        }
      } catch { /* skip */ }
    }
  }

  if (fs.existsSync(cacheDir)) {
    const logFile = path.join(cacheDir, 'skill.log');
    if (fs.existsSync(logFile)) {
      try {
        const content = fs.readFileSync(logFile, 'utf-8');
        context.skillLogs.push({ path: logFile, content });
        for (const line of content.split('\n')) {
          if (!line) continue;
          try {
            const entry = JSON.parse(line);
            if (entry.level === 'ERROR') {
              context.recentErrors.push(entry.message);
            }
          } catch { /* skip */ }
        }
      } catch { /* skip */ }
    }
  }

  const sessionsDir = path.join(home, '.openclaw', 'sessions');
  if (fs.existsSync(sessionsDir)) {
    for (const dir of fs.readdirSync(sessionsDir)) {
      const transcript = path.join(sessionsDir, dir, 'transcript.jsonl');
      if (fs.existsSync(transcript)) {
        try {
          const stat = fs.statSync(transcript);
          if (stat.mtimeMs > cutoff) {
            const lines = fs.readFileSync(transcript, 'utf-8')
              .split('\n')
              .filter(l => l.trim())
              .slice(-100);
            context.sessionLogs.push(...lines);
          }
        } catch { /* skip */ }
      }
    }
  }

  return context;
}

function flattenContext(ctx: RuntimeContext): string {
  const parts: string[] = [];
  for (const f of ctx.memoryFiles) parts.push(`[${f.path}]\n${f.content}`);
  for (const l of ctx.skillLogs) parts.push(`[${l.path}]\n${l.content}`);
  return parts.join('\n\n');
}

// =============================================================================
// Gene 生成器
// =============================================================================

interface GeneCandidate {
  signal: string;
  taskType: string;
  displayName: string;
  description: string;
  category: 'OPTIMIZE' | 'REPAIR' | 'INNOVATE';
  strategy: {
    steps: string[];
    algorithm?: string;
    execMode: 'PROMPT' | 'CODE' | 'WORKFLOW';
    gdiScore?: number;
  };
  confidence: number;
  usageCount: number;
  signals: string[];
  alreadyExists: boolean;
}

function analyzeAndGenerateGenes(ctx: RuntimeContext): GeneCandidate[] {
  const text = flattenContext(ctx);
  const patterns = extractErrorPatterns(text);
  const candidates: GeneCandidate[] = [];

  for (const p of patterns) {
    candidates.push({
      signal: p.signal,
      taskType: p.taskType,
      displayName: signalToDisplayName(p.signal),
      description: p.description,
      category: p.category,
      strategy: {
        steps: p.strategy.steps,
        algorithm: p.strategy.algorithm,
        execMode: p.strategy.execMode,
        gdiScore: severityToGdi(p.severity),
      },
      confidence: severityToConfidence(p.severity),
      usageCount: 0,
      signals: [p.signal],
      alreadyExists: false,
    });
  }

  return candidates;
}

function signalToDisplayName(signal: string): string {
  const map: Record<string, string> = {
    network_timeout: '网络超时指数退避策略',
    json_parse_error: 'JSON 容错解析策略',
    auth_failure: '认证失败重试策略',
    rate_limit: '速率限制冷却策略',
    module_not_found: '模块加载失败降级策略',
    file_not_found: '文件不存在处理策略',
    encoding_error: '字符编码强制 UTF-8 策略',
    repeated_failure: '重复失败熔断器策略',
    memory_exhaustion: '内存耗尽流式处理策略',
    permission_error: '权限不足降级策略',
    disk_full: '磁盘空间不足清理策略',
  };
  return map[signal] || signal.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function severityToGdi(s: 'HIGH' | 'MEDIUM' | 'LOW'): number {
  return { HIGH: 80, MEDIUM: 65, LOW: 55 }[s];
}

function severityToConfidence(s: 'HIGH' | 'MEDIUM' | 'LOW'): number {
  return { HIGH: 85, MEDIUM: 65, LOW: 45 }[s];
}

// =============================================================================
// 负载感知
// =============================================================================

function getLoadAvg(): number {
  try {
    // Windows 上 os.loadavg() 返回 [0,0,0]，用系统调用替代
    if (process.platform === 'win32') {
      const out = require('child_process').execSync(
        'powershell -Command "Get-Counter \'\\Processor(_Total)\\% Processor Time\' -SampleInterval 1 -MaxSamples 1 | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue"',
        { encoding: 'utf-8', timeout: 5000, windowsHide: true }
      ).trim();
      return parseFloat(out) / 100; // 转换为 0-1
    }
    const [m1] = os.loadavg();
    return m1 / os.cpus().length;
  } catch {
    return 0;
  }
}

function shouldBackoff(): boolean {
  const maxLoad = parseFloat(process.env.EVOLVE_LOAD_MAX || '2.0');
  return getLoadAvg() > maxLoad;
}

// =============================================================================
// GitOps 集成
// =============================================================================

async function gitStash(): Promise<GitOps.StashResult> {
  try {
    return GitOps.stash('evolver-auto-stash-' + Date.now());
  } catch (e) {
    return { success: false, message: String(e) };
  }
}

async function gitRollback(mode: GitOps.RollbackMode = 'hard'): Promise<GitOps.RollbackResult> {
  try {
    return GitOps.rollback(mode);
  } catch (e) {
    return { success: false, mode, message: String(e) };
  }
}

// =============================================================================
// A2A 协议集成
// =============================================================================

async function a2aHeartbeat(): Promise<void> {
  try {
    const result = await A2A.helloAndHeartbeat();
    if (result.success) {
      log('INFO', 'evolver', `A2A heartbeat OK: ${result.timestamp}`);
    } else {
      log('WARN', 'evolver', `A2A heartbeat failed: ${result.message}`);
    }
  } catch (e) {
    log('WARN', 'evolver', `A2A heartbeat error: ${e instanceof Error ? e.message : String(e)}`);
  }
}

async function a2aFetchCapsules(): Promise<void> {
  try {
    const result = await A2A.fetchAssets({
      asset_type: 'Capsule',
      signals: [],
      limit: 3,
    });
    if (result.success && result.assets.length > 0) {
      log('INFO', 'evolver', `Fetched ${result.assets.length} capsules from Hub`);
    }
  } catch (e) {
    log('WARN', 'evolver', `A2A fetch failed: ${e instanceof Error ? e.message : String(e)}`);
  }
}

// =============================================================================
// MemoryGraph 集成
// =============================================================================

function recordErrorInGraph(signal: string, description: string, taskType: string): void {
  try {
    const node = MemoryGraph.recordError(signal, description, taskType);
    log('INFO', 'evolver', `Recorded error in graph: ${signal} (node=${node.id})`);
  } catch (e) {
    log('WARN', 'evolver', `Failed to record in graph: ${e instanceof Error ? e.message : String(e)}`);
  }
}

// =============================================================================
// 检查 Gene 是否已存在
// =============================================================================

async function checkGeneExists(signal: string, apiKey: string): Promise<boolean> {
  try {
    const { fetchGenes } = await import('../lib/api.js');
    const resp = await fetchGenes(apiKey, { limit: 50 });
    return resp.genes.some(g => g.signals?.includes(signal));
  } catch {
    return false;
  }
}

// =============================================================================
// 发布 Gene（含 LLM Review）
// =============================================================================

async function publishCandidate(
  candidate: GeneCandidate,
  apiKey: string,
  agentId: string,
  reviewMode: boolean
): Promise<{ success: boolean; geneId?: string; error?: string; skipped?: boolean }> {
  // 1. LLM Review
  if (needsReview() && !reviewMode) {
    const review = await reviewGene({
      name: candidate.signal,
      displayName: candidate.displayName,
      description: candidate.description,
      taskType: candidate.taskType,
      category: candidate.category,
      signals: candidate.signals,
      strategy: candidate.strategy,
      confidence: candidate.confidence,
      gdiScore: candidate.strategy.gdiScore || 70,
    });

    if (!review.approved) {
      log('WARN', 'evolver', `LLM Review rejected ${candidate.displayName} (score=${review.score.toFixed(2)}): ${review.safetyIssues?.join('; ')}`);
      writeEvolutionEvent('gene_rejected', candidate.displayName, {
        signal: candidate.signal,
        reviewScore: review.score,
        safetyIssues: review.safetyIssues,
      });
      return { success: false, skipped: true, error: `LLM Review rejected (score=${review.score.toFixed(2)})` };
    }
    log('INFO', 'evolver', `LLM Review approved ${candidate.displayName} (score=${review.score.toFixed(2)})`);
  }

  // 2. 发布
  try {
    const result = await publishGene(apiKey, {
      name: candidate.signal,
      displayName: candidate.displayName,
      description: candidate.description,
      taskType: candidate.taskType,
      category: candidate.category,
      signals: candidate.signals,
      execMode: candidate.strategy.execMode,
      strategy: {
        description: candidate.description,
        steps: candidate.strategy.steps,
        algorithm: candidate.strategy.algorithm,
      },
      gdiScore: candidate.strategy.gdiScore || 70,
      confidence: candidate.confidence,
      usageCount: 0,
      sourceAgentId: agentId,
      version: '1.0.0',
    });

    log('INFO', 'evolver', `Published Gene: ${candidate.displayName}`);

    // 3. 上报 A2A Hub
    await A2A.publishGeneToHub({
      name: candidate.signal,
      displayName: candidate.displayName,
      description: candidate.description,
      taskType: candidate.taskType,
      signals: candidate.signals,
      category: candidate.category,
      confidence: candidate.confidence,
      strategy: candidate.strategy as Record<string, unknown>,
    });

    return { success: true, geneId: result.id };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    log('ERROR', 'evolver', `Publish failed: ${candidate.displayName} - ${msg}`);
    return { success: false, error: msg };
  }
}

// =============================================================================
// EvolutionEvent 本地日志
// =============================================================================

function writeEvolutionEvent(
  type: 'gene_created' | 'gene_published' | 'gene_rejected' | 'analysis_run' | 'no_candidates' | 'rollback',
  geneName: string,
  details: Record<string, unknown>
): void {
  const cacheDir = path.join(os.homedir(), '.cache', 'singularity-forum');
  if (!fs.existsSync(cacheDir)) fs.mkdirSync(cacheDir, { recursive: true });

  const eventFile = path.join(cacheDir, 'evolution-events.jsonl');
  const event = {
    timestamp: new Date().toISOString(),
    type,
    geneName,
    agentId: 'singularity-forum-evolver-v1.2',
    ...details,
  };

  fs.appendFileSync(eventFile, JSON.stringify(event) + '\n', 'utf-8');
}

// =============================================================================
// Review 模式：打印变更，等待确认
// =============================================================================

function printReviewSummary(
  ctx: RuntimeContext,
  candidates: GeneCandidate[],
  health: GitOps.HealthCheck
): void {
  console.log('\n========== EVOLUTION REVIEW ==========\n');
  console.log(`Analyzed files: ${ctx.memoryFiles.length}`);
  console.log(`Errors found: ${ctx.recentErrors.length}`);
  console.log(`New gene candidates: ${candidates.length}\n`);

  if (candidates.length > 0) {
    console.log('--- Candidates ---');
    for (const c of candidates) {
      console.log(`  [${c.category}] ${c.displayName} (GDI=${c.strategy.gdiScore}, confidence=${c.confidence}%)`);
      console.log(`    Signal: ${c.signals.join(', ')}`);
      console.log(`    Steps: ${c.strategy.steps.join(' -> ')}`);
      if (c.strategy.algorithm) console.log(`    Algorithm: ${c.strategy.algorithm}`);
      console.log();
    }
  }

  console.log('--- Git Status ---');
  console.log(`  Clean: ${health.pass ? 'YES' : 'NO (will stash)'}`);
  if (health.warnings.length > 0) {
    console.log(`  Warnings: ${health.warnings.join('; ')}`);
  }

  console.log('\n======================================');
  console.log('To proceed: node src/evolver.js --review --force');
  console.log('======================================\n');
}

// =============================================================================
// 主进化循环
// =============================================================================

export interface EvolveResult {
  analyzed: number;
  candidates: number;
  published: number;
  skipped: number;
  errors: string[];
  duration: number;
  loadBackedOff?: boolean;
  rollbackTriggered?: boolean;
}

export async function runEvolutionCycle(
  days = 3,
  forcePublish = false,
  reviewMode = false
): Promise<EvolveResult> {
  const start = Date.now();
  const errors: string[] = [];
  const startIso = new Date().toISOString();

  // 0. 前置检查
  let cred;
  try {
    cred = loadCredentials();
  } catch {
    return { analyzed: 0, candidates: 0, published: 0, skipped: 0, errors: ['Credentials not configured'], duration: Date.now() - start };
  }

  // 0b. 负载感知
  if (shouldBackoff()) {
    log('WARN', 'evolver', 'Load too high, backing off');
    return { analyzed: 0, candidates: 0, published: 0, skipped: 0, errors: [], duration: Date.now() - start, loadBackedOff: true };
  }

  // 0c. Git 健康检查
  const health = GitOps.healthCheck();
  log('INFO', 'evolver', `Git health: ${health.pass ? 'PASS' : 'FAIL'} | clean=${health.clean} | warnings=${health.warnings.length}`);

  log('INFO', 'evolver', `Evolution starting (days=${days}, review=${reviewMode}, force=${forcePublish})`);

  // 1. A2A 心跳
  await a2aHeartbeat();

  // 2. 收集上下文
  const ctx = collectContext(days);
  log('INFO', 'evolver', `Context: ${ctx.memoryFiles.length} memory files, ${ctx.recentErrors.length} errors`);

  // 3. 分析并生成候选
  const candidates = analyzeAndGenerateGenes(ctx);
  log('INFO', 'evolver', `Found ${candidates.length} candidates`);

  // 4. Review 模式：打印摘要，等用户确认
  if (reviewMode && !forcePublish) {
    printReviewSummary(ctx, candidates, health);
    return { analyzed: ctx.memoryFiles.length, candidates: candidates.length, published: 0, skipped: 0, errors: [], duration: Date.now() - start };
  }

  if (candidates.length === 0) {
    writeEvolutionEvent('no_candidates', '', { analyzedFiles: ctx.memoryFiles.length });
    log('INFO', 'evolver', 'No candidates, skipping');
    return { analyzed: ctx.memoryFiles.length, candidates: 0, published: 0, skipped: 0, errors: [], duration: Date.now() - start };
  }

  // 5. 检查重复
  const uniqueCandidates: GeneCandidate[] = [];
  for (const c of candidates) {
    const exists = await checkGeneExists(c.signal, cred.forum_api_key);
    c.alreadyExists = exists;
    if (!exists) uniqueCandidates.push(c);
  }
  log('INFO', 'evolver', `Deduplicated: ${uniqueCandidates.length} new, ${candidates.length - uniqueCandidates.length} already exist`);

  // 6. GitOps: 暂存现有改动
  let stashed = false;
  if (!health.clean) {
    const stashResult = await gitStash();
    stashed = stashResult.success;
    log('INFO', 'evolver', `Git stash: ${stashResult.message}`);
  }

  // 7. 发布
  let published = 0;
  let skipped = 0;
  const rollbackMode = (process.env.EVOLVER_ROLLBACK_MODE || 'hard') as GitOps.RollbackMode;

  for (const c of uniqueCandidates) {
    // 跳过低 GDI
    if (!forcePublish && c.strategy.gdiScore && c.strategy.gdiScore < 65) {
      log('INFO', 'evolver', `Skipping low-GDI gene: ${c.displayName} (${c.strategy.gdiScore})`);
      skipped++;
      continue;
    }

    const result = await publishCandidate(c, cred.forum_api_key, cred.openclaw_agent_id, reviewMode);

    if (result.success) {
      published++;
      // 记录到 MemoryGraph
      recordErrorInGraph(c.signal, c.description, c.taskType);
      writeEvolutionEvent('gene_published', c.displayName, {
        geneId: result.geneId,
        signal: c.signal,
        gdiScore: c.strategy.gdiScore,
      });
    } else if (result.skipped) {
      skipped++;
    } else {
      errors.push(`${c.displayName}: ${result.error}`);
      writeEvolutionEvent('gene_created', c.displayName, { error: result.error });
    }
  }

  // 8. 回滚（如需要）
  if (stashed && errors.length > 0 && rollbackMode !== 'none') {
    const rb = await gitRollback(rollbackMode);
    log('INFO', 'evolver', `Rollback: ${rb.message}`);
    writeEvolutionEvent('rollback', '', { mode: rollbackMode, message: rb.message });
  }

  writeEvolutionEvent('analysis_run', '', {
    candidates: uniqueCandidates.length,
    published,
    skipped,
    duration: Date.now() - start,
  });

  const duration = Date.now() - start;
  log('INFO', 'evolver', `Done: ${published} published, ${skipped} skipped, ${errors.length} errors in ${duration}ms`);

  return {
    analyzed: ctx.memoryFiles.length,
    candidates: uniqueCandidates.length,
    published,
    skipped,
    errors,
    duration,
    rollbackTriggered: stashed && errors.length > 0,
  };
}

// =============================================================================
// CLI
// =============================================================================

const args = process.argv.slice(2);
const daysArg = args.find(a => a.startsWith('--days='));
const forceArg = args.includes('--force');
const reviewArg = args.includes('--review');
const days = daysArg ? parseInt(daysArg.split('=')[1]) : 3;

runEvolutionCycle(days, forceArg, reviewArg)
  .then(result => {
    console.log('\n=== Evolution Result ===');
    console.log(`Analyzed: ${result.analyzed}`);
    console.log(`Candidates: ${result.candidates}`);
    console.log(`Published: ${result.published}`);
    console.log(`Skipped: ${result.skipped}`);
    if (result.loadBackedOff) console.log('(Load backoff triggered)');
    if (result.rollbackTriggered) console.log('(Rollback triggered)');
    if (result.errors.length > 0) {
      console.log('Errors:', result.errors.join(', '));
    }
    console.log(`Duration: ${result.duration}ms`);
    process.exit(result.errors.length > 0 ? 1 : 0);
  })
  .catch(err => {
    console.error('Fatal:', err instanceof Error ? err.message : String(err));
    process.exit(1);
  });
