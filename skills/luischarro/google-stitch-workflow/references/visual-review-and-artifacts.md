# Visual Review And Artifacts

Use this reference when a Stitch session has multiple candidate screens or
needs a clearer operator trail between prompt, result, and implementation.

## Visual review loop

After each `generate_screen_from_text` or `edit_screens` call:

1. inspect the returned screen metadata
2. review the current screenshot or other visual artifact when available
3. decide whether the result is:
   - `accepted`
   - `candidate`
   - `rejected`
4. record the decision before issuing another large prompt

Do not let the session drift through several edits without visual confirmation.

## Screen selection rule

When more than one candidate screen exists:

- identify each screen in human terms, not only by ID
- nominate one canonical target before further edits
- record the exact screen ID that later implementation should follow

## Revision checkpoint contents

One local checkpoint folder per accepted revision is usually enough.

Capture:

- prompt text
- project ID
- screen ID
- screenshot URL when present
- HTML reference when present
- timestamp
- one-line note such as `accepted`, `candidate`, or `rejected`

Keep this lightweight. The goal is traceability, not a heavy local state
system.

## Artifact naming

Prefer short stable names:

- `home-canonical`
- `paywall-v2`
- `settings-profile`
- `dashboard-mobile-primary`

Attach the alias to the latest accepted screen, but do not treat aliases as a
replacement for real Stitch identifiers.

## Before export or code translation

Do not move to implementation from prompt text alone.

Confirm:

- which visually reviewed screen is canonical
- which exact screen ID implementation should follow
- whether the current screen is accepted or still exploratory
