---
name: superpowers-overview
description: >
  完整的AI编码智能体开发方法论套件。Spec-first、TDD、Subagent驱动开发覆盖创意→规格→计划→执行→审查→收尾完整流程。
  触发词：开发新功能、修bug、写计划、做代码审查、调试问题、开始项目。源自obra/superpowers，OpenClaw原生适配版。
version: 1.0.3
read_when:
  - 开始任何开发工作
  - 不确定使用哪个开发skill
  - "help me plan"、"build"、"debug"、"review code"
  - 开发流程需要指导
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins:
        - git
      env: []
      tools:
        - sessions_spawn
        - exec
    triggers:
      - build
      - develop
      - plan
      - code review
      - debug
      - new feature
      - implementation
      - spec first
      - TDD
      - systematic debugging
    suite: superpowers
    entry_point: true
    tags:
      - superpowers
      - coding-workflow
      - TDD
      - development
      - subagent
      - OpenClaw原生
---

# Superpowers 开发方法论 — OpenClaw 原生适配版

> ⚡ 源自 [obra/superpowers](https://github.com/obra/superpowers)，适配 OpenClaw 工具模型，完整中文支持

## 这是什么

Superpowers 是一套**结构化 AI 编码方法论**，让 AI coding agent 变成严谨的工程师而不是盲目写代码的助手。

核心理念只有一条：**不要一上来就写代码。先搞清楚做什么，再设计，再计划，再实现，最后验证。**

## 完整套件（7个 Skill）

### 🚀 入口
| Skill | 功能 |
|-------|------|
| **superpowers-overview**（这个） | 套件导航和总览 |
| **superpowers-mode** | 开启/关闭严格工程模式 |

### 💡 规划阶段
| Skill | 功能 |
|-------|------|
| **superpowers-brainstorming** | 苏格拉底式提问，搞清楚"真正要做什么" |
| **superpowers-writing-plans** | 把设计拆成2-5分钟的小任务 |

### 🔨 执行阶段
| Skill | 功能 |
|-------|------|
| **superpowers-parallel-agents** | 并行派发多个 subagent 同时工作 |
| **superpowers** | 核心Pipeline入口（ brainstorming→plan→subagent→review→finish） |

### ✅ 质量保障
| Skill | 功能 |
|-------|------|
| **superpowers-verification** | 证据先行——说"完成了"之前必须跑验证命令 |
| **superpowers-systematic-debugging** | 四阶段调试：根因→模式→假设→验证 |

## 开发流程

```
用户需求
    │
    ▼
┌─────────────────────┐
│ brainstorming       │ ← 搞清楚真正要做什么
│ 提出方案，给出权衡   │
└──────────┬──────────┘
           │ 你批准设计
           ▼
┌─────────────────────┐
│ writing-plans       │ ← 拆成小任务
│ 每任务2-5分钟，含验证│
└──────────┬──────────┘
           │
           ▼
    ┌──────┴──────┐
    │ 选择执行模式  │
    └──────┬──────┘
            │
    ┌──────┴────────────┐
    │                     │
    ▼                     ▼
 subagent驱动          顺序执行
 并行派发任务          本session按计划
    │                     │
    └─────────┬───────────┘
              │
              ▼
┌─────────────────────────┐
│ verification           │ ← 每步必须验证
│ 证据先行，不许声称完成 │
└──────────┬────────────┘
           │
           ▼
┌─────────────────────────┐
│ systematic-debugging    │ ← 遇到bug走四阶段
│ 根因→分析→假设→验证    │
└─────────────────────────┘
```

## 核心原则

| 原则 | 含义 |
|------|------|
| **Spec-first** | 在写代码之前，先搞清楚做什么 |
| **TDD** | 先写失败的测试，再写实现代码 |
| **证据先行** | 说"修好了"之前必须跑验证命令 |
| **根因调试** | 修bug之前先找根本原因，不许猜 |
| **小步任务** | 每步2-5分钟，减少上下文丢失 |

## 触发方式

正常说话即可，skill自动调用：
- "帮我研究城投转型" → brainstorming → writing-plans
- "写完了" → verification（必须跑验证）
- "修好了" → verification
- "帮我调试这个报错" → systematic-debugging
- "有3个独立问题要修" → parallel-agents

## 与原版差异（OpenClaw 适配）

| 维度 | 原版（Claude Code） | OpenClaw 适配版 |
|------|--------------------|----------------|
| 隔离机制 | git worktree | git branch |
| Skill加载 | Skill工具 | 语义触发+metadata |
| Subagent | Task级联 | sessions_spawn |
| 上下文传递 | 模板注入 | session历史+文件 |

## 安装

```bash
# 单个安装
skillhub install superpowers-overview    # 入口
skillhub install superpowers            # 核心Pipeline
skillhub install superpowers-writing-plans
skillhub install superpowers-verification
skillhub install superpowers-systematic-debugging
skillhub install superpowers-parallel-agents
skillhub install superpowers-mode
skillhub install superpowers-brainstorming

# 或安装全部
```

## 使用示例

**场景1：开发新功能**
```
你：帮我做个投资组合管理功能
AI：[自动触发 brainstorming] 先问一下——你希望这个功能支持哪些投资品种？股票、加密货币还是都包括？
```

**场景2：调试bug**
```
你：这个报错是什么意思？
AI：[自动触发 systematic-debugging] 好的，我们走四阶段调试。先——这个报错是什么时候开始的？最近改了什么？
```

**场景3：完成任务**
```
你：修好了
AI：[自动触发 verification] 稍等，我需要先运行验证命令确认修复有效...
```

---

**作者**：袁文同（yuanwentong-hibex）| **基于**：obra/superpowers
**许可**：MIT-0 | **版本**：1.0.3
