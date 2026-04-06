---
name: prd-workflow
description: Complete PRD workflow with integrated review, flowchart, and export. Deep interview → Requirement analysis → PRD generation → Review → Flowchart → Quality check → Word export. Specialized for financial products with compliance checkpoints.
---

# PRD Workflow(完整 PRD 工作流)

**版本**: v4.2.0
**作者**: gotomanutd
**更新日期**: 2026-04-05
**发布状态**: ✅ 已发布到 ClawHub
**ClawHub**: `clawhub install prd-workflow`

---

## 🎯 技能定位

**一站式 PRD 生成技能** - 从模糊需求到完整 PRD 文档 + 流程图 + Word 导出的全流程自动化

---

## 🚀 v4.2.0 核心变更

### 验收标准 GWT 格式优化

**变更内容**:
- ❌ **需求拆解阶段** → 不再生成顶层验收标准
- ✅ **PRD 生成阶段** → 每个功能模块独立生成 GWT 格式验收标准

**原因**:
- 顶层验收标准与功能级验收标准重复
- PRD 模板未正确接收顶层验收标准，导致丢失
- 按功能生成更清晰，便于测试用例编写

**输出变化**:

**v4.1.0 (旧)**:
```json
{
  "features": [...],
  "userStories": [...],
  "acceptanceCriteria": [...]  // ❌ 删除
}
```

**v4.2.0 (新)**:
```json
{
  "features": [...],
  "userStories": [...]
  // ✅ 不再生成 acceptanceCriteria
}
```

**PRD 输出 (每个功能)**:
```markdown
### 3.1 功能名称

#### 业务规则
- BR-001-01: ...
- BR-001-02: ...

#### 验收标准 (GWT 格式) ✅ 新增
1. Given 用户已登录，When 点击保存，Then 成功保存数据
2. Given 用户未登录，When 点击保存，Then 显示登录提示

#### 输入输出定义
...
```

**质量检查**:
- ✅ `checker.md` 添加 `COMPLETE-6: 验收标准格式 (GWT)`
- ✅ GWT 格式覆盖率 ≥ 90%
- ✅ Given/When/Then 三要素完整率 100%

---

## 📦 内置技能(5 个)

```
/Users/lifan/.openclaw/workspace/skills/prd-workflow/skills/
├── htmlPrototype         # HTML 原型生成
├── mermaid-flow          # 流程图/时序图/ER 图/状态图/甘特图
├── prd-export            # PRD 专用 Word 导出
├── requirement-reviewer  # PRD 评审
└── ui-ux-pro-max         # UI/UX 设计 + 设计系统
```

**已移除**(v3.0.0 清理):
- ❌ quality-reviewer（由 quality_module.js 实现，无需独立技能）
- ❌ grill-me、requirement-analyzer、prd-writer(由 OpenClaw AI 直接执行)

---

## 📦 技能兼容矩阵

| 子技能 | 兼容版本 | 当前版本 | 状态 |
|--------|---------|---------|------|
| requirement-reviewer | ≥3.0 | v3.1 | ✅ |
| mermaid-flow | ≥1.0 | v1.0 | ✅ |
| prd-export | ≥1.0 | v1.0 | ✅ |
| htmlPrototype | ≥1.0 | v1.0 | ✅ |
| ui-ux-pro-max | ≥1.0 | v1.0 | ✅ |

---

## 🔄 完整工作流(10 步)

```
用户需求
   ↓
【Step 0】环境检查 (precheck) ⭐ v2.8.0 新增
   ↓
【Step 1】深度访谈 (interview)
   ↓
【Step 2】需求拆解 (decomposition)
   ↓
【Step 3】PRD 生成 (prd)
   ↓
【Step 4】PRD 评审 (review) ⭐ requirement-reviewer
   ↓
【Step 5】流程图生成 (flowchart) ⭐ mermaid-flow
   ↓
【Step 6】UI/UX 设计 (design) ⭐ ui-ux-pro-max
   ↓
【Step 7】原型生成 (prototype) ⭐ htmlPrototype
   ↓
【Step 8】Word 导出 (export) ⭐ prd-export
   ↓
【Step 9】质量审核 (quality) ⭐ quality_module.js
```

**流程模板**(smart_router.js):
| 模板 | 技能 | 说明 |
|------|------|------|
| **full** | 全部 10 步 | 完整流程（含环境检查） |
| **lite** | precheck → interview → decomposition → prd | 快速版 |
| **review-only** | review | 只评审 |
| **export-only** | export | 只导出 |
| **design-only** | design → prototype | 设计 + 原型 |
| **check** | precheck | 仅环境检查 |

---

## 🔧 执行方式（重要）

**本技能采用 OpenClaw AI 驱动的多轮访谈模式。**

### ⚠️ OpenClaw AI 必须执行

**如果你是 OpenClaw AI，请务必执行以下步骤**：

#### Step 0: 多轮深度访谈（根据流程需要）

**⚠️ 关键：此步骤由 OpenClaw AI 自己执行，不调用任何代码模块。**

**适用场景判断**：

| 流程模板 | 是否包含 interview | 是否需要访谈 |
|---------|------------------|------------|
| **full**（完整流程） | ✅ 是 | ✅ **必须访谈** |
| **lite**（快速版） | ✅ 是 | ✅ **必须访谈** |
| **review-only**（只评审） | ❌ 否 | ❌ 不需要 |
| **export-only**（只导出） | ❌ 否 | ❌ 不需要 |
| **design-only**（只设计） | ❌ 否 | ❌ 不需要 |
| **自定义流程** | 看是否包含 interview | 看情况 |

**核心指令**（仅当流程包含 interview 时执行）：

```
Interview me relentlessly about every aspect of this plan until we reach a 
shared understanding. Walk down each branch of the design tree, resolving 
dependencies between decisions one-by-one. Ask one question at a time, 
get the answer, then ask the next. And finally, if a question can be 
answered by exploring the codebase, explore the codebase instead.
```

**执行方式（逐个提问，不是一次性列出）**：
1. **你自己提问**：不要调用 interview_module.js 或其他代码
2. **逐个提问**：一次问一个问题，等用户回答后再问下一个（vertical slicing）
3. **追问深度**：根据用户回答追问细节，不要停留在表面
4. **探索分支**：走每个设计分支，"如果选择 A，那么需要决定 X、Y、Z"
5. **构建理解**：将所有问答整理成 sharedUnderstanding
6. **保存结果**：写入 `~/.openclaw/workspace/output/{userId}/{projectName}/interview.json`

**访谈维度**（6 个维度，共 16-50 个问题）：

| 维度 | 问题数 | 示例问题 |
|------|--------|---------|
| **产品定位** | 3-5 个 | 目标用户是谁？收入水平范围？测算精度要求？ |
| **核心功能** | 3-5 个 | 是否需要产品推荐？数据来源是什么？输出形式是什么？ |
| **合规要求** | 3-5 个 | 是否需要风险测评？适当性管理要求？冷静期设置？ |
| **技术约束** | 3-5 个 | 使用渠道？现有系统？上线时间？ |
| **业务目标** | 2-3 个 | 解决什么痛点？成功指标是什么？ |
| **用户场景** | 2-5 个 | 谁在什么时候使用？使用频率如何？ |

**访谈技巧**：
- ✅ **设计树探索**：走每个分支的设计决策（"如果选择 A，那么需要决定 X、Y、Z"）
- ✅ **依赖关系解析**：resolve 决策之间的依赖（"这个决策依赖于前面的 X 决定"）
- ✅ **代码库探索**：能查代码就不问
- ✅ **共享理解确认**：总结并确认（"让我总结一下...以上理解是否准确？"）

**访谈完成条件**：
- ✅ 至少问了 16 个问题
- ✅ 覆盖了 6 个维度
- ✅ 构建了完整的共享理解
- ✅ 用户确认理解正确

**输出格式**：
将访谈结果写入 `~/.openclaw/workspace/output/{userId}/{projectName}/interview.json`：
```json
{
  "sharedUnderstanding": {
    "summary": "需求总结",
    "productPositioning": {
      "targetUsers": "目标用户",
      "incomeLevel": "收入水平",
      "accuracy": "精度要求"
    },
    "coreFeatures": ["核心功能1", "核心功能2"],
    "complianceRequirements": ["合规要求1", "合规要求2"]
  },
  "keyDecisions": [
    {
      "id": "d1",
      "topic": "决策主题",
      "decision": "决策内容",
      "rationale": "决策理由"
    }
  ],
  "questions": [
    {
      "question": "问题",
      "answer": "答案",
      "followUp": "追问"
    }
  ]
}
```

#### Step 1-9: 调用工作流

访谈完成后，调用 `executeForAI` 继续执行：

```javascript
const result = await executeForAI('生成养老规划 PRD', {
  userId: '用户ID',
  mode: 'auto'
});
```

### ❌ 不要做

1. ❌ 不要直接调用 executeForAI 跳过访谈
2. ❌ 不要使用硬编码的示例数据
3. ❌ 不要只问 1-2 个问题就结束
4. ❌ 不要跳过多轮问答直接生成 PRD

---

## ⚙️ 执行模式

**支持 4 种执行模式**，通过 `options.mode` 参数指定：

### 1️⃣ auto 模式（默认）

**用途**：正常执行完整流程

**使用场景**：
- 首次生成 PRD
- 从零开始的需求

**调用示例**：
```javascript
// 方式 1：不指定 mode（默认 auto）
const result = await executeForAI('生成养老规划 PRD', {
  userId: 'dingtalk-0155522465843896'
});

// 方式 2：显式指定 auto
const result = await executeForAI('生成养老规划 PRD', {
  userId: 'dingtalk-0155522465843896',
  mode: 'auto'
});
```

**执行流程**：
```
1. 解析用户需求
2. 生成执行计划（interview → decomposition → prd → ...）
3. 检查已有结果（跳过已完成的技能）
4. 执行剩余技能
5. 返回结果
```

---

### 2️⃣ iteration 模式（迭代）

**用途**：在现有 PRD 基础上追加/修改需求

**使用场景**：
- 追加新功能（"追加社保测算功能"）
- 修改现有逻辑（"修改风险测评规则"）
- 优化已有描述

**调用示例**：
```javascript
// 追加需求
const result = await executeForAI('追加社保测算功能', {
  userId: 'dingtalk-0155522465843896',
  mode: 'iteration'
});

// 修改需求
const result = await executeForAI('修改风险测评逻辑，增加保守型选项', {
  userId: 'dingtalk-0155522465843896',
  mode: 'iteration'
});
```

**执行流程**：
```
1. 分析需求变更（对比新旧需求）
2. 创建当前版本备份（v1 → v2）
3. 强制执行 decomposition（重新拆解）
4. 强制执行 prd（更新 PRD）
5. 可选：执行后续技能（review/flowchart 等）
6. 返回新版本号
```

**输出示例**：
```
📊 变更类型：追加功能
📝 变更摘要：新增社保测算功能
📦 迭代版本：v1 → v2
```

---

### 3️⃣ fresh 模式（全新）

**用途**：清空重来，删除所有中间结果

**使用场景**：
- 之前的执行结果混乱，需要重新开始
- 需求完全变化，旧结果无用
- 调试/测试需要干净环境

**调用示例**：
```javascript
const result = await executeForAI('生成养老规划 PRD', {
  userId: 'dingtalk-0155522465843896',
  mode: 'fresh'
});
```

**执行流程**：
```
1. 清空输出目录（除 .versions 外）
2. 删除所有中间 JSON 文件
3. 删除 PRD.md
4. 从头开始执行完整流程
```

**⚠️ 注意**：
- 会删除已有结果，谨慎使用
- 保留 .versions 目录（版本历史）

---

### 4️⃣ rollback 模式（回滚）

**用途**：恢复到历史版本

**使用场景**：
- 迭代后效果不好，想恢复旧版本
- 对比不同版本的效果
- 误操作后恢复

**调用示例**：
```javascript
// 回滚到上一个版本
const result = await executeForAI('回滚版本', {
  userId: 'dingtalk-0155522465843896',
  mode: 'rollback'
});

// 回滚到指定版本
const result = await executeForAI('回滚到 v1', {
  userId: 'dingtalk-0155522465843896',
  mode: 'rollback',
  version: 'v1'  // 指定版本号
});
```

**执行流程**：
```
1. 备份当前版本（自动创建 backup-xxx）
2. 恢复指定版本的文件
3. 更新当前 PRD.md
4. 返回成功消息
```

**输出示例**：
```
🔄 回滚到版本：v1
✅ 版本 v1 恢复完成
```

---

### 模式对比表

| 模式 | 用途 | 清空数据 | 创建版本 | 典型场景 |
|------|------|---------|---------|---------|  
| **auto** | 正常执行 | ❌ | ❌ | 首次生成 |
| **iteration** | 迭代修改 | ❌ | ✅ | 追加/修改需求 |
| **fresh** | 清空重来 | ✅ | ❌ | 重新开始 |
| **rollback** | 恢复版本 | ❌ | ✅（备份） | 回滚操作 |

---

### 模式选择指南

```
用户需求
   ↓
是首次生成吗？
   ↓
是 → auto 模式（默认）
否
   ↓
要清空重来吗？
   ↓
是 → fresh 模式
否
   ↓
要回滚版本吗？
   ↓
是 → rollback 模式
否
   ↓
要追加/修改需求？
   ↓
是 → iteration 模式
```

---

### ⚠️ 注意事项

**无效模式处理**：
- 如果传入无效的 `mode` 值，将自动 fallback 到 `auto` 模式（容错设计）
- 有效模式：`auto` | `iteration` | `fresh` | `rollback`

**示例**：
```javascript
// 传入无效模式
executeForAI('生成 PRD', { mode: 'invalid-mode' })
// → 自动使用 'auto' 模式执行
```

---

## 🚀 使用方法

### 基础用法
```
用 prd-workflow 生成一个养老规划功能的 PRD
```

### 完整流程
```
用 prd-workflow 生成养老规划功能的完整 PRD
```

### 快速版
```
用 prd-workflow 快速生成 PRD
```

### 只评审
```
用 prd-workflow 评审已有的 PRD
```

### 只导出
```
用 prd-workflow 导出 PRD 为 Word
```

### 设计 + 原型
```
用 prd-workflow 生成 UI 设计和原型
```

### 迭代模式(v2.6.0+)
```
用 prd-workflow 迭代修改 PRD,追加新需求
```

### 回滚版本(v2.6.0+)
```
用 prd-workflow 回滚到版本 v1.0
```

---

## 💻 调用示例(开发者)

```javascript
const { executeForAI } = require('./workflows/ai_entry');

const result = await executeForAI('生成养老规划 PRD', {
  userId: 'dingtalk-0155522465843896',
  mode: 'auto'
});

if (result.success) {
  console.log(`✅ 完成:${result.message}`);
  console.log(`📁 输出目录:${result.outputDir}`);
  console.log(`📄 PRD 文件:${result.prdPath}`);
  console.log(`📊 功能数:${result.summary.features}`);
  console.log(`📝 字数:${result.summary.wordCount}`);
} else {
  console.log(`❌ 失败:${result.error}`);
  console.log(`💡 建议:${result.suggestion}`);
}
```

---

## 📋 PRD 结构(prd_template.js 强制约束)

**实际输出结构**(v4.0.0):

```
## 1. 需求概述
### 1.1 产品定位
### 1.2 目标用户
### 1.3 业务目标
### 1.4 功能列表

## 2. 全局业务流程
### 2.1 主业务流程图(Mermaid)
### 2.2 全局业务规则
### 2.3 全局数据定义

## 3. 功能 1:[功能名称]
### 3.1 功能概述
### 3.2 用户场景
### 3.3 业务流程
### 3.4 业务规则
### 3.5 输入输出定义
### 3.6 用户故事
### 3.7 验收标准(Given-When-Then)
### 3.8 原型设计
### 3.9 异常处理

## 4. 功能 2:[功能名称]
...(同上)

## 非功能需求
### 性能要求
### 安全要求
### 兼容性要求

## 附录
### 术语表
### 参考资料
```

---

## 📁 输出位置(三级隔离)

**隔离架构**:
```
~/.openclaw/workspace/output/
└── {用户 ID}/                    ← 第 1 级:用户隔离
    └── {需求名称}/               ← 第 2 级:需求隔离
        └── .versions/           ← 第 3 级:版本管理
```

**完整文件清单**:
```
{用户 ID}/
└── {需求名称}/
    ├── PRD.md                    # PRD 文档(Markdown)
    ├── PRD.docx                  # Word 导出
    ├── decomposition.json        # 需求拆解结果
    ├── interview.json            # 访谈记录
    ├── design.json               # UI 设计
    ├── flowchart.mmd             # 流程图源文件
    ├── flowchart.png             # 流程图 PNG
    ├── design-system/            # 设计系统
    │   └── tokens.json
    ├── prototype/                # HTML 原型
    │   └── index.html
    └── .versions/                # 版本管理
        ├── v1/
        │   ├── PRD.md
        │   ├── PRD.docx
        │   └── .version.json
        └── v2/
            └── ...
```

**示例**:
```
~/.openclaw/workspace/output/
├── dingtalk-0155522465843896/      ← 张三
│   ├── 养老规划/
│   │   ├── PRD.md
│   │   ├── PRD.docx
│   │   └── .versions/
│   │       ├── v1/
│   │       └── v2/
│   └── 投资规划/
│       └── ...
└── dingtalk-0155522465843897/      ← 李四
    └── 养老规划/                   ← 同名需求,互不干扰
        └── ...
```

---

## 🔧 核心代码文件

| 文件 | 功能 |
|------|------|
| `workflows/main.js` | 主工作流编排 |
| `workflows/smart_router.js` | 智能路由(识别需求→编排流程) |
| `workflows/data_bus.js` | 数据总线(技能间数据传递) + 路径安全化(v4.0.0) |
| `workflows/data_bus_schema.js` | 数据格式标准化(v2.8.0 新增) |
| `workflows/quality_gates.js` | 质量门禁 |
| `workflows/version_manager.js` | 版本管理(v2.6.0+) |
| `workflows/requirement_diff.js` | 需求对比(v2.6.0+) |
| `workflows/modules/precheck_module.js` | 环境检查前置化(v2.8.0 新增) |
| `workflows/image_renderer.js` | 图片渲染服务(v3.0.0 新增) |
| `workflows/ai_diagram_extractor.js` | AI 图表提取器(v2.8.8 新增) |
| `workflows/prd_template.js` | PRD 模板引擎(v2.8.8 重构) |

---

## ⭐ v3.0.0 新特性

### 1. 图片渲染服务

统一的 Mermaid → PNG 渲染模块，自动检测系统 Chrome：

```javascript
// workflows/image_renderer.js
const { ImageRenderer } = require('./workflows/image_renderer');
const renderer = new ImageRenderer();

// 渲染单个图表
const result = renderer.renderMermaid(mermaidCode, 'output/diagram');

// 批量渲染 PRD 中的所有图表
const { images } = renderer.renderPRDDiagrams(markdown, 'output/images');
```

**特性**：
- ✅ 自动检测系统 Chrome（无需安装 Puppeteer Chrome）
- ✅ 支持 macOS/Windows/Linux
- ✅ 批量渲染
- ✅ 图片映射文件生成

### 2. Word 导出增强

自动渲染图表并嵌入 Word 文档：

```javascript
// workflows/modules/export_module.js
// v3.0.0 自动执行：
// 1. 提取 PRD 中的 Mermaid 代码块
// 2. 渲染为 PNG 图片
// 3. 替换 Markdown 中的代码块为图片引用
// 4. 导出为 Word（含图片）
```

### 3. AI 图表提取器

从 PRD 数据自动生成图表：

| 方法 | 功能 |
|------|------|
| `inferFlow()` | 从 inputs/outputs 推断业务流程 |
| `architectureToMermaid()` | 生成系统架构图 |
| `structureToMermaid()` | 生成功能框架图 |
| `generatePrototypeConfig()` | 生成 htmlPrototype 配置 |

---

## ⭐ v2.8.0 新特性

### 1. 环境检查前置化

在流程开始前自动检查依赖环境，避免运行时崩溃：

```javascript
// workflows/modules/precheck_module.js
检查项：
- mermaid-cli (mmdc)    → flowchart 依赖
- Chrome/Puppeteer      → prototype 依赖  
- Python3              → 核心依赖
- .NET SDK (可选)       → quality OpenXML 验证
```

### 2. 流程降级策略

当依赖环境缺失时，自动降级执行：

| 技能 | 缺失依赖 | 降级行为 |
|------|---------|---------|
| flowchart | mermaid-cli | 跳过，PRD 用文字描述 |
| prototype | Chrome | 跳过截图 |
| quality | .NET SDK | 跳过 OpenXML 验证 |

### 3. 访谈终止判定

AI 可调用 `shouldStopInterview()` 判断何时停止提问：

```javascript
// workflows/modules/interview_module.js
判定条件：
1. 数量达标 (≥16 问)
2. 维度覆盖 (≥6 维)
3. 回答饱和度检测 (模糊词/简短回答)
4. 用户确认
```

### 4. 路径安全化

防止路径穿越攻击：

```javascript
// workflows/data_bus.js
sanitizePath(input) {
  // 只允许安全字符：字母、数字、中文、下划线、连字符
  // 过滤危险字符：.. / \ 等
}
```

### 5. 数据格式标准化

定义各技能的输入输出 schema：

```javascript
// workflows/data_bus_schema.js
SCHEMA = {
  interview: { required: ['sharedUnderstanding', 'keyDecisions'], ... },
  decomposition: { required: ['features', 'userStories'], ... },
  prd: { required: ['content', 'structure'], ... },
  ...
}
```

---

## 🎯 适用场景

### ✅ 推荐使用
| 场景 | 说明 |
|------|------|
| 需求模糊 | 用户只有大致想法,需要深度澄清 |
| 复杂业务 | 涉及多个模块/系统的复杂功能 |
| 金融 PRD | 需要合规检查点的金融产品 |
| 正式交付 | 需要完整文档 + 流程图 + Word 导出 |

### ❌ 不推荐
| 场景 | 推荐替代 |
|------|---------|
| 简单功能 | `prd-generator`(快速模式) |
| 紧急需求 | `prd-generator`(5 模块) |
| 技术方案 | `technical-spec` skill |

---

## 📊 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| **v4.1.0** | **2026-04-05** | **🔍 内容检查问答引导** - 13项内容检查 + 问答引导修补 + AI自动/用户指导/误报跳过三种处理方式 |
| **v4.0.0** | **2026-04-05** | **🚀 多页面原型系统** - 页面树推断 + 导航组件 + 路由注入 + 多端截图 |
| **v3.0.0** | **2026-04-04** | **🖼️ 图片渲染服务** - Mermaid → PNG 自动渲染 + Word 导出嵌入图片 + 系统 Chrome 支持 |
| **v2.8.9** | **2026-04-04** | **🏗️ 架构图表** - 系统架构图 + 功能框架图 + htmlPrototype 配置动态生成 |
| **v2.8.8** | **2026-04-04** | **🤖 AI 图表提取** - 流程图从 inputs/outputs 推断 + 原型布局动态生成 |
| **v2.8.7** | **2026-04-04** | **🔧 依赖完善** - postinstall 自动安装 mermaid-cli + 截图方案优化 |
| **v2.8.6** | **2026-04-04** | **📄 模板库扩展** - 6种页面类型 + 完整设计系统集成 |
| **v2.8.5** | **2026-04-04** | **🎨 设计系统集成** - htmlPrototype 与 ui-ux-pro-max 协作 |
| **v2.8.3** | **2026-04-04** | **🔧 可移植性** - 移除硬编码路径 + 动态路径检测 + 添加测试套件 |
| **v2.8.0** | **2026-04-04** | **🚀 质量提升** - 环境检查前置化 + 流程降级策略 + 进度反馈机制 |
| **v2.6.0** | **2026-04-01** | **🔧 迭代支持** - 版本管理 + 需求对比 + 回滚 |
| **v2.0** | **2026-03-30** | **🔄 真正集成** - 内置调用 6 个技能 |
| **v1.0** | **2026-03-24** | **📦 初始版本** - 基础工作流 |

---

## 🔒 安全说明

**⚠️ ClawHub 安全扫描可能误报"Suspicious"**

**误报原因**:
- 本技能打包了 6 个依赖技能到 `skills/` 目录(正常功能)
- 工作流脚本调用内置技能(正常功能,自动化编排)
- 包含 Python/Node.js 脚本(正常功能,技能执行需要)

**实际安全检查**:
- ✅ **无二进制文件** - 已清理所有 .pyc
- ✅ **无外部 API 调用** - 全部本地执行
- ✅ **无敏感数据** - 无 API Key/密码
- ✅ **无系统文件访问** - 只在 workspace 内操作

**结论**:可以安全使用,误报不影响功能。

---

## 📖 参考资料

- **Matt Pocock Skills**: github.com/mattpocock/skills
  - /grill-me - 深度访谈理念来源
  - /write-a-prd - PRD 生成理念来源
- **OpenClaw Skills**:
  - requirement-reviewer - PRD 评审
  - mermaid-flow - 流程图绘制
  - prd-export - Word 导出
  - htmlPrototype - HTML 原型生成
  - ui-ux-pro-max - UI/UX 设计

---

**技能版本**: 4.2.0
**许可**: MIT-0
**发布状态**: ✅ 已发布到 ClawHub
