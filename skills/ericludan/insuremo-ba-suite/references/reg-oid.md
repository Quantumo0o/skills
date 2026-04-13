# OCI/ISA Regulatory Requirements — Vietnam
# Source: Vietnam Insurance Regulatory Framework V26.03
# Scope: BA knowledge base for Agent 3 (Regulatory Compliance)
# Version: 2.0 | Updated: 2026-03

---

## Purpose

Regulatory requirements for Vietnam market (OCI/ISA). Current as of March 2026.

---

## Regulatory Framework

| Authority | Full Name | Scope |
|-----------|-----------|-------|
| **MoF** | Ministry of Finance | Primary regulator; issues licences and approves products |
| **ISA** | Insurance Supervisory Authority (under MoF) | Day-to-day supervision; regulated under Decision 373/QD-BTC (Feb 2025) |
| **VIDI** | Vietnam Insurance Development Institute | Research and training (reorganised Nov 2020 from IRTC) |
| **IAIS** | International Association of Insurance Supervisors | Vietnam member since 2007; ComFrame standards apply |

**Active Legislation (as of 2026):**

| Instrument | Description | Effective |
|-----------|-------------|-----------|
| Law on Insurance Business No. 08/2022/QH15 | Primary insurance law | 2023 |
| Decree No. 46/2023/ND-CP | Implementation guidance | 1 Jul 2023 |
| Decree No. 174/2024/ND-CP | Administrative sanctions | 30 Dec 2024 |
| Law on Health Insurance No. 51/2024/QH15 | Health insurance amendments | 1 Jan 2025 |
| **Law on Social Insurance No. 41/2024/QH15** | **Social insurance overhaul** | **1 Jul 2025** |
| Decree 13/2023/ND-CP | Personal Data Protection (PDPD) | 2023 |

---

## Key Requirements

### 1. Market Entry & Licensing

| Requirement | Description |
|-------------|-------------|
| Regulator | MoF issues Establishment and Operation Licence |
| FDI | 100% foreign direct investment permitted |
| Composite Insurance | NOT permitted; life and non-life must be separate entities |
| Application | 3 sets of documents; MoF notifies within 21 days; licence within 60 days |

### 2. Minimum Capital

| Entity Type | Requirement |
|-------------|-------------|
| Life / Non-Life / Reinsurance / Brokerage | Per Decree 46/2023 thresholds (increased from Decree 73/2016) |
| Transitional Period | Companies licensed before 1 Jan 2023 may retain Decree 73/2016 capital during transition; agency compliance required by 1 Jul 2024 |

### 3. Product Approval

| Requirement | Description |
|-------------|-------------|
| Filing | Products must be approved/registered with MoF/ISA before launch |
| Actuarial Sign-off | Required for pricing |
| MoF Insurance Database | Policy and policyholder data submitted to database from 1 Jan 2024 (mandatory) |

### 4. Distribution Channels

| Channel | Status | Notes |
|---------|--------|-------|
| Bancassurance | ✅ | Permitted |
| Agency | ✅ | Organisational agencies must maintain conditions throughout contract term (Decree 46) |
| Direct | ✅ | Permitted |
| Digital | ✅ | MoF Insurance Database digital reporting mandatory |

**Organisational Agency Requirement (Decree 46):**
- Must maintain qualifying conditions for full term of agency agreement
- Non-compliance → insurer may terminate agency contract
- Grace period: 1 Jul 2024

### 5. Underwriting

| Requirement | Description |
|-------------|-------------|
| Non-Disclosure | Policy cancellation based on non-disclosure must be mutually agreed or court-ordered (Constitutional Court Decision No. 83/PUU-XXII/2024 — regional precedent) |
| Compulsory Insurance | Motor third-party liability; aviation third-party liability; professional indemnity (lawyers, notaries, auditors, engineers, architects, insurance brokers) |

### 6. Health Insurance (Updated 2025–2026)

**Law on Health Insurance No. 51/2024 (Effective 1 Jan 2025):**

| Change | Description |
|--------|-------------|
| Expanded Coverage | Revised eligibility criteria; aligned with Law on Social Insurance |
| Referral Elimination | Referral procedures eliminated for specific rare and serious diseases; direct access to specialised care |
| Ministry of Health Responsibility | Additional MOH responsibilities for managing and regulating health insurance services |

**Law on Social Insurance No. 41/2024 (Effective 1 Jul 2025):**

| Change | Description |
|--------|-------------|
| Part-Time Officials | Now entitled to sickness and maternity benefits |
| Lump-Sum Withdrawal | Eligible if: reached retirement age with <15 years contributions; or disability >81%; or severe disability |
| Contribution Base | Temporary reference level = VND 2.34 million/month (Decree 73/2024) |
| Enforcement | Daily interest for delayed contributions; criminal liability for intentional evasion |
| Electronic SI Books | From 1 Jan 2026 |
| Digital Processing | All SI benefit procedures via digital platforms from 1 Jan 2027 |

> **Note:** Social and mandatory insurance is NOT in scope for commercial InsureMO platform. Included for awareness.

### 7. Investment Restrictions

| Restriction | Rule |
|-------------|------|
| Offshore Investment | Permitted only to establish offshore insurance company/branch; requires MoF approval |
| Related-Party Investment | Investments in return for shareholder contributions NOT allowed (except credit institution deposits) |
| Corporate Bond Restriction | Cannot purchase bonds issued to restructure loans of the issuing company |
| Fiduciary Investment | Trustees must hold fiduciary investment licence |

---

## Data Protection & AML

| Requirement | Status | Notes |
|-------------|--------|-------|
| PDPD (Decree 13/2023) | ✅ | Vietnam's data protection framework; personal data of policyholders |
| Consent Required | ✅ | |
| Data Retention | 10 years | Insurance policy records; MoF database retention |
| MoF Insurance Database | ✅ **Mandatory from 1 Jan 2024** | All policy and policyholder data submitted |
| **Electronic SI Books** | ✅ **From 1 Jan 2026** | For social insurance; awareness only |
| FATCA | ❌ | Vietnam is not a FATCA IGA signatory |
| CRS | ✅ | CRS participant |
| AML / CFT | ✅ | Suspicious transaction reporting required |

---

## Common Config Gaps

| Scenario | Gap Type | Solution |
|----------|----------|----------|
| MoF Insurance Database API submission | Integration | File-based or API submission; policy + policyholder data export |
| Electronic SI books (1 Jan 2026) | Awareness | Social insurance only; not InsureMO scope but affects HR integrations |
| Organisational agency compliance tracking | Config | Flag agency contracts; compliance monitoring |
| Product registration workflow | Config | MoF/ISA approval status per product |
| Compulsory insurance product setup | Config | Motor liability, aviation liability, professional indemnity product codes |
| Decree 46 capital threshold validation | Config | Capital adequacy check |
| Health insurance referral rule update | Config | Rare/serious disease list → no referral required for listed conditions |

---

## INVARIANT Declarations

```
INVARIANT 1: Composite insurance (life + non-life) is NOT permitted in Vietnam
  Effect: InsureMO must be for a single-category licensed entity only

INVARIANT 2: MoF Insurance Database submission is mandatory from 1 Jan 2024
  Effect: All new policy and policyholder records must be submitted;
          InsureMO integration or export capability required

INVARIANT 3: Policy cancellation on non-disclosure requires mutual agreement or court order
  Source: Regional constitutional court precedent (parallel to Indonesia Decision 83/PUU-XXII/2024)
  Effect: System cannot auto-cancel on non-disclosure grounds alone

INVARIANT 4: Offshore investment requires MoF prior approval
  Effect: Investment module must include MoF approval flag before offshore transactions
```

---

## Regulatory Change Log (2024–2026)

| Change | Effective | Impact on InsureMO |
|--------|-----------|-------------------|
| Decree 46/2023 — Agency capital + compliance conditions | 1 Jul 2024 | Agency onboarding config |
| MoF Insurance Database mandatory | 1 Jan 2024 | Policy/policyholder data export integration |
| Health Insurance Law 51 — referral elimination | 1 Jan 2025 | Health benefit config — rare disease referral rules |
| Decree 174/2024 — Administrative sanctions | 30 Dec 2024 | Compliance monitoring; sanctions tracking |
| Social Insurance Law 41 — benefits overhaul | 1 Jul 2025 | Awareness only (not platform scope) |
| **Electronic SI books** | **1 Jan 2026** | **Social insurance awareness; HR system impact** |
| Digital SI processing (all procedures) | 1 Jan 2027 | Future awareness |

---

## References

- Law on Insurance Business No. 08/2022/QH15
- Decree No. 46/2023/ND-CP
- Decree No. 174/2024/ND-CP
- Law on Health Insurance No. 51/2024/QH15 (effective 1 Jan 2025)
- **Law on Social Insurance No. 41/2024/QH15 (effective 1 Jul 2025)**
- Decree 13/2023/ND-CP (Personal Data Protection)
- IAIS ComFrame Standards
