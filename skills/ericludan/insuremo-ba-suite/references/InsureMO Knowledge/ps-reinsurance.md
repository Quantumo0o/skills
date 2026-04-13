# InsureMO Platform Guide — Reinsurance (RI)
# Source: Reinsurance User Guide (Gemini V3)
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb.md instead
# Version: 1.0 | Created: 2026-04-08

---

## Purpose of This File

This file answers **"how does Reinsurance work in InsureMO"** — cession rules, treaty/facultative structures, RI accounting, SAR calculation, and RI configuration paths.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a RI-related gap
- Agent 6 is generating a **Config Runbook** for RI configuration items
- A BA needs to verify RI cession logic before classifying a requirement as Dev Gap

---

## Module Overview

```
Reinsurance (RI) Module
│
├── RI Setup                  ← Reinsurer + Treaty configuration
├── RI Cession               ← Automatic / Facultative cession per policy
├── RI Accounting             ← RI premium / claim settlement
├── RI Reporting              ← SAR calculation, RI schedule generation
└── RI Query                 ← RI position and history
```

---

## Key Concepts

### RI Cession Types

| Type | Description | Trigger |
|------|-------------|---------|
| **Automatic Treaty** | Policy automatically ceded to treaty if criteria met | Product config + UW decision |
| **Facultative** | Manual decision per policy | Underwriter decision |
| **Quota Share** | Fixed % of premium and benefit ceded | Treaty config |
| **Surplus Reinsurance** | Cedant retains surplus above RI's share | Treaty config |
| **YRT (Yearly Renewable Term)** | Renewable term reinsurance | Product config |

### SAR (Sum at Risk)

SAR = Sum Assured (SA) − Reserve (PFV)

| Scenario | SAR Calculation |
|---------|---------------|
| Death claim | SA at date of death − Reserve at date of death |
| TI claim | SA at TI diagnosis date − Reserve at TI date |
| Maturity | SAR = 0 (no death benefit) |
| Surrender | SAR = 0 (no protection) |
| Rider | Rider SA − Rider Reserve |

---

## RI Cession Rules

### Automatic Cession Trigger
A policy is automatically ceded when ALL of:
1. Product RI Indicator = Y
2. SA / Premium exceeds automatic treaty threshold
3. UW decision = Accepted
4. Policy is in-force

### Cession Amount
| Cession Type | Formula |
|---|---|
| Quota Share | Cession % x Premium AND Cession % x SA |
| Surplus | (SA − Surplus Retention) x RI's share % |
| YRT | RI rate x SA (per 1000 or per unit) |



## Treaty Configuration

### Treaty Setup Screen
Path: Reinsurance > Configuration > Treaty Setup

Key fields:
| Field | Rule | Mandatory |
|---|---|---|
| Treaty Code | Unique identifier | Y |
| Treaty Type | Quota Share / Surplus / YRT | Y |
| Reinsurer Code | From reinsurer table | Y |
| RI Share % | 0-100% | Y |
| Retention Limit | Max cedant retains per policy | Y |
| Min SA for Cession | Threshold to trigger treaty | Y |
| Max SA for Cession | Upper limit of treaty coverage | Y |
| Max Cession % | Treaty-level cap | Y |



## RI Accounting

### RI Premium Flow
| Event | RI Action |
|---|---|
| Policy Inforce | RI premium calculated and ceded |
| Premium Received | RI share credited to RI account |
| Death Claim | RI share of claim = RI % x Death Benefit |
| TI Claim | RI share = RI % x TI Benefit |
| Maturity | No RI payment (protection ended) |
| Surrender | No RI payment (no protection) |
| Policy Lapse | RI reserve returned to cedant |

### RI Commission
| Type | Calculation |
|---|---|
| Override Commission | RI % x Premium x Override Rate |
| Profit Commission | (RI Premium − RI Claims − RI Expenses) x PC % |


## SAR Calculation (from RI UG)

### SAR at Each Valuation Date
System calculates SAR on:
- Daily: For daily RI accounting
- Monthly: For RI statement generation
- Event-triggered: On claim, surrender, maturity

| Event | SAR Formula |
|---|---|
| Death claim | SA at date of death − Reserve (PFV) at date of death |
| TI claim | SA at TI diagnosis − Reserve at TI diagnosis date |
| Surrender | SAR = 0 (protection not applicable) |
| Maturity | SAR = 0 (end of protection) |
| Lapse | SAR = 0 (date of lapse) |



## Facultative Reinsurance

### Facultative vs Automatic
| Feature | Automatic | Facultative |
|---|---|---|
| Trigger | Product config + threshold | Manual UW decision |
| Rate | Treaty rate | Negotiated rate |
| Approval | Auto if within treaty limits | Always requires approval |
| Cover | Up to treaty max | No treaty limit |

### Facultative Workflow
1. UW flags policy for facultative referral
2. RI team reviews and quotes
3. Quote accepted → facultative cover note generated
4. Policy inforced with facultative cession
