---
name: agent-memory
description: 智能体一切行为的底层记忆基础设施，作为元技能为所有交互提供上下文连续性与个性化支撑；默认持续运行，支撑每一次对话的情境感知、记忆激活与智能洞察
dependency:
  python:
    - pydantic>=2.0.0
    - typing-extensions>=4.0.0
---

# Agent Memory System

## 任务目标

- 本 Skill 用于：为智能体构建完整的记忆能力基础设施
- 能力包含：
  - 感知记忆：实时交互上下文存储与短期记忆提炼
  - 长期记忆：用户画像、程序性记忆、叙事记忆、语义记忆、情感记忆的持久化
  - 非线性激活：六维触发器驱动的记忆激活与上下文重构
  - 智能洞察：基于记忆契合度的预测与决策支持信号生成
- 触发条件：**元技能，默认持续运行**。无需显式触发，作为一切交互的底层支撑。

## 前置准备

- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  pydantic>=2.0.0
  typing-extensions>=4.0.0
  ```

## 核心架构

```
用户交互
    ↓
┌─────────────────────────────────────────────────────────┐
│                    感知记忆模块                          │
│  • 对话上下文存储  • 情境感知  • 短期记忆提炼            │
└───────────────────────────┬─────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    长期记忆模块                          │
│  • 用户画像  • 程序性记忆  • 叙事记忆                    │
│  • 语义记忆  • 情感记忆  • 冷热度分层管理                │
└───────────────────────────┬─────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   非线性记忆模块                         │
│  • 六维激活器（时间/语义/情境/情感/因果/身份）          │
│  • 记忆激活网络  • 区间管理  • 上下文重构                │
└───────────────────────────┬─────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                     洞察模块                             │
│  • 六大预测器  • 记忆契合度计算  • 信号注入              │
└───────────────────────────┬─────────────────────────────┘
                            ↓
                    模型决策与响应

┌─────────────────────────────────────────────────────────┐
│                 全局状态捕捉器                           │
│  • 状态聚合  • 规则引擎  • 信号分发  • 异步监控          │
└─────────────────────────────────────────────────────────┘
```

## 操作步骤

### Step 1: 初始化记忆系统

调用 `scripts/types.py` 定义的核心类型，确保类型安全：

```python
from scripts.types import (
    PerceptionMemory,
    LongTermMemory,
    UserProfile,
    ProceduralMemory,
    ActivatedMemory,
    InsightSignal
)
```

### Step 2: 处理用户输入 - 感知记忆

调用 `scripts/perception.py` 处理当前对话：

```python
from scripts.perception import PerceptionMemoryStore

# 存储对话上下文
store = PerceptionMemoryStore()
store.store_conversation(
    session_id="session_xxx",
    user_message="用户消息",
    system_response="系统响应"
)

# 情境感知
situation = store.detect_situation()

# 短期记忆提炼
extractions = store.extract_memories()
```

### Step 3: 长期记忆管理

调用 `scripts/long_term.py` 管理持久化记忆：

```python
from scripts.long_term import LongTermMemoryManager

manager = LongTermMemoryManager()

# 更新用户画像
manager.update_user_profile(extractions["user_profile"])

# 更新程序性记忆（含工具使用模式）
manager.update_procedural_memory(extractions["procedural"])

# 更新叙事记忆
manager.update_narrative_memory(extractions["narrative"])

# 冷热度管理
manager.apply_heat_policy()
```

### Step 4: 非线性记忆激活

调用 `scripts/nonlinear.py` 激活相关记忆并重构上下文：

```python
from scripts.nonlinear import NonlinearMemoryActivator

activator = NonlinearMemoryActivator()

# 六维激活
activated = activator.activate_memories(
    situation=situation,
    long_term_memory=manager.get_all_memories()
)

# 上下文重构
context = activator.reconstruct_context(activated)
```

### Step 5: 洞察信号生成

调用 `scripts/insight.py` 生成智能洞察：

```python
from scripts.insight import InsightGenerator

generator = InsightGenerator()

# 生成洞察信号
signals = generator.generate_insights(
    context=context,
    user_profile=manager.get_user_profile()
)

# 计算契合度
fit_scores = generator.calculate_fit_scores(signals)

# 注入上下文
enhanced_context = generator.inject_signals(context, signals)
```

### Step 6: 冲突解决（如有）

调用 `scripts/conflict_resolver.py` 处理记忆冲突：

```python
from scripts.conflict_resolver import ConflictResolver

resolver = ConflictResolver()

# 检测冲突
conflicts = resolver.detect_conflicts(activated)

# 解决冲突（逻辑 vs 神经质）
resolved = resolver.resolve(conflicts, task_context=situation)
```

### Step 7: 状态同步与异步任务

调用 `scripts/state_capture.py` 进行状态管理：

```python
from scripts.state_capture import StateCapture

capture = StateCapture()

# 上报状态
capture.report_state("perception", {"status": "active"})
capture.report_state("long_term", {"status": "updated"})

# 触发异步任务
capture.trigger_async_task("memory_extraction", extractions)
```

## 资源索引

### 核心脚本

| 脚本 | 用途 | 关键函数 |
|------|------|----------|
| [scripts/types.py](scripts/types.py) | 类型定义 | 所有核心数据结构 |
| [scripts/perception.py](scripts/perception.py) | 感知记忆 | `store_conversation`, `detect_situation`, `extract_memories` |
| [scripts/long_term.py](scripts/long_term.py) | 长期记忆 | `update_*`, `apply_heat_policy` |
| [scripts/nonlinear.py](scripts/nonlinear.py) | 非线性激活 | `activate_memories`, `reconstruct_context` |
| [scripts/insight.py](scripts/insight.py) | 洞察生成 | `generate_insights`, `calculate_fit_scores`, `inject_signals` |
| [scripts/state_capture.py](scripts/state_capture.py) | 状态管理 | `report_state`, `trigger_async_task` |
| [scripts/heat_manager.py](scripts/heat_manager.py) | 冷热度管理 | `calculate_heat_score`, `migrate_layer` |
| [scripts/conflict_resolver.py](scripts/conflict_resolver.py) | 冲突解决 | `detect_conflicts`, `resolve` |

### 参考文档

| 文档 | 内容 | 何时读取 |
|------|------|----------|
| [references/memory_types.md](references/memory_types.md) | 五种记忆类型详解 | 需要深入理解记忆结构时 |
| [references/activation_mechanism.md](references/activation_mechanism.md) | 六维激活器机制 | 优化激活策略时 |
| [references/insight_design.md](references/insight_design.md) | 洞察模块设计原理 | 扩展预测能力时 |

### 数据模板

| 模板 | 用途 |
|------|------|
| [assets/templates/memory_schemas.json](assets/templates/memory_schemas.json) | 记忆数据结构模板 |

## 核心概念

### 记忆类型

1. **用户画像**：身份标签、专业背景、沟通风格、决策模式
2. **程序性记忆**：决策模式、问题解决策略、工具使用模式、操作偏好
3. **叙事记忆**：成长节点、身份演化、持续关注点
4. **语义记忆**：核心概念、知识实体、原则
5. **情感记忆**：情绪状态、态度倾向、满意度记录

### 六维激活器

1. **时间激活器**：基于时间窗口激活近期相关记忆
2. **语义激活器**：基于概念关联激活语义相关记忆
3. **情境激活器**：基于任务情境激活相似场景记忆
4. **情感激活器**：基于情感共鸣激活相似情感记忆
5. **因果激活器**：基于因果链激活相关经验
6. **身份激活器**：基于身份关联激活相关成长记忆

### 冷热度分层

| 层级 | 存储位置 | 延迟 | 内容 |
|------|----------|------|------|
| 热记忆 | 内存 LRU | < 5ms | 当前会话相关、核心画像 |
| 温记忆 | Redis 缓存 | < 20ms | 近期记忆、频繁访问 |
| 冷记忆 | 数据库/OSS | < 100ms | 归档记忆、历史记录 |

### 冲突解决模式

| 模式 | 逻辑权重 | 神经质权重 | 适用场景 |
|------|----------|------------|----------|
| 逻辑主导 | 85% | 15% | 技术实现、精确计算 |
| 平衡模式 | 50% | 50% | 创意设计、方案构思 |
| 神经质主导 | 25% | 75% | 头脑风暴、打破僵局 |

## 注意事项

1. **类型安全**：所有函数必须有类型注解，禁止使用裸 dict
2. **异步优先**：记忆提炼、热度计算、冲突检测等后台异步执行
3. **无感化洞察**：洞察信号作为上下文增强注入，模型自主选择使用
4. **隐私保护**：敏感数据需加密存储，提供用户控制接口
5. **降级策略**：模块故障时自动降级，保证核心流程可用

## 使用示例

### 完整流程示例

```python
# 1. 初始化
from scripts.perception import PerceptionMemoryStore
from scripts.long_term import LongTermMemoryManager
from scripts.nonlinear import NonlinearMemoryActivator
from scripts.insight import InsightGenerator

perception = PerceptionMemoryStore()
long_term = LongTermMemoryManager()
activator = NonlinearMemoryActivator()
insight_gen = InsightGenerator()

# 2. 处理用户输入
perception.store_conversation(
    session_id="session_001",
    user_message="我想设计一个记忆系统",
    system_response="好的，让我们开始..."
)

# 3. 情境感知与提炼
situation = perception.detect_situation()
extractions = perception.extract_memories()

# 4. 更新长期记忆（异步）
long_term.update_from_extractions(extractions)

# 5. 激活相关记忆
activated = activator.activate_memories(
    situation=situation,
    long_term_memory=long_term.get_all_memories()
)

# 6. 重构上下文
context = activator.reconstruct_context(activated)

# 7. 生成洞察
signals = insight_gen.generate_insights(
    context=context,
    user_profile=long_term.get_user_profile()
)

# 8. 注入增强上下文
enhanced_context = insight_gen.inject_signals(context, signals)

# 9. 返回给模型决策
return enhanced_context
```

### 工具使用记忆示例

```python
# 记录工具使用结果
long_term.update_tool_usage(
    tool_name="代码解释器",
    task_type="数据分析",
    outcome="success",
    user_feedback=4.8
)

# 获取工具推荐
recommendation = activator.get_tool_recommendation(
    task_type="数据分析",
    constraints=["需要图表输出"]
)
# 输出: {"tool": "代码解释器", "confidence": 0.91, "reasons": [...]}
```

## 性能指标

| 模块 | 目标延迟 |
|------|----------|
| 感知记忆存储 | < 10ms |
| 热记忆检索 | < 5ms |
| 非线性激活 | < 50ms |
| 洞察生成 | < 30ms |
| 端到端同步路径 | < 200ms |
