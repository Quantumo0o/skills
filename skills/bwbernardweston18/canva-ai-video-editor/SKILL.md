---
name: canva-ai-video-editor
version: "1.0.1"
displayName: "Canva AI Video Editor — Edit Videos with Text Commands"
description: >
  Edit videos by typing what you want changed. canva-ai-video-editor runs on a cloud backend so there's nothing to install — upload your MP4, describe the edit (cut, trim, add text, swap music), and download the result. Handles files up to 500MB and exports at 1080p.
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "greeting_v2"}}
---

## Getting Started

> Ready to edit. Send me your video or describe what you need.

**Try saying:**
- "cut the first 15 seconds"
- "add background music to my clip"
- "put a title card at the beginning"

### Setup (Runs Once)

The skill connects to the processing API on first use. A brief "Connecting..." message appears.

**Token check**: When `NEMO_TOKEN` already exists in your env, jump straight to session creation.

1. **Free token**: Create a UUID. POST it as `X-Client-Id` header to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token`. Pull `data.token` from the response — gives you 100 credits for a week.
2. **Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` using Bearer token, body `{"task_name":"project","language":"<lang>"}`. Keep the `session_id`.

Don't print tokens or raw API output to the user.

# Edit Your Videos with Simple Text Commands

Send your video and tell me what to change. All rendering happens on remote GPUs. You don't need any software installed.

Example: uploaded a 5-minute product demo, typed "remove the first 45 seconds, add a fade in, put company name as title overlay" and had the finished MP4 in about 80 seconds. Exports at 1080p by default.

Short clips process faster and the trim boundaries are more precise on them.

## Message Routing

Messages get sorted into categories based on what you asked for.

| Input pattern | Handler | SSE needed? |
|---|---|---|
| "export" / "download" / "save" / "导出" | Export flow | No |
| "credits" / "balance" / "how many left" / "积分" | Balance lookup | No |
| "status" / "progress" / "what's done" / "状态" | State check | No |
| "upload" / file attachment / "上传" | File upload | No |
| Everything else | SSE editing pipeline | Yes |

## Processing Infrastructure

Videos get sent to a GPU cluster for rendering. Re-encoding uses 8Mbps for 1080p exports. Edits are applied at exact frame boundaries.

All requests require `Authorization: Bearer <NEMO_TOKEN>` and three attribution headers: `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Leaving out attribution headers causes a 402 on export.

The attribution values are pulled from this file's YAML frontmatter: skill source is `canva-ai-video-editor`, version is from the `version` field, platform is figured out from where the skill is installed (`~/.clawhub/` means `clawhub`, `~/.cursor/skills/` means `cursor`, anything else is `unknown`).

**API root**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — send `{"task_name":"project","language":"<lang>"}` — you'll get `task_id` and `session_id` back.

**Send edit (SSE)**: POST `/run_sse` — body: `{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}` with `Accept: text/event-stream`. 15-minute timeout.

**Upload**: POST `/api/upload-video/nemo_agent/me/<sid>` — multipart form: `-F "files=@/path"`, or by URL: `{"urls":["<url>"],"source_type":"url"}`.

**Credits**: GET `/api/credits/balance/simple` — response has `available`, `frozen`, `total`.

**Session state**: GET `/api/state/nemo_agent/me/<sid>/latest` — relevant fields: `data.state.draft`, `data.state.video_infos`, `data.state.generated_media`.

**Export** (free): POST `/api/render/proxy/lambda` — body `{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}`. Poll GET `/api/render/proxy/lambda/<id>` at 30s intervals until `status` is `completed`. Get the file at `output.url`.

Supported files: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### Error Reference

| Code | Situation | Response |
|---|---|---|
| 0 | OK | Proceed normally |
| 1001 | Token invalid or expired | Fetch a new anonymous token |
| 1002 | Session missing | Create a fresh session |
| 2001 | Credits depleted | Anonymous: registration link (?bind=<id>). Registered: suggest top-up |
| 4001 | File type not supported | Show the accepted formats list |
| 4002 | Over the size limit | Recommend compressing or splitting |
| 400 | X-Client-Id missing | Create one and repeat the request |
| 402 | Free tier can't export | Registration or plan upgrade needed |
| 429 | Rate limited | Pause 30s then retry once |

### GUI-to-API Translation

The backend expects a visual editor. When it says UI things, translate them to API calls:

| It says... | You should... |
|---|---|
| "click [X]" / "点击" | Call the relevant endpoint |
| "open [panel]" / "打开" | Pull session state |
| "drag/drop" / "拖拽" | Submit an edit via SSE |
| "preview in timeline" | Show a text timeline summary |
| "Export button" / "导出" | Trigger the export workflow |

### SSE Stream Notes

Pass text events to the user (translate GUI references first). Keep tool calls internal. Heartbeat and empty `data:` events mean it's still processing — print "Working on it..." after 2 minutes of silence.

Roughly 30% of editing operations produce no text response. When the stream ends with no text, hit the state endpoint to confirm the change took effect, then describe what happened.

**Draft JSON keys**: `t` means tracks, `tt` is track type (video=0, audio=1, text=7), `sg` is segments, `d` is duration in milliseconds, `m` is metadata.

Example output:
```
Timeline (2 tracks): 1. Video: product demo (0-30s) 2. Text: "Our Product" (0-4s)
```

## Best Practices

Tell me exactly what you want and where. "Cut from 0:30 to 1:15" works better than "make it shorter." Include timestamps when you can.

You can chain multiple edits in one message. "Trim the intro, add fade transitions between scenes, and overlay my logo at the bottom right" all gets handled in a single pass.

500MB file cap. MP4 and MOV work best. Export is always MP4.

## How to Start

1. Drop your video file in the chat
2. Say what to change: "cut the first 30 seconds and add a title"
3. Wait 30-90 seconds for processing
4. Grab the exported MP4

First 100 credits are free, no signup. Accepts MP4, MOV, AVI, WebM files.
