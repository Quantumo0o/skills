---
name: online-course-video-maker
version: 1.2.1
displayName: "Online Course Video Maker — Create and Edit eLearning Videos with AI"
description: >
  Online Course Video Maker — Create and Edit eLearning Videos with AI.
metadata: {"openclaw": {"emoji": "🎓", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# Online Course Video Maker — Create and Edit eLearning Videos

You spent 200 hours building the curriculum. You know the material cold. Then you hit record and discover the real problem: the camera doesn't care how much you know — it cares whether you can hold attention for 12 minutes while explaining database normalization to someone who would rather be on TikTok. The gap between expertise and watchable video is where most online course creators stall, producing content that is technically accurate but pedagogically flat — talking-head footage with no visual variation, slides read aloud verbatim, and 45-minute lectures that could have been 12 minutes if someone had edited out the ums, the tangents, and the three minutes spent fumbling with screen share. NemoVideo closes that gap by handling the production pipeline so the instructor can focus on teaching: it structures raw recordings into lesson modules with chapter markers, generates animated overlays from slide content, syncs screen recordings with face-cam footage, adds knowledge-check interstitials at retention-critical intervals, and exports in the exact specifications required by Udemy, Coursera, Teachable, Kajabi, and Thinkific — because each platform has different resolution, bitrate, and file-size requirements that no instructor should have to memorize.

## Use Cases

1. **Udemy Course Production** — Record 8 hours of raw screen-share-plus-webcam footage for a Python programming course. NemoVideo segments it into 42 lessons averaging 11 minutes each, adds chapter markers at concept boundaries, inserts animated code-output overlays when the terminal is too small to read, generates intro/outro bumpers with course branding, and exports each lesson as a separate MP4 meeting Udemy's 1080p H.264 spec with AAC audio.
2. **Cohort-Based Course Launch** — Produce a 6-module leadership course for a live cohort. Each module: a 15-minute pre-recorded lesson, a 2-minute recap animation, and a discussion-prompt card. NemoVideo generates the recap from the lesson transcript automatically and renders the discussion card with the question, timer, and course branding.
3. **Micro-Course for Social Media** — Convert a 45-minute masterclass into five 3-minute vertical videos for Instagram/TikTok. NemoVideo identifies the five highest-engagement segments, crops to 9:16, adds captions (89% of mobile learners watch without sound), and inserts a "Full course link in bio" CTA at the end of each clip.
4. **Corporate LMS Upload** — Reformat an existing course for a company's SCORM-compliant LMS. NemoVideo adjusts resolution to 720p (bandwidth-constrained corporate networks), embeds chapter metadata for LMS navigation, and generates a completion-tracking thumbnail for each module.
5. **Multilingual Course Variant** — Take a completed English course and produce a Spanish version. NemoVideo generates translated captions, syncs AI voiceover in Spanish, and adjusts on-screen text overlays — without re-recording a single frame of footage.

## How It Works

### Step 1 — Upload Raw Materials
Provide your screen recordings, webcam footage, slide decks (PDF/PPTX), and any supplementary assets (diagrams, code files, brand kit). NemoVideo accepts up to 10 hours of raw footage per project.

### Step 2 — Define Course Structure
Specify the module and lesson breakdown, or let NemoVideo auto-segment based on topic changes detected in the audio transcript. Set target lesson length (recommended: 8-15 minutes for retention).

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "online-course-video-maker",
    "prompt": "Produce Module 3 of a Python course: 4 lessons covering functions, arguments, return values, and scope. Source: 55-minute raw recording with screen share and webcam. Auto-segment into 4 lessons at topic boundaries. Add chapter markers within each lesson. Generate animated overlay when terminal text is below 14pt. Insert knowledge-check card after each lesson (multiple choice, 3 options). Branded intro bumper with course logo. Export as separate MP4s, Udemy spec 1080p H.264 AAC.",
    "duration": "4 lessons",
    "style": "screen-share-course",
    "platform": "udemy",
    "captions": true,
    "knowledge_checks": true,
    "format": "16:9"
  }'
```

### Step 4 — Review and Publish
Preview each lesson in the NemoVideo editor. Adjust cut points, overlay timing, or knowledge-check questions. Export final files and upload directly to your course platform.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the course topic, module structure, and production requirements |
| `duration` | string | | Target per-lesson length or total: "12 min/lesson", "4 lessons", "2 hours total" |
| `style` | string | | "screen-share-course", "talking-head", "slide-narration", "hybrid-webcam-slides", "micro-course" |
| `platform` | string | | Target platform specs: "udemy", "coursera", "teachable", "kajabi", "thinkific", "lms-scorm" |
| `format` | string | | "16:9", "9:16", "1:1" |
| `captions` | boolean | | Burn in or sidecar captions (default: true) |
| `knowledge_checks` | boolean | | Insert quiz/check interstitials between lessons (default: false) |

## Output Example

```json
{
  "job_id": "ocvm-20260328-001",
  "status": "completed",
  "course_title": "Python Fundamentals — Module 3: Functions",
  "lessons": [
    {
      "lesson": 1,
      "title": "Defining Functions",
      "duration_seconds": 682,
      "file": "module3-lesson1-defining-functions.mp4",
      "file_size_mb": 124.3,
      "chapters": ["Syntax basics 0:00", "Calling functions 3:12", "Docstrings 7:45"],
      "knowledge_check": {"question": "What keyword defines a function in Python?", "options": ["func", "def", "function"], "answer": "def"}
    },
    {
      "lesson": 2,
      "title": "Arguments and Parameters",
      "duration_seconds": 714,
      "file": "module3-lesson2-arguments-parameters.mp4",
      "file_size_mb": 131.8,
      "chapters": ["Positional args 0:00", "Keyword args 4:28", "Default values 8:02"],
      "knowledge_check": {"question": "Which allows calling f(name='Alice')?", "options": ["Positional argument", "Keyword argument", "Return value"], "answer": "Keyword argument"}
    },
    {
      "lesson": 3,
      "title": "Return Values",
      "duration_seconds": 648,
      "file": "module3-lesson3-return-values.mp4",
      "file_size_mb": 118.6
    },
    {
      "lesson": 4,
      "title": "Scope and Namespaces",
      "duration_seconds": 695,
      "file": "module3-lesson4-scope-namespaces.mp4",
      "file_size_mb": 127.1
    }
  ],
  "total_duration_minutes": 45.6,
  "platform_compliance": "udemy-1080p-h264-aac ✓"
}
```

## Tips

1. **Keep lessons under 15 minutes** — Completion rates drop 40% past the 15-minute mark on every major platform. NemoVideo auto-segments at natural topic boundaries to hit this target.
2. **Add captions always** — 89% of mobile learners watch without sound at least some of the time. Burned-in captions aren't optional; they're accessibility and engagement infrastructure.
3. **Use knowledge checks at module boundaries** — A 3-question multiple-choice card between lessons activates recall and increases retention by 25-35% vs. passive viewing.
4. **Record at the highest quality your setup allows** — NemoVideo can downscale 4K to 1080p cleanly, but it cannot upscale 720p to 1080p without quality loss. Start high.
5. **Batch-produce, don't perfectionist-loop** — Record all modules in one session, then edit. Re-recording one lesson 7 times produces worse content than recording it once and letting NemoVideo handle the polish.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | Udemy / Coursera / Teachable / website |
| MP4 9:16 | 1080p | TikTok / Reels micro-course clip |
| MP4 1:1 | 1080p | LinkedIn Learning / social promo |
| SRT/VTT | — | Sidecar caption file for platform upload |

## Related Skills

- [lecture-video-editor](/skills/lecture-video-editor) — Lecture and teaching video editing
- [training-video-creator](/skills/training-video-creator) — Corporate training video production
- [tutorial-video-maker](/skills/tutorial-video-maker) — Tutorial and how-to video creation
