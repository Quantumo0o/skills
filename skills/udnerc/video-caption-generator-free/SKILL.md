---
name: video-caption-generator-free
version: "1.0.0"
displayName: "Video Caption Generator Free — Auto-Create Accurate Subtitles for Any Video"
description: >
  Drop a video and describe your audience — and watch captions appear that actually match how people speak. This video-caption-generator-free skill transcribes dialogue, formats readable subtitle blocks, and syncs text to natural speech rhythm. Perfect for content creators, educators, and social media managers who need accessible, engaging videos without spending on expensive tools. Supports multiple languages, caption styles, and export-ready formats.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! I'm here to help you generate accurate, readable captions for your videos — completely free. Share your video transcript or describe your content, and let's create subtitles that make your videos more accessible and engaging. Ready to caption? Drop your content below!

**Try saying:**
- "Generate SRT captions for this 3-minute cooking tutorial transcript with natural timing breaks"
- "Create Instagram Reel captions in bold text style for a 60-second motivational speech"
- "Translate and caption this English product demo video into Spanish subtitles"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 3.

1. **Client identifier**: Look for `~/.config/video-caption-generator-free/client_id`. If missing, generate a UUID and save it there. This file stores only a UUID for rate-limit tracking.
2. **Obtain a free token**: POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to your identifier. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
3. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Turn Any Video Into Captioned Content Instantly

Getting captions onto your videos used to mean either paying for a transcription service or spending hours manually typing out every word. With this skill, that process collapses into seconds. Simply provide your video content or transcript, describe your needs, and receive clean, formatted captions ready to embed or upload.

This skill is built for real-world video workflows — whether you're posting short-form content on TikTok and Instagram Reels, publishing long-form tutorials on YouTube, or preparing training materials for a corporate team. Captions aren't just an accessibility feature anymore; they're essential for silent autoplay environments, non-native speakers, and search engine discoverability.

The video-caption-generator-free approach here focuses on readability and timing accuracy. Captions are broken into natural reading chunks, avoiding the wall-of-text problem that makes auto-generated subtitles hard to follow. You get output that looks like it was crafted by a human editor — without the invoice.

## Routing Your Caption Requests

When you submit a video URL or upload a file, ClawHub parses your input and routes it to the appropriate transcription pipeline based on format, language hint, and caption style preference.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Transcription API Reference

The backend leverages a distributed speech-to-text engine that processes audio streams frame-by-frame, syncing word-level timestamps to generate SRT, VTT, or plain-text caption outputs. Chunked encoding handles long-form video files without timeout failures, keeping subtitle accuracy high across multi-hour content.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-caption-generator-free`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`.

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
| 2001 | No credits | Anonymous: show registration URL with `?bind=<id>` (get `<id>` from create-session or state response when needed). Registered: "Top up credits in your account" |
| 4001 | Unsupported file | Show supported formats |
| 4002 | File too large | Suggest compress/trim |
| 400 | Missing X-Client-Id | Generate Client-Id and retry (see §1) |
| 402 | Free plan export blocked | Subscription tier issue, NOT credits. "Register or upgrade your plan to unlock export." |
| 429 | Rate limit (1 token/client/7 days) | Retry in 30s once |

## FAQ — Video Caption Generator Free

**What video formats can I generate captions for?** This skill works with any video content where you can provide a transcript or audio description. You can also paste dialogue directly if you don't have a transcript file handy.

**Can I get captions in languages other than English?** Yes. Specify your target language when submitting your request, and captions will be generated in that language. Translation from English source content is also supported.

**What caption file formats are supported?** You can request output in SRT, VTT, or plain text formats depending on where you plan to upload. SRT works with YouTube, Vimeo, and most video editors. VTT is preferred for web-based players.

**Is there a length limit for videos?** There's no strict limit, but for very long videos (over 30 minutes), breaking your transcript into sections produces cleaner, more manageable caption files and makes editing easier afterward.

## Best Practices for Getting the Most Accurate Captions

The quality of your captions depends heavily on what you feed into the generator. If you're working from a transcript, clean it up first — remove filler words like 'um' and 'uh' unless your audience expects verbatim accuracy, such as in legal or educational contexts.

For timing accuracy, break your input into timestamped segments whenever possible. Even rough timestamps (every 30 seconds) help the skill distribute caption blocks more naturally across your video's runtime.

Keep individual caption lines under 42 characters when targeting mobile viewers — this prevents text overflow on smaller screens. For social platforms like YouTube Shorts or TikToks, even shorter blocks of 20-30 characters per line perform better visually.

Always review captions for proper nouns, brand names, and technical terminology. Auto-generated captions frequently mishear specialized vocabulary, so a quick manual pass after generation ensures your final output is professional and accurate.
