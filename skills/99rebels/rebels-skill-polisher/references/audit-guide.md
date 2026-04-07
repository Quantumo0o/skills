# Audit Guide

Compare the original SKILL.md against the polished version. Flag anything that could hurt LLM effectiveness.

---

## Audit Checklist

Run through these checks after every polish. Flag anything that fails.

### Description (frontmatter)

- [ ] Trigger phrases preserved or improved
- [ ] No trigger phrases removed
- [ ] Still under 1024 characters
- [ ] Credentials still mentioned (if required)
- [ ] Uses imperative phrasing

### Security

- [ ] Security notes preserved (moved to references/ is OK, deleted is NOT)
- [ ] Credential instructions still accessible
- [ ] Token storage location still mentioned
- [ ] No permissions broadened or narrowed without noting it

### LLM Execution

- [ ] Exact commands still provided (file paths, flags, arguments)
- [ ] Config file locations still mentioned
- [ ] Dependencies still listed
- [ ] Setup steps still complete (not shortened to the point of being unusable)
- [ ] Error handling guidance preserved (or moved to references/)

### Content Accounting

- [ ] Nothing deleted without a reference/ home
- [ ] Every reference/ file created is non-empty and useful
- [ ] Every reference/ file is linked from SKILL.md
- [ ] No broken references (file mentioned but doesn't exist)
- [ ] No duplicate content (same info in SKILL.md AND references/)

### Formatting

- [ ] No dense paragraphs (max 2 lines)
- [ ] Lists use code blocks where appropriate
- [ ] Tables have 3 columns max, short cells
- [ ] Sections have clear headings
- [ ] Output example included (if skill produces user-facing text)

## Audit Report Format

Present the audit as:

```
📊 Audit Report

✅ Safe changes:
• Commands table → code block (formatting only)
• Credential section compressed (content preserved)

📦 Content moved to references/:
• Platform formatting → references/formatting.md
• Setup tutorial → references/setup.md

⚠ Flagged:
• Security note about plaintext storage was removed → MOVED TO REFERENCES/NOTES.MD
• API rate limit note was dropped → ADDED TO NOTES SECTION
```

Be specific. Name exactly what was moved and where. Don't say "some notes were moved" — say "the API rate limit note was moved to references/notes.md."

## What to Flag vs What's Safe

**Safe to change:**
- Dense paragraphs → short paragraphs
- Bullet lists → code blocks
- Markdown tables → code blocks
- Long setup steps → compressed code block
- Repeated info → consolidated

**Flag as potentially risky:**
- Any security note removal
- Any credential instruction removal
- Any command path change
- Any dependency removal
- Any trigger phrase removal
- Content removed without a reference/ destination
