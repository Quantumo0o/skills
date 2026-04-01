---
name: harness-engineer
description: >
  A persistent autonomous engineering harness runtime that transforms any repository into a
  self-improving software system. Use this skill whenever the user wants to: build or run an
  autonomous coding agent, set up a self-healing engineering loop, orchestrate multi-agent
  software development, implement harness engineering principles, create a doc-driven
  development workflow, or run long-horizon autonomous software tasks. Trigger on phrases like
  "autonomous agent", "self-healing codebase", "harness engineering", "multi-agent pipeline",
  "continuous improvement loop", "OpenClaw skill", or any request for an agentic engineering
  system that runs without constant human input. Primarily designed for Claude Code and
  OpenClaw environments.

metadata:
  platform_enforcement: required
  platform_note: >
    This skill is instruction-only. Safe operation depends on the host platform
    enforcing: MCP tool router (blocked sensitive reads, protected writes, output
    redaction), sandboxed test execution, scoped git credentials (no direct push to
    main), and human approval gates. If these cannot be confirmed, run single-pass
    with manual oversight only. Full checklist in PLATFORM_REQUIREMENTS.md.
  required_platform_capabilities:
    - mcp_tool_router
    - sandboxed_test_execution
    - git_credential_scoping
    - human_approval_gates
  safe_defaults:
    - loop_mode: single-pass
    - verify_platform_requirements_before_first_use: true
---

# HARNESS AUTONOMOUS RUNTIME

A production-grade skill for Claude Code and OpenClaw that transforms a repository into a
self-improving software system using six core harness engineering principles.

---

## SIX CORE PRINCIPLES

### P1: CONTEXT ENGINEERING
Treat context as a finite, precious resource. Curate aggressively.
- Read CLAUDE.md / AGENTS.md first for base knowledge -- never infer what is written
- Pull runtime/error logs for real-time status, not docs (docs lie; codebase does not)
- 40% Rule: compact or outsource to a sub-agent when context exceeds 40% of window
- Use sub-agents to isolate concerns and prevent context pollution in the main agent
- Three-phase sub-agent model: Research => Plan => Implement (see agents/dispatcher.md)
- Anything the agent cannot access is assumed to not exist

### P2: TOOL USAGE
Each sub-agent receives only the tools it needs -- no more.
- Tools are assigned per-role (see tools/TOOL_REGISTRY.md, per-agent subsets)
- All tools use MCP (Model Context Protocol) as the unified interface
- Generated code runs in a sandbox isolated from the harness security context
- Harness secrets are never visible to generated code or agent context directly

### P3: VERIFICATION MECHANISM
Every output is verified by someone other than who produced it.
- Deterministic first: linter, pre-commit hooks, structured tests -- no LLM judgment
- Generation-review isolation: the agent that writes code never reviews its own code
- 3-layer recursive review: reviewer sub-agents => comment-generator => implementer =>
  re-review, recursively until all reviewers approve
- Details in references/testing-standards.md and agents/reviewer.md

### P4: STATUS MANAGEMENT
State lives outside the context window, in the repo.
- Progress tracked in docs/status/PROGRESS.md (structured checklist markdown)
- Git commit after every atomic task completion (checkpoint)
- Context reset = new chat + structured handoff from docs/status/HANDOFF.md
- Checkpoint recovery: new agent reads handoff and resumes from last checkpoint
- Details in runtime/status-management.md

### P5: OBSERVABILITY AND FEEDBACK CLOSED-LOOP
Track what happens. Feed failures back into the harness, not the code.
- Execution tracking in docs/generated/tool-logs/
- Quality categorization and prioritization (see runtime/observability.md)
- Abnormality detection: unexpected patterns trigger debugger_agent
- Critical: when a failure occurs, analyze the harness gap -- not the model or code
- Continuously improve the harness, not just the application
- Details in runtime/observability.md

### P6: HUMAN SUPERVISION
Humans approve high-impact events. The harness surfaces them explicitly.
- Plan approval before implementation begins
- Architecture changes require human sign-off
- Failure retry decisions after N retries
- Lifespan hooks: on-start, on-plan-complete, on-cycle-complete, on-error, on-halt
- Details in runtime/autonomy-rules.md

---

## NON-NEGOTIABLE RULES

1. CLAUDE.md / AGENTS.md IS GROUND TRUTH -- read it first, every session.
2. CODEBASE OVER DOCS -- when they conflict, trust the code.
3. 40% CONTEXT RULE -- compact or sub-agent before crossing 40% of context window.
4. NO IMPLEMENTATION WITHOUT a research output, a plan, and validation criteria.
5. GENERATION AND REVIEW ARE ALWAYS SEPARATE -- never the same agent.
6. FAILURE = HARNESS GAP -- fix the harness, not just the symptom.
7. OPTIMIZATION PRIORITY: Security => Correctness => Reliability => Performance =>
   Memory => Maintainability => Cost

---

## SAFE START GUIDE

Before anything else: read PLATFORM_REQUIREMENTS.md and verify every item.
The harness depends on platform enforcement that cannot be checked from these files alone.

Step 1 -- Verify platform requirements (PLATFORM_REQUIREMENTS.md)
Run through the five platform capability checks before any other step.

Step 2 -- Sandbox first
Run on a throwaway branch. Observe one single-pass cycle before enabling continuous mode.

Step 2 -- Review CONFIG.yaml before every run
| loop_mode            | single-pass | Change after sandbox validation        |
| max_parallel_agents  | 3           | Increase after confirming behavior     |
| block_destructive... | true        | Never change                           |

PRs always require human approval. There is no auto-merge.

Step 3 -- Protect main branch
Require human reviewers on main/trunk in your git host.

Step 4 -- Graduation path: single-pass => maintenance => continuous

---

## HOW TO USE THIS SKILL

When activated in Claude Code or OpenClaw, read in this order:

1. CLAUDE.md or AGENTS.md if present (base context)
2. CONFIG.yaml (runtime settings)
3. runtime/loop.md (execution model)
4. runtime/context-engineering.md (context budget rules)
5. runtime/status-management.md (restore checkpoint if resuming)
6. MEMORY.md (prior failure context)
7. agents/dispatcher.md (task decomposition model)
8. Begin the loop

---

## REFERENCE FILES

| File                              | When to read                              |
|-----------------------------------|-------------------------------------------|
| CLAUDE.md / AGENTS.md             | First, every session -- base knowledge    |
| CONFIG.yaml                       | At startup                                |
| MEMORY.md                         | At startup and after every failure        |
| runtime/loop.md                   | Each loop cycle                           |
| runtime/context-engineering.md    | Continuously -- governs context budget    |
| runtime/status-management.md      | At startup (resume) and after each task   |
| runtime/observability.md          | After VERIFY phase                        |
| runtime/memory-system.md          | When writing or querying memory           |
| runtime/self-improvement.md       | After any failure                         |
| runtime/prioritization.md         | When selecting the next task              |
| runtime/autonomy-rules.md         | When blocked or at human gate             |
| agents/dispatcher.md              | Before decomposing any task               |
| agents/researcher.md              | Research phase                            |
| agents/planner.md                 | Plan phase                                |
| agents/implementer.md             | Implement phase                           |
| agents/reviewer.md                | Review cycle                              |
| agents/debugger.md                | On any failure                            |
| agents/optimizer.md               | Optimization mode                         |
| agents/garbage-collector.md       | GC interval                               |
| tools/TOOL_REGISTRY.md            | Before any tool call                      |
| tools/tool-router.md              | Routing and redaction rules               |
| tools/execution-protocol.md       | Full tool call lifecycle                  |
| references/harness-rules.md       | Core constraints                          |
| references/testing-standards.md   | Before writing or running tests           |
| references/security-performance.md| Before any implementation                 |
| references/git-workflow.md        | Before any commit or PR                   |
| references/mcp-tools.md           | MCP tool definitions and per-agent sets   |
| references/sensitive-paths.md     | Forbidden read paths -- enforced in-skill |
| templates/                        | Plans, ADRs, handoffs, status docs        |
