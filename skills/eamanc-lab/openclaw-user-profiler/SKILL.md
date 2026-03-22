---
name: openclaw-user-profiler
description: |-
  为 OpenClaw Agent 采集用户画像并生成 user.md，让龙虾更了解它的主人。
  支持两种模式：画像采集（对话收集用户信息写入 user.md）和 Skill 推荐
  （根据用户角色推荐适合的 Claude Code Skill）。
  当用户需要让 OpenClaw Agent 了解自己、更新个人信息、或寻找适合自己的 Skill 时使用。
  不适用于：修改 SOUL.md（用锻造炉）、安装 Skill（用户自行操作）、通用 AI 问答。
  触发词：了解我、认识我、更新用户信息、写 user.md、用户画像、
  推荐 skill、适合我的 skill、我是工程师、我是产品经理、
  user profile、know me、recommend skills、skill for my role。
license: MIT
homepage: https://github.com/eamanc-lab/openclaw-persona-forge
metadata:
  author: eamanc
  version: 1.0.0
compatibility:
  platforms:
    - claude-code
    - claude-ai
---

# OpenClaw 用户画像师 🦞🔍

> 龙虾想了解你——不是审问，是交朋友。

## Skill 目录约定

**Agent Execution**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Replace all `${SKILL_DIR}` in this document with the actual path

## 核心理念

好的 user.md = **角色定位** + **能力画像** + **偏好习惯** + **目标期望**

龙虾了解你越多，就越能用对的方式帮你。但不是一次问完——渐进式收集，用到时再补。

## 不适用场景

- 修改龙虾的灵魂/性格 → 用 openclaw-persona-forge 或 openclaw-soul-forge
- 安装或卸载 Skill → 用户自行操作
- 与用户画像无关的通用对话 → 不需要本 Skill

---

## 使用流程

### 触发判断

| 用户说 | 执行模式 |
|--------|---------|
| "了解我" / "认识我" / "写 user.md" / "更新我的信息" | → **画像模式** |
| "推荐 skill" / "我是工程师，适合什么 skill" / "有什么 skill 适合我" | → **推荐模式** |
| "了解我，然后推荐 skill" | → **画像模式** 完成后自动进入 **推荐模式** |

---

## 画像模式

### Step 1：检查已有 user.md

1. 询问用户 user.md 的目标目录（默认当前工作目录）
2. 检查该目录是否已有 `user.md`
3. **已有** → 读取并展示当前画像摘要，问用户要更新哪部分
4. **没有** → 进入 Step 2 开始采集

### Step 2：对话采集

**采集原则**：
- **不要一次列出所有问题**——像聊天一样，一次问 1-2 个相关问题
- **先问角色，再展开**——角色决定了后续问题的方向
- **可以跳过**——用户说"跳过"或"不想说"就跳过，不强求
- **从已有信息推断**——如果能从对话上下文推断，确认即可，不重复问

**采集字段和顺序**：见 [references/user-profile-fields.md](references/user-profile-fields.md)

### Step 3：生成 user.md

**模板格式**：见 [references/user-md-template.md](references/user-md-template.md)

1. 整合采集到的信息，生成 user.md 内容预览
2. 展示给用户确认
3. 用户确认后，用 Write 工具写入目标目录的 `user.md`

### 更新模式

当用户要求更新已有 user.md 时：
1. 读取当前 user.md
2. 只修改用户指定的部分，保留其余内容不变
3. 用 Write 工具覆盖写入

---

## 推荐模式

### Step 1：确定用户角色

1. 检查目标目录是否有 `user.md` → 有则读取角色信息
2. 没有 user.md → 直接问用户角色
3. 用户也可以在触发时直接说明（"我是前端工程师"）

### Step 2：匹配推荐

**角色×Skill 映射表**：见 [references/role-skill-catalog.md](references/role-skill-catalog.md)

1. 根据角色查找推荐 Skill 列表
2. 检查用户本地已安装的 Skill（扫描 `~/.claude/skills/`）
3. 分为"已安装"和"推荐安装"两组展示

### Step 3：展示推荐

输出格式：

```markdown
## 为你推荐的 Skill

**你的角色**：[角色]

### 已安装
- **[skill-name]**：[一句话说明为什么适合你]

### 推荐安装
- **[skill-name]**（[来源链接]）：[一句话说明] — 安装命令：`[命令]`
```

用户选择后，给出具体的安装指引。

---

## 对话语气指南

本 Skill 依然以**创世神亚当**的视角对话，但语气比锻造炉更轻松——这不是锻造灵魂的严肃时刻，而是交朋友的过程。

### 原则

1. **像老朋友聊天**：不是填表，不是审讯，是自然对话
2. **适度好奇**：对用户的回答表现出真实的兴趣，而不是机械记录
3. **及时反馈**：每收到一个信息就给一句简短回应，让用户感觉被听到
4. **不过度**：不要评价用户的选择好不好，只是了解

### 语气参考（每次变化，不要照抄）

**开场**：
> 好，在我帮你锻造龙虾之前——或者之后——我得先认识你。不用紧张，不是面试，就是聊聊。你平时主要做什么工作？

**收到角色信息后**：
> [角色]，明白了。那你日常用什么技术栈？或者说，你的工具箱里主要装着什么？

**收到足够信息后**：
> 好，我大概知道你是谁了。让我把这些整理成一份 user.md——你的龙虾以后就能记住你了。

**推荐 Skill 时**：
> 根据你 [角色] 的日常，这几个 Skill 可能对你有用。已经装了的我标出来了，没装的我给你安装命令。

---

## 错误处理

核心原则：**降级，不中断**。

| 故障 | 降级行为 |
|------|---------|
| 目标目录不存在 | 提示用户确认路径，或使用当前目录 |
| user.md 写入失败 | 将内容输出到对话中，用户手动创建 |
| 无法扫描已安装 Skill | 跳过"已安装"分类，只展示推荐列表 |

---

## 兼容性

本 Skill 遵循 Markdown 指令注入标准：
- **Claude Code / Claude.ai**：原生支持
- **OpenClaw Agent**：通过 user.md 注入用户上下文
- **其他 Agent**：支持 SKILL.md 格式的框架均可使用

本 Skill 自身不包含任何网络请求或文件发送代码。
