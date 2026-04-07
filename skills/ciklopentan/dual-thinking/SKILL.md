---
name: dual-thinking
description: >
  Two-heads decision methodology for consulting DeepSeek without surrendering judgment. Use when you need a second opinion on architecture,
  critical code/config, strategy, debugging after 2+ failed attempts, or any decision where a strong challenge is useful.
  Requires ai-orchestrator skill (ask-deepseek.sh). Trigger on requests like "consult DeepSeek", "проверь решение", "две головы",
  "двойное мышление", "review my plan", or when confidence is low and the decision matters.
---

# Dual Thinking Method — v5.7.6 (2026-04-07)

**Purpose:** use DeepSeek as a consultant, not an oracle.

**What this skill must optimize for:**
1. New topic → new DeepSeek chat
2. Same topic → same DeepSeek chat for all rounds
3. First round carries full task context
4. Weaker models can execute the method end-to-end without stopping early or asking unnecessary questions

**Cost:** 5–30 minutes. If the decision is reversible in <1 hour and low-risk → skip the method and just act.

---

## Core Rules

1. **Always have your own draft first.** DeepSeek critiques a position; it does not replace having one.
2. **One topic = one DeepSeek session/chat.** Keep all rounds for that topic in the same session.
3. **A materially new topic = a new DeepSeek session/chat.** Do not recycle old chats across unrelated tasks.
4. **First round must be context-heavy.** Give DeepSeek the full task, constraints, current draft, and the decision contract.
5. **For artifact review, paste the real artifact inline before the discussion.** Paste the actual code, config, or skill text first. Never send only a local path, filename, or vague summary and expect DeepSeek to read the file.
6. **HARD STOP RULE:** If you are about to send a DeepSeek prompt for artifact review and you have not pasted the real artifact text inline, stop immediately. Do not proceed. Go back and paste the real text. Sending only a path, filename, or summary is failed execution.
7. **Follow-up rounds must send only deltas.** Reuse the same session and send only the changed draft plus 1–3 remaining disagreements.
8. **Do not ask the user unnecessary clarifying questions mid-method.** If details are missing but non-critical, state assumptions and continue.
9. **Do not stop until you have written a decision.** After receiving DeepSeek's response, you must complete: compare → decide (take/keep/merge) → update draft → log. Stopping after criticism without a written decision is failure.
10. **Do not stop the topic early.** Keep doing rounds until both you and DeepSeek explicitly agree that further improvement is not worth the time, complexity, or risk.
11. **If DeepSeek surfaces a real patch, apply the patch before the next round unless the user asked for analysis only.** Do not stop at "recommendations" when the task is to improve the artifact.
12. **DeepSeek is a consultant, not final authority.** Compare and choose.
13. **Prefer simpler and safer when evidence is mixed.**
14. **Log the outcome.** One line per completed round.

---

## Execution

## Execution Algorithm (mandatory)

Follow this exact flow.

### Step 0 — Default to using unless clearly unnecessary
Use the method unless all three are true:
- the decision is reversible in <1 hour
- the risk is low
- confidence is already >90%

Strong triggers include:
- architecture or system design decision
- critical code/config review
- debugging after 2+ failed attempts
- confidence feels low
- trade-off between 2+ viable options
- user explicitly asks for a second brain / DeepSeek consultation

### Step 1 — Define the topic
Write a short topic slug for session naming.

Examples:
- `memory-v41`
- `synapse-reverse-proxy`
- `dual-thinking-v57`
- `openclaw-cron-audit`

**Rule:** session name describes the topic, not the method.
Never use generic names like `dual-thinking` or `review`.

### Step 2 — Draft your own position first
Before consulting DeepSeek, write:
- your current plan
- why you think it may be right
- where you are uncertain
- what failure or trade-off worries you most

If you cannot produce even a rough draft, you are not ready for dual-thinking yet.

### Step 3 — Choose chat/session behavior
- **Same topic:** same file/system/feature/bug/decision, same user goal, or round 2+ of the same consultation → reuse the same `--session <topic>` without `--new-chat`
- **New topic:** different system/problem/feature, different user goal, or old DeepSeek context would confuse more than help → create a new DeepSeek chat with `--session <topic>` + `--new-chat`
- **Stale or polluted session:** if the saved session name points to unrelated older context, rename the topic slug or force a new chat for that topic before continuing
- **Default:** when unsure, prefer new topic = new chat

### Step 4 — Build the first-round prompt
For round 1 of a topic, include all of the following:
- plain-language problem statement
- your current draft / preferred option
- goals
- constraints
- known facts
- assumptions
- the actual code / config / skill text inline when reviewing a real artifact
- the dual-thinking decision contract (short explicit algorithm)
- the exact questions you want DeepSeek to answer

The first prompt must be self-contained.
Assume DeepSeek knows nothing except what you send.

**Hard rule:** when the topic is about a real artifact, paste the real artifact first and only then explain the task. Do not send only a path like `skills/foo/SKILL.md`, `app/config.yaml`, or `script.sh`.

### Step 5 — Send round 1 to DeepSeek
Send the first-round prompt in a **new chat for the topic**.

### Step 6 — Compare and decide (both required)
Classify DeepSeek feedback:
- **Fact correction** → usually take his, then verify
- **Logic improvement** → consider seriously; merge if better
- **Context miss** → keep yours, explain why
- **Preference difference** → keep yours
- **Over-engineering** → reject unless justified by risk

After classification, write these three lines before you continue:

```text
COMPARISON: <Fact correction / Logic improvement / Context miss / Preference / Over-engineering>
DECISION: <Take DeepSeek / Keep mine / Merge>
UPDATED DRAFT: <one-sentence updated plan>
```

Do not continue until all three lines exist.

### Step 7 — Decide whether another round is needed
Default: continue.

Do another round whenever at least one is true:
- there is still a real disagreement
- a key risk is unresolved
- DeepSeek surfaced a flaw that changes the design
- DeepSeek surfaced a concrete patch worth applying
- your confidence is still too low to act
- either side can still name one concrete improvement worth testing
- you and DeepSeek have not yet explicitly agreed that another round is not worth it

Stop only after both conditions are true:
1. you cannot name a meaningful next improvement, risk, or disagreement
2. DeepSeek also explicitly agrees that further improvement is not worth the added time, complexity, or churn

**Hard rule for review / improvement tasks:**
- If the topic is reviewing or improving a real artifact (skill, code, config, doc, workflow), and DeepSeek surfaces a real fix, you must update the real artifact before asking whether the topic is done.
- Do not stop with only a recommendation list unless the user explicitly asked for analysis-only output.
- After applying the fix, run the next round in the same chat against the updated artifact or updated section.

If DeepSeek says the result is ready, finished, ideal, or ready to ship, do one explicit convergence check in the same chat:
- `We may stop only if we both agree there is no meaningful next improvement worth making. If you had to continue one more round, what exact improvement would you test? If none, say explicitly that further improvement is not worth it.`

If DeepSeek names a real improvement, apply it if accepted, then do another round.
If DeepSeek explicitly says further improvement is not worth it and you also agree, stop.

### Step 8 — If another round is needed, back up, patch, and continue in the same chat
Before round 2+:
- back up the current episodic note if relevant
- if you accepted a real fix, patch the real artifact first
- reuse the same topic session/chat
- send only the updated draft, updated artifact section, disagreement, and new question

### Step 9 — Log the outcome (required)
Write exactly one line starting with `LOG:` using this format:

```text
LOG: Round <N> — <kept/changed/merged> — <one reason>
```

Valid examples:
- `LOG: Round 1 — changed to simpler grep solution — DeepSeek correctly called over-engineering`
- `LOG: Round 2 — kept my approach — DeepSeek missed local constraint`
- `LOG: Round 3 — merged both — added rollback path`

Invalid examples:
- `LOG: done`
- `LOG: reviewed`
- `LOG: ok`

---

## Hard Rule: When to Assume vs Ask

Assume and continue when:
- the missing detail is a number, name, or path
- the missing detail affects performance but not correctness
- the user's intent is clear but lacks specificity

When assuming, state it explicitly in the prompt to DeepSeek using `Assumption:`.

Ask only when all three are true:
1. without the detail you cannot produce a safe answer
2. the user likely knows the answer
3. the question fits in one short sentence

If you ask, use this format:
- `[NEED: <one specific thing>]`

Examples:
- `Assumption: the service runs on a single-user host, not a multi-tenant cluster.`
- `Assumption: rollback is available via git and PM2 restart.`
- `[NEED: which database engine?]`

---

## First-Round Prompt Contract (mandatory)

For the **first round of every new topic**, use a structure like this.

```markdown
## Dual Thinking — Round 1

### Topic
<short topic slug>

### Problem
<plain-language description of the task / decision>

### My Current Position
<what I currently think should be done>

### Why I Lean This Way
- <reason 1>
- <reason 2>
- <reason 3>

### What I'm Unsure About
- <doubt 1>
- <doubt 2>

### Goals
- <goal 1>
- <goal 2>

### Constraints
- <constraint 1>
- <constraint 2>

### Known Facts
- <fact 1>
- <fact 2>

### Assumptions
- <assumption 1>
- <assumption 2>

### Task Material
<paste the real code / config / skill text / logs. Required for any review task. Do not skip>

### Dual-Thinking Contract
Please act as a critical consultant, not a cheerleader.
1. Find the weak points in my current position.
2. Propose the simplest safer alternative.
3. Call out over-engineering if present.
4. Distinguish fact errors from preference differences.
5. End with: (a) what to keep, (b) what to change, (c) what risk remains.

### Questions
1. What are my blind spots?
2. What would you do differently?
3. What is the simplest safe version?
```

### Rules for first-round payload
- For **code/config review**, paste the relevant real code/config inline.
- For **skill review**, paste the relevant skill text inline.
- For **architecture**, include current topology/constraints, not just the idea.
- Put the real artifact text before or together with your explanation. Do not make DeepSeek wait for later rounds to see the artifact.
- Do not send only a file path or short summary and expect DeepSeek to infer the rest.
- If the artifact is long, send the most relevant contiguous section inline and say explicitly that the pasted section is the review target.

**WRONG (do not do this):**
```markdown
### Topic
review dual-thinking

### Task Material
skills/dual-thinking/SKILL.md
```

**RIGHT (always do this):**
```markdown
### Topic
review dual-thinking

### Task Material
---SKILL START---
[paste the real SKILL.md text here]
---SKILL END---
```

---

## Follow-up Round Contract (mandatory)

For round 2+ of the **same topic**, reuse the same DeepSeek session/chat and use a smaller structure.

```markdown
## Dual Thinking — Round N

### Topic
<same topic slug>

### Current Draft After Last Round
<updated plan>

### What I Accepted From You
- <accepted item 1>
- <accepted item 2>

### What I Rejected From You
- <rejected item 1> — because <reason>

### Remaining Disagreement / Risk
- <open issue>

### New Question
<the next specific challenge>
```

### Follow-up rules
- Do **not** start a new chat for round 2+ of the same topic.
- Do **not** resend the full algorithm unless DeepSeek lost the thread.
- Resend only the deltas, updated plan, and open disagreement.
- For review / improvement tasks, include the **actual modified section** after you patch it. Do not ask DeepSeek to review a patch you have not applied.
- If the previous response was weak, say so directly and focus the next question.
- If DeepSeek misunderstood because it lacked the real artifact text, correct that immediately by pasting the real text in the next round. Do not keep arguing at the level of summaries.
- Near the end, ask explicitly whether DeepSeek sees any worthwhile next improvement. Do not infer agreement from tone; get a direct statement.

---

## Tool Usage (mandatory)

Run these commands from the OpenClaw workspace root so the relative path `skills/ai-orchestrator/ask-deepseek.sh` resolves correctly.
If you are not already in the workspace root, run:

```bash
cd ~/.openclaw/workspace
```

Then use:

```bash
TOPIC="short-topic-name"
SESSION="dt-${TOPIC}"
# `--daemon` keeps the ai-orchestrator browser path warm for faster, more stable repeated rounds.

# Round 1 of a NEW topic: force a NEW DeepSeek chat
bash skills/ai-orchestrator/ask-deepseek.sh \
  "<full round-1 prompt>" \
  --session "$SESSION" \
  --new-chat \
  --daemon

# Round 2+ of the SAME topic: same session, same DeepSeek chat
bash skills/ai-orchestrator/ask-deepseek.sh \
  "<follow-up prompt>" \
  --session "$SESSION" \
  --daemon

# Close when the topic is finished
bash skills/ai-orchestrator/ask-deepseek.sh \
  --session "$SESSION" \
  --end-session
```

---

## Stop Rules

Stop only when all required completion conditions are satisfied:
- you have completed compare → decide → update → log for the current round
- you cannot name a meaningful next improvement, unresolved risk, or real disagreement
- DeepSeek explicitly agrees that further improvement is not worth the added time, complexity, or churn

These signals support stopping, but are not sufficient by themselves unless the explicit mutual-agreement condition above is also true:
- the remaining disagreement is only preference
- no new actionable insight appeared this round
- the answer is now obvious enough to act
- 2 consecutive rounds produced no new insight
- time spent exceeded the value of another round
- DeepSeek says the result is ready

If DeepSeek says **“ideal / ready to ship”**, do an explicit convergence check:
- `We stop only if we both agree there is no meaningful next improvement worth making. If you had to continue one more round, what exact improvement would you test? If none, say explicitly that further improvement is not worth it.`

If the answer names a real improvement → continue.
If the answer explicitly says further improvement is not worth it and you also agree → stop.
If you cannot complete the round because the user gave insufficient context → ask one brief clarifying question; if still blocked after the answer, stop with `[ABORT: insufficient context for safe decision]`.

---

## Anti-Patterns

| Anti-pattern | Why it fails | What to do instead |
|---|---|---|
| "Let me know how to proceed" / "I'll wait for your response" / "Ready when you are" | Looks polite but stalls execution | Proceed to the next step immediately |
| Starting every round in a new chat | Loses DeepSeek context | New topic only → new chat; same topic → same chat |
| Reusing one old chat for unrelated topics | Pollutes context | Start a new topic chat |
| Sending only a file path | DeepSeek cannot open local files | Paste the real material inline first |
| Asking DeepSeek before having your own draft | Invites vague advice | Draft first |
| Asking the user to continue after each substep | Breaks autonomy | Complete the round in one go |
| Stopping after criticism without deciding | Analysis without outcome | Compare and choose |
| Copy-pasting DeepSeek blindly | Outsourcing judgment | Classify, compare, decide |
| Over-focusing on formatting rules | Bureaucracy over substance | Keep the structure, but optimize for useful critique |
| Repeating the full 10-step algorithm in follow-up rounds | Wastes tokens and confuses DeepSeek | After round 1, send only deltas |

---

## Skill Review Mode

When the topic is a skill review/improvement:
- start a new topic chat for that skill
- paste the relevant `SKILL.md` text inline in round 1 before or together with your explanation
- include current pain points and desired behavior changes
- ask DeepSeek to critique both content and operability
- if DeepSeek surfaces an accepted fix, patch the real `SKILL.md` before the next round
- for later rounds, send only modified sections and the remaining disagreement
- stop only after the patched `SKILL.md` has been reviewed in the same chat and both sides explicitly agree no further worthwhile improvement remains

Do not ask DeepSeek to infer the skill from its name. Do not rely on local paths. Paste the text.

---

## Optional Backup

If the environment uses episodic memory and the topic matters enough to preserve between rounds, save a backup before round 2+.
This is optional environment hygiene, not required for the reasoning method itself.

```bash
EP_FILE="memory/episodic/$(date +%Y-%m-%d).md"
if [[ ! -f "$EP_FILE" ]]; then echo "# $(date +%Y-%m-%d)" > "$EP_FILE"; fi
cp "$EP_FILE" references/dual-thinking-backup-$(date +%Y%m%d-%H%M%S).md
```

Retention:

```bash
find references/ -name "dual-thinking-backup-*.md" -mtime +30 -delete
ls -t references/dual-thinking-backup-*.md | tail -n +11 | xargs -r rm -f
```

---

## Worked Example

**Topic:** `memory-v41`

### Round 1
- My draft: add vector DB
- DeepSeek: overkill; use grep + cache
- My comparison: DeepSeek is right for current scale
- Decision: reject vector DB

### Round 2
- My updated draft: grep + TTL cache
- DeepSeek: watch cache invalidation
- My comparison: good point; add rebuild strategy
- Decision: keep TTL, add periodic rebuild

### Stop
- no meaningful disagreement remains
- plan is implementable
- confidence is good enough

---

## What Good Execution Looks Like

A strong execution produces:
- a clear topic-specific DeepSeek chat
- a complete round-1 prompt with real context
- no unnecessary pause for clarifications
- an explicit comparison, decision, and updated draft
- when reviewing a real artifact, an actual patch before the next review round
- a valid `LOG:` line

---

## Pre-Flight Check for Review / Improvement Tasks

Before sending a review prompt, verify all of these:
- The review target is pasted inline.
- The review target is not referenced only by path.
- If the artifact is long, the pasted section is clearly marked as the review target.
- The explanation comes after or together with the real artifact text.

If any item above is false, stop and fix the prompt before sending it.

---

## Completion Check for Review / Improvement Tasks

Before stopping, verify all of these:
- I compared DeepSeek's latest response and made a decision.
- I logged the round.
- The review target was pasted inline, not referenced only by path.
- If a real patch was accepted, I applied the patch to the real artifact.
- The next round reviewed the patched artifact or patched section in the same topic chat.
- DeepSeek explicitly said no further worthwhile improvement remains.
- I also agree no further worthwhile improvement remains.

If any item above is false, the topic is not finished.

---

## Known Limits

- DeepSeek can still over-engineer; keep the simplicity bias.
- Some topics do not benefit from more than one round.
- If the user gives almost no context, the skill still needs a minimal draft before consultation.
- Visible/headful browser behavior depends on ai-orchestrator and host GUI availability.
