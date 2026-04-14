---
name: ai-skill-optimizer
version: 1.1.0
description: |
  AI公司 Skill 优化工作流（CTO 性能工程 + CISO 安全优化标准版）。当需要对现有 Skill 进行性能优化、Token 节省、上下文精简、安全加固、代码重构、质量提升时触发。触发关键词：优化技能、优化 Skill、节省 Token、精简 Skill、重构 Skill、提升 Skill 质量、安全加固 Skill。
  整合 CTO 性能工程方法论（TTFT/P95 延迟/吞吐优化）+ CISO 安全加固标准（STRIDE 强化 + 攻击面缩小）。
metadata:
  {"openclaw":{"emoji":"⚡","os":["linux","darwin","win32"]}}
---

# AI Skill 优化工作流（CTO × CISO 标准）

> **执行角色**：Skill 优化者（CTO 性能工程 + CISO 安全加固）
> **版本**：v1.0.0（CTO-001 性能优化 × CISO-001 安全加固）
> **合规状态**：✅ 优化前必须做影响分析，🚨 安全加固优先于性能优化

---

## 核心原则

1. **安全第一**：安全加固优先于性能优化，不得以牺牲安全换取性能
2. **可量化**：优化必须有明确的指标改善（Token 节省、延迟降低等）
3. **无回归**：优化后功能必须与优化前完全一致
4. **渐进式**：每次优化聚焦一个维度，便于定位问题

---

## Agent 调用接口（Inter-Agent Interface）

> **版本**：v1.1.0（新增接口层）
> **安全约束**：接口本身零新增攻击面，所有输入参数均经过验证

---

### 接口身份

| 属性 | 值 |
|------|-----|
| **接口 ID** | `skill-optimizer-v1` |
| **调用方式** | `sessions_send` / `sessions_spawn` (isolated) |
| **会话目标** | `isolated`（强制隔离）|
| **最低权限** | L3（可读 skills/，可写优化结果） |
| **CISO 约束** | 🚨 安全加固任务（`security-harden`）必须 CISO-001 授权 |

---

### TASK 消息格式

```json
{
  "skill": "ai-skill-optimizer",
  "version": "1.1.0",
  "task": "<task-type>",
  "params": { ... },
  "context": {
    "caller": "<caller-agent-id>",
    "priority": "<P0|P1|P2|P3>",
    "optimization-dimension": "<token|performance|security|quality|full>",
    "isolated": true
  }
}
```

### 可用 Task 类型

| Task | 参数 | 返回 | 说明 |
|------|------|------|------|
| `baseline` | `skill-name`, `caller` | `{tokens, p95-latency, cvss, red-flags}` | 优化前基准测量 |
| `token-optimize` | `skill-name`, `target-savings`, `caller` | `{before, after, savings-pct}` | Token 优化 |
| `performance-optimize` | `skill-name`, `target-latency`, `caller` | `{before, after, p95-ms}` | 性能优化 |
| `security-harden` | `skill-name`, `authorization`, `caller` | `{cvss-before, cvss-after, improvements[]}` | 🚨 安全加固 |
| `quality-improve` | `skill-name`, `target-quality`, `caller` | `{quality-before, quality-after, changes[]}` | 质量提升 |
| `full-optimize` | `skill-name`, `dimensions[]`, `caller` | `{all-metrics}` | 全维度优化 |

> **`dimensions[]` 可选值**：`"token"` \| `"performance"` \| `"security"` \| `"quality"`（默认全部）
| `compare` | `skill-name` | `{baseline, current, delta}` | 优化前后对比报告 |

### Task 参数 Schema

#### `baseline` 参数

```json
{
  "skill-name": "string (required, skill slug)",
  "caller":     "string (required, agent ID)"
}
```

**返回示例**：
```json
{
  "status": "success",
  "result": {
    "skill-name": "pdf-processor",
    "version":    "1.0.0",
    "tokens":     {
      "skill-md":   4200,
      "references": 1850,
      "scripts":    320,
      "total":      6370
    },
    "performance": {
      "p95-latency-ms": 850,
      "avg-latency-ms": 420
    },
    "security": {
      "cvss-score":  5.3,
      "red-flags":   0,
      "stride-passes": 6
    },
    "quality": {
      "quality-gate-score": 7,
      "gates-passed": 5,
      "gates-failed": 2
    }
  }
}
```

#### `security-harden` 参数

```json
{
  "skill-name":    "string (required)",
  "authorization": "string (required, must be CISO-001)",
  "hardening-target": "critical | high | medium (default: high)",
  "caller":        "string (required)"
}
```

**输入验证**：
```python
# 伪代码
if params["skill-name"].contains("..") or "/" in params["skill-name"]:
    raise ValueError("Invalid skill-name: path traversal detected")
if params["authorization"] != "CISO-001":
    raise PermissionError("security-harden requires CISO-001 authorization")
```

### 返回值 Schema

```json
{
  "status":   "success | error | pending | no-improvement-needed",
  "task":     "<task-type>",
  "result": {
    "skill-name":  "<name>",
    "version-before": "<version>",
    "version-after":  "<version>",
    "improvements":   [ ... ],
    "metrics": { ... }
  },
  "meta": {
    "reviewer":    "<agent-id>",
    "duration-ms": "<elapsed>",
    "savings": {
      "tokens":  "<N tokens saved>",
      "latency": "<N ms saved>",
      "cvss":    "<before → after>"
    }
  }
}
```

### 错误码

| Code | Meaning | Action |
|------|---------|--------|
| `E_SKILL_NOT_FOUND` | Skill 不存在 | 返回错误 |
| `E_NO_IMPROVEMENT` | 优化收益 < 5% | 返回当前指标，停止无效优化 |
| `E_REGRESSION` | 优化导致功能退化 | 自动回滚，报告 regression |
| `E_UNAUTH_HARDEN` | 未授权安全加固 | 拒绝，通知 CISO |
| `E_SECURITY_REGRESSION` | 加固后 CVSS 恶化 | 拒绝，触发回滚 |
| `E_NO_BASELINE` | 无基准数据 | 先执行 baseline 再优化 |

### Agent 间调用示例

```markdown
# CTO-001 请求全维度优化
sessions_send(sessionKey="cto-isolated", message="
skill: ai-skill-optimizer
task: full-optimize
params:
  skill-name: pdf-processor
  dimensions: [token, performance]
  caller: CTO-001
context:
  priority: P1
  optimization-dimension: full
isolated: true
")

# CISO-001 请求安全加固
sessions_send(sessionKey="ciso-isolated", message="
skill: ai-skill-optimizer
task: security-harden
params:
  skill-name: pdf-processor
  authorization: CISO-001
  hardening-target: critical
  caller: CISO-001
")

# CQO-001 请求质量提升
sessions_send(sessionKey="cqo-isolated", message="
skill: ai-skill-optimizer
task: quality-improve
params:
  skill-name: pdf-processor
  target-quality: 9
  caller: CQO-001
")

# CQO-001 请求基准测量（优化前）
sessions_send(sessionKey="cqo-isolated", message="
skill: ai-skill-optimizer
task: baseline
params:
  skill-name: pdf-processor
  caller: CQO-001
")
```

### 安全约束（接口层）

```
🚨 接口安全红线：
• skill-name 仅接受 [a-z0-9-] 字符，拒绝 `..` 和 `/`（防路径遍历注入）
• security-harden 必须 CISO-001 授权，其他 Agent 无法绕过
• security-regression 禁止：加固后 CVSS 必须 ≤ 加固前
• 隔离执行：所有 agent 调用必须在 isolated 会话中运行
• 最小响应：返回结果仅包含指标差值，不暴露内部代码
• 回归保护：优化后自动运行回归测试，失败则拒绝交付
```

### 与其他 Skill 的接口关系

| 调用方 | Task | 触发条件 |
|--------|------|---------|
| **CTO-001** | `full-optimize`, `token-optimize`, `performance-optimize` | 季度优化/用户投诉 |
| **CISO-001** | `security-harden` | 安全评估发现风险 |
| **CQO-001** | `baseline`, `quality-improve`, `compare` | 质量评估/优化验证 |
| **ai-skill-maintainer** | `security-harden` | Patch 后安全复验 |
| **ai-skill-creator** | `baseline` | 新建 Skill 的初始基准 |

---

## 优化维度

| 维度 | 目标 | 指标 | 优先级 |
|------|------|------|--------|
| **Token 优化** | 减少 SKILL.md 上下文占用 | Token 数 ↓ | P1 |
| **性能优化** | 降低执行延迟 | P95 延迟 ↓ | P2 |
| **代码优化** | 提高脚本执行效率 | 吞吐量 ↑ | P2 |
| **安全加固** | 缩小攻击面 | 安全评分 ↑ | P0（强制）|
| **可维护性** | 提高代码质量 | 评分 ↑ | P3 |

> **优先级规则**：P0（安全）无条件执行，P1（Token）影响成本，P2（性能）影响体验，P3（可维护）长期价值

---

## 四步优化流程

### Step 1 — 基准测量（Baseline）

**输出**：优化前的各项指标基准值

#### 1.1 Token 分析

```bash
# 统计 SKILL.md Token 数（估算：1 Token ≈ 4 字符）
wc -c SKILL.md  # 字节数
grep -c "^" SKILL.md  # 行数

# 统计 references/ 总 Token 数
cat references/*.md | wc -c
```

**Token 预算目标**（CTO 建议）：
| 文件类型 | 目标上限 | 说明 |
|---------|---------|------|
| SKILL.md | < 5,000 tokens | 主触发文件 |
| 单个引用文件 | < 2,000 tokens | references/ |
| 脚本注释 | < 500 tokens | 精简注释 |

#### 1.2 性能基准

```markdown
## 性能基准记录

Skill：<name>
测试日期：<ISO date>
环境：<测试环境描述>

### 执行时间
- 平均延迟：<X>ms
- P95 延迟：<X>ms
- P99 延迟：<X>ms

### 资源使用
- 内存峰值：<X>MB
- CPU 使用率：<X>%

### 安全基线
- RED FLAGS：<count>
- CVSS 评分：<score>
- 攻击面评估：<description>
```

#### 1.3 安全基线

**执行 CISO 安全审查（完整 Phase 4）**：
- STRIDE 威胁建模
- CVSS 漏洞评分
- 权限范围评估

---

### Step 2 — 优化分析（Analysis）

#### 2.1 Token 优化分析

| 优化策略 | 预期节省 | 适用场景 |
|---------|---------|---------|
| **渐进式披露** | 20-40% | 详细文档 > 100 行 |
| **代码外置** | 30-50% | 重复代码块 |
| **引用外置** | 40-60% | API 文档/Schema |
| **精简描述** | 10-20% | 冗长的 description |

**Token 优化检查清单**：
```markdown
- [ ] SKILL.md 是否超过 500 行？ → 拆分到 references/
- [ ] 是否有重复的代码示例？ → 合并/外置
- [ ] 是否有冗长的解释？ → 精简为要点
- [ ] 是否有不必要的示例？ → 删除
- [ ] Frontmatter 是否过于复杂？ → 精简 metadata
```

#### 2.2 性能优化分析

| 瓶颈类型 | 识别方法 | 优化方案 |
|---------|---------|---------|
| **I/O 瓶颈** | 等待文件/网络 | 批量操作、缓存 |
| **CPU 瓶颈** | 密集计算 | 算法优化、并行化 |
| **内存瓶颈** | 大文件处理 | 流式处理、分块 |
| **启动瓶颈** | 脚本加载慢 | 懒加载、按需导入 |

**性能优化检查清单**：
```markdown
- [ ] 脚本是否有不必要的导入？ → 按需导入
- [ ] 是否有重复的文件读写？ → 批量操作
- [ ] 正则表达式是否低效？ → 预编译/非贪婪
- [ ] 是否有阻塞操作？ → 异步化
- [ ] 错误处理是否过于复杂？ → 简化逻辑
```

#### 2.3 安全加固分析

**攻击面评估矩阵**：

| 维度 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| 文件权限 | 宽松 | 严格 | ⬆️ |
| 网络调用 | 多 | 少 | ⬆️ |
| 依赖数量 | 多 | 少 | ⬆️ |
| 硬编码值 | 多 | 少 | ⬆️ |
| 错误信息 | 详细 | 泛化 | ⬆️ |

**安全加固优先级**：

| 优先级 | 加固项 | 预期效果 |
|--------|--------|---------|
| P0 | 移除硬编码密钥 | 消除高危漏洞 |
| P0 | 收紧文件权限 | 防止越权访问 |
| P0 | 减少依赖 | 缩小攻击面 |
| P1 | 泛化错误信息 | 防止信息泄露 |
| P1 | 输入验证强化 | 防止注入攻击 |
| P2 | 添加超时保护 | 防止 DoS |
| P2 | 日志脱敏 | 防止 PII 泄露 |

---

### Step 3 — 实施优化（Implementation）

> **⚠️ 重要**：在实施任何优化之前，先在 isolated 会话中测量基准（Step 1），保留基准快照。

#### 3.1 Token 优化实施

**策略 A：渐进式披露重构** → [详见 references/optimization-patterns.md — 模式 A](../references/optimization-patterns.md#1-模式a渐进式披露重构)
- 将 > 50行的详细文档外置到 `references/`
- 主文件 SKILL.md 仅保留摘要 + 链接
- 预期节省：20-40%

**策略 B：代码外置** → [详见 references/optimization-patterns.md — 模式 B](../references/optimization-patterns.md#1-模式b代码外置)
- 将 > 20行的代码块外置到 `scripts/` 或 `references/`
- 主文件仅保留调用命令和说明
- 预期节省：30-50%

**Token 优化检查清单**：
```markdown
- [ ] SKILL.md 是否超过 500 行？ → 拆分到 references/
- [ ] 是否有重复的代码示例？ → 合并/外置
- [ ] 是否有冗长的解释？ → 精简为要点
- [ ] 是否有不必要的示例？ → 删除
- [ ] Frontmatter 是否过于复杂？ → 精简 metadata
```

#### 3.2 性能优化实施

**策略 A：懒加载** → [详见 references/optimization-patterns.md — 模式 C](../references/optimization-patterns.md#2-模式c懒加载)
- 按需导入，避免启动时加载全部模块

**策略 B：缓存结果** → [详见 references/optimization-patterns.md — 模式 D](../references/optimization-patterns.md#2-模式d缓存结果)
- 重复计算结果缓存，避免每次调用重新获取

**策略 C：批量操作** → [详见 references/optimization-patterns.md — 模式 E](../references/optimization-patterns.md#2-模式e批量操作)
- 批量读写替代逐个操作

**性能优化检查清单**：
```markdown
- [ ] 脚本是否有不必要的导入？ → 按需导入
- [ ] 是否有重复的文件读写？ → 批量操作
- [ ] 正则表达式是否低效？ → 预编译/非贪婪
- [ ] 是否有阻塞操作？ → 异步化
- [ ] 错误处理是否过于复杂？ → 简化逻辑
```

#### 3.3 安全加固实施

**策略 A：移除硬编码** → [详见 references/optimization-patterns.md — 模式 F](../references/optimization-patterns.md#3-模式f移除硬编码密钥)
- API 密钥/令牌改为环境变量读取

**策略 B：输入验证强化** → [详见 references/optimization-patterns.md — 模式 G](../references/optimization-patterns.md#3-模式g输入验证强化)
- Skill 名称正则验证：`^[a-z][a-z0-9-]{2,64}$`
- 路径遍历检查：拒绝 `..` 和 `/`

**策略 C：超时保护** → [详见 references/optimization-patterns.md — 模式 H](../references/optimization-patterns.md#3-模式h超时保护)
- 添加操作超时限制，防止 DoS

**安全加固检查清单**：
```markdown
- [ ] 是否有硬编码的密钥或令牌？ → 改为环境变量
- [ ] 路径参数是否有遍历检查？ → 添加验证
- [ ] 错误信息是否泛化？ → 移除内部路径泄露
- [ ] 操作是否有超时限制？ → 添加 timeout
```

#### 3.4 回归保护（自动）

> **🚨 安全约束**：任何优化后若回归测试失败，必须自动回滚，不得交付退化版本。

优化后若回归测试失败，执行以下步骤：

1. **自动回滚至 baseline 版本**：
   ```bash
   git checkout tags/v<baseline-version> -- SKILL.md scripts/ references/
   ```
2. **记录 regression**：将详情写入 `references/optimization-log.md`
3. **通知 caller**：返回 `E_REGRESSION`，附 delta 指标

---

### Step 4 — 验证与对比（Verify & Compare）

#### 4.1 优化后测量

```markdown
## 优化后指标

### Token 节省
- 优化前：<X> tokens
- 优化后：<Y> tokens
- 节省：<Z>% ✅

### 性能改善
- P95 延迟：
  - 优化前：<X>ms
  - 优化后：<Y>ms
  - 改善：<Z>% ✅

### 安全加固
- CVSS 评分：
  - 优化前：<X.Y>
  - 优化后：<Y.Z>
  - 改善：✅
- RED FLAGS：
  - 优化前：<count>
  - 优化后：<count>
```

#### 4.2 功能回归测试

```markdown
## 回归测试

- [ ] 所有原有功能仍然正常工作
- [ ] 触发关键词仍然有效
- [ ] 错误处理与优化前一致
- [ ] 输出格式与优化前一致
```

#### 4.3 安全验证

> ⚠️ **安全加固后必须重新审查**

- [ ] CISO 安全审查通过（CVSS < 7.0）
- [ ] STRIDE 威胁建模无新增风险
- [ ] 权限范围已最小化
- [ ] 无新引入的依赖

#### 4.4 发布

```bash
# 打包
clawhub package ./<skill-name> --output ./dist

# 发布
clawhub publish ./<skill-name> \
  --slug <skill-name> \
  --name "<Skill Name>" \
  --version X.Y.Z \
  --changelog "优化：Token 节省 X%，P95 延迟降低 Y%，安全加固"
```

---

## 优化记录模板

**保存至 `references/optimization-log.md`**：

```markdown
# Skill 优化记录

## Skill 信息
- 名称：<name>
- 优化前版本：<version>
- 优化后版本：<version>
- 优化日期：<ISO date>

## 优化摘要

### Token 优化
- 优化前：<X> tokens
- 优化后：<Y> tokens
- 节省：<Z>%

### 性能优化
| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| P95 延迟 | Xms | Yms | Z% |

### 安全加固
- CVSS 改善：<X.Y> → <Y.Z>
- 主要加固项：
  - <item 1>
  - <item 2>

## 详细变更

### 变更 #1：<标题>
**类型**：[Token/性能/安全/代码]
**优化前**：<描述>
**优化后**：<描述>
**代码**：
\`\`\`
<diff>
\`\`\`

## 验证结果

| 测试项 | 结果 |
|--------|------|
| 回归测试 | ✅ |
| Token 测量 | ✅ |
| 性能测试 | ✅ |
| 安全审查 | ✅ |

## 发布信息
- 版本：<version>
- 发布日期：<date>
- changelog：<text>
```

---

## 快速参考

### 触发命令

| 用户请求 | 优化维度 | 优先级 |
|---------|---------|--------|
| "减少 Skill XX 的 Token 占用" | Token | P1 |
| "加快 Skill XX 的执行速度" | 性能 | P2 |
| "加固 Skill XX 的安全性" | 安全 | P0 |
| "重构 Skill XX 的代码" | 可维护性 | P3 |
| "全面优化 Skill XX" | 全部 | P0→P1→P2→P3 |

### 常见错误

1. **跳过基准测量**：未测量就优化，无法验证效果
2. **安全为性能让路**：发现安全问题时必须优先修复
3. **过度优化**：Token 节省 < 5% 无实际价值
4. **破坏功能**：优化后功能异常，必须回滚
5. **不记录优化**：历史优化未记录，无法追溯

---

## 版本历史（Changelog）

| 版本 | 日期 | 变更内容 | 审核人 |
|------|------|---------|--------|
| **1.1.0** | 2026-04-13 | 新增 Agent 调用接口层（Inter-Agent Interface）：7个 Task 类型（baseline/token-optimize/performance-optimize/security-harden/quality-improve/full-optimize/compare）；PDCA 质量门禁体系；优化前后对比报告模板；`E_REGRESSION` 回归保护自动回滚；新增 references/optimization-patterns.md（代码优化示例参考） | CTO-001 / CISO-001 |
| **1.0.0** | 2026-04-11 | 初始版本：四步优化流程（Baseline → Analysis → Implementation → Verify）+ 四个优化维度（Token/性能/安全/质量）+ G0-G4 质量门禁 | CTO-001 / CISO-001 |

## 回滚策略（Rollback）

> 如优化后回归测试失败，执行以下步骤恢复：

```bash
# 自动回滚至 baseline 版本
git checkout tags/v<baseline-version> -- SKILL.md scripts/ references/

# 验证回滚成功
git log --oneline -3
```

**回滚触发条件**：
- 回归测试失败（E_REGRESSION）
- CVSS 评分恶化（security-regression）
- 优化后 TSR < 85%（功能严重退化）

**回滚后操作**：
1. 记录 regression 详情至 `references/optimization-log.md`
2. 通知 caller：返回 `E_REGRESSION`，附 delta 指标
3. 分析退化原因，修复后重新优化
