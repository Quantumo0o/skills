---
name: skill-manager-all-in-one
description: "Manage OpenClaw skills end to end: find, audit, create, update, publish, and promote. 一站式管理 OpenClaw 技能：查找、审计、创建、更新、发布与宣传。"
---

# Skill Manager | 技能管理器

Manage OpenClaw skills from local discovery to ClawHub publishing. 负责 OpenClaw 技能从本地发现到 ClawHub 发布的全流程管理。

## Core rules | 核心规则

1. **Local first, network second** — check installed skills before searching ClawHub.  
   **先本地，后网络**——先检查已安装技能，再决定是否搜索 ClawHub。

2. **User approval first** — do not publish, update, delete, hide, or materially rewrite a skill without explicit user consent.  
   **先获用户同意**——未经明确确认，不要发布、更新、删除、隐藏，或实质性改写技能。

3. **Be concrete** — report exact paths, exact commands, and exact version changes.  
   **表达具体**——汇报时写清楚准确路径、准确命令、准确版本变化。

4. **Prefer formal release language** — ClawHub release text should read like a product release note, not a casual chat log.  
   **发布语言要正式**——ClawHub 发布文本应像正式发布说明，而不是聊天记录。

5. **Teach good output, not just good structure** — this is a supervisory skill, so its guidance must produce clean, publishable names, descriptions, changelogs, and promotion copy.  
   **不仅结构达标，输出也要达标**——这是指导性技能，它给出的名称、描述、changelog 和宣传文案也必须干净、可发布、对外体面。

6. **Write for both AI and humans** — future skills should be readable by agents and by people, especially Chinese-speaking users.  
   **同时面向 AI 和人类**——后续制作的技能应兼顾 agent 与人类可读性，尤其要照顾中文用户。

## Required naming and writing rules | 命名与写作规范

### Slug | 部署名

- Use lowercase letters, digits, and hyphens only.  
  只使用小写字母、数字和连字符。

### Display name | 显示名

- Use English first, then Chinese.  
  英文在前，中文在后。
- Format as: `English Name | 中文名`  
  格式统一为：`English Name | 中文名`

Example | 示例:
- `Camera YOLO Operator | 摄像头 YOLO 操控者`

### Description | 描述

- Write English first, then Chinese.  
  英文在前，中文在后。
- Keep it concrete, specific, and attractive.  
  要具体、明确、抓眼。
- Prefer about **150 characters** when possible.  
  尽量控制在 **150 字符左右**。
- Avoid keyword stuffing.  
  避免关键词堆砌。
- Write something that would still look professional on a public listing page.  
  写出来的内容要能直接放到公开列表页上，仍然显得专业。

Good example | 推荐示例:
- `Manage OpenClaw skills end to end: find, audit, create, update, publish, and promote. 一站式管理 OpenClaw 技能：查找、审计、创建、更新、发布与宣传。`

### Body text | 正文

- Write skill bodies in bilingual form when practical.  
  skill 正文在可行时应写成英中文双语。
- Keep English as the main structural spine, with shorter Chinese support when needed.  
  英文可以作为主骨架，中文可以稍简，但关键规则与关键流程要覆盖到。
- Do not make the Chinese an afterthought if the skill is meant to be read by human users.  
  如果技能预期也会被人类阅读，就不要把中文写成可有可无的附属品。

### Changelog | 发布说明

- Write bilingual changelogs for ClawHub releases.  
  ClawHub 发布说明必须使用英中文双语。
- Put **English first, Chinese after**.  
  **英文在前，中文在后**。
- Keep the tone **formal and release-ready**.  
  语气必须**正式、可直接发布**。
- Focus on user-visible value, stability, compatibility, and workflow improvements.  
  聚焦用户可感知价值、稳定性、兼容性和流程优化。
- Do **not** add casual filler, apology-style phrasing, or wording that exposes small mistakes.  
  不要加入随意口吻、道歉式措辞，或暴露小失误的话。
- Do **not** write like an internal debug note.  
  不要写成内部调试记录。

Good style | 推荐风格:
- `Improve cross-platform behavior with automatic Windows/macOS detection. 优化跨平台行为，新增 Windows/macOS 自动识别。`

Avoid | 避免:
- casual jokes / 随意玩笑
- self-deprecating notes / 自嘲式描述
- "fixed a silly bug"
- "the old way was fragile and bad"

## Working flow | 工作流

### 1. Review or search skills | 查看或搜索技能

- Check local formal skills directory first: `~/.openclaw/skills`  
  先检查本地正式技能目录：`~/.openclaw/skills`
- Check built-in skills if relevant.  
  如有需要，再检查内置技能。
- If the skill is not local, search ClawHub.  
  本地没有时，再搜索 ClawHub。

For search and audit details, read:  
搜索与审计细节请读：
- `references/search-and-audit.md`

### 2. Create or revise a skill | 创建或修订技能

- Prefer building drafts in `~/.openclaw/workspace/temp-skills/<slug>/`  
  草稿优先放在 `~/.openclaw/workspace/temp-skills/<slug>/`
- Let the user review meaningful edits before publish or update actions.  
  在发布或升版前，让用户先审阅关键修改。
- Keep `SKILL.md` lean; move long operational details into `references/`.  
  保持 `SKILL.md` 精简，把较长操作细节放进 `references/`。
- When a skill is expected to be human-readable, write the body in bilingual form.  
  如果技能也预期给人看，正文应写成双语形式。

### 3. Publish or update on ClawHub | 在 ClawHub 发布或更新

- Confirm slug, display name, version, and changelog.  
  确认 slug、显示名、版本号和 changelog。
- Check CLI help if command details may have changed.  
  如果命令细节可能变化，先查看 CLI help。
- Publish only after explicit user confirmation.  
  只有在用户明确确认后才执行发布。

For publish details, read:  
发布细节请读：
- `references/clawhub-publish.md`

### 4. Inspect published skills | 查看已发布技能

- Do not assume the browser is always the best tool.  
  不要默认浏览器永远是最优工具。
- Recheck current CLI help before choosing tools, because the CLI can gain new commands and options over time.  
  先重新查看当前 CLI help，再决定用什么工具，因为 CLI 会持续增加新命令和新参数。
- Choose CLI or Dashboard based on the current task after that check.  
  检查之后，再根据当前任务选择 CLI 或 Dashboard。

For inspection details, read:  
查看细节请读：
- `references/clawhub-inspect.md`

### 5. Promote published skills | 宣传已发布技能

- Check de-identification first.  
  先做去标识化检查。
- Use polished bilingual copy.  
  使用体面、清晰的双语文案。
- Keep links and install commands exact.  
  保证链接与安装命令准确无误。

For promotion details, read:  
宣传细节请读：
- `references/promotion.md`

## Directory terms | 目录术语

- **Built-in skills**: OpenClaw bundled skills  
  **内置技能**：OpenClaw 自带技能
- **Formal skills**: `~/.openclaw/skills`  
  **正式技能目录**：`~/.openclaw/skills`
- **Temporary draft skills**: `~/.openclaw/workspace/temp-skills`  
  **临时草稿目录**：`~/.openclaw/workspace/temp-skills`

Formal skills override built-in skills with the same slug.  
正式技能目录中的同名技能会覆盖内置技能。

## Practical note | 实用说明

This skill was tested primarily on Linux-style workflows, but the ClawHub CLI guidance should be rechecked with `clawhub --help` on the current machine before sensitive actions.  
本技能主要按 Linux 风格流程整理，但在当前机器上执行敏感操作前，仍应先用 `clawhub --help` 重新核对 CLI 行为。
