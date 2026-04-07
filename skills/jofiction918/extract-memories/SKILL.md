---
name: extract-memories
version: 3.0.5
description: "对话结束时主动提炼关键记忆到 topic 文件（提醒型自动）/ 触发词：提炼记忆、提取记忆 / 命令：/extract-memories"
license: MIT
triggers:
  - 提炼记忆
  - 提取记忆
  - extract-memories
  - "/extract-memories"
---

# extract-memories v3.0.0 — 对话记忆提炼

对话结束时主动分析本轮对话，将值得持久化的信息写入 `memory/topics/` 下的独立 topic 文件，同时更新 `MEMORY.md` 索引。

## 安装后配置

首次安装后，请确保 `memory/heartbeat-state.json` 文件存在，内容如下：
```json
{
  "lastExtraction": null,
  "lastDreamAt": null,
  "sessionCount": 0,
  "lastEmailCheck": null,
  "lastCalendarCheck": null
}
```

---

## 触发机制

### 主会话主动触发（主要）

每次对话结束时，主 agent 会：
1. 检测结束模式：中文（`再见`/`bye`/`下次见`/`拜拜`/`结束了`/`先这样`）或英文（`bye`/`see you`/`that's all`）
2. 检测到结束模式 → 主动执行记忆提炼
3. 提炼完成后提示："已为您提炼本轮记忆 ✅"

> **注意**：主动触发依赖 agent 侧实现。建议在 AGENTS.md 中加入一行：
> ```
> 对话结束时，主动调用 /extract-memories 提炼关键记忆。
> ```
> 这样可以确保每次对话结束都会自动执行。

### Heartbeat 辅助检测

每次 heartbeat 时检查：
- 最近消息是否匹配结束模式
- 或距上次提炼是否超过 30 分钟
- 若满足条件则触发提炼

### 手动触发

- 命令：`/extract-memories`

---

## 核心概念

**MEMORY.md = 索引，不是记忆文件。**

```
memory/
├── MEMORY.md              ← 纯索引（一行一个指针，不含记忆内容）
├── heartbeat-state.json   ← 状态记录（lastExtraction 时间戳）
└── topics/               ← 所有记忆文件
    ├── user_role.md
    ├── feedback_concise.md
    ├── project_deadline.md
    └── reference_xxx.md
```

## 四种记忆类型

| 类型 | 什么时候存 | 正文结构 |
|------|-----------|---------|
| `user` | 学到用户角色/偏好/知识时 | 一段文字即可，无强制结构 |
| `feedback` | 用户纠正你或确认你做对了 | **规则本身 → Why:（原因）→ How to apply:（何时适用）** |
| `project` | 学到项目截止/动机/约束时 | **事实 → Why:（动机）→ How to apply:（如何影响工作）** |
| `reference` | 学到外部系统指针时 | URL/路径 + 用途说明 |

### body 结构示例

**feedback 示例**：

> 集成测试必须用真实数据库，不能用 mock。
> **Why:** 上次 mock 测试通过了，但 prod 迁移时才发现行为不一致，导致故障。
> **How to apply:** 任何涉及数据库的测试优先用真实实例而非 mock 对象。

**project 示例**：

> 非关键 PR 合并冻结：2026-04-05 起，所有非关键 PR 暂停合并。
> **Why:** 移动端团队需要从 release 分支切出，周五前完成代码冻结。
> **How to apply:** 评估任何计划中的 PR 是否属于"非关键"，若是则延后。

---

## 提炼输出

提炼完成后提示：

> 已为您提炼本轮记忆 ✅
> 写入位置：memory/topics/
>
> **提炼结果：2条**
>
> ### user
> - [记忆系统触发机制修复v3]: 记录三件套触发机制修复方案
>   核心问题：OpenClaw 无 conversation-end 钩子，skill 描述夸大
>
> ### project
> - [记忆系统触发机制修复v3]: 记录三件套触发机制修复方案
>   桌面说明文件路径需同步更新
>   **Why:** 三端版本对齐问题反复出现
>   **How to apply:** 按 UPDATE_FLOW.md 规范执行

---

## 写入规范（两步写入）

**Step 1**：写 topic 文件到 `memory/topics/`（APPEND 模式，不覆盖已有内容）

文件命名：`memory/topics/[type]_[slug].md`

**Step 2**：在 `MEMORY.md` 末尾追加一行指针

格式：`- [名称](topics/文件名.md) — 一句话 hook`（不超过 150 字符）

---

## frontmatter 格式（必须包含）

```yaml
---
name: 一句话名称
description: 一行描述（用于判断 relevance，决定未来是否调取这条记忆）
type: user / feedback / project / reference
---
正文内容
```

**name 命名规范**：
- `user_role.md` — 用户身份/角色
- `feedback_[主题].md` — 用户偏好和纠正
- `project_[项目/主题].md` — 项目上下文
- `reference_[系统名].md` — 外部系统指针

---

## What NOT to Save（6条禁止）

即使用户明确要求保存以下内容，也要先询问"这个值得保存吗"：

1. **代码结构/架构/文件路径**——可从源码重新读取
2. **Git 历史**——`git log` / `git blame` 是权威来源
3. **调试方案/fix 配方**——修复方案在代码里，commit message 有上下文
4. **CLAUDE.md / AGENTS.md 已有的内容**——不要重复
5. **临时任务状态**——属于 plan，不属于记忆
6. **即使用户要求也不保存**：PR 列表、活动摘要——改为问"有什么非 очевидный（不明显的）值得记忆"

---

## 权限要求

- `FileRead`：读取对话上下文、MEMORY.md、topics/
- `FileWrite` / `FileEdit`：写入 `memory/topics/`、`MEMORY.md`、`memory/heartbeat-state.json`
- `sessions_history`：读取主会话消息（heartbeat 触发时）

## 触发词

- 自动：主会话主动检测结束模式（提醒型）
- 自动：Heartbeat 检测（辅助）
- 手动：`/extract-memories`

---

*本 Skill 基于 CC 记忆系统 extractMemories 设计，适配 OpenClaw v3.0.0*
