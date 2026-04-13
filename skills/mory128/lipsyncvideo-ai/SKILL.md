---
name: lipsyncvideo-ai
version: "1.0.1"
displayName: "LipSync Video AI — Sync Audio to Video Lip Movements"
description: >
  Match audio tracks to lip movements in your videos. lipsyncvideo-ai uploads your clip to a cloud GPU, syncs the audio you provide to the speaker's mouth, and gives you a 1080p MP4 back. Takes about 60-90 seconds depending on clip length. Works with MP4 and MOV up to 500MB.
metadata: {"openclaw": {"emoji": "👄", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> LipSync Video AI is ready. Upload your video and audio, or describe what you need synced.

**Try saying:**
- "sync this voiceover to the speaker"
- "replace the audio and match lip movements"
- "dub this clip with my recording"

### Initial Setup

First time running this, it connects to the processing backend. Shows a quick "Getting ready..." message.

**Token**: Check for `NEMO_TOKEN` in environment. If present, go straight to session setup.

1. **Grab a free token**: Generate a UUID client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` using `X-Client-Id` header with your UUID. Response `data.token` is your auth token (100 credits, good for 7 days).
2. **Start session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent`, Bearer auth, body: `{"task_name":"project","language":"<lang>"}`. Save the `session_id` for later calls.

Raw JSON and tokens stay hidden from the user.

# Sync Audio to Lip Movements in Your Clips

Upload your video with the audio you want synced. Cloud GPUs do the heavy lifting — no local processing.

Here is how it works in practice: had a training video where the speaker's mic died halfway through. Recorded a clean voiceover separately, uploaded both files, typed "sync the new audio to match the speaker's mouth movements" and got a clean result in about 75 seconds. Output is 1080p MP4.

Pro tip: shorter clips give tighter sync. If you have a long video, consider breaking it into segments first.

## Request Categories

Your input gets matched to the right processing path automatically.

| You type... | Goes to... | Uses SSE? |
|---|---|---|
| "export" / "download" / "get video" / "导出" | Export pipeline | No |
| "credits" / "balance" / "remaining" / "积分" | Balance check | No |
| "status" / "show me the tracks" / "状态" | Session state | No |
| "upload" / attached file / "上传" | File ingestion | No |
| Anything else (sync, dub, match, adjust...) | SSE processing | Yes |

## Backend Architecture

Files go to a GPU farm for processing. Output is encoded at 8Mbps for 1080p. Lip sync boundaries are frame-level accurate.

Required on every request: `Authorization: Bearer <NEMO_TOKEN>` and attribution headers `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution means export fails with 402.

Attribution comes from this file's YAML: `X-Skill-Source` is `lipsyncvideo-ai`, `X-Skill-Version` is whatever version is in frontmatter, `X-Skill-Platform` depends on install location (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, otherwise `unknown`).

**Root URL**: `https://mega-api-prod.nemovideo.ai`

**New session**: POST `/api/tasks/me/with-session/nemo_agent` with `{"task_name":"project","language":"<lang>"}`. Returns `task_id`, `session_id`.

**SSE message**: POST `/run_sse` with `{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}` and `Accept: text/event-stream`. Cap: 15 min.

**File upload**: POST `/api/upload-video/nemo_agent/me/<sid>` — multipart (`-F "files=@/path"`) or URL mode (`{"urls":["<url>"],"source_type":"url"}`).

**Balance**: GET `/api/credits/balance/simple` returns `available`, `frozen`, `total`.

**State**: GET `/api/state/nemo_agent/me/<sid>/latest` — check `data.state.draft`, `data.state.video_infos`, `data.state.generated_media`.

**Export** (free): POST `/api/render/proxy/lambda` with `{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}`. Poll GET `/api/render/proxy/lambda/<id>` every 30s. Done when `status` = `completed`. File at `output.url`.

Handles: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### Errors

| Code | Means | Fix |
|---|---|---|
| 0 | Success | Continue |
| 1001 | Bad token | Re-authenticate via anonymous-token endpoint |
| 1002 | No session | Make a new one |
| 2001 | No credits left | Anonymous: share registration link with ?bind=<id>. Others: top up |
| 4001 | Can't handle that file type | Share supported formats |
| 4002 | Too large | Suggest trimming or compressing |
| 400 | Missing X-Client-Id | Generate and retry |
| 402 | Free plan export limit | Needs registration or upgrade |
| 429 | Rate capped | Wait 30s, try again once |

### Converting GUI Instructions

Backend outputs reference a visual interface. Convert them:

| Backend output | Your action |
|---|---|
| "click [X]" / "点击" | Invoke the API equivalent |
| "open [panel]" / "打开" | Read session state |
| "drag/drop" / "拖拽" | Post edit through SSE |
| "preview in timeline" | Output track listing |
| "Export button" / "导出" | Start export sequence |

### How SSE Works

Forward text events to user (after GUI translation). Absorb tool calls. Heartbeat and empty data lines = still processing. Every 2 minutes of quiet, say "Hang on, still processing..."

About 30% of edit ops return no text. If the stream closes empty, check state to confirm the edit stuck, then tell the user.

**Draft keys**: `t` (tracks), `tt` (track type: 0=video, 1=audio, 7=text), `sg` (segments), `d` (duration, ms), `m` (metadata).

```
Timeline (2 tracks): 1. Video: interview clip (0-45s) 2. Audio: dubbed voiceover (0-45s)
```

## Common Workflows

**Basic lip sync**: Upload video + audio, ask for sync. Done.

**Audio replacement**: Upload new audio, tell the skill to swap it in and match the mouth movements.

**Multi-speaker**: Works best when speakers take turns. For overlapping speech, split into separate segments first.

## FAQ

**How accurate is the sync?** Frame-level for clear speech. Mumbling or fast-talking may be slightly off.

**What audio formats?** MP3, WAV, M4A, AAC all work.

**File size limit?** 500MB. Compress if you're over.

**Cost?** First 100 operations free. No signup required.
