# CLAUDE.md

## Keep SKILL.md and AGENTS.md in sync

`SKILL.md` (Claude Code) and `AGENTS.md` (other agent runtimes) are parallel entry points for the same skill and must stay in sync in content and structure. Any substantive change to one must be mirrored in the other in the same commit — including the frontmatter/description, opening "Two APIs" paragraph, Quick Start, Key Rules, Core Patterns, Reference Documentation list, and CLI Commands. Format differences are fine (e.g., SKILL.md has YAML frontmatter, AGENTS.md has a `<!-- version: -->` comment), but the meaning, ordering, and coverage must match. If a section exists in one file, it should exist in the other unless there's an explicit reason it doesn't apply.

## Version bumping

Only bump the skill version **once, at the very end** of a change — after all edits are finalized and the user has confirmed they're done. Do not bump mid-change, do not bump after each individual edit, and do not bump speculatively. If the user is still iterating, hold off.

When bumping at the end, update all four places in the same commit:

1. `CHANGELOG.md` — add a new version entry at the top with a summary of changes
2. `SKILL.md` — update the `version:` field in the frontmatter metadata
3. `AGENTS.md` — update the `<!-- version: x.x.x -->` comment
4. `.claude-plugin/plugin.json` — update the `"version"` field
