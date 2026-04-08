# Heartbeat And Browser Notes

Use this file when the task involves live browser automation and progress monitoring.

## Browser Constraints

- Use the installed Google Chrome application directly.
- Prefer the currently open Chrome window.
- Open additional tabs in the same window instead of creating a new window.
- Keep navigation linear enough that the user can observe progress if they look at the browser.

## OpenClaw Monitoring

Enable heartbeat before the run:

```bash
openclaw system heartbeat enable
```

## Failure Handling

- If heartbeat enable fails, continue and report the failure.
- If LinkedIn blocks or rate-limits, slow down, capture the blocker in `notes`, and move to the next viable company after a reasonable retry.
- If the website is inaccessible, record the failure and continue to Google Maps email fallback only when the company identity is still trustworthy.
