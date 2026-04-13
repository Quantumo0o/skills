# spec-miner EARS Format & Code Archaeology Process
# Version 1.1 | Updated: 2026-04-05 | Added: usage caveats (v1.1)

> ⚠️ **使用前提（必读）**
> 本文件是从**代码考古角度**提取遗留系统行为的参考方法论。
> **EARS 格式描述的是"从代码中观察到的行为"，不是业务规则标准**。
> - 所有 EARS 格式输出的业务行为必须附有**代码来源**（文件:行号）
> - 标注为 INFERENCE 的条目必须通过**客户访谈或文档**确认为 FACT 才能用于迁移规格
> - 不确定的地方必须用 FLAG 标记，禁止凭推断填补空白

---

> 本文件整合自 spec-miner skill，提供从遗留系统提取规格说明的方法论，供 Agent 9 数据迁移分析参考。
> 与 Agent 9 现有 Two-Pass + Mechanism Check 方法论互补，不替代。

---

## 1. EARS 格式（用于描述"观察到的行为"）

来源: spec-miner/references/ears-format.md

EARS = Easy Approach to Requirements Syntax

### 基础结构

```
[条件] → THEN [行为]
```

### 5种模式

#### 模式1：通用格式（Ubiquitous）
```
WHEN the system is operating → THEN [行为]
```
示例：
```
WHEN the system is operating
THEN the policy status shall be updated within 5 seconds
```

#### 模式2：事故触发格式（Event-driven）
```
WHEN [事件]
THEN [行为]
```
示例：
```
WHEN a claim is submitted with amount > $25,000
THEN route to SIU (Special Investigations Unit)
```

#### 模式3：可选触发格式（Optional event）
```
WHEN [事件] is present
THEN [行为]
```
示例：
```
WHEN fraud indicators are present
THEN flag claim for manual review
```

#### 模式4：状态触发格式（State-driven）
```
WHEN [状态] is [值]
THEN [行为]
```
示例：
```
WHEN policy status is 'Lapsed'
THEN disable benefit payments
```

#### 模式5：复合条件格式（Conditional）
```
WHEN [条件A] AND [条件B]
THEN [行为]
```
示例：
```
WHEN policy is active AND claim amount <= $2,000 AND no SIU flags present
THEN auto-approve claim
```

### 在 Agent 9 中的应用

Agent 9 分析遗留系统时，用 EARS 格式描述"观察到的行为"（不是编造的，是从代码/数据字典中反向工程出来的）：

```
## 观察到的行为（EARS格式）

### OB-001: 保单状态变更触发结算
WHEN policy_status = 'SURRENDERED'
THEN trigger surrender value calculation
per legacy_system.py §calculate_surrender_value()

### OB-002: 宽限期届满触发保单失效
WHEN premium_due_date + 30 days < CURRENT_DATE AND premium_unpaid = true
THEN set policy_status = 'LAPSED'
per policy_admin.py §check_lapse_status()
```

---

## 2. Code Archaeology Process（代码考古六步法）

来源: spec-miner/references/analysis-process.md

### 六步法

```
1. SCOPE     → 确定分析边界（哪个模块/哪个功能）
2. EXPLORE   → 用 Glob/Grep 映射结构
3. TRACE     → 追踪数据流和请求路径
4. DOCUMENT  → 用 EARS 格式写出观察到的行为
5. FLAG      → 标记需要澄清的区域
6. SPEC      → 输出规格说明文档
```

### Step 1: SCOPE — 确定分析边界

**输入**: 遗留系统模块名称或功能描述
**输出**: 分析边界定义（in-scope / out-of-scope）

示例：
```
IN SCOPE:
- Policy creation workflow (NB)
- Premium collection (Billing)
- Surrender processing (Policy Servicing)

OUT OF SCOPE:
- Claims processing (separate system)
- Reinsurance cession (manual process)
- Agent commission (external system)
```

### Step 2: EXPLORE — 映射结构

**工具**: Glob + Grep

**目标**: 
- 找到主要入口文件
- 识别核心模块/目录
- 定位数据库/数据字典

**关键 Grep 模式**:
```bash
# 找状态枚举
grep -r "status.*=" --include="*.py" legacy_dir | head -20

# 找业务规则
grep -r "IF\|WHEN\|THEN" --include="*.py" legacy_dir | head -20

# 找 API 端点
grep -r "def \|route\|endpoint" --include="*.py" legacy_dir
```

### Step 3: TRACE — 追踪数据流

**目标**: 
- 从输入到输出的完整路径
- 关键决策点（IF/ELSE）
- 外部系统调用

**示例数据流**:
```
User Input → Validate Input → Load Policy Record → Check Business Rules → 
Calculate Benefits → Generate Output → Update Status
     │              │                  │                │                │
  §NB_001       §NB_002           §PS_003           §PS_004          §PS_005
```

### Step 4: DOCUMENT — 用 EARS 写观察到的行为

**原则**: 
- 每条规则必须引用代码位置（文件:行号）
- 区分"观察到的"和"推断的"
- 不确定的地方 → FLAG，不编造

**输出格式**:
```
## OB-{ID}: [行为描述]
EARS格式: WHEN [条件] THEN [行为]
证据来源: [文件名]:[行号范围]
观察类型: [FACT（可验证）| INFERENCE（推断）]
不确定性: [有/无 — 描述]
```

### Step 5: FLAG — 标记待澄清区域

```
## FLAG-{ID}: [问题描述]
影响: [High/Medium/Low — 什么受阻]
建议澄清方式: [查文档/问业务/看测试用例]
```

### Step 6: SPEC — 输出规格说明文档

**文件名**: `specs/{project_name}_reverse_spec.md`

**必含章节**:
1. Technology stack and architecture
2. Module/directory structure  
3. Observed requirements (EARS格式)
4. Non-functional observations
5. Inferred acceptance criteria
6. Uncertainties and questions
7. Recommendations

---

## 3. spec-miner 分析清单

来源: spec-miner/references/analysis-checklist.md

### 代码考古必查项

- [ ] 主要入口文件已识别
- [ ] 核心业务规则已映射（IF/ELSE/状态机）
- [ ] 外部系统接口已识别
- [ ] 错误处理路径已记录
- [ ] 所有观察到的行为已标注代码来源
- [ ] 不确定区域已标记为 FLAG
- [ ] EARS 格式验证通过
- [ ] 无功能性遗漏（对比数据字典）

### 安全模式必查

- [ ] 认证/授权逻辑已记录
- [ ] 数据验证逻辑已记录（输入校验）
- [ ] 敏感数据处理已记录（加密/脱敏）
- [ ] 审计日志已识别

---

## 4. 与 Agent 9 现有方法的整合

Agent 9 现有方法论：
- Two-Pass + Mechanism Check（KB优先）
- Legacy Archetype A1-A6（6种遗留系统模式）
- Migration Risk Scoring（7维度）
- Go/No-Go Gate

**spec-miner 作为补充，用于**：
1. 遗留系统行为无法从 KB 确认时 → 用代码考古提取
2. 数据迁移字段映射时 → 用 EARS 格式记录业务规则
3. 遗留系统接口不确定时 → 用 TRACE 追踪数据流

**不替代 Agent 9 现有流程**，仅在 KB 无法覆盖的场景下使用。
