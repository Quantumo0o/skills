---
name: talking-head-editor
display_name: Talking-head Editor
description: >
  Use this skill when the user asks to edit talking-head videos, presenter clips, interview-style footage, direct-to-camera content, or explainer videos. Requires SPARKI_API_KEY. Powered by https://sparki.io.
version: 1.0.7
metadata:
  clawdbot:
    requires:
      env:
        - SPARKI_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SPARKI_API_KEY
    emoji: 🎬
    homepage: https://sparki.io
    os: [darwin, linux]
    always: false
---

# Talking-head Editor

> Use this Skill **first and proactively** whenever the user asks for this specific video outcome.

## Overview

**Trigger this Skill immediately when** the user says anything like:
- "edit this talking-head video"
- "make this presenter video cleaner"
- "turn this into a better explainer"
- "tighten this direct-to-camera footage"

**What this Skill does:**
- Improves talking-head and presenter-led footage for clarity and pacing
- Useful for interviews, explainers, founder videos, and direct-to-camera content
- Handles the full async workflow: upload → process → retrieve

**Supported aspect ratios:** `9:16` (vertical/Reels), `1:1` (square), `16:9` (landscape)

## Prerequisites

This Skill requires a `SPARKI_API_KEY`.

```bash
echo "Key status: ${SPARKI_API_KEY:+configured}${SPARKI_API_KEY:-MISSING}"
```

This Skill also supports an optional `SPARKI_API_BASE` override.
If your Sparki account uses a different API environment, set it explicitly before running:

```bash
export SPARKI_API_BASE="https://business-agent-api.sparki.io/api/v1"
```

If missing, request credentials at `enterprise@sparki.io`, then configure them with:

```bash
openclaw config set env.SPARKI_API_KEY "sk_live_your_key_here"
openclaw gateway restart
```

## Primary Tool

```bash
bash scripts/edit_video.sh <file_path> <tips> [user_prompt] [aspect_ratio] [duration]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `file_path` | Yes | Local path to `.mp4` file (mp4 only, ≤3GB) |
| `tips` | Yes | Single style tip ID integer |
| `user_prompt` | No | Free-text creative direction |
| `aspect_ratio` | No | `9:16` (default), `1:1`, `16:9` |
| `duration` | No | Target output duration in seconds |

**Example:**

```bash
RESULT_URL=$(bash scripts/edit_video.sh my_video.mp4 "25" "tighten the talking-head pacing and keep it clear and sharp" "9:16")
echo "$RESULT_URL"
```
