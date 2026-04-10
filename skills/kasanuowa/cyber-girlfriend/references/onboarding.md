# Onboarding Flow

Use this when a user wants to install or configure the skill from scratch on OpenClaw.

## Goal

Make setup easy for a smart agent that can read `SKILL.md` directly:
- ask only the minimum useful questions
- default to a good starter profile when the user has no strong preference
- separate config from cron from testing
- avoid treating the current session as the delivery target; proactive outbound delivery follows the local config's `delivery` block

## Recommended Conversation Order

## Fast Decision Tree

Use this tiny decision tree before asking lots of follow-up questions:

- If the user says “make it like your current setup” / “先给我一套能跑的” / has no strong opinion:
  - choose **Recommended Starter Profile**
- If the user already knows the time slots or wants unusual labels/times:
  - choose **Custom Schedule**
- If the user only wants one or two proactive touchpoints:
  - choose **Minimal Profile** (custom schedule with very few modes)
- If the user wants more spontaneous nudges between named schedule slots:
  - enable **`heartbeat`**
- If the user is sensitive to interruptions:
  - disable `heartbeat` first, then tighten quiet hours / cooldown / daily limit

### Step 1 — Confirm destination

Ask for or infer:
- `delivery.channel`
- `delivery.owner_target`
- `delivery.account` when the channel needs it

If the user already has a working owner DM channel in the current workspace, reuse that instead of re-asking.

### Step 2 — Ask profile choice

Offer two choices:
1. **Recommended starter profile**
2. **Custom schedule**

Also keep one lightweight fallback in mind:
- **Minimal profile** = fewer slots, same architecture

If the user says “make it like your current setup” or has no strong preference, use the recommended starter profile.

## Recommended Starter Profile

Default mode set:
- `morning`
- `afternoon`
- `evening`
- `night`
- optional `heartbeat`

Default interpretation:
- `morning`: light good-morning / weather-aware nudge
- `afternoon`: small brief or topical share
- `evening`: casual check-in or selfie / what-I’m-doing vibe
- `night`: soft wrap-up / gentle goodnight
- `heartbeat`: lightweight spontaneous ping outside the named schedule slots

These are examples, not product limits.

## Minimum Config Questions

Ask only these first:
- Which channel should proactive messages use?
- What owner target/account should delivery use?
- Starter profile or custom schedule?
- Quiet hours?
- Cooldown?
- Daily limit?
- Enable `heartbeat` or not?

Do not force users to decide advanced style variants up front.

## Suggested Build Sequence

1. Create/update local config.
2. Verify delivery fields are correct.
3. Choose starter vs custom.
4. Create the live cron jobs.
5. Dry-run one mode.
6. Confirm the user-visible message reaches the intended channel.
7. Only then refine wording and personality details.

For the default four-slot setup, use [cron-blueprints.md](./cron-blueprints.md). If the reader needs copy-pasteable OpenClaw cron job objects instead of prompt-only blueprints, use [live-cron-templates.md](./live-cron-templates.md).

## Starter Cron Blueprint

The exact cron payload text may vary by workspace, but the shape should stay consistent. For concrete OpenClaw `jobs.json`-style starter templates, see [live-cron-templates.md](./live-cron-templates.md).

For each mode:
1. call `companion_ping.py <mode> --config ...`
2. stop quietly if it returns `skip`
3. continue with the richer per-mode behavior if it returns `ok`
4. send the proactive message via the config's `delivery` target
5. only after successful delivery, call `companion_ping.py <mode> --config ... --mark-sent`

## Custom Mode Guidance

If the user wants custom modes:
- allow any mode label
- allow any cron time
- reuse the same handler shape
- add `behavior.mode_profiles.<mode>` only if the user wants mode-specific style/content hints

Examples of valid custom labels:
- `lunch`
- `commute`
- `weekend`
- `post-meeting`
- `late-night`

## Anti-Patterns

Do not:
- hardcode one channel in the skill logic
- reply into whichever session happened to receive the system wakeup
- store full cron payload text in local config
- update cooldown state before the user-visible message is actually delivered
- force every user into the four-slot profile if they clearly want something custom
