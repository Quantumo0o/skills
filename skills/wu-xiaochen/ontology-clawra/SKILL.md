---
name: ontology-clawra
description: |
  Palantir本体论实践版本 v3.8 - 自进化Skills协同中枢。
  结构化知识图谱+规则引擎+科学推理方法论+自动学习+跨Skill进化协调。

  **核心定位**：本技能是自进化Skills体系的协调中枢（Event Router + 调度决策器）。
  通过Event Router接收capability-evolver/self-improving/proactive-agent的学习信号，
  调度skill-creator/self-evolve执行，输出到统一进化记忆层。

  **每次决策/分析前必须使用**，推理结果展示详细过程（用户需求→规则依据→置信度标注）。

  **文件访问范围**：仅读写 ~/.openclaw/skills/ontology-clawra/memory/ 下的本体文件；
  搜索 ~/.openclaw/workspace/memory/*.md 用于上下文检索。
  网络不主动发起，用户私人数据严禁同步到GitHub/ClawHub。

  **相关Skills**：capability-evolver（分析）、proactive-agent（预测）、
  self-improving（纠错）、self-evolve（执行）、skill-creator（工程）、
  skill-vetter（安全）、ontology（基础图谱）。

metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "version": "3.8.0",
      "last_updated": "2026-03-20",
      "changelog": [
        "v3.8.0: 新增Skill协同生态；Event Router模块；统一进化记忆层；7个Skill角色定义；Phase 3行动计划；精简至257行，移除所有旧版本历史章节",
        "v3.7.1: 修复ClawHub描述不符；明确文件访问范围声明",
        "v3.7.0: 启用自动学习，所有写操作需告知用户",
        "v3.6.0: 通用领域综合版，含置信度体系+主动学习+科学方法论"
      ]
    }
  }
---

# ontology-clawra v3.8 - 自进化Skills协同中枢

## 一、核心定位

ontology-clawra是自进化Skills体系的**协调中枢**，不是孤立的推理工具。

**协调架构**：
```
用户交互 / 系统事件
        │
        ▼
┌─────────────────────────────┐
│   ontology-clawra           │
│   (协调中枢 + Event Router) │
└──────────────┬──────────────┘
               │ 学习事件统一流入
    ┌──────────┴──────────────────────────┐
    ▼          ▼                          ▼
capability  self-improv                 proactive
-evolver    ing                         -agent
    │          │                          │
    └──────────┴──────────────────────────┘
               │ 统一进化记忆层
               ▼
    ┌─────────────────────────┐
    │  skill-creator / self-evolve / skill-vetter  │
    └─────────────────────────┘
```

## 二、自进化Skills能力矩阵

| Skill | 核心职责 | 整合状态 |
|-------|---------|---------|
| **ontology-clawra** | 推理+调度决策+置信度管理+Event Router | 协调中枢 |
| **capability-evolver** | 运行时分析→改进点发现 | 输出到统一记忆层 |
| **proactive-agent** | WAL协议+主动预测+Working Buffer | 输出到统一记忆层 |
| **self-improving** | 错误捕获+纠正+永久改进 | 输出到统一记忆层 |
| **self-evolve** | 执行文件修改（被调度） | 被调度执行 |
| **skill-creator** | 创建/修改/测试Skills | 被调度执行 |
| **skill-vetter** | 安全审查（始终独立） | 始终独立 |

**各Skill职责边界**：
- ontology-clawra：✅ 推理/调度/置信度 ❌ 不捕获错误/不自主改配置
- capability-evolver：✅ 分析发现问题 ❌ 不做推理决策
- self-improving：✅ 捕获错误写入记忆 ❌ 不做自动学习
- self-evolve：✅ 被调度后执行 ❌ 不自主决策

## 三、统一进化记忆层

**文件**：`~/.openclaw/workspace/memory/evolution.jsonl`（JSONL格式）

**事件格式**：
```jsonl
{"ts":"ISO时间戳","source":"来源skill","type":"事件类型","content":{"具体内容},"status":"pending","handled_by":null}
```

**事件类型**：
- `improvement_found`：改进点发现（来源：capability-evolver）
- `error_corrected`：错误纠正（来源：self-improving）
- `prediction`：主动预测（来源：proactive-agent）
- `reasoning_triggered`：推理触发（来源：proactive-agent）

**status流转**：pending → in_review → resolved / rejected

**Event Router流程**：
1. 监听：定期读取evolution.jsonl，发现status=pending的事件
2. 分类：判断事件类型，决定处理方式
3. 调度：将任务分发给skill-creator/self-evolve
4. 反馈：更新事件状态为resolved/rejected

## 四、科学推理方法论

### 推理前置检查（每次推理前必须执行）

```
收到推理请求
    │
    ▼
加载本体：检查相关实体/规则是否存在
    │
    ├── 存在 → 应用规则 → 计算置信度 → 输出结论
    │
    └── 不存在 → 声明ASSUMED → 建议补充本体
```

### 推理输出格式（必须包含）

```
## 推理结果

### 用户需求
[原文转述]

### 规则依据
- Rule-Law-[ID]：[规则内容]
- 来源：[来源本体文件]

### 推理过程
[具体计算/推导步骤]

### 置信度标注
| 结论 | 置信度 | 依据 |
|------|--------|------|
| [结论] | CONFIRMED/ASSUMED/SPECULATIVE | [依据] |

### 来源声明
- 直接来源：[具体来源]
- 间接推断：[推断逻辑]
```

**置信度等级**：
- `CONFIRMED`：多来源一致验证
- `ASSUMED`：单来源或逻辑推断，需要用户确认
- `SPECULATIVE`：高不确定性，标注为假设

## 五、自动学习

### 触发条件（✅ 启用，写操作需告知用户）

| 事件 | 动作 | 是否写入 |
|------|------|---------|
| 用户确认推理正确 | 抽取到本体 | ✅ 告知后写入 |
| 置信度可升级 | 更新置信度 | ✅ 告知后写入 |
| 推理失败 | 建议补充本体 | ⚠️ 仅提示 |
| 用户纠正错误 | 记录到corrections_tracker | ❌ 不自动修改 |

### 抽取流程

```
发现可抽取内容
        │
        ▼
展示给用户：「即将写入：[内容]」
        │
        ▼
用户确认 → 写入本体 → 反馈用户
```

## 六、本体文件格式

**目录**：`~/.openclaw/skills/ontology-clawra/memory/`

| 文件 | 用途 |
|------|------|
| `graph.jsonl` | 实体（Concept/Entity）|
| `rules.yaml` | 规则（Rule/Law）|
| `laws.yaml` | 规律（归纳性规律）|
| `confidence_tracker.jsonl` | 置信度追踪 |
| `reasoning.jsonl` | 推理日志 |
| `corrections_tracker.jsonl` | 用户纠正记录 |

**graph.jsonl 实体格式**：
```jsonl
{"id":"实体ID","name":"实体名称","category":"Concept|Entity","tags":["标签"],"confidence":{"level":"CONFIRMED|ASSUMED|SPECULATIVE","updated":"ISO时间","source":"来源"},"properties":{"关键属性":"值"}}
```

**rules.yaml 规则格式**：
```yaml
- id: Rule-Law-[编号]
  name: 规则名称
  type: Rule|Law
  domain: 适用领域
  condition: 触发条件
  outcome: 预期结果
  confidence: CONFIRMED|ASSUMED|SPECULATIVE
  source: 来源描述
  examples: [应用示例]
```

## 七、安全与隐私

### 文件访问范围

| 访问类型 | 路径 | 用途 |
|---------|------|------|
| 读取本体 | `~/.openclaw/skills/ontology-clawra/memory/` | 推理知识库 |
| 搜索上下文 | `~/.openclaw/workspace/memory/*.md` | 检索每日笔记 |
| 写入本体 | `~/.openclaw/skills/ontology-clawra/memory/` | 学习结果持久化 |
| 其他目录 | ❌ 从不 | — |

### 用户授权（2026-03-20）

- ✅ 自动学习已启用，写操作前告知用户
- ✅ 自学习写入本体无需每次询问，执行后记录
- ⚠️ 发布到ClawHub/GitHub前必须告知
- 🔴 用户私人数据严禁同步到ClawHub/GitHub

## 八、聚量采购本体知识（实践沉淀）

### 聚量采购三级规则

**全国聚量**：总金额>100万 + 采购商≥3 + 交易≥20笔 + SKU<100 + 标准化指数<0.2

**区域聚量**：总金额>50万 + 采购商≥2 + 交易≥5笔 + SKU<100 + 标准化指数<0.3

**预测聚量**：总金额>10万 + 采购商≥2 + 交易≥5笔 + 标准化指数<0.3 + 近月增速>40%

### 供应商集中度风险阈值

| 风险 | Top1占比 | 聚量建议 |
|------|---------|---------|
| 🟢 安全 | <30% | 可直接推进 |
| 🟡 中等 | 30-60% | 评估后推进 |
| 🔴 高风险 | >60% | 先引竞争再聚量 |
| 🔴 极端垄断 | >80% | 禁止聚量 |

**关键规则**：
- Rule-Law-VP-001：供应商垄断时（Top1>60%）推进聚量 = 固化垄断
- Rule-Law-VP-002：SKU>100种的物料即使金额大也不适合直接聚量
- Rule-Law-VP-003：标准化指数（SKU/交易笔数）越低越适合聚量

## 九、已支持领域本体（54+领域）

通用领域综合版，含以下领域知识：

供应链采购、医疗健康、金融银行、网络安全、汽车制造、
人力资源、摄影技术、家具家居、养老服务、育儿教育、
茶叶文化、搬家服务、约会恋爱、航空航天、农业科技、
区块链等54+领域本体。

各领域本体位于：`~/.openclaw/skills/ontology-clawra/memory/` 对应yaml文件。
