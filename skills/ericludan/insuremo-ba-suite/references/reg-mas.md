# MAS Regulatory Requirements — Singapore
# Source: Monetary Authority of Singapore Guidelines V26.03
# Scope: BA knowledge base for Agent 3 (Regulatory Compliance)
# Version: 2.0 | Updated: 2026-03

---

## Purpose

Regulatory requirements for Singapore market (MAS). Current as of March 2026.

---

## Regulatory Framework

| Authority | Scope |
|-----------|-------|
| **MAS** | Monetary Authority of Singapore — primary insurance regulator |
| **SGX** | Singapore Exchange — investment-linked products |
| **CCCS** | Competition Commission — market conduct |
| **MOH** | Ministry of Health — CareShield Life + Integrated Shield Plan co-regulation |

---

## Key MAS Requirements

### 1. Policy Illustration & Disclosure

| Requirement | Description | Applies To |
|------------|-------------|-------------|
| Policy Illustration | Projected returns: worst, best, most likely scenarios | All life insurance |
| Fund Performance | Past performance with disclaimer | ILP |
| Fee Disclosure | All charges clearly disclosed | All products |
| Cooling-off Period | 14 days to cancel | All products |

### 2. Underwriting

| Requirement | Description |
|-------------|-------------|
| Medical Reinsurance | Reinsurance arrangements disclosed |
| Occupation Loading | Justified with actuarial basis |
| Non-disclosure | Clear disclosure requirements |

### 3. Claims

| Requirement | Description |
|-------------|-------------|
| Claims Processing Time | 30 days for simple claims |
| Investigation Period | Up to 6 months for complex claims |
| Fraud Detection | Mandatory anti-fraud procedures |

### 4. ILP (Investment-Linked Policy)

| Requirement | Description |
|-------------|-------------|
| Fund Switching | Max 12 free switches per year |
| Bid/Ask Spread | Max 5% |
| Performance Disclosure | 1Y, 3Y, 5Y returns mandatory |
| Risk Coverage | Minimum 5% of total premium to protection |
| Fund Lock-in | Cannot exceed 10 years |
| Sales Charge | Maximum 90% of first year premium |

### 5. AI Risk Management — 2026 Focus 🆕

| Requirement | Description |
|-------------|-------------|
| AI Model Risk Management Guidelines | MAS published guidelines Dec 2024; consultation closed Jan 2026; full framework in effect |
| Principles-Based Framework | Technology-neutral; operates alongside FEAT Principles and Veritas Initiative |
| Underwriting / Claims AI | Insurers must set clear boundaries on automated tools influencing underwriting or claims decisions |
| Model Monitoring | Regular monitoring for errors; strong controls over data use and privacy |
| Regulatory Evolution | AI regulatory landscape expected to evolve rapidly through 2026 and beyond |

### 6. Digital Distribution — e-Commerce (Feb 2026 Parliamentary Clarification) 🆕

| Requirement | Description |
|-------------|-------------|
| No New Legislation Planned | MAS confirmed (Feb 12, 2026 parliamentary sitting) no immediate plan to amend Insurance Act for e-commerce distribution |
| Existing Safeguards Apply | All financial institutions distributing via digital / e-commerce platforms must meet conduct standards regardless of channel |
| Agent Registration | General insurance agents distributing online must be registered with GIA's Agents' Registration Board |
| Technology-Neutral | MAS supervisory approach: conduct expectations apply consistently across all distribution channels |
| Monitoring | MAS will introduce additional protections if digital distribution risks materialise |

### 7. Recovery and Resolution Planning

| Requirement | Description |
|-------------|-------------|
| MAS Notice 134 | Notified insurers must comply with Recovery and Resolution Planning (RRP) |
| RRP Guidelines | Effective 1 Jan 2025; guidance on requirements under MAS Notice 134 |
| Purpose | Reduce systemic risk; ensure continuity of critical economic functions; enable orderly restructuring |

### 8. Climate Risk — Growing Regulatory Focus 🆕

| Requirement | Description |
|-------------|-------------|
| Physical + Transition Risk | Insurers expected to assess climate risks in underwriting and investment portfolios |
| Greenwashing | MAS increasing focus on greenwashing risks; insurers must ensure ESG claims are substantiated |
| Climate Disclosure | TCFD-aligned disclosures expected for larger insurers |
| Nat Cat Exposure | Insurance and reinsurance market facing increased scrutiny on natural catastrophe pricing and capacity |

### 9. CareShield Life / LTC (MOH + MAS Co-Regulation)

| Requirement | Description |
|-------------|-------------|
| CareShield Life | Mandatory national LTC scheme; all citizens/PRs born 1980+ auto-enrolled |
| Severe Disability Trigger | Inability to perform 3 or more Activities of Daily Living (ADLs) |
| Benefit Amount | S$600/month (2020 base); increases ~2% per year |
| CareShield Life Supplement (CSLS) | Private insurers may offer supplements; MOH approval required |
| ElderShield | Legacy scheme (born 1979 and earlier); private insurers continue managing |

### 10. Integrated Shield Plan (ISP — MOH + MAS)

| Requirement | Description |
|-------------|-------------|
| Structure | Rider on top of MediShield Life; administered by MOH / CPF Board |
| Full Rider Ban | Full-rider plans (no co-payment) disallowed since 2019; only co-payment ISP riders permitted |
| Claims Processing | Via MediShield Life claims system; insurer must integrate with MOH/CPF Board |
| Premium Adjustment | Insurers must notify policyholders at least 60 days before ISP premium adjustment |

### 11. Compliance Toolkit Update (Feb 2026) 🆕

| Item | Notes |
|------|-------|
| MAS Compliance Toolkit | Last revised 9 Feb 2026; guides direct insurers' and reinsurers' compliance with MAS approval and reporting requirements |
| Use in InsureMO | Agent 3 should reference current toolkit version when answering compliance questions |

---

## Product-Specific Requirements

### Critical Illness

| Requirement | Notes |
|-------------|-------|
| Definition | Must follow LIA 37 critical illness definitions (updated; previously 25) |
| Survival Period | Typically 30 days |
| Exclusion Period | Standard exclusions apply |

### Direct Purchase Insurance (DPI)

| Requirement | Notes |
|-------------|-------|
| Products | Term life and whole life sold without financial adviser |
| Disclosure | Simplified product highlights sheet required |
| Limits | Sum assured limits apply per MAS DPI framework |

---

## Data Protection

| Requirement | Status | Notes |
|-------------|--------|-------|
| PDPA (2012 + 2020 Amendment) | ✅ | Mandatory breach notification within 3 business days for breaches affecting 500+ or causing significant harm |
| Deemed Consent | ✅ | Contractual necessity basis (2020 amendment) |
| Data Portability | ✅ | Phased implementation; right to transfer data to another organisation |
| Data Retention | 6 years | |
| FATCA | ✅ | IGA jurisdiction |
| CRS | ✅ | Participant |
| MyInfo Integration | ✅ | SingPass MyInfo for KYC; customer consent required |

---

## Common Config Gaps

| Scenario | Gap Type | Solution |
|----------|----------|----------|
| AI model decision boundaries in underwriting/claims | Config | Flag automated decision points; audit trail for AI-driven outcomes |
| CareShield Life Supplement product setup | Config | MOH-approved product; disability trigger (3 ADLs); monthly benefit |
| ISP co-payment configuration | Config | ISP product: mandatory co-payment; no full-rider without co-payment |
| Recovery and Resolution Plan data | Config | Policy data export for RRP reporting requirements |
| MAS Compliance Toolkit alignment | Config | Annual review against latest toolkit version (last revised Feb 2026) |
| e-Commerce embedded insurance conduct | Config | Conduct standard applies regardless of channel; same disclosure requirements |
| PDPA breach notification workflow | Config | Incident response → breach notification within 3 business days if threshold met |
| MyInfo integration for KYC | Integration | SingPass MyInfo API for eKYC; consent capture required |
| Custom ILP fund creation | Config | SGX-approved fund list |
| MAS disclosure template | Config | MAS-compliant product illustration template |

---

## INVARIANT Declarations

```
INVARIANT 1: ISP co-payment is mandatory; full-rider plans (no co-payment) are not permitted
  Source: MOH/MAS rule effective 2019
  Effect: ISP product config must enforce minimum co-payment; full-rider cannot be configured

INVARIANT 2: CareShield Life Supplement requires MOH approval before launch
  Source: MOH CareShield Life framework
  Effect: CSLS product cannot be sold without documented MOH approval

INVARIANT 3: AI automated tools influencing underwriting or claims must have clear operational boundaries
  Source: MAS AI Model Risk Management Guidelines (Dec 2024; effective 2026)
  Effect: Any AI-driven decision in underwriting or claims must have documented boundaries,
          monitoring controls, and override capability

INVARIANT 4: MAS conduct standards apply to ALL distribution channels including e-commerce
  Source: MAS parliamentary clarification Feb 12, 2026
  Effect: No reduced disclosure or conduct standards for digital/embedded insurance distribution

INVARIANT 5: Recovery and Resolution Plan must be maintained by notified insurers
  Source: MAS Notice 134 + RRP Guidelines (effective 1 Jan 2025)
  Effect: Designated insurers must have current RRP; InsureMO data must support RRP reporting
```

---

## 2026 Regulatory Themes (MAS)

| Theme | Description |
|-------|-------------|
| AI Regulation | Rapid evolution expected; principles-based now, more specific rules likely |
| Climate Risk | Nat Cat exposure, greenwashing scrutiny, TCFD disclosure |
| Digital Distribution | No new law; existing conduct standards apply to all channels |
| Emerging Markets | SEA growth markets attracting Singapore hub activity |
| Financial Stability | Tighter economic environment; political uncertainty; trade frictions |

---

## References

- MAS Insurance Act (Cap. 142)
- MAS Notice 307 — Policy Illustration
- MAS Notice 134 — Recovery and Resolution Planning
- **MAS AI Model Risk Management Guidelines (Dec 2024; effective 2026)**
- **MAS Compliance Toolkit (revised 9 Feb 2026)**
- **MAS Parliamentary Clarification on e-commerce insurance (Feb 12, 2026)**
- LIA Critical Illness Definition (LIA 37)
- MOH CareShield Life Framework
- PDPA 2012 + 2020 Amendment
