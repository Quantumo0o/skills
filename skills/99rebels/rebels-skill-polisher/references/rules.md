# Polishing Rules

Formatting rules for making SKILL.md files look great on ClawHub. Apply these when polishing.

---

## Structure

Follow this order. Every section earns its place.

```
Frontmatter (name + description + homepage)
│
├── One-line hook (bold) — what it does
├── Why (2-3 lines) — context before the how-to
├── When to Use (bullet list) — trigger phrases for browsing
├── Setup (minimal, one code block)
├── Commands / Workflow (code block or short table)
├── Output Example (one clean code block)
├── Credentials / Dependencies (brief)
└── Notes (implementation details, only if needed)
    └── Deep detail → references/
```

## Frontmatter

```yaml
---
name: skill-name
description: >
  What it does. When to trigger it. One to three sentences max.
homepage: https://github.com/owner/repo  # if available
---
```

Rules:
- `name`: lowercase, hyphens, under 64 chars
- `description`: under 1024 chars, imperative phrasing, include trigger phrases
- `homepage`: link to source repo (helps ClawHub trust score)

## Short Paragraphs

One idea per paragraph. Two lines max.

Bad example:
```
The setup process requires you to first obtain a GitHub Personal Access Token
by navigating to github.com/settings/tokens, creating a new fine-grained token
with public repository read-only access, and then passing it to the setup command
which will save it to your credentials directory for future use.
```

Good example:
```
Create a GitHub fine-grained PAT with public repo read access.

Run `setup --token <TOKEN>` to save it for future use.
```

## Code Blocks for Lists

Renders as visual boxes on ClawHub. Use for checklists, reference lists, and examples.

Bad example:
```
Priority rules:
- HIGH: Sender domain matches config
- MEDIUM: Gmail-labeled personal
- LOW: Everything else
```

Good example:
```
Priority Rules:
🔴 HIGH   → Sender domain matches config
🟡 MEDIUM → Gmail-labeled personal
🟢 LOW    → Everything else
```

## Emoji as Anchors

Use consistently, one per section. Not decoration — navigation.

- 🔒 Security
- 📊 Data/analytics
- ⚡ Automation
- 📧 Email/messaging
- 🚨 Warnings
- ✅ Safe/approved
- ⚠️ Cautions
- ❌ Rejected

## Tables: Keep Them Tight

3 columns max. Short cell content. If it's wrapping, use a code block instead.

## One Code Block Per Concept

Not three variations for three platforms. Pick the best default. Move alternatives to references/.

## "Why" Section

2-3 lines explaining why someone would want this. Makes the skill immediately understandable to browsers.

## "When to Use" Section

4-6 bullet points with natural trigger phrases. How would a user actually ask for this?

```
- "Check my repo stats"
- "How's my project doing?"
- "Give me a growth digest"
```

## Output Example

Show what the skill produces. One clean example. Proves it works.

## Format Output Guidance

One sentence max in SKILL.md:

```
Format output for the current channel — adapt formatting to match what the platform supports.
```

Only include this when the skill delivers text to a user channel. Skip for skills that only modify files or run commands silently.

## What to Move to references/

Move, don't delete:

| Content | Destination |
|---------|------------|
| Platform-specific formatting | `references/formatting.md` |
| Detailed credential setup | `references/setup.md` |
| Extended config reference | `references/configuration.md` |
| Implementation notes | `references/notes.md` or brief Notes section |
| API details / error handling | `references/api.md` |

Every moved file must be valid, properly formatted, and referenced from SKILL.md.
