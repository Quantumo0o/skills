# InsureMO V3 — LifeSystem System Configuration Guide

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ls-system-config.md |
| Source | eBaoTech_LifeSystem_System_Configuration_Guide.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | ~2015 |
| Category | System Administration / LifeSystem Configuration |
| Pages | 270+ |

## 1. Purpose of This File

**Master System Configuration Reference** for LifeSystem 3.8.1. Covers the complete access control model, NB/UW configuration, billing/finance rate tables, RI configuration, claim configuration, report management, batch jobs, and rate table/FMS/RMS tools. Most comprehensive of the three System Config Guides (ProductFactory + LifeClaimSystem + LifeSystem). Provides domain-specific configuration details not found in the other two guides.

---

## 2. Document Structure

```
Chapter 1: Access Control (Organization / Users / Profiles / Roles)
Chapter 2: Limitation Roles (NBU / CS / Billing / BCP)
Chapter 3: Shared Limitation Roles (BCP Adjustments / Documents / etc.)
Chapter 4: NB / UW Configuration
Chapter 5: NBU Limitation Roles
Chapter 6: Rate Table Configuration (Billing / Finance)
Chapter 7: RI Configuration
Chapter 8: Claim Configuration
Chapter 9: Report Management
Chapter 10: Document Configuration
Chapter 11: Batch Configuration and Monitoring
Chapter 12: Product Definition (?)
Chapter 13: Shared Topics (Rate Table / FMS / RMS)
```

---

## 3. Access Control Model

Same as ProductFactory and LifeClaimSystem:
- **Operation Role**: Menus/modules accessible
- **Limitation Role**: What user can do within operation role
- **Accessible Organization Role**: Data scope (org + branches + departments + users)

### New Limitation Roles Specific to LifeSystem

| Limitation Role | Description |
|----------------|-------------|
| D_NBU | NB Underwriting authority |
| D_NB_AUTO | Auto-approval for NB |
| D_CS | Customer service operations |
| D_CS_AUTO | Auto-approval for CS |
| D_BCP | BCP adjustment limits |
| D_BCP_BACKDATE | BCP backdating |
| D_BCP_WAIVE | BCP interest waiver |
| D_BILLING | Billing operations |
| D_PAYMENT | Payment operations |
| D_GL | GL/posting operations |
| Change Payment Details | Modify payment bank/account |
| GP_Collbank / GP_Paybank | Collection/Payment bank access |

---

## 4. NB / UW Configuration (Chapter 4)

### 4.1 Proposal Prefixes

Pre-configured prefix codes (Table 4-2):

| PREFIX_CODE | AUTO_PROPOS | PREFIX_DESC | SERVICE_BRANCH |
|------------|-------------|-------------|----------------|
| HO | Y | Head Office | 1 |
| HOM | N | Head Office | 1 |
| HX | Y | Great Eastern House | 1 |
| HXM | N | Great Eastern House | 1 |
| CC | Y | Changi Centre | 1 |
| AFA | Y | Changi Centre | 1 |
| GHO | Y | Head Office | 1 |

### 4.2 Campaign Type
- Codes maintained by IT in code table
- Used on NB Data Entry page

### 4.3 Underwriting Decision Reasons
- Codes maintained by IT in code table
- Used on Underwriting page

### 4.4 Discount Types
Pre-configured (Table 4-3):

| TYPE_CODE | TYPE_NAME |
|-----------|-----------|
| 0 | No special discount |
| 1 | Staff Discount |
| 2 | Staff's Family Discount |
| 3 | Agent Discount |
| 4 | Agent's Spouse |
| 5 | Agent's Children |
| 6 | Bank Employee Discount |
| 7 | OCBC Discount |
| 8 | Kobank Scheme |
| 9 | Family Package |
| 10 | U Type |
| 11 | NUS Alumni |

### 4.5 Underwriting Authority

**raUWCategory + raUWLevel rate tables** define:
- Underwriting limits per category and level
- Category = combination of: Type of UW + Submission Channel + Organization
- Used in Role Management for underwriting authority limits

### 4.6 Policy Issue Without Premium

Rate Table: `POLICY_ISSUE`
- Define whether policy can be issued without premium
- Organization-related setting

### 4.7 Monthly Policy Inforcing Installments

Rate Table: `Monthly Policy Inforcing Installs`
- For monthly payment policies
- Define number of installments to enforce policy
- Can be related with organization and product

### 4.8 Risk Aggregation

Rate Table: `raUWAgeSarFactor`
- Define aggregate risk rate for waiver products

### 4.9 Proposal Rules and Underwriting Rules

Defined in **RMS (Rule Management System)**:

| Category | Description |
|----------|-------------|
| Non-UW Rules | General proposal validation rules |
| UW Rules | Underwriting decision rules |
| Rejection Rules | Rules for rejecting proposals |

---

## 5. Rate Table Configuration (Chapter 6)

### 6.1 Billing Rate Tables

| Rate Table | Purpose |
|-----------|---------|
| SpringBean_Count_Collect_Ex | Collection counting extension |
| Billing_Notice_Cfg | Billing notice configuration |
| Deduction Schedule | Defines deduction order and timing |
| Deduction bank | Bank-specific deduction rules |
| Bank Charge Rate | Bank charges per transaction |
| Saving Account Rate Entry | Interest rate configuration |

### 6.2 Bank Transfer File Configuration

**Define Main Features of Bank Transfer File:**
- File format (format name, delimiter)
- File path
- File naming convention

**Define Body of Bank File:**
- Header/body/trailer structure
- Field mapping

**Define Attribute for Each Field:**
- Field name
- Field type (string/number/date)
- Field length
- Padding character
- Justification (left/right)

### 6.3 Stamp Duty Configuration

Rate Table: `Stamp Duty Definition`
- Define stamp duty rates per transaction type
- Applies to: collections, policy loans

### 6.4 Payment Approval Configuration

Rate Table: `SpringBean_Pay_Alloc_Ex`
- Define whether payment requisition requires approval
- Per organization / product / payment type

---

## 6. RI Configuration (Chapter 7)

### 6.1 RI Retain Order

Configure retention layers:
- Layer 1: Ceding company retains first loss
- Layer 2+: Successive RI layers

### 6.2 RI Risk Category

Define risk categories for RI:
- Medical / Non-Medical / Group / etc.

### 6.3 Treaty Information

**Treaty Types:**

| Type | Abbreviation | Description |
|------|-------------|-------------|
| Quota Share | QS | Fixed % of risk ceded |
| Surplus | SUR | Excess over retention |
| XOL | XOL | Excess of Loss |
| Facultative | FAC | Per-policy arrangement |

**Treaty Configuration Tabs:**
- Treaty Information Tab: treaty type, effective dates, RI share
- Treaty Product Tab: which products are covered
- Treaty Reinsurer Tab: reinsurer details and shares

### 6.4 Treaty Commission Rates

RI Commission Rate page:
- Add/Edit/Delete commission rates
- Batch Upload via template
- Commission rate = % of RI premium

### 6.5 Treaty Premium Rates

RI Premium Rate page:
- Factors: Treaty ID, Risk Type, Reinsurer, Product, Age, Occupation Class, Gender, Smoker Status, Preferred Life Indicator, Coverage Term, ER Indicator, Wait Period, Benefit Period, Endorsement Code
- Batch Upload via template

**Wait Period:** Days of waiting period for claim

---

## 7. Claim Configuration (Chapter 8)

### 7.1 Claim Type and Liability Category Mapping

Code Table: `T_CLAIM_TYPE_LIAB`
- Maps claim types to liability categories
- Product's liability category determines which claim types are accepted
- **Exception:** Case Classification = "Special" → bypasses mapping

**Mapping Examples:**

| Claim Type | Liability Category |
|-----------|------------------|
| Accident | Accident |
| Death | Life |
| Hospitalisation | Medical |
| Medical | Medical |

### 7.2 Claim Type Checklist

Code Table: `T_CLAIM_TYPE_CHKLIST`
- Maps claim type + organization → required documents
- Different organizations may require different documents for same claim type
- Displayed on Claim Acceptance page

### 7.3 Claim Auto-Acceptance Rules

Two types:
1. **Validation rules:** Which cases can go to auto-acceptance
2. **Processing rules:** How auto-acceptance is processed

### 7.4 Claim Auto-Approval Rules

Similar to auto-acceptance — define which claims can be auto-approved without manual review.

---

## 8. Report Management (Chapter 9)

### 8.1 Report Deployment

**Steps:**
1. Create report template (Crystal Reports or other)
2. Deploy report to Report Management page
3. Configure report parameters
4. Assign report to users via Crystal Report Roles

### 8.2 Report Parameters

**Parameter Information Area:**
- Parameter name
- Parameter type
- Default value
- Mandatory flag

**Edit Report Parameter Page:**
- Modify parameter settings
- Set validation rules

### 8.3 Key Claim Reports (Pre-configured)

| Report | Description |
|--------|-------------|
| Claim Registered Case Management Report | Online claim registration |
| Paid Claims Report | Online paid claims |
| Claim Turnaround Time Report | Processing time analysis |
| Acceptance and Settled Claim Distribution Report | Claim distribution by type |
| Outstanding Payment Report | Online outstanding payments |
| Print Claim Provision | Provision reports |

---

## 9. Batch Configuration and Monitoring (Chapter 11)

### 9.1 Job Net

A **Job Net** = collection of jobs with dependencies.

**New Job Net:** Create a job net to group related batch jobs.

### 9.2 Job Definition

Define individual batch jobs:
- Job name
- Job type
- Execution frequency
- Parameters

### 9.3 Job Dependencies

Define dependencies between jobs:
- Job A must complete before Job B can start
- Circular dependencies are not allowed
- Used to ensure correct processing order

### 9.4 Ad hoc Job

Submit one-time jobs outside of scheduled job nets.

### 9.5 Pre-scheduled Jobs

Requires:
- Job Net already defined
- Job Net must exist before scheduling

---

## 10. Shared Topics (Chapter 13)

### Rate Table Management

**Create/Modify Rate Table:**
1. Define columns (Column Name, Value Type, Description)
2. Define result columns
3. Set rates (import or manual)
4. Test rate table
5. Save/Publish

**Rate Table Fields:**

| Field | Description |
|-------|-------------|
| Column Name | Input parameter name |
| Value Type | String / Number / Date / Boolean |
| Is Range | Whether column uses range values |
| Description | Column description |
| Result Column | Output calculation result |

**Rate Table Tolerance:**
- Define acceptable tolerance for rate lookups
- Used in NB/Renewal tolerance checking

### FMS (Formula Management System)

Two implementations:
- **PL/SQL FMS:** Formula in PL/SQL
- **JAVA FMS:** Formula in JAVA with graphic editor

### RMS (Rule Management System)

Manage business rules for:
- Non-UW rules
- UW rules
- Rejection rules

---

## 11. Key Configuration Menu Paths

| Configuration | Path |
|--------------|------|
| Proposal Prefixes | NB Configuration > Proposal Prefix |
| Campaign Type | NB Configuration > Campaign Type |
| Discount Types | NB Configuration > Discount Type |
| Underwriting Authority | Configuration Center > iFoundation > Rate Table > raUWCategory, raUWLevel |
| Policy Issue Without Premium | Configuration Center > iFoundation > Rate Table > POLICY_ISSUE |
| RI Configuration | Configuration Center > Reinsurance Configuration |
| RI Treaty Premium Rates | Configuration Center > Reinsurance Configuration > Premium Rate |
| RI Commission Rates | Configuration Center > Reinsurance Configuration > Commission Rate |
| Bank Transfer File | Configuration Center > iFoundation > Rate Table > Bank Transfer |
| Stamp Duty | Configuration Center > iFoundation > Rate Table > Stamp Duty |
| Report Management | Configuration Center > Report |
| Batch Job Net | Configuration Center > iService > Batch Configuration and Monitor > Definition > Job Net |
| Rate Table Definition | Configuration Center > iFoundation > Rate Table > Rate Table Definition |

---

## 12. Comparison with Other System Config Guides

| Aspect | LifeSystem | LifeClaimSystem | ProductFactory |
|--------|-----------|----------------|----------------|
| Main Domain | NB, CS, Billing, Claims | Claims only | Products only |
| NB/UW Config | ✅ Chapter 4 | ❌ | ❌ |
| Billing Rate Tables | ✅ Chapter 6 | ❌ | ❌ |
| RI Config | ✅ Broad (QS/Surplus/XOL/FAC) | Limited | ❌ |
| Report Management | ✅ Chapter 9 | ❌ | ❌ |
| Batch Jobs | ✅ Chapter 11 | Basic | ❌ |
| FMS/RMS Tools | ✅ Chapter 13 | ❌ | ✅ |

---

## 13. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-pf-system-config.md | PF System Config — same access control model |
| insuremo-v3-lc-system-config.md | LC System Config — claim-specific roles |
| insuremo-v3-ug-nb.md | NB — proposal prefixes, UW rules |
| insuremo-v3-ug-reinsurance.md | RI — cession, claim recovery |
| insuremo-v3-ug-renewal.md | Renewal — billing rate tables |
| insuremo-v3-ug-component-rules.md | Component Rules — all calculation formulas |
