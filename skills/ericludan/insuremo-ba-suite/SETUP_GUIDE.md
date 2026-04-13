# OpenClaw Setup Guide — insuremo-ba-suite v4.8

---

## v4.8 Change Log

- AGENTS.md restructured: system-level content moved to SOUL.md
- SKILL_TREE.md streamlined: visual reference only, structure → SKILL.md
- bsd-writing deprecated: BSD guidance fully absorbed into insuremo-ba-suite
- Master Routing Table removed from SKILL.md: now authoritative in AGENTS.md

---

## Step 1 — Folder Structure

Current structure (v4.8):

```
insuremo-ba-suite/
├── SKILL.md                              # Entry point
├── AGENTS.md                             # Routing & workflow (v4.8 — authoritative)
├── SETUP_GUIDE.md                        # This file
├── agents/                               # Agent 0-9 definitions
│   ├── agent0-discovery.md
│   ├── agent1-gap.md
│   ├── agent2-bsd.md
│   ├── agent3-regulatory.md
│   ├── agent4-techspec.md
│   ├── agent5-decoder.md
│   ├── agent6-product-factory-configurator.md
│   ├── agent7-cross-module-impact-analyzer.md
│   ├── agent8-uat-generator.md
│   └── agent9-data-migration.md
├── contracts/
│   └── input-contract.md
└── references/
    ├── InsureMO Knowledge/              # ps-* KB (always needed — all modules)
    │   └── ps-product-factory.md + ps-investment.md  # Only for VUL/ILP (add on top of all-modules base)
    ├── InsureMO V3 User Guide/         # V3 UG (on-demand supplement)
    ├── output-templates.md              # BSD v9.0 templates
    ├── bsd-patterns.md / bsd-quality-gate.md / gap-description-patterns.md
    ├── insuremo-gap-detection-rules.md  # R1-R9 gap detection
    ├── KB_USAGE_GUIDE.md               # KB reading strategy
    ├── case-index.md / unknown-register.md / delivery-traceability.md
    ├── regulatory-report-template.md / sea-regulatory.md
    ├── reg-mas.md / reg-bnm.md / reg-hkia.md / reg-oid.md / reg-ojk.md / reg-sea-common.md
    ├── afrexai-benchmarks.md / spec-miner-ears-format.md
```

---

## Step 2 — Verify SKILL.md Frontmatter

```yaml
---
name: insuremo-ba-suite
version: 4.8.0
description: InsureMO insurance BA workflow suite. Use when analyzing insurance
  product requirements, writing BSD or functional spec for UL/HI/rider products,
  performing gap analysis against InsureMO OOTB, generating developer-ready tech
  specs, or handling SEA regulatory compliance checks (MAS/BNM/OIC/HKIA/OID/OJK).
author: InsureMO BC Team
tools: Read, Write, exec, web_search
user-invocable: true
---
```

**Critical fields:**
- `name`: lowercase with hyphens
- `tools`: must include `exec` and `web_search`
- `user-invocable: true`: allows manual trigger via `/insuremo-ba-suite`
- `description`: used by OpenClaw for auto-trigger matching

---

## Step 3 — Configure clawhub.md

```markdown
## insuremo-ba-suite
- **Trigger:** Insurance BA tasks — requirement analysis, gap analysis,
  BSD, tech spec, SEA compliance (MAS/BNM/OIC/HKIA/OID/OJK)
- **Entry point:** `skills/insuremo-ba-suite/SKILL.md`
- **Reads at runtime:** agents/, contracts/input-contract.md
- **Reads on demand:** references/ (loaded by specific agents only)
- **Required tools:** exec, web_search
- **Do NOT inject into Claude context:** references/ files are loaded
  on-demand by agents, not upfront
```

> ⚠️ Do NOT add `agents/` or `references/` to global context. Only `SKILL.md` should be in always-on context.

---

## Step 4 — Configure SOUL.md, AGENTS.md, USER.md

These files go into Claude's system prompt context (not OpenClaw's skill runtime).

**v4.8 change:** Identity, Memory System, and Security have been removed from `AGENTS.md`. They now live in:
- `SOUL.md v3.3` — Identity, Communication Style, Memory System
- `USER.md v3.1` — Output Standards, Audience Switching

**Separation:**
```
OpenClaw reads:   clawhub.md, SKILL.md (and sub-files at runtime)
Claude reads:     SOUL.md, AGENTS.md, USER.md, input-contract.md
```

---

## Step 5 — Configure OpenClaw→Claude Prompt Wrapper

```
INPUT_TYPE: {{input_type}}
AGENT: {{agent_id}}
ASSUMPTION_REGISTER: {{assumption_register_json}}
OPEN_QUESTIONS: {{open_questions_json}}

{{user_input_or_skill_output}}
```

| Variable | Source |
|---|---|
| `input_type` | Set by OpenClaw based on which skill/stage produced the input |
| `agent_id` | Set by OpenClaw based on routing logic in `AGENTS.md` |
| `assumption_register_json` | Persisted state from previous turns, or `[]` |
| `open_questions_json` | Persisted state from previous turns, or `[]` |

---

## Step 6 — Routing Verification

After installation, verify routing:

| User says | Should trigger |
|-----------|---------------|
| "Help me analyze HI rider requirements" | Agent 1 (Gap) |
| "Write a BSD for a UL product" | Agent 2 (BSD) |
| "Does InsureMO support this OOTB?" | Agent 1 (Gap — OOTB check) |
| "Generate tech spec for the developer" | Agent 4 (Tech Spec) |
| "Malaysia market compliance check" | Agent 3 (Regulatory) |
| "Create UAT test scenarios" | Agent 8 (UAT) |
| "Analyze data migration from legacy system" | Agent 9 (Migration) |

**Complete routing table:** `AGENTS.md § Insurance BA Input Routing`

---

## Step 7 — Maintenance

| Task | Frequency | Action |
|------|-----------|--------|
| Update sea-regulatory.md | Every 6 months | Re-check regulatory sources via web_search |
| Update insuremo-ootb.md | On InsureMO version upgrade | Re-verify OOTB capability list |
| Sync version | Any structural change | Update SKILL.md AND AGENTS.md together |
| Clean backups | Quarterly | Remove old versions from `agents/backup/` |
| Verify routing | After any agent file change | Run Step 6 test sequence |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Skill not triggering | Check `description` field in SKILL.md — add user trigger phrases |
| Claude ignoring INPUT_TYPE | Verify prompt wrapper (Step 5) injects header before user input |
| exec not running | Confirm `exec` in `tools` field of SKILL.md frontmatter |
| Routing accuracy drops | Review `AGENTS.md § Insurance BA Input Routing` |
| bsd-writing skill still appearing | Update description field to mark deprecated; user should use insuremo-ba-suite |
