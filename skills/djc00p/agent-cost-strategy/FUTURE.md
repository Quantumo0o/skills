# Future Enhancements (Pull Request Ideas)

## Pending v2 Updates (from claude-api-cost-optimizer review)

- ~~**Cache write vs read cost math**~~ ✅ Done — added to `references/cache-optimization.md` with break-even formula
- ~~**Batch API**~~ ✅ Done — added to SKILL.md and cache-optimization.md

---

Local workflow integrations to consider upstream:

- **Auto-escalate model tier when context swells** — Track injected context size per message; if >200K tokens detected, suggest switching from Sonnet → Haiku or recommend context pruning (integration with `ontology` and `problem-solving-methodology` for root cause analysis).

- **Cross-skill cost logging via mmlog with parseable tags** — When routing a decision or delegation occurs, emit structured cost-decision logs (`mmlog --tags cost:routing,model:haiku,expected-savings:40%`) so patterns can be analyzed across sessions and fed back to `self-improving-agent`.

- **Cache TTL alignment heartbeat template** — Pre-generate a `HEARTBEAT.md` snippet that maintains Anthropic cache warmth at optimal intervals based on detected provider (parse `openclaw.json` to recommend 55min for API key vs. 30min for OAuth).

- **Sub-agent model selection automation** — When spawning a sub-agent, parse the task description and auto-suggest model tier (e.g., "fix failing tests" → Haiku, "write architecture doc" → Opus) via integration with a lightweight task classifier.

- **Cost forecast per workspace file** — Analyze which SOUL.md, MEMORY.md, and memory/* files contribute most to context bloat each session; generate a `references/cost-attribution.md` showing token cost per file and suggesting which could be lazy-loaded without functionality loss.

Status: Prototype in local workspace; ready for contribution when time permits.
