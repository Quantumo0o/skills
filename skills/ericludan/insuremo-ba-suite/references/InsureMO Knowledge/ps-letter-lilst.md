# InsureMO Platform Guide — Letter Management
# Source: Gemini Letter List V25.04
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb-full.md instead
# Version: 1.0 | Updated: 2026-03

---

## Purpose of This File

This file answers **"what letters does Gemini generate, when are they triggered, and who receives them"** — letter catalogue by module, trigger points, recipient rules, reminder linkage, and LOB applicability.

Use this file when:
- Agent 2 is writing **3.X.7 Configuration Task** for a letter-related gap
- Agent 6 is generating a **Config Runbook** for letter generation items
- A BA needs to verify **trigger conditions**, **recipient logic**, **reminder setup**, or **LOB coverage** for a specific letter

---

## Module Overview

```
Letter Management
│
├── NB APP    — New Business letters (4 letters)
├── UW APP    — Underwriting letters (6 letters)
├── CS APP    — Customer Service / Policy Servicing letters (10 letters)
├── FIN APP   — Finance / Collection letters (5 letters)
└── CLM APP   — Claims letters (11 letters)
```

---

## Letter Catalogue Field Reference

| Field | Description |
|---|---|
| APP | System module that owns the letter |
| Letter Name | Official letter name in Gemini |
| Purpose | Business purpose of the letter |
| Has Reminder Y/N | Whether a follow-up reminder letter is configured |
| Reminder Letter | Name of the reminder letter (if applicable) |
| Address Type | Mailing address used for dispatch |
| Recipient | Primary recipient of the letter |
| CC Agent | Whether agent is copied (Y = configurable; blank = no) |
| Trigger Point | System event or user action that initiates letter generation |
| LOB Applicability | Which lines of business the letter applies to |

**LOB codes:**

| Code | Line of Business |
|---|---|
| Term | Term Life |
| Life | Whole Life / Endowment |
| Investment | Investment-Linked Policy (ILP) |
| Health | Health / Medical |
| Shield (SG) | MediShield Life / Integrated Shield Plan (Singapore) |
| LTC (SG) | Long-Term Care (Singapore) |

---

## NB APP — New Business Letters

### Application Cancellation Letter (NTU)

| Field | Value |
|---|---|
| Purpose | Notify customer that policy is not taken up or manually withdrawn |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- Auto withdraw / NTU by batch job
- User manually withdraws per customer request

---

### Letter of Acceptance

| Field | Value |
|---|---|
| Purpose | Notify customer that policy is pending issuance and premium collection is required |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- STP policy: proposal passes all pre-issuance rules and reaches pending issuance stage
- Non-STP policy: underwriting completed and all pre-issuance rule validations passed

---

### NB Premium Reminder Letter

| Field | Value |
|---|---|
| Purpose | Remind customer to make premium payment before policy issuance deadline |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- Generated after Letter of Acceptance is issued AND total inforcing premium has NOT been collected within the configured period

---

### Policy Document Pack

| Field | Value |
|---|---|
| Purpose | Notify customer of policy issued with benefit and term information |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- Total in-force premium collected AND all issuance rules passed (STP auto-issuance)
- User manually issues policy with sufficient premium collected

---

## UW APP — Underwriting Letters

### Underwriting Requirement Letter

| Field | Value |
|---|---|
| Purpose | Notify customer to submit medical check or additional documents for underwriting |
| Has Reminder | Y → **Underwriting Requirement Letter** (same letter re-sent) |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- During manual underwriting: underwriter selects manual UW issue and clicks **[Generate Letter]**

---

### Advisor Requirement Letter

| Field | Value |
|---|---|
| Purpose | Notify agent to provide documents for underwriting |
| Has Reminder | Y → **Advisor Requirement Letter** (same letter re-sent) |
| Address Type | Agent mailing address |
| Recipient | Agent |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- During manual underwriting: underwriter selects manual UW issue for **'Advisor Requirement'** and clicks **[Generate Letter]**

---

### Conditional Acceptance Letter (LCA)

| Field | Value |
|---|---|
| Purpose | Notify customer that policy is conditionally accepted with loading, exclusion, or other conditions; awaiting customer agreement |
| Has Reminder | Y → **Conditional Acceptance Letter** (same letter re-sent) |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- During manual underwriting: underwriter selects UW decision = **'Conditional Accept'** with condition (loading / exclusion / etc.) and clicks **[Generate LCA]**

---

### Underwriting Postpone / Decline Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that policy has been declined or postponed |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- During manual underwriting: underwriter selects UW decision = **'Decline'** or **'Postpone'** and submits / completes UW task

---

### Request for Medical Report Letter

| Field | Value |
|---|---|
| Purpose | Request Medical Assessment Report (MAR) from hospital / clinic for underwriting or claims |
| Has Reminder | Y → **Request for Medical Report Letter** (same letter re-sent) |
| Address Type | Hospital / Clinic mailing address |
| Recipient | Hospital / Clinic |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- During manual underwriting: underwriter selects manual UW issue for **'Medical Requirement'**, clicks **[Medical Report]** → pop-up window for letter content input → clicks **[Generate Letter]**

---

### MAR Cancellation Letter

| Field | Value |
|---|---|
| Purpose | Notify hospital / clinic that the MAR request has been withdrawn |
| Has Reminder | N |
| Address Type | Hospital / Clinic mailing address |
| Recipient | Hospital / Clinic |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- During manual underwriting: underwriter manually cancels an existing medical report letter

---

## CS APP — Customer Service / Policy Servicing Letters

### CS Pending Premium Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that CS request is approved and pending premium payment |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** CS transaction approved and pending premium collection. Applicable CS transactions:
- Reinstatement
- Change Birth Date or Gender (where premium is pending)

---

### CS Confirmation Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that CS request is completed / confirmed |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** CS transaction completed (In-Force). Applicable CS transactions:
- Increase Sum Assured
- Decrease Sum Assured
- Reinstatement
- Change Payment Method
- Cancellation (Voidance)
- Termination / Surrender (Auto Paid-Up)
- Termination / Surrender (No Refund)
- Freelook
- Change Birth Date or Gender

---

### CS Pending Requirement Letter

| Field | Value |
|---|---|
| Purpose | Notify customer to submit additional documents for CS request |
| Has Reminder | Y → **Requirement Letter** |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** User requests requirement during CS data entry. Applicable CS transactions:
- Change Payment Method
- Reinstatement
- Termination / Surrender
- Increase Sum Assured
- Decrease Sum Assured
- Change Birth Date or Gender
- Freelook

---

### Withdrawal of Request Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that CS request is withdrawn (deadline missed or customer instruction) |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
1. CS withdrawn due to customer failing to submit required documents by deadline. Applicable CS transactions:
   - Change Payment Method
   - Freelook
   - Increase Sum Assured
   - Reinstatement
   - Termination / Surrender (No Refund)
   - Decrease Sum Assured
2. CS withdrawn per customer instruction → applicable for **any** CS transaction

---

### CS Request Unsuccessful Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that CS request is invalid / rejected |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** CS transaction rejected. Applicable CS transactions:
- Change Payment Method
- Freelook
- Increase Sum Assured
- Reinstatement
- Termination / Surrender (No Refund)
- Decrease Sum Assured

---

### Renewal Notice

| Field | Value |
|---|---|
| Purpose | Notify customer of upcoming premium renewal (default: 2 months in advance) |
| Has Reminder | Y → **Premium Reminder Letter** |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Generated X days before renewal due date. X is configurable.

---

### Unsuccessful Renewal Premium Deduction Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that scheduled auto debit (GIRO / auto deduction) failed or was partially deducted; inform of alternative payment methods |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Auto debit deduction for renewal or CS transaction fails or is partially deducted

---

### Premium Reminder Letter

| Field | Value |
|---|---|
| Purpose | Reminder for customer to make premium payment before deadline |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
1. Policy has unpaid renewal premium at renewal date + 60 days (configurable)
2. Policy has unpaid premium for CS transaction by CS approval letter generation date + 60 days (configurable)

---

### Lapse Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that policy has lapsed due to non-payment or has been auto paid-up |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Policy lapses or is auto paid-up due to outstanding premium

---

### Policy Termination Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that policy has been terminated |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | PH or Estate of PH |
| CC Agent | Y (configurable) |
| LOB | **LTC (SG) only** |

**Trigger:** Policy terminated due to any of the following:
1. Basic policy becomes inactive (LTC policy only)
2. PH / Insured death
3. Non-disclosure

---

## FIN APP — Finance / Collection Letters

### Official Receipt

| Field | Value |
|---|---|
| Purpose | Confirm to customer that premium collection has been received |
| Has Reminder | N |
| Address Type | — |
| Recipient | — |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Confirmed cash collection via:
- Manual collection
- Auto Collections via PayNow
- GIRO Fast
- GIRO Batch

---

### GIRO Unsuccessful Collection Letter

| Field | Value |
|---|---|
| Purpose | Notify customer of GIRO batch deduction failure |
| Has Reminder | N |
| Address Type | — |
| Recipient | — |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Deduction failure record returned from GIRO Batch return file

---

### GIRO Application Rejection by Bank Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that auto deduction authorisation has been rejected by bank |
| Has Reminder | N |
| Address Type | — |
| Recipient | — |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Bank-rejected IBG (Interbank GIRO) returned from DAS interface file

---

### GIRO Application Approval Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that auto deduction authorisation has been approved by bank |
| Has Reminder | N |
| Address Type | — |
| Recipient | — |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Approved IBG returned from DAS interface file

---

### GIRO Cancellation Letter

| Field | Value |
|---|---|
| Purpose | Notify customer that auto deduction has been terminated |
| Has Reminder | N |
| Address Type | — |
| Recipient | — |
| CC Agent | — |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Terminated IBG returned from DAS interface file

---

## CLM APP — Claims Letters

### Submission Acknowledgement Letter

| Field | Value |
|---|---|
| Purpose | Notify informant that claim has been registered |
| Has Reminder | N |
| Address Type | — |
| Recipient | Informant |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Claim registration is successful

---

### Claim Acknowledgement Letter

| Field | Value |
|---|---|
| Purpose | Notify claimant / PH that claim has been registered |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | PH or Estate of PH |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- Claim registration is successful (auto)
- Manually triggered in **Claim Issue** tab

---

### Claim Requirement Letter

| Field | Value |
|---|---|
| Purpose | Notify customer to submit additional documents for claim |
| Has Reminder | Y → **Reminder (Checklist / General)** / **Last Reminder (Checklist / General)** |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Manually triggered in **Claim Issue** tab during claim acceptance and evaluation

---

### Medical Report Application

| Field | Value |
|---|---|
| Purpose | Request medical report, clarification, or medical history from hospital / clinic for claims |
| Has Reminder | Y → **Reminder to Medical Institution** |
| Address Type | Hospital / Clinic mailing address |
| Recipient | Hospital / Clinic |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Manually triggered in **Claim Issue** tab during claim acceptance and evaluation

---

### Claim Status Letter

| Field | Value |
|---|---|
| Purpose | Notify customer of claim status; indicate pending documents / reports / clarification from hospital / clinic |
| Has Reminder | Y → **Follow Up Status Letter — Still Pending Report** |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- Manually triggered in **Claim Issue** tab during claim acceptance and evaluation
- Auto-triggered by batch for the **first** status letter

---

### Claim Outcome Letter

| Field | Value |
|---|---|
| Purpose | Notify customer of claim outcome / settlement decision |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | PH or Estate of PH |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** New or ongoing claim is approved

---

### Claim Recovery Letter

| Field | Value |
|---|---|
| Purpose | Notify customer of outstanding claim recovery amount and request for recovery |
| Has Reminder | Y → **Claim Recovery Reminder Letter** / **Pass to Recovery Agency** |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | **LTC (SG) only** |

**Trigger:** Ongoing claim is auto-closed (fully paid or no response in PR/SC review) with outstanding claim recovery amount

---

### Medical Report Reimbursement Letter

| Field | Value |
|---|---|
| Purpose | Notify customer of payment for medical check / report fee |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Payment of medical check / report fee is approved and generated

---

### Changes to Payee Details Letter

| Field | Value |
|---|---|
| Purpose | Notify customer of changes to payee or disbursement method during claim |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:** Payee or disbursement method is changed in an ongoing, disbursing, or withholding claim

---

### Claim Review Letter

| Field | Value |
|---|---|
| Purpose | Notify customer of periodic review or survivorship check request |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | **LTC (SG) only** |

**Trigger:**
- Auto-triggered by batch
- Manually triggered in **Claim Issue** tab of ongoing claim

---

### Claim Invite Letter

| Field | Value |
|---|---|
| Purpose | Notify customer to submit a claim |
| Has Reminder | N |
| Address Type | Policy mailing address |
| Recipient | Policy Holder (PH) |
| CC Agent | Y (configurable) |
| LOB | Term / Life / Investment / Health / Shield (SG) / LTC (SG) |

**Trigger:**
- No active LTC claim AND basic claim status = Approved with monthly payment > 0
- Manually triggered in **Claim Issue** tab during acceptance / evaluation / ongoing claim

---

## Letter Summary Tables

### Letters with Reminder Chains

| Letter | Module | Reminder Letter Name |
|---|---|---|
| Underwriting Requirement Letter | UW APP | Underwriting Requirement Letter |
| Advisor Requirement Letter | UW APP | Advisor Requirement Letter |
| Conditional Acceptance Letter | UW APP | Conditional Acceptance Letter |
| Request for Medical Report Letter | UW APP | Request for Medical Report Letter |
| Renewal Notice | CS APP | Premium Reminder Letter |
| CS Pending Requirement Letter | CS APP | Requirement Letter |
| Claim Requirement Letter | CLM APP | Reminder (Checklist / General) / Last Reminder (Checklist / General) |
| Medical Report Application | CLM APP | Reminder to Medical Institution |
| Claim Status Letter | CLM APP | Follow Up Status Letter — Still Pending Report |
| Claim Recovery Letter | CLM APP | Claim Recovery Reminder Letter / Pass to Recovery Agency |

---

### Letters by Recipient Type

| Recipient | Letters |
|---|---|
| Policy Holder (PH) | All NB / CS / FIN letters; most CLM letters |
| PH or Estate of PH | Claim Acknowledgement Letter; Claim Outcome Letter; Policy Termination Letter |
| Agent | Advisor Requirement Letter |
| Hospital / Clinic | Request for Medical Report Letter; MAR Cancellation Letter; Medical Report Application |
| Informant | Submission Acknowledgement Letter |

---

### LOB-Restricted Letters (Not Universal)

| Letter | Restricted To |
|---|---|
| Policy Termination Letter | LTC (SG) only |
| Claim Recovery Letter | LTC (SG) only |
| Claim Review Letter | LTC (SG) only |

---

### Letters by Trigger Type

| Trigger Type | Letters |
|---|---|
| Fully Automatic (Batch) | Application Cancellation Letter (NTU); Official Receipt; GIRO letters (all 4); Claim Status Letter (1st); Claim Invite Letter (auto path); Renewal Notice; Lapse Letter |
| User-Initiated (Manual) | Underwriting Requirement Letter; Advisor Requirement Letter; Conditional Acceptance Letter (LCA); Request for Medical Report Letter; MAR Cancellation Letter; Claim Requirement Letter; Medical Report Application; Claim Status Letter (manual path) |
| Mixed (Auto + Manual) | Claim Acknowledgement Letter; Claim Invite Letter |
| Event-Driven (CS Transaction) | CS Pending Premium Letter; CS Confirmation Letter; CS Pending Requirement Letter; Withdrawal of Request Letter; CS Request Unsuccessful Letter |

---

## Config Gaps Commonly Encountered in Letter Management

| Scenario | Gap Type | Config Location |
|---|---|---|
| CC Agent flag per letter | Config Gap | Letter Config → CC Agent = Y (configurable) |
| Renewal Notice lead days (X days before renewal) | Config Gap | Letter Config → Renewal Notice Lead Days |
| Premium Reminder trigger days post renewal date | Config Gap | Letter Config → Premium Reminder Overdue Days (default 60; configurable) |
| NB Premium Reminder trigger period after Letter of Acceptance | Config Gap | Letter Config → NB Collection Grace Period |
| Reminder frequency / interval per letter | Config Gap | Letter Config → Reminder Interval Days |
| Letter template per LOB / product | Config Gap | Letter Management → Letter Template Definition |
| Address type selection per letter | Config Gap | Letter Config → Address Type |
| Auto vs manual generation flag per letter | Config Gap | Letter Config → Auto Generate Indicator |
| Batch advance days for auto-triggered letters | Config Gap | Batch_Advance_Days_Cfg table |

---

## INVARIANT Declarations (Letter Module)

```
INVARIANT 1: Letter of Acceptance is a prerequisite for NB Premium Reminder Letter
  Enforced at: NB Premium Reminder Letter trigger
  Effect: Reminder not generated unless Letter of Acceptance has already been sent

INVARIANT 2: CS Confirmation Letter only generated upon CS transaction reaching In-Force status
  Enforced at: CS Confirmation Letter trigger
  Effect: Letter not generated at approval stage; only upon successful completion

INVARIANT 3: Policy Termination Letter, Claim Recovery Letter, and Claim Review Letter are LTC (SG) only
  Enforced at: Letter generation — LOB check
  Effect: These letters suppressed for all non-LTC LOBs

INVARIANT 4: Claim Status Letter first instance may be auto-triggered by batch; subsequent instances are manual
  Enforced at: Claim Status Letter trigger
  Effect: Only first status letter has batch trigger; follow-ups require manual action in Claim Issue tab

INVARIANT 5: Claim Invite Letter (auto path) requires no active LTC claim AND basic claim approved with monthly payment > 0
  Enforced at: Claim Invite Letter — auto trigger batch
  Effect: Letter suppressed if active LTC claim already exists or monthly payment = 0

INVARIANT 6: MAR Cancellation Letter requires an existing MAR (Request for Medical Report Letter) to cancel
  Enforced at: MAR Cancellation Letter trigger
  Effect: Cannot generate cancellation if no prior medical report request exists for that UW application
```

---

## ⚠️ Limitations & Unsupported Scenarios

> This section documents known limitations and scenarios NOT supported by the system. Updated: 2026-03-14

### Letter Generation

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Custom Letter Templates | Limited | Config | Predefined templates only |
| Dynamic Content | Fixed placeholders | Config | Custom fields limited |
| Real-time Generation | Batch mostly | Config | Some letters real-time capable |

### Delivery Methods

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Email Delivery | Basic | Config | Advanced tracking limited |
| SMS Delivery | Limited | Config | Character limits apply |
| Digital Signature | Not supported | Code | Requires integration |

### Template Management

| Feature | Limitation | Type | Notes |
|---------|------------|------|-------|
| Multi-language | Limited languages | Config | Check available languages |
| Template Versioning | Basic | Config | Advanced versioning needs customization |
| Conditional Content | Limited | Config | Complex conditions need development |

---

## Related Files

| File | Purpose |
|---|---|
| `ps-customer-service.md` | CS transactions that trigger CS APP letters (Confirmation, Pending Premium, Requirement, etc.) |
| `ps-renewal.md` | Renewal batch triggers Renewal Notice and Premium Reminder Letter |
| `ps-fund-administration.md` | ILP fund transaction letters generated post fund transaction confirmation |
| `insuremo-ootb-full.md` | OOTB capability classification (use for Gap Analysis) |
| `output-templates.md` | BSD output templates for letter-related gaps |