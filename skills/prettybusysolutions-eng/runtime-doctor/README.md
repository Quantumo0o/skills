# Runtime Doctor

Runtime Doctor is a small local utility for diagnosing OpenClaw runtime and config drift before you start poking at files blindly.

I wrote it after wasting too much time on vague gateway state, broken config, and sessions that looked dead for unclear reasons.

## What it does
- checks a few core runtime/state surfaces
- writes a local diagnosis report
- stays non-destructive
- is safe to rerun

## Why use it
When OpenClaw feels broken, half the battle is figuring out whether the local state is coherent before you start "fixing" things that are not actually the problem.

## Files
- `runtime_doctor.py` — local diagnostic script
- `SKILL.md` — skill wrapper / usage context
- `LICENSE`
- `CONTRIBUTING.md`

## Usage
```bash
python3 runtime_doctor.py
```

That writes a local `runtime-doctor-report.json` in the current working directory.

## Safety
- no destructive actions
- no secret embedding
- no outbound network behavior in the script
- report generation only

## Upgrade to Pro
The free version handles the obvious checks.
The Pro version is for when the environment is messy and you need to save 5+ hours of debugging instead of guessing your way through runtime drift.

Pro is intended to include:
- deeper config drift diagnosis
- likely root-cause explanations
- backup-first repair plans
- prioritized next actions
- richer diagnostic output for real broken environments

Stripe Payment Link:
- https://buy.stripe.com/4gM28q7W0agjbg4bkG0kE06

## Support
If the free version helped, great. If you want the deeper version that saves real debugging time, the Pro path is there for that.
