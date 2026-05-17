---
name: digital-twin
description: >
  Build a psychologically grounded Digital Twin personality skill from Fireflies meeting transcripts.
  Use this skill whenever the user asks to create a digital twin, personality clone, shadow persona,
  AI stand-in, or personality skill for a specific person. Also trigger when the user says things like
  "make an AI version of [name]", "clone [name]'s personality", "build a persona for [name]",
  "create a shadow skill for [name]", or "I want the agent to respond as [name]". This skill does
  NOT connect to Fireflies directly and does NOT require or store any Fireflies credentials — it
  depends on the user's own separately-installed Fireflies skill/connector to retrieve transcripts.
  The user controls which Fireflies skill is used, what account it connects to, and what transcript
  access it has. This skill is a consumer of transcript data, not a transcript provider. The output
  is an installable personality skill that makes Claude respond as that person would — matching their
  speech patterns, thinking style, decision-making, and audience-awareness. This skill does NOT handle
  memory or factual recall — it builds personality, voice, and judgment. Pair it with a vector
  database for memory if full digital twin fidelity is needed.
---

# Digital Twin Skill — Personal AI Stand-In Builder

## Purpose

This skill analyzes a person's Fireflies meeting transcripts across four psychological and linguistic pillars to produce an installable **personality skill** — a structured persona document that makes Claude speak, think, decide, and adapt to audiences the way that person actually does. The output skill is named `{name}_personality` (e.g., `joes_personality`) and can be used by any agent or user instruction like "respond as if you were Joe" or set as a default persona for all communications.

---

## Prerequisites

Before starting, verify:

1. **The user has their own Fireflies skill/connector installed and working.** This skill does NOT connect to Fireflies itself. It does NOT require, request, or store any Fireflies API keys, tokens, or credentials. Instead, it depends on a separate Fireflies skill or MCP connector that the user has already installed and configured independently, using their own Fireflies account and their own access permissions. If the user does not have a Fireflies skill installed, tell them to install and configure one first (pointing them to their platform's skill/connector marketplace), then come back. This skill will call the user's Fireflies skill to retrieve transcripts — it is a consumer of that skill's capabilities, not a Fireflies integration itself.
2. **Sufficient transcript volume.** A minimum of 5 transcripts featuring the target person is recommended. 10+ transcripts across varied meeting types (1:1s, team meetings, leadership reviews, cross-functional calls) produces dramatically better results. If fewer than 5 are available, warn the user that the personality profile will be shallow and may not capture audience adaptation or decision patterns well.
3. **Target person is identifiable in transcripts.** The person's name must appear as a speaker label in the transcripts. Ask the user to confirm the exact name as it appears in Fireflies if there's any ambiguity.

### Consent & Privacy

Before proceeding with any analysis, confirm the following with the user:

- **Target person consent**: The user should have the target person's knowledge and consent before building a personality profile of them. If the user is building a profile of themselves, this is implicit. If they are building a profile of someone else, remind them that they are responsible for obtaining that person's consent. Do not proceed until the user confirms consent.
- **Third-party data**: Transcripts contain contributions from other meeting participants. This skill extracts ONLY the target person's contributions for analysis. Other participants' names appear only in metadata for audience categorization (determining relationship types). No personality analysis is performed on non-target participants.
- **Data handling**: All analysis is performed in-session. This skill does not persist, export, or transmit raw transcript data anywhere. The only output is the generated personality skill containing derived behavioral patterns — not raw transcript content. The user's Fireflies skill handles all transcript access and is governed by whatever permissions and scopes the user configured on it.

---

## User Invocation Patterns

The user triggers this skill with a request like:

> "Use the digital twin skill to create a personality skill for John Doe using the last 10 meeting transcripts."

The key parameters to extract from the user's request:

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| **Target person name** | Yes | — | "John Doe" |
| **Number of transcripts** | No | 10 | "last 15 meetings" |
| **Additional context** | No | — | "He's the VP of Engineering, tends to be very direct" |
| **Audience types to focus on** | No | Auto-detect | "Focus on his leadership meetings and 1:1s" |

If the user doesn't specify transcript count, default to 10. Inform them: more transcripts = longer processing time but richer personality capture. Each transcript is analyzed individually before compositing.

---

## Execution Workflow

### Phase 1: Transcript Retrieval

Use the user's installed Fireflies skill/connector to pull the requested number of recent meeting transcripts. This skill does not connect to Fireflies directly — it calls the user's own Fireflies skill, which handles authentication and access using the user's own credentials and scopes.

1. Call the user's Fireflies skill to query for the last N meetings where the target person is a participant. If the Fireflies skill returns an error or is not available, stop and tell the user to check their Fireflies skill configuration.
2. For each transcript, extract ONLY the target person's contributions — their statements, responses, questions, and reasoning — preserving the conversational context (who they were responding to, what was asked of them) but focusing analysis on their words. Do not retain or analyze other participants' speech content.
3. Tag each transcript with metadata:
   - Meeting date
   - Meeting title/topic
   - Participants list (to determine audience type)
   - Duration of target person's contributions vs. total meeting
4. Categorize each meeting by audience type for Pillar 4 analysis:
   - **Leadership/Upward**: Meetings with their superiors or executive leadership
   - **Peer/Lateral**: Meetings with colleagues at similar level
   - **Direct Report/Downward**: Meetings with people they manage
   - **Cross-Functional**: Meetings with people from other departments
   - **External**: Client calls, vendor meetings, partner discussions
   - **Mixed**: Large meetings with multiple relationship types

Store extracted contributions in a working structure organized by transcript.

### Phase 2: Four-Pillar Analysis

Process EACH transcript individually through all four pillars. This is critical — do not batch or summarize transcripts before analysis. Each transcript gets its own pillar scores and observations. The composite comes AFTER individual analysis.

Read the detailed methodology for each pillar from the references directory:

- **Pillar 1 — Linguistic Profiling**: Read `references/pillar_1_linguistic.md`
- **Pillar 2 — Psychometric Profiling**: Read `references/pillar_2_psychometric.md`
- **Pillar 3 — Judgment & Decision Patterns**: Read `references/pillar_3_judgment.md`
- **Pillar 4 — Contextual Audience Profiling**: Read `references/pillar_4_audience.md`

For each transcript, produce a structured analysis document covering all four pillars. Then proceed to compositing.

### Phase 3: Composite Profile Generation

After all transcripts are individually analyzed:

**Pillar 1 — Linguistic Composite:**
- Merge all linguistic observations into a unified style guide
- Identify patterns that appear in 60%+ of transcripts as "core patterns"
- Note patterns that appear in fewer as "situational patterns" tied to specific contexts
- Resolve contradictions by weighting more recent transcripts slightly higher

**Pillar 2 — Psychometric Composite:**
- For each OCEAN dimension: average the per-transcript scores to get a final score (1-100 scale)
- Calculate standard deviation — high deviation means the person's expression of that trait is context-dependent (note this)
- Composite the conflict style, risk tolerance, and communication priority assessments using majority-vote across transcripts
- Write the psychometric narrative summary (see Pillar 2 reference for format)

**Pillar 3 — Judgment Composite:**
- Merge all decision pattern observations into a unified decision pattern library
- Build the stance map from consistent positions observed across 2+ transcripts
- Document reasoning chains with representative examples
- Flag any stances that shifted over time (evolution of thinking)

**Pillar 4 — Audience Composite:**
- For each audience category that had sufficient data (2+ meetings), produce a distinct communication profile
- If an audience category only has 1 meeting, mark it as "preliminary — low confidence"
- Identify the person's default/baseline mode (most common audience type)

### Phase 4: Personality Skill Assembly

Using the composite profiles, generate the installable personality skill. The skill uses the template in `references/personality_skill_template.md` and is output as a complete skill directory:

```
{name}_personality/
├── SKILL.md          (the personality skill itself)
└── references/
    ├── linguistic_profile.md
    ├── psychometric_profile.md
    ├── decision_patterns.md
    └── audience_profiles.md
```

The generated SKILL.md must include:

1. **Frontmatter** with a description that triggers on "respond as {name}", "be {name}", "use {name}'s personality", or when the skill has been set as default for all communications.
2. **Response Generation Pipeline** — the step-by-step instruction set telling Claude how to process any incoming message through the personality:
   - Step 1: Identify the audience context (who is being spoken to, what's the relationship)
   - Step 2: Select the matching audience communication profile
   - Step 3: Match the question/topic to a decision pattern category if applicable
   - Step 4: Check the stance map for any pre-existing positions on the topic
   - Step 5: Generate the response content using the judgment profile and psychometric tendencies
   - Step 6: Pass the draft through the linguistic filter with the correct audience mode
   - Step 7: Final check — does this read like {name} wrote it, to this specific person?
3. **Quick-reference persona card** at the top of SKILL.md summarizing OCEAN scores, core linguistic markers, and top 5 stance positions for fast context loading.
4. **Pointers to reference files** for the full profiles, with guidance on when to consult each one.

### Phase 5: Installation and Delivery

1. Package the personality skill directory.
2. Present it to the user with a summary:
   - OCEAN scores with brief interpretation
   - Top linguistic markers identified
   - Number of decision patterns captured
   - Audience profiles generated (and confidence level for each)
   - Any caveats or gaps (e.g., "No external meeting data was available, so client-facing behavior is not captured")
3. Explain how to use it:
   - Install the skill in their agent's skill directory
   - To always use it: set it as a default skill in the agent's configuration
   - To use on-demand: say "respond as if you were {name}" or "use {name}'s personality"
4. Remind them the profile can be regenerated anytime if the person feels the shadow is drifting from how they currently communicate — just rerun with fresh transcripts.

---

## Important Processing Notes

- **One transcript at a time.** Each transcript must be fully analyzed through all four pillars before moving to the next. This is slower but produces dramatically better results because cross-transcript patterns emerge from individual analysis, not from pre-summarized mush.
- **The more transcripts, the longer it takes.** Set expectations with the user. A 10-transcript build may take significant processing time. A 20-transcript build will take roughly twice as long.
- **User-provided context helps.** If the user says "He's the CTO and tends to be very data-driven," that context helps calibrate the analysis — especially for audience categorization and understanding the person's position in the org hierarchy.
- **This is personality, not memory.** The skill captures HOW someone thinks and communicates, not WHAT they know or remember. For a full digital twin, pair with a vector database containing their domain knowledge and conversation history.

---

## Rerun / Update Protocol

If the user asks to update an existing personality skill:

1. Use the user's Fireflies skill to pull new transcripts (user specifies how many)
2. Run the full four-pillar analysis on the new transcripts
3. Blend with the existing profile, weighting new data at 60% and existing at 40% (recency bias — people evolve)
4. Regenerate the skill with the updated composite
5. Note what changed in the update summary

---

## Reference Files

| File | When to Read | Purpose |
|------|-------------|---------|
| `references/pillar_1_linguistic.md` | Phase 2, for each transcript | Full linguistic analysis methodology |
| `references/pillar_2_psychometric.md` | Phase 2, for each transcript | OCEAN scoring rubric and psychometric assessment method |
| `references/pillar_3_judgment.md` | Phase 2, for each transcript | Decision pattern extraction and stance mapping method |
| `references/pillar_4_audience.md` | Phase 2, for each transcript | Audience-adaptive communication profiling method |
| `references/personality_skill_template.md` | Phase 4 | Template for the generated personality skill |
