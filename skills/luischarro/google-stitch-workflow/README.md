# Google Stitch Workflow

Disciplined OpenClaw skill bundle for using Google Stitch through the verified MCP surface.

## At a glance

- MCP-first: separates verified MCP actions from browser-only Stitch features
- practical: optimized for project inspection, screen generation, controlled edits, and redesign iteration
- cautious: emphasizes parameter discipline, visual review, and failure recovery

## Best for

- inspecting Stitch projects and screens before editing
- generating one screen at a time from a structured prompt
- refining generated screens with small preservation-oriented edits
- redesigning existing app screens from reliable references
- deciding when to stay in Stitch and when to move to code

## Not for

- direct production UI implementation
- pixel-perfect code-side fixes
- whole-product planning in one giant prompt
- blind reliance on browser-only Stitch features through MCP

## Quick start

1. Read [`SKILL.md`](./SKILL.md).
2. Inspect the project and target screen before editing.
3. Generate one screen or make one small edit.
4. Review the visual result immediately.
5. Move to code only after one canonical screen direction is accepted.

## Included files

- [`SKILL.md`](./SKILL.md): main operating instructions
- [`references/prompt-structuring.md`](./references/prompt-structuring.md): prompt shaping and repair
- [`references/visual-review-and-artifacts.md`](./references/visual-review-and-artifacts.md): review and traceability guidance
- [`references/redesign-prompt-patterns.md`](./references/redesign-prompt-patterns.md): redesign-oriented prompt patterns
- [`references/local-workflow-conventions.md`](./references/local-workflow-conventions.md): optional aliases, artifacts, and history conventions
- [`CHANGELOG.md`](./CHANGELOG.md): published version notes
- [`PUBLISHING.md`](./PUBLISHING.md): publish workflow for future releases

## Publishing

This folder is a self-contained ClawHub skill bundle.

Typical command from the repo root:

```bash
clawhub publish ./publish/google-stitch-workflow --slug google-stitch-workflow --name "Google Stitch Workflow" --version 1.1.0 --tags latest
```

## License

Released under the MIT License. See [`LICENSE`](./LICENSE).
