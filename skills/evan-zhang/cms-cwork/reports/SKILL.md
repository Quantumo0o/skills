---
name: cwork-reports
description: Send, draft, query, and reply to work reports in CWork. Use when sending reports, querying inbox/unread, replying to reports, managing drafts, or running AI analysis on report content.
---

## When to Use

- 发送、生成、改写工作汇报
- 查询收件箱、发件箱、未读汇报
- 回复汇报、标记已读
- 管理草稿（保存/确认/发送/删除）
- 对汇报内容进行 AI 问答

## Skills

| Skill | 说明 | LLM |
|-------|------|-----|
| draft-gen | 将零散内容整理为结构化草稿 | ✅ |
| outline-gen | 生成汇报大纲 | ✅ |
| report-rewrite | 结构/表达优化 | ✅ |
| report-complete | 补齐缺失字段 | ✅ |
| report-tone-adapt | 调整表达口径 | ✅ |
| report-formality-adjust | 调整正式程度 | ✅ |
| report-submit | 正式提交汇报 | ❌ |
| report-submit-with-attachments | 一站式发送带附件汇报 | ❌ |
| file-upload | 上传文件获取 fileId | ❌ |
| report-prepare | 准备确认内容（不调 API）| ❌ |
| report-validate-receivers | 按姓名校验接收人 | ❌ |
| report-reply | 回复汇报 | ❌ |
| report-read-mark | 标记已读 | ❌ |
| unread-report-list | 获取未读汇报列表 | ❌ |
| report-is-read | 判断是否已读 | ❌ |
| ai-report-chat | AI 问答（SSE 流式）| ❌ |
| template-list | 查询事项列表 | ❌ |
| template-info-batch | 批量查事项详情 | ❌ |
| report-format | 按模板格式化内容 | ❌ |

## Core Rules

1. **必须走草稿流程发送汇报**：`draftSave` → 展示给用户确认 → `draftSubmit`。直接调 `report-submit` 仅限用户明确要求跳过确认。

2. **姓名自动解析**：接收人支持传姓名，内部自动调 `emp-search`。不要让用户提供 empId。

3. **LLM 由调用方注入**：✅ 标记的 Skill 需传 `{ llmClient }`，本域不存储 LLM 凭证。

## References

- `references/examples.md` — 6 个场景完整代码示例（发送/附件/回复/未读/AI问答）
- `references/types.md` — 类型枚举（reportLevelList.type / reportRecordType / myStatus）
