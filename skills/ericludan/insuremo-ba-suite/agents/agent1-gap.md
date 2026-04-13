# Agent 1: Gap Analysis
# Version 1.8 | Updated: 2026-04-08 | Portability fix: V3 UG path replaced with relative path

## Trigger Condition
INPUT_TYPE = `PARSED_CLIENT_DOC` or a completed Requirement Brief

## Input Format
```
[PARSED_CLIENT_DOC]
source_file: "filename"
extracted_features:
  - feature_id: F001
    description: "..."
    raw_text: "original text excerpt"
```

## Prohibited Actions
- Do NOT add features not mentioned in the client document
- **Do NOT assume OOTB** — verify each item against the **PURE** `references/InsureMO Knowledge/insuremo-ootb.md` (only ✅ items)
- **Do NOT search too narrowly** — same feature may have different field names in different sections
- Do NOT include Low Priority items in the current delivery scope
- Do NOT begin gap classification until the Pre-Analysis Checklist is complete
- Do NOT mix OOTB with Config/Dev gaps in the reference file (see 2026-03-13 cleanup)

---

## ⚠️ CRITICAL: BROAD Search + Cross-Validate

When searching ps-* knowledge base, you MUST:

### Step 1: Use BROAD Keywords
The same option may appear under **different field names**:
- Example: "Effective Date" can also be found as:
  - `Effective Date type`
  - `Commencement type`
  - `Next Due Date`
  - `Anniversary`

### Step 2: Cross-Validate Multiple Sections
- Don't stop at first match
- Search for the same concept in **multiple sections**
- Verify all possible locations before concluding

### Step 3: Document All Variations
If you find different field names for the same feature, document all of them in your analysis.

---

## Pre-Analysis Checklist (mandatory before Step 1)
All four items must be confirmed before any gap extraction begins:
- [ ] Scope explicitly defined — products / riders / markets / screens are named
- [ ] Future state goals are specific and measurable (not "improve the system")
- [ ] Current state documentation reviewed and validated with stakeholders
- [ ] Stakeholder alignment confirmed on scope and objectives

**Automation Tools (must be run before gap analysis):**
- [ ] **R10 Scanner** — Run `scripts/r10-scanner.py` on the source spec before analysis:
  ```
  python scripts/r10-scanner.py [spec_file.txt] --show-context
  ```
  All R10-flagged features must have R10 = YES in the Gap Matrix.
- [ ] **Traceability Checker** — After BSD is written, run `scripts/traceability-checker.py` to verify BSD → Gap Matrix traceability:
  ```
  python scripts/traceability-checker.py --bsd [BSD_FILE] --gap-matrix [GAP_MATRIX_FILE]
  ```
- [ ] **KB Coverage Audit** — Before gap extraction, verify every spec §N has a corresponding KB file (per kb-manifest.md). Sections with KB MISSING but concrete spec parameters → must still be analyzed (do NOT skip). See Step 2B.6 for the KB-Missing Degradation strategy.

**R1-R9 Systematic Checklist (must be run before Gap Matrix finalization):**
- [ ] **R1 NFR** — Scanned for performance SLAs, availability, data residency, security, DR requirements *(→ actually executed in Step 2C — not a separate Pre-Analysis task)*
- [ ] **R2 Blind Spot** — Every functional requirement has a matching KB row or is flagged as blind spot *(→ actually executed in Step 2E — see §R2 Execution below)*
- [ ] **R3 Overflow** — Every OOTB/Config item tested against R3 overflow table (Step 2B.7)
- [ ] **R4 Integration** — Every third-party integration has an R4 Integration Record (Step 2B.8)
- [ ] **R5 Migration** — Confirmed greenfield (no legacy migration scope) or data migration section added *(→ handled in Step 2B.5 KB-Missing Degradation — R5 is a scope check, not a separate analysis step)*
- [ ] **R6 Regulatory** — Market-specific regulatory matrix applied (MAS/BNM/OJK/OIC/IA); Agent 3 triggered where required *(→ actually executed within Step 2B classification logic — see Step 2B §R6 Note below)*
- [ ] **R7 UI/UX** — Every user-facing Dev Gap has R7 UI/UX dimension recorded in Solution Design *(→ actually executed in Step 2D)*
- [ ] **R8 Batch/SLA** — Every monitoring/enforce pattern checked for batch vs real-time vs manual *(→ actually executed in Step 2B.9)*
- [ ] **R9 Complexity** — Every Config Gap complexity-rated (Low/Medium/High) *(→ actually executed in Step 2B.10)*
- [ ] **Dev Gap SD 100% Coverage — HARD GATE** — every Dev Gap has a completed Solution Design Template. Zero exceptions. If any SD is missing, the Gap Matrix is INCOMPLETE and must NOT be submitted to Agent 2.
- [ ] **R10** — Scanned all features against R10 keyword list; all matches have Dev Gap or override justification *(→ actually executed in Step 2A — R10 is the first gate, not a final checklist)*

If any item is unchecked → stop and address before finalizing Gap Matrix.

---

## Gap Severity Reference

| Severity | Business Impact | Urgency | Priority |
|----------|----------------|---------|----------|
| Critical | >$100k financial impact / regulatory non-compliance / blocks core flow | Immediate — resolve within 2 weeks | High |
| High | $10k-$100k impact / affects >1,000 users / workaround is costly | Resolve within 4 weeks | High |
| Medium | $1k-$10k impact / affects 100-1,000 users / workaround exists | Resolve within 8 weeks | Medium |
| Low | <$1k impact / affects <100 users / cosmetic change | Deferrable to future release | Low — Backlog |

Use this table to assign Priority in Step 4. Document which criterion was applied.

---

---

## Mode B: Rapid Change Scan (Natural Language Requirements)

> **When to use Mode B:** Dan provides a requirement in natural language (email, meeting notes, verbal description) — NOT a product spec PDF. Mode B is a lightweight scan that produces a structured Gap Analysis Note in 15–30 minutes. It is NOT a substitute for the full Phase 0→1→2 flow when a formal Gap Matrix + BSD is required.

**Mode B vs Mode A (Product Spec Analysis):**

| Dimension | Mode A (Product Spec) | Mode B (Rapid Scan) |
|-----------|----------------------|---------------------|
| Input | Product spec PDF | Natural language requirement |
| KB depth | Full KB search | Targeted 4–6 files |
| Output | Gap Matrix + Dev Gap SD Template | Gap Analysis Note |
| Time | 30–60 min | 15–20 min |
| Use case | Client delivery | Internal initial assessment |
| Quality gate | GATE-A/B/C before output | Step 7 Checklist |

### Step 1: Change Type Identification (30 seconds)

Identify the **primary Change Type** from the requirement description:

| Change Type | Trigger Keywords | Primary Route |
|-------------|-----------------|---------------|
| **Functional** | New benefit, rider, rule change, product variant | Mode B applies |
| **Operational** | Process efficiency, UI change, workflow | Mode B applies |
| **Regulatory** | MAS/HKIA/BNM/OIC compliance | Agent 3 + Mode B parallel |
| **Technical** | API version, integration, system upgrade | Consider Agent 9 |
| **Data** | Historical migration, legacy conversion | Agent 9 + Mode B |

If multiple types apply, use the **highest-risk type** as primary route.

### Step 2: Scope Lock (1 minute)

Explicitly declare what this scan **covers** and **does not cover**:

**Covers:**
- Affected InsureMO modules: [NB / CS / UW / Claims / Billing / RI / Fund Admin]
- Specific CS Items or features involved

**Does NOT Cover:**
- [e.g., NB illustration impact, unless explicitly mentioned]

> **Why Scope Lock matters in Mode B:** Without a product spec, the requirement may imply changes outside its apparent scope. Explicitly bounding the scan prevents mission creep and sets client expectations.

### Step 3: Key KB Rapid Search (5–7 minutes)

**Rule:** Read strategically, not exhaustively.

For each affected module, search **1–2 key KB files** with **3 targeted keywords**. Do NOT read entire files.

**Targeted KB files by module:**

| Module | Primary KB File | Keywords to Search |
|--------|----------------|-------------------|
| CS (alterations) | `insuremo-v3-ug-cs-new.md` | [feature name, e.g., "Increase SA", "SA change"] |
| CS (workflow) | `ps-customer-service.md` | [CS Item name, e.g., "Sum Assured", "Increase"] |
| Renewal/Billing | `insuremo-v3-ug-renewal.md` | ["anniversary", "premium due", "billing"] |
| UW | `ps-underwriting.md` | ["underwriting review", "extra premium", "SA"] |
| RI | `ps-reinsurance.md` OR `insuremo-v3-ug-reinsurance.md` | ["cession", "SAR", "reinsurance"] |
| Fund Admin | `ps-fund-administration.md` | ["surrender", "withdrawal", "ILP"] |
| Product Config | `ps-product-factory-limo-product-config.md` | [feature config, e.g., "SA change", "Not Allowed CS Items"] |

**Search output format (per file):**

```
KB File: [filename]
Keywords searched: [3 keywords]
Findings:
  - [keyword]: [what InsureMO does / does not support]
  - [keyword]: [evidence from KB, include section/line reference]
KB Conclusion: [Supports OOTB / Config Gap found / Dev Gap found / Not found]
Confidence: [H/M/L] — [reason]
```

### Step 4: Gap Preliminary Classification (2 minutes)

Classify each identified gap using the **same four-category system** as Mode A:

| Classification | Definition | Action |
|---------------|-----------|--------|
| **OOTB** | InsureMO supports natively | Note and move on |
| **Config Gap** | InsureMO supports but requires product/config change | Flag for Config item |
| **Dev Gap** | InsureMO does not support; requires development | Flag for BSD |
| **UNKNOWN** | InsureMO behavior not confirmed in KB | Flag for client clarification |

**Per gap, record:**
```
Gap-[N]: [Brief name]
  InsureMO Status: [OOTB / Config / Dev / Unknown]
  KB Evidence: [File] — [quote or section reference]
  Confidence: [H/M/L] — [why]
  Action: [None / Config item / BSD / Client clarification]
```

> **Confidence Rule:** If KB does not explicitly confirm OOTB, do NOT classify as OOTB. Lower confidence = more likely to need Mode A full analysis later.

### Step 5: Open Questions Extraction (1 minute)

List every question that **blocks decision**:

| Q# | Question | Impact | Owner | Priority |
|----|----------|--------|-------|---------|
| OQ-01 | [e.g., Is anniversary date defined as policy year rollover or modal due date in anniversary month?] | Blocks: Gap classification | Client | P1 |
| OQ-02 | [e.g., Which SA applies if claim occurs before anniversary?] | Blocks: Dev Gap rule | Underwriter | P1 |

> **Rule:** If you cannot find the answer in KB in 2 minutes, it is an Open Question. Do NOT guess.

### Step 6: Ripple Quick Check (1 minute)

Check 6 key ripple vectors. For each, estimate magnitude:

| Ripple Vector | Magnitude | Notes |
|--------------|-----------|-------|
| NB Illustration ↔ Claims | [High/Medium/Low] | [impact description] |
| Underwriting ↔ RI | [High/Medium/Low] | [impact description] |
| Fund Admin ↔ CS | [High/Medium/Low] | [impact description] |
| Billing ↔ Policy Admin | [High/Medium/Low] | [impact description] |
| Claims ↔ RI | [High/Medium/Low] | [impact description] |

### Step 7: Gap Analysis Note Output (structured, deliverable)

**Produce this output as a file** (not just chat text). Recommended path:
```
work/YYYY-MM-DD/GapAnalysisNote_[Product]_[Feature]_v1.0.md
```

**Gap Analysis Note template:**

---

# Gap Analysis Note: [Feature Name]
**Date:** [YYYY-MM-DD]
**Product:** [Product Name]
**Analyst:** Lele
**Mode:** Mode B — Rapid Change Scan
**Requirement Source:** [Dan description / email / meeting notes]
**Change Type:** [Primary type]

## Scope
**Covers:** [Modules and features]
**Does NOT Cover:** [Explicit exclusions]

## Change Type: [Type]
[1-sentence justification]

## KB Coverage Log

| KB File | Keywords | Conclusion | Confidence |
|---------|----------|-----------|-----------|
| [file] | [3 keywords] | [finding] | [H/M/L] |

## Gap Summary

| Gap ID | Feature | InsureMO Status | KB Evidence | Confidence | Action |
|--------|---------|----------------|-------------|-----------|--------|
| Gap-1 | [name] | [OOTB/Config/Dev/UNKNOWN] | [file] — [ref] | [H/M/L] | [None/Config/BSD/Clarification] |

## Open Questions (Blocking)

| Q# | Question | Impact | Owner | Priority |
|----|----------|--------|-------|---------|
| OQ-01 | [text] | Blocks: [what] | [who] | P1 |

## Ripple Check

| Module Pair | Magnitude | Description |
|-------------|-----------|-------------|
| UW → RI | [H/M/L] | [description] |

## Recommendation

- [ ] **Proceed to Mode A (Full Gap Matrix + BSD)** — required for Dev Gaps identified
- [ ] **Config Only** — no Dev Gap; proceed to Agent 6 Config Runbook
- [ ] **Client Clarification First** — OQ-01/02 must be resolved before classification
- [ ] **No Action** — OOTB confirmed; no change required

---

### Mode B Quality Checklist (before sending to Dan)

Before completing Mode B, confirm:

- [ ] Change Type is explicitly stated and justified
- [ ] Scope boundaries are explicit (what is NOT covered)
- [ ] Every gap cites a KB file + section reference (no unverified claims)
- [ ] Every UNKNOWN is recorded as an Open Question with Owner + Priority
- [ ] Confidence is H/M/L for every gap classification
- [ ] Recommendation explicitly states next action
- [ ] Output is written to a file (not just chat text)

### Transitioning from Mode B to Mode A

Mode B is **not** a substitute for Mode A when:
- Dev Gap is confirmed with Confidence = H
- Client needs a formal Gap Matrix for stakeholder review
- BSD writing is required before development can start
- Regulatory compliance needs formal Agent 3 sign-off

To transition: share the Gap Analysis Note with Dan, confirm next action, then re-run Agent 1 with the full product spec as Mode A input.

---

## Phase 0: KB Readiness Check (MANDATORY — before anything else)

> **Problem from v3.0实战:** `ps-reinsurance.md` was missing, causing all reinsurance-related features to be incorrectly classified as Dev Gap + KB-Missing. This was discovered AFTER the full analysis — too late.

**Step 0** runs BEFORE Step 1 to catch missing KB files upfront.

```
FOR each spec section (§1 through §11 or equivalent):
  1. Look up the corresponding KB file in kb-manifest.md
  2. IF the KB file exists and is populated (> 1KB):
       → Mark: KB_READY = TRUE for this section
  3. IF the KB file does NOT exist or is empty (< 1KB):
       → Mark: KB_READY = FALSE
       → Add to KB Risk Register: "§N uses [topic] but [KB file] is MISSING/EMPTY"
  4. IF spec has features related to the missing KB section:
       → Add WARNING: "§N has [X] features requiring [KB file] — will use KB-Missing Degradation"
```

**KB Readiness Report (output of Step 0):**
```
## KB Readiness Report

| Spec Section | KB File | Status | Risk Items |
|-------------|---------|--------|-----------|
| §1 General Info | ps-product-factory.md | ✅ READY | — |
| §3 Premium | ps-product-factory.md | ✅ READY | — |
| §5 Fees & Charges | ps-product-factory.md | ✅ READY | — |
| §8 Reinsurance | ps-reinsurance.md | 🔴 MISSING | 3 features at risk |

KB Risk Items:
  🔴 ps-reinsurance.md MISSING — §8 has RGA quota share features. All §8 items will use KB-Missing Degradation (Step 2B.6). Pre-flag as Dev Gap + R4 candidates.
  🟡 ps-document-generation.md MISSING — §10 has permitted asset documentation. May affect policy document output.
```

**Step 0 must be complete before proceeding. If KB gaps are found, note them in the Gap Matrix KB Risk Register column.**

---

## Phase 1: Triage Scan (MANDATORY — before full analysis)

> **Problem from v3.0实战:** 60 Gap IDs at full 20-step depth caused token/time overflow risk. Not all features are equally risky — triage first.

**Phase 1** is a FAST scan of the entire spec (read all sections, 30-60 minutes) to classify each feature as High / Medium / Low risk before Phase 2 deep dive.

**Phase 1 Triage Criteria — CONSERVATIVE VERSION:**

> **&#9888; HARD RULE: When in doubt, mark HIGH. The cost of under-triaging a Dev Gap is 11 missing BSDs. The cost of over-triaging is extra analysis minutes.**

| Risk Level | Criteria | Phase 2 Depth |
|------------|---------|--------------|
| 🔴 **High — MANDATORY** | ANY formula in spec (MAX/MIN/IF-THEN/conditional/tiered); ANY regulatory/compliance keyword; ANY third-party integration; ANY cross-policy/cross-system data; ANY UNKNOWN; No KB file for this section; Death/TI/ Surrender/Maturity benefits; SA reduction rules; Benefit cap/limit rules; Currency/ conversion rules; Commission/payment rules | Full 20-step analysis |
| 🟡 **Medium — PRE-SCREEN REQUIRED** | Config Gap clearly indicated in spec AND KB has explicit Config Path for the exact parameter AND no formula/variant/cross-module involved. If uncertain, mark HIGH instead. | Abbreviated: Steps 1-2B-2E-3-4 only |
| 🟢 **Low — RARE** | ONLY if ALL of: (a) spec explicitly states OOTB supported; (b) KB has explicit OOTB section for this exact feature; (c) no variants in spec; (d) no formula/conditional logic; (e) no cross-module impact. If any of these fail, mark HIGH. | Lite: Steps 1-2B only |

**Safe Harbor — features that MUST be marked HIGH regardless of other signals:**
```
- Death Benefit / TD / TI / Maturity / Surrender Benefit formulas
- SA reduction rules (partial withdrawal, TI payment, top-up)
- Benefit caps or limits (per life, per policy, aggregate)
- Premium loading or charge formulas
- RI cession or recovery calculations
- Currency conversion or FX rules
- Commission or compensation rules
- Any "or equivalent" or "as determined by" language in spec
- Any threshold that triggers a different calculation
- Any tiered/banded parameter
```

**Phase 1 Triage Post-Processing Rule:**
> After initial triage, cross-check: if any feature was marked Medium or Low but has a formula in the spec, OR has R10 keywords, OR was flagged as potentially complex in the spec — **UPGRADE TO HIGH IMMEDIATELY**. Do not continue with abbreviated analysis for such features.

**Phase 1 Output — Triage Register:**
```
## Phase 1 Triage Register

| Feature ID | Feature Description | Spec Ref | Triage Risk | Rationale |
|------------|------------------|----------|-------------|-----------|
| F001 | Death Benefit formula | §5, p.11 | 🔴 High | R10 (MAX/SAR/PFV formula) + cross-policy |
| F002 | TI Benefit cap USD 2M | §5, p.12 | 🔴 High | R10 (per life) + R6 (LIA CI Framework) + R4 (global counter) |
| F003 | Policy currency selection | §1, p.7 | 🟢 Low | OOTB confirmed ps-product-factory.md §II.2 |
| F004 | Establishment Fee dialable 5-12% | §3, p.9 | 🟡 Medium | Config likely; KB has Premium Charge config |
| ... | ... | ... | ... | ... |

Phase 1 Summary:
  🔴 High: X features → Full 20-step analysis in Phase 2
  🟡 Medium: X features → Abbreviated 5-step analysis in Phase 2
  🟢 Low: X features → Lite 2-step in Phase 2
```

**⚠️ Rule:** Do NOT skip Phase 1. Every feature must appear in the Triage Register before Phase 2 begins. If a feature is not in the register, it was not triaged — do not analyze it.

**Phase 1 must complete before Phase 2. Triage risk level can be upgraded (not downgraded) during Phase 2 if new information emerges.**

---

## Phase 2: Deep Dive Analysis

> Phase 2 applies full analysis depth based on Phase 1 triage level.

---

### Step 1 — Feature Extraction with Business Semantic Understanding
Extract every functional requirement, business rule, and UI requirement from the input document.
Assign a unique ID (F001, F002...) to each item. Record the original text for traceability.

**⚠️ CRITICAL: Business Semantic Understanding Checklist**
Before extracting features, MUST analyze the product spec for these patterns:

#### 1. Cross-System / Cross-Policy Patterns
| Pattern Keywords | Example from Spec | Gap Implication |
|-----------------|-------------------|----------------|
| "per life", "across all policies", "cumulative" | "USD 2M max per life (all policies)" | Requires cross-policy data check → **Dev Gap** |
| "aggregate", "total", "combined" | "aggregate limit across products" | Requires global counter → **Dev Gap** |
| "any other policies", "existing policy" | "check any existing policies" | Requires policy lookup → **Dev Gap** |

#### 2. Dynamic Calculation Patterns
| Pattern Keywords | Example from Spec | Gap Implication |
|-----------------|-------------------|----------------|
| "MAX(A, B)", "MIN(A, B)" | "MAX(Sum Assured - Withdrawals, PFV)" | May be configurable or require dev |
| "percentage of", "% of" | "15% of Initial Premium" | Check if formula is fixed or configurable |
| "tiered", "sliding scale" | "0% if ≤25%, 5% on excess" | Complex tier logic → verify config support |

#### 3. Third-Party Integration Patterns
| Pattern Keywords | Example from Spec | Gap Implication |
|-----------------|-------------------|----------------|
| "custodian", "asset manager" | "Platform partner custodians" | External system integration → **Dev Gap** |
| "reinsurer", "quota share" | "50% Quota Share to reinsurer" | RI system integration → **Dev Gap** |
| "exchange", "listed" | "listed securities" | Trading system integration → **Dev Gap** |

#### 4. Regulatory / Compliance Patterns
| Pattern Keywords | Example from Spec | Gap Implication |
|-----------------|-------------------|----------------|
| "MAS", "SFA", "CMFAS" | "SFA Section 4A" | Regulatory module → **Dev Gap** |
| "disclosure", "notice" | "MAS Notice 307" | Process Gap - compliance team |
| "license", "certification" | "CMFAS license" | Process Gap - ops team |

#### 5. Boundary Condition Patterns
| Pattern Keywords | Example from Spec | Gap Implication |
|-----------------|-------------------|----------------|
| "no limit", "unlimited" | "No maximum limit" | May not be truly unlimited → research |
| "first", "initial", "1st time" | "first withdrawal free" | State tracking needed → verify |
| "maintain", "must maintain" | "maintain minimum PFV" | Ongoing validation → **Dev Gap** |

**Output from Step 1:** Each extracted feature must have:
- [ ] Original spec text (verbatim)
- [ ] Section/Page reference
- [ ] Semantic interpretation (what it really means)
- [ ] Cross-system flag (Y/N)
- [ ] Third-party flag (Y/N)

### Step 1.5 — Spec Traceability (MANDATORY for every Gap entry)

> Every Gap ID must trace back to the source spec. This is non-negotiable.
> Without section/page references, the Gap Matrix cannot be verified or audited.

```
For each feature extracted from the Product Profile:

Step 1.5.1: Record the SPEC SECTION and PAGE NUMBER
  → "Spec §X.X — [Section Title], p.Y"
  → Copy the EXACT section heading as it appears in the spec
  → Example: "Section 8.3 — Establishment Fee for Initial Premium, p.8"

Step 1.5.2: Copy the ORIGINAL SPEC TEXT verbatim
  → Do NOT paraphrase, summarize, or interpret
  → Use quotation marks; include the exact quote
  → Example: "Establishment Fee for Initial Premium (% of Premium): Up to 12.0% of Initial Premium"

Step 1.5.3: Verify the Product Profile references this section
  → Confirm the Product Profile FORMULA-ID or CFG-ID maps to this spec section
  → If the Product Profile does NOT reference this section → flag it

IF any gap cannot be traced to a specific spec section/page:
  → Mark as "Source: UNKNOWN — spec section not found"
  → This is a Gap Analysis quality defect — do not proceed without fixing
```

---

### Step 2 — Gap Classification (Two-Pass + Unknown-First + R10 Pre-Scan + Semantic Validation)

> **IMPORTANT:** This step has THREE mandatory sub-steps executed in order.
> Step 2A (R10 Scan) fires FIRST, before any OOTB lookup. It cannot be skipped.

---

#### Step 2A — R10 Cross-System Semantic Scan (MANDATORY — fires first)

> **Automation:** Run `scripts/r10-scanner.py` on the source spec FIRST to get all R10 keyword matches with line numbers. Cross-reference matches to features in the Product Profile.

**Workflow:**
```
Step A1: Run scanner: python scripts/r10-scanner.py [spec_file.txt] --json > r10_results.json
Step A2: For each R10 match in r10_results.json:
  - Note the line number and keyword matched
  - Find which feature's raw_text/spec section contains this line
  - Mark that feature with R10_Flag = YES
Step A3: If scanner unavailable (manual mode):
  Manually scan each feature's raw_text and description against the R10 keyword list below.
```

Before any OOTB lookup, scan every feature's `raw_text` and `description` against the R10 keyword list
(`references/insuremo-gap-detection-rules.md` Rule R10):

```
FOR each feature F:
  FOR each keyword K in R10_KEYWORD_LIST:
    IF K found in F.raw_text OR F.description:
      SET F.gap_type → "Dev Gap"  (pre-classified, not yet final)
      SET F.R10_Flag = "YES"
      ADD to F.notes: "R10-[K] triggered. Override requires cited proof of native
                       InsureMO cross-policy/cross-system support — see R10 override
                       conditions in insuremo-gap-detection-rules.md."
```

**R10 Keyword List (from `references/insuremo-gap-detection-rules.md`):**

Cross-Policy / Aggregate Patterns:
- `per life`, `lifetime`, `lifetime limit`, `across all policies`, `any existing policy`, `all policies`
- `cumulative`, `aggregate`, `total across`, `combined`, `combined limit`, `aggregate limit`
- `in-force`, `lapsed policy`, `reinstatement`, `policy count`
- `contestable`, `misrepresentation`, `concealment`, `non-disclosure`

Third-Party / Reinsurance Patterns:
- `custodian`, `custody`, `asset manager`, `fund manager`
- `reinsurer`, `quota share`, `ceding`, `ceding company`, `retrocession`, `retention limit`
- `listed securities`, `exchange`, `trading`, `market data`, `real-time NAV`

Dynamic / Real-Time Calculation Patterns:
- `real-time`, `on-the-fly`, `dynamic calculation`, `dynamic`
- `MAX(`, `MIN(`, `whichever is higher`, `whichever is lower`, `greater of`

Regulatory / Compliance Patterns:
- `regulatory filing`, `submission to [authority]`, `MAS`, `BNM`, `OJK`, `IA35`
- `disclosure`, `notice`, `compliance`, `license`, `authorisation`

**Output from Step 2A:** All R10-flagged items are pre-classified as Dev Gap.
Proceed to Step 2B.

---

#### Step 2B — OOTB Classification Lookup (fires after Step 2A)

Use BOTH `references/InsureMO Knowledge/insuremo-ootb.md` and `ps-*.md` documents together for comprehensive analysis:

**🎯 Core Principle: "Not Explicitly Documented = UNKNOWN"**
- If ps-docs do NOT explicitly state "supported", assume UNKNOWN
- Absence of documentation ≠ proof of capability
- This prevents gaps from being missed due to incomplete KB

**Pass 1 — Quick Scan (references/InsureMO Knowledge/insuremo-ootb.md):**
- `references/InsureMO Knowledge/insuremo-ootb.md` — **PURE OOTB** capability list
- Purpose: Quick index to locate relevant capability areas
- ⚠️ OOTB alone is NOT sufficient for classification

**Pass 2 — Detailed Verification (ps-*.md):**

> Before starting, read the **KB Registry** at `references/kb-manifest.md` to find the correct KB file for your module. Do NOT rely on hardcoded lists.

- Check the **Module → KB File Mapping** table in `references/kb-manifest.md`
- For each feature, identify the relevant module and read the corresponding KB file
- Always check the **Coverage** column to confirm the file covers your specific topic
- If a module is not listed or coverage is unclear → mark as `UNKNOWN — requires KB confirmation`

**Pass 3 — Limitation Check:**
- Check **⚠️ Limitations & Unsupported Scenarios** section in each KB file
- Check **⚠️ Limitations & Non-Configurable Items** in `references/InsureMO Knowledge/ps-product-factory.md`

**R10 Override (Step 2B only — applies only to R10-flagged items):**
A feature pre-flagged as Dev Gap by R10 Step 2A may be overridden to Config Gap or OOTB
ONLY if **all three** substantive conditions are met (cite sources in Gap Matrix notes):

1. InsureMO natively supports cross-policy lookups for this specific pattern
2. A documented OOTB config path exists (cite exact Product Factory path from ps-*.md)
3. The capability is confirmed in the relevant `ps-*.md` module guide

**And** the following documentation requirement must also be met:
4. Override justification written in Gap Matrix notes: `"R10 OVERRIDE: [which conditions met + KB citation]"`

**If any R10 keyword is matched but no override proof exists → Dev Gap classification stands.**



#### Step 2B.5 — InsureMO V3 User Guide Cross-Reference (MANDATORY when available)

> **IMPORTANT:** This step runs AFTER Step 2B (ps-docs check) and BEFORE Step 2C (Semantic Override). V3 cannot override a ps-docs Dev Gap, but can upgrade OOTB/Config to Dev Gap or resolve UNKNOWNs.
> It applies to every feature where ps-docs gave a non-Dev classification (OOTB / Config / UNKNOWN).

**Purpose:** Validate or challenge the ps-docs conclusion against the more detailed V3 User Guide.
V3 findings are labeled `V3-OOTB` / `V3-Config` / `V3-Dev` / `V3-UNKNOWN` to distinguish them from ps-docs findings.

**When to run:**
```
IF ps-docs Classification is OOTB / Config / UNKNOWN AND InsureMO V3 User Guide is available for this module:
  → Run Step 2B.5
IF ps-docs Classification is Dev Gap AND InsureMO V3 User Guide is available:
  → Run Step 2B.5 — V3 may confirm OR reveal the Dev Gap classification was premature
  → V3 can downgrade Dev Gap to Config/OOTB ONLY if V3 provides explicit evidence the limitation does not apply
```

> **V3 File Location:** All V3 User Guides are in:
> `./references/InsureMO V3 User Guide/`
> When reading a V3 file, use the path above + filename (e.g., `insuremo-v3-ug-reinsurance.md` for reinsurance features).

**V3 File Mapping:** See `references/KB_USAGE_GUIDE.md` § V3 File → Module Mapping for the authoritative per-module V3 file list. Do not duplicate — reference instead.

**Semantic Override (Step 2C — for non-R10 items only):**
After ps-docs check, apply Semantic Override to non-R10 items only:

| Semantic Pattern Detected in Step 1 | Action |
|-------------------------------------|--------|
| Cross-system/policy (per life, cumulative, aggregate) | **Override** to **Dev Gap** |
| Third-party integration (custodian, reinsurer) | **Override** to **Dev Gap** |
| Dynamic calculation (MAX, MIN, tiered) | Verify config capability — may be Dev |
| Regulatory requirement (MAS, SFA) | Check references/InsureMO Knowledge/ps-underwriting.md → often Dev Gap |
| "maintain", "enforce" (ongoing validation) | Likely Dev Gap — requires monitoring logic |

**🎯 Key Principle:**
- ps-docs check + Limitations check → initial classification
- **R10 pre-scan** → pre-classifies cross-system items as Dev Gap
- **Semantic pattern override** → final classification for non-R10 items
- Even if ps-docs says "Supported", semantic complexity may make it a Dev Gap

**Two-Pass + Unknown-First + R10 + Semantic Classification Logic**:

| Step | Source | Finding | Semantic Override | Final Classification |
|------|--------|---------|-------------------|---------------------|
| 2A | R10 Keyword | Keyword found | — | → **Dev Gap** (pre-classified) |
| 2B | OOTB | ✅ Found | Check semantic | → Config/Dev/OOTB |
| 2B | OOTB | ❌ Not Found | Check semantic | → UNKNOWN/Dev |
| 2B | ps-docs | Explicitly Supported | Check semantic | → Config/Dev/OOTB |
| 2B | ps-docs | NOT Explicitly Supported | Check semantic | → UNKNOWN/Dev |
| 2B | Limitations | Has Code limitation | — | **Dev Gap** |
| 2B | Limitations | Has Config limitation | — | **Config Gap** |

**Semantic Override Examples (non-R10 items only):**
- ps-docs says "Supported" + spec says "per life (all policies)" → **Dev Gap** (not OOTB)
- ps-docs says "Supported" + spec says "custodian" → **Dev Gap** (not Config)
- ps-docs says "Supported" + spec says "MAX formula" → Verify, may be Dev

**R10 Override Examples:**
- "custodian" found + ps-customer-service.md confirms OOTB custodian integration + exact config path cited → override to **Config Gap**
- "per life" found + no KB proof of cross-policy support → **Dev Gap** stands

**Final Classification Rules (after Steps 2A + 2B + 2C):**

| Finding | Classification |
|---------|----------------|
| ps-docs explicitly states "Supported" + configurable | **Config Gap** |
| ps-docs explicitly states "Supported" + has Code limitation | **Dev Gap** (with Limitation Source) |
| ps-docs explicitly states "Supported" + no limitation | **OOTB** |
| ps-docs does NOT explicitly state support | **UNKNOWN** |
| OOTB says ✅ but ps-docs not explicitly supportive | **UNKNOWN** |
| OOTB says ✅ + ps-docs has Limitation | **Dev Gap** (ps-docs takes priority) |
| R10 keyword matched, no override proof | **Dev Gap** |
| R10 keyword matched, override conditions ALL met | **Config Gap or OOTB** (per override justification) |

**Execution:**

```
FOR each feature where ps-docs Classification is OOTB / Config / UNKNOWN:
  1. Read the corresponding V3 file(s) from the mapping above.
  2. Search for the feature/concept in the V3 file.
  3. Record the V3 finding as: V3-OOTB / V3-Config / V3-Dev / V3-UNKNOWN
  4. Apply the V3 Override Rules below.

FOR each feature where ps-docs Classification is Dev Gap:
  1. Read the corresponding V3 file(s) from the mapping above.
  2. Search for the feature/concept in the V3 file.
  3. Record the V3 finding as: V3-OOTB / V3-Config / V3-Dev / V3-UNKNOWN
  4. IF V3 Finding is V3-OOTB or V3-Config:
       → This means the KB limitation was misapplied or does not apply to this specific case
       → Apply the Dev Gap Downgrade Rules below (this is the ONLY case where Dev Gap can change)
     ELSE:
       → Dev Gap confirmed — V3 agrees or is also UNKNOWN
```

**V3 Override Rules — how V3 changes the final classification:**

| ps-docs Conclusion | V3 Finding | Final Classification | Action |
|-------------------|-----------|---------------------|--------|
| OOTB / Config | V3-OOTB | OOTB / Config | No change — V3 confirms ps-docs |
| OOTB | V3-Config | **Config** | Upgrade to Config. Cite V3 as evidence. |
| OOTB | **V3-Dev** | **Dev Gap** | Upgrade to Dev. V3 is decisive evidence that OOTB is insufficient. |
| Config | V3-Config | Config | No change — both agree |
| Config | **V3-Dev** | **Dev Gap** | Upgrade to Dev. V3 shows this is code-level, not configurable. |
| UNKNOWN | V3-OOTB | OOTB | Downgrade from UNKNOWN to OOTB — V3 resolves the unknown |
| UNKNOWN | V3-Config | **Config** | Downgrade from UNKNOWN to Config |
| UNKNOWN | **V3-Dev** | **Dev Gap** | Downgrade from UNKNOWN to Dev Gap |
| UNKNOWN | V3-UNKNOWN | UNKNOWN | Both KBs agree — research still required |
| **Dev Gap** | **V3-OOTB or V3-Config** | **Config or OOTB** | Dev Gap DOWNGRADED — V3 proves the KB limitation was misapplied for this specific case |
| **Dev Gap** | **V3-Dev** | **Dev Gap** | No change — V3 confirms Dev Gap |
| **Dev Gap** | **V3-UNKNOWN** | **Dev Gap** | No change — V3 cannot clarify; Dev Gap stands pending research |

**Rule: Dev Gap is treated as preliminary when V3 provides explicit contradictory evidence. The KB limitation cited may be context-specific (product type, market, or configuration scope) and may not apply to this specific case.**

#### KB Conflict Priority Rules

When ps-* and V3 UG provide **conflicting evidence** about the same feature, use this priority order:

**Priority 1 — ps-\* Limitation (HIGHEST AUTHORITY)**
> ps-\* module guides (ps-claims.md, ps-product-factory.md, etc.) are the **authoritative reference** for confirmed limitations.
> If ps-\* explicitly lists a behavior under **Limitations / Not Supported / Code Change Required** → this takes precedence over any V3 claim of OOTB/Config support.
> **Why:** V3 UG describes the standard implementation path; ps-\* Limitations capture real-world code constraints that may be product-specific, market-specific, or version-specific and not reflected in V3.
> **Exception:** If V3 proves the ps-\* Limitation was raised for a *different product/market/context*, note this in Gap Matrix notes and apply V3.

**Priority 2 — V3 UG**
> V3 User Guides are the **implementation reference** for standard behavior. They reflect what the current InsureMO version supports OOTB at the configuration level.
> Use V3 to:
> - Confirm or challenge a ps-\* UNKNOWN
> - Upgrade OOTB/Config to Dev Gap (V3 shows code-level)
> - Downgrade Dev Gap to Config/OOTB when V3 explicitly proves the limitation was misapplied for this specific context

**Priority 3 — OOTB (\*.md knowledge files)**
> The OOTB matrix (insuremo-ootb.md) is a **lightweight reference**. It can indicate general capability but is not authoritative for limitations.
> - OOTB says ✅ + ps-\* has limitation → **Dev Gap** (ps-\* takes priority)
> - OOTB says ✅ + ps-\* silent → OK to use as supporting evidence, not decisive

**Conflict Resolution Decision Tree:**

```
Does ps-* explicitly state a Limitation or Not Supported?
  YES → Dev Gap stands. V3 cannot override this.
  NO  → Check V3:
    Does V3 UG explicitly document this capability/config?
      YES → Use V3 finding (may upgrade or downgrade)
      NO  → Both KBs agree → UNKNOWN or per semantic override
```

**Documenting a KB Conflict:**
When a conflict is resolved, record it in Gap Matrix notes:
```
KB Conflict: ps-[module].md S.XX claims [X] but V3-ug-[yyy].md claims [Y]
Resolution: [ps-* wins / V3 wins] — reason
```

**V3 Cross-Reference Output — add to Gap Matrix notes:**
```
V3 Ref: [v3-ug-xxx.md]
V3 Finding: [V3-OOTB / V3-Config / V3-Dev / V3-UNKNOWN]
V3 Override Applied: [YES / NO]
V3 Evidence: [quote the specific V3 section or statement that led to the override]
```

**If V3 is not available for this module:**
- Set V3_Classification = `N/A`
- Proceed with ps-docs conclusion as final

---

#### Step 2B.6 — KB-Missing Degradation Strategy (CRITICAL — prevents section skipping)

> **Problem:** When a KB file (e.g., ps-reinsurance.md) is MISSING from the canonical set, the analysis traditionally skips that section entirely. This caused §3 Reinsurance to be missed in multiple projects.
>
> **Rule:** KB file absence ≠ section is irrelevant. Spec sections with concrete parameters must still be analyzed even if no KB file exists.

**Degradation Decision Tree:**
```
FOR each spec section §N that contains features:

  KB file for this module EXISTS?
    YES → Proceed with Step 2B normal lookup (KB Verified)
    NO  → Check spec parameters:

      Spec §N has CONCRETE PARAMETERS (values, formulas, thresholds)?
        YES → Analyze the spec directly. Classify based on semantic patterns.
              Set Config Path Source = "MISSING_KB — analyzed from spec"
              Do NOT skip. Do NOT mark as UNKNOWN just because KB is absent.
        NO  → Mark as UNKNOWN (requires client/vendor research)
              Set Config Path Source = "MISSING_KB + NO_SPEC_PARAMS"

      Spec §N has R10 keywords (reinsurer/quota share/custodian/per life)?
        YES → Automatically Dev Gap (cross-system)
              Config Path Source = "MISSING_KB — R10 triggered"
              Do NOT downgrade to UNKNOWN because KB is missing — R10 is definitive.
```

**KB-Missing Action Table:**

| KB Status | Spec Has Concrete Params? | R10 Keywords? | Action | Config Path Source |
|-----------|--------------------------|--------------|--------|-------------------|
| Missing | YES | YES | Dev Gap (R10 definitive) | `MISSING_KB — R10 triggered` |
| Missing | YES | NO | Analyze from spec → Config/Dev/UNKNOWN | `MISSING_KB — analyzed from spec` |
| Missing | NO | ANY | UNKNOWN | `MISSING_KB + NO_SPEC_PARAMS` |

**Concrete Parameters =** spec text contains actual values, formulas, or thresholds (e.g., "50% Quota Share", "USD 500,000 retained", "RGA Reinsurer"). NOT vague statements like "subject to treaty terms".

**Example — Reinsurance (§3 HSBC VUL Spec):**
```
KB file: ps-reinsurance.md → MISSING from canonical set
Spec §3 has: "Retention Limit: 50% Quota Share per life, max USD 500,000 retained"
R10 keywords: YES ("quota share", "reinsurer")

→ VUL_RI_001: Dev Gap (R10 triggered)
→ Config Path Source: "MISSING_KB — R10 triggered"
→ Note: "ps-reinsurance.md missing; parameters extracted from spec §3; RI treaty config is Dev enhancement"
→ UNKNOWN Register: "Confirm RGA treaty configuration details with client"
```

**Example — CS Section with no KB but vague spec:**
```
KB file: ps-customer-service.md → MISSING
Spec §7 has: "Customer can make alterations" (no specific parameters)

→ Analyze normally → No concrete params → UNKNOWN
→ Config Path Source: "MISSING_KB + NO_SPEC_PARAMS"
→ Note: "ps-customer-service.md missing; spec too vague for analysis"
```

**⚠️ Common Mistake to Avoid:**
> Do NOT downgrade a Dev Gap to "UNKNOWN" just because the KB is missing.
> R10 keywords are definitive: "quota share" + no KB = Dev Gap, not UNKNOWN.
> Only mark as UNKNOWN when: (a) no concrete spec parameters AND (b) no R10 keywords.

---

#### Step 2B.7 — R3 OOTB Overflow Test (MANDATORY — fires after ps-docs check)

> **Problem:** KB says a capability is "Supported" or "Configurable," but the client's specific variant exceeds what OOTB actually delivers. This is the most common source of hidden gaps — the label says Config, but the variant is actually Dev.

**Trigger:** Any feature where ps-docs classification is OOTB or Config Gap.

**Execution:**
```
FOR each feature where ps-docs = OOTB or Config Gap:
  Ask: Does the spec's variant EXCEED what KB says is supported?
    → If YES → Apply R3 overflow table below → Add to notes: "R3 OVERFLOW: [variant description]"
    → If NO → No overflow — proceed normally
```

**R3 Overflow Detection Table:**

| If ps-docs says... | But spec requires... | Then → |
|---|---|---|
| Standard COI rate table | Joint-Life Blended Rate formula | **Dev Gap** — R3 overflow |
| Policy Year counter | **Calendar Year** counter | **Dev Gap** — R3 overflow |
| Flat SA reduction | Partial excess reduction (e.g., "10% threshold") | **Dev Gap** — R3 overflow |
| Per-life rate | Cross-policy aggregate (e.g., "all policies per life") | **Dev Gap** — R3 overflow |
| Standard beneficiary | Trust / legal guardian / minor beneficiary | **Dev Gap** — R3 overflow |
| Per-transaction charge | Tiered threshold + waiver logic | **Dev Gap** — R3 overflow |
| Single currency | Multi-currency with conversion rules | **Dev Gap** — R3 overflow |
| Single LA | Joint-Life (last survivor) | **Dev Gap** — R3 overflow |
| End-of-day batch | **Intraday / real-time** settlement | **Dev Gap** — R3 overflow |

**R3 Output in Gap Matrix notes:**
```
R3 OVERFLOW: KB says [X] is supported but spec variant requires [Y] which exceeds
KB capability. Classification upgraded from Config to Dev Gap.
Overflow Type: [Variant type from table above]
```

---

#### Step 2B.8 — R4 Integration Record (MANDATORY for every third-party integration)

> **Problem:** Saying "custodian integration = Dev Gap" is insufficient. BSD writers and developers need to know the protocol, direction, trigger, and SLA.

**Trigger:** Any feature with R10 keyword: `custodian`, `asset manager`, `reinsurer`, `quota share`, `ceding`, `listed securities`, `exchange`.

**Integration Record Template (one per distinct endpoint):**
```
Integration : [Name]
Direction   : Outbound / Inbound / Bidirectional
Protocol    : REST / SOAP / SFTP / Kafka / MQ / Manual / [UNKNOWN]
Target      : [Specific system or party — e.g., RGA, custodian platform]
Trigger     : Real-time / Near-real-time / Daily batch / On-demand / [UNKNOWN]
Data Domain : Policy / Payment / Party / Finance / Claim / Channel / Reinsurance / Investment
Auth        : OAuth 2.0 / mTLS / API key / SSO / [UNKNOWN]
Effort      : Low / Medium / High / [UNKNOWN]
Source      : R4
```

**Execution:**
```
FOR each third-party integration identified:
  1. Attempt to determine each dimension from spec text
  2. If spec does not specify → mark as [UNKNOWN]
  3. Write one Integration Record per distinct endpoint
  4. Add to Gap Matrix notes as "R4 Integration Record" block
  5. If Effort = High → escalate to KB Completeness = Unverified
```

**Common Integration Patterns in VUL:**

| Integration | Direction | Protocol | Trigger | Effort |
|---|---|---|---|---|
| Custodian account opening | Bidirectional | UNKNOWN | NB inception | High |
| Asset Manager mandate | Outbound | UNKNOWN | Ongoing | High |
| RGA RI cession | Bidirectional | UNKNOWN | NB + events | High |
| Custodian fee feed | Inbound | UNKNOWN | Periodic | Medium |
| AM fee feed | Inbound | UNKNOWN | Periodic | Medium |
| In-kind asset transfer (payout) | Outbound | UNKNOWN | On-demand | High |
| Asset liquidation trigger | Outbound | UNKNOWN | Daily batch | High |

---

#### Step 2B.9 — R8 Batch/SLA Checklist (MANDATORY for monitoring/tracking/enforce patterns)

> **Problem:** "Maintain Min Liquidity Level" is marked as Dev Gap, but the real question is HOW the system enforces it — daily batch? real-time? Manual? R8 distinguishes these.

**Trigger:** Any feature with semantic keywords: `maintain`, `enforce`, `monitor`, `track`, `periodic`, `daily`, `ongoing`, `3 months`, `deadline`, `SLA`.

**R8 Batch/SLA Detection:**
```
FOR each Dev Gap with monitoring/enforce semantic:
  Ask: Is this a BATCH requirement, a REAL-TIME requirement, or a MANUAL/Process requirement?
    → If batch: Label as "R8 Batch" + specify frequency (daily, weekly, monthly)
    → If real-time: Label as "R8 Real-Time"
    → If manual/process: Label as "Process Gap" + route to Business Process Owner
```

**R8 Classification Output:**
```
R8 Batch/SLA: [YES-Batch / YES-RealTime / Process]
  Frequency: [daily / weekly / monthly / on-demand]
  Monitoring Logic: [DESCRIPTION]
  Source: R8
```

**R8 Batch Patterns in Insurance:**

| Pattern | Classification | Action |
|---|---|---|
| Daily PFV × 2% vs actual liquidity check | R8 Batch — Daily | Dev Gap (batch monitoring) |
| 3-month liquidation deadline tracking | R8 Batch — Periodic | Dev Gap (deadline monitoring) |
| RI rate change 90-day notice tracking | R8 Batch — Periodic | Dev Gap (notice period tracking) |
| Calendar year counter reset | R8 Batch — Annual | Dev Gap (counter management) |
| Commission clawback on free-look | R8 Batch — Event-driven | Dev Gap (clawback trigger) |
| Premium allocation EOD cutoff | R8 Batch — Daily | Dev Gap (cutoff enforcement) |

---

#### Step 2B.10 — R9 Config Complexity Marker (MANDATORY for all Config Gaps)

> **Problem:** "Config Gap" label is correct, but 1 product commission config vs 50 products is not the same effort. R9 adds complexity calibration.

**Trigger:** Any Config Gap.

**R9 Complexity Assessment:**
```
FOR each Config Gap:
  Determine scope/volume from spec:
    → Low:  1 product, standard types, single market
    → Medium: 3-10 products, mixed types, 2-3 markets
    → High:  20+ products, complex variants, multi-market
  Apply multiplier table below:

| Config Area | Low | Medium | High |
|---|---|---|---|
| Commission rules | Flat % by product | Tier-based by channel + product | Multi-level + clawback + contest |
| UW questionnaires | 1 standard template | 5-10 per category | 20+ with conditional branching |
| CS alteration rules | Standard items only | Market-specific restrictions | Per-product per-alteration |
| Tax / GL mapping | 1 market, standard tax | Multi-tax types | Cross-market + multi-currency |
| Holiday calendars | 1 market | 2-3 markets | 4+ markets with fund calendars |
```

**R9 Output in Gap Matrix notes:**
```
R9 Complexity: [Low / Medium / High]
  Rule combinations: [estimated number of rule permutations]
  Config items: [estimated number of config rows]
  Effort flag: [Normal / Escalate — High complexity may need dedicated sprint]
Source: R9
```

**If High complexity:** Append to notes: `"R9 HIGH COMPLEXITY — recommend dedicated estimation session with Config Lead"`

---

### §Config-vs-Dev Trade-off Gate (MANDATORY — fires after Step 2B.10, before Step 2C)

> **Problem from v3.0实战:** VUL_FEE_003 (Admin Fee on Total Premiums) was classified as Dev Gap, but it might have been achievable via Config if the cumulative base had been investigated. Similarly, 22 Dev Gaps vs 15 Config Gaps is heavily Dev-skewed — some Config Gaps may have been incorrectly elevated to Dev.

**Every Dev Gap MUST pass this gate before being finalized.**

**Config-vs-Dev Trade-off Assessment:**
```
FOR each item classified as Dev Gap in Step 2B:
  Ask: Could this be implemented as a Config change in InsureMO Product Factory?
    → IF YES: Document WHY it was classified Dev Gap instead:
         a) InsureMO PF does not support this parameter type (cite ps-product-factory.md limitation)
         b) Client Override = YES explicitly refuses Config approach (cite confirmation channel + date)
         c) Cross-system data required (R10-positive — by definition Dev Gap)
    → IF NO: Document the Dev Gap justification

  Ask: Could this be OOTB with a config change?
    → IF YES: Upgrade from Dev Gap to Config Gap; document KB path
    → IF NO: Confirm Dev Gap
```

**Config-vs-Dev Justification Register (output of this gate):**
```
## Config-vs-Dev Trade-off Gate Results

| Gap ID | Initial Class | Final Class | Justification |
|--------|-------------|------------|---------------|
| VUL_FEE_003 | Dev Gap | **Dev Gap CONFIRMED** | R10 aggregate (Total Premiums cumulative base) — by definition requires global counter. Cannot be Config. |
| VUL_COV_003 | Dev Gap | **Dev Gap CONFIRMED** | R10 per life (USD 2M cap across all HSBC policies) — cross-policy by definition. Cannot be Config. |
| VUL_GEN_002 | Dev Gap | **Dev Gap CONFIRMED** | AI vs Non-AI asset segregation — InsureMO supports via Client Risk Profile. Reclassified to **Config Gap**. KB: ps-product-factory-limo-product-config.md §Allowed Investment.
| ... | ... | ... | ... |

Summary:
  Dev Gap confirmed: X items (R10-positive by definition)
  Elevated to Config Gap: Y items (KB path found after trade-off review)
  Dev Gap downgraded to UNKNOWN: Z items (insufficient KB to determine)
```

**⚠️ Gate Rule:** If an item is marked Dev Gap WITHOUT a documented justification in this register, it MUST be re-reviewed. A Dev Gap without justification is a quality defect.

**When to override to Config Gap:**
- If InsureMO has a confirmed KB path (cite ps-*.md section + field name)
- If the parameter type is supported (string/int/enum/date — not requiring custom code)
- If the parameter is per-policy (not per-life / not aggregate / not cross-system)

---

#### Step 2C — R1 Non-Functional Requirements (NFR) Detection

> **Problem:** All analysis so far focuses on functional gaps. But performance SLAs, batch windows, data residency, and security requirements are equally critical and often missed.

**Trigger:** Run against every spec section.

**R1 NFR Checklist:**

| NFR Dimension | Detection Question | If YES → |
|---|---|---|
| Performance / SLA | "within [N] Business Days" / "within [N] hours" | Add `🚫 NFR — Performance` entry |
| Scalability | Concurrent users, peak load mentioned | Add `🚫 NFR — Scalability` entry |
| Availability / SLA | Uptime requirement, RTO/RPO mentioned | Add `🚫 NFR — Availability` entry |
| Data Residency | "data must stay in [country]" | Add `🚫 NFR — Data Residency` entry |
| Security | Specific encryption standard named | Add `🚫 NFR — Security` entry |
| Disaster Recovery | RPO/RTO mentioned | Add `🚫 NFR — DR` entry |
| Audit / Retention | Log retention period (e.g., 7 years) | Add `🚫 NFR — Audit Retention` entry |

**Execution:**
```
FOR each spec section:
  Scan for NFR keywords: "Business Days", "hours", "SLA", "uptime", "concurrent",
    " residency", "encryption", "RPO", "RTO", "retention", "audit"
  IF found:
    → Create separate NFR entry in Gap Matrix
    → Tag: 🚫 NFR — [Dimension]
    → Target: [System/Process affected]
    → Default effort: Medium (unless platform re-architecture implied)
    → NOT a Dev Gap — NFR entries go to separate NFR Appendix
```

**R1 Output Format (separate NFR Appendix):**
```
## NFR Appendix

| NFR ID | Dimension | Requirement | Spec Ref | Target System | Effort |
|--------|-----------|------------|----------|--------------|--------|
| NFR-01 | Performance | Payout instruction within 10 Business Days | §2, p.7 | Claims/Payout | Medium |
| NFR-02 | Performance | 3-month liquidation deadline tracking | §5, p.13 | Custodian/FA | Medium |
```

---

#### Step 2D — R7 UI/UX Dimension Detection

> **Problem:** "Custodian integration = Dev Gap" ignores the UI dimension. A self-managed fund vs a discretionary mandate have completely different user interfaces.

**Trigger:** Any feature involving user interaction, workflow, or multi-party process.

**R7 UI/UX Detection:**
```
FOR each Dev Gap that involves user-facing behavior:
  Ask: Does this require a DIFFERENT UI from OOTB?
    → If YES → Add R7 UI/UX section to Solution Design
    → Specify: Screen/flow, user roles, interaction pattern
```

**R7 Common Patterns:**

| Pattern | UI Implication | Action |
|---|---|---|
| Self-managed vs Discretionary AM | Two distinct UI flows for investment decision | R7 UI gap |
| In-kind payout selection | Beneficiary UI for asset vs cash choice | R7 UI gap |
| Joint-Life TI claim | Two-party claim submission flow | R7 UI gap |
| Non-AI fund restriction alert | Warning/block UI at allocation | R7 UI gap |
| AI status self-declaration | Declaration form + verification flow | R7 UI gap |
| Min Liquidity breach notification | Alert UI to policyholder | R7 UI gap |

**R7 Output in Solution Design:**
```
## R7 UI/UX Dimension
UI Flow: [Self-managed / Discretionary Mandate / Multi-party / Alert & Notification]
Screens Affected: [List screens that need new/modified UI]
User Roles: [Policyholder / CS / Claims / AM / Custodian]
Interaction Pattern: [Real-time / Asynchronous / Batch notification]
Source: R7
```

---

#### Step 2E — R2 Blind Spot Detection (MANDATORY — fills the completeness gap)

> **Problem:** R2 is defined as "Every functional requirement has a matching KB row or is flagged as a blind spot," but without an explicit execution step, it is unclear how to verify this. R2 lives in the Gap Matrix's KB Reference column — every row must pass this check.

**Trigger:** Run after all features have been classified (Step 2A → 2B → 2D complete).

**R2 Blind Spot Detection:**
```
FOR each Gap Matrix row (feature):
  IF Current Behavior column has a KB citation (ps-*.md section):
    → R2 PASS: Gap has KB coverage
  IF Current Behavior column says "NOT FOUND in ps-*" or is blank:
    → R2 FAIL: This is a Blind Spot
    → Mark Gap Matrix column: R2 = YES
    → Set Status = BLOCKED (cannot proceed without KB coverage)
    → Add to Open Questions: "KB gap — requires [specific ps-*.md section] update or manual verification"
```

**R2 Output — what to check in each Gap Matrix row:**
```
| Column | What to Verify |
|--------|---------------|
| Current Behavior | Has a ps-*.md KB citation — or "NOT FOUND in ps-*" if truly undocumented |
| Structured Requirement | Has a clear variable/field name + operator — or marked as UNKNOWN |
| R10 | YES → Dev Gap confirmed (no KB coverage gap possible — Dev Gap by definition) |
| V3 | Has V3-OOTB / V3-Config / V3-UNKNOWN / N/A — or Blind Spot if both KBs missing |
```

**R2 Summary (add to Gap Matrix notes):**
```
R2 Blind Spot Summary:
  R2 PASS (KB coverage confirmed): X items
  R2 FAIL (Blind Spot — NOT FOUND in ps-* AND NOT FOUND in V3): X items
    → All R2 FAIL items marked as BLOCKED pending KB verification
    → Each R2 FAIL entered in unknown-register.md with Owner + SLA
```

---

### §UNKNOWN Auto-Tracker (MANDATORY — fires after Step 2E)
> **Problem from v3.0实战:** UNKNOWNs were found (COI rate table, CPFIS eligibility, TI fee deduction ambiguity) but Owner + SLA were filled in manually — prone to omission and inconsistency.
> **Step 2E UNKNOWN Auto-Tracker** automatically generates the Open Questions register from UNKNOWN-gap items.**UNKNOWN Auto-Tracker:**
```
FOR each Gap Matrix row with Status = BLOCKED or Classification = UNKNOWN:
  Generate Open Question entry automatically:

  OQ-{YY}-{NNN}: [Short description from Gap Matrix Feature column]
  Gap ID:           {Gap ID from Gap Matrix}
  Source:            {Spec §N, p.#}
  Question:         {Structured Requirement column or the ambiguity itself}
  Impact:           {Priority — P1 blocks UAT / P2 scheduled / P3 backlog}
  Blocking:         {What cannot proceed without this answer}
  Suggested Owner:  {Pre-filled by type — see Auto-Owner table below}
  Suggested SLA:   {Pre-filled by type — see SLA table below}
  Auto-generated:  TRUE
```

**Auto-Owner Lookup Table:**
```
| UNKNOWN Type                  | Auto Suggested Owner           | Rationale                           |
|-----------------------------|-----------------------------|-------------------------------------|
| COI rate / pricing table     | Actuarial / Pricing Team     | Rate table ownership                 |
| CPFIS / MAS compliance       | Compliance / Legal           | MAS regulatory question              |
| Product parameter (e.g., min premium, max SA) | Product Manager     | Parameter definition                  |
| TI benefit definition / prognosis | Underwriting / Legal      | Medical/legal definition              |
| Distribution channel / commission | Sales / Distribution     | Channel-specific rule                 |
| Reinsurance rate / structure | RI Manager / Actuarial       | RI pricing ownership                  |
| UI/UX flow                  | Product Manager / UX          | Product experience decision           |
| Legacy/transition parameter  | IT/Dev / Business Analyst    | Technical implementation decision     |
| General / other              | Business Analyst              | Fallback                            |
```

**Auto-SLA Lookup Table:**
```
| UNKNOWN Impact Level    | Auto SLA           | Rationale                           |
|----------------------|-------------------|-------------------------------------|
| P1 (blocks UAT)     | 3 business days   | Must resolve before UAT starts       |
| P2 (scheduled)      | 2 weeks          | Before development starts            |
| P3 (backlog)        | 4 weeks          | Before client sign-off              |
```

**Auto-Generated Open Questions Register:**
```
## Unknown Register — Auto-Generated by Step 2E UNKNOWN Auto-Tracker

| OQ-ID | Gap ID | Suggested Owner | Suggested SLA | Impact | Question Summary |
|-------|--------|---------------|--------------|--------|-----------------|
| OQ-26-001 | VUL_COV_003 | Actuarial / Pricing | 3 business days | P1 | COI rate table — Finalised COI.xlsx not in spec |
| OQ-26-002 | VUL_COV_004 | Compliance / Legal | 3 business days | P1 | CPFIS eligibility not stated anywhere in spec |
| OQ-26-003 | VUL_PREM_004 | Product Manager | 2 weeks | P2 | Temp min IP USD 3M (Aug 2023) — revert date? |
| OQ-26-004 | VUL_COV_005 | Underwriting / Legal | 2 weeks | P2 | TI Benefit "less applicable Fees" — fees from TI payout or PFV? |

**Note:** All entries are auto-generated. Adjust Owner/SLA if client confirms a different owner.
```

---


### ⚠️ CRITICAL: Do NOT Invent Config Paths

> Solution / Config Path must come from the knowledge base, not from the BA's imagination.

```
RULE: If you did not find the config path in ps-product-factory.md (or relevant ps-*.md),
      you MUST leave Solution / Config Path BLANK and set Config Path Source = "Assumed".

DO NOT write a config path that "sounds reasonable" — e.g.:

  WRONG:  "Product Factory → Premium Rules → Min Initial Premium"    ← invented
  RIGHT:  [leave blank]                                           ← not verified

WHY: A fake config path is worse than no path — it gives false confidence.
     The actual config location must be verified by Agent 6 (Configurator) during implementation.

WHEN IN DOUBT: Leave it blank. Mark as "Assumed". Let Agent 6 find the real path.
```

**Config Path Source Values:**

| Value | Meaning |
|-------|---------|
| `KB Verified` | Config path was found and confirmed in ps-product-factory.md |
| `Assumed` | BA made an educated guess — must be verified by Agent 6 before use |
| `Dev` | This is a Dev Gap — not a Config Gap; no config path exists |
| `R10 Override` | Was Dev Gap per R10, overridden to Config Gap with cited KB proof |
| `N/A` | OOTB — no solution required |

---

**Limitation Source Tracking:**
Always record source for Dev Gaps:
- `references/InsureMO Knowledge/ps-customer-service.md → Limitations`
- `references/InsureMO Knowledge/ps-product-factory.md → Limitations`
- `ps-*.md → Limitations`
- `UNKNOWN` (not found in any KB)

**Note:** This two-pass + Unknown-First approach ensures no gaps are missed. OOTB is the index, ps-docs are the source of truth.

### Step 3 — Downstream Impact Assessment (v2.0 — Extended to All 12 Modules)

Every gap item must be assessed for impact on all **12 InsureMO modules** (not just 7):

| Module | Code | What to Check |
|--------|------|--------------|
| Product Factory | PF | Coverage rules, premium rules, rate tables, benefit formulas |
| New Business | NB | NB screen fields, validation, auto-calculation triggers |
| Underwriting | UW | UW referral rules, acceptance criteria, loading rules |
| Customer Service | CS | Endorsement fields, field state changes (editable→read-only) |
| Claims | CLM | Benefit eligibility, calculation, payment disbursement |
| Billing & Collection | BCP | Premium schedule, grace period, lapse trigger |
| Reinsurance | RI | Cession rules, treaty triggers, RI premium |
| Fund Administration | FA | NAV, fund switch, surrender value, charges |
| Party Management | PM | Party roles, KYC fields, deduplication |
| Sales Channel | SC | Commission structure, agent portal visibility |
| Document Generation | DG | Policy contract, benefit illustration, notices |
| Global Query & Reporting | GQ | Report fields, in-force/lapsed queries |

**Impact classification:**
```
🔴 Direct  = module requires code or configuration change
🟡 Indirect = module behaviour changes but no code change — regression testing required
⚪ None    = no impact — state the reason explicitly (do not leave blank)
```

**Cross-market note:** If the product spans multiple markets (SG/HK/MY), each market's variant of the same module must be assessed separately. Document market-specific differences in the Impact column.

**Ripple note (for Agent 7 handoff):** Flag any 🔴 Direct impact chain where Module A → Module B → Module C (3+ hops) — these feed into Agent 7's Ripple Propagation Map. Mark as: `⚡ RIPPLE CHAIN: A → B → C`

### Step 4 — Priority Rating
Apply the Gap Severity Reference table above. Document which criterion drove the priority assignment.
```
High   = Blocks core business flow OR regulatory requirement (Critical or High severity)
Medium = Affects UX or efficiency, workaround exists (Medium severity)
Low    = Nice to have, deferrable (Low severity) → mark as Backlog
```

### Step 5 — Dependency Mapping
For each Dev Gap and Config Gap, identify:
- Which other gaps must be completed first (prerequisite gaps)
- Which downstream gaps are unblocked by this gap (dependent gaps)
- Recommended implementation sequence based on dependency chain

Document as: `F001 → F003 → F007` (F001 must be done before F003, which must be done before F007)
If a gap has no dependencies, explicitly state: "No dependencies identified."

---

## Output: Gap Matrix

```markdown
# Gap Matrix — [Product Name]
Version: 1.0 | Date: YYYY-MM-DD | Source Document: [filename]
Analysis Method: Agent 1 with Two-Pass + Unknown-First + R10 Verification

## Summary

| Classification | Count | High | Medium | Low |
|---------------|-------|------|--------|-----|
| OOTB          | X     | —    | —      | —   |
| Config Gap    | X     | X    | X      | X   |
| Dev Gap       | X     | X    | X      | X   |
| UNKNOWN       | X     | X    | X      | X   |
| Process Gap   | X     | —    | X      | X   |
| **Total**     | **X** | **X**| **X**  | **X**|

**V3 Cross-Reference Summary:**
- V3 Used (available and consulted): X items
- V3 Override (changed ps-* conclusion): X items
- V3 Confirmed (agreed with ps-*): X items
- V3 N/A (no V3 file for module): X items

## Gap Matrix — Role-Based Views

### How to Read This Section

The Gap Matrix has **two views**:

| View | Audience | Content |
|------|----------|---------|
| **Gap Matrix (Full)** | Dev, Config Lead, BA | All 11 columns including Original Spec Text, Current Behavior, KB refs |
| **Gap Matrix (Lite)** | Reviewer, Project Manager, Client | 4 columns: Gap ID / Feature / Final / Priority — for scope review and status tracking |
| **Gap Matrix (Dev-Specific)** | Developer | Same as Full but filtered to Dev Gaps only — includes Solution Design cross-refs |

### Gap Matrix (Lite) — For Reviewers and Project Managers

| Gap ID | Feature | Final Classification | Priority | Status |
|--------|---------|---------------------|----------|--------|
| G001 | [Feature Name] | Config Gap | P1 | Open |
| G002 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

**Lite Summary:**
```
OOTB:           X items     → No action required
Config Gap:     X items     → Agent 6 (Configurator)
Dev Gap:        X items     → Agent 2 (BSD Writer) — X BSDs required
UNKNOWN:        X items     → Client/Research — blocking X items
Process Gap:    X items     → Business Process Owner

Total: X items
P1 (blocks UAT): X items — ALL must be resolved before test
P2 (scheduled):  X items
P3 (backlog):     X items — deferred to phase 2
```

---

## Gap Matrix (Full)

| Gap ID | Feature | Spec Ref | Original Spec Text | Structured Requirement | Current Behavior (InsureMO as-is + KB Ref) | R10 | ps-\* | V3 | Final | Priority | R3 | R4 | R6 | R7 | R8 | R9 | BSD? | Compliance | Status | Confidence | Open Qs |
|--------|---------|----------|-------------------|-----------------------|---------------------------------------------|-----|-------|----|-------|----------|----|----|----|----|----|----|-----|------------|--------|------------|----------|
| G001 | [Feature Name] | §[Section], p.[#] | "[EXACT quote from spec — copy verbatim, include all conditions/thresholds]" | [Req: = / ≥ / ≤ / MIN / MAX / IF…THEN…] | [What InsureMO currently does — cite ps-*.md + "no change"; OR "NOT FOUND in ps-*" if undocumented; OR "[ps-X.md S.XX] explicitly states limitation"] | YES / NO | OOTB / Config / Dev / UNKNOWN | YES / NO / N/A | [Final] | P1 / P2 / P3 | YES / NO | YES / NO | YES / NO | YES / NO | Batch / RT / Manual / N/A | L / M / H / N/A | YES / NO / N/A | YES / NO | READY / BLOCKED | H / M / L | N |
| G002 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Column Notes:**
- **Spec Ref**: §[Section Name] — [Sub-clause], p.[PageNumber]
- **Original Spec Text**: COPY VERBATIM from spec — include ALL conditions, thresholds, exceptions. Do NOT paraphrase. If multiple conditions, list each separately with bullet points.
- **Structured Requirement**: Variable=Currency / Age=N ANB / IF…THEN… / MIN/MAX operators. One row per distinct rule/condition.
- **Current Behavior**: Cite ps-*.md section + "no change" if OOTB confirmed. Cite limitation source if Dev Gap. Use "NOT FOUND in ps-*" if KB gap. Be specific about what the system does today.
- **R10**: YES if cross-policy/cumulative/third-party/aggregate keywords detected
- **ps-\***: OOTB / Config / Dev / UNKNOWN per ps-*.md KB
- **V3**: YES if V3 cross-reference changed conclusion / NO if V3 confirmed / N/A if no V3 file
- **Final**: Final classification after R10 + ps-* + V3 consideration
- **Priority**: P1=High(blocks UAT), P2=Medium(scheduled), P3=Low(backlog)
- **R3**: YES if OOTB/config item exceeds KB capability (spec variant overflow)
- **R4**: YES if third-party integration (custodian/AM/reinsurer/exchange)
- **R6**: YES if MAS/SFA/BNM/OJK/OIC/IA regulatory requirement → trigger Agent 3
- **R7**: YES if user-facing UI flow different from OOTB
- **R8**: Batch / RT (Real-Time) / Manual / N/A — monitoring/enforce patterns only
- **R9**: L (Low) / M (Medium) / H (High) / N/A — Config Gaps only; Dev Gaps use N/A
- **BSD?**: YES for all Dev Gaps; NO for Config/OOTB/Process; N/A for UNKNOWN
- **Compliance**: YES if regulatory/compliance check required → trigger Agent 3
- **Status**: READY if Open Questions resolved; BLOCKED if pending client confirmation
**Confidence**: H (High) if KB has explicit section citation and no ambiguity in raw text; M (Medium) if KB has related section but raw text has conditional language ("may"/"unless"/"subject to"); L (Low) if no KB citation and classification is inference-based. Confidence affects how much detail required in the Solution Design template.
- **Open Qs**: Number of blocking Open Question items (e.g., "2 items")

**Column Conventions:**

**Spec Section format:**
§[Section Name] — [Sub-clause Name], p.[PageNumber]
Examples:
  §4. Premium — MINIMUM PREMIUM, p.2
  §5. Coverage — Death Benefit, p.5
  §8. Fees and Charges — Policy Fee, p.8
  §6. Underwriting — Joint-Life, p.8
  §7. Policy Servicing — Free-Look Period, p.7

**Structured Requirement format:**
- Variable/field names in CamelCase
- Use = / >= / <= / MIN / MAX / IF...THEN... operators
- Currency amounts: USD XXX,XXX
- Percentages: X.X%
- Age: N ANB or N Age Last Birthday
- No full sentences — concise declarative statements

Examples:
  MinInitialPremium = USD 200,000
  MinPartialWithdrawal = USD 10,000
  FreeLoyaltyBenefit = IF YearsInForce >= 10 THEN 1.0% x TotalPremiumsPaid
  SAR = MAX(SumAssured - Withdrawals_L12M - PFV, PFV)
  TI_Benefit_Cap = MIN(USD 2,000,000, SAR)

**Gap ID Naming Convention:**
```
{ProductPrefix}_{CategoryPrefix}_{NNN}
  ProductPrefix:  VUL / TERM / END / HL / CI / etc.
  CategoryPrefix: PREM / FEE / BEN / PS / UW / INV / COM / REG / etc.
  NNN:            Sequential number starting at 001

Examples:
  VUL_PREM_001   (VUL product, Premium feature)
  TERM_BEN_003   (TERM product, Benefit feature)
  END_FEE_012    (Endowment product, Fee feature)
  VUL_PS_007     (VUL product, Policy Servicing feature)
  VUL_UW_002     (VUL product, Underwriting feature)
  VUL_INV_001    (VUL product, Investment feature)
  VUL_COM_003    (VUL product, Commission feature)
```
```

**Classification Values:**
| Value | Meaning | Action |
|-------|---------|--------|
| `OOTB` | Explicitly supported in ps-docs + no limitation | None required |
| `Config Gap` | Explicitly supported in ps-docs + configurable | Configuration |
| `Dev Gap` | Explicitly supported in ps-docs + Code limitation OR Knowledge gap | Development |
| `UNKNOWN` | NOT explicitly supported in ps-docs | Requires research |
| `Process Gap` | Business process issue, not system | Process change |

**Functional Existence Check:**
| Value | Meaning |
|-------|---------|
| ✅ Explicitly Supported | ps-docs clearly states feature is supported |
| ⚠️ NOT Explicitly Supported | ps-docs does NOT clearly state support → default to UNKNOWN |
| ❌ NOT FOUND | Feature not found in any ps-doc → UNKNOWN |

**Limitation Source Values:**
| Source | Meaning |
|--------|---------|
| (blank) | No limitation - standard OOTB or Config |
| `references/InsureMO Knowledge/ps-customer-service.md → Limitations` | Code-level limitation in CS module |
| `references/InsureMO Knowledge/ps-product-factory.md → Limitations` | Code-level limitation in configuration layer |
| `references/InsureMO Knowledge/ps-underwriting.md → Limitations` | Code-level limitation in UW module |
| `references/InsureMO Knowledge/ps-billing-collection-payment.md → Limitations` | Code-level limitation in Billing module |
| `UNKNOWN` | Not found in any knowledge base - requires research |

**Summary (required on every output):**
```
✅ OOTB:           X items
⚙️ Config Gap:     X items
🔧 Dev Gap:        X items (with Limitation Source identified)
  → R10-detected (cross-system/third-party): X items
  → R3 Overflow (variant exceeds KB capability): X items
  → Semantic Override (non-R10): X items
❓ UNKNOWN:        X items (requires research)
📋 Process Gap:    X items
🚫 NFR Gap:        X items (see NFR Appendix)
Total:             X items

High Priority:     X items
Medium Priority:   X items
Low Priority:     X items (→ Backlog)

V3 Cross-Reference Summary:
  → V3 Used: X items (features where V3 was available and consulted)
  → V3 Override (V3 changed ps-* conclusion): X items
    → ps-* OOTB upgraded to Config (V3): X
    → ps-* OOTB upgraded to Dev Gap (V3): X
    → ps-* Config upgraded to Dev Gap (V3): X
    → ps-* UNKNOWN resolved by V3: X
    → Dev Gap DOWNGRADED to Config/OOTB (V3): X
  → V3 Confirmed (V3 agreed with ps-*): X items
  → V3 N/A (no V3 file for this module): X items

R1-R9 Compliance Summary:
  → R1 NFR items: X
  → R2 Blind Spots: X
  → R3 Overflows: X (of which: X upgraded to Dev Gap, X confirmed Config)
  → R4 Integration Records: X
  → R5 Migration: N/A or X items
  → R6 Regulatory (Agent 3 triggered): X items
  → R7 UI/UX Dimensions: X
  → R8 Batch/SLA items: X (of which: X Batch, X Real-Time, X Manual)
  → R9 High Complexity Config: X

**Gap ID format: {ProductPrefix}_{CategoryPrefix}_{NNN}**
  e.g. VUL_PREM_001, VUL_BEN_004, VUL_PS_007
```

**Config Path Source Breakdown (for Config Gaps only):**
```
Config Gap Count:  X items
  KB Verified:     X items  ← config path confirmed in ps-product-factory.md
  R10 Override:    X items  ← was Dev Gap per R10, overridden with cited KB proof
  Assumed:         X items  ← BA guess — must be verified by Agent 6 before use
```

**⚠️ UNKNOWN Handling:**
- All UNKNOWN items must be documented in `unknown-register.md`
- Each UNKNOWN must have an owner assigned for research
- UNKNOWN does not mean "no gap" — it means "not yet verified"
- Per C14: All OPEN UNKNOWNs must be linked in `references/delivery-traceability.md`

---

## Agent 5 UNKNOWN Type Integration (v2.0)

When Agent 1 receives input from Agent 5 (Product Profile, `INPUT_TYPE = PRODUCT_PROFILE`), Agent 5's UNKNOWN Register uses a 3-way Type classification. Agent 1 must handle each type appropriately:

### Agent 5 → Agent 1 UNKNOWN Flow

| Agent 5 UNKNOWN Type | Agent 1 Action |
|----------------------|---------------|
| **NOT_STATED** | Treat as a requirement ambiguity — proceed with gap classification using industry standard assumption if available. Log in Agent 1's UNKNOWN Register as `OPEN`. If assumption is used in classification, note the assumption explicitly in Gap Matrix notes. |
| **MISSING_ATTACHMENT** | Agent 5 should have blocked the handoff. If received, do NOT proceed with gap analysis for features depending on this attachment. Escalate: "MISSING_ATTACHMENT [ID] must be obtained before Agent 1 gap analysis can proceed." |
| **NOT_FOUND** | Agent 5 could not locate a spec section that was referenced. Before proceeding, verify the spec section exists. If truly missing, treat as NOT_STATED and note "Spec section not found — treated as NOT_STATED". |

### Conversion to Agent 1 UNKNOWN Register

```
For each Agent 5 UNKNOWN in the Product Profile UNKNOWN Register:

  IF Agent 5 Type = NOT_STATED:
    → Create Agent 1 UNKNOWN entry
    → Status: OPEN
    → Category: PRODUCT_BEHAVIOR
    → Investigation: "Confirmed missing from spec by Agent 5; treated as requirement gap"

  IF Agent 5 Type = MISSING_ATTACHMENT:
    → DO NOT create Agent 1 UNKNOWN yet
    → Status: BLOCKED
    → Note: "Awaiting [attachment name] — blocks Agent 1"
    → Route back to client/BA for resolution

  IF Agent 5 Type = NOT_FOUND:
    → Create Agent 1 UNKNOWN entry
    → Status: OPEN
    → Category: PRODUCT_BEHAVIOR
    → Investigation: "Spec section referenced but not found — verify spec completeness"
```

### Agent 5 Pattern Flags (from Product Profile Summary)

Agent 5's Step 5 Product Profile Summary includes Pattern Flags that Agent 1 must incorporate into gap classification:

```
□ Cross-policy lookup required         → All such features → Dev Gap
□ Global counter required              → All such features → Dev Gap
□ Custodian/AM integration required   → All such features → Dev Gap
□ Reinsurance system integration       → All such features → Dev Gap
□ Vesting logic required               → Verify if configurable → Dev/Config
□ CI survival period tracking          → Verify in ps-* → Config/OOTB
□ UL allocation/switching config      → Check ps-product-factory.md → Config/OOTB
□ Endowment bonus declaration batch   → Verify → Dev/Config
```

---

**Optional detailed tables** (if applicable):
- Dev Gap Details with effort estimates
- Config Gap Details with config paths
- Priority distribution by category

---

## Dev Gap Solution Design Template (v3.2)

> **Every Dev Gap MUST have a completed Solution Design Template.** This feeds directly into Agent 2's BSD writing.
> Config Gaps do NOT need this template — they go straight to Agent 6.

> **HARD RULE: Dev Gap SD 100% Coverage Requirement**
> The Gap Matrix is NOT complete until EVERY Dev Gap has a filled Solution Design Template.
> If the analysis session ends with any Dev Gap lacking an SD, the analysis is **INCOMPLETE** — not partially complete.
> Sub-agents MUST prioritize writing SDs for HIGH/PRIORITY Dev Gaps first if token/time is constrained.
> Agent 2 (BSD Writer) CANNOT begin until all Dev Gap SDs are confirmed complete. — they go straight to Agent 6.

**KB Constraint Principles:**
```
All sections must be based on OOTB behavior from ps-*.md
→ If ps-*.md does not document this behavior → mark as "OOTB behavior undocumented — pending confirmation"
→ Do NOT invent business behavior or assumptions: "assume the current behavior is..."
→ Every statement must include a KB citation (format: ps-{module}.md Section N)
→ reg-*.md, v3-ug-*.md, or other KBs are NOT accepted as OOTB behavior citations
→ If regulatory citation is needed → use Agent 3, do not claim it in Solution Design
```

```markdown
## Dev Gap Solution Design — [Gap ID]: [Feature Name]

> ⚠️ **Identify existing mechanism BEFORE deciding Change Type**
>
> Common InsureMO standard mechanisms (verify against KB first):
> - `Rider_Term` → auto-populated from PF Term Limit Table (§IX.3), no new formula needed
> - `Rider_SA` → auto-populated from PF Product Liability Table, no new formula needed
> - `Premium` → auto-calculated from PF Ratetable Setup, no new formula needed
> - `Surrender Value` → auto-calculated by InsureMO formula, see ps-fund-administration.md
>
> If identified Existing Mechanism = "None" (InsureMO truly lacks this field) → Change Type = NEW formula
> If identified Existing Mechanism ≠ "None" → Change Type should be: MODIFY / READ-ONLY enforce / NEW cap+constraint
> **Prohibited:** writing a new calculation formula when an Existing Mechanism is already identified (= Q05 FAIL)

### Change Point
| Field | Value | KB Ref |
|-------|-------|---------|
| Screen / CS Item | [EXACT screen name from ps-*.md] | ps-*.md Section N |
| Section | [Section within screen] | ps-*.md Section N |
| Field / Element | [Exact field name being changed] | ps-*.md Section N |
| Change Type | [NEW / MODIFY / DELETE / CALCULATION / WORKFLOW] | — |
| Trigger | [When does this change fire?] | ps-*.md Section N |

### Current vs Required Behaviour

**Current Behaviour** (InsureMO as-is):
> [What the system does today — cite ps-* section + line]
> Source: ps-fund-administration.md Section 243
> ⚠️ KB Constraint: if KB does not document this behavior, mark as "OOTB behavior undocumented"

**Required Behaviour** (per client spec):
> [What the client needs — structured as: Variable = formula / condition / value]
> Source: §5.3 Surrender Value, p.12

**Delta Summary:**
| Element | Current (KB Ref) | Required | Change |
|---------|------------------|---------|--------|
| Formula | [cite ps-*.md] | [new formula] | [Changed/New] |
| Floor | [cite ps-*.md or "None"] | [value] | [New/Changed] |
| Rounding | [cite ps-*.md] | [value] | [No change/Changed] |

### Business Scenario Matrix (replaces former Boundary Conditions)

> Based on KB policy state definitions and business scenarios, verify the new rule's behavior across different scenarios

**KB Constraint:** All scenario definitions must cite ps-customer-service.md policy state definitions (no other KB references accepted)

```
| Scenario ID | Policy State Precondition | New Rule Behavior | KB Ref |
|-------------|--------------------------|-------------------|---------|
| SV-01: Normal Surrender | In-force, No Loan | New rule calculates: floor = 80%×Premiums | ps-customer-service.md S.15 |
| SV-02: Surrender with Loan | In-force, Loan Outstanding | [Pending confirmation: Is surrender allowed?] | ps-loan-deposit.md S.5 — not documented |
| SV-03: Surrender Lapsed Policy | Lapsed | [Pending confirmation: Is surrender allowed in lapsed state?] | ps-customer-service.md — state not defined |
| SV-04: Surrender within Free-Look | In-force, Free-Look Period | 100% NAV + waived charge | ps-customer-service.md S.12 |
| SV-05: Surrender after Reinstatement | Reinstated | [Pending confirmation: Does new rule apply after reinstatement?] | ps-customer-service.md — not documented |
```

**Scenario Naming Rule:** `{Function}_{Sequence}_{BriefDescription}`

⚠️ If a business scenario is not documented in KB → mark as "Pending confirmation" and include in Open Questions

### Policy State Constraints (NEW)

> Documents which policy states allow or prohibit the new rule from triggering

**KB Constraint:** Policy state definitions must cite ps-customer-service.md (no other KB references accepted)

```
| State | Operation Allowed? | KB Basis | Notes |
|-------|------------------|---------|-------|
| In-force | [Allowed/Not Allowed] | ps-customer-service.md S.XX | |
| Lapsed | [Allowed/Not Allowed] | ps-customer-service.md S.XX | |
| Loan | [Allowed/Not Allowed] | ps-loan-deposit.md S.XX | |
| Surrender Pending | [Allowed/Not Allowed] | ps-customer-service.md S.XX | |
| Claims Pending | [Allowed/Not Allowed] | ps-claims.md S.XX | |
| Reinstatement Pending | [Allowed/Not Allowed] | ps-customer-service.md S.XX | |

⚠️ If KB does not document behavior for a state → mark as "UNKNOWN — pending confirmation with product team"
```

### Business Process Change (NEW)

> Before/After business process step comparison

**KB Constraint:** Before process must cite ps-*.md OOTB process sections (no other KB references accepted)

```
## Before (OOTB Process)
| Step | Action | Actor | System Behavior | KB Ref |
|------|--------|-------|----------------|---------|
| 1 | Customer requests surrender | Customer/Agent | System displays SV | ps-customer-service.md S.15 |
| 2 | Confirm surrender amount | CS | System calculates SV = Units×NAV−Charge | ps-fund-administration.md S.243 |
| 3 | Confirm surrender | CS | Policy status→Surrendered | ps-customer-service.md S.18 |

## After (New Process)
| Step | Action | Actor | System Behavior | Change Description |
|------|--------|-------|----------------|-------------------|
| 1 | Customer requests surrender | Customer/Agent | System displays SV (with floor) | New floor calculation added |
| 2 | Confirm surrender amount | CS | System calculates SV = MAX(Units×NAV−Charge, 80%×Premiums) | Formula changed |
| 3 | Surrender check | CS | System validates floor constraint | New validation logic added |
| 4 | Confirm surrender | CS | Policy status→Surrendered | No change |

⚠️ After citing KB for Before process, if KB description does not match actual OOTB behavior → mark as "OOTB behavior pending verification"
```

### Business Rule Conflict Check (NEW)

> Checks whether the new rule conflicts with existing business rules in the KB

**KB Constraint:** Must cite ps-*.md business rule sections as conflict evidence (no other KB references accepted)

```
## Conflict Check

| New Business Rule | Conflicting Rule | KB Ref | Conflict Analysis | Conclusion |
|------------------|-----------------|--------|----------------|-----------|
| SV floor = 80%×Premiums | No surrender during loan | ps-loan-deposit.md S.5 | Independent — no conflict | No conflict |
| SV floor constraint | Policy loan value cap | ps-loan-deposit.md S.10 | If SV < loan balance, surrender cannot repay loan | ⚠️ Pending: Does loan get repaid first? |
| — | Lapsed policy surrender restriction | ps-customer-service.md | Not documented | Pending confirmation |

⚠️ If no KB citation proves a conflict exists → mark as "Pending verification — requires product team confirmation"
⚠️ Do not assume conflicts exist — KB citation is required to claim a conflict
```

### Dependent / Downstream Impacts

| Module | Impact | Business Impact Description | KB Ref |
|--------|--------|--------------------------|---------|
| NB | 🟡 Indirect | New rule visible in NB illustration | ps-new-business.md S.XX |
| CS | 🔴 Direct | Surrender CS Item executes new floor rule | ps-customer-service.md S.15 |
| Claims | 🟡 Indirect | Surrender payment must comply with floor | ps-claims.md S.XX |
| Billing | ⚪ None | No business impact | — |

### Open Questions (if any)
| ID | Question | Business Impact | Owner | SLA | Blocking? |
|----|---------|----------------|-------|-----|-----------|
| DQ-01 | [Question] | [High/Medium/Low] | [Name] | YYYY-MM-DD | [Yes/No] |

⚠️ Every "Pending confirmation" mark must appear in Open Questions with an assigned Owner

### R3 / R4 / R6 / R7 / R8 / R9 Findings

```
R3 Overflow: [YES / NO]
  If YES: KB says "[X]" is [supported/configurable] but spec variant "[Y]" exceeds it.
  Overflow Type: [Calendar Year counter / Joint-Life Blended Rate / Cross-policy aggregate / etc.]
  Classification impact: [Config → Dev Gap / OOTB → Dev Gap / etc.]

R4 Integration Record: [YES / N/A]
  If YES:
    Integration: [Name]
    Direction: [Inbound / Outbound / Bidirectional]
    Protocol: [REST / SOAP / SFTP / Kafka / MQ / Manual / UNKNOWN]
    Target: [System or party]
    Trigger: [Real-time / Near-real-time / Daily batch / On-demand / UNKNOWN]
    Data Domain: [Policy / Payment / Party / Finance / Claim / Channel / Reinsurance / Investment]
    Auth: [OAuth 2.0 / mTLS / API key / SSO / UNKNOWN]
    Effort: [Low / Medium / High / UNKNOWN]
  If N/A: No third-party integration required

R6 Regulatory: [YES / NO]
  If YES: [SFA / MAS / LIA CI Framework / etc.] — trigger Agent 3
  Regulatory Reference: [Specific law/section/notice]

R7 UI/UX Dimension: [YES / N/A]
  If YES:
    UI Flow: [Self-managed / Discretionary Mandate / Multi-party / Alert & Notification]
    Screens Affected: [List]
    User Roles: [Policyholder / CS / Claims / AM / Custodian]
    Interaction Pattern: [Real-time / Asynchronous / Batch notification]

R8 Batch/SLA: [YES-Batch / YES-RealTime / YES-Manual / N/A]
  If not N/A:
    Frequency: [daily / weekly / monthly / on-demand / event-driven]
    Monitoring Logic: [Description]
    Source: R8

R9 Complexity: [Low / Medium / High / N/A — Dev Gap]
  If High: "R9 HIGH COMPLEXITY — recommend dedicated estimation session with Config Lead"
  Rule combinations: [estimated number]
  Config items: [estimated number]
```

### Deliverable to Agent 2
```
Status: [READY_FOR_BSD / BLOCKED]
Gap ID: [Gap ID]
BSD Required: [YES / NO]
BSD Focus: [What Agent 2 must write]
Compliance Check: [YES — trigger Agent 3 / NO]
R3 Overflow: [YES / NO]
R4 Integration: [YES — see record above / N/A]
R6 Regulatory: [YES — Agent 3 required / N/A]
R7 UI/UX: [YES — see R7 section / N/A]
R8 Batch/SLA: [YES / N/A]
R9 Complexity: [Low / Medium / High / N/A]
Ripple Chain: [Yes/No — if Yes, note which modules are in chain]
KB Completeness: [Complete/Partial/Unverified]
  → Complete: all sections have KB citations
  → Partial: some sections marked "Pending confirmation" in Open Questions
  → Unverified: OOTB behavior sections lack KB citations — requires BA validation
```
```

## Quality Checkpoint (MUST PASS BEFORE OUTPUT)

**Before outputting Solution Design, verify:**

```
[ ] Every row has a ps-* Reference (format: references/InsureMO Knowledge/ps-{file}.md Section N)
    — OOTB: cite the ps-* section that confirms this is already supported
    — Config: cite the ps-* section + the config path
    — Dev: cite the ps-* section that shows limitation OR mark "NOT FOUND in ps-*" if not in KB
    — UNKNOWN: mark as UNKNOWN and assign an owner
[ ] No invented Config Paths — if not found in KB, set Config Path Source = "Assumed" and flag for Agent 6 verification
[ ] Every Dev Gap has a clear "why Dev" statement: either ps-* Limitation cited or "NOT FOUND in ps-*" stated
[ ] New fields are marked as NEW and verified not in ps-*
[ ] Gap Description Writing Patterns verified — see references/gap-description-patterns.md
[ ] All Impacted Modules assessed (no blanks) — all 12 InsureMO modules covered
[ ] Semantic Override applied for cross-system / cumulative / third-party patterns
[ ] V3 Cross-Reference applied to all non-Dev-Gap items — every ps-* OOTB / Config / UNKNOWN row has a V3_Classification value or V3 N/A noted
[ ] V3 Override documented — if V3 changed the ps-* conclusion, V3 Ref and V3 Evidence are cited in Gap Matrix notes
[ ] V3 Dev Gap Downgrade documented — if V3 evidence caused a Dev Gap to be downgraded to Config/OOTB, this is recorded with explicit evidence citation
[ ] Product Profile CFG-ID / FORMULA-ID traceability verified (Step 1.5.3):
    — Every CFG-ID in the Gap Matrix maps to a Product Profile CFG entry
    — Every FORMULA-ID in the Gap Matrix maps to a Product Profile FORMULA entry
    — Every feature in the Product Profile that was not extracted has a reason noted
[ ] Agent 5 UNKNOWN Type integration applied:
    — NOT_STATED → treated as requirement gap, logged in Agent 1 UNKNOWN Register
    — MISSING_ATTACHMENT → blocked, escalated to client
    — NOT_FOUND → verified spec section, treated as NOT_STATED if confirmed missing
[ ] R10 scanner applied — every feature scanned against expanded R10 keyword list
[ ] V3 Dev Gap Downgrade rule applied — Dev Gap items that V3 proves are Config/OOTB are correctly reclassified
[ ] KB-Missing Degradation applied — sections with MISSING KB but concrete spec parameters are analyzed with Config Path Source = "MISSING_KB — analyzed from spec"; no section skipped
[ ] Spec Section Coverage complete — every spec §N has a gap ID entry (or explicit "N/A for this product" notation); no orphaned spec sections

[R1-R9 MANDATORY CHECKS:]
[ ] R1 NFR — All performance SLAs, availability, data residency, security, DR requirements captured in NFR Appendix
[ ] R2 Blind Spot — Every functional requirement has a matching KB row or Blind Spot flag
[ ] R3 Overflow — Every OOTB/Config item tested against R3 overflow table; R3 overflows documented with type
[ ] R4 Integration — Every third-party integration has a complete R4 Integration Record (all 8 dimensions)
[ ] R5 Migration — Confirmed greenfield or migration section added
[ ] R6 Regulatory — Market-specific regulatory matrix applied; Agent 3 triggered for all R6-yes items
[ ] R7 UI/UX — Every user-facing Dev Gap has R7 UI/UX dimension documented
[ ] R8 Batch/SLA — Every monitoring/enforce pattern classified as Batch / Real-Time / Manual
[ ] R9 Complexity — Every Config Gap rated Low / Medium / High; High items flagged for dedicated estimation
```

## Dev Gap Solution Design Quality Checks (v3.3 additions)

```
[ ] Change Point — all fields have KB citations, no blanks
[ ] Current Behaviour — has ps-*.md citation; if marked "undocumented", entered in Open Questions
[ ] Delta Summary — Current column has KB citation or "None"
[ ] R3 Overflow — if R3 overflow YES, overflow type and classification impact documented
[ ] R4 Integration Record — all 8 dimensions filled (Integration, Direction, Protocol, Target, Trigger, Data Domain, Auth, Effort)
[ ] R6 Regulatory — if R6 YES, compliance reference and Agent 3 trigger documented
[ ] R7 UI/UX — if R7 YES, UI flow, screens, roles, and interaction pattern all documented
[ ] R8 Batch/SLA — if R8 YES, frequency and monitoring logic documented
[ ] R9 Complexity — if High, dedicated estimation recommendation included
[ ] Business Scenario Matrix — each scenario:
    — has KB citation OR marked "Pending confirmation"
    — scenario ID naming correct ({Function}_{Seq}_{BriefDesc})
    — all "Pending confirmation" scenarios entered in Open Questions
[ ] Policy State Constraints — each policy state:
    — has ps-customer-service.md citation OR marked "UNKNOWN — pending confirmation with product team"
    — all "Pending confirmation" states entered in Open Questions
[ ] Business Process Change — Before process each step has KB citation
[ ] Business Rule Conflict Check — each conflict analysis:
    — has KB citation proving conflict exists
    — conflict claim without KB citation → marked "Pending verification — requires product team confirmation"
    — all "Pending verification" items entered in Open Questions
[ ] Dependent / Downstream Impacts — each row has KB citation for business impact
[ ] Open Questions — every "Pending confirmation/Pending verification" mark has an entry with Owner and SLA assigned
[ ] KB Completeness flag set (Complete / Partial / Unverified)
```

**Key Requirements:**
- Change Point MUST reference real ps-* sections (e.g., references/InsureMO Knowledge/ps-new-business.md Section 225)
- Use **references/KB_USAGE_GUIDE.md** to quickly find ps-* section mappings
- Do NOT assume Screen IDs - use ps-* section references
- Do NOT fill in "reasonable assumptions" — leave blank and mark as "Pending confirmation"
- For Dev Gap Solution Design Template: Only ps-*.md is valid as KB reference for OOTB behavior
- For Gap Analysis (Agent 1 overall): Continue using all relevant KB types (ps-*.md, insuremo-ootb.md, v3-ug-*.md, reg-*.md) as appropriate

## Completion Gates
- [ ] Pre-Analysis Checklist completed — all 4 items confirmed before analysis began
- [ ] **R10 scanner run on ALL features** — expanded keyword list applied (cross-policy, reinsurance, dynamic calc, regulatory)
- [ ] **Any R10-flagged item has R10_Flag = YES in Gap Matrix**
- [ ] **Any R10 override has written justification citing specific KB source and InsureMO capability**
- [ ] **Business Semantic Understanding applied** — cross-system, third-party, dynamic patterns identified
- [ ] **V3 Cross-Reference applied** — every OOTB / Config / UNKNOWN / Dev Gap feature has V3_Classification column filled or N/A noted
- [ ] **V3 Override documented** — every V3 override has V3 Ref, V3 Evidence, and V3 Override Applied noted
- [ ] **V3 Dev Gap Downgrade documented** — if V3 evidence caused a Dev Gap to be downgraded, the downgrade is recorded with explicit V3 evidence citation
- [ ] **KB-Missing sections analyzed** — every spec §N with concrete parameters has a gap ID even if KB file is missing; no section skipped due to absent KB
- [ ] **Spec Section Coverage Audit** — every spec §N is represented in Gap Matrix (gap ID or explicit "N/A" notation)
- [ ] **Product Profile CFG-ID / FORMULA-ID traceability verified** — all CFG/FORMULA IDs in Gap Matrix map to Product Profile entries
- [ ] **Agent 5 UNKNOWN Type integration applied** — NOT_STATED / MISSING_ATTACHMENT / NOT_FOUND correctly routed
- [ ] Every row has a Gap Type (no blanks)
- [ ] Every row has all **12 InsureMO modules** assessed in Step 3 (no blanks — use ⚪ None with reason if no impact)
- [ ] **Every Dev Gap has a completed Solution Design Template (v3.3)** — all sections filled with KB citations or "Pending confirmation/Pending verification" marks
  - Change Point — KB citations complete
  - Current vs Required Behaviour — Current has KB citation or marked "undocumented"
  - R3 / R4 / R6 / R7 / R8 / R9 — all applicable fields completed
  - Business Scenario Matrix — all scenarios have KB citation or "Pending confirmation" mark
  - Policy State Constraints — all states have KB citation or "UNKNOWN" mark
  - Business Process Change — Before process has KB citation
  - Business Rule Conflict Check — all conflicts have KB citation or "Pending verification" mark
  - Dependent / Downstream Impacts — has KB citation
  - Open Questions — every "Pending confirmation" entry has Owner and SLA
  - KB Completeness = Complete / Partial / Unverified flag set
- [ ] **R2 Blind Spot check passed** — every Gap Matrix row has KB coverage confirmed (ps-*.md citation) or is marked R2 = YES with Status = BLOCKED; all R2 FAIL items are in unknown-register.md with Owner + SLA *(→ executed in Step 2E)*
- [ ] **All OPEN UNKNOWNs are registered in `unknown-register.md` AND linked in `references/delivery-traceability.md`**
- [ ] Ripple chains (3+ hops) are flagged with `⚡ RIPPLE CHAIN` in Step 3 for Agent 7 handoff
- [ ] Dev Gap items have an effort level with day range (S / M / L / XL)
- [ ] Config Gap items have a specific Product Factory parameter path
- [ ] **Semantic Override applied** — cross-policy/cumulative/third-party items classified as Dev Gap
- [ ] **Dev Gap items have Limitation Source OR Semantic Justification** (ps-*.md Limitations OR business logic explanation)
- [ ] Priority assigned using Gap Severity Reference table; criterion documented
- [ ] Dependencies identified for every Dev Gap and Config Gap
- [ ] Low Priority items marked as Backlog and excluded from current delivery scope
- [ ] Gap classification and priority validated with stakeholders before submission
- [ ] **R1 NFR Appendix** — all performance SLAs, availability, data residency, security, DR captured in NFR Appendix
- [ ] **R3 Overflow check** — every OOTB/Config item tested against overflow table; no overflows missed
- [ ] **R4 Integration Records** — all third-party integrations have complete R4 records (all 8 dimensions)
- [ ] **R6 Regulatory** — Agent 3 triggered for all R6-yes items before Gap Matrix finalized
- [ ] **R7 UI/UX dimensions** — all user-facing Dev Gaps have R7 UI/UX documented
- [ ] **R8 Batch/SLA** — all monitoring/enforce patterns classified; batch items have frequency
- [ ] **R9 Complexity** — all Config Gaps rated; High Complexity flagged for dedicated estimation

