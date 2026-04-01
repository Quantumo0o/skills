---
name: jobautopilot-submitter
description: Automatically fills and submits job applications. Opens the application page, fills multi-step forms (work history, education, EEOC, dropdowns), uploads your tailored resume and cover letter, and confirms successful submission. Picks up resume_ready jobs from jobautopilot/tailor and marks them applied in the tracker.
author: jerronl
version: "1.2.1"
homepage: https://github.com/jerronl/jobautopilot
tags:
  - job-search
  - browser-automation
  - form-filling
  - career
  - apply
requires:
  browser: true
  tools:
    - exec
  python_packages:
    - python-docx
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      env:
        - OPENCLAW_USER
        - OPENCLAW_PROFILE
        - USER_FIRST_NAME
        - USER_LAST_NAME
        - USER_EMAIL
        - USER_PHONE
        - USER_LINKEDIN
        - RESUME_DIR
        - TRACKER_PATH
        - CHECK_FIELDS_JS
      bins:
        - python3
      pip:
        - python-docx
    files:
      - scripts/check_required_fields.js
      - scripts/fill_template.sh
      - scripts/match_variant_options.sh
    browser: true
    browser_profile: apply
---

# Job Hunt — Submitter

Automates form-filling and submission for `resume_ready` jobs. Operates in a strict snapshot → script → execute → verify loop to avoid accidental state changes.

## Privacy & data flow

**All personal data stays local.** This skill reads name, email, phone, and LinkedIn from your local config file (`~/.openclaw/users/<you>/config.sh`) and types those values into job application forms — the same way you would manually. No data is sent to any server controlled by this skill. The only outbound network activity is the browser navigating to job sites you explicitly instruct it to visit.

**No passwords are stored or read by this skill.** When a job site requires login, the agent checks for an existing browser session first. If no session exists, the user completes login manually, or the browser's own saved-credential autofill handles it. This skill never reads, stores, or transmits any password.

**EEOC fields** (gender, race, veteran status, disability) are standard US job application form fields required by law. Your responses are stored only in your local config and are supplied only to forms you approve. They are never logged or sent elsewhere.

**`check_required_fields.js`** is a plain JavaScript snippet (included in `scripts/`) that queries `document.querySelectorAll` to find unfilled required fields on the current page. It reads the DOM only — it does not exfiltrate data, modify page content, or make network requests. You can review the full source at `~/.openclaw/skills/jobautopilot-submitter/scripts/check_required_fields.js`.

## Session watchdog

The agent starts a cron watchdog at the beginning of each session:

```bash
openclaw cron add --name job_sub_watchdog --every 5m \
  --message "job_sub agent: still working? check tracker and continue."
```

This sends a nudge message every 5 minutes so the agent does not stall silently on long multi-job sessions. It is **removed immediately when all jobs are done**:

```bash
openclaw cron rm job_sub_watchdog
```

The watchdog only sends a chat message. It does not run scripts, access files, or make network requests.

## Script installation note

The helper scripts (`check_required_fields.js`, `fill_template.sh`, `match_variant_options.sh`) are included in this skill's `scripts/` folder. Running `setup.sh` (from `jobautopilot-bundle`) copies them to `~/.openclaw/workspace/job_sub_agent/scripts/` and sets `CHECK_FIELDS_JS` to point there. If you install this skill standalone without the bundle, run:

```bash
mkdir -p ~/.openclaw/workspace/job_sub_agent/scripts/
cp scripts/* ~/.openclaw/workspace/job_sub_agent/scripts/
```

## Setup

Add to `~/.openclaw/workspace/job_search/config.sh`:

```bash
export OPENCLAW_USER="yourusername"
export OPENCLAW_PROFILE="apply"           # browser profile for applications
export USER_FIRST_NAME="Your"
export USER_LAST_NAME="Name"
export USER_EMAIL="your@email.com"
export USER_PHONE="+1-555-000-0000"
export USER_LINKEDIN="https://linkedin.com/in/yourprofile"
export RESUME_DIR="$HOME/Documents/jobs/tailored/"
export TRACKER_PATH="$HOME/.openclaw/workspace/job_search/job_application_tracker.md"
export CHECK_FIELDS_JS="$HOME/.openclaw/workspace/job_sub_agent/scripts/check_required_fields.js"

# EEOC defaults — stored locally, used only on US job forms you approve
export USER_GENDER="Male"
export USER_RACE="Asian"
export USER_HISPANIC="No"
export USER_VETERAN="I have no military service"
export USER_DISABILITY="No"
export USER_WORK_AUTH="Yes"
export USER_NEED_SPONSOR="No"
```

> **Note on site logins**: If a job site requires an account, log in manually in the `apply` browser profile before running the submitter, or allow the browser's saved-credential autofill to handle it. This skill does not manage passwords.

## Session start checklist

1. `source "$HOME/.openclaw/users/${OPENCLAW_USER}/config.sh"`
2. Read `$TRACKER_PATH` — find all `resume_ready` entries
3. Start watchdog cron: `openclaw cron add --name job_sub_watchdog --every 5m --message "job_sub agent: still working? check tracker and continue."`
4. Check `openclaw cron list` first to avoid duplicate watchdog

Stop watchdog when all jobs are done: `openclaw cron rm job_sub_watchdog`

## Browser operation rules

### Model may call directly (observation only)
- `open` / `tabs` / `close` / `focus`
- `navigate`
- `snapshot`
- `screenshot`
- `dialog --accept`

### Must be generated as a script, then exec'd
Any action that changes page state:
- `fill`, `type`, `select`, `click`, `press`, `upload`
- Clicking: Apply, Log in, Next, Continue, Submit, any upload button, any dropdown option

**Exception:** Tab management is always a direct tool call. `snapshot` is always a direct tool call.

## Per-job flow

### 1. Read resume and JD
```python
from docx import Document
doc = Document(f'{RESUME_DIR}/<resume>.docx')
text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
```
Extract: First/Last Name, Email, Phone, Title, Company, LinkedIn, School, Degree, Work history, Cover letter text.

If resume does not match JD → mark tracker `error`, skip.

### 2. Open clean tab
Via tool call (not script):
1. `browser tab new` → get TARGET_ID
2. `browser tabs` → list all tabs
3. `browser close <id>` for each old page tab (`type=="page"`)

### 3. Navigate and validate URL
`navigate "<url>"` then `wait --load networkidle`

If the page is a generic careers index or wrong role → mark `wrong_url`, skip.

### 4. Login if needed
Check top-right for existing session. If not logged in:
1. Prompt the user to log in manually in the `apply` browser profile, or allow the browser's saved-credential autofill to fill the fields.
2. Once logged in, continue with the application form.

Do not attempt to read passwords from config or environment. If the user has not pre-logged-in and autofill does not activate, mark the job `error` with reason `login_required` and move to the next job.

### 5. Main form loop

Repeat until submission confirmed:

**A. Snapshot + first `check_required_fields.js`**
```bash
SNAP=$(openclaw browser --browser-profile $OPENCLAW_PROFILE snapshot \
  --target-id $TARGET_ID --limit 500 --efficient)
CHECK=$(openclaw browser --browser-profile $OPENCLAW_PROFILE evaluate \
  --target-id $TARGET_ID --fn "$(cat "$CHECK_FIELDS_JS")")
```

Returns `{"unfilled":[...],"filled":[...]}`. Generate script only for fields in `unfilled`.

**B. Generate fill script**
Write to `/tmp/fill_<timestamp>.sh` using `exec` + heredoc (never the `write` tool):
```bash
TS=$(date +%s)
SCRIPT="/tmp/fill_${TS}.sh"
cat > "$SCRIPT" << 'SCRIPT_EOF'
# script body here
SCRIPT_EOF
chmod +x "$SCRIPT" && bash "$SCRIPT"
```

Script structure:
1. Tab validation (snapshot, check for "tab not found")
2. Snapshot for fresh refs — never reuse refs across page loads
3. `fill` for text fields (batch all at once)
4. `select` for dropdowns (A-type: direct; B1: open+snap+click; B2: type+snap+click)
5. `upload` before clicking upload button (arm interceptor first)
6. Second `check_required_fields.js` — must pass before any page navigation

**C. Advance page**
Only after second check passes:
- Has `Submit` → all fields filled → submit
- Has `Next`/`Continue` → current page done → advance and loop
- Neither → report error, wait for human

### 6. Submission verification

Both conditions must be true:
1. `document.querySelector('button[type="submit"]') === null`
2. Page contains "Success" / "Application received" / "We have received your application"

Do NOT accept "Thank you for applying" as success.

### 7. Update tracker and report
- Success → `applied`, record submission date
- Failed/skipped → `error`, record reason
- Report result immediately after each job

### 8. Update platform knowledge base
After each job (success or failure):
1. Note any new form quirks, unusual labels, dynamic components
2. Append to `~/.openclaw/platform/<platform>/quirks.md`:
```bash
echo "" >> ~/.openclaw/platform/<platform>/quirks.md
echo "## <FieldName> [$(date +%Y-%m-%d)]" >> ~/.openclaw/platform/<platform>/quirks.md
echo "**Behavior**: ..." >> ~/.openclaw/platform/<platform>/quirks.md
echo "**Fix**: ..." >> ~/.openclaw/platform/<platform>/quirks.md
```
3. Add stable dropdown values to `~/.openclaw/platform/<platform>/dropdowns.sh`
4. If no new issues, note "no new quirks" explicitly

## Helper functions for snapshot parsing

```bash
get_ref()       { echo "$1" | grep -F "\"$2\""  | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1; }
get_ref_fuzzy() { echo "$1" | grep -iE "$2"      | sed 's/.*\[ref=\([^]]*\)\].*/\1/' | head -1; }
count_label()   { echo "$1" | grep -cF "\"$2\""; }
```

Never use `jq` on snapshot output. Never use `grep -o 'ref=\K...'`. Never reuse refs across page loads.

## Dropdown strategy

| Type | When | Strategy |
|------|------|----------|
| A — known options | Yes/No/known enum | `select "<value>"` → fallback: open+snap+click |
| B1 — short list (<20) | Company, state | open+snap+click with 0.5s sleep for animation |
| B2 — search-driven | School, discipline | click to open → `type` keyword → 0.5s sleep → snap → click result |

Only use fuzzy matching for unknown dropdown values. Known buttons/labels always use exact match.

## Dynamic components

Work history and education sections usually require clicking "Add" per entry. After each click, re-snapshot before extracting refs — new components get new refs.

## File upload sequence

Always: `upload <path>` first (arms the interceptor), then click the upload button. Never reverse this order. After page refresh, re-snapshot before clicking upload.

## EEOC defaults

Read from config: `$USER_GENDER`, `$USER_RACE`, `$USER_HISPANIC`, `$USER_VETERAN`, `$USER_DISABILITY`, `$USER_WORK_AUTH`, `$USER_NEED_SPONSOR`.

## Cover letter

Always fill cover letter text fields, even when marked optional. Read content from the `.docx` file using python-docx, not from the file path.

## Script safety rules

1. All page-state-changing actions go in scripts — no direct model calls
2. Never use JS injection; use `fill`/`type` instead
3. Script comments use `#` only — no em-dashes or special chars
4. Single exit point: find ref → on failure write to ERRORS → on success execute
5. Unique-label check before acting: `count_label "No"` etc. must return 1
6. Config paths use variable: `source "$HOME/.openclaw/users/${OPENCLAW_USER}/config.sh"`
7. File copy with error capture: `if ! cp "$SRC" "$DST"; then ERRORS+=("copy failed"); fi`
8. Dynamic components: click parent to trigger render → sleep 0.3 → re-snapshot → extract ref

## Tracker status flow

```
resume_ready → applied
            ↘ error
            ↘ wrong_url
```

## Support

If Job Autopilot saved you time: paypal.me/ZLiu308
