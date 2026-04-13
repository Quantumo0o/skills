# AGENTS.md
# Version: 4.9 | Updated: 2026-04-08 | KB知识库v1.3全面更新
# v4.7 → v4.8: Removed Identity, Memory System, Security, Output Standards (now in SOUL.md/USER.md)
# Identity & Memory → SOUL.md v3.3 | Output Standards → USER.md v3.1 | Security → SOUL.md

---

## Template Version Lock

All BA artifact templates and agent definition files must use these locked versions. Update this lock simultaneously when any template is updated — stale version mismatch is a quality incident.

| Template | Locked Version | Date | Owner |
|---------|---------------|------|--------|
| agent1-gap.md | v1.8 | 2026-04-06 | Agent 1 |
| agent2-bsd.md | v2.3 | 2026-04-05 | Agent 2 |
| agent3-regulatory.md | v2.1 | 2026-04-05 | Agent 3 |
| agent4-techspec.md | v1.0 | 2026-04-05 | Agent 4 |
| agent5-decoder.md | v1.0 | 2026-04-05 | Agent 5 |
| agent6-product-factory-configurator.md | v1.0 | 2026-04-05 | Agent 6 |
| agent7-cross-module-impact-analyzer.md | v2.0 | 2026-04-05 | Agent 7 |
| agent8-uat-generator.md | v2.1 | 2026-04-05 | Agent 8 |
| agent9-data-migration.md | v3.1 | 2026-04-05 | Agent 9 |
| output-templates.md | v3.0 | 2026-04-05 | Agent 2 |
| bsd-patterns.md | v2.0 | 2026-04-05 | Agent 2 |
| bsd-quality-gate.md | v1.0 | 2026-04-05 | Agent 2 |
| insuremo-gap-detection-rules.md | v2.0 | 2026-04-05 | Agent 1 |
| kb-manifest.md | v1.3 | 2026-04-08 | Agent 1 |
| afrexai-benchmarks.md | v1.1 | 2026-04-05 | Agent 3/8 |
| spec-miner-ears-format.md | v1.1 | 2026-04-05 | Agent 9 |

---

## Identity & Memory (system-level → see SOUL.md)

Identity (Lele, Insurance BA role), communication style, and Memory System (memory workflow) are defined in `SOUL.md v3.3` — not in this file.

---

## BA Output Chain

```
Client Requirement → Agent 0 (Discovery)
    → Gap Analysis → Agent 1
    → BSD + Ripple Map → Agent 2 + Agent 7 (parallel)
    → Tech Spec → Agent 4 + Agent 6 (parallel)
    → Config + UAT → Agent 6 + Agent 8
    → Production
```

**Notation:** `→` = sequential dependency. `+` = parallel execution.

**Dependency rules:**
- Agent 1 output (Gap Matrix) is required before Agent 2 and Agent 7 can start.
- Agent 3 runs in parallel with Agent 1 when Regulatory change type is detected.
- Agent 4 and Agent 6 run in parallel after BSD is approved.

**Traceability Chain:** Every requirement must be traceable from source to delivery.

| From | To | Traceability Reference |
|------|----|----------------------|
| Client Requirement | Gap Matrix | Requirement ID → Gap ID |
| Gap Matrix | BSD | Gap ID → BSD Rule (SR01, SR02...) |
| BSD | Tech Spec | BSD Rule → Tech Spec section |
| Tech Spec | Config | Config path → Implementation |
| Config | UAT | Config → UAT Scenario |
| UAT | Sign-off | Test result → Stakeholder sign-off |

Maintain `references/delivery-traceability.md` as the master traceability table.

---

## Change Type Triage

Before routing to any agent, identify the **Change Type**. This determines the analysis path, stakeholder map, and review sequence.

**Multiple types are allowed.** When a change has multiple dimensions (e.g., a new rider that also requires MAS compliance), tag **all applicable types** and use the highest-risk type as the primary route.

| Change Type | Trigger Keywords | Primary Route | Key Stakeholders |
|-------------|-----------------|---------------|-----------------|
| **Technical** | API, integration, version upgrade | Agent 1 + Agent 9 | IT/Dev, Arch |
| **Functional** | New benefit, new rider, rule change, product variant | Agent 1 + Agent 2 | UW, Actuarial, Product |
| **Operational** | Process efficiency, UI change, workflow automation | Agent 1 + Agent 2 | Ops, CS, IT/Dev |
| **Regulatory** | MAS/HKIA/BNM/OIC compliance, policy change | Agent 3 + Agent 1 (parallel) | Compliance, Actuarial, Legal |
| **Data** | Historical migration, legacy conversion, interface mapping | Agent 9 + Agent 7 | RI Manager, Finance, IT/Dev |

> **Q11/Q12 Parallel Execution:** Agent 2 (BSD), Agent 3 (Compliance), and Agent 7 (Ripple Map) run in parallel. Q11 (§2.2 Compliance) and Q12 (§2.3 Ripple) are **Implementation Readiness Gates** — they block development start, not BA sign-off. BSD drafting proceeds immediately; §2.2 and §2.3 are updated when Agent 3/7 deliver. Both must be resolved before UAT.

---

## Insurance BA Input Routing

| Input | Route |
|-------|-------|
| Vague requirement | Agent 0 |
| Client requirement doc | Agent 1 |
| Product spec doc | Agent 5 → then Agent 1 |
| Confirmed requirement (no Gap analysis needed) | Agent 2 |
| Confirmed Gap matrix | Agent 2 + Agent 7 (parallel) |
| GAP_MATRIX_UPDATE | Agent 7 + Agent 2 + Agent 6 (parallel) |
| BSD_UPDATE | Agent 7 + Agent 4 + Agent 6 (parallel) |
| CONFIG_GAP_LIST | Agent 6 |
| Change request with data migration | Agent 9 + Agent 7 (parallel) |
| APPROVED_BSD | Agent 4 + Agent 6 (parallel) |
| TECH_SPEC | Agent 8 |
| Compliance query | Agent 3 |

---

## Mandatory Auto-Triggers

Run on every requirement input:

| Signal | Action |
|--------|--------|
| Regulatory keywords detected | Agent 3 + Agent 1 (parallel) |
| Data migration / legacy keywords detected | Agent 9 + Agent 7 (parallel) |
| Cross-system integration keywords detected | Agent 7 first, then Agent 1 |
| Gap Matrix ready | Agent 7 + Agent 2 (parallel) |
| APPROVED_BSD | Agent 4 + Agent 6 (parallel) |
| BSD update | Incremental analysis + Tech Spec + Config (parallel) |
| Tech Spec complete | Prompt user to trigger Agent 8 |
| User mentions "legacy / historical data / migration" | Prompt user to trigger Agent 9 |

---

## Hand-off Protocol

### Agent 1 → Agent 2

| Mode | Description |
|------|-------------|
| Mode A (structured) | Gap Matrix → Agent 2 directly |
| Mode B (natural language) | OpenClaw pre-processor converts to JSON → Agent 2 directly (bypasses Agent 1) |

Both modes produce the same BSD output quality.

### Agent 4 → Agent 6

- **Primary input:** APPROVED_BSD (full v9.0 BSD)
- **Config Gap source:** BSD §4.0 Open Questions + Implementation Notes. Same BSD artifact for both agents — no separate "Lite BSD" artifact.

### Loop-back Paths

| Trigger | Return To | Action |
|---------|-----------|--------|
| Agent 2 assumption fails after KB verification | Agent 1 | Re-run Step 1.3 mechanism check; update Gap Matrix |
| Agent 4 Dev infeasible | Agent 2 | Revise BSD rule; re-trigger Tech Spec |
| Client changes requirement | Agent 0 | Re-run Discovery; reassess Change Type |
| Agent 6 surfaces new Dev Gap | Agent 4 | Re-run Tech Spec with clarified config path |

---

## Product Spec Analysis (shared across Agent 1, 2, 5)

Core rules (aligned with `agent1-gap.md` Step 1.3):

- `ps-*` KB is the truth source for InsureMO behavior
- **Identify existing InsureMO mechanism FIRST** — before writing any rule, check INVARIANT / PF config / Standard formula / CS Item / Field
- If existing mechanism covers it → do NOT write a new formula unless `Client Override = YES`
- Not documented in `ps-*` = Unknown — never default to Dev Gap
- **Two-Pass:** Pass 1 = identify mechanism (Step 1.3) | Pass 2 = classify via ps-* + OOTB | Uncertain → mark Unknown

---

## File Output

Format: `work/YYYY-MM-DD/{date}_{type}_{name}_v{version}.md`

Update `index.md` in the same folder on completion.

---

## Sub-agent Notification Convention

**Sub-agent responsibilities:**
- Write output to the specified file path
- Complete the task and return results in the completion event
- MUST NOT call `message` tool directly (Feishu plugin unavailable in sub-agent context)

**Main agent responsibilities (after receiving `subagent_announce`):**
- Receive completion event with results summary
- Send Feishu card notification to Dan with: file path + key findings (3-5 bullets)
- Verify file exists before notifying

> Do NOT include Feishu notification instructions in the sub-agent task field.
