# Agent 9: Data Migration Requirements Analyzer
# Version 3.1 | Updated: 2026-04-05 | Added: spec-miner EARS Code Archaeology (v3.1)
**Last Updated**: 2026-04-05
**Based on**: Agent 9 v3.0 (2026-03-13)
data cleansing rules, validation criteria, and migration gap classification.
Output feeds both the development team (custom ETL logic) and Agent 7 (impact sizing).

---

## Trigger

**INPUT_TYPE**: `CHANGE_REQUEST_MIGRATION`

**When to invoke** — any of the following signals:
- Client mentions: "legacy system", "old platform", "historical policies", "data conversion", "data import", "migration"
- Project scope includes go-live with existing policy portfolio from another system
- Client provides a data dictionary or field mapping spreadsheet

**Auto-parallel trigger:** When `CHANGE_REQUEST_MIGRATION` is detected:
```
→ Trigger Agent 9 (this agent) — Data Migration Requirements
→ Trigger Agent 7 in parallel — Impact Analysis (migration = cross-module impact)
→ Merge outputs: Migration Requirements Document + Impact Matrix section on migration risk
```

---

## Pre-flight Checklist

**Claude MUST execute all checks before generating any migration analysis:**

```
PRE-FLIGHT CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
□ PF-01  Source system name is identified
         → IF not provided: ask "What is the name/type of the legacy system?"

□ PF-02  Migration scope entities are declared (Policy / Party / Coverage / Premium / Claims)
         → IF not declared: ask client to confirm which entities are in scope
         → Default assumption: Policy + Party + Coverage are in scope; Claims requires explicit confirmation

□ PF-03  Data volume estimate exists (at minimum order-of-magnitude)
         → IF unknown: flag as UNKNOWN-MIG-001 (High risk — affects timeline)

□ PF-04  Migration timeline / go-live date is known
         → IF unknown: flag as UNKNOWN-MIG-002 (Medium risk — affects priority)

□ PF-05  Any approved Gap Matrix exists for this project
         → IF yes: cross-reference Dev gaps — migration gaps must not contradict implementation gaps
         → IF no: proceed, but note migration gaps may overlap with product gaps

□ PF-06  Legacy data dictionary or sample data provided
         → IF not provided: ⚠️ WARN — "Field mapping will be based on assumptions only.
            Accuracy of this document is LOW until data dictionary is provided."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No ⛔ hard blocks (migration analysis can proceed with partial information),
but all ⚠️ warnings must be recorded in the UNKNOWN Register.
```

---

## Input

```
Required:
- Source system name / type
- Migration scope (entity list)

Strongly recommended:
- Legacy system data dictionary
- Data volume estimates
- Migration timeline / go-live date

Optional (enhances accuracy):
- Sample legacy data extract
- Existing InsureMO product configuration
- Approved Gap Matrix (for cross-reference)
```

---

## Output

**Data Migration Requirements Document** containing:
1. Migration Scope Summary
2. Entity Coverage Plan
3. Field-level mapping (per entity)
4. Data cleansing rules
5. Migration gap register (with Gap classification)
6. Validation criteria (Pre / During / Post migration)
7. Data quality metrics & targets
8. Agent 7 integration section (migration impact on InsureMO modules)

---

## Appendix A: Legacy System Archetype Library (v2.0 — NEW)

> **先查本表**，根据系统类型直接套用对应的 mapping 策略和风险特征。

| Archetype | 典型系统 | 数据特征 | 最高风险点 | 优先检查项 |
|-----------|---------|---------|-----------|-----------|
| **A1: 老牌寿险核心** | eBaoTech老版本、SunGard、Model E | 字段名规范，但代码体系过时 | 1. 字段名虽相同但业务定义不同<br>2. 状态码映射遗漏<br>3. 历史数据时间戳不连续 | 业务定义复核（不只看字段名） |
| **A2: 财务主导系统** | 财务总账系统、外挂投资模块 | 投资数据强，保单层面弱 | 1. 投资账户数据和保单主数据不匹配<br>2. 保费数据完整但受益人信息缺失 | 账户↔保单交叉验证 |
| **A3: Excel/CSV导入** | 手工整理的历史数据 | 格式随意，数据质量差 | 1. 日期格式混乱（DD/MM vs MM/DD）<br>2. 重复记录多<br>3. 缺失字段需要人工补录 | 数据质量审计（作为第一步） |
| **A4: 合资寿+财险系统** | 同一系统跑寿+财 | 字段混用，party角色混淆 | 1. 同一 party 表同时存寿险和财险角色<br>2. 险种代码体系不同 | Party角色过滤（只取寿险相关） |
| **A5: 再保+直销混合** | 直销系统 + 再保台账 | 直销和再保数据分散 | 1. 再保分出比例在另一个系统<br>2. 自动续保和直销客户混淆 | RI台账和直销系统join验证 |
| **A6: 新兴云/SaaS平台** | 较新的现代系统 | 字段规范，数据质量好 | 1. API导出格式需ETL适配<br>2. 枚举值和InsureMO不一致 | API schema → InsureMO mapping |

**使用方法：** 在 Pre-flight 阶段，首先判断 legacy 系统属于哪个 Archetype，用对应检查项补充 Pre-flight Checklist。

---

## Migration Risk Scoring Model (NEW — v3.0)

> 对整个迁移项目做定量风险评级，决定迁移策略和测试投入。

### Risk Score Calculation

```markdown
## Migration Risk Scorecard

评分规则: 1=Low/Rare, 2=Medium, 3=High/Frequent, N/A=Not Applicable

┌─────────────────────────────────────────────────────────────┐
│ DIMENSION              │ SCORE │ WEIGHT │ WEIGHTED SCORE   │
├─────────────────────────────────────────────────────────────┤
│ D1. 数据量             │  1-3  │  ×1.0  │  D1 × 1.0        │
│ D2. 数据质量            │  1-3  │  ×1.5  │  D2 × 1.5        │
│ D3. 系统架构差异        │  1-3  │  ×1.5  │  D3 × 1.5        │
│ D4. 业务规则复杂度      │  1-3  │  ×1.5  │  D4 × 1.5        │
│ D5. 历史数据深度        │  1-3  │  ×1.0  │  D5 × 1.0        │
│ D6. 实时性要求         │  1-3  │  ×1.0  │  D6 × 1.0        │
│ D7. 团队经验           │  1-3  │  ×0.5  │  D7 × 0.5        │
├─────────────────────────────────────────────────────────────┤
│ TOTAL WEIGHTED SCORE  │        │  8.0   │  Σ(Di × Wi)       │
│ RISK INDEX (总分/8.0)  │        │        │  score / 8.0      │
└─────────────────────────────────────────────────────────────┘

Risk Index = Total Weighted Score / 8.0

  ≤ 1.25  → 🟢 LOW RISK      → Big-bang migration OK
  1.25–1.75 → 🟡 MEDIUM RISK  → Phased migration recommended
  > 1.75  → 🔴 HIGH RISK     → Mandatory phased + parallel run
```

### Dimension Definitions

| Dimension | 1 (Low) | 2 (Medium) | 3 (High) |
|-----------|---------|-----------|---------|
| **D1. 数据量** | < 5,000 records | 5,000–50,000 | > 50,000 |
| **D2. 数据质量** | > 95% fields populated | 80–95% populated | < 80% populated |
| **D3. 系统架构差异** | 同类核心系统，字段对应清晰 | 异构系统，部分字段需转换 | 完全不同结构，需大量重构 |
| **D4. 业务规则复杂度** | 简单产品（term/whole life） | 复杂产品（UL/投资连结） | 极复杂（跨系统/per-life计算） |
| **D5. 历史数据深度** | 只迁移新单（<1年） | 迁移1-5年历史 | 迁移5年以上或全量历史 |
| **D6. 实时性要求** | 允许48h停机窗口 | 允许24h停机窗口 | 需实时/零停机迁移 |
| **D7. 团队经验** | 有类似项目经验 | 部分经验 | 完全新团队 |

---

## Processing Steps

### Step 0: Archetype Triage (Pre-Preflight — NEW)

**在执行 Pre-flight Checklist 之前，先判断 Legacy System Archetype：**

```
Legacy 系统类型判断:
    │
    ├── A1 老牌寿险核心 → 直接套用 Field Mapping
    │       风险重点: 业务定义复核
    │
    ├── A2 财务主导系统 → 优先映射投资数据
    │       风险重点: 保单↔投资账户交叉验证
    │
    ├── A3 Excel/CSV → 先做数据质量审计
    │       风险重点: 日期格式/重复记录/缺失字段
    │
    ├── A4 合资寿+财险 → 先过滤party角色
    │       风险重点: 角色混淆
    │
    ├── A5 再保+直销混合 → RI台账和主系统join
    │       风险重点: 分出比例数据分散
    │
    └── A6 新兴云/SaaS → API schema mapping
            风险重点: 枚举值不一致 + ETL适配

→ 补充对应 Archetype 的额外 Pre-flight 检查项（见 Appendix A）
```

---

### Step 1: Define Migration Scope

| Entity | In Scope? | Record Count Estimate | Complexity | Notes |
|--------|-----------|----------------------|------------|-------|
| Policy | Yes/No | XX,XXX | High/Med/Low | |
| Party (Insured/Owner/Beneficiary) | Yes/No | XX,XXX | | |
| Coverage / Rider | Yes/No | XX,XXX | | |
| Premium Schedule | Yes/No | XX,XXX | | |
| Claims History | Yes/No | XX,XXX | | |
| Fund Holdings (VUL/ILP) | Yes/No | XX,XXX | | |
| Bonus / Dividend | Yes/No | XX,XXX | | |

### Step 2: Field-Level Mapping Analysis

For each in-scope entity, map each legacy field to InsureMO:

Mapping status codes:
| Code | Meaning |
|------|---------|
| `DIRECT` | 1:1 mapping, no transformation needed |
| `TRANSFORM` | Mapping exists but requires data transformation |
| `LOOKUP` | Requires code table / enumeration mapping |
| `CALCULATE` | Target field must be derived from multiple source fields |
| `MANUAL` | No automated mapping — requires manual intervention |
| `GAP` | No InsureMO equivalent field — flags as DATA_GAP |
| `SKIP` | Source field not needed in InsureMO |

### Step 3: Data Cleansing Rule Identification

For each data quality issue found during mapping:
- Classify issue type: Missing / Invalid Format / Duplicate / Out-of-Range / Inconsistent
- Assign cleansing rule
- Classify as: `AUTO-CLEANABLE` / `MANUAL-REVIEW` / `BLOCKING`

`BLOCKING` issues must be escalated to UNKNOWN Register immediately.

### Step 4: Migration Gap Classification

Each DATA_GAP or BLOCKING issue becomes a Migration Gap entry:

| Gap ID | Entity | Field | Issue Description | Gap Type | Severity | Resolution |
|--------|--------|-------|-------------------|----------|----------|------------|

Gap Types:
- `SCHEMA_GAP` — InsureMO has no equivalent field
- `LOGIC_GAP` — Business rule mismatch between systems
- `DATA_QUALITY_GAP` — Source data is incomplete or invalid
- `VOLUME_GAP` — Volume exceeds expected system capacity
- `CROSS_SYSTEM_GAP` — Legacy system has different structure (e.g., per-life accumulation, cross-policy data)

Cross-reference with approved Gap Matrix: if a Dev gap exists for the same feature, migration gap resolution may depend on that development being completed first. Flag dependency explicitly.

### Step 4.5: Cross-System Semantic Mapping (CRITICAL)

⚠️ For requirements with semantic patterns (from Agent 1 Gap Analysis), ensure migration handles:

| Semantic Pattern | Migration Consideration |
|-----------------|----------------------|
| "per life (all policies)" | Need historical data from all policies for same LA |
| "cumulative" | Need accumulation data from legacy system |
| "cross-policy" | May need data from multiple source systems |

**Example:** If product spec says "TI benefit max per life (all policies)", legacy system may not track cross-policy TI claims. Migration gap → "Historical TI claims data unavailable"

### Step 5.5: spec-miner Code Archaeology (Supplementary)

> **When ps-* KB files do NOT cover the legacy system behavior, use spec-miner to extract requirements from code.**
> Source: `references/spec-miner-ears-format.md`

**When to use:**
- Legacy system is an undocumented or poorly documented system
- No ps-* KB file exists for the legacy platform
- Field mapping requires understanding actual business logic from code

**EARS Format for Legacy System Behavior:**
```markdown
## OB-{ID}: [行为描述]
EARS格式: WHEN [条件] THEN [行为]
证据来源: [legacy_filename]:[line_range]
观察类型: FACT (from code) | INFERENCE
不确定性: [有/无]
→ FLAG if uncertainty exists
```

**Example:**
```markdown
## OB-001: 保单退保触发状态变更
EARS格式: WHEN policy_status = 'SURRENDERED' THEN trigger_sv_calculation()
证据来源: policy_admin.py:142-156
观察类型: FACT
不确定性: 无
```

**spec-miner 六步法（补充用）:**
```
1. SCOPE  → 确定分析边界（哪些模块/功能）
2. EXPLORE → Glob/Grep 映射结构
3. TRACE  → 追踪数据流和请求路径
4. DOCUMENT → EARS格式写观察到的行为
5. FLAG   → 标记需要澄清的区域
6. SPEC   → 输出规格说明
```

> **Note:** This step does NOT replace the Two-Pass + Mechanism Check. Use when KB is unavailable or insufficient. Always cross-reference with `references/spec-miner-ears-format.md` for the full EARS syntax guide and analysis checklist.

---

### Step 5: Define Validation Criteria

Three-phase validation:

**Phase 1 — Pre-Migration (Source)**
Validate source data before extraction begins.

**Phase 2 — Transformation**
Validate data during ETL processing.

**Phase 3 — Post-Migration (Target)**
Validate data after load into InsureMO.

### Step 6: Agent 7 Integration — Migration Impact

Migration is a cross-module event. Produce an impact summary for Agent 7:

| InsureMO Module | Migration Impact | Risk Level | Notes |
|----------------|-----------------|------------|-------|
| Product Factory | Product codes must pre-exist | High | Migration blocked if products not configured first |
| New Business | Policy number series must be reserved | High | |
| Party | Dedup logic must be configured | Medium | |
| Underwriting | Legacy UW decisions may not map to InsureMO rules | Medium | |
| Billing | Premium schedule migration requires active payment method | High | |
| Claims | Historical claims status codes need mapping | Medium | |
| CS / Policy Admin | Policy status codes must align | High | |

---

## Output Format

```markdown
# Data Migration Requirements Document
## Project: [Project Name]
## Source System: [Legacy System Name]
## Target System: InsureMO [version]
## Date: [YYYY-MM-DD]
## Status: Draft

---

## 1. Pre-flight Status

| Check | Status | Notes |
|-------|--------|-------|
| PF-01 Source system identified | ✅ / ⚠️ | |
| PF-02 Scope entities declared | ✅ / ⚠️ | |
| PF-03 Data volume estimate | ✅ / ⚠️ | |
| PF-04 Migration timeline | ✅ / ⚠️ | |
| PF-05 Gap Matrix cross-reference | ✅ / ⚠️ / N/A | |
| PF-06 Data dictionary provided | ✅ / ⚠️ | |

---

## 2. Migration Scope

[Entity table from Step 1]

---

## 3. Field Mapping Summary

| Status | Count | % of Total |
|--------|-------|-----------|
| DIRECT | XX | XX% |
| TRANSFORM | XX | XX% |
| LOOKUP | XX | XX% |
| CALCULATE | XX | XX% |
| MANUAL | XX | XX% |
| GAP (DATA_GAP) | XX | XX% |
| SKIP | XX | XX% |

---

## 4. Field Mapping Details

### 4.1 Policy Entity

| Legacy Field | Type | InsureMO Field | Mapping Type | Transformation Logic | Validation Rule |
|---|---|---|---|---|---|
| POL_NUM | String | PolicyNumber | DIRECT | — | Required, unique |
| ISSUE_DATE | Date | PolicyIssueDate | TRANSFORM | DD/MM/YYYY → YYYY-MM-DD | Valid date |
| SUM_ASSURED | Decimal | TotalSA | DIRECT | — | > 0 |

### 4.2 Party Entity
[Same structure]

### 4.3 Coverage Entity
[Same structure]

### 4.4 Premium Entity
[Same structure]

### 4.5 Claims Entity (if in scope)
[Same structure]

---

## 5. Data Cleansing Rules

| Rule ID | Entity | Issue Type | Field | Cleansing Rule | Classification | Owner |
|---------|--------|-----------|-------|----------------|----------------|-------|
| DCR-001 | Policy | Missing | PREMIUM | Calculate from coverage data | AUTO-CLEANABLE | Dev |
| DCR-002 | Party | Format | DOB | Convert to ISO 8601 | AUTO-CLEANABLE | Dev |
| DCR-003 | Policy | Duplicate | POL_NUM | Flag for manual review | MANUAL-REVIEW | BA |
| DCR-004 | Coverage | Invalid | OCC_CODE | Map to InsureMO 'Other' | BLOCKING | BA + UW |

---

## 6. Migration Gap Register

| Gap ID | Entity | Field | Description | Gap Type | Severity | Blocking? | Resolution | Owner | Resolve By |
|--------|--------|-------|-------------|----------|----------|-----------|------------|-------|-----------|
| DMG-001 | Policy | LEGACY_FLD | No InsureMO equivalent | SCHEMA_GAP | High | Yes | Manual re-entry | BA | YYYY-MM-DD |
| DMG-002 | Coverage | RIDER_TYPE | Code table mismatch | LOGIC_GAP | Medium | No | Lookup mapping | Dev | YYYY-MM-DD |

**Dev Gap Dependencies:**
| Migration Gap | Depends On (Gap Matrix) | Status |
|---------------|------------------------|--------|
| DMG-XXX | G-XXX (Dev Gap) | Pending dev completion |

---

## 7. Validation Criteria

### Phase 1 — Pre-Migration (Source)
- [ ] All required fields populated (per mandatory field list)
- [ ] Date formats valid and parseable
- [ ] Numeric values within expected ranges
- [ ] No duplicate policy/party records
- [ ] All BLOCKING cleansing rules resolved

### Phase 2 — Transformation
- [ ] All TRANSFORM mappings applied correctly
- [ ] All LOOKUP codes resolved to valid InsureMO values
- [ ] All CALCULATE fields produce non-null results
- [ ] Row count matches source extract count

### Phase 3 — Post-Migration (Target)
- [ ] Policies created in InsureMO with correct status
- [ ] Party links verified (Insured / Owner / Beneficiary)
- [ ] Coverage terms and SA amounts match source
- [ ] Premium schedules active and correct
- [ ] Product Factory product codes exist for all migrated products

---

## 8. Data Quality Targets

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Field Mapping Coverage | ≥ 95% | Mapped fields / Total source fields |
| Record Migration Success | 100% | Successfully migrated / Total records |
| Auto-Cleansing Rate | ≥ 85% | AUTO-CLEANABLE issues / Total issues |
| Post-Migration Validation | ≥ 99% | Records passing Phase 3 checks / Total |

---

## 9. Module Impact Summary (for Agent 7)

[Table from Step 6]

---

## 9.5: Migration Go / No-Go Decision Gate (NEW — v3.0)

> **必须在首次数据迁移执行前通过此 gate。**

```markdown
## Migration Go / No-Go Checklist

执行日期: YYYY-MM-DD | Gate 版本: v3.0

### Pre-Migration Quality Gates

| # | Gate Criterion | Threshold | Actual | Status | Owner |
|---|---------------|----------|--------|--------|-------|
| G-01 | 数据质量评分 | D2 Risk Score ≤ 2 | _ | ✅/❌ | _ |
| G-02 | Field Mapping Coverage | ≥ 95% DIRECT + TRANSFORM | _% | ✅/❌ | _ |
| G-03 | BLOCKING issues resolved | 0 remaining | _ | ✅/❌ | _ |
| G-04 | Archetype-specific check (per A1-A6) | All pass | _ | ✅/❌ | _ |
| G-05 | 试迁移（pilot）成功率 | ≥ 99% records | _% | ✅/❌ | _ |
| G-06 | Product Factory products configured | 100% migrated products | _% | ✅/❌ | _ |
| G-07 | Party dedup rules configured | Done | _ | ✅/❌ | _ |
| G-08 | RI treaty codes mapped | 100% RI records | _% | ✅/❌ | _ |
| G-09 | Claims status code mapping | 100% mapped | _% | ✅/❌ | _ |
| G-10 | 备用方案 documented | Fallback plan exists | _ | ✅/❌ | _ |

Go Decision:
  ✅ ALL gates pass → MIGRATE
  ❌ ANY gate fails → NO-GO → 修复后重新评估

Risk Index at this stage: _ (must be ≤ 1.75 for 🟡MEDIUM, ≤ 1.25 for 🟢LOW)
```

---

## 9.6: Migration Dependency Timeline (NEW — v3.0)

> 迁移不是独立事件——它的完成依赖于上游产品配置，同时下游的 UAT 和上线都依赖迁移完成。

```markdown
## Migration Dependency Timeline

Legend: [====] 依赖期  ● Go/No-Go Gate  ▼ 里程碑

Project Start ───────────────────────────────────────────────────────▶ Go-Live

[产品配置 (Agent 6)]
 ████████████████████████████████████

                        [Migration Data Prep]
                         ████████████████████
                                        ● G-01 to G-10 (Go/No-Go)
                                              ▼ Pilot Migration
                                           ████████████████
                                                       ▼ Full Migration
                                                    ████████████
                                                              ▼ SIT
                                                           ████
                                                              ▼ UAT
                                                            ████████
                                                                   ▼
                                                                Go-Live

### Critical Path Milestones

| Milestone | 依赖前置 | 最晚完成日 | 责任人 |
|-----------|---------|----------|--------|
| 产品配置完成 (Agent 6) | None | T-60 | Client/Dev |
| Migration Data Prep 完成 | PF-01~06 通过 | T-30 | Client |
| **Go/No-Go Gate 通过** | 所有Gates | T-14 | BA+Dev |
| Pilot Migration 完成 | Go/No-Go | T-10 | Dev |
| Full Migration 完成 | Pilot | T-3 | Dev |
| SIT 开始 | Migration | T | QA |
| UAT 开始 | SIT | T+5 | BA+Client |

T = Go-Live date

### Blocker Escalation Path

```
Migration blocker identified
    │
    ├── D1-D3 (Data Issue) → Data Steward → Resolve by T-20
    ├── D4-D6 (Config Issue) → Agent 6 → Resolve by T-30
    ├── D7-D8 (Dev Issue) → Agent 4 Tech Spec → Resolve by T-40
    └── D9-D10 (Business Decision) → Client → Resolve by T-45
```
```

---

## 9.7: Per-Life / Per-Coverage Semantic Pattern Library (NEW — v3.0)

> **保险迁移特有挑战**：per-life vs per-coverage 的语义差异是最常见的 migration gap 来源。
> 每个 pattern 必须显式检查，不能假设。

```markdown
## Semantic Pattern Checklist

执行时机: Step 2 (Field Mapping) 必须逐项确认

| Pattern ID | 语义场景 | 检查方法 | 风险级别 |
|-----------|---------|---------|---------|
| SP-001 | per-life vs per-coverage | 确认legacy系统是否按life聚合coverage，还是独立记录 | 🔴 High |
| SP-002 | Joint-Life 排序 | 检查legacy如何区分第一被保人和第二被保人 | 🔴 High |
| SP-003 | 跨policy累计（TI/Mortality） | 确认legacy是否维护跨policy累计值 | 🔴 High |
| SP-004 | 历史加费/除外  | 确认UW加费记录是否随policy迁移或仅最新状态 | 🟡 Medium |
| SP-005 | 投资账户单位价格 | 确认NAV日期是否与policy anniversary一致 | 🟡 Medium |
| SP-006 | 冷结账户标识 | 确认legacy如何标记失效policy（是否单独表） | 🟡 Medium |
| SP-007 | Currency/汇率来源 | 确认汇率取数来源（日期/系统） | 🟡 Medium |
| SP-008 | 宽限期/自动贷款 | 确认legacyAPL触发规则是否和InsureMO一致 | 🟡 Medium |
| SP-009 | 分红/红利累计方式 | 确认是否用复利或单利累计 | 🟢 Low |
| SP-010 | 受益人法定继承顺序 | 确认legacy是否维护继承顺序规则 | 🟢 Low |

**逐项确认记录:**

```markdown
| Pattern ID | Legacy行为确认 | InsureMO行为 | 一致性 | Gap ID | 行动 |
|-----------|--------------|------------|--------|--------|------|
| SP-001 | □ Yes □ No □ Unknown | Per-coverage | □ Match □ Mismatch □ Unknown | DMG-XXX | 制定转换逻辑 |
| SP-002 | □ Yes □ No □ Unknown | 第一被保人优先 | □ Match □ Mismatch □ Unknown | DMG-XXX | 对齐排序规则 |
| SP-003 | □ Yes □ No □ Unknown | 不支持跨policy | □ Match □ Mismatch □ Unknown | DMG-XXX | 明确无法迁移 |
| ... | | | | | |
```
```

---

## 10. UNKNOWN Register (Migration)

| ID | Issue | Impact | Status | Owner | Resolve By |
|----|-------|--------|--------|-------|-----------|
| UNKNOWN-MIG-001 | Data volume unknown | High — timeline risk | Open | [Name] | YYYY-MM-DD |
```

---

## Completion Gates

- [ ] CG-01  Pre-flight checklist completed and all ⚠️ items entered in UNKNOWN Register
- [ ] CG-02  All in-scope entities have a field mapping table
- [ ] CG-03  Every source field has an assigned mapping status (no blanks)
- [ ] CG-04  All BLOCKING cleansing issues have Owner and Resolve By date
- [ ] CG-05  Migration Gap Register is complete — no unclassified rows
- [ ] CG-06  Dev Gap dependencies are cross-referenced against approved Gap Matrix
- [ ] CG-07  Three-phase validation criteria defined (Pre / Transform / Post)
- [ ] CG-08  Data quality targets table is populated
- [ ] CG-09  Module Impact Summary section completed (for Agent 7 handoff)
- [ ] CG-10  Field Mapping Summary totals are consistent with detail tables
- [ ] CG-11  Document version, source system, and date populated in header

---

## Related Files

| Direction | File | Purpose |
|-----------|------|---------|
| Input | Legacy data dictionary | Source field definitions |
| Input | InsureMO Product Factory config | Target field reference |
| Cross-ref | Approved Gap Matrix | Dev gap dependency check |
| Parallel | Agent 7 (Impact Analysis) | Migration impact on all modules |
| Downstream | Agent 4 (Tech Spec) | Custom ETL / transformation logic may require Dev |
| Downstream | Agent 6 (Config Runbook) | Product Factory products must be configured before migration |
