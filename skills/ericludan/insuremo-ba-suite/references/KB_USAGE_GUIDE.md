# Knowledge Base Usage Reference
# Version: 2.0 | Updated: 2026-04-03

## Core KB (Always Required)

| Knowledge Base | 适用场景 |
|---------------|---------|
| `references/InsureMO Knowledge/insuremo-ootb.md` | 所有产品 - OOTB判断 |
| `references/InsureMO Knowledge/ps-new-business.md` | 所有产品 - NB发单条件 |
| `references/InsureMO Knowledge/ps-underwriting.md` | 所有产品 - 核保规则 |
| `references/InsureMO Knowledge/ps-customer-service.md` | 所有产品 - 客服模块 |
| `references/InsureMO Knowledge/ps-billing-collection-payment.md` | 所有产品 - 账单/收费 |

## Module-Specific KB

| 产品类型/模块 | 必须读取的KB |
|--------------|-------------|
| **VUL/ILP** | references/InsureMO Knowledge/ps-investment.md + references/InsureMO Knowledge/ps-fund-administration.md + cs + nb + uw |
| **UL (Whole Life)** | references/InsureMO Knowledge/ps-customer-service.md + references/InsureMO Knowledge/ps-billing-collection-payment.md |
| **Term Life** | references/InsureMO Knowledge/ps-renew.md + references/InsureMO Knowledge/ps-underwriting.md |
| **Health/Medical** | references/InsureMO Knowledge/ps-underwriting.md + references/InsureMO Knowledge/ps-new-business.md |
| **Annuity** | references/InsureMO Knowledge/ps-annuity.md |
| **Bonus/Dividend** | references/InsureMO Knowledge/ps-bonus-allocate.md |
| **Loan** | references/InsureMO Knowledge/ps-loan-deposit.md |
| **Claims** | references/InsureMO Knowledge/ps-claims.md |

## Analysis Type → KB Mapping

### 1. 产品文档分析 (完整流程)

```
步骤1: 判断产品类型
步骤2: 读取 core KB (NB/UW/CS/BCP)
步骤3: 读取 module-specific KB
步骤4: 读取 reg-[market].md
```

| 产品类型 | Core KB | Module KB |
|----------|---------|-----------|
| VUL/ILP | NB+UW+CS+BCP | Investment + Fund Admin |
| UL | NB+UW+CS+BCP | (无专门) |
| Term Life | NB+UW+CS+BCP | Renewal |
| Health | NB+UW+CS+BCP | (无专门) |
| Annuity | NB+UW+CS+BCP | Annuity |

### 2. 明确需求分析

根据需求描述判断涉及的模块，读取对应KB：

| 需求关键词 | 可能涉及的模块 | KB文件 |
|-----------|---------------|--------|
| "coverage term" | NB | references/InsureMO Knowledge/ps-new-business.md |
| "underwriting" | UW | references/InsureMO Knowledge/ps-underwriting.md |
| "claim" | Claims | references/InsureMO Knowledge/ps-claims.md |
| "surrender" | CS | references/InsureMO Knowledge/ps-customer-service.md |
| "premium" | BCP | references/InsureMO Knowledge/ps-billing-collection-payment.md |
| "fund" | Investment | references/InsureMO Knowledge/ps-investment.md |

### 3. 法规合规检查

| 市场 | KB文件 |
|------|--------|
| Singapore | reg-mas.md |
| Malaysia | reg-bnm.md |
| Hong Kong | reg-hkia.md |
| Vietnam | reg-oid.md |
| Indonesia | reg-ojk.md |

---

## InsureMO V3 User Guide — Secondary KB (for Cross-Reference)

> The V3 User Guide is used in **Step 2B.5** of Agent 1 as a secondary cross-reference.
> It does NOT replace InsureMO Knowledge — it validates or challenges InsureMO Knowledge findings.

### V3 vs InsureMO Knowledge — When to Use Each

| KB | Role | Used In |
|----|------|---------|
| **InsureMO Knowledge** (ps-*.md) | Primary source — first-pass classification | Agent 1 Step 2B |
| **InsureMO V3 User Guide** (insuremo-v3-ug-*.md) | Secondary validation — second-pass cross-reference | Agent 1 Step 2B.5 |

### V3 File → Module Mapping

| Feature / Module | V3 File |
|-----------------|---------|
| NB screens, data entry, submission | `insuremo-v3-ug-nb.md` |
| CS alterations, surrender, fund switch | `insuremo-v3-ug-cs-new.md` |
| Underwriting rules | `insuremo-v3-ug-nb.md` (UW section) |
| Collection, billing schedule | `insuremo-v3-ug-collection.md` |
| Fund administration, ILP account | `insuremo-v3-ug-fund-admin.md` |
| Sales channel, agent management | `insuremo-v3-ug-sales-channel.md` |
| Premium payment | `insuremo-v3-ug-payment.md` |
| Renewal process | `insuremo-v3-ug-renewal.md` |
| Bonus / dividend allocation | `insuremo-v3-ug-bonus.md` |
| Maturity / survival benefit | `insuremo-v3-ug-maturity.md`, `insuremo-v3-ug-survival-payment.md` |
| Loan / deposit | `insuremo-v3-ug-loan-deposit.md` |
| Reinsurance cession | `insuremo-v3-ug-reinsurance.md` |
| GL posting, accounting | `insuremo-v3-ug-posting-gl.md` |
| Policy query | `insuremo-v3-ug-query.md` |
| Component rules | `insuremo-v3-ug-component-rules.md` |
| Life (LS) Product Definition | `insuremo-v3-ls-product-definition.md` |
| Life (LS) System Config | `insuremo-v3-ls-system-config.md` |
| Life (LC) System Config | `insuremo-v3-lc-system-config.md` |
| Product Factory (PF) Product Definition | `insuremo-v3-pf-product-definition.md` |
| Product Factory (PF) System Config | `insuremo-v3-pf-system-config.md` |

### V3 Override Priority (Agent 1 Step 2B.5 Rules)

| ps-docs says | V3 says | Final |
|---|---|---|
| OOTB / Config | V3-OOTB / V3-Config | No change |
| OOTB | V3-Config | **Config** |
| OOTB | **V3-Dev** | **Dev Gap** |
| Config | **V3-Dev** | **Dev Gap** |
| UNKNOWN | V3-OOTB/Config/Dev | Resolves to V3 finding |
| **Dev Gap** | **Any V3** | **Dev Gap** (V3 cannot override) |

**Key rule: ps-docs Dev Gap is bulletproof — V3 never downgrades it.**

### V3 Cross-Reference Output Format

In Gap Matrix notes column, add:
```
V3 Ref: [v3-ug-xxx.md]
V3 Finding: [V3-OOTB / V3-Config / V3-Dev / V3-UNKNOWN]
V3 Override Applied: [YES / NO]
V3 Evidence: [quote from V3 that drove the override]
```

---

## Quick Decision Tree

```
产品分析时：
1. 先读 core KB: NB + UW + CS + BCP
2. 判断产品类型:
   ├── VUL/ILP → + Investment + Fund Admin
   ├── Term Life → + Renewal
   ├── Annuity → + Annuity
   ├── Bonus → + Bonus
   └── (任何产品涉及理赔) → + Claims
3. 读 reg-[market].md
4. 分析跨模块影响 (Agent 7)
5. 有旧系统迁移 → 触发 Agent 9 + 读 ps-claims (if claims in scope)
```

---

## 实际使用统计 (改进后)

| 分析任务 | 应该使用 | 改进前 | 改进后 |
|----------|----------|---------|--------|
| HSBC VUL (PDF) | ootb + NB + UW + CS + BCP + mas + investment + fund | ootb + mas + PF | ✅ 完整 |
