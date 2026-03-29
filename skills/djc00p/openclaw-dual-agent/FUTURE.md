# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Automatic workload balancing between agents** — Monitor cost/latency per agent over time; if free agent (OpenRouter) consistently performs well on certain task types (e.g., data parsing, simple rewrites), auto-route future similar tasks there; log routing decisions to mmlog for pattern analysis (pairs with `agent-cost-strategy`).

- **Unified memory bridge** — Share selected ontology entities (Projects, Tasks, Events) between agents via `memory/ontology/graph.jsonl`; allow paid agent to delegate work to free agent by creating Task entities with explicit requirements, free agent processes and updates status.

- **Separate notification channels for dual output** — Route paid agent responses to primary Telegram chat, free agent responses to secondary chat or thread; user reviews both and picks which response to act on; log quality comparison to help refine workload distribution.

- **Health check and failover automation** — Monitor OpenRouter API status and response latencies; if latencies exceed threshold, automatically failover to paid agent (Anthropic); log all failovers to `memory/episodic/` with reason and recovery metrics.

- **Cost reconciliation dashboard** — Aggregate token usage from both agents across accounts/billing profiles; generate monthly reconciliation report showing cost split, per-agent efficiency, and recommendations for model/provider adjustments (pairs with `token-optimizer` for cross-agent savings analysis).

Status: Prototype in local workspace; ready for contribution when time permits.
