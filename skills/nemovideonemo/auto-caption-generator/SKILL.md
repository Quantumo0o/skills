---
name: subtitle-generator
version: "1.0.0"
displayName: "Subtitle Generator - Auto Add Subtitles to Video with AI, Burn-In Captions"
description: >
  Subtitle generator that auto-transcribes any video and produces ready-to-use caption
  files. Drop a video or paste a URL — get back SRT, VTT, or hardcoded subtitles burned
  directly into the footage. Handles speech recognition in 50+ languages, subtitle
  translation between language pairs, and styled burn-in with custom fonts, colors, and
  positioning. Built for content creators who need captions for YouTube, TikTok, or
  Instagram without learning subtitle editing software. Supports mp4, mov, avi, webm, mkv.
metadata:
  openclaw:
    emoji: 💬
---

# Subtitle Generator — From Video to Captions in One Step

Drop a video, get subtitles. No timecoding, no manual sync, no subtitle editor needed.

## Description

Use this skill when the user wants to **generate subtitles from video**, **auto-caption any clip**, **transcribe spoken audio**, **translate captions to another language**, **burn hardcoded text onto footage**, or **export SRT/VTT files**. Powered by NemoVideo AI.

This skill covers the full subtitle pipeline: speech-to-text transcription with word-level timing, multi-language translation, styled burn-in rendering, and file export — all through a single chat interface.

**Trigger phrases:** subtitle generator, generate subtitles, auto subtitles, auto captions, caption generator, transcribe video, video to text, burn subtitles, hardcode captions, export SRT, SRT file, VTT export, bilingual subtitles, translate subtitles, add captions to video, closed captions, open captions, speech to text, video transcript

**Primary use cases:**
- Transcribe video/audio speech into timed subtitles (Whisper-powered, any language)
- Export subtitle files as SRT, VTT, or plain text transcript
- Translate generated or uploaded subtitles into any of 50+ target languages
- Burn styled captions directly into video (font, size, color, outline, position)
- Create bilingual dual-language subtitle overlays (e.g. English + Chinese)
- Batch process multiple clips with consistent caption styling
- Generate accessibility-compliant captions for social platforms

**Not for:** general video editing, video generation from text, or screen recording.

---

## Setup

**Base URL:** `https://mega-api-prod.nemovideo.ai`

All requests require:
```
Authorization: Bearer <NEMOVIDEO_API_KEY>
Content-Type: application/json
```

Set `NEMOVIDEO_API_KEY` in your environment or OpenClaw secrets.

---

## Workflow Overview

```
Upload video/audio → Start subtitle job → Poll status → Get SRT/VTT/transcript
                                                      → Burn subtitles into video
```

---

## API Reference

### 1. Upload Media

Upload a video or audio file before processing.

```http
POST /v1/upload
Content-Type: multipart/form-data

file=<binary>
```

**Response:**
```json
{
  "file_id": "f_abc123",
  "filename": "interview.mp4",
  "duration_seconds": 182,
  "size_bytes": 45000000
}
```

Use `file_id` in subsequent requests.

---

### 2. Generate Subtitles (Transcription)

Transcribe speech and produce time-coded subtitles.

```http
POST /v1/subtitles/generate
Content-Type: application/json

{
  "file_id": "f_abc123",
  "language": "en",
  "output_formats": ["srt", "vtt", "txt"],
  "options": {
    "punctuate": true,
    "max_chars_per_line": 42,
    "max_lines": 2
  }
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | string | ✅ | Uploaded file ID |
| `language` | string | ✅ | Source language code (`en`, `zh`, `ja`, `ko`, `es`, `fr`, `de`, `auto`) — use `auto` for auto-detect |
| `output_formats` | array | ✅ | One or more of: `srt`, `vtt`, `txt`, `json` |
| `options.punctuate` | bool | ❌ | Auto-add punctuation (default: true) |
| `options.max_chars_per_line` | int | ❌ | Max characters per subtitle line (default: 42) |
| `options.max_lines` | int | ❌ | Max lines per subtitle block (default: 2) |

**Response:**
```json
{
  "job_id": "job_gen_789",
  "status": "queued",
  "estimated_seconds": 45
}
```

---

### 3. Translate Subtitles

Translate existing subtitles into a target language.

```http
POST /v1/subtitles/translate
Content-Type: application/json

{
  "source": {
    "type": "job_id",
    "value": "job_gen_789"
  },
  "target_language": "zh",
  "preserve_timing": true,
  "output_formats": ["srt"]
}
```

**Or translate from an uploaded SRT file:**
```json
{
  "source": {
    "type": "file_id",
    "value": "f_srt_456"
  },
  "target_language": "zh",
  "preserve_timing": true,
  "output_formats": ["srt", "vtt"]
}
```

**Supported language codes:** `en`, `zh`, `zh-tw`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ar`, `ru`, `hi`, `vi`, `th`, `id`

---

### 4. Burn Subtitles Into Video

Hardcode captions permanently into the video frame.

```http
POST /v1/subtitles/burn
Content-Type: application/json

{
  "file_id": "f_abc123",
  "subtitle_source": {
    "type": "job_id",
    "value": "job_gen_789"
  },
  "style": {
    "font": "Arial",
    "font_size": 28,
    "color": "#FFFFFF",
    "outline_color": "#000000",
    "outline_width": 2,
    "position": "bottom",
    "margin_bottom": 40
  },
  "output_format": "mp4"
}
```

**Style parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `font` | `"Arial"` | Font family |
| `font_size` | `28` | Font size in pixels |
| `color` | `"#FFFFFF"` | Text color (hex) |
| `outline_color` | `"#000000"` | Outline/shadow color |
| `outline_width` | `2` | Outline thickness |
| `position` | `"bottom"` | `"top"` or `"bottom"` |
| `margin_bottom` | `40` | Pixels from edge |
| `background_box` | `false` | Semi-transparent background |
| `background_opacity` | `0.5` | Box opacity (0.0–1.0) |

---

### 5. Bilingual Subtitles

Burn two subtitle tracks simultaneously.

```http
POST /v1/subtitles/burn-bilingual
Content-Type: application/json

{
  "file_id": "f_abc123",
  "primary": {
    "subtitle_source": { "type": "job_id", "value": "job_gen_789" },
    "style": { "font_size": 26, "color": "#FFFF00", "position": "bottom", "margin_bottom": 70 }
  },
  "secondary": {
    "subtitle_source": { "type": "job_id", "value": "job_translate_321" },
    "style": { "font_size": 22, "color": "#FFFFFF", "position": "bottom", "margin_bottom": 30 }
  },
  "output_format": "mp4"
}
```

---

### 6. Poll Job Status

All jobs are async. Poll until `completed` or `failed`.

```http
GET /v1/jobs/{job_id}
```

**Polling strategy:** every 3-5s for short files, 10-15s for longer ones. Timeout after 10 minutes.

---

### 7. Download Output

Download from the URL in job outputs. CDN URLs are pre-signed, valid 24 hours.

---

## Common Workflows

### A: Generate + Export SRT
Upload → generate (language: auto, formats: ["srt"]) → poll → download SRT

### B: Translate Existing Subtitles
Upload SRT → translate (target: "es") → poll → download translated SRT

### C: Full Pipeline (Video → Hardcoded Chinese Subtitles)
Upload video → generate (en) → translate (zh) → burn (zh) → poll → return MP4

### D: Bilingual Video (EN + ZH)
Upload → generate (en) → translate (zh) → burn-bilingual → poll → return MP4

---

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Bad request | Check params |
| 401 | Invalid API key | Prompt user to verify key |
| 413 | File too large | Compress or use shorter clip |
| 422 | Unsupported format/language | List supported options |
| 429 | Rate limited | Wait 10s, retry with backoff |
| 500/503 | Server error | Retry after 30s |

---

## Behavior Notes

- Use `language: "auto"` when source language is unknown (+5s detection time)
- `zh` = Simplified Chinese, `zh-tw` = Traditional Chinese
- SRT is more universal; VTT for web players. When unsure, offer both
- Burning re-encodes the video — takes longer than SRT export alone
- File limits: 2GB upload, 4h max duration
- Output URLs expire after 24 hours

---

## Example Prompts → Actions

| User says | Action |
|-----------|--------|
| "Add subtitles to my video" | Upload → generate → burn → MP4 |
| "Generate SRT for this" | Upload → generate (srt) → download |
| "Translate subtitles to Spanish" | Upload SRT → translate (es) → download |
| "Chinese subtitles on English video" | Upload → generate (en) → translate (zh) → burn → MP4 |
| "Bilingual EN + ZH captions" | Upload → generate (en) → translate (zh) → burn-bilingual → MP4 |
| "Get transcript from podcast" | Upload → generate (txt) → download |
| "Burn white text black outline" | Upload + SRT → burn (style) → MP4 |
