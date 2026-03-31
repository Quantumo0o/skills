/**
 * Skill: task-create
 * 创建工作任务
 *
 * 支持姓名自动解析：所有人员字段（assignee/reportEmpIdList/assistEmpIdList 等）
 * 均可传姓名或 empId，内部自动调用 emp-search 解析。
 * - 纯数字 → 直接作为 empId 使用
 * - 姓名字符串 → 调用 searchEmpByName 解析
 *   - 唯一匹配 → 自动使用
 *   - 多个候选 → 抛出错误，列出候选让用户选择
 *   - 未找到 → 抛出错误
 */

import { cworkClient } from '../shared/cwork-client.js';
import type { TaskCreateInput, TaskCreateOutput } from '../shared/types.js';

// ---------------------------------------------------------------------------
// 姓名 → empId 解析
// ---------------------------------------------------------------------------

async function resolveEmpId(nameOrId: string): Promise<string> {
  // 纯数字视为 empId，直接返回
  if (/^\d+$/.test(nameOrId.trim())) return nameOrId.trim();

  const result = await cworkClient.searchEmpByName(nameOrId.trim());
  const allEmps = [
    ...(result.inside?.empList ?? []),
    ...(result.outside?.empList ?? []),
  ];

  if (allEmps.length === 0) {
    throw new Error(`未找到员工"${nameOrId}"，请确认姓名是否正确`);
  }
  if (allEmps.length === 1) {
    return String(allEmps[0].empId ?? allEmps[0].id);
  }
  // 多个候选，精确匹配姓名
  const exact = allEmps.filter(e => e.name === nameOrId.trim());
  if (exact.length === 1) {
    return String(exact[0].empId ?? exact[0].id);
  }
  // 列出候选
  const candidates = allEmps.slice(0, 5).map(e => `${e.name}（${e.mainDept ?? e.deptName ?? ''}）`).join('、');
  throw new Error(`"${nameOrId}" 匹配到多个员工：${candidates}，请提供更精确的姓名`);
}

async function resolveEmpIds(list: string[]): Promise<string[]> {
  const results: string[] = [];
  for (const item of list) {
    results.push(await resolveEmpId(item));
  }
  return results;
}

// ---------------------------------------------------------------------------
// 主函数
// ---------------------------------------------------------------------------

export async function taskCreate(input: TaskCreateInput): Promise<TaskCreateOutput> {
  const {
    title,
    content,
    target,
    assignee,
    deadline,
    grades,
    reportEmpIdList = [],
    assistEmpIdList,
    supervisorEmpIdList,
    copyEmpIdList,
    observerEmpIdList,
    pushNow = true,
  } = input;

  if (!title?.trim()) return { success: false, message: '任务标题不能为空' };
  if (!content?.trim()) return { success: false, message: '任务描述不能为空' };
  if (!deadline) return { success: false, message: '任务截止时间不能为空（必须是毫秒时间戳，如 new Date("2026-04-14").getTime()）' };
  if (typeof deadline === 'string') {
    return { success: false, message: `任务截止时间必须是数字（毫秒时间戳），收到字符串"${deadline}"。正确用法：new Date("2026-04-14 23:59:59").getTime()` };
  }

  try {
    // 并行解析所有人员字段
    const [
      resolvedAssignee,
      resolvedReporters,
      resolvedAssists,
      resolvedSupervisors,
      resolvedCopies,
      resolvedObservers,
    ] = await Promise.all([
      assignee ? resolveEmpId(assignee) : Promise.resolve(undefined),
      reportEmpIdList.length > 0 ? resolveEmpIds(reportEmpIdList) : Promise.resolve([]),
      assistEmpIdList?.length ? resolveEmpIds(assistEmpIdList) : Promise.resolve(undefined),
      supervisorEmpIdList?.length ? resolveEmpIds(supervisorEmpIdList) : Promise.resolve(undefined),
      copyEmpIdList?.length ? resolveEmpIds(copyEmpIdList) : Promise.resolve(undefined),
      observerEmpIdList?.length ? resolveEmpIds(observerEmpIdList) : Promise.resolve(undefined),
    ]);

    const params = {
      main: title.trim(),
      needful: content.trim(),
      target: target?.trim() || content.trim(),
      typeId: 9999,
      reportEmpIdList: resolvedReporters.length > 0
        ? resolvedReporters
        : resolvedAssignee ? [resolvedAssignee] : [],
      endTime: deadline,
      ownerEmpIdList: resolvedAssignee ? [resolvedAssignee] : undefined,
      assistEmpIdList: resolvedAssists?.length ? resolvedAssists : undefined,
      supervisorEmpIdList: resolvedSupervisors?.length ? resolvedSupervisors : undefined,
      copyEmpIdList: resolvedCopies?.length ? resolvedCopies : undefined,
      observerEmpIdList: resolvedObservers?.length ? resolvedObservers : undefined,
      pushNow: pushNow ? 1 : 0,
    };

    const taskId = await cworkClient.createPlan(params);
    return { success: true, data: { taskId } };
  } catch (error) {
    return {
      success: false,
      message: `任务创建失败: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}
