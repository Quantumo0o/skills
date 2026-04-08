---
name: linkedin-company-scout
description: Collect company intelligence for sourcing or research by automating Google Chrome against LinkedIn, company websites, and Google Maps. Use when Codex needs to gather non-China companies for one or more industry keywords, extract a strict set of company profile fields, find contact email addresses with source attribution, enforce per-keyword quotas, and keep long-running collection work observable with OpenClaw heartbeat monitoring.
---

# LinkedIn Company Scout

Collect company profiles in a repeatable way when the user wants lead discovery or market scanning from LinkedIn first, then enrichment from official websites and Google Maps.

Read [references/output-schema.md](./references/output-schema.md) before collecting. Read [references/heartbeat-and-browser.md](./references/heartbeat-and-browser.md) before opening the browser or starting a long run.

Run [run_linkedin_company_scout.py](./scripts/run_linkedin_company_scout.py) when the task is a straight collection run and the environment is macOS with Google Chrome plus Selenium available.

Run [run_full_pipeline.py](./scripts/run_full_pipeline.py) when the user wants the full automation chain:
- data mining
- email sending (skip already successful sends)
- dashboard data refresh

## Workflow

1. Normalize the request.
2. Prepare heartbeat and browser session.
3. Collect candidate companies from LinkedIn.
4. Enrich each company from its official website.
5. Fallback to Google Maps for email only when the official site does not expose one.
6. Produce a structured result with source attribution and gap notes.

## Normalize The Request

- Use the user's keywords exactly unless they ask for expansion.
- Treat each keyword as an independent collection bucket.
- Default target count to `5` companies per keyword unless the user specifies another number.
- Exclude companies whose operating location is in China, whose LinkedIn location is China, or whose website clearly shows China-only presence.
- Prefer one row per unique company. Deduplicate across keywords, but keep the matched keyword on each retained row.
- If one company matches multiple keywords, keep separate output rows only when the user explicitly wants overlap preserved. Otherwise keep the strongest keyword match and note the dropped keyword matches.

## Prepare Heartbeat And Browser Session

- Use the normal installed Google Chrome application, not an embedded browser and not a freshly created separate automation window.
- Prefer the current Chrome window after attachment. The bundled script launches Chrome with a remote debugging port only when needed, then continues work in tabs under that real Chrome session.
- The bundled script stops only the automation driver on exit. It does not intentionally close the user's Chrome session.
- Before starting collection, enable OpenClaw heartbeat:
```bash
openclaw system heartbeat enable
```
- If heartbeat commands fail, continue the collection task but mention that monitoring could not be enabled.
- If LinkedIn is not already logged in inside the automation profile, allow a manual login pause, then resume the scripted run.

## Run The Script

Use this command for the common case:

```bash
python3 /Users/m1/.codex/skills/linkedin-company-scout/scripts/run_linkedin_company_scout.py \
  --keywords "industrial design,hardware design,smart wearable" \
  --count 5 \
  --output-dir /Users/m1/Documents/Playground/linkedin-company-scout-output
```

Use this command when the user wants deep collection such as 100 companies per keyword with pagination:

```bash
python3 /Users/m1/.codex/skills/linkedin-company-scout/scripts/run_linkedin_company_scout.py \
  --keywords "industrial design,hardware design,smart wearable" \
  --count 100 \
  --max-search-pages 20 \
  --output-dir /Users/m1/Documents/Playground/linkedin-company-scout-output-100
```

Useful flags:

- `--no-heartbeat`: skip OpenClaw heartbeat enablement
- `--chrome-profile-dir <path>`: keep a dedicated Chrome profile with a persistent LinkedIn login
- `--debug-port <port>`: change the Chrome debugging port if `9222` is occupied
- `--linkedin-wait-seconds <n>`: allow more time for manual login
- `--max-search-pages <n>`: scan additional LinkedIn result pages when one page is not enough

## Full Pipeline (Mining + Email + Dashboard)

Use this one command when the user asks for complete execution flow:

```bash
python3 /Users/m1/.codex/skills/linkedin-company-scout/scripts/run_full_pipeline.py \
  --keywords "industrial design" \
  --count 200 \
  --output-dir /Users/m1/Documents/Playground/linkedin-company-scout-output-industrial-200-verified \
  --db-path /Users/m1/Documents/Playground/linkedin-company-scout-output-industrial-200-verified/results.db \
  --max-search-pages 400 \
  --no-heartbeat \
  --send-email \
  --send-backend imap-smtp-email \
  --smtp-password "<SMTP_PASSWORD>" \
  --refresh-dashboard
```

Key behavior:
- Email phase defaults to **not** passing `--allow-resend`, so records with `status='sent'` in prior campaigns are skipped.
- Email template is persisted as `通用模版` in template DB.
- Push logs include send timestamp + content snapshot in campaign DB and source DB history table.
- Dashboard refresh regenerates `linkedin-dashboard/dashboard-data.js`.

Expected outputs:

- `linkedin_company_scout_results.json`
- `linkedin_company_scout_results.csv`
- `run_metadata.json`

## Collect From LinkedIn

- Search LinkedIn for companies related to the current keyword.
- Prefer actual company pages over posts, people, jobs, schools, or groups.
- Accept a company only after confirming all required profile fields can be filled or marked as unavailable with a reason.
- Capture these fields from LinkedIn whenever available:
  - company name
  - company website
  - company summary or about text
  - industry
  - location
  - LinkedIn URL
  - matched keyword
- Keep the company only if the location is outside China.
- If LinkedIn does not expose the website but the company page clearly references an official domain elsewhere, use the official domain and note that the website came from a nonstandard LinkedIn surface.

## Enrich From Official Website

- Visit the official website for each accepted company.
- Search obvious contact surfaces first: `Contact`, `About`, `Footer`, `Legal`, `Imprint`, `Support`, `Team`.
- Capture one or more email addresses when present.
- If multiple emails exist, prefer the most general business contact such as `hello@`, `info@`, `contact@`, `support@`, or a departmental email clearly relevant to external inquiries.
- Record the email source as `official_website`.
- If no email is visible, note the checked page or section so the absence is auditable.

## Fallback To Google Maps For Email

- Only use Google Maps when the official website did not yield any email address.
- Search by exact company name plus location to reduce mismatches.
- Confirm the listing is the same business before taking contact details from it.
- Capture an email only when it is explicitly displayed on the listing or clearly reachable through the listing's surfaced contact details.
- Record the email source as `google_maps`.
- If Google Maps also has no usable email, leave the email field blank and set the email source to `not_found`.

## Output Rules

- Return results in a structured table or JSON using the schema in [references/output-schema.md](./references/output-schema.md).
- Every accepted row must include:
  - `keyword`
  - `company_name`
  - `company_website`
  - `company_intro`
  - `industry`
  - `location`
  - `linkedin_url`
  - `email`
  - `email_source`
- Do not omit required fields. If a field cannot be found, leave it empty and add a brief note in `notes`.
- Maintain exactly 5 accepted companies per keyword when possible. If fewer than 5 valid non-China companies are found, report the shortfall clearly.
- Keep source attribution concise and explicit. Valid values are `official_website`, `google_maps`, or `not_found`.

## Quality Bar

- Prefer companies with enough public information to fill the profile cleanly.
- Avoid agencies, stealth entities, duplicate subsidiaries, and irrelevant firms unless the keyword space is sparse.
- Do not infer an email address from a pattern such as `firstname@domain.com` unless the exact address is shown publicly.
- Do not fabricate industries, locations, or descriptions. Use the public wording when available, otherwise summarize faithfully.
- When summarizing a company intro, keep it short and factual.
- Respect site friction. If LinkedIn presents a login wall, checkpoint, or anti-bot screen, slow down and continue only after the user session is valid.

## Deliverable Format

- Provide one result block per keyword followed by a combined summary.
- For each keyword, state:
  - accepted company count
  - rejected or skipped count if material
  - any shortfall against the target of 5
- Include a final note on whether OpenClaw heartbeat monitoring was enabled successfully.
