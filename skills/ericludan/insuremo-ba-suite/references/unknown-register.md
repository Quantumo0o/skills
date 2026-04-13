# UNKNOWN Register Template & Usage Guide
# Version: 1.0 | Updated: 2026-03

---

## Purpose

This document defines the UNKNOWN Register format, trigger rules, and state transitions for the InsureMO BA workflow.

---

## When to Create UNKNOWN Entry

### Mandatory Triggers (Agent 1 - Gap Analysis)

Create an UNKNOWN entry when:

1. **Cannot determine if feature is OOTB / Config / Dev**
   - After checking `references/InsureMO Knowledge/insuremo-ootb.md` and all `ps-*.md` references
   - No clear match found in OOTB capability matrix

2. **Missing required information**
   - Product specification missing critical details
   - Client requirement is ambiguous despite probing

3. **Conflicting information**
   - Two or more knowledge sources provide contradictory guidance
   - Client provides inconsistent requirements

---

## UNKNOWN Entry Format

```
### UNKNOWN-[###]
**Category**: [OOTB_GAP | CONFIG_PATH | REGULATORY | PRODUCT_BEHAVIOR | THIRD_PARTY | CROSS_SYSTEM]

**Question**: [Specific question that needs clarification]

**Context**: [Where this question arose - which document/process/module]

**Impact**:
- Affects: [Scope/Schedule/Cost/Quality]
- Severity: [High/Medium/Low]
- Blocks: [Implementation/Test/Configuration]

**Investigation Done**:
1. [First source checked]
2. [Second source checked]
3. [Analysis performed]

**Options** (if identified):
- Option A: [Description]
- Option B: [Description]

**Target Resolution Date**: [YYYY-MM-DD]
**SLA Deadline**: [YYYY-MM-DD HH:MM] — High priority only; calculated as Created + 48h
**Created Date**: [YYYY-MM-DD] ← **NEW — mandatory**
**Resolved Date**: [YYYY-MM-DD] ← **NEW — required when terminal state reached**
**Resolved From**: [Free text] ← **NEW — required when terminal state reached. How was it resolved? Example: "Client call 2026-04-05", "ps-claims.md S.3.2 updated", "UAT feedback — reclassified as Dev Gap 2026-04-10"**
**UAT Feedback Trigger**: [TRUE / FALSE] ← **NEW — set TRUE if UAT testing found this OOTB classification was wrong**

**Status History**:
| Date | Status | Updated By | Notes |
|------|--------|-----------|-------|
| YYYY-MM-DD | Open | [Name] | Created |
```

---

## Status Transitions

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│  OPEN   │ ──► │ CLARIFIED  │ ──► │ RESOLVED   │
└─────────┘     └─────────────┘     └─────────────┘
    │               │                   │
    │               │                   │
    │               ▼                   │
    │         ┌─────────────┐          │
    │         │  WONT_FIX  │          │
    │         └─────────────┘          │
    │               │                   │
    └───────────────┴───────────────────┘
                    │
                    ▼
              [Removed from Register]
```

### Status Definitions

| Status | Definition | Action Required |
|--------|------------|----------------|
| **OPEN** | Initial state - question raised | Awaiting client response |
| **CLARIFIED** | Client provided clarification | BA evaluating resolution options |
| **RESOLVED** | Question answered, can classify | Update Gap Matrix / Close entry |
| **WONT_FIX** | Won't fix / Out of scope | Move to Backlog, close entry |
| **REMOVED** | Duplicate / Invalid entry | Close without action |

---

## SLA Timers

SLA timer starts when UNKNOWN is first registered. Timer pauses when status = `CLARIFIED`. Timer resumes when client responds but response is insufficient.

| Priority | SLA | Escalation |
|----------|-----|------------|
| **High** | 48 hours from OPEN | Auto-flag to BA lead at 24h and 48h |
| **Medium** | 5 business days | Reminder at Day 3 |
| **Low** | 30 days | No reminder — tracked passively |

**SLA Clock Rules:**
- Timer starts: UNKNOWN first registered
- Timer pauses: status → `CLARIFIED`
- Timer resumes: client responds but response is insufficient
- Timer stops: terminal state reached (`RESOLVED` / `WONT_FIX` / `REMOVED`)
- Timer expiry: UNKNOWN is escalated — owner must provide update + revised deadline

**Escalation action at SLA expiry:**
→ UNKNOWN is flagged `OVERDUE` in the register
→ BA lead notified for resolution action
→ If > 1 overdue HIGH-severity UNKNOWN → project timeline is at risk

---

## Trigger Rules by Agent

### Agent 0 (Discovery)
- Create UNKNOWN when: Client cannot clarify requirement
- Focus: Business intent, scope boundaries

### Agent 1 (Gap Analysis)
- Create UNKNOWN when: Cannot determine OOTB/Config/Dev classification
- Focus: Technical feasibility, configuration options

### Agent 5 (Product Spec Decoder)
- Create UNKNOWN when: Product spec missing critical information
- Focus: Coverage details, calculation formulas

---

## Agent 5 UNKNOWN Type Classification (v2.0)

Agent 5 uses a **3-way UNKNOWN Type classification** to distinguish between different kinds of missing information. This replaces the simpler UNKNOWN notation for Agent 5 output.

### Three Types of Missing Information

| Type | Definition | Agent 5 Handling | Downstream Action |
|------|------------|-----------------|-------------------|
| **NOT_STATED** | The spec itself does not contain this information | Mark with `[NOT STATED]`; use industry standard default if available | Agent 1 treats as requirement gap — classify as Config/Dev/OOTB |
| **MISSING_ATTACHMENT** | Spec references or mentions this information but the attachment/document is missing | **MUST obtain** — blocks Product Factory config and Agent 1 | Do NOT proceed to Agent 1 until attachment is received |
| **NOT_FOUND** | Spec should contain this section/chapter but it was not found during spec reading | Re-check Step 0.3 section list; confirm if section was skipped | May be a spec quality issue — escalate to client for spec correction |

### Why Three Types?

| Type | Blocks Agent 1? | Blocks Product Factory? | Example |
|------|----------------|------------------------|---------|
| NOT_STATED | No — can proceed with assumption logged | No — config can use default | Age calculation basis (ANB vs ALB) not stated |
| MISSING_ATTACHMENT | **YES — blocks** | **YES — blocks** | Rate table referenced but not attached |
| NOT_FOUND | No — but flag for verification | No — if section truly missing | HI rider term section referenced but not found |

### Agent 5 → Agent 1 Handoff

When Agent 5 produces a Product Profile with UNKNOWNs:

```
IF UNKNOWN.type = MISSING_ATTACHMENT:
  → Product Profile Summary outputs: ⛔ STOP — do not proceed to Agent 1
  → List all MISSING_ATTACHMENT UNKNOWNs with "MUST obtain before Agent 1"

IF UNKNOWN.type = NOT_STATED:
  → Product Profile Summary outputs: "Can proceed to Agent 1 with assumption logged"
  → Each NOT_STATED UNKNOWN is logged with default assumption if used

IF UNKNOWN.type = NOT_FOUND:
  → Product Profile Summary outputs: "Re-check spec before proceeding"
  → Agent 1 should verify spec completeness before gap analysis
```

### Integration with Existing UNKNOWN Register

The existing UNKNOWN Register (Agent 1) uses `OPEN / CLARIFIED / RESOLVED / WONT_FIX` status workflow. Agent 5 UNKNOWN Types feed into this workflow as follows:

| Agent 5 UNKNOWN Type | Becomes Agent 1 Entry? | Initial Status | Notes |
|---------------------|----------------------|----------------|-------|
| NOT_STATED | Yes, if it affects gap classification | OPEN | BA must classify as Config/Dev/OOTB |
| MISSING_ATTACHMENT | Yes, after attachment received | OPEN | Blocks until attachment obtained |
| NOT_FOUND | Yes, after section confirmed missing | OPEN | Escalate to client for spec correction |

### Example: Agent 5 UNKNOWN Entry

```
### UNKNOWN-[###]
**Category**: PRODUCT_BEHAVIOR
**Type**: NOT_STATED
**Dimension**: Dim 2 — Eligibility & Underwriting
**Question**: What is the age calculation basis (ANB vs ALB)?
**Context**: Premium calculation in Dim 3 requires this to finalize
**Impact**: High — all age-based premium formulas cannot be finalized
**Investigation Done**:
1. Checked spec Section 3 (Premium) — not mentioned
2. Checked spec Section 2 (Eligibility) — not mentioned
3. No industry standard default applies — market practice varies
**Options**: ANB / ALB — client must confirm
**Created Date**: [YYYY-MM-DD]
**Target Resolution Date**: [YYYY-MM-DD]
**Status**: OPEN
```

---

## Usage Example

```
### UNKNOWN-001
**Category**: OOTB_GAP

**Question**: Does InsureMO support automatic premium holiday after 3 consecutive missed payments?

**Context**: 
- Product: UL with Waiver of Premium Rider
- Module: Premium Collection
- Source: Client requirement doc

**Impact**:
- Affects: Scope
- Severity: High
- Blocks: Agent 1 Gap Classification

**Investigation Done**:
1. Checked `references/InsureMO Knowledge/insuremo-ootb.md` - No explicit mention
2. Checked `references/InsureMO Knowledge/ps-customer-service.md` - Premium holiday exists but trigger is manual
3. Checked Product Factory config - No auto-trigger configuration found

**Options**:
- Option A: Manual premium holiday trigger (current OOTB)
- Option B: Custom development for auto-trigger
- Option C: Workaround via CS process

**Target Resolution Date**: 2026-03-20

**Status History**:
| Date | Status | Updated By | Notes |
|------|--------|-----------|-------|
| 2026-03-13 | Open | Lele | Created from Gap Analysis |
```

---

## Integration with Output Templates

### In BSD (Appendix C)

```
## Appendix C: UNKNOWN Register

| ID | UNKNOWN Item | Source | Impact Severity | Estimated Effort (h-days) | Owner | Status | Created | SLA Deadline | UAT Feedback |
|----|-------------|--------|----------------|---------------------------|-------|--------|---------|--------------|--------------|
| UNKNOWN-001 | [Brief description of unknown item] | Client doc / PS spec / OOTB check | High / Medium / Low | Xh or Xd | [Owner] | Open | YYYY-MM-DD | YYYY-MM-DD HH:MM | FALSE |

**Column Descriptions:**

| Column | Description |
|--------|-------------|
| ID | UNKNOWN-001 to UNKNOWN-999 |
| UNKNOWN Item | Brief description of the unknown question |
| Source | Where the question arose: Client doc / PS spec / OOTB check / Regulatory |
| Impact Severity | High / Medium / Low |
| Estimated Effort (h-days) | Provide best-effort estimate in hours/days. Format: Xh (hours) or Xd (days). Use:<br>- 1-2h: Minor clarification needed<br>- 4-8h: Requires small research spike<br>- 1-2d: Needs dedicated investigation<br>- 3d+: Major discovery work required |
| Owner | Person responsible for resolving |
| Status | Open / Clarified / Resolved / WontFix / Removed |
| Created | Date the UNKNOWN was first registered (YYYY-MM-DD) — **mandatory** |
| SLA Deadline | Calculated: Created + 48h for High priority, +5d for Medium. Left blank for Low. — **mandatory for High** |
| UAT Feedback | TRUE / FALSE — set TRUE if UAT testing found this OOTB classification was wrong |

| Example Entry | |
|--------------|--|
| UNKNOWN-001 | Auto PH trigger — High - Scope - Open - 4h |
| UNKNOWN-002 | STP config path — Medium - Schedule - Clarified - 1d |
```

### In Gap Matrix

Add column for UNKNOWN references:
```
| Feature | Requirement | OOTB | Gap Type | UNKNOWN Ref | Priority |
|---------|------------|------|----------|-------------|----------|
| Premium Holiday | Auto-trigger | ? | ? | UNKNOWN-001 | High |
```

---

## Quality Gates

- [ ] Every UNKNOWN has Impact severity rated
- [ ] Every UNKNOWN has `Created_Date` and `SLA_Deadline` (High priority only)
- [ ] Zero OPEN items older than 48h without escalation record
- [ ] Every terminal-state UNKNOWN has `Resolved_Date` and `Resolved_From`
- [ ] Every UNKNOWN with `UAT_Feedback_Trigger = TRUE` is re-triggering Agent 1
- [ ] Open UNKNOWNs reviewed in weekly sync
- [ ] UNKNOWN-001 to UNKNOWN-999 format maintained
- [ ] Status transitions logged with date and owner
- [ ] High severity UNKNOWN blocks scope confirmation
- [ ] Resolved UNKNOWNs used to update knowledge base
- [ ] Overdue SLA items escalated to BA lead

---

## UAT Feedback Loop

When UAT testing discovers that an OOTB-classified feature failed:

1. UAT tester or BA sets `UAT_Feedback_Trigger = TRUE` on the relevant UNKNOWN entry
2. If the entry is in a terminal state (`RESOLVED` / `WONT_FIX` / `REMOVED`):
   → Re-open the entry: status → `OPEN`
   → Assign new SLA deadline from re-open date
   → Issue new UNKNOWN ID if the item is re-framed as a different gap
3. `Resolved_From` on the original entry records: `"Re-opened due to UAT feedback [YYYY-MM-DD]"`
4. Agent 1 is re-triggered to re-analyze the item
5. The re-analysis result updates the Gap Matrix with corrected classification
6. If confirmed as OOTB misclassification → update the relevant `ps-*.md` KB file with the correction

**Feedback Loop Integration Points:**

| Stage | Action | Register Update |
|-------|--------|----------------|
| UAT execution | Any OOTB claim fails | Set `UAT_Feedback_Trigger = TRUE` on UNKNOWN entry |
| UAT sign-off | UNKNOWN with `UAT_Feedback_Trigger = TRUE` exists | Block UAT sign-off until resolved |
| Post-project | KB correction identified | Update `ps-*.md` with corrected OOTB status |
