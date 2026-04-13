# Common SEA Regulatory Framework
# Source: Regional Regulatory Guidelines V26.03
# Scope: BA knowledge base for Agent 3 (Regulatory Compliance)
# Version: 2.0 | Updated: 2026-03

---

## Purpose

Common regulatory framework applicable across SEA markets: Singapore (SG), Malaysia (MY), Thailand (TH), Philippines (PH), Indonesia (ID), Vietnam (VN).

---

## Agent 3 Routing Table

| Trigger Keyword | File to Load |
|----------------|-------------|
| "MAS", "Singapore", "SG" | reg-mas.md |
| "BNM", "Malaysia", "MY", "Takaful Malaysia" | reg-bnm.md |
| "OJK", "Indonesia", "ID", "Takaful Indonesia" | reg-ojk.md |
| "ISA", "Vietnam", "VN", "MoF Vietnam" | reg-oid.md |
| "HKIA", "Hong Kong", "HK", "Insurance Authority" | reg-hkia.md |
| "ILAS", "IUL", "Class C", "RBC Hong Kong", "GBA" | reg-hkia.md |
| "PDPA", "data protection", "CRS", "FATCA" | reg-sea-common.md |
| "IFRS 17", "MFRS 17", "SFRS 17" | reg-sea-common.md + market file |
| "Takaful", "Sharia" | reg-bnm.md (MY) or reg-ojk.md (ID) |

---

## Common Regulatory Principles

### 1. Customer Due Diligence

| Requirement | SG | MY | TH | PH | ID | VN | HK |
|-------------|----|----|----|----|----|----|-----|
| KYC Required | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| FATCA | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |
| CRS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### 2. Data Protection

| Requirement | SG | MY | TH | PH | ID | VN | HK |
|-------------|----|----|----|----|----|----|-----|
| Data Protection Law | ✅ PDPA | ✅ PDPA | ✅ PDPA | ✅ DPA | ✅ UU PDP | ✅ PDPD | ✅ PDPO |
| Consent Required | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Data Retention | 6 yrs | 7 yrs | 5 yrs | 5 yrs | 7 yrs | 10 yrs | 7 yrs |
| Mandatory Breach Notification | ✅ (3 biz days) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### 3. Anti-Money Laundering

| Requirement | All Markets |
|-------------|-------------|
| Suspicious Transaction Reporting | Required |
| Customer Screening | Required |
| Record Keeping | Required |

### 4. Non-Disclosure Policy Cancellation Restriction 🆕

| Market | Rule |
|--------|------|
| Indonesia | Policy cancellation for non-disclosure must be mutual agreement or court order (Constitutional Court Decision No. 83/PUU-XXII/2024) |
| Vietnam | Same principle applies (regional parallel ruling) |
| Singapore | MAS conduct framework; restrictive non-disclosure cancellation practices discouraged |
| Malaysia | BNM prohibits unknown exclusions; fair treatment principles apply |

**System impact (all markets):** CS cancellation workflow must not auto-lapse on non-disclosure grounds; require documented evidence and approval step.

---

## Market Comparison

### Product Classification

| Product Type | SG | MY | TH | PH | ID | VN | HK |
|--------------|----|----|----|----|----|----|-----|
| Term Life | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Whole Life | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Endowment | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ILP/Unit Link (ILAS) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| IUL (Indexed Universal Life) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ PI-only |
| Health | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Takaful | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Credit Insurance | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Composite (Life + Non-Life same entity) | ✅* | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |

*SG: Composite licence exists; most life insurers are standalone.
HK: Composite permitted but minimum capital HK$20M; IUL = PI-only (IA/SFC Joint Circular 2025).

### Channel Restrictions

| Channel | SG | MY | TH | PH | ID | VN | HK |
|---------|----|----|----|----|----|----|----|
| Bancassurance | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Agency | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ max 4 insurers |
| Direct | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Digital | ✅ | ✅ | ✅ | ❌ | ✅* | ✅ | ✅ |
| e-Commerce / Embedded | ✅ | ✅ | ✅ | ❌ | ✅* | ✅ | ✅ |
| Active Marketing from Outside Market | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ prohibited |

*Indonesia: requires PSE registration + prior OJK approval (POJK 36/2024)
HK: Active marketing to HK public from outside HK is prohibited under Insurance Ordinance.

---

## Health Insurance Co-Payment Requirements (2025–2026) 🆕

| Market | Co-Payment Rule | Effective |
|--------|----------------|-----------|
| Indonesia | Min 10% co-pay (POJK 36/2025); outpatient cap IDR 300k; inpatient cap IDR 3M | 2026 (phased; auto-renewing by 31 Dec 2026) |
| Malaysia | Base MHIT: in-network no co-share; out-of-network 20% co-share (capped RM 3,000) | H2 2026 pilot; 2027 full |
| Singapore (ISP) | Mandatory co-payment for ISP riders; full-rider plans banned since 2019 | In force |
| Thailand | Per product terms (no universal co-pay mandate) | — |
| Philippines | Per PhilHealth coordination rules | — |
| Vietnam | Per product terms | — |

---

## IFRS 17 Adoption Status by Market

| Market | Standard | Effective | Status |
|--------|----------|-----------|--------|
| Singapore | SFRS(I) 17 | 1 Jan 2023 | ✅ In force |
| Malaysia | MFRS 17 | 1 Jan 2023 | ✅ In force |
| **Hong Kong** | **HKFRS 17** | **1 Jan 2023** | **✅ In force** |
| Thailand | TFRS 17 | 1 Jan 2025 | ✅ In force |
| Philippines | PFRS 17 | 1 Jan 2025 | ✅ In force |
| Indonesia | PSAK 117 | 2025 phased | ⏳ Transitional |
| Vietnam | VAS (local) | TBC | 🔴 Under development |

**System impact:** GL posting and actuarial calculation modules require MFRS 17 / SFRS 17 output fields (CSM, risk adjustment) for SG and MY. Config/Dev Gap for other markets as standards roll in.

---

## Common Compliance Checkpoints

| Checkpoint | Description |
|------------|-------------|
| Product Approval | Market-specific filing required |
| Pricing | Actuarial sign-off per market |
| Distribution | Licensed channel only |
| Documentation | Local language required |
| Claims | Local TPA/panel required |
| Reporting | Market-specific periodic reports |
| Non-Disclosure | Cancellation must follow fair treatment principles; mutual agreement or court order where required |
| Unknown Exclusions | Cannot enforce policy conditions not disclosed to policyholder (MY, SG) |
| Health Co-Payment | Mandatory minimum co-payment for health insurance (ID, SG ISP) |

---

## Cross-Border Considerations

| Scenario | Regulatory Approach |
|----------|---------------------|
| Multi-country product | Separate filing per market |
| Regional hub | Head office + local filing |
| Group policy | Local implementation rules |
| IFRS 17 multi-market | Each market's local standard; timing may differ |

---

## 2026 Regional Regulatory Themes

| Theme | Markets | Description |
|-------|---------|-------------|
| Health insurance reform | ID, MY | Co-payment mandates, co-payment caps, BPJS coordination (ID), Base MHIT (MY) |
| AI regulation | SG, HK | MAS AI Model Risk Management Guidelines (SG); IA increasingly focused on AI in underwriting/claims |
| Digital insurance | ID, MY, SG | POJK 36/2024 (ID), DITO licence (MY), e-commerce clarification (SG) |
| Capital strengthening | ID, HK | ID: 2026 milestone (Rp 250bn conventional); HK: RBC PCA + Pillar 3 public disclosure (2026) |
| Broker / intermediary conduct | MY, HK | BNM broker policy document (1 Jan 2026); IA Practice Note on par commissions (1 Jan 2026) |
| Non-disclosure reform | ID, VN | Constitutional court rulings restrict insurer unilateral cancellation |
| Participating business governance | HK | IA reviewing design and sale of par policies; referral scheme focus |
| IUL / high net worth products | HK | New PI-only IUL regime (2025); further guidance expected |
| Re-domiciliation | HK | May 2025 mechanism; major international groups re-domiciling Bermuda branches to HK |
| Policyholder protection | HK | PPF legislation under development |
| GBA cross-border | HK | Insurance Connect; cross-border motor; GBA scheme under discussion |
| Electronic records | VN | Electronic social insurance books from 1 Jan 2026 |

---

## References

- ASEAN Insurance Council
- OECD Common Reporting Standard
- FATCA Agreement
- IAIS ComFrame Standards
- Market-specific files: reg-mas.md, reg-bnm.md, reg-ojk.md, reg-oid.md
