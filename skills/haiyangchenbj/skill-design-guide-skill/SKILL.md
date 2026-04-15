---
name: skill-design-guide
display_name: "Skill Design Guide"
description: >
  Design better AI skills with proven architecture patterns. Helps you decide
  Workflow vs Agent, pick the right pattern (Prompt Chaining, Routing,
  Parallelization, Orchestrator-Workers, Evaluator-Optimizer), write clean
  SKILL.md files, and catch common mistakes with a 25-point quality checklist.
  Based on design principles from Anthropic, OpenAI, and LangChain.
  Chinese version included (SKILL_zh.md).
version: "1.3.2"
author: haiyangchen (Coralyx)
category: "Architecture / Design Patterns"
license: "MIT"
homepage: https://github.com/haiyangchenbj/skill-design-guide-skill
read_when:
  - Starting a new skill and unsure whether to use Workflow or Agent
  - Don't know which of the 5 workflow patterns to choose
  - Code works but architecture feels messy
  - Need to review a skill before production
  - "design skill architecture, workflow or agent, choose workflow pattern"
  - "review skill design, skill quality checklist, brain hands session"
  - "skill anti-patterns, prompt chaining vs routing, when to use agent"
---

# Skill / Agent Design Guide

> **30-Second Test**: If you're about to write a SKILL.md file OR your skill "works but feels messy", load this guide.

## 🆚 What Makes This Different

| Tool | What It Does | When You Need It |
|------|-------------|------------------|
| **skill-creator** | Helps you WRITE skill code | "How do I structure this file?" |
| **template-skill** | Gives you COPY-PASTE templates | "What's the standard format?" |
| **THIS GUIDE** | Teaches you DESIGN decisions | "Should this be Workflow or Agent?" |

**This guide answers WHY, not HOW.**

## ✅ 3 Ways to Use This Guide

### 1. New Skill Design (Most Common)
**You say**: "I want to build a [X] skill"
**I help you decide**:
- Workflow or Agent?
- Which of the 5 workflow patterns?
- Brain/Hands/Session separation?

**Output**: Architecture blueprint (not code)

### 2. Skill Review
**You say**: "Review my skill design" or "Check this skill's quality"
**I do**: Run 25-point checklist
- Structure check
- Principle alignment  
- Anti-pattern detection

**Output**: Review report with improvement suggestions

### 3. Pattern Selection
**You say**: "Should I use Prompt Chaining or Routing?"
**I explain**: 5 workflow patterns with decision criteria

**Output**: Pattern recommendation with rationale

---

Load this guide as a constraint layer whenever designing any Skill or Agent. Distilled from official engineering blogs and technical docs by Anthropic, OpenAI, and LangChain.

---

## Principle Zero: Simplicity First

> **Start simple. Add complexity only when simpler solutions fall short.**

This is the consensus baseline across Anthropic, OpenAI, and LangChain. Any design violating this principle gets sent back to the drawing board.

**Practical checklist:**
- If a single SKILL.md can solve it, don't split into multiple files
- If a step can be done with deterministic code (scripts), don't use an LLM
- If a fixed-step workflow can solve it, don't use a dynamic Agent
- Ship the MVP first, iterate based on actual output quality

---

## Principle One: Brain / Hands / Session Separation

From Anthropic's April 2026 architecture essay: well-designed Agent systems should separate three concerns:

| Component | Role | In Your Skill |
|-----------|------|---------------|
| **Brain** | Decision logic, workflow definition | `SKILL.md` — the orchestration layer |
| **Hands** | Deterministic execution, tool operations | `scripts/` — code that actually does things |
| **Session** | Context, knowledge base, configuration | `references/`, `assets/`, config files |

**Why this matters:**
- Modify Skill logic without touching knowledge bases
- Update reference materials without changing Skill code
- Swap file directory structures without rewriting the Skill

**Your skills already follow this:** `data-ai-daily-brief` (scripts=fetches data), `benjie-model` (serves as Session layer for other skills).

---

## Step 1: Workflow or Agent?

Before designing anything, answer one question: **Are the task steps predetermined, or does the LLM need to decide the next step dynamically?**

| Type | Definition | When to choose |
|------|-----------|----------------|
| **Workflow** | Executes along predefined steps | Steps are clear, predictable; stability matters |
| **Agent** | LLM dynamically plans the flow | Steps are uncertain; flexibility needed; uncertainty acceptable |

Most real-world scenarios are workflows. Don't pick Agent just because it sounds more advanced — workflows are faster, cheaper, and easier to debug.

---

## Step 2: Choose a Workflow Pattern

If you determined it's a workflow (most likely), pick the best-fit pattern from these five:

### Pattern 1: Prompt Chaining
```
Step A → [checkpoint] → Step B → [checkpoint] → Step C
```
- Task decomposes into sequential steps, each processing the previous output
- Programmatic checks (non-LLM) can be inserted between steps
- **Most common pattern** — fits most content generation tasks

### Pattern 2: Routing
```
Input → [classify] → Route A / Route B / Route C
```
- Input has clear types; different types need different processing flows
- Example: article type → corresponding template and rules

### Pattern 3: Parallelization
```
Input → [split] → Subtask A + Subtask B + Subtask C → [merge]
```
- Subtasks are independent, can run in parallel for speed
- Example: core article → simultaneously generate blog, social, newsletter versions

### Pattern 4: Orchestrator-Workers
```
Central LLM → [dynamic dispatch] → Worker1 + Worker2 + ... → [merge]
```
- Use when subtasks cannot be predefined
- **Use sparingly** — high complexity, hard to debug

### Pattern 5: Evaluator-Optimizer
```
Generate → Evaluate → Feedback → Regenerate → ... until pass
```
- Clear evaluation criteria exist; iteration brings measurable improvement
- Example: content review, code review

---

## Step 3: Design the Skill Structure

### Required

| Component | Content | Notes |
|-----------|---------|-------|
| **SKILL.md** | YAML metadata + workflow instructions + hard rules | The only mandatory file |

### Optional (add as needed)

| Component | When needed | Notes |
|-----------|------------|-------|
| **reference/** | Skill needs domain knowledge or reference docs | Load on demand, not pre-loaded |
| **scripts/** | Deterministic steps can be implemented as scripts | Reduces LLM calls, improves reliability |
| **assets/** | Templates, configs, or resources needed | Writing templates, brand guides, etc. |

### SKILL.md Template

```yaml
---
name: my-skill-name
description: |
  One sentence describing what it does. Second sentence on trigger scenarios.
  Trigger keywords: keyword1, keyword2, keyword3.
version: 1.0.0
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - execute_command
  - web_search
disable: false
---

# Skill Name

One paragraph overview: what this Skill does, for whom, and what it outputs.

## Workflow

### Step 1: [Deterministic] Confirm Input
- Read xxx
- Validate xxx exists
- If missing, stop and report

### Step 2: [Deterministic] Load Materials
- Read `reference/xxx.md` (only needed files, don't read everything)
- Read `assets/template.md`

### Step 3: [LLM] Core Generation
- Based on materials above, generate xxx
- Follow these rules:
  - Rule 1
  - Rule 2

### Step 4: [LLM] Self-Check
- Verify output meets xxx criteria
- If not, fix and re-output

### Step 5: [Deterministic] Save Output
- Write to `output/xxx`

## Hard Rules

> These rules cannot be violated. They take priority over everything else.

1. [Rule 1 — e.g., Never fabricate data]
2. [Rule 2 — e.g., Sensitive content check]
3. [Rule 3 — e.g., Product names must use official names]

## Failure Handling

| Failure Scenario | Action |
|-----------------|--------|
| Source material file not found | Stop generation, report missing file |
| Output exceeds target word count by 50% | Compress and rewrite |
| [Other scenario] | [Action] |

## Output Format

[Define exact output format and required fields]
```

---

## Step 4: Quality Checklist

Run this checklist after completing every Skill design:

### Structure

- [ ] SKILL.md YAML metadata includes `name` and `description`
- [ ] `description` contains trigger keywords
- [ ] Workflow steps are clear; each step tagged `[Deterministic]` or `[LLM]`
- [ ] Has a "Hard Rules" section
- [ ] Has a "Failure Handling" section
- [ ] Has an "Output Format" definition

### Principles

- [ ] **Simplicity first**: Is this the simplest approach? Have all removable steps been removed?
- [ ] **Workflow vs Agent**: Correctly chose workflow/agent? (Most should be workflows)
- [ ] **Pattern match**: Which workflow pattern was selected? What's the rationale?
- [ ] **LLM minimized**: Are all deterministic steps using scripts/deterministic logic instead of LLM?
- [ ] **Progressive disclosure**: Are references loaded on-demand or all pre-loaded? (Should be on-demand)

### Tools & Paths

- [ ] All file references use **absolute paths** or paths clearly relative to Skill directory
- [ ] Tool descriptions are unambiguous (parameter names like `user_id` not `user`)
- [ ] Return values contain only high-signal info (name, content), not low-value metadata (UUID, mime_type)

### Guardrails

- [ ] Input validation: Does it check input validity?
- [ ] Output filtering: Is there a sensitive content check?
- [ ] Failure handling: Every possible failure scenario has a response?
- [ ] Human-in-the-loop: Are there checkpoints before high-risk outputs?

### Observability

- [ ] Can you trace which materials the Skill referenced?
- [ ] Can you pinpoint which step failed when errors occur?

### Production-Ready Extensions (Optional)

For skills running in automation or serving multiple users:

- [ ] **Quality vs Latency**: Have you traded off accuracy against response time? (More reflection steps → better quality but slower)
- [ ] **Guardrails**: Input validation, output filtering, human checkpoints before high-risk outputs
- [ ] **Evaluation**: End-to-end quality checks, component-level accuracy tests, continuous monitoring

---

## Anti-Patterns (Must Avoid)

| Anti-Pattern | Description | Correct Approach |
|-------------|-------------|-----------------|
| **Over-engineering** | Complex architecture before a working MVP | Start with simplest SKILL.md, iterate from there |
| **Full preload** | Dumping all references into context at once | Specify which files to read at each step |
| **God Skill** | One Skill handling too many responsibilities | Split duties — each Skill does one thing |
| **Relative paths** | File references using relative paths | Use absolute paths or explicit base paths |
| **No guardrails** | Missing output checks and failure handling | Every Skill must have hard rules + failure handling |
| **All-LLM** | Using LLM for every step | Deterministic steps use scripts; LLM only when necessary |
| **Vague output** | No defined output format | Explicitly define format, fields, and length requirements |
| **No evaluation** | Shipping without testing | Test with real tasks; observe where the Agent fails |

---

## Platform Compatibility

This guide applies to any Skill/Agent platform:

| Platform | Skill Manifest | Scripts Directory | Notes |
|----------|---------------|-------------------|-------|
| **ClawHub** | `SKILL.md` | `scripts/` | Native support |
| **OpenAI GPTs** | Instructions + Functions | Code Interpreter | Map concepts to GPT architecture |
| **Anthropic Claude** | System Prompt + Tools | External functions | Brain=system prompt, Hands=tools |
| **LangChain** | Chain definition | Runnable lambdas | Patterns map to LCEL |
| **Custom Agents** | Agent config | Tool implementations | Architecture principles universal |

**Key insight**: Brain/Hands/Session separation is platform-agnostic. Adapt the file structure to your platform's conventions.

---

## Credits & References

This guide distills official engineering practices from:

- **Anthropic**: "Building Effective Agents" (Dec 2024), "Brain, Hands, and Session" (Apr 2026)
- **OpenAI**: Function Calling Best Practices, Agent SDK guidelines
- **LangChain**: "State of AI Agents" report, LCEL documentation

---

## Deep Dive References

When you need more detailed design guidance, load these on demand:

| Scenario | Reference Document |
|----------|-------------------|
| Full industry research (Anthropic/OpenAI/LangChain principles) | `reference/agent-design-research.md` |
| Anthropic tool design detailed guide | `reference/anthropic-tool-design.md` |

---

*v1.3.0 | Based on Anthropic/OpenAI/LangChain engineering practices | 2026-04-15*

**Changelog:**
- v1.3.0: Added usage scenarios, created Chinese version (SKILL_zh.md), optimized value communication
- v1.2.0: Platform-agnostic rewrite, added Credits, enhanced keywords for architecture focus
- v1.1.0: Added Principle One (Brain/Hands/Session separation) and Production-Ready extensions
- v1.0.0: Initial release
