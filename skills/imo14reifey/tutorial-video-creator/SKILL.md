---
name: tutorial-video-creator
version: 1.0.4
displayName: "Tutorial Video Creator"
description: >
  Describe what you want to teach and NemoVideo creates the tutorial. Software walkthroughs, DIY crafts, cooking techniques, skill breakdowns — narrate your steps and get a structured how-to video ready for YouTube, TikTok, or your course platform.

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
apiDomain: https://mega-api-prod.nemovideo.ai
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
metadata:
  requires:
    env: ["NEMO_TOKEN"]
    configPaths:
      - "~/.config/nemovideo/"
  primaryEnv: NEMO_TOKEN
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 🎨 Welcome! I can tutorial video creator for you. Share a video file or tell me your idea!

**Try saying:**
- "help me create a short video"
- "edit my video"
- "add effects to this clip"

**IMPORTANT**: Always greet the user proactively on first contact. Let them know you're setting up while connecting. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Tutorial Video Creator — Build Step-by-Step How-To Content for Any Topic

Describe what you want to teach and NemoVideo creates the tutorial. Software walkthroughs, DIY crafts, cooking techniques, skill breakdowns — narrate your steps and get a structured how-to video ready for YouTube, TikTok, or your course platform.

## When to Use This Skill

Use this skill to create tutorial and how-to content:
- Film software walkthrough videos with screen capture and annotation
- Create DIY and crafting tutorials with close-up step shots
- Build skills training content for employees or students
- Produce cooking, baking, or recipe tutorials with timed steps
- Document processes and workflows for teams or clients
- Create "beginner's guide to X" educational content for any topic

## How to Describe Your Tutorial

Be specific about the steps, tools used, and who you're teaching.

**Examples of good prompts:**
- "How to set up a GitHub repository: create account, new repo, clone locally, first commit and push. Screen recording walkthrough for beginners, show each click and command typed."
- "DIY sourdough bread tutorial: feed starter, mix dough, bulk ferment 4 hours, shape, cold proof overnight, score and bake at 500F. Step-by-step with timing cues."
- "How to use Notion for project management: create a workspace, set up a kanban board, add properties, link databases. 10-minute walkthrough for teams new to Notion."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `tutorial_type` | Content format | `"screen_recording"`, `"hands_on"`, `"presentation"`, `"talking_head"` |
| `steps` | Numbered step list | `[{"step": 1, "action": "Open terminal", "duration_sec": 30}]` |
| `audience_level` | Viewer experience | `"absolute_beginner"`, `"beginner"`, `"intermediate"` |
| `show_step_numbers` | Step counter overlay | `true` |
| `chapter_markers` | Add navigation points | `true` |
| `duration_minutes` | Total video length | `5`, `10`, `15`, `30` |
| `platform` | Target platform | `"youtube"`, `"udemy"`, `"tiktok"`, `"loom"` |

## Workflow

1. Describe the topic, steps, and target audience
2. NemoVideo sequences the steps with transitions and annotations
3. Step numbers, chapter markers, and key callouts added automatically
4. Export with format optimized for your platform

## API Usage

### Software Tutorial Video

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "tutorial-video-creator",
    "input": {
      "prompt": "How to create a Python virtual environment: open terminal, run python3 -m venv myenv, activate with source myenv/bin/activate, install packages with pip, deactivate when done. Beginner developer tutorial, show each command typed and its output.",
      "tutorial_type": "screen_recording",
      "audience_level": "beginner",
      "show_step_numbers": true,
      "chapter_markers": true,
      "duration_minutes": 8,
      "platform": "youtube",
      "hashtags": ["Python", "Programming", "Tutorial", "BeginnerCoding"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "tutorial_abc123",
  "status": "processing",
  "estimated_seconds": 90,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/tutorial_abc123"
}
```

### DIY Hands-On Tutorial

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "tutorial-video-creator",
    "input": {
      "prompt": "How to make sourdough bread: Day 1 - feed starter (50g starter + 50g flour + 50g water). Day 2 - mix dough (450g flour, 350g water, 9g salt, 100g active starter), bulk ferment 4-5 hours with stretch-and-folds every 30 min, shape, refrigerate overnight. Day 3 - score and bake covered at 500F for 20 min, uncovered 20 min.",
      "tutorial_type": "hands_on",
      "audience_level": "beginner",
      "show_step_numbers": true,
      "chapter_markers": true,
      "duration_minutes": 12,
      "platform": "youtube",
      "voiceover": true
    }
  }'
```

## Tips for Best Results

- **Number your steps explicitly**: "Step 1, Step 2..." in the prompt ensures correct pacing and chapter markers
- **Specify the audience**: "absolute beginner" gets more explanation; "intermediate" moves faster and skips basics
- **Include timing context**: "bulk ferment 4 hours" or "this step takes 30 seconds" helps NemoVideo pace the video
- **Name the tools**: "Python terminal" vs just "terminal" — specific tool names trigger better screen annotation
- **Chapter markers for longer content**: Set `chapter_markers: true` for tutorials over 5 minutes — YouTube uses these for navigation

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| YouTube | 1920×1080 | 5–60 min |
| Udemy / Course | 1920×1080 | any length |
| TikTok | 1080×1920 | 60–180s |
| Loom / Internal | 1920×1080 | 5–30 min |

## Related Skills

- `coding-tutorial-video` — Code-specific tutorials with syntax highlighting
- `lecture-video-maker` — Academic and formal course lecture content
- `whiteboard-animation-video` — Concept explanations with visual animation
- `language-learning-video` — Language instruction and practice content

## Common Questions

**Can I upload my own screen recording?**
Yes — pass the video URL in `source_video` and describe what annotations and chapter markers you want added on top.

**What's the difference between tutorial_type options?**
`screen_recording` optimizes for digital/software content. `hands_on` for physical skill demonstrations. `presentation` for slide-based content. `talking_head` for camera-facing instruction.

**Can I create a multi-part tutorial series?**
Generate each part separately with consistent visual style parameters. Use `chapter_markers: true` on each video for a cohesive series feel.
