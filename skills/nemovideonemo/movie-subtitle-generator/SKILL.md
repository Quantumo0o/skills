---
name: movie-subtitle-generator
version: "1.0.0"
displayName: "Movie Subtitle Generator — Auto-Create Accurate Subtitles for Any Film or Video"
description: >
  Tell me what you need and I'll generate precise, well-timed subtitles for your movie or video in minutes. This movie-subtitle-generator skill transcribes spoken dialogue, syncs text to audio timing, and exports ready-to-use subtitle files. Upload your video in mp4, mov, avi, webm, or mkv format and get clean, readable subtitles styled for any audience. Perfect for filmmakers, content creators, educators, and accessibility advocates who need reliable captions without manual effort.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! I'm here to help you generate accurate, well-timed subtitles for your movie or video — just share your file and tell me what you need, and let's get your subtitles created right away.

**Try saying:**
- "Generate subtitles for my short film uploaded in mp4 format and sync them to the dialogue timing"
- "Create English subtitles for this interview video and format them for YouTube upload"
- "Transcribe the spoken audio from my documentary and export the subtitles as an SRT file"

### First-Time Connection

When a user first opens this skill, connect to the NemoVideo backend automatically. Briefly let them know (e.g. "Connecting to NemoVideo...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 3.

1. **Client identifier**: Look for `~/.config/nemovideo/client_id`. If missing, generate a UUID and save it there. This file stores only a UUID for rate-limit tracking.
2. **Obtain a free token**: POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to your identifier. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
3. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Turn Any Movie Into a Fully Subtitled Experience

Getting subtitles right is one of the most time-consuming parts of post-production — and one of the most important. Whether you're a filmmaker preparing a festival submission, a YouTube creator trying to reach a global audience, or an educator making video content more accessible, subtitles make the difference between content that connects and content that gets skipped.

This skill listens to your video's audio track and generates accurately timed subtitles that follow the natural rhythm of speech. It doesn't just dump text on screen — it breaks dialogue into readable chunks, respects pauses, and keeps lines short enough to read comfortably without missing the action.

You can use it for short films, full-length movies, documentary footage, interviews, online courses, or any video where spoken words need to appear on screen. The result is a clean subtitle track you can embed directly or export as a standalone file, ready to drop into your editing timeline or video platform.

## Subtitle Request Routing Logic

Every subtitle request — whether you're generating SRT files, syncing dialogue timecodes, or translating captions into a target language — is parsed and routed to the appropriate NemoVideo processing pipeline based on media type, language pair, and output format.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference

The NemoVideo backend handles frame-accurate speech detection, forced alignment, and multi-language subtitle rendering, returning subtitle tracks in SRT, VTT, or ASS formats with precise in/out timecodes. All transcription and translation calls are authenticated via bearer token and processed asynchronously for longer video files.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `movie-subtitle-generator`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=&task=<task_id>&session=<session_id>&skill_name=movie-subtitle-generator&skill_version=1.0.0&skill_source=<platform>`

**Send message (SSE)**: POST `/run_sse` — body `{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}` with `Accept: text/event-stream`. Max timeout: 15 minutes.

**Upload**: POST `/api/upload-video/nemo_agent/me/<sid>` — file: multipart `-F "files=@/path"`, or URL: `{"urls":["<url>"],"source_type":"url"}`

**Credits**: GET `/api/credits/balance/simple` — returns `available`, `frozen`, `total`

**Session state**: GET `/api/state/nemo_agent/me/<sid>/latest` — key fields: `data.state.draft`, `data.state.video_infos`, `data.state.generated_media`

**Export** (free, no credits): POST `/api/render/proxy/lambda` — body `{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}`. Poll GET `/api/render/proxy/lambda/<id>` every 30s until `status` = `completed`. Download URL at `output.url`.

Supported formats: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### SSE Event Handling

| Event | Action |
|-------|--------|
| Text response | Apply GUI translation (§4), present to user |
| Tool call/result | Process internally, don't forward |
| `heartbeat` / empty `data:` | Keep waiting. Every 2 min: "⏳ Still working..." |
| Stream closes | Process final response |

~30% of editing operations return no text in the SSE stream. When this happens: poll session state to verify the edit was applied, then summarize changes to the user.

### Backend Response Translation

The backend assumes a GUI exists. Translate these into API actions:

| Backend says | You do |
|-------------|--------|
| "click [button]" / "点击" | Execute via API |
| "open [panel]" / "打开" | Query session state |
| "drag/drop" / "拖拽" | Send edit via SSE |
| "preview in timeline" | Show track summary |
| "Export button" / "导出" | Execute export workflow |

**Draft field mapping**: `t`=tracks, `tt`=track type (0=video, 1=audio, 7=text), `sg`=segments, `d`=duration(ms), `m`=metadata.

```
Timeline (3 tracks): 1. Video: city timelapse (0-10s) 2. BGM: Lo-fi (0-10s, 35%) 3. Title: "Urban Dreams" (0-3s)
```

### Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue |
| 1001 | Bad/expired token | Re-auth via anonymous-token (tokens expire after 7 days) |
| 1002 | Session not found | New session §3.0 |
| 2001 | No credits | Anonymous: show registration URL with `?bind=<id>` (get `<id>` from create-session or state response when needed). Registered: "Top up at nemovideo.ai" |
| 4001 | Unsupported file | Show supported formats |
| 4002 | File too large | Suggest compress/trim |
| 400 | Missing X-Client-Id | Generate Client-Id and retry (see §1) |
| 402 | Free plan export blocked | Subscription tier issue, NOT credits. "Register at nemovideo.ai to unlock export." |
| 429 | Rate limit (1 token/client/7 days) | Retry in 30s once |

## Quick Start Guide

Getting started with the movie-subtitle-generator is straightforward. First, upload your video file — supported formats include mp4, mov, avi, webm, and mkv. Then describe what you need: the language of the dialogue, your preferred subtitle style (standard, SDH for hearing impaired, or clean captions), and your output format preference such as SRT, VTT, or embedded text.

Once processing is complete, review the generated subtitles for any proper nouns, technical terms, or stylized dialogue that may need a quick manual tweak. Most transcriptions are highly accurate, but names, slang, and accented speech occasionally benefit from a light review pass.

Finally, download your subtitle file and import it into your video editor, streaming platform, or media player. If you're uploading to YouTube or Vimeo, the SRT format works universally. For DCP or broadcast delivery, request the appropriate format in your prompt and the skill will tailor the output accordingly.

## Tips and Tricks

For the most accurate subtitle output, make sure your video has clear audio with minimal background noise. If your film has overlapping dialogue or heavy ambient sound, consider providing a clean audio mix alongside the video file — this significantly improves transcription accuracy.

If your movie includes multiple speakers, you can request speaker-labeled subtitles so viewers can tell who is talking, which is especially useful for interview-style documentaries or multi-character scenes.

When working with foreign-language films, specify the source language upfront so the skill can transcribe correctly rather than defaulting to English detection. You can also request translated subtitles in a second language in the same session — just ask for both in one prompt.

For long-form content like feature films, breaking the video into scenes or chapters before uploading can give you more granular control over subtitle timing and formatting per section.

## Best Practices

Always aim for subtitle lines that are no longer than 42 characters per line and no more than two lines on screen at once. When prompting the skill, you can specify these formatting preferences explicitly to get broadcast-ready results from the start.

For narrative films, avoid placing subtitle cuts in the middle of a sentence whenever possible. Ask the skill to align subtitle breaks with natural speech pauses or punctuation — this keeps the reading experience smooth and doesn't pull viewers out of the story.

If your movie contains song lyrics, sound effects, or off-screen narration that need to be captioned differently from standard dialogue, mention this in your prompt. The skill can handle SDH-style formatting that distinguishes spoken words from audio descriptions, which is essential for accessibility compliance.

Finally, always do a final sync check by playing back your video with the generated subtitles before publishing. Even highly accurate auto-generated subtitles benefit from a human review pass, especially around scene transitions where timing can occasionally drift by a fraction of a second.
