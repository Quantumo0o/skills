# InsureMO V3 — LifeClaimSystem System Configuration Guide

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-lc-system-config.md |
| Source | eBaoTech_LifeClaimSystem_System_Configuration_Guide.pdf |
| System | LifeClaimSystem |
| Version | V3 (legacy) |
| Date | ~2015 |
| Category | System Administration / Claims Configuration |
| Pages | 137 |

## 1. Purpose of This File

Answers questions about LifeClaimSystem access control and claims-specific configuration. Structure mirrors the ProductFactory System Config Guide (same 3-role model), but adds claims-specific limitation roles. Used for understanding claims system configuration and authorization setup.

---

## 2. Access Control Model

Same as ProductFactory: **Operation / Limitation / Accessible Organization** roles.

**Key difference from LifeSystem:** LifeClaimSystem has additional claim-specific limitation roles for case classification, policy type, amount limits, and claim officer/committee/investigator.

---

## 3. Claim-Specific Limitation Roles

### 3.1 Case Classification Role

Defines which types of claim cases a user can process (Evaluation and Approval).

**Case Types:** Special / Normal / Major / Appeal

**Initial Setting Example:**

| Role | Special | Normal | Major | Appeal |
|------|---------|--------|-------|--------|
| D_CLM_CASE_SuperUser | ✓ | ✓ | ✓ | ✓ |
| D_CLM_CASE_HOD_VP | ✓ | ✓ | ✓ | ✓ |
| D_CLM_CASE_AVP | ✓ | ✓ | ✓ | ✓ |
| D_CLM_CASE_M | ✓ | ✓ | ✓ | ✓ |
| D_CLM_CASE_AM | ✓ | ✓ | | |
| D_CLM_CASE_SA | ✓ | ✓ | | |
| D_CLM_CASE_A | ✓ | | | |

**Note:** Case Classification is decided by user during case registration (Figure 2-21).

---

### 3.2 Policy Type Role

Defines which policy types a user can process (Acceptance / Evaluation / Approval).

**Policy Types:** Individual / Group / Bancassurance

**Initial Setting Example:**

| Role | Individual | Group | Bancassurance |
|------|-----------|-------|--------------|
| D_CLM_CATEGORY_SuperUser | ✓ | ✓ | ✓ |
| D_CLM_CATEGORY_HOD_VP | ✓ | | |
| D_CLM_CATEGORY_AVP | ✓ | | |
| D_CLM_CATEGORY_M | ✓ | | |
| D_CLM_CATEGORY_AM | ✓ | | |
| D_CLM_CATEGORY_SA | ✓ | | |
| D_CLM_CATEGORY_A | ✓ | | |

---

### 3.3 Amount Limit Role

Defines claim authorization limits for approval.

**Three types of limits checked in order:**
1. **Case Payment Limits** — Total payment amount limit
2. **Type of Claim Limits** — Per claim type (Death/Accident/Hospitalisation/Medical/etc.)
3. **Claim Decision Limits** — Per decision (Admit/Repudiate/Cancel/Ex-gratia/Withdrawn)

**Approval check logic:**
```
Step a: Case Payment Limits → if payment ≤ limit → PASS
Step b: Type of Claim Limits → if payment ≤ limit for this type → PASS
Step c: Claim Decision Limits → if payment ≤ limit for this decision → PASS
All 3 must pass → User CAN approve
```

**Note:** For Repudiate/Cancel/Withdrawn → payment amount = 0 → always passes limit check.

**Example:**

| Claim Type | Amount Limit |
|-----------|-------------|
| Accident | $15,000 |
| Death | $125,000 |
| Hospitalisation | $15,000 |
| Medical | $15,000 |
| TPD | $125,000 |

| Claim Decision | Amount Limit |
|-------------|-------------|
| Admit | $200,000 |
| Repudiate | $200,000 |
| Cancel | $200,000 |
| Ex-gratia Full | $200,000 |
| Ex-gratia Partial | $200,000 |

Case Payment Limit: $150,000

**Scenario:**
- Death, Admit, $120,000 → All 3 pass → CAN approve
- Accident, Cancel, $250,000 → Cancel = $0 payment → All 3 pass → CAN approve

---

### 3.4 Claim Officer / Committee / Investigator Roles

For **escalation** only:

| Role | Escalation Option | Displayed In |
|------|------------------|-------------|
| D_CLM_OFFICER | Escalate to senior claim officer | Escalation To dropdown |
| D_CLM_INVESTIGATOR | Submit to Investigator | Escalation To dropdown |
| D_CLM_COMMITTEE | Submit to Committee | Committee Selection area (only when "Submit to Committee" chosen) |

---

### 3.5 Workflow Claim Assignment Role

Defines which claim work list tasks a user can access:

| Role | Accessible Tasks |
|------|----------------|
| D_WF_TASK_CLM_REGISTRATION | Case Registration |
| D_WF_TASK_CLM_ACCEPTANCE | Case Acceptance |
| D_WF_TASK_CLM_EVALUATION | Case Evaluation |
| D_WF_TASK_CLM_APPROVAL | Case Approval |

---

## 4. Other Limitation Roles

### Medical Billing Access Matrix
- **Query:** Can only search medical billing information
- **All:** Can add/delete/cancel/reverse medical billings

### BCP Backdating Limit
- Permit Modify Fees
- Permit Backdating

### Financial Adjustment Limits
- Define which adjustments a user can perform

### BCP Cancel Cheque
- Cancel cheque authorization

### GP_Collbank / GP_Paybank
- Collection bank / Payment bank access

### Product Roles (View/Create/Edit/Editable Product)
Same as ProductFactory System Config Guide.

### Document Management Limit
Defines which document categories an organization can access:
- NBU Query, LIA, CPF, Miscellaneous, Underwriting, Panel Doctor
- Refund, ILP, CS Trad, Party, Statement, Policy Alteration
- Premium Notice, BCP Premium Reminder, Direct Debit
- Credit Card, Cheque Printing, Direct Credit, Manage Suspense
- Annuity, Claim Maturity, CLM, etc.

### Crystal Report Roles
Defines which reports a user can access. Key claim reports:
- Claim Registered Case Management Report (Online)
- Paid Claims Report (Online)
- Claim Turnaround Time Report
- Acceptance and Settled Claim Distribution Report
- Outstanding Payment Report (Online)
- Print Claim Provision

### Action Control
Defines rate table edit actions:
- Delete All Relevance Relatedata, Load/Save/Upload/Download RateData
- Add/Delete/Edit/Clear RateTable, Create/Register RateTable
- Import/Export Rate, Enter Rate, Try, Preview

### Party Information Scope
Defines party management authorities by category:
- Person-Individual Customer (Create, 5 Basic Info Update, Correspondence Address, Bank Account, Change Account Link, Change Address Link)
- Person-Doctor (Create, Update)
- Person-Employee (Create, Update)
- Organization-Company Customer (Create, Update, Correspondent Address, Bank Account, Change Account Link, Change Address Link)
- Organization-Hospital/Clinic, Reinsurer, Others, Department, Organization

---

## 5. Claim Configuration

### 5.1 Dynamic Code Tables

All via IT staff (code tables T_*). Users can request replacements or upload directly.

| Code Table | Used On |
|-----------|---------|
| T_CLAIM_REJECT_REASON | Reason dropdown on Acceptance/Evaluation page |
| T_DEATH_CODE | Death Code dropdown on Case Acceptance |
| T_INCIDENT_CODE | Incident Code dropdown on Case Acceptance |
| T_PENDING_REASON | Pending Reason field on Disbursement Plan |
| T_CLAIM_TYPE | Type of Claim field on Case Registration |
| T_CLAIMANT_TYPE | Relation with Life Assured on Case Registration |
| T_LIABILITY_CATEGORY | Liability Category on Product Definition |
| T_LIABILITY | Liability Name on Product Definition (excl. SB/Annuity/Maturity) |
| T_REPORT_TYPE | Report Type on Case Registration |
| T_CHECKLIST | Checklist types: Document/Pending Reply/Claim Tip/Missing Doc/Form Creation/Compliance/General |

**After modifying any code table:** Must run Implementation Support > Clear Cache.

---

### 5.2 Operation Code

**Path:** Configuration Center > Claim Configuration > Operation Code

- Define operation codes and operation types
- Used on claim acceptance page

---

### 5.3 Diagnosis Code

**Path:** Configuration Center > Claim Configuration > Diagnosis Code

- Define diagnosis codes with type and category
- Used on claim acceptance page

---

### 5.4 Claim Type and Liability Category Mapping

**Code Table:** T_CLAIM_TYPE_LIAB

- Maps which claim types accept which liability categories
- Example: Claim Type 1 → maps to Liability Category 4

---

### 5.5 Claim Type Checklist

Maps checklist items to claim type + policy organization.

**Checklist Types:**
1. Document
2. Pending Reply
3. Claim Tip
4. Missing Documents
5. Form Creation
6. Compliance Check
7. General Checks

---

### 5.6 Claim Auto-Acceptance Rules

System auto-accepts claims meeting certain criteria without manual acceptance review.

---

### 5.7 Claim Auto-Approval Rules

System auto-approves claims meeting certain criteria without manual approval review.

---

## 6. Document Configuration

### Create Document Templates
**Access:** Configuration > Document Configuration

### Create Documents
Documents linked to document templates for claims processes.

---

## 7. Batch Configuration

Batch jobs for claim processing:
- Claim batch jobs
- Job scheduling and dependencies
- Pre-scheduled job submission

---

## 8. New Organization Configuration

Same pattern as ProductFactory:
1. Create Organization / Department / User
2. Assign Operation Roles
3. Assign Limitation Roles (including claim-specific ones)
4. Assign Accessible Organization Roles

---

## 9. Key Menus

| Action | Path |
|--------|------|
| Organization/User/Profile setup | Party Management > Maintain Party |
| Profile Management | System Administration > Profile Management |
| Role Management | System Administration > Role Management |
| Organization Authority | System Administration > Organization Authority Management |
| Assign Role to User | System Administration > Profile/Role Authorization |
| Claim Configuration | Configuration Center > Claim Configuration |
| Operation Code | Configuration Center > Claim Configuration > Operation Code |
| Diagnosis Code | Configuration Center > Claim Configuration > Diagnosis Code |
| Clear Cache | Implementation Support > Clear Cache |

---

## 10. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-pf-system-config.md | PF System Config — same access control model |
| insuremo-v3-ug-claims.md | Claims UG — claim processing workflow |
| insuremo-v3-ug-component-rules.md | Component Rules — claim calculation rules |
| insuremo-v3-ug-reinsurance.md | Reinsurance — RI claim recovery |
