---
name: pixbim-lip-sync-ai
version: "1.0.0"
displayName: "Pixbim Lip Sync AI — Automatically Sync Lips to Any Audio Track"
description: >
  Turn any video into a perfectly lip-synced production using pixbim-lip-sync-ai — the tool that matches mouth movements to dialogue, dubbing, or voiceover with frame-level precision. Whether you're localizing content for new markets, fixing out-of-sync audio, or animating a character's speech, this skill helps you generate accurate lip sync results without manual keyframing or rotoscoping. Built for content creators, filmmakers, and localization teams.
metadata: {"openclaw": {"emoji": "🎤", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome to Pixbim Lip Sync AI — your shortcut to perfectly synchronized lips and audio in any video. Share your video details or audio track and let's get your lip sync dialed in right now.

**Try saying:**
- "I have a Spanish dubbed audio track and an English video — can you help me sync the lip movements to the Spanish dialogue using Pixbim Lip Sync AI?"
- "My interview footage has audio that drifted out of sync halfway through the recording. How do I use Pixbim Lip Sync AI to fix the mouth movement alignment?"
- "I'm working on an animated character and I want to use Pixbim Lip Sync AI to match the mouth shapes to a recorded voiceover line — what's the best approach?"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Make Every Word Match Every Mouth Movement

Lip sync errors are one of the most distracting problems in video production — whether you're dubbing a film into a new language, adding a voiceover to an animated character, or correcting audio drift in a recorded interview. Pixbim Lip Sync AI solves this by analyzing both the audio track and the facial movements in your video, then intelligently aligning them so every syllable lands exactly when the lips move.

This skill gives you direct access to Pixbim's lip sync engine through a conversational interface. You can describe your project, specify your source video and target audio, and get back a synchronized output without needing to touch a timeline or manually adjust keyframes. It's designed for workflows where speed and accuracy both matter.

Content creators producing multilingual versions of their videos, game developers animating NPC dialogue, and post-production teams cleaning up dubbing artifacts will all find this tool cuts hours of manual work down to minutes. The result is natural-looking mouth movement that holds up under scrutiny — not the rubbery, approximate sync you get from generic tools.

## Routing Lip Sync Requests

When you submit a lip sync job, your request is parsed for the target video clip, audio track, and facial detection parameters, then dispatched to the appropriate Pixbim processing pipeline based on resolution tier and sync mode selected.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Pixbim API Backend Reference

Pixbim Lip Sync AI runs on a cloud-based neural rendering backend that performs per-frame phoneme mapping and mouth-shape blending using its trained deep learning model. All video assets are temporarily staged in secure cloud storage during the synthesis pass, then returned as a processed output file once the lip sync render is finalized.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `pixbim-lip-sync-ai`
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

## Integration Guide

Pixbim Lip Sync AI works by taking a source video containing a face or character and a separate audio track, then processing both to generate a synchronized output. To get the best results, your video should have a clearly visible face or mouth region with consistent lighting — heavy motion blur or extreme camera angles can reduce sync accuracy.

When submitting a project through this skill, provide the video resolution, frame rate, and whether the subject is a live-action person or a 2D/3D animated character. Pixbim handles both, but the processing pipeline differs. For dubbing workflows, supply the target language audio as a clean WAV or MP3 file, and specify whether you want the original background audio preserved beneath the new dialogue.

For batch localization — syncing the same video to multiple language tracks — describe all target audio files in a single request and the skill will structure the job accordingly. Output files are delivered in the same format and resolution as your source video unless you specify otherwise.

## Troubleshooting

If your lip sync output looks off, the most common cause is a mismatch between the audio sample rate and the video frame rate. Make sure your audio file is exported at 44.1kHz or 48kHz and your video is a standard frame rate (24, 25, or 30fps) before submitting. Non-standard frame rates can cause Pixbim Lip Sync AI to miscalculate the timing offsets.

For animated characters, if the mouth shapes appear generic or don't match the phonemes in the audio, check whether the character rig supports viseme-based animation. Pixbim Lip Sync AI outputs viseme data that requires a compatible rig — if your character only has basic open/close mouth states, the sync will appear simplified.

If the face is not being detected in the source video, ensure the subject's face occupies at least 15% of the frame and is not obscured by masks, heavy makeup, or extreme lighting. Submitting a short test clip first is a good way to confirm detection before processing a full-length video.
