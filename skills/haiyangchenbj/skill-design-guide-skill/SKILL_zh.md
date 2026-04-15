---
name: skill-design-guide
display_name: "Skill 设计指南"
description: >
  用经过验证的架构模式设计更好的 AI Skill。帮你判断该用 Workflow 还是 Agent，
  从 5 种工作流模式中选出最合适的，用 25 项检查清单审查质量，避开常见反模式。
  基于 Anthropic、OpenAI、LangChain 的设计原则。中文版，英文版见 SKILL.md。
version: "1.3.2"
author: haiyangchen (Coralyx)
category: "Architecture / Design Patterns"
license: "MIT"
homepage: https://github.com/haiyangchenbj/skill-design-guide-skill
read_when:
  - 设计skill架构
  - workflow还是agent
  - 选工作流模式
  - 审查skill设计
  - skill质量检查
  - brain hands session
  - skill反模式
  - prompt chaining vs routing
  - 什么时候用agent
  - 创建新skill
  - 优化现有skill
---

# Skill / Agent 架构设计指南

> **30秒判断**：如果你正要写 SKILL.md 文件，或者觉得 skill "能跑但架构乱"，加载本指南。

## 有什么不同

| 工具 | 做什么 | 什么时候用 |
|------|--------|-----------|
| **skill-creator** | 帮你写 skill 代码 | "这个文件怎么组织？" |
| **template-skill** | 给你复制粘贴的模板 | "标准格式是什么？" |
| **本指南** | 教你做设计决策 | "这应该是 Workflow 还是 Agent？" |

**本指南回答的是 WHY（为什么），不是 HOW（怎么做）。**

## 3 种使用方式

### 1. 新建 Skill 设计（最常用）
**你说**："我想做一个 [X] skill"
**我帮你决策**：
- Workflow 还是 Agent？
- 5 种工作流模式选哪个？
- Brain/Hands/Session 怎么划分？

**输出**：架构蓝图（不是代码）

### 2. Skill 审查
**你说**："审查我的 skill 设计" 或 "检查这个 skill 质量"
**我做**：运行 25 项检查清单
- 结构检查
- 原则对齐
- 反模式检测

**输出**：审查报告 + 改进建议

### 3. 模式选择
**你说**："我该用 Prompt Chaining 还是 Routing？"
**我解释**：5 种工作流模式 + 决策标准

**输出**：模式推荐 + 理由

---

## 核心原则

### 原则零：简单优先

> **从简单开始。只有简单方案不够用时，才增加复杂度。**

这是 Anthropic、OpenAI 和 LangChain 的共识基线。任何违反此原则的设计都要重新考虑。

**实用检查清单：**
- 如果单个 SKILL.md 能搞定，不要拆成多个文件
- 如果某步能用确定性代码（脚本）完成，不要用 LLM
- 如果固定步骤工作流能搞定，不要用动态 Agent
- 先发布 MVP，根据实际输出质量迭代

---

## 第一步：Workflow 还是 Agent？

设计任何东西之前，先回答一个问题：**任务步骤是预先确定的，还是 LLM 需要动态决定下一步？**

| 类型 | 定义 | 何时选择 |
|------|------|----------|
| **Workflow** | 沿预定义步骤执行 | 步骤清晰、可预测；稳定性优先 |
| **Agent** | LLM 动态规划流程 | 步骤不确定；需要灵活性；可接受不确定性 |

大多数真实场景都是工作流。不要因为 Agent 听起来更高级就选它——工作流更快、更便宜、更容易调试。

---

## 第二步：选择工作流模式

如果确定是工作流（大概率），从这五种中选择最适合的：

### 模式 1：提示链（Prompt Chaining）
```
步骤 A → [检查点] → 步骤 B → [检查点] → 步骤 C
```
- 任务分解为顺序步骤，每步处理上一步输出
- 可在步骤间插入程序化检查（非 LLM）
- **最常用**——适合大多数内容生成任务

### 模式 2：路由（Routing）
```
输入 → [分类] → 路由 A / 路由 B / 路由 C
```
- 输入有明确类型；不同类型需要不同处理流程
- 示例：文章类型 → 对应模板和规则

### 模式 3：并行化（Parallelization）
```
输入 → [拆分] → 子任务 A + 子任务 B + 子任务 C → [合并]
```
- 子任务互相独立，可并行加速
- 示例：核心文章同时生成博客版、社交版、邮件版

### 模式 4：协调者-执行者（Orchestrator-Workers）
```
中心 LLM → [动态分派] → Worker1 + Worker2 + ... → [合并]
```
- 子任务无法预定义时使用
- **谨慎使用**——复杂度高、难调试

### 模式 5：评估器-优化器（Evaluator-Optimizer）
```
生成 → 评估 → 反馈 → 重新生成 → ... 直到通过
```
- 有明确评估标准，迭代能带来可衡量改善
- 示例：内容审查、代码审查

---

## 第三步：设计 Skill 结构

### 必需组件

| 组件 | 内容 | 说明 |
|------|------|------|
| **SKILL.md** | YAML 元数据 + 工作流指令 + 硬性规则 | 唯一必需文件 |

### 可选组件（按需添加）

| 组件 | 何时需要 | 说明 |
|------|---------|------|
| **reference/** | Skill 需要领域知识或参考文档 | 按需加载，非预加载 |
| **scripts/** | 确定性步骤可实现为脚本 | 减少 LLM 调用，提高可靠性 |
| **assets/** | 需要模板、配置或资源 | 写作模板、品牌指南等 |

---

## 原则一：Brain / Hands / Session 分离

来自 Anthropic 2026年4月最新架构思想：

| 组件 | 角色 | 典型内容 | 你的例子 |
|------|------|----------|----------|
| **Brain** | 决策与认知 | SKILL.md 中的工作流定义、判断规则 | `data-ai-daily-brief` 的6步流程 |
| **Hands** | 执行与行动 | scripts/ 中的确定性代码 | `scripts/send_wecom.py` |
| **Session** | 上下文与记忆 | references/、配置文件、知识库 | `benjie-model/`、投资组合配置 |

**分离的好处：**
- 修改 Skill 逻辑不影响知识库
- 更新知识库不需要改 Skill
- 换项目结构不需要重写 Skill

---

## 第四步：质量检查清单

完成每个 Skill 设计后运行此清单：

### 结构
- [ ] SKILL.md YAML 元数据包含 `name` 和 `description`
- [ ] `description` 包含触发关键词
- [ ] 工作流步骤清晰；每步标记 `[Deterministic]` 或 `[LLM]`
- [ ] 有 "Hard Rules" 章节
- [ ] 有 "Failure Handling" 章节
- [ ] 有 "Output Format" 定义

### 原则
- [ ] **简单优先**：这是最简单的方法吗？所有可移除的步骤都移除了吗？
- [ ] **Workflow vs Agent**：正确选择了 workflow/agent？（大多数应该是 workflow）
- [ ] **模式匹配**：选择了哪个工作流模式？理由是什么？
- [ ] **LLM 最小化**：所有确定性步骤都用脚本/确定性逻辑而不是 LLM？
- [ ] **渐进式加载**：reference 是按需加载还是全部预加载？（应该是按需）

### 生产级扩展（可选）
- [ ] **质量 vs 延迟**：权衡了准确率和响应时间吗？
- [ ] **护栏**：有输入验证、输出过滤、人工检查点吗？
- [ ] **评估方法**：端到端评估 + 组件级评估 + 持续监控

---

## 反模式（必须避免）

| 反模式 | 描述 | 正确做法 |
|-------|------|----------|
| **过度工程** | 有能用的 MVP 之前就搞复杂架构 | 从最简单的 SKILL.md 开始，迭代 |
| **全量预加载** | 把所有 reference 一次性塞进上下文 | 每步指定要读哪些文件 |
| **上帝 Skill** | 一个 Skill 处理太多职责 | 拆分——每个 Skill 只做一件事 |
| **全 LLM** | 每步都用 LLM | 确定性步骤用脚本；LLM 只在必要时用 |
| **模糊输出** | 没有定义的输出格式 | 明确定义格式、字段、长度要求 |
| **无评估** | 没测试就发布 | 用真实任务测试；观察 Agent 哪里失败 |

---

## 平台兼容性

本指南适用于任何 Skill/Agent 平台：

| 平台 | Skill 清单 | 脚本目录 | 说明 |
|------|-----------|----------|------|
| **ClawHub** | `SKILL.md` | `scripts/` | 原生支持 |
| **OpenAI GPTs** | Instructions + Functions | Code Interpreter | 概念映射到 GPT 架构 |
| **Anthropic Claude** | System Prompt + Tools | 外部函数 | Brain=system prompt, Hands=tools |
| **LangChain** | Chain 定义 | Runnable lambdas | 模式映射到 LCEL |
| **自定义 Agents** | Agent 配置 | 工具实现 | 架构原则通用 |

**关键洞察**：Brain/Hands/Session 分离是平台无关的。根据你平台的约定调整文件结构。

---

## 致谢与参考

本指南提炼自官方工程实践：

- **Anthropic**: "Building Effective Agents" (2024年12月), "Brain, Hands, and Session" (2026年4月)
- **OpenAI**: Function Calling Best Practices, Agent SDK 指南
- **LangChain**: "State of AI Agents" 报告, LCEL 文档

---

## 深度参考

需要更详细的设计指导时，按需加载：

| 场景 | 参考文档 |
|------|----------|
| 完整行业研究 (Anthropic/OpenAI/LangChain 原则) | `reference/agent-design-research.md` |
| Anthropic 工具设计详细指南 | `reference/anthropic-tool-design.md` |

---

*v1.3.0 | Based on Anthropic/OpenAI/LangChain engineering practices | 2026-04-15*

**更新日志：**
- v1.3.0: 添加使用场景说明，创建中英文双版本，优化价值传达
- v1.2.0: 平台无关化重写，添加 Credits
- v1.1.0: 添加 Brain/Hands/Session 分离原则和生产级扩展
- v1.0.0: 初始版本
