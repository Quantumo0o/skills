/**
 * EvoMap Gene Matcher
 * 基于检测到的信号，找到最匹配的 Gene 和对应 Capsule
 */

import type { DetectedSignal } from './signal-detector';

export interface GeneMatch {
  geneId: string;
  geneName: string;
  displayName: string;
  taskType: string;
  score: number;           // 匹配度 0-1
  matchedSignals: string[];
  capsuleId?: string;
  capsuleConfidence?: number;
  capsulePayload?: unknown;
  geneStrategy?: unknown;
}

export interface MatchResult {
  matches: GeneMatch[];
  taskType: string;
  detectedSignals: string[];
}

/**
 * 基于信号列表，从数据库中匹配 Gene
 */
export async function matchGene(params: {
  signals: DetectedSignal[];
  taskType: string;
  prisma: any;
}): Promise<MatchResult> {
  const { signals, taskType, prisma } = params;

  const signalSet = new Set(signals.map(s => s.signal));

  // 1. 查找所有活跃的 Gene（按 taskType 过滤 + 支持信号匹配的）
  const genes = await prisma.evolutionGene.findMany({
    where: {
      isActive: true,
      taskType: taskType as any,
    },
    include: {
      capsules: {
        where: {
          reviewStatus: 'APPROVED',
          confidence: { gte: 0.5 }, // 预筛：>= 0.5；selectBestMatch 再用 >= 0.7 二次过滤
        },
        orderBy: { confidence: 'desc' },
        take: 1,
      },
    },
  });

  if (genes.length === 0) {
    return { matches: [], taskType, detectedSignals: [...signalSet] };
  }

  // 2. 计算每个 Gene 的匹配得分
  const matches: GeneMatch[] = genes.map((gene: any) => {
    const geneSignals = new Set((gene.signals as string[]) || []);
    const matched = [...signalSet].filter(s => geneSignals.has(s));

    // 主得分：信号重叠率
    // 备选得分：如果 Gene 没有 signals 数组，则用 taskType 完全匹配
    let score: number;
    if (geneSignals.size > 0) {
      score = matched.length / geneSignals.size;
    } else {
      // 没有 signals 的 Gene，靠 taskType 匹配，得基础分
      score = 0.5;
    }

    const capsule = gene.capsules[0];

    return {
      geneId: gene.id,
      geneName: gene.name,
      displayName: gene.displayName,
      taskType: gene.taskType,
      score,
      matchedSignals: matched,
      capsuleId: capsule?.id,
      capsuleConfidence: capsule?.confidence,
      capsulePayload: capsule?.payload,
      geneStrategy: gene.strategy,
    };
  });

  // 3. 排序：得分高的在前，过滤掉得分 < 0.1 的
  matches.sort((a, b) => b.score - a.score);

  const filtered = matches.filter(m => m.score >= 0.1);

  return {
    matches: filtered,
    taskType,
    detectedSignals: [...signalSet],
  };
}

/**
 * 选择最佳匹配（得分最高且有 Capsule 的）
 */
export function selectBestMatch(result: MatchResult): GeneMatch | null {
  return result.matches.find(m => m.capsuleId && m.capsuleConfidence && m.capsuleConfidence >= 0.7) || null;
}

/**
 * 构建匹配报告（用于日志/调试）
 */
export function buildMatchReport(result: MatchResult, best: GeneMatch | null): string {
  const lines: string[] = [];
  lines.push(`TaskType: ${result.taskType}`);
  lines.push(`Detected signals: ${result.detectedSignals.join(', ') || '(none)'}`);
  lines.push(`Total candidates: ${result.matches.length}`);

  if (result.matches.length > 0) {
    lines.push('\nCandidate rankings:');
    result.matches.slice(0, 5).forEach((m, i) => {
      lines.push(`  #${i + 1} ${m.geneName} (score=${m.score.toFixed(2)}, capsule=${m.capsuleId ? 'yes' : 'no'})`);
      lines.push(`      matched signals: ${m.matchedSignals.join(', ') || 'none'}`);
    });
  }

  if (best) {
    lines.push(`\nSelected: ${best.geneName} (confidence=${best.capsuleConfidence})`);
  } else {
    lines.push('\nSelected: none (no capsule with sufficient confidence)');
  }

  return lines.join('\n');
}
