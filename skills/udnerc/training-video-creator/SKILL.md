---
name: training-video-creator
version: "1.0.0"
displayName: "Training Video Creator — Make Corporate Training and Onboarding Videos"
description: >
  Training Video Creator — Make Corporate Training and Onboarding Videos.
metadata: {"openclaw": {"emoji": "🏢", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Training Video Creator — Corporate Training and Onboarding Videos

NemoVideo's training video creator produces the five categories of corporate training content that L&D departments deliver every quarter: compliance training (the videos employees are legally required to watch), onboarding sequences (the videos that turn a new hire into a functioning team member), process documentation (the videos that replace the 40-page SOP nobody reads), soft-skills development (the videos that teach managers to give feedback without causing resignations), and product training (the videos that teach sales teams what the product actually does before they start promising features that don't exist). Each category has different requirements — compliance needs completion tracking and quiz integration, onboarding needs personality and culture communication, process docs need screen recordings with annotations, soft skills need scenario role-plays, and product training needs demo recordings with feature callouts — and this tool handles all five without requiring five different production workflows.

## Core Capabilities

- **Screen recording + annotation** — Capture software workflows with automatic step-numbering, click-highlight circles, and zoom-to-region when UI elements are small
- **Scenario branching** — Create choose-your-own-path training where the viewer selects a response and sees the consequence play out
- **Quiz integration** — Insert multiple-choice, true/false, or drag-and-drop knowledge checks at specified intervals with pass/fail tracking
- **Multi-language support** — Generate translated captions and AI voiceover in 30+ languages from a single English source recording
- **SCORM/xAPI export** — Package videos with completion tracking metadata for any standards-compliant LMS
- **Brand templating** — Apply consistent intro/outro, lower-thirds, color scheme, and logo placement across an entire training library

## Use Cases

1. **New Hire Onboarding Series** — Produce a 5-video onboarding sequence: company history and culture (3 min), org structure and your team (4 min), tools and systems setup (8 min with screen recording), HR policies and benefits overview (5 min), and first-week expectations with manager introduction (3 min). Total: 23 minutes replacing a full-day orientation that new hires rated 2.1/5 in satisfaction surveys.
2. **Annual Compliance Training** — Create the legally mandated harassment prevention, data privacy (GDPR/CCPA), workplace safety, and ethics training modules. Each module: 10-15 minutes with scenario-based examples, followed by a graded quiz (80% pass threshold). SCORM-packaged for LMS tracking with completion certificates auto-generated.
3. **Software Rollout Training** — The company is migrating from Salesforce Classic to Lightning. Produce 12 micro-training videos (3-5 min each) covering the most common workflows: creating a lead, logging an activity, running a report, building a dashboard. Screen recordings with click annotations, before/after comparisons, and a "try it yourself" prompt at the end of each video.
4. **Manager Development Program** — Build a 6-module soft-skills series: giving feedback, running 1:1s, handling conflict, delegating effectively, conducting performance reviews, and supporting struggling employees. Each module: a 2-minute concept explanation, a 3-minute scenario role-play (good example and bad example side by side), and a 1-minute action-item summary.
5. **Sales Enablement Library** — Produce product training for a sales team launching a new feature. Videos: feature overview (what it does, 3 min), competitive positioning (how it compares, 4 min), objection handling (common pushbacks with scripted responses, 5 min), and demo walkthrough (how to show it to a prospect, 6 min).

## How It Works

### Step 1 — Define Training Scope
Specify the training category, target audience (new hires, all employees, managers, sales), required compliance standards, and LMS platform.

### Step 2 — Provide Source Material
Upload raw recordings, slide decks, SOPs, scripts, or subject-matter-expert interview footage. NemoVideo can also generate training content from a written outline alone using AI narration and stock-footage assembly.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "training-video-creator",
    "prompt": "Create Module 2 of new-hire onboarding: Org Structure and Your Team. Open with animated org chart showing company divisions (Engineering, Product, Sales, Operations, HR). Zoom into the Engineering division where the new hire sits. Show team photo with names and roles. Manager appears on camera: 60-second welcome message explaining team mission and how the new hire fits in. Close with interactive org chart where viewer can click departments to learn more. Branded intro/outro with company logo. Captions in English and Spanish.",
    "duration": "4 min",
    "style": "onboarding",
    "captions": true,
    "languages": ["en", "es"],
    "quiz": false,
    "lms_export": "scorm-1.2",
    "format": "16:9"
  }'
```

### Step 4 — Review, Test, and Deploy
Preview the module. Test the interactive elements. Verify quiz scoring logic if applicable. Export the SCORM package and upload to LMS. Monitor completion rates in the LMS dashboard.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the training topic, audience, and module structure |
| `duration` | string | | Target length: "3 min", "5 min", "15 min" |
| `style` | string | | "onboarding", "compliance", "software-training", "soft-skills", "sales-enablement", "process-doc" |
| `captions` | boolean | | Generate burned-in or sidecar captions (default: true) |
| `languages` | array | | Caption/voiceover languages: ["en"], ["en", "es", "fr"] |
| `quiz` | boolean | | Insert knowledge-check questions (default: false) |
| `lms_export` | string | | LMS package format: "scorm-1.2", "scorm-2004", "xapi", "none" |
| `format` | string | | "16:9", "9:16", "1:1" |

## Output Example

```json
{
  "job_id": "tvc-20260328-001",
  "status": "completed",
  "module_title": "Onboarding Module 2 — Org Structure and Your Team",
  "duration_seconds": 246,
  "format": "mp4",
  "resolution": "1920x1080",
  "file_size_mb": 72.8,
  "output_files": {
    "video": "onboarding-m2-org-structure.mp4",
    "scorm_package": "onboarding-m2-org-structure-scorm12.zip",
    "captions_en": "onboarding-m2-org-structure.en.vtt",
    "captions_es": "onboarding-m2-org-structure.es.vtt"
  },
  "interactive_elements": [
    {"type": "clickable_org_chart", "timestamp": "3:28", "departments": 5}
  ],
  "completion_tracking": {
    "standard": "SCORM 1.2",
    "completion_threshold": "video_end",
    "score_tracking": false
  }
}
```

## Tips

1. **Keep compliance modules under 15 minutes** — Regulatory requirements don't specify video length. Shorter modules with quizzes have higher completion rates AND better knowledge retention than 45-minute marathons.
2. **Use scenario role-plays for soft skills** — "Good example vs bad example" side by side teaches through contrast. The bad example should be realistic, not cartoonishly terrible — employees recognize the nuance.
3. **Screen recordings need click annotations** — A cursor moving across a screen is hard to follow. NemoVideo's automatic click-highlight (yellow circle on each click) makes software workflows trackable.
4. **Translate captions, don't dub immediately** — Captions in 5 languages cost a fraction of 5 dubbed versions. Start with captions; invest in dubbing only for languages where literacy rates require it.
5. **SCORM-package everything** — Even if your LMS technically accepts raw MP4, SCORM packaging enables completion tracking, quiz scoring, and per-module analytics. The 30 seconds of packaging time saves hours of manual tracking.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p | LMS upload / internal portal / meeting presentation |
| MP4 9:16 | 1080p | Mobile-first training for field employees |
| SCORM 1.2/2004 | — | LMS with completion and quiz tracking |
| xAPI | — | Modern LMS with experience tracking |
| SRT/VTT | — | Multilingual caption files |

## Related Skills

- [online-course-video-maker](/skills/online-course-video-maker) — Full online course production
- [lecture-video-editor](/skills/lecture-video-editor) — Lecture and teaching video editing
- [tutorial-video-maker](/skills/tutorial-video-maker) — Tutorial and how-to video creation
