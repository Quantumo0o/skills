---
name: seedance-lip-sync-generator
version: "1.0.0"
displayName: "Seedance Lip Sync Generator — Sync Mouth Movements to Audio"
description: >
  Need to matching mouth movements to a dubbed or replaced audio track? This seedance-lip-sync-generator skill handles AI lip sync generation on a remote backend — just upload your video and audio and describe what you want. You'll get 1080p MP4 output in about 30-60 seconds. Built for content creators, dubbing editors, social media marketers who need realistic lip sync without manual frame-by-frame animation.
metadata: {"openclaw": {"emoji": "🎙️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "greeting_v2"}}
---

## Getting Started

> Share your video and audio and I'll get started on AI lip sync generation. Or just tell me what you're thinking.

**Try saying:**
- "generate a 30-second talking-head video clip with a new voiceover audio file into a 1080p MP4"
- "sync the character's mouth movements to the new audio track I uploaded"
- "matching mouth movements to a dubbed or replaced audio track for content creators, dubbing editors, social media marketers"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# How Seedance Lip Sync Generator Works Here

So here's how this works. You give me video and audio and I AI lip sync generation it through NemoVideo's backend. No local software, no plugins, no GPU on your end.

Tested it with a a 30-second talking-head video clip with a new voiceover audio file last week. Asked for sync the character's mouth movements to the new audio track I uploaded and had a MP4 back in 30-60 seconds. 1080p quality, decent file size.

shorter clips under 60 seconds produce the most accurate lip sync results. That's about it.

## Matching Input to Actions

Each message you send gets routed to the right handler based on what you're asking for.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Technical Details

Processing runs on remote GPUs through NemoVideo's API. The skill sends your input, waits for the render, and hands back the result — all server-side.

Every API call needs `Authorization: Bearer <NEMO_TOKEN>` plus the three attribution headers above. If any header is missing, exports return 402.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `seedance-lip-sync-generator`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`.

**Send message (SSE)**: POST `/run_sse` — body `{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}` with `Accept: text/event-stream`. Max timeout: 15 minutes.

**Upload**: POST `/api/upload-video/nemo_agent/me/<sid>` — file: multipart `-F "files=@/path"`, or URL: `{"urls":["<url>"],"source_type":"url"}`

**Credits**: GET `/api/credits/balance/simple` — returns `available`, `frozen`, `total`

**Session state**: GET `/api/state/nemo_agent/me/<sid>/latest` — key fields: `data.state.draft`, `data.state.video_infos`, `data.state.generated_media`

**Export** (free, no credits): POST `/api/render/proxy/lambda` — body `{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}`. Poll GET `/api/render/proxy/lambda/<id>` every 30s until `status` = `completed`. Download URL at `output.url`.

Supported formats: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### Error Codes

- `0` — success, continue normally
- `1001` — token expired or invalid; re-acquire via `/api/auth/anonymous-token`
- `1002` — session not found; create a new one
- `2001` — out of credits; anonymous users get a registration link with `?bind=<id>`, registered users top up
- `4001` — unsupported file type; show accepted formats
- `4002` — file too large; suggest compressing or trimming
- `400` — missing `X-Client-Id`; generate one and retry
- `402` — free plan export blocked; not a credit issue, subscription tier
- `429` — rate limited; wait 30s and retry once

### Translating GUI Instructions

The backend responds as if there's a visual interface. Map its instructions to API calls:

- "click" or "点击" → execute the action via the relevant endpoint
- "open" or "打开" → query session state to get the data
- "drag/drop" or "拖拽" → send the edit command through SSE
- "preview in timeline" → show a text summary of current tracks
- "Export" or "导出" → run the export workflow

### SSE Event Handling

| Event | Action |
|-------|--------|
| Text response | Apply GUI translation (§4), present to user |
| Tool call/result | Process internally, don't forward |
| `heartbeat` / empty `data:` | Keep waiting. Every 2 min: "⏳ Still working..." |
| Stream closes | Process final response |

~30% of editing operations return no text in the SSE stream. When this happens: poll session state to verify the edit was applied, then summarize changes to the user.

Draft JSON uses short keys: `t` for tracks, `tt` for track type (0=video, 1=audio, 7=text), `sg` for segments, `d` for duration in ms, `m` for metadata.

Example timeline summary:
```
Timeline (3 tracks): 1. Video: city timelapse (0-10s) 2. BGM: Lo-fi (0-10s, 35%) 3. Title: "Urban Dreams" (0-3s)
```

## Quick Start Guide

First time? Just upload a video and audio and describe what you need. I'll run it through NemoVideo's backend and hand you back a 1080p MP4.

Processing takes about 30-60 seconds depending on video length. You start with 100 free credits — most edits cost 1-3.

## Tips and Tricks

Keep your source files under 500MB for fastest processing. If you're working with longer content, split it into chunks first.

For best results at 1080p, make sure your input is at least 720p. Upscaling from 480p works but you'll notice it.

Export as MP4 with H.264 codec for the best compatibility across platforms.

## Best Practices

Use source footage in MP4, MOV, WAV, MP3 format for best compatibility. 1080p input gives the cleanest results but 720p works fine too.

Be specific with your requests — "add upbeat background music at 30% volume" beats "add some music". The AI works better with concrete details.

Export as MP4 with H.264 codec for the best compatibility across platforms.
