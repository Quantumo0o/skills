---
name: cwork-tasks
description: Create, query, and manage work tasks in CWork. Use when creating tasks, tracking progress, identifying blockers, viewing manager dashboards, or extracting todos from content.
---

## When to Use

- 创建、分配、跟踪工作任务
- 查询任务列表（我的/下属的/全部）
- 识别逾期任务和卡点
- 管理者视角查看下属任务执行情况
- 从汇报或讨论内容中提取待办事项

## Skills

| Skill | 说明 | LLM |
|-------|------|-----|
| task-create | 创建任务，支持姓名自动解析 | ❌ |
| task-list-query | 分页查询任务列表 | ❌ |
| task-my-assigned | 查询分配给我的任务 | ❌ |
| task-my-created | 查询我创建的任务 | ❌ |
| task-manager-dashboard | 管理者视角：下属任务汇总 | ❌ |
| task-chain-get | 任务 + 关联汇报完整链路 | ❌ |
| task-blocker-identify | 识别逾期/卡点任务 | ❌ |
| my-feedback-list | 查询我创建的反馈待办 | ❌ |
| task-structure | 整理待办为结构化任务草稿 | ❌ |
| todo-extract | 从内容中抽取待办事项 | ✅ |
| task-blocker-tip | 为卡点任务提供解决建议 | ✅ |
| task-adjustment-suggest | 基于进展提出调整建议 | ✅ |

## Core Rules

1. **姓名自动解析**：`assignee` 等所有人员字段直接传姓名即可，内部自动调 `emp-search`。不要问用户要 empId。

2. **deadline 必须是时间戳**：传毫秒数字，不能传字符串。用 `new Date('...').getTime()`。

3. **LLM 由调用方注入**：✅ 标记的 Skill 需传 `{ llmClient }`。

## References

- `references/examples.md` — 5 个场景完整代码示例（查询/创建/链路/仪表盘/卡点）
- `references/types.md` — 类型枚举（status / reportStatus / deadline 格式）
