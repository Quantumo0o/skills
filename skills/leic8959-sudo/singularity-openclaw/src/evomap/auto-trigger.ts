/**
 * EvoMap 自动触发层
 * 在业务路由 catch 块中调用，fire-and-forget，不阻塞主响应
 */

import { executeWithEvoMap } from './engine';

type TaskType =
  | 'POST_SUMMARY'
  | 'VIOLATION_DETECTION'
  | 'AUTO_REPLY'
  | 'CONTENT_MODERATION'
  | 'SENTIMENT_ANALYSIS';

/**
 * 捕获到错误时自动创建 EvolutionTask 并触发引擎
 * 异步执行，不抛出异常
 */
export function triggerEvoMapOnError(params: {
  prisma: any;
  agentId: string;
  taskType: TaskType;
  input: unknown;
  error: Error | string;
}): void {
  const { prisma, agentId, taskType, input, error } = params;
  const errorMessage = error instanceof Error ? error.message : String(error);

  // fire-and-forget
  (async () => {
    try {
      const task = await prisma.evolutionTask.create({
        data: {
          taskType,
          input: input as any,
          error: errorMessage,
          agentId,
          status: 'PENDING',
        },
      });
      await executeWithEvoMap(task.id, { prisma });
    } catch (e) {
      console.warn('[EvoMap AutoTrigger] failed:', (e as Error).message);
    }
  })();
}
