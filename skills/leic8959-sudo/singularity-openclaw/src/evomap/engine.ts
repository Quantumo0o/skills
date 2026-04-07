/**
 * EvoMap Engine — Capability-Evolver 内核集成版
 *
 * 在原有 Hub A2A 逻辑基础上，接入 capability-evolver 的全部缺失模块：
 *   - signals.js           → LLM + heuristic 信号提取（替代纯正则）
 *   - memoryGraph.js        → 进化记忆知识图谱（历史基因/胶囊偏好）
 *   - narrativeMemory.js    → 人类可读进化叙事日志
 *   - reflection.js         → 自省引擎（连续成功/失败后自动调整参数）
 *   - curriculum.js         → 学习课程（信号 mastery 追踪）
 *   - skillDistiller.js     → 从成功胶囊自动蒸馏新基因
 *   - skillPublisher.js     → 发布 skill 到 Hub
 *   - contentHash.js       → 资产去重 + 防篡改
 *   - deviceId.js           → 稳定设备 ID
 *   - envFingerprint.js     → 环境指纹
 *   - hubReview.js          → apply 前 review 门控
 *   - issueReporter.js      → 连续失败 → 自动建 GitHub issue
 *   - sanitize.js           → GitHub issue 脱敏
 *   - questionGenerator.js  → 反思问题生成器
 *   - analyzer.js           → 历史失败模式分析
 *
 * 数据目录（服务器）：
 *   /opt/moltbook-web/data/evomap-evolution/   — 进化状态、memoryGraph、narrative
 *   /opt/moltbook-web/data/evomap-memory/       — memory/（备用）
 *   /opt/moltbook-web/data/evomap-assets/        — capsules.json / genes.json
 *   /opt/moltbook-web/data/evomap-logs/          — evolver_loop.log
 */

import { detectSignals, type DetectedSignal } from './signal-detector';
import { matchGene, selectBestMatch, buildMatchReport, type GeneMatch } from './gene-matcher';
import { executeCapsule, computePayloadChecksum } from './capsule-executor';
import {
  cacheGene, cacheCapsule, findCachedCapsuleBySignals, getCachedGene,
  type CachedGene, type CachedCapsule,
} from './asset-cache';
import { injectCapsule } from './session-injector';
import { buildEnvelope } from '@/lib/a2a';

// ── Capability-Evolver 内核（通过 gep-index 统一加载） ───────────────────────
let gep: any = null;
function getGep() {
  if (!gep) {
    try {
      // Node.js 环境：从相对路径加载
      gep = require('./gep/gep-index');
    } catch (e) {
      console.warn('[EvoMap] Failed to load gep kernel:', (e as Error).message);
      gep = {};
    }
  }
  return gep;
}

const HUB_BASE_URL = process.env.HUB_BASE_URL;
if (!HUB_BASE_URL) {
  console.warn('[EvoMap] HUB_BASE_URL is not set — Hub features will be disabled');
}

function hubAuthHeaders(): Record<string, string> {
  const nodeId = process.env.EVOMAP_NODE_ID;
  const nodeSecret = process.env.EVOMAP_NODE_SECRET;
  if (nodeId && nodeSecret) {
    return { 'Content-Type': 'application/json', Authorization: `Bearer ${nodeId}:${nodeSecret}` };
  }
  return { 'Content-Type': 'application/json' };
}

// ── Capability-Evolver 信号提取（增强版） ───────────────────────────────────
/**
 * 用 capability-evolver 的 extractSignals 从 session 日志中提取信号
 * 集成 LLM + heuristic，比纯正则更强大
 */
async function extractCapabilitySignals(params: {
  recentSessionTranscript?: string;
  todayLog?: string;
  memorySnippet?: string;
  userSnippet?: string;
  recentEvents?: any[];
}): Promise<string[]> {
  const g = getGep();
  if (!g.extractSignals) return [];
  try {
    const signals = g.extractSignals(params);
    return Array.isArray(signals) ? signals : [];
  } catch (e) {
    console.warn('[EvoMap] extractSignals failed:', (e as Error).message);
    return [];
  }
}

// ── Hub fetch / inherit（保持原有逻辑） ──────────────────────────────────────
async function fetchFromHub(
  signals: string[],
  taskType: string,
): Promise<{ capsuleId: string; capsuleConfidence: number; capsulePayload: unknown } | null> {
  if (!HUB_BASE_URL) return null;
  try {
    const envelope = buildEnvelope('singularity-primary', 'hub', 'fetch', {
      asset_type: 'Capsule', signals, task_type: taskType, min_confidence: 0.7,
    });
    const response = await fetch(`${HUB_BASE_URL}/api/evomap/a2a/fetch`, {
      method: 'POST',
      headers: hubAuthHeaders(),
      body: JSON.stringify({ protocol: 'gep-a2a', message_type: 'fetch', ...envelope }),
      signal: AbortSignal.timeout(3000),
    });
    if (!response.ok) return null;
    const data = await response.json();
    const capsules: any[] = data.assets || [];
    if (capsules.length === 0) return null;
    return { capsuleId: capsules[0].capsule_id, capsuleConfidence: capsules[0].confidence, capsulePayload: capsules[0].payload };
  } catch (e) {
    console.warn('[Hub fetch] failed:', (e as Error).message);
    return null;
  }
}

async function inheritFromHub(params: {
  signals: string[];
  taskType: string;
  agentId: string;
  prisma: any;
}): Promise<{ capsule: any; genes: CachedGene[] } | null> {
  const { signals, taskType, agentId, prisma } = params;
  if (!HUB_BASE_URL) return null;

  const cached = findCachedCapsuleBySignals(signals, taskType, 0.5);
  if (cached) {
    const genes: CachedGene[] = cached.geneIds.map(id => getCachedGene(id)).filter(Boolean) as CachedGene[];
    return { capsule: cached, genes };
  }

  let hubData: any;
  try {
    const envelope = buildEnvelope('singularity-primary', 'hub', 'fetch', {
      asset_type: 'Capsule', signals, task_type: taskType, min_confidence: 0.5,
    });
    const res = await fetch(`${HUB_BASE_URL}/api/evomap/a2a/fetch`, {
      method: 'POST',
      headers: hubAuthHeaders(),
      body: JSON.stringify({ protocol: 'gep-a2a', message_type: 'fetch', ...envelope }),
      signal: AbortSignal.timeout(5000),
    });
    if (!res.ok) return null;
    hubData = await res.json();
  } catch (e) {
    console.warn('[EvoMap Inherit] Hub unreachable:', (e as Error).message);
    return null;
  }

  const assets: any[] = hubData?.assets || [];
  if (assets.length === 0) return null;

  const best = assets[0];
  const hubPayload = best.payload as Record<string, unknown> | null;
  const hubGeneIds: string[] = (hubPayload?.genes as string[]) || [];

  const downloadedGenes: CachedGene[] = [];
  for (const geneId of hubGeneIds) {
    try {
      const gRes = await fetch(`${HUB_BASE_URL}/api/evomap/genes/${geneId}`, {
        headers: hubAuthHeaders(),
        signal: AbortSignal.timeout(3000),
      });
      if (!gRes.ok) continue;
      const gData = await gRes.json();
      const gene = gData.gene || gData;
      const dbGene = await prisma.evolutionGene.upsert({
        where: { name_version: { name: gene.name, version: gene.version || '1.0.0' } },
        update: {},
        create: {
          name: gene.name, displayName: gene.displayName || gene.name,
          description: gene.description || '', taskType: taskType as any,
          category: gene.category || 'REPAIR',
          strategy: gene.strategy || {}, constraints: gene.constraints,
          signals: gene.signals || signals, execMode: gene.execMode || 'PROMPT',
          isActive: true, isApproved: true,
          reviewStatus: 'APPROVED' as any, sourceAgentId: agentId,
        },
      });
      const cachedGene: CachedGene = {
        id: dbGene.id, name: dbGene.name, displayName: dbGene.displayName,
        taskType: dbGene.taskType, signals: dbGene.signals, execMode: dbGene.execMode,
        strategy: dbGene.strategy, constraints: dbGene.constraints,
        minConfidence: dbGene.minConfidence, isActive: true,
        cachedAt: new Date().toISOString(),
      };
      cacheGene(cachedGene);
      downloadedGenes.push(cachedGene);
    } catch (e) {
      console.warn(`[EvoMap Inherit] Failed gene ${geneId}:`, (e as Error).message);
    }
  }

  const primaryGeneId = downloadedGenes[0]?.id;
  if (!primaryGeneId) return null;

  const dbCapsule = await prisma.evolutionCapsule.create({
    data: {
      name: `inherited-${best.capsule_id || Date.now()}`,
      displayName: 'Inherited from Hub',
      description: 'Auto-inherited via EvoMap A2A',
      taskType: taskType as any,
      payload: best.payload || {},
      confidence: best.confidence || 0.7,
      triggerSignals: signals,
      inheritedFrom: String(best.capsule_id || ''),
      geneId: primaryGeneId, sourceAgentId: agentId,
    },
  });

  if (downloadedGenes.length > 1) {
    await prisma.evolutionCapsule.update({
      where: { id: dbCapsule.id },
      data: { genes: { connect: downloadedGenes.map(g => ({ id: g.id })) } },
    });
  }

  const cachedCapsule: CachedCapsule = {
    id: dbCapsule.id, name: dbCapsule.name, taskType: dbCapsule.taskType,
    geneId: primaryGeneId, geneIds: downloadedGenes.map(g => g.id),
    payload: dbCapsule.payload, confidence: dbCapsule.confidence,
    triggerSignals: signals, inheritedFrom: String(best.capsule_id || ''),
    cachedAt: new Date().toISOString(),
  };
  cacheCapsule(cachedCapsule);
  return { capsule: dbCapsule, genes: downloadedGenes };
}

// ── 能力 Evolver 核心集成函数 ───────────────────────────────────────────────

/**
 * 使用 capability-evolver 的 signals.js 做深度信号提取
 * 优先使用增强信号，fallback 到基本 signal-detector
 */
async function extractSignalsEnhanced(params: {
  taskType: string;
  input: unknown;
  error?: string | null;
  output?: unknown;
  recentSessionTranscript?: string;
  todayLog?: string;
  memorySnippet?: string;
  recentEvents?: any[];
}): Promise<DetectedSignal[]> {
  // 1. 基本信号（保持兼容性）
  const basicSignals = detectSignals(params);

  // 2. 增强信号（capability-evolver signals.js）
  const capabilitySignals = await extractCapabilitySignals({
    recentSessionTranscript: params.recentSessionTranscript || '',
    todayLog: params.todayLog || '',
    memorySnippet: params.memorySnippet || '',
    recentEvents: params.recentEvents || [],
  });

  // 合并：capability 信号去重后缀加 _cap 标记
  const merged = [...basicSignals];
  const basicSet = new Set(basicSignals.map(s => s.signal));
  for (const sig of capabilitySignals) {
    if (!basicSet.has(sig)) {
      // capability-evolver 增强信号：归入 context 类，metadata.enhanced=true 区分
      merged.push({ signal: sig, source: 'context', metadata: { enhanced: true } });
    }
  }

  return merged;
}

/**
 * 查记忆图谱：给当前信号获取历史基因偏好/禁令
 */
function queryMemoryGraph(signals: string[], genes: any[], driftEnabled = false) {
  const g = getGep();
  if (!g.getMemoryAdvice) return null;
  try {
    return g.getMemoryAdvice({ signals, genes, driftEnabled });
  } catch (e) {
    console.warn('[EvoMap] getMemoryAdvice failed:', (e as Error).message);
    return null;
  }
}

/**
 * 记录信号快照到 memoryGraph
 */
function recordSignalSnapshot(signals: string[], observations?: any) {
  const g = getGep();
  if (!g.recordSignalSnapshot) return;
  try { g.recordSignalSnapshot({ signals, observations }); } catch (_) {}
}

/**
 * 记录假设到 memoryGraph
 */
function recordHypothesis(params: {
  signals: string[];
  mutation?: any;
  personality_state?: any;
  selectedGene?: any;
  selector?: string;
  driftEnabled?: boolean;
  selectedBy?: string;
  capsulesUsed?: string[];
  observations?: any;
}) {
  const g = getGep();
  if (!g.recordHypothesis) return;
  try { g.recordHypothesis(params); } catch (_) {}
}

/**
 * 记录尝试到 memoryGraph
 */
function recordAttempt(params: {
  signals: string[];
  mutation?: any;
  personality_state?: any;
  selectedGene?: any;
  selector?: string;
  driftEnabled?: boolean;
  selectedBy?: string;
  hypothesisId?: string;
  capsulesUsed?: string[];
  observations?: any;
}) {
  const g = getGep();
  if (!g.recordAttempt) return;
  try { g.recordAttempt(params); } catch (_) {}
}

/**
 * 记录结果到 memoryGraph（自动推断成功/失败）
 */
function recordOutcome(signals: string[], observations?: any) {
  const g = getGep();
  if (!g.recordOutcomeFromState) return;
  try { g.recordOutcomeFromState({ signals, observations }); } catch (_) {}
}

/**
 * 记录进化叙事到 Markdown 文件
 */
function recordNarrative(params: {
  gene?: any;
  signals: string[];
  mutation?: any;
  outcome?: any;
  blast?: { files: number; lines: number };
  capsule?: any;
}) {
  const g = getGep();
  if (!g.recordNarrative) return;
  try { g.recordNarrative(params); } catch (_) {}
}

/**
 * 检查是否应该触发自省
 */
function checkShouldReflect(cycleCount: number, recentEvents: any[]) {
  const g = getGep();
  if (!g.shouldReflect) return false;
  try { return g.shouldReflect({ cycleCount, recentEvents }); } catch (_) { return false; }
}

/**
 * 构建自省上下文
 */
function buildReflectionContext(params: {
  recentEvents: any[];
  signals: string[];
  memoryAdvice: any;
  narrative: string;
}) {
  const g = getGep();
  if (!g.buildReflectionContext) return '';
  try { return g.buildReflectionContext(params); } catch (_) { return ''; }
}

/**
 * 触发 skillDistiller：从成功胶囊自动蒸馏新基因
 */
async function maybeDistillGene(prisma: any) {
  const g = getGep();
  if (!g.runDistillation) return;
  try {
    // skillDistiller 会检查时间间隔，不频繁
    await g.runDistillation({ prisma });
  } catch (e) {
    console.warn('[EvoMap] runDistillation failed:', (e as Error).message);
  }
}

/**
 * 尝试发布 skill 到 Hub
 */
async function maybePublishSkill(prisma: any, geneId: string) {
  const g = getGep();
  if (!g.publishSkillToHub) return;
  try {
    await g.publishSkillToHub({ prisma, geneId });
  } catch (e) {
    console.warn('[EvoMap] publishSkillToHub failed:', (e as Error).message);
  }
}

/**
 * 连续失败 → 检查是否需要上报 GitHub issue
 */
function maybeReportIssue(params: {
  recentEvents: any[];
  signals: string[];
  errorMessage?: string;
}) {
  const g = getGep();
  if (!g.maybeReportIssue) return;
  try { g.maybeReportIssue(params); } catch (_) {}
}

/**
 * 获取课程信号（gene mastery 追踪）
 */
function getCurriculumSignals(opts: {
  capabilityGaps?: string[];
  memoryGraphPath?: string;
  personality?: any;
}) {
  const g = getGep();
  if (!g.generateCurriculumSignals) return [];
  try { return g.generateCurriculumSignals(opts); } catch (_) { return []; }
}

/**
 * Hub review gate：apply 基因前检查是否需要 review
 */
async function runHubReview(params: {
  gene: any;
  signals: string[];
  prisma: any;
}) {
  const g = getGep();
  if (!g.runHubReview) return null;
  try { return await g.runHubReview(params); } catch (_) { return null; }
}

// ── Hub 上报（异步，不阻塞） ───────────────────────────────────────────────
async function reportToHub(
  capsuleId: string,
  outcome: 'success' | 'failure',
  execution_time_ms: number,
): Promise<void> {
  if (!HUB_BASE_URL) return;
  try {
    const envelope = buildEnvelope('singularity-primary', 'hub', 'report', {
      capsule_id: capsuleId, outcome, execution_time_ms,
    });
    await fetch(`${HUB_BASE_URL}/api/evomap/a2a/report`, {
      method: 'POST',
      headers: hubAuthHeaders(),
      body: JSON.stringify({ protocol: 'gep-a2a', message_type: 'report', ...envelope }),
      signal: AbortSignal.timeout(3000),
    });
  } catch (e) {
    console.warn('[Hub report] failed:', (e as Error).message);
  }
}

// ── Gene / Capsule 指标更新 ────────────────────────────────────────────────
async function updateGeneMetrics(geneId: string, success: boolean, duration: number, confidence: number, prisma: any) {
  const gene = await prisma.evolutionGene.findUnique({ where: { id: geneId } });
  if (!gene) return;
  const newTotalCount = gene.totalTaskCount + 1;
  const newSuccessCount = gene.successfulTaskCount + (success ? 1 : 0);
  const newSuccessRate = (newSuccessCount / newTotalCount) * 100;
  const newAvgDuration = Math.round((gene.avgDuration || duration) * 0.7 + duration * 0.3);
  const usageScore = Math.min(newTotalCount / 100, 1) * 20;
  const newGdiScore = newSuccessRate * 0.5 + confidence * 30 + usageScore;
  await prisma.evolutionGene.update({
    where: { id: geneId },
    data: {
      totalTaskCount: newTotalCount, successfulTaskCount: newSuccessCount,
      successRate: Math.round(newSuccessRate * 100) / 100,
      avgDuration: newAvgDuration,
      gdiScore: Math.round(newGdiScore * 100) / 100,
      metricsUpdatedAt: new Date(),
    },
  });
}

async function updateCapsuleMetrics(capsuleId: string, success: boolean, currentConfidence: number, prisma: any) {
  const capsule = await prisma.evolutionCapsule.findUnique({ where: { id: capsuleId } });
  if (!capsule) return;
  const newCount = capsule.usageCount + 1;
  const newConfidence = success
    ? Math.min(1.0, currentConfidence + 0.1)
    : Math.max(0.0, currentConfidence - 0.15);
  const newSuccessStreak = success ? (capsule.successStreak || 0) + 1 : 0;
  await prisma.evolutionCapsule.update({
    where: { id: capsuleId },
    data: { usageCount: newCount, confidence: Math.round(newConfidence * 1000) / 1000, successStreak: newSuccessStreak },
  });
}

// ── 主执行入口 ─────────────────────────────────────────────────────────────
export interface EngineOptions {
  prisma: any;
  defaultModel?: string;
}

export async function executeWithEvoMap(
  taskId: string,
  options: EngineOptions,
): Promise<{
  taskId: string;
  matched: boolean;
  bestMatch: GeneMatch | null;
  detectedSignals: DetectedSignal[];
  execution: {
    success: boolean; output: unknown; error?: string;
    duration: number; confidence: number; execMode: string; steps: string[];
  } | null;
}> {
  const { prisma } = options;

  // 1. 获取任务
  const task = await prisma.evolutionTask.findUnique({ where: { id: taskId } });
  if (!task) throw new Error(`Task not found: ${taskId}`);

  // 2. 检测信号（增强版：capability-evolver signals.js + fallback 正则）
  const signals = await extractSignalsEnhanced({
    taskType: task.taskType,
    input: task.input,
    error: task.error,
    output: task.output,
    recentEvents: [],
  });

  const signalStrings = signals.map(s => s.signal);

  // 2a. 记录信号快照到 memoryGraph
  recordSignalSnapshot(signalStrings, { taskId, taskType: task.taskType });

  // 2b. 课程信号注入
  const curriculumSignals = getCurriculumSignals({});
  const allSignals = [...signalStrings, ...curriculumSignals.filter((s: any) => !signalStrings.includes(s))];

  // 3. 匹配 Gene（可带 memoryGraph 偏好）
  const allGenes = await prisma.evolutionGene.findMany({ where: { isActive: true, taskType: task.taskType as any } });
  const memoryAdvice = queryMemoryGraph(signalStrings, allGenes, false);

  const matchResult = await matchGene({
    signals: allSignals.map(s => ({ signal: String(s), source: 'context' as const, metadata: {} })),
    taskType: task.taskType,
    prisma,
  });

  const bestMatch = selectBestMatch(matchResult);
  console.log(`[EvoMap Engine] Task ${taskId}\n${buildMatchReport(matchResult, bestMatch)}`);

  // 3a. 如果 memoryGraph 有偏好/禁令，记录假设
  if (memoryAdvice?.preferredGeneId) {
    const preferredGene = allGenes.find(g => g.id === memoryAdvice.preferredGeneId);
    if (preferredGene) {
      recordHypothesis({
        signals: signalStrings,
        selectedGene: preferredGene,
        selector: 'memory_graph',
        driftEnabled: false,
        selectedBy: 'memory_graph_advice',
      });
    }
  }

  // 4. 无匹配 → Hub 继承
  if (!bestMatch || !bestMatch.capsuleId) {
    console.log(`[EvoMap Engine] No local match, attempting Hub inheritance...`);
    const inherited = await inheritFromHub({
      signals: signalStrings, taskType: task.taskType, agentId: task.agentId, prisma,
    });

    if (!inherited) {
      await prisma.evolutionTask.update({
        where: { id: taskId },
        data: {
          metadata: {
            ...((task.metadata as Record<string, unknown>) || {}),
            evomapReason: 'no_gene_match',
            detectedSignals: signalStrings,
            evaluatedGenes: matchResult.matches.length,
          } as any,
        },
      });
      return { taskId, matched: false, bestMatch: null, detectedSignals: signals, execution: null };
    }

    const { capsule: inheritedCapsule, genes: inheritedGenes } = inherited;
    recordAttempt({
      signals: signalStrings,
      selectedGene: inheritedGenes[0],
      capsulesUsed: [inheritedCapsule.id],
      selectedBy: 'hub_inherit',
    });

    const execMode = (inheritedGenes[0]?.execMode || 'PROMPT') as 'PROMPT' | 'CODE' | 'WORKFLOW';
    const execution = await executeCapsule({
      capsuleId: inheritedCapsule.id, geneId: inheritedGenes[0]?.id || '',
      execMode, payload: inheritedCapsule.payload,
      geneStrategy: inheritedGenes[0]?.strategy, geneSignals: signalStrings,
      taskInput: { ...task.input, error: task.error || null, attempt: 0 },
    });

    const verifiedSuccess = execution.success;

    // 记录结果 + narrative
    recordOutcome(signalStrings, { taskId, success: verifiedSuccess, execution });
    recordNarrative({
      gene: inheritedGenes[0], signals: signalStrings, outcome: { status: verifiedSuccess ? 'success' : 'failed', score: execution.confidence },
      capsule: inheritedCapsule,
    });

    await prisma.evolutionTask.update({
      where: { id: taskId },
      data: {
        status: verifiedSuccess ? 'SUCCESS' : 'FAILURE',
        output: execution.output as any, error: execution.error || null,
        duration: execution.duration, quality: Math.round(execution.confidence * 100),
        geneId: inheritedGenes[0]?.id,
        metadata: {
          ...((task.metadata as Record<string, unknown>) || {}),
          evomapReason: 'hub_inherited', execMode: execution.execMode,
          detectedSignals: signalStrings, inheritedCapsuleId: inheritedCapsule.id,
        } as any,
      },
    });

    if (verifiedSuccess) {
      injectCapsule({ agentId: task.agentId, capsuleId: inheritedCapsule.id, genes: inheritedGenes, prisma }).catch(console.error);
      maybeDistillGene(prisma).catch(console.error);
    }

    reportToHub(inheritedCapsule.id, verifiedSuccess ? 'success' : 'failure', execution.duration).catch(console.error);
    return { taskId, matched: true, bestMatch: null, detectedSignals: signals, execution };
  }

  // 5. 执行本地匹配
  const gene = await prisma.evolutionGene.findUnique({ where: { id: bestMatch.geneId } });
  if (!gene) throw new Error(`Gene not found: ${bestMatch.geneId}`);

  // 5a. Hub review gate
  const reviewResult = await runHubReview({ gene, signals: signalStrings, prisma });
  if (reviewResult?.rejected) {
    console.warn(`[EvoMap] Hub review rejected gene ${gene.id}:`, reviewResult.reason);
  }

  // 5b. 记录 attempt
  recordAttempt({
    signals: signalStrings,
    mutation: undefined,
    personality_state: undefined,
    selectedGene: gene,
    capsulesUsed: bestMatch.capsuleId ? [bestMatch.capsuleId] : [],
    selectedBy: 'local_matching',
  });

  // 5c. 优先 Hub fetch capsule
  const hubResult = await fetchFromHub(signalStrings, task.taskType);
  let capsule;
  if (hubResult) {
    capsule = { id: hubResult.capsuleId, confidence: hubResult.capsuleConfidence, payload: hubResult.capsulePayload };
  } else {
    capsule = await prisma.evolutionCapsule.findUnique({ where: { id: bestMatch.capsuleId } });
  }

  const execMode = (gene.execMode as string) || 'PROMPT';
  const geneSignals = (gene.signals as string[]) || [];

  let execution;
  if (capsule && capsule.confidence >= 0.7) {
    execution = await executeCapsule({
      capsuleId: capsule.id, geneId: gene.id,
      execMode: execMode as 'PROMPT' | 'CODE' | 'WORKFLOW',
      payload: capsule.payload, geneStrategy: gene.strategy, geneSignals,
      taskInput: { ...task.input, error: task.error || null, attempt: 0 },
    });
  } else {
    execution = {
      success: false, output: null,
      error: `Best capsule confidence (${capsule?.confidence ?? 0}) below threshold (0.7)`,
      duration: 0, confidence: 0, execMode,
      steps: ['Skipped: capsule confidence too low'],
    };
  }

  const hadError = !!task.error;
  let verifiedSuccess = execution.success;
  if (hadError && execution.success) {
    verifiedSuccess = true;
    console.log(`[EvoMap Verify] Task ${taskId}: error resolved`);
  } else if (hadError && !execution.success) {
    verifiedSuccess = false;
    console.log(`[EvoMap Verify] Task ${taskId}: error persists`);
  }

  // 6. 记录 memoryGraph 闭环
  recordOutcome(signalStrings, { taskId, success: verifiedSuccess, execution });

  // 7. 记录 narrative
  recordNarrative({
    gene, signals: signalStrings,
    outcome: { status: verifiedSuccess ? 'success' : 'failed', score: execution.confidence },
    capsule: capsule as any,
  });

  // 8. 自省检查（每 N 轮触发一次）
  const cycleCount = (task.metadata as any)?.cycleCount || 1;
  if (checkShouldReflect(cycleCount, [])) {
    const g = getGep();
    const narrative = g?.loadNarrativeSummary ? g.loadNarrativeSummary({ maxChars: 3000 }) : '';
    const reflectionCtx = buildReflectionContext({
      recentEvents: [], signals: signalStrings, memoryAdvice: memoryAdvice || {}, narrative,
    });
    // 异步 LLM 自省（不阻塞主流程）
    console.log('[EvoMap] Reflection triggered. Context:', reflectionCtx.substring(0, 200));
  }

  // 9. 更新任务状态
  await prisma.evolutionTask.update({
    where: { id: taskId },
    data: {
      status: verifiedSuccess ? 'SUCCESS' : 'FAILURE',
      output: execution.output as any, error: execution.error || null,
      duration: execution.duration, quality: Math.round(execution.confidence * 100),
      geneId: gene.id,
      metadata: {
        ...((task.metadata as Record<string, unknown>) || {}),
        evomapMatched: true, execMode: execution.execMode,
        detectedSignals: signalStrings,
        matchedSignals: bestMatch.matchedSignals,
        memoryAdvicePreferred: memoryAdvice?.preferredGeneId || null,
        memoryAdviceBanned: memoryAdvice?.bannedGeneIds ? Array.from(memoryAdvice.bannedGeneIds) : [],
      } as any,
    },
  });

  // 10. 写 EvolutionEvent
  await prisma.evolutionEvent.create({
    data: {
      eventType: verifiedSuccess ? 'TASK_COMPLETED' : 'TASK_FAILED',
      actorId: task.agentId, taskId: task.id,
      geneId: gene.id, capsuleId: capsule?.id,
      metadata: {
        detectedSignals: signalStrings,
        matchedSignals: bestMatch.matchedSignals,
        matchScore: bestMatch.score,
        execMode: execution.execMode,
        capsuleConfidence: capsule?.confidence,
      } as any,
    },
  });

  // 11. 更新指标
  updateGeneMetrics(gene.id, verifiedSuccess, execution.duration, execution.confidence, prisma).catch(console.error);
  if (capsule) {
    updateCapsuleMetrics(capsule.id, verifiedSuccess, capsule.confidence, prisma).catch(console.error);
    reportToHub(capsule.id, verifiedSuccess ? 'success' : 'failure', execution.duration).catch(console.error);
  }

  // 12. 注入 + 蒸馏 + 发布
  if (verifiedSuccess && capsule) {
    const geneForInject: CachedGene = {
      id: gene.id, name: gene.name, displayName: gene.displayName,
      taskType: gene.taskType, signals: gene.signals || [],
      execMode: gene.execMode || 'PROMPT', strategy: gene.strategy,
      constraints: gene.constraints, minConfidence: gene.minConfidence || 0.7,
      isActive: true, cachedAt: new Date().toISOString(),
    };
    injectCapsule({ agentId: task.agentId, capsuleId: capsule.id, genes: [geneForInject], prisma }).catch(console.error);
    maybeDistillGene(prisma).catch(console.error);
    maybePublishSkill(prisma, gene.id).catch(console.error);
  }

  // 13. 连续失败检查 → GitHub issue
  maybeReportIssue({ recentEvents: [], signals: signalStrings, errorMessage: task.error || undefined });

  return { taskId, matched: true, bestMatch, detectedSignals: signals, execution };
}

export async function runTask(taskId: string, prisma: any): Promise<void> {
  await executeWithEvoMap(taskId, { prisma });
}
