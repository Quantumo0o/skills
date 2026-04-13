---
name: insuremo-kb-builder
description: Convert InsureMO / eBaoTech user guide documents (.docx, .pdf, or raw markdown) into clean, structured OpenClaw agent knowledge base files (ps-*.md format). Use this skill whenever the user uploads an InsureMO user guide and asks to build a knowledge base, convert it to KB format, or create a ps-*.md reference file. Also triggers on phrases like "help me build the KB", "convert this user guide", "write the knowledge base", "generate the ps file", or when the user says "整理成知识库" / "转成md" / "转成知识库". Produces files that are directly usable by Agent 1 (Gap Analysis) and Agent 6 (Config Runbook) in the InsureMO BA Agent suite.
---

# InsureMO KB Builder

Converts InsureMO / eBaoTech user guide documents into clean OpenClaw knowledge base files (`ps-*.md`).

The output must be immediately useful to Agent 1 (Gap Analysis) and Agent 6 (Config Runbook) — not a reformatted copy of the user guide, but a structured reference that answers: *"what does the system do, what are the prerequisites, what are the business rules, and where is it configured?"*

---

## Input Types

1. **`.docx` file** — extract with pandoc, clean tracked-change markup
2. **`.pdf` file** — extract with pdfplumber, clean page/header noise
3. **Raw or dirty markdown** — clean and restructure
4. **Multiple files** — if both docx and pdf provided for the same module, docx takes priority (better structure preservation)

---

## Step 1 — Extract & Clean

### 1A — If input is .docx

```bash
pandoc --track-changes=all input.docx -o raw.md
```

Then clean the pandoc output:

```python
import re

with open('raw.md') as f:
    text = f.read()

# Remove tracked-change markup from pandoc
text = re.sub(r'\{\.(?:insertion|deletion|paragraph-insertion|paragraph-deletion)[^}]*\}', '', text)
text = re.sub(r'\[\]\{[^}]*\}', '', text)
text = re.sub(r'\[([^\]]*)\]\{[^}]*\}', r'\1', text)

# Remove Word revision sidebar noise (Chinese or English)
text = re.sub(r'(?m)^(?:设置格式|删除|插入)\[.*?\]:\s*\n(?:.*\n)*?(?=\n)', '', text)
text = re.sub(r'(?m)^字体:.*$', '', text)
text = re.sub(r'(?m)^(?:删除|插入)\[.*?$', '', text)

# Remove page numbers (standalone digit lines)
text = re.sub(r'(?m)^\d{1,3}\s*$', '', text)

# Remove figure/image references (no useful content)
text = re.sub(r'!\[.*?\]\(media/[^)]+\)[^\n]*', '', text)
text = re.sub(r'(?m)^\*?\*?Figure \d+\..*$', '', text)

# Remove TOC lines (e.g. "Register a Case 9")
text = re.sub(r'(?m)^.{5,60}\s{2,}\d+\s*$', '', text)

# Remove copyright / cover boilerplate
text = re.sub(r'(?s)©.*?eBaoTech Corporation.*?(\n\n)', r'\1', text)

# Collapse excess blank lines
text = re.sub(r'\n{4,}', '\n\n\n', text)

with open('clean.md', 'w') as f:
    f.write(text)
```

### 1B — If input is .pdf

```bash
pip install pdfplumber --break-system-packages -q
```

```python
import pdfplumber, re

pages_text = []
with pdfplumber.open('input.pdf') as pdf:
    for page in pdf.pages:
        # Try table extraction first — pdfplumber handles bordered tables well
        tables = page.extract_tables()
        if tables:
            for table in tables:
                for row in table:
                    cells = [c.strip() if c else '' for c in row]
                    pages_text.append(' | '.join(cells))
        # Always extract full text too (tables may be partial)
        text = page.extract_text()
        if text:
            pages_text.append(text)

raw = '\n'.join(pages_text)

# --- PDF-specific noise removal ---

# Remove repeating page headers/footers (lines that appear 3+ times verbatim)
from collections import Counter
lines = raw.split('\n')
line_counts = Counter(l.strip() for l in lines if len(l.strip()) > 3)
repeating = {l for l, c in line_counts.items() if c >= 3}
lines = [l for l in lines if l.strip() not in repeating]
raw = '\n'.join(lines)

# Remove standalone page numbers
raw = re.sub(r'(?m)^\d{1,3}\s*$', '', raw)

# Remove Figure caption lines
raw = re.sub(r'(?m)^Figure \d+[.:)].+$', '', raw)

# Remove TOC lines (text followed by spaces/dots and a page number)
raw = re.sub(r'(?m)^.{5,60}[. ]{2,}\d+\s*$', '', raw)

# Remove copyright boilerplate
raw = re.sub(r'(?s)©.*?eBaoTech Corporation.*?\n\n', '\n', raw)

# Collapse excess blank lines
raw = re.sub(r'\n{4,}', '\n\n\n', raw)

with open('clean.md', 'w') as f:
    f.write(raw)
```

**PDF extraction notes:**
- `pdfplumber` handles text-based PDFs well; scanned image PDFs will produce empty or garbage output — if that happens, tell the user the PDF appears to be scanned and ask for a text-based version or docx instead
- Table extraction from PDF is less reliable than from docx — after extracting, manually verify that field description tables came through correctly before writing the KB; if a table looks garbled, re-extract that page with `page.extract_text()` only and parse manually
- PDF has no heading hierarchy — section boundaries are inferred from text patterns (ALL CAPS lines, lines matching known section names like "PREREQUISITE", "Register a Case", etc.)

### 1C — If input is raw/dirty markdown

Apply only the relevant cleaning steps from 1A (skip pandoc; run the regex cleanup directly on the uploaded content).

---

Read `clean.md` and proceed to Step 2.

---

## Step 2 — Build an Extraction Inventory

Before writing a single line of output, scan the entire cleaned source and build an explicit inventory. This inventory is your contract — every item must appear in the output.

**2A — Count and list every field table in the source:**

Go through every table in the document (Appendix A, inline field description tables, rule tables). For each one, record:
```
TABLE INVENTORY
- [Table name / section it appears in] — [N rows of data]
- [Table name / section it appears in] — [N rows of data]
...
Total: N tables, ~N field rows
```

**2B — Count and list every rule block:**

Identify every PREREQUISITE block, NOTE with system behaviour, Appendix B rule section, auto-acceptance/approval condition list, validation error message, and submission check list. Record:
```
RULE BLOCK INVENTORY
- PREREQUISITE: [section name]
- Validation rules at submit: [section name]
- Auto-acceptance conditions: [section name]
- Business rules appendix: [section name]
...
Total: N rule blocks
```

**2C — Identify process variations:**

List every variant that needs a separate subsection:
- Auto vs Manual (per stage)
- Claim type variants (TPD/Death vs Medical vs Waiver)
- ILP vs Traditional where rules differ

**2D — Answer these questions:**
1. What module is this?
2. What are the major workflow stages?
3. What menu navigation paths appear?
4. What status transitions are described?
5. What config items are mentioned as configurable?

**The inventory is mandatory.** If a table or rule block is in the inventory, it MUST appear in the output. Do not proceed to Step 3 until the inventory is complete.

The reason this matters: the default tendency when converting a long document is to summarise rather than extract. A 200-row field table summarised as "Field Reference: [3 rows]" is useless to an agent trying to write a config runbook. Every row in the source table must appear in the output table.

---

## Step 3 — Write the ps-*.md File

### File naming
- `ps-claims.md` for Claims
- `ps-customer-service.md` for Customer Service / Policy Servicing
- `ps-new-business.md` for New Business
- `ps-underwriting.md` for Underwriting
- `ps-billing.md` for Billing & Collection
- `ps-product-factory.md` for Product Factory / LI Expert Designer

### Required file header

```markdown
# InsureMO Platform Guide — [Module Name]
# Source: [Document name and version]
# Scope: BA knowledge base for Agent 2 (BSD Configuration Task) and Agent 6 (Config Runbook)
# Do NOT use for Gap Analysis — use insuremo-ootb.md instead
# Version: 1.0 | Updated: [YYYY-MM]
```

### Required sections (adapt based on what the source contains)

Every ps-*.md file must include these sections — skip a section only if the source genuinely has no relevant content for it, and note the omission.

#### 1. Purpose of This File
Two sentences: what questions this file answers, and when to use it (Agent 2 / Agent 6 / BA verification).

#### 2. Module Overview
ASCII tree showing sub-components. Example:
```
Claims Module
│
├── Standard Claims
│   ├── Case Registration
│   ├── Case Acceptance
│   └── ...
└── Advanced Functions
```

#### 3. Workflow — Standard Sequence
Show the main flow as a code block diagram. Include branching for Auto vs Manual if applicable.

#### 4. Menu Navigation Table
| Action | Path |
|---|---|

Always use the exact menu paths from the source (e.g. `Claims > Registration`).

#### 5. Status Reference Table (if applicable)
| Status | When Set |
|---|---|

#### 6. Per-Process Sections
One `## Part N —` section per major workflow step (e.g. `## Part 1 — Case Registration`).

**Do NOT use a single `### Key Rules` catch-all.** Each type of rule gets its own named `###` subsection. This is mandatory — agents search by subsection name.

Required `###` subsections per process section (create all that have content in the source):

| Subsection | What goes here |
|---|---|
| `### Prerequisites` | Every bullet condition from PREREQUISITE blocks |
| `### Navigation` | Exact menu path |
| `### Steps` | Numbered steps; remove pure-UI sub-steps only |
| `### [Variant A] Steps` | If Auto/Manual or claim-type variants exist, one subsection per variant |
| `### [Variant B] Steps` | e.g. `### Evaluate TPD/Death Claims`, `### Evaluate Medical Claims`, `### Evaluate Waiver Claims` |
| `### [Process Name] Rules` | Named business rules (e.g. `### Case Number Generation Rule`, `### Duplicate Case Rule`, `### Diagnosis Code Rules`, `### Policy Lock Rules`) — one subsection per distinct named rule cluster |
| `### Submission Validation` | **Mandatory table format:** `\| Condition \| System Action \|` — one row per check; include exact error/warning message text from source |
| `### [Stage] Field Reference` | One table per Appendix A table or inline field description block; all rows, all columns |
| `### Default Payee Rules` | Payee logic tables where applicable |
| `### [Item] Field Reference` | Additional field tables (e.g. `### Installment Plan Field Reference`) |

**The "Submission Validation" subsection is especially critical.** Every document has a list of checks that run when the user clicks Submit. These must always be a `| Condition | System Action |` table, never a bullet list. Example:

```markdown
### Submission Validation

| Condition | System Action |
|---|---|
| Policy has outstanding premium | Warning: "Policy has outstanding premium" |
| Required document Completeness ≠ Y AND Waive ≠ N | Warning: "There is uncompleted required document. Please confirm to continue?" |
| Query letter not replied | Error: "Query letter is not replied." |
```

**Process variants** (Auto vs Manual, claim type differences) must be separate named subsections, not merged. Example:
- ✅ `### Evaluate TPD/Death Claims` + `### Evaluate Medical Claims` + `### Evaluate Waiver Claims`
- ❌ `### Evaluation Steps` (merged)

#### 7. Config Gaps Commonly Encountered
Table of typical config gaps for this module:

| Scenario | Gap Type | Config Location |
|---|---|---|

Use `Config Gap` or `Dev Gap (LIMO IT)` as Gap Type. Config Location should reference the exact menu path or config table name from the source.

#### 8. INVARIANT Declarations
Numbered list of system constraints that always apply, formatted as:

```
INVARIANT N: [One-sentence statement of the constraint]
  Checked at: [Where in the workflow]
  Error/Effect if violated: [What happens]
```

Only declare INVARIANTs for hard system-enforced rules (not soft warnings).

#### 9. Related Files
| File | Purpose |
|---|---|
| `insuremo-ootb.md` | Gap Analysis |
| `ps-product-factory.md` | (if config paths reference Product Factory) |
| `ps-customer-service.md` | (if cross-module interaction documented) |
| `output-templates.md` | BSD templates |

---

## Writing Rules

### Completeness is the primary obligation

The KB file is only useful if it is **complete**. An agent reading a field table with 3 rows instead of 30 will produce incorrect output. Summarising or paraphrasing field tables is a defect, not a feature.

**Hard rules:**
- Every field table from the source → a complete markdown table in its own `### [Name] Field Reference` subsection. Zero rows may be omitted.
- Every PREREQUISITE block → a bullet list under `### Prerequisites`. Zero conditions may be omitted.
- Every Appendix B rule cluster → moved under the relevant workflow section as its own named `###` subsection. Never left in a catch-all `### Key Rules` or separate appendix.
- Every submission check list (on Submit, on Save) → a `| Condition | System Action |` table with exact error/warning message text. **Never a bullet list.**
- Every auto-acceptance / auto-approval condition list → full bullet list under its own `### Auto [Stage] Rules` subsection.
- Every named rule cluster → its own `###` subsection. Examples: `### Case Number Generation Rule`, `### Duplicate Case Rule`, `### Diagnosis Code Rules`, `### Policy Lock Rules`, `### ILP Evaluation Rules`, `### Default Payee Rules`.
- Every process variant → a separate named `###` subsection. Never merged.

**Anti-patterns to avoid:**

❌ `### Key Rules` with 6 different rule types merged → ✅ One `###` subsection per distinct rule cluster  
❌ Submission check list as bullet points → ✅ `| Condition | System Action |` table with exact message text  
❌ `### Evaluation Steps` (all claim types merged) → ✅ Separate: `### Evaluate TPD/Death Claims` + `### Evaluate Medical Claims` + `### Evaluate Waiver Claims`  
❌ `### Installment Steps` without a separate `### Installment Plan Field Reference` → ✅ Both present  
❌ "Field Reference: [5 rows]" when source has 20 rows → ✅ All 20 rows  
❌ "Auto acceptance conditions: configurable rules apply" → ✅ All 10 conditions listed  
❌ Leaving Appendix B at end of file → ✅ Each rule cluster moved to its workflow section  

---

**What to include:**
- All field descriptions from Appendix A — every row, every column
- All business rules from Appendix B — under the relevant workflow section
- All PREREQUISITE blocks — every bullet condition
- All validation/submission check lists — every condition + system response
- All auto-acceptance and auto-approval conditions — every item
- All process variants — as separate subsections
- All menu navigation paths — exact paths as they appear
- All status transitions — every status value and when it is set
- All formulas and calculation rules — explicit, not paraphrased
- All error messages — exact text where given
- All configurable items — with the config location

**What to strip** (and only these things):
- Figure/image references (`Figure N. ...`) — no images in KB
- Page numbers (standalone digit lines)
- TOC entries
- Copyright / cover boilerplate
- `Step Result:` lines that only say "the page appears"
- `NOTE:` blocks that only say "for more information, see [section]"
- UI navigation sub-steps that contain zero field or rule information (e.g. "click OK on the confirmation dialog")
- Word revision markup (`设置格式`, `删除`, `字体:`)

**What to restructure** (preserve all content, change structure only):
- Source tables (Word grid format) → clean markdown `| Field | Allowed Values | Description |`
- Appendix B rules → moved under relevant workflow section
- Inline bullet conditions → grouped under named header
- Numbered steps → keep, remove only pure-UI sub-steps

**Precision rules:**
- Every validation condition: what triggers it AND what happens (no half-rules)
- Every field with enumerated values: all values listed
- Every formula: written explicitly as `Result = A - B - C`, not described in prose
- Named constants: state the source "(as configured in Product Factory)" or "(code table X)"
- No "etc." / "as applicable" / "configurable" without naming what is configurable and where

---

## Step 4 — Self-Check Before Delivering

This checklist is driven by the inventory you built in Step 2. The numbers must match.

```
INVENTORY RECONCILIATION (numbers from Step 2 must match output):
□ Tables: [N tables in inventory] → [N tables in output] — counts match
□ Field rows: [N rows in inventory] → [N rows in output] — counts match
□ Rule blocks: [N blocks in inventory] → [N blocks placed in output] — counts match
□ Process variants: [list from 2C] → each has its own named subsection

Content completeness:
□ All PREREQUISITE blocks reproduced in full (zero conditions omitted)
□ All Appendix A field tables: every row present, no summarising
□ All Appendix B rules moved to relevant workflow section (no orphan appendix)
□ All auto-acceptance / auto-approval condition lists reproduced in full
□ All submission validation check lists present as Condition → System Action tables
□ All status values listed in status reference table
□ All process variants (Auto/Manual, claim type variants, ILP/Trad) have separate subsections

Structure:
□ File header present (source, scope, version)
□ Module Overview tree present
□ Workflow sequence diagram present
□ Menu Navigation table present
□ Per-process sections follow: Prerequisites → Navigation → Steps → Rules → Fields
□ Config Gaps table present
□ INVARIANT declarations present (minimum 3)
□ Related Files section present

Quality:
□ No figure references in output
□ No page numbers in output
□ No Word revision markup in output
□ No half-rules (every condition has a consequence)
□ No "etc." / "TBD" / "configurable" without naming what and where
□ All fields with enumerated values have Allowed Values column listing all values
□ All formulas written explicitly (not paraphrased)
□ PDF source: all field tables verified correct (not garbled)
```

**If any inventory count does not match → go back and add the missing content.**
Do not deliver a file where the inventory reconciliation numbers don't match.

---

## Output Format

Deliver as a `.md` file saved to `/mnt/user-data/outputs/ps-[module].md` and presented via `present_files`.

After presenting, give a one-line summary:
- Lines written
- Sections included
- Any source gaps (content in the source that was unclear or missing)

Do NOT summarise the contents of the file in detail — the user can read it.
---

## Additional Requirements (v1.1)

### Submission Validation - MUST Be Stage-Specific

Each stage's submission validation must have a UNIQUE ### name:

| Stage | Required Subsection Name |
|-------|------------------------|
| Registration | ### Registration Submission Validation |
| Acceptance | ### Acceptance Submission Validation (on Submit in Acceptance Summary) |
| Evaluation | ### Evaluation Submission Validation (on Submit in Case Evaluation) |
| Disbursement | ### Disbursement Submission Validation |
| Approval | ### Approval Submission Validation |

Do NOT use generic "### Submission Validation" - must be stage-specific!

### Advanced Functions - MUST Have Separate ### Subsections

For Claims, these MUST each have their own ### subsection under ## Part 7 — Advanced Functions:

- ### Claims Watch List
- ### Change Disbursement Plan
- ### Cancel a Case
- ### Reverse Case
- ### Claims Query
- ### Copy Case
- ### Add Insured for Claim
- ### Medical Report Fee Payment

Do NOT merge into one "### Advanced Functions" section!

### Field Tables - Verify All Rows

After writing the output, verify that each field table has the same number of rows as the source:
1. Count tables in source document
2. Count tables in output
3. If counts don't match, find and add missing tables

---

## 4-Phase Processing (Recommended for Large Documents)

For documents with 50+ pages or complex tables, use this phased approach to avoid timeout:

### Phase 1 — Extract + Build Inventory (Step 1 + Step 2)
- Input: PDF/docx file
- Output: Extraction Inventory only (not the full document)
- This verifies completeness before writing

### Phase 2 — Write Core Parts (Part 1~3)
- Input: Cleaned text + Inventory
- Output: ps-[module].md (Part 1-3: Core workflow sections)

### Phase 3 — Write Extended Parts (Part 4~9)
- Input: ps-[module].md (from Phase 2) + Inventory
- Output: Append Part 4-9 (Advanced functions, Config Gaps, INVARIANTs)

### Phase 4 — Self-Check + Finalize (Step 4)
- Input: Complete draft
- Output: Final ps-[module].md with inventory reconciliation

**Files during processing:**
- `ps-[module]-p1-inventory.md` — Phase 1 output
- `ps-[module]-p2.md` — Phase 2 output  
- `ps-[module]-p3.md` — Phase 3 output
- `ps-[module].md` — Final output

**Timeout prevention:**
- Each phase runs in a separate turn (no timeout)
- Inventory ensures completeness even if interrupted
- Intermediate files allow resume from last phase
