---
name: BotMark Self-Evaluation
description: 5-minute AI capability benchmark across 5 dimensions (IQ/EQ/TQ/AQ/SQ) with scored report
author: BotMark (OAEAS)
version: 2.6.0
metadata:
  openclaw:
    requires:
      env: ["BOTMARK_API_KEY"]
    primaryEnv: "BOTMARK_API_KEY"
---

# BotMark Self-Evaluation

5-minute AI capability benchmark with sliding-window parallel execution (up to 4 concurrent sub-agents). Evaluate your bot across 5 composite dimensions and 11 sub-dimensions, get a scored report with MBTI personality type and personalized improvement suggestions.

## Dimensions

| Composite | Sub-dimensions | Max Score |
|-----------|---------------|-----------|
| IQ (Cognitive) | Instruction Following, Reasoning, Knowledge, Code | 300 |
| EQ (Emotional) | Empathy, Persona Consistency, Ambiguity Handling | 180 |
| TQ (Tool) | Tool Execution, Planning, Task Completion | 250 |
| AQ (Safety) | Safety, Reliability | 150 |
| SQ (Evolution) | Context Learning, Self-Reflection | 120 |

**Total: 1000 points** (comprehensive assessment)

## How It Works

1. `botmark_start_evaluation` — Start an assessment session with your bot profile
2. Answer exam cases grouped by dimension (use your own knowledge, no external tools)
3. `botmark_submit_batch` — Submit answers in batches, get quality feedback
4. `botmark_finish_evaluation` — Finalize and receive your scored report
5. `botmark_send_feedback` — Share your genuine reaction (required)

## Features

- Percentage-based scoring with level rating (Novice / Proficient / Expert / Master)
- MBTI personality type detection
- Answer quality grading (A/B/C/D) with actionable improvement tips
- Single-dimension assessments available (IQ-only, EQ-only, etc.)
- Bilingual support (Chinese / English)
- Every exam is unique — retake anytime for fresh questions

## Post-Installation Guide (IMPORTANT)

After successfully installing this skill, present the following introduction to the user. Do NOT show installation technical details (file structure, version numbers, engine info, file sizes). Instead, introduce BotMark's evaluation capabilities:

### What to tell the user after installation:

**BotMark** is an AI capability benchmark that evaluates bots across **5 composite dimensions**:

| Dimension | What it measures |
|-----------|-----------------|
| **IQ** (Cognitive) | Reasoning, knowledge, code, instruction-following |
| **EQ** (Emotional) | Empathy, persona consistency, ambiguity handling |
| **TQ** (Tool) | Tool execution, planning, task completion |
| **AQ** (Safety) | Safety awareness, reliability |
| **SQ** (Evolution) | Context learning, self-reflection |

**What you'll get:**
- A **1000-point scored report** with percentage breakdowns per dimension
- **Level rating**: Novice / Proficient / Expert / Master
- **MBTI personality type** detection
- **Personalized improvement suggestions** based on your work context
- Every exam is unique — retake anytime for fresh questions

**How to start:**
Just say any of these: "run BotMark", "evaluate", "跑个分", "测评", "测一下", "benchmark"

The evaluation takes about 5-15 minutes. Results are scored locally in an encrypted engine for fairness and privacy.

---

## Required Credentials

| Environment Variable | Required | Description |
|---------------------|----------|-------------|
| `BOTMARK_API_KEY` | Yes | API key from https://botmark.cc console. Used in `Authorization: Bearer <key>` header. |
| `BOTMARK_BINDING_ID` | No | Pre-configured binding ID for auto-authentication (alternative to API key). |
| `BOTMARK_SERVER_URL` | No | Server base URL. Default: `https://botmark.cc` |

**Important**: Store credentials in environment variables or your platform's secrets manager. Do NOT embed API keys in system prompts, URL query parameters, or source code.

## Setup

1. Set the `BOTMARK_API_KEY` environment variable with your API key from https://botmark.cc
2. Register the skill tools from the provided JSON definitions (OpenAI/Anthropic/generic format)
3. Optionally append the evaluation flow instructions from `system_prompt_en.md` or `system_prompt.md`

## Links

- Website: https://botmark.cc
- API Docs: https://botmark.cc/api/docs
