# Delivery Traceability Map
# Version: 1.0 | Updated: 2026-04-03
# Purpose: Single source of truth for tracking every requirement item across the full InsureMO delivery chain

---

## Concept

Every discrete requirement / business rule starts as a line item in the Gap Matrix and evolves through a defined chain:

```
Requirement
    │
    ├──→ Gap Matrix (Agent 1)          ← Gap ID + Classification + Solution Design
    │       │
    │       ├──→ BSD (Agent 2)         ← BSD ID + Rules + Compliance Check (Agent 3)
    │       │       │
    │       │       ├──→ Tech Spec (Agent 4) ← Dev items only
    │       │       │
    │       │       └──→ Config Runbook (Agent 6) ← Config items only
    │       │
    │       └──→ Cross-Module Impact (Agent 7) ← Ripple analysis
    │
    ├──→ UAT (Agent 8)                 ← Test scenarios linked to Gap ID
    │
    └──→ Data Migration (Agent 9)        ← if legacy migration required
```

**The Traceability Map keeps every item at every stage visible — no requirement falls through the cracks.**

---

## Master Traceability Table Format

```markdown
# [Project Name] — Delivery Traceability Map
Version: X.X | Date: YYYY-MM-DD | BA: [Name] | Status: [Draft/In Progress/Complete]

Legend:
  Classification: OOTB / CONFIG / DEV / PROCESS / UNKNOWN
  Stage: ████ = Complete | ▓▓▓▓ = In Progress | ░░░░ = Pending | ✗ = Not Applicable

────────────────────────────────────────────────────────────────────────────────
│ Item ID │ Requirement │ Gap Cls │ Solution    │ BSD  │ Tech  │ Config │ UAT  │
│         │ (Feature)   │        │ Design      │ (v)  │ Spec  │ (v)   │      │
├─────────┼────────────┼────────┼────────────┼──────┼───────┼────────┼──────┤
│ PS3_001 │ SA Change  │ CONFIG │ Agent7 ✓    │ v1.2 │ N/A   │ v2.0  │ ✅   │
│         │ Eff Date   │        │             │      │       │        │      │
├─────────┼────────────┼────────┼────────────┼──────┼───────┼────────┼──────┤
│ VUL_PREM│ Top-up    │ DEV    │ Agent7 ✓    │ —    │ v0.8  │ —     │ 🔄   │
│ _003    │ frequency │        │             │      │       │        │      │
├─────────┼────────────┼────────┼────────────┼──────┼───────┼────────┼──────┤
│ VUL_BEN │ Mature    │ OOTB   │ No change   │ N/A  │ N/A   │ N/A   │ N/A  │
│ _001    │ benefit   │        │             │      │       │        │      │
└─────────┴────────────┴────────┴────────────┴──────┴───────┴────────┴──────┘

Stage Legend:
  BSD: vX.X = versioned | ✅ = Signed off | 🔄 = In Progress | ✗ = Not Applicable | — = Not yet started
  Tech Spec: vX.X = versioned | ✅ = Signed off | 🔄 = In Progress | ✗ = N/A
  Config: vX.X = versioned | ✅ = Signed off | 🔄 = In Progress | ✗ = N/A
  UAT: ✅ = Passed | 🔄 = In Progress | ✗ = N/A | — = Not yet started

Open UNKNOWNs in this project:
  │ Item ID  │ UNKNOWN ID │ Question                            │ Severity │ Status │ SLA    │
  │ PS3_001  │ UNKNOWN-003│ SAR 12M formula — exact multiplier? │ High    │ Open   │ T+2d   │
  │ VUL_PREM_003 │ UNKNOWN-005 │ Top-up min amount — TBD from client │ Medium │ Open   │ T+5d   │
```

---

## Per-Stage Linkage Format

For each item in the Master Table, the detailed chain is:

```markdown
## [Item ID]: [Requirement Summary]

### Chain
Gap Matrix → [Gap Matrix file]
  └─→ BSD → [BSD file] (vX.X, signed off: Y/N)
        └─→ Tech Spec → [Tech Spec file] (vX.X, signed off: Y/N) [if DEV]
        └─→ Config Runbook → [Config file] (vX.X, signed off: Y/N) [if CONFIG]
  └─→ Agent 7 Impact → [Impact doc]
  └─→ UAT Scenarios → [UAT file] (N scenarios: X P0 passed / Y total)
  └─→ Data Migration → [Migration doc] [if applicable]

### UNKNOWN Register Linkage
  └─→ [UNKNOWN-XXX] — [Question summary] — Status: [Open/Resolved]
        Resolved From: [Source] on [YYYY-MM-DD]

### Compliance Linkage (Agent 3)
  └─→ [C-XXX] — [Compliance item] — Status: [Compliant/Config Needed/Dev Required]

### Open Issues
  - [Issue description] — Owner: [Name] — Due: [YYYY-MM-DD]
```

---

## Weekly Status Summary Section

```markdown
## Weekly Status Summary — YYYY-WXX

**Report Date:** YYYY-MM-DD
**Reporting Period:** YYYY-MM-DD → YYYY-MM-DD
**Prepared By:** [Name]

### Deliverable Progress

| Deliverable          │ Count │ Complete │ In Progress │ Pending │ Blocked │
|---------------------│------:│--------:│-----------:│--------:│--------:│
| Gap Matrix Items    │   XX  │     XX  │     XX     │   XX    │    XX   │
|  └─ OOTB            │   XX  │     XX  │      -     │   XX    │    -    │
|  └─ CONFIG          │   XX  │     XX  │     XX     │   XX    │    XX   │
|  └─ DEV             │   XX  │     XX  │     XX     │   XX    │    XX   │
|  └─ UNKNOWN         │   XX  │     XX  │      -     │   XX    │    -    │
| BSD Documents       │   XX  │     XX  │     XX     │   XX    │    -    │
| Tech Specs          │   XX  │     XX  │     XX     │   XX    │    -    │
| Config Runbooks     │   XX  │     XX  │     XX     │   XX    │    -    │
| UAT Scenarios       │   XX  │     XX  │     XX     │   XX    │    -    │
│ Migration Docs      │   XX  │     XX  │     XX     │   XX    │    -    │

### UNKNOWN Health

| Metric                       │ This Week │ Last Week │
|-----------------------------│----------:│----------:│
| Total OPEN UNKNOWNs         │        XX │        XX │
| New UNKNOWNs created        │        XX │        XX │
| UNKNOWNs resolved           │        XX │        XX │
| UNKNOWNs overdue (SLA breach)│        XX │        XX │
| High-severity OPEN          │        XX │        XX │

### Ripple Risk Summary (Agent 7)

| Risk Chain         │ Risk Level │ Status     │ Mitigation           │
|--------------------│-----------│------------│---------------------│
| PF→UW→RI→UW ⚡     │ 🔴 High   │ Open       │ Circuit breaker at 2 │ │
| PF→NB→CS→Billing   │ 🟡 Medium │ Mitigated  │ Defined stop condition │

### Go-Live Readiness

| Check                           │ Status    │ Notes                    │
|--------------------------------│-----------│--------------------------│
| All OOTB items confirmed       │ ✅ / ⚠️   │                          │
| All CONFIG items configured    │ ✅ / ⚠️   │                          │
| All DEV items coded + tested   │ ✅ / ⚠️   │                          │
| All UNKNOWNs resolved          │ ✅ / ⚠️   │                          │
| UAT P0 scenarios passed        │ ✅ / ⚠️   │ X/Y passed               │
| Migration Go/No-Go passed      │ ✅ / ⚠️ / N/A │                    │
| Compliance checklist complete  │ ✅ / ⚠️   │                          │
```

---

## Agent Integration Points

### Agent 5 (Product Spec Decoder) → Creates Initial Entry (via Product Profile)
```
Agent 5 output: Product Profile (PRODUCT_PROFILE)
    │
    └─→ 在 Traceability Map 中:
          Product Profile 版本: vX.X
          Spec Quality Score: 🟢/🟡/🔴
          Market-Specific UNKNOWNs: HK/SG/MY各几条
          Formula Conflicts Detected: FC-01~FC-06
          Recommended Route: Agent 1 (if 🟢/🟡) / BLOCKED if FC-03 found
    │
    └─→ 如果 Spec Quality = 🔴 LOW:
          → 明确标注 NOT SUITABLE FOR CONFIG CLASSIFICATION
          → Agent 1 改用 UNKNOWN-FIRST 方法
    └─→ 如果 FC-03 (Mutual Exclusivity Conflict) found:
          → BLOCKED — escalate to client before any downstream work
```

### Agent 1 (Gap Analysis) → Creates Initial Entry
```
输出 Gap Matrix 时:
  └─→ 在 Traceability Map 中为每个 Gap ID 创建一行
  └─→ Item ID = Gap ID
  └─→ Gap Class = OOTB/CONFIG/DEV/UNKNOWN
  └─→ Solution Design = Agent7输出引用
  └─→ BSD Status = ✗ (Pending)
  └─→ Tech Spec Status = ✗ (Pending)
  └─→ Config Status = ✗ (Pending)
  └─→ UAT Status = ✗ (Pending)
```

### Agent 2 (BSD) → Updates Traceability
```
BSD 签署时:
  └─→ Traceability Map 中:
        BSD Status → vX.X
        BSD Signed Off → ✅
  └─→ 如有 NEW UNKNOWN → 同时在 UNKNOWN Register 中创建条目
  └─→ 如有 Compliance Item → 记录在 Compliance Linkage 列
```

### Agent 3 (Compliance) → Links to Traceability
```
合规审查完成时:
  └─→ Traceability Map 中为每个 compliance item 创建一行
  └─→ Compliance ID = C-XXX format
  └─→ Status: Compliant / Config Needed / Dev Required
  └─→ Links back to Gap ID(s) affected
```

### Agent 4 (Tech Spec) → Updates Traceability
```
Tech Spec 签署时:
  └─→ Traceability Map 中:
        Tech Spec Status → vX.X
        Tech Spec Signed Off → ✅
  └─→ 确保对应的 Gap ID 行已更新
```

### Agent 6 (Config) → Updates Traceability
```
Config Runbook 签署时:
  └─→ Traceability Map 中:
        Config Status → vX.X
        Config Signed Off → ✅
```

### Agent 7 (Ripple) → Updates Traceability
```
Ripple 分析完成时:
  └─→ 在 Traceability Map 中:
        记录 Ripple Risk Level
        记录 Feedback Loop ⚡ 标识
        更新受影响模块的 Cross-Module 列
```

### Agent 8 (UAT) → Updates Traceability
```
UAT 完成时:
  └─→ Traceability Map 中:
        UAT Status → ✅ (passed) / 🔄 (in progress)
        P0 scenarios passed: X / Y total
```

### Agent 9 (Migration) → Links to Traceability
```
Migration 分析完成时:
  └─→ 在 Traceability Map 中为迁移相关 Gap ID 标注:
        Migration Status: vX.X / ✅ Complete / 🔄 In Progress
  └─→ Go/No-Go Gate 结果记录在 Weekly Summary
```

---

## Traceability Quality Gates

- [ ] Every Gap ID has a corresponding row in the Traceability Map
- [ ] Every row has at least one downstream artifact (BSD / Config / Tech Spec)
- [ ] UNKNOWN items are cross-linked between Traceability Map and UNKNOWN Register
- [ ] Compliance items (Agent 3) are linked to relevant Gap IDs
- [ ] No item is marked "Complete" (✅) unless all downstream stages are signed off
- [ ] Weekly Status Summary is updated at end of each working week
- [ ] Ripple Risk section is updated when Agent 7 analysis is completed
- [ ] Go/No-Go Gate result is recorded in the Weekly Summary before migration execution
- [ ] UAT pass/fail is recorded per item (not just at project level)

---

## Usage in Project Reviews

**In weekly sync:** Show Weekly Status Summary section — focus on:
1. NEW OPEN UNKNOWNs this week
2. Items blocked by unresolved UNKNOWNs
3. 🔴 Ripple Risk chains
4. Go-Live readiness checklist progress

**In milestone review:** Show full Master Traceability Table — every row reviewed
**In go/no-go meeting:** Show Weekly Status Summary → Migration section + Go/No-Go Gate results
