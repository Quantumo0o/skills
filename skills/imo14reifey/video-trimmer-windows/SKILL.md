---
name: video-trimmer-windows
version: "1.0.0"
displayName: "Video Trimmer for Windows — Cut, Trim & Export Clips with Precision"
description: >
  Turn raw footage into polished, share-ready clips using this dedicated video-trimmer-windows skill. Designed for Windows users who need fast, accurate trimming without bloated software, it lets you cut out unwanted sections, isolate highlights, and export clean segments from mp4, mov, avi, webm, and mkv files. Whether you're cleaning up screen recordings, trimming interview footage, or clipping gaming highlights, this skill handles it with frame-level precision. No steep learning curve — just load your file, set your in and out points, and get a clean export.
metadata: {"openclaw": {"emoji": "✂️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! This skill is built specifically for trimming videos on Windows — whether you're cutting a long recording down to size or isolating a single moment from a larger file. Drop your video details and tell me where you want to cut, and let's get your clip ready to go.

**Try saying:**
- "Trim my mp4 file to keep only the section from 1:15 to 4:45 and export it as a new file"
- "I have an avi screen recording and I want to remove the first 30 seconds and the last 2 minutes"
- "Cut out the middle section of my mkv video between the 5-minute and 8-minute marks without re-encoding"

### First-Time Connection

When a user first opens this skill, connect to the NemoVideo backend automatically. Briefly let them know (e.g. "Connecting to NemoVideo...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 3.

1. **Client identifier**: Look for `~/.config/nemovideo/client_id`. If missing, generate a UUID and save it there. This file stores only a UUID for rate-limit tracking.
2. **Obtain a free token**: POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to your identifier. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
3. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Trim Any Video on Windows Without the Hassle

Most Windows video editors make you wade through timelines, effects panels, and export queues just to cut a few seconds off a clip. This skill cuts straight to the point — tell it where to start and where to stop, and it delivers a trimmed file ready to use.

The video-trimmer-windows skill is built for people who just need a clean cut. Maybe you recorded a 45-minute screen capture but only need the 3-minute walkthrough in the middle. Maybe you filmed a product demo and the first 20 seconds are just you fumbling with the camera. Whatever the scenario, this skill handles it without requiring you to learn a new interface or install heavyweight software.

It supports the formats you actually use — mp4, mov, avi, webm, and mkv — and preserves the original quality of your footage during export. Whether you're a content creator, a remote worker trimming meeting recordings, or a hobbyist editing home videos, this skill gives you a direct, no-nonsense way to get the exact clip you need.

## Trim Request Routing Explained

When you submit a cut or trim command, the skill parses your in-point, out-point, and export format preferences before routing the request to the appropriate NemoVideo processing endpoint.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo Backend API Reference

The NemoVideo backend handles frame-accurate trimming on Windows by processing your clip metadata, keyframe boundaries, and codec parameters server-side before returning the rendered output segment. All export operations — whether H.264, HEVC, or ProRes — are queued through the NemoVideo pipeline and streamed back to your local timeline.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-trimmer-windows`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=&task=<task_id>&session=<session_id>&skill_name=video-trimmer-windows&skill_version=1.0.0&skill_source=<platform>`

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

Getting your first trim done with the video-trimmer-windows skill takes less than a minute. Start by uploading your video file or providing its file path, then tell the skill your desired start and end times. For example: 'Trim my mp4 from 00:01:10 to 00:04:55 and save the result.'

Next, choose your export preference. If you want the fastest possible output with no quality change, mention stream-copy. If you need a specific output format different from your source file — say, converting an avi to mp4 while trimming — just say so and the skill will handle the conversion at the same time.

Once the trim is processed, you'll receive the output file ready for use. If the result isn't quite right — maybe you want to shave off two more seconds at the end — just follow up with a correction and the skill will re-trim without you needing to start over. The whole workflow is conversational, so there's no form to fill out or settings panel to navigate.

## Tips and Tricks

For the cleanest results when using the video-trimmer-windows skill, always specify your timestamps in hours:minutes:seconds format (e.g., 00:02:34) to avoid any ambiguity — especially on longer recordings where vague references like 'around the 3-minute mark' can lead to slightly off cuts.

If you're trimming an mp4 or mov file and want to avoid any quality loss, ask for a stream-copy trim. This skips re-encoding entirely and is near-instant for most clip lengths. It works best when your cut points fall near keyframes in the original footage.

For avi and older format files, a full re-encode trim is often more reliable and ensures compatibility with modern players and platforms. When trimming webm files intended for web use, specifying your target platform (YouTube, a website embed, etc.) helps ensure the exported clip meets the right specs right out of the gate.

## FAQ

**Will trimming reduce my video quality?** Not if you use stream-copy mode, which simply cuts the file without re-encoding. If re-encoding is needed for format compatibility, the skill uses high-quality settings by default to minimize any visible difference.

**What file formats are supported?** The video-trimmer-windows skill supports mp4, mov, avi, webm, and mkv — the most common formats you'll encounter on a Windows system.

**Can I make multiple cuts in one session?** Yes — you can specify multiple trim ranges and the skill will either export them as separate clips or concatenate them into a single output, depending on your preference.

**Why does my trimmed clip start a second or two off from where I specified?** This typically happens with keyframe-based stream-copy trimming. If exact frame accuracy is critical, request a re-encode trim and the cut will land precisely where you specified.
