# InsureMO BA Suite — Skill Tree
# Version: 4.8.0 | Updated: 2026-04-07

> **v4.8 change:** SKILL_TREE.md is now a visual reference only. Full file structure → see `SKILL.md § File Structure`.

---

## Agent Map

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     InsureMO BA Suite v4.8                                  │
│                                                                              │
│  INPUT                          AGENTS                          OUTPUT       │
│  ─────                          ──────                          ──────       │
│                                                                              │
│  Vague request      ───────────► Agent 0: Discovery        ► Req Brief       │
│                                                                              │
│  Client doc         ───────────► Agent 1: Gap Analysis    ► Gap Matrix       │
│                                       │                                        │
│                                       ▼                                        │
│                               ┌─────────────────────┐                         │
│                               │  UNKNOWN Register   │                         │
│                               └─────────────────────┘                         │
│                                       │                                        │
│  Product spec      ───────────► Agent 5: Decoder         ► Product Profile    │
│                                       │                                        │
│                                       ▼                                        │
│                                 Agent 1: Gap Analysis                         │
│                                       │                                        │
│                                       ▼                                        │
│                               Gap Matrix ───────────────┐                     │
│                                                         │                     │
│               ┌─────────────────────┬───────────────────┼───────────────┐     │
│               │                     │                   │               │     │
│               ▼                     ▼                   ▼               ▼     │
│        ┌─────────────┐       ┌─────────────┐      ┌─────────────┐           │
│        │  Agent 2:   │       │  Agent 6:   │      │  Agent 7:   │           │
│        │  BSD/BSD    │       │  Config     │      │  Impact     │           │
│        └──────┬──────┘       └──────┬──────┘      └──────┬──────┘           │
│               │                      │                     │                  │
│               ▼                      ▼                     │                  │
│        ┌─────────────┐       ┌─────────────┐               │                  │
│        │  APPROVED   │       │  Config     │               │                  │
│        │     BSD     │       │  Runbook    │               │                  │
│        └──────┬──────┘       └──────┬──────┘               │                  │
│               │                      │                     │                  │
│               ▼                      ▼                     ▼                  │
│        ┌─────────────┐       ┌─────────────┐       ┌─────────────┐           │
│        │ Agent 4:   │       │ Agent 8:   │       │ Agent 9:   │           │
│        │ Tech Spec  │       │ UAT Tests  │       │ Data Migr. │           │
│        └─────────────┘       └─────────────┘       └─────────────┘           │
│               │                      │                     │                  │
│               ▼                      ▼                     ▼                  │
│        Tech Spec             UAT Matrix           Migration Req               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Responsibility Summary

| Agent | Name | Key Input | Key Output |
|-------|------|-----------|------------|
| Agent 0 | Discovery | Vague request | Requirement Brief |
| Agent 1 | Gap Analysis | Client doc / Product Profile | Gap Matrix |
| Agent 2 | BSD Generation | Gap Matrix | BSD v9.0 |
| Agent 3 | Regulatory Compliance | Any product/requirement | Regulatory Report |
| Agent 4 | Tech Spec | APPROVED_BSD | Developer-ready Tech Spec |
| Agent 5 | Product Decoder | Product spec PDF | Product Profile |
| Agent 6 | Configurator | APPROVED_BSD / Config gaps | Config Runbook |
| Agent 7 | Impact Analyzer | BSD / Gap Matrix | Impact Matrix |
| Agent 8 | UAT Generator | Tech Spec | UAT Test Cases |
| Agent 9 | Data Migration | Legacy system / change request | Migration Requirements |

---

## Full File Structure Reference

See `SKILL.md § File Structure` for complete directory tree.
