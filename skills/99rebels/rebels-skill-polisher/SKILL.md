---
name: skill-polisher
description: >
  Polish a skill's SKILL.md for ClawHub readability without sacrificing LLM effectiveness.
  Use when improving a skill's listing, making a skill look better on ClawHub, or preparing
  a skill for publish. Rewrites SKILL.md with better formatting, then audits the changes
  to ensure nothing the LLM needs was lost. Moved content goes to references/ — never deleted.
---

# Skill Polisher 🪚

Improve a skill's SKILL.md for ClawHub readability. Run after the skill is built and tested — never before.

## Priority Order

1. **LLM execution** — the agent must still be able to do the task correctly
2. **Triggering** — the skill must still activate on the right queries
3. **ClawHub display** — browsers should understand the skill at a glance

Readability supports these goals. Never sacrifice clarity for aesthetics.

## How It Works

```
1. Read the existing SKILL.md
2. Rewrite for readability (apply rules from references/)
3. Audit the rewrite against the original
4. Output: polished SKILL.md + audit report + any new reference files
```

## Before Polishing

Ensure the skill is:
- ✅ Functionally working (scripts tested)
- ✅ Validated (`quick_validate.py` passes)
- ✅ Description is correct (triggers on the right queries)

If any of these fail, fix them first. Don't polish a broken skill.

## Polishing Rules

Read [references/rules.md](references/rules.md) for the full set of formatting rules.

Key principles:
- Short paragraphs (1-2 lines) — dense blocks kill readability
- Code blocks for lists — renders as visual boxes on ClawHub
- Emoji as section anchors — 🔒 📊 ⚡ give instant visual context
- One code block per concept — not three variations for three platforms
- "Why" and "When to Use" sections — help browsers understand value

## What Gets Moved to references/

Content that's valuable but doesn't belong in the storefront:

- Platform-specific formatting examples (Slack, WhatsApp, Discord)
- Detailed credential setup tutorials
- Implementation notes (API rate limits, edge cases, gotchas)
- Extended configuration reference
- Historical changelogs

**Rule: Content is moved, never deleted. Every reference file must be valid and useful.**

## The Audit

After rewriting, compare the original against the polished version. Flag:

```
⚠ Potentially risky changes:
• Security notes removed
• Credential instructions lost
• Implementation details dropped without a reference file
• Trigger phrases removed from description
• Reference files created but empty or incomplete
```

See [references/audit-guide.md](references/audit-guide.md) for the full audit checklist.

## Output

Present three things to the user:

1. **The polished SKILL.md** — ready to review
2. **Any new reference files** — created from moved content
3. **Audit report** — what changed, what was moved, anything flagged

Wait for user approval before overwriting the original.

## When to Use

- "Make this skill look better on ClawHub"
- "Polish my SKILL.md"
- "Improve this skill's listing"
- "Ready to publish, but clean it up first"

## Not a Replacement for skill-creator

This skill polishes existing skills. Use the built-in `skill-creator` to build skills from scratch. Polish after building, not during.
