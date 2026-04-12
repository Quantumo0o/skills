---
name: tiktok-video-editor
version: "1.0.6"
displayName: "TikTok Video Editor — Edit and Export TikTok Videos"
description: >
  Get 1080p MP4 files from your raw video clips using this tiktok-video-editor tool. It runs AI video editing on cloud GPUs, so your machine does zero heavy lifting. TikTok creators can editing short vertical videos for TikTok posting in roughly 30-60 seconds — supports MP4, MOV, AVI, WebM.
metadata: {"openclaw": {"emoji": "🎵", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "greeting_v2"}}
---

## Getting Started

> Share your raw video clips and I'll get started on AI video editing. Or just tell me what you're thinking.

**Try saying:**
- "edit a 60-second vertical phone recording into a 1080p MP4"
- "add trending text overlays, trim pauses, and sync cuts to the beat"
- "editing short vertical videos for TikTok posting for TikTok creators"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# From Raw Video Clips to Polished Tiktok Clips

So here's how this works. You give me raw video clips and I AI video editing it through NemoVideo's backend. No local software, no plugins, no GPU on your end.

Tested it with a a 60-second vertical phone recording last week. Asked for add trending text overlays, trim pauses, and sync cuts to the beat and had a MP4 back in 30-60 seconds. 1080p quality, decent file size.

vertical 9:16 video is natively supported so no cropping is needed. That's about it.

## Request Routing

Your request is matched to one of several actions depending on what you typed.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## How It Works Internally

Everything happens on cloud infrastructure. Your tiktok video editor job gets queued, rendered on GPU nodes, and the finished file comes back as a download link.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `tiktok-video-editor`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

Include `Authorization: Bearer <NEMO_TOKEN>` and all attribution headers on every request — omitting them triggers a 402 on export.

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

### Translating GUI Instructions

The backend responds as if there's a visual interface. Map its instructions to API calls:

- "click" or "点击" → execute the action via the relevant endpoint
- "open" or "打开" → query session state to get the data
- "drag/drop" or "拖拽" → send the edit command through SSE
- "preview in timeline" → show a text summary of current tracks
- "Export" or "导出" → run the export workflow

Draft JSON uses short keys: `t` for tracks, `tt` for track type (0=video, 1=audio, 7=text), `sg` for segments, `d` for duration in ms, `m` for metadata.

Example timeline summary:
```
Timeline (3 tracks): 1. Video: city timelapse (0-10s) 2. BGM: Lo-fi (0-10s, 35%) 3. Title: "Urban Dreams" (0-3s)
```

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

## FAQ

**What resolution can I get?** Up to 1080p. Input quality matters though — garbage in, garbage out.

**Can I use this on my phone footage?** Yes. Vertical (9:16), horizontal (16:9), square — all work. Just upload and specify what you want.

**Credits?** 100 free to start. Most operations cost 1-5 credits depending on video length.

## Common Workflows

**From scratch**: Describe what you want and the AI generates a draft. You refine from there.

**Polish existing content**: Upload your raw video clips, ask for specific changes — add trending text overlays, trim pauses, and sync cuts to the beat, adjust colors, swap music. The backend handles rendering.

**Export ready**: Once you're happy, export at 1080p in MP4. File lands in your downloads.

## Best Practices

Use source footage in MP4, MOV, AVI, WebM format for best compatibility. 1080p input gives the cleanest results but 720p works fine too.

Be specific with your requests — "add upbeat background music at 30% volume" beats "add some music". The AI works better with concrete details.

Export as MP4 with H.264 codec for best TikTok upload compatibility.
