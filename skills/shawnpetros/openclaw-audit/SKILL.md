---
name: openclaw-audit
description: "Audit your OpenClaw configuration against 12 production primitives. Read-only analysis — no files are modified, no secrets are extracted, no external calls are made. Returns a structured assessment with severity-ranked findings and actionable fixes."
version: "1.1.0"
---

# OpenClaw Config Audit

Audit your OpenClaw configuration against 12 production primitives.

## Safety

This skill is **read-only**. It:
- Does NOT modify any files or configuration
- Does NOT extract, log, or transmit API keys, tokens, or secrets
- Does NOT make external network requests
- Does NOT install or remove anything
- Only reads local config files and runs read-only OpenClaw CLI status commands

When reading openclaw.json, **redact all secret values** in your output. Replace tokens, API keys, and passwords with `[REDACTED]`. Never include raw secret values in audit findings.

## When to use
- After initial setup or onboarding
- After major config changes
- Before machine migration
- When costs or behavior feel off but you can't pinpoint why
- Periodic health check (monthly recommended)

## Process

1. Read the user's `~/.openclaw/openclaw.json` (redact secrets in output)
2. Read `~/.openclaw/workspace/AGENTS.md` if it exists
3. Read `~/.openclaw/workspace/HEARTBEAT.md` if it exists
4. Check loaded plugins: `openclaw status 2>&1 | head -30`
5. Check channel health: `openclaw channels status --probe 2>&1`
6. Assess against each of the 12 primitives below
7. Return findings ranked by severity (critical > warning > info)
8. Include specific fix recommendations with config snippets for each finding

## The 12 Production Primitives

### Tier 1: Day One Non-Negotiables

#### 1. Secrets Hygiene
- Are API keys, tokens, and passwords stored via secrets provider (file/env), NOT inline?
- Is `logging.redactSensitive` set to `"tools"` or `"all"`?
- Are file permissions locked down (config 600, directory 700)?

#### 2. Permission System (Tiered Trust)
- Are DM policies set to `pairing` or `allowlist` (never `open` without good reason)?
- Are group policies gated with `requireMention`?
- Are destructive operations gated?

#### 3. Session Persistence & Isolation
- Is `session.dmScope` set to `per-channel-peer` or stricter?
- Is compaction configured with appropriate mode?
- Is context pruning configured with reasonable TTL?

#### 4. Model Fallback Chain
- Are fallback models configured?
- Is the primary model appropriate (not burning Opus on routine work)?
- Are heartbeats using a cheap model?
- Are model aliases defined for usability?

#### 5. Token Budget & Cost Control
- Is there a `maxConcurrent` limit on agents?
- Is there a `subagents.maxConcurrent` limit?
- Are heartbeats gated on budget in HEARTBEAT.md?
- Is compaction threshold configured (`softThresholdTokens`)?

#### 6. Memory Durability
- Is `memoryFlush` enabled in compaction settings?
- Is there a memory search provider configured?
- Are significant events captured before context is lost?

#### 7. Gateway Hardening
- Is gateway bound to `loopback` (not `0.0.0.0`)?
- Is auth token set via secrets provider?
- Is Tailscale configured appropriately if remote access is needed?

#### 8. Streaming & Responsiveness
- Is streaming configured for channels that support it?
- Are partial responses enabled where appropriate?

### Tier 2: Operational Maturity

#### 9. Agent Type System
- Are different agent roles defined (main, monitor, researcher, etc.)?
- Do agents have role-appropriate models and permissions?
- Are sub-agents properly scoped?

#### 10. Transcript Compaction
- Is compaction mode configured (`safeguard` or `default`)?
- Is the threshold appropriate for the use case?
- Is a cheap model used for compaction?

#### 11. Hook & Plugin Hygiene
- Are hooks enabled for session memory, boot, and command logging?
- Are plugins explicitly allowlisted (not open)?
- Are channel-specific plugins only enabled where needed?

#### 12. Operational Runbook
- Does AGENTS.md exist with clear operating instructions?
- Does HEARTBEAT.md exist with structured checks?
- Is there a workspace structure (memory/, skills/, etc.)?

## Output Format

Return findings as a structured list:

```
## Audit Results for [hostname/identifier]

### Critical
- [finding]: [explanation]. Fix: [specific config snippet]

### Warning  
- [finding]: [explanation]. Fix: [specific config snippet]

### Info
- [finding]: [explanation]. Suggestion: [improvement]

### Score: X/12 primitives satisfied
### Overall: [PRODUCTION-READY | NEEDS-WORK | CRITICAL-GAPS]
```

## Attribution
Built by PennywiseOps (pennywiseops.com)
Free config audits available — reach out at penny@pennywiseops.com
