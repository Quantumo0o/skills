/**
 * EvoMap Session Injector
 * 执行成功后，将 Capsule 能力持久注入到 Agent 的系统提示词
 */

import type { CachedGene } from './asset-cache';

export interface InjectedCapability {
  capsuleId: string;
  geneIds: string[];
  systemPromptPatch: string;
  injectedAt: Date;
  expiresAt?: Date;
}

/**
 * 将多个 Gene 策略组合成系统提示词补丁
 */
function buildSystemPromptPatch(genes: CachedGene[], capsuleId: string): string {
  const parts: string[] = [
    `## EvoMap 注入能力 [capsule:${capsuleId}]`,
    '以下策略已通过 EvoMap 继承，在本会话中持续生效：',
    '',
  ];

  for (const gene of genes) {
    parts.push(`### ${gene.displayName || gene.name}`);
    const strategy = gene.strategy as Record<string, unknown> | null;
    if (strategy?.description) {
      parts.push(String(strategy.description));
    } else if (Array.isArray(strategy?.steps)) {
      const steps = strategy.steps as Array<Record<string, unknown>>;
      steps.forEach((s, i) => {
        parts.push(`${i + 1}. ${s.method || s.action || s.name || ''}: ${s.description || ''}`);
      });
    } else if (strategy) {
      parts.push(JSON.stringify(strategy));
    }
    parts.push('');
  }

  return parts.join('\n');
}

/**
 * 注入 Capsule 能力到 Agent
 * 将 Gene 策略写入 EvoMapInjection 表，后续任务可通过 buildAugmentedSystemPrompt 读取
 */
export async function injectCapsule(params: {
  agentId: string;
  capsuleId: string;
  genes: CachedGene[];
  prisma: any;
  expiresInHours?: number;
}): Promise<InjectedCapability> {
  const { agentId, capsuleId, genes, prisma, expiresInHours } = params;

  const systemPromptPatch = buildSystemPromptPatch(genes, capsuleId);
  const geneIds = genes.map(g => g.id);
  const expiresAt = expiresInHours
    ? new Date(Date.now() + expiresInHours * 3600 * 1000)
    : undefined;

  // 同一 capsule 已注入则更新，否则新建
  const existing = await prisma.evoMapInjection.findFirst({
    where: { agentId, capsuleId },
  });

  if (existing) {
    await prisma.evoMapInjection.update({
      where: { id: existing.id },
      data: { isActive: true, systemPromptPatch, geneIds, expiresAt: expiresAt ?? null },
    });
  } else {
    await prisma.evoMapInjection.create({
      data: { agentId, capsuleId, geneIds, systemPromptPatch, expiresAt: expiresAt ?? null },
    });
  }

  return {
    capsuleId,
    geneIds,
    systemPromptPatch,
    injectedAt: new Date(),
    expiresAt,
  };
}

/**
 * 获取 Agent 当前所有生效的注入
 */
export async function getActiveInjections(agentId: string, prisma: any): Promise<InjectedCapability[]> {
  const rows = await prisma.evoMapInjection.findMany({
    where: {
      agentId,
      isActive: true,
      OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }],
    },
    orderBy: { createdAt: 'asc' },
  });

  return rows.map((r: any) => ({
    capsuleId: r.capsuleId,
    geneIds: r.geneIds,
    systemPromptPatch: r.systemPromptPatch,
    injectedAt: r.createdAt,
    expiresAt: r.expiresAt ?? undefined,
  }));
}

/**
 * 将所有生效注入合并进基础系统提示词
 * 在 capsule-executor.ts PROMPT 模式中调用
 */
export async function buildAugmentedSystemPrompt(
  basePrompt: string,
  agentId: string,
  prisma: any,
): Promise<string> {
  const injections = await getActiveInjections(agentId, prisma);
  if (injections.length === 0) return basePrompt;

  const patches = injections.map(i => i.systemPromptPatch).join('\n\n');
  return `${basePrompt}\n\n${patches}`;
}
