---
name: ai-mental-health-video
version: "1.0.0"
displayName: "AI Mental Health Video Maker — Create Wellness and Therapy Education Videos"
description: >
  Create AI-powered mental health education videos, coping-skill demonstrations, and therapy awareness content. NemoVideo produces anxiety and depression explainers with clinical accuracy, guided breathing exercises with animated visual cues, therapist introduction videos, workplace wellness campaigns, and crisis-aware content that follows WHO and APA media guidelines — because mental health communication requires sensitivity that generic video tools don't provide.
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Mental Health Video Maker — Wellness and Therapy Education Videos

One in five adults experiences a mental health condition in any given year, yet most of them will search YouTube before they search for a therapist — typing "am I having a panic attack" at 2 AM, watching a 3-minute video, and making a decision about whether to seek help based on whether that video made them feel understood or ashamed. This is the stakes of mental health video content: it is often the first point of contact between a person in distress and the mental health system, a responsibility that most content creators don't recognize and most video tools don't support. NemoVideo's AI mental health video maker is built around the principle that mental health content must move the viewer from suffering to action — not dwell in the pain, not minimize it, but acknowledge it and provide a concrete next step. It integrates clinical media guidelines (WHO suicide-prevention reporting standards, APA language recommendations, SAMHSA content frameworks) directly into the production pipeline, flagging harmful phrases before they're published, auto-inserting crisis resources when content discusses suicide or self-harm, and structuring every video to end with a specific, actionable step the viewer can take in the next 24 hours.

## Use Cases

1. **Condition Explainer — Understanding Panic Attacks (2 min)** — Animated video for a therapy practice website. NemoVideo structures: the physical experience (animated body — racing heart, chest tightness, tingling hands, feeling of unreality — 25 sec), what's actually happening (amygdala hijack, fight-or-flight misfire — simplified neuroscience with brain animation, 20 sec), what a panic attack is NOT (not a heart attack, not "going crazy," not dangerous even though it feels terrifying — 15 sec), what to do during one (grounding technique: 5-4-3-2-1 senses, demonstrated with animated examples — 25 sec), when to seek help (happening more than once a month, avoiding situations because of fear, affecting work or relationships — 20 sec), CTA with practice info plus 988 Lifeline displayed (15 sec). Language: 6th-grade reading level. Palette: calming blues and warm creams.
2. **Guided Coping Exercise — Box Breathing (90 sec)** — A therapist on camera guides the viewer through box breathing. NemoVideo adds: an animated expanding/contracting circle synced precisely to the 4-4-4-4 count, phase labels (Inhale... Hold... Exhale... Hold...), a round counter ("Round 2 of 4"), and ambient soundscape (ocean waves at -22dB). The viewer follows along in real time. Exported 9:16 for Instagram and TikTok where anxiety-relief content gets the highest save rates on the platform.
3. **Therapist Profile — Building Trust Before the First Session (60 sec)** — A therapist introduces themselves from their actual office (the couch, the plants, the warm lighting). NemoVideo structures: name and credential title card (5 sec), who they help ("adults navigating anxiety, grief, and life transitions" — 10 sec), their approach in plain language ("We'll figure out what's keeping you stuck and build practical strategies to move forward" — 15 sec), what a first session looks like ("Just a conversation — no couch, no Freud, no judgment" — 15 sec), and CTA with booking link (10 sec). The goal: reduce the fear of making the first appointment.
4. **Workplace Mental Health Campaign (60 sec)** — Internal video for a company's Employee Assistance Program launch. NemoVideo produces: statistic hook ("1 in 5 of us experiences a mental health challenge each year — including people in this room," 8 sec), normalization ("Asking for help is strength, not weakness," 8 sec), what the EAP provides (free confidential counseling, 24/7 crisis line, 6 sessions per issue — animated checklist, 20 sec), how to access it (phone number, app, website URL — 15 sec), closing reassurance (9 sec). Tone: warm, matter-of-fact, non-clinical. Distributed via internal Slack, email, and office screens.
5. **Youth Mental Health — Signs for Parents (2 min)** — A children's hospital video helping parents recognize when a teen is struggling. NemoVideo structures: behavioral changes to watch for (withdrawal from friends, sleep disruption, grade drops, irritability, loss of interest — each illustrated, not performed by a real teen, 30 sec), what to say ("I've noticed you've been different lately. I'm not judging — I want to understand" — 15 sec), what NOT to say ("Just cheer up" / "Other kids have it worse" / "What do you have to be depressed about?" — 15 sec with red X overlays), when professional help is needed (specific frequency and duration criteria, 15 sec), local resources and national crisis numbers (15 sec), closing: "Starting the conversation is the hardest part — and you just learned how" (10 sec).

## How It Works

### Step 1 — Define Content and Compliance Needs
Specify the mental health topic, target audience (patients, general public, employees, parents, teens), and whether the content requires crisis-resource display. Any content mentioning suicide, self-harm, or acute crisis automatically triggers the 988 Lifeline inclusion.

### Step 2 — Provide Source Material or Script
Upload therapist recordings, animation scripts, or breathing-exercise footage. NemoVideo can produce fully animated explainers from a script alone — no filming required.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-mental-health-video",
    "prompt": "Create a 2-minute panic attack explainer. Animated, no real people. Sections: (1) Physical experience — body outline with racing heart pulse, chest band tightening, tingling hands with sparkle effect, tunnel-vision overlay, 25 sec. (2) Neuroscience — amygdala as oversensitive alarm, fight-or-flight activation for non-dangerous trigger (elevator, crowd), 20 sec. (3) What it is NOT — animated checkmarks dismissing heart attack, insanity, death, 15 sec. (4) Grounding technique 5-4-3-2-1 — animated examples: 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste, demonstrated with illustrated room scene, 25 sec. (5) When to seek help — frequency/avoidance/life-impact checklist, 20 sec. (6) CTA — practice info plus 988 Suicide and Crisis Lifeline, 15 sec. Palette: soft blue, cream, gentle green. Music: ambient calm at -20dB. Reading level: 6th grade.",
    "duration": "2 min",
    "style": "condition-explainer",
    "animation": true,
    "crisis_resources": true,
    "language_check": true,
    "reading_level": "6th-grade",
    "music": "ambient-calm",
    "format": "16:9"
  }'
```

### Step 4 — Clinical Review and Publish
Route through a licensed clinician for medical accuracy review. NemoVideo's language_check has already flagged any harmful phrasing, but human clinical sign-off is required before publication. Deploy to practice website, YouTube, social media, and patient-portal education library.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the mental health topic, audience, and video structure |
| `duration` | string | | Target length: "60 sec", "90 sec", "2 min", "3 min" |
| `style` | string | | "condition-explainer", "coping-exercise", "therapist-profile", "workplace-campaign", "youth-parent" |
| `animation` | boolean | | Use animated illustrations instead of live footage (default: false) |
| `crisis_resources` | boolean | | Display 988 Lifeline / crisis numbers when content warrants (default: auto-detect) |
| `language_check` | boolean | | Flag harmful language per WHO/APA guidelines (default: true) |
| `reading_level` | string | | "6th-grade", "8th-grade", "clinical" |
| `music` | string | | "ambient-calm", "hopeful-gentle", "breathing-sync", "silence" |
| `format` | string | | "16:9", "9:16", "1:1" |

## Output Example

```json
{
  "job_id": "amhv-20260328-001",
  "status": "completed",
  "title": "Understanding Panic Attacks — What's Happening and What to Do",
  "duration_seconds": 122,
  "format": "mp4",
  "resolution": "1920x1080",
  "file_size_mb": 30.2,
  "output_url": "https://mega-api-prod.nemovideo.ai/output/amhv-20260328-001.mp4",
  "sections": [
    {"label": "Physical Experience", "start": 0, "end": 25},
    {"label": "Neuroscience — Amygdala Alarm", "start": 25, "end": 45},
    {"label": "What It Is NOT", "start": 45, "end": 60},
    {"label": "Grounding — 5-4-3-2-1 Technique", "start": 60, "end": 85},
    {"label": "When to Seek Help", "start": 85, "end": 105},
    {"label": "CTA + Crisis Resources", "start": 105, "end": 122}
  ],
  "compliance": {
    "language_check": "passed — 0 harmful phrases detected",
    "crisis_resources": "988 Suicide & Crisis Lifeline displayed 5 sec",
    "reading_level": "Flesch-Kincaid 5.4 (6th grade)"
  }
}
```

## Tips

1. **Always end with action, never with suffering** — Every mental health video must move the viewer toward a next step: a phone number, a breathing technique, a conversation to have. Ending on the pain without a path forward is clinically irresponsible.
2. **"Died by suicide," never "committed suicide"** — "Committed" implies criminality. NemoVideo's language_check flags this and 40+ other harmful phrasings per WHO and APA media guidelines.
3. **Animated illustrations for condition explainers** — Real people depicting panic or depression can feel exploitative or triggering. Illustrated figures allow viewers to project their own experience without voyeurism.
4. **988 Lifeline on any content discussing crisis** — This is not optional. It's a media guideline requirement and potentially life-saving. NemoVideo auto-detects crisis-adjacent content and inserts the resource.
5. **The therapist's office IS the trust signal** — The couch, the plants, the warm light communicate safety. A studio or green screen removes the environmental cue that says "this is a place where people heal."

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | Practice website / YouTube / patient portal |
| MP4 9:16 | 1080p | Instagram Reels / TikTok coping exercise |
| MP4 1:1 | 1080p | Facebook / LinkedIn awareness campaign |
| MP3 | — | Guided breathing audio-only distribution |

## Related Skills

- [ai-cooking-video](/skills/ai-cooking-video) — AI recipe and food content
- [ai-wedding-video](/skills/ai-wedding-video) — AI wedding film production
- [ai-legal-video](/skills/ai-legal-video) — AI legal explainer videos
