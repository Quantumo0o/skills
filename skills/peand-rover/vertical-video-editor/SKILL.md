---
name: vertical-video-editor
version: 1.0.2
displayName: "Vertical Video Editor — Reframe, Crop & Optimize Clips for Mobile and Reels"
description: >
  Drop a video and describe what you need — this vertical-video-editor skill transforms horizontal or square footage into polished 9:16 content ready for TikTok, Instagram Reels, and YouTube Shorts. It handles smart cropping, subject reframing, caption placement, aspect ratio conversion, and pacing adjustments so your content feels native to mobile screens. Works with mp4, mov, avi, webm, and mkv files. Built for creators, social media managers, and brands who shoot wide but publish tall.
metadata: {"openclaw": {"emoji": "📱", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! Ready to make your footage look perfect on mobile Drop your video file and tell me how you'd like it reframed — whether it's cropping for Reels, adjusting for Shorts, or repositioning a subject for a 9:16 layout, let's get your vertical video edit started.

**Try saying:**
- "Crop this landscape interview video to 9:16 and keep the speaker centered throughout"
- "Convert this 16:9 product demo to vertical format and add space at the top for a text overlay"
- "Reframe this travel clip for Instagram Reels — the horizon should stay level and cut out the dead space on the sides"

### First-Time Connection

When a user first opens this skill, connect to the NemoVideo backend automatically. Briefly let them know (e.g. "Connecting to NemoVideo...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 3.

1. **Client identifier**: Look for `~/.config/nemovideo/client_id`. If missing, generate a UUID and save it there. This file stores only a UUID for rate-limit tracking.
2. **Obtain a free token**: POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to your identifier. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
3. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Turn Any Footage Into Scroll-Stopping Vertical Content

Most video is shot wide — but audiences scroll tall. This skill exists to close that gap without making you relearn an editing suite or wrestle with export presets. Whether you're repurposing a landscape interview, a product demo, or a travel clip, the vertical-video-editor intelligently identifies the focal point of each scene and repositions the frame so nothing important gets cut off.

You stay in control of the creative decisions. Want the subject anchored to the left third Need safe zones respected for caption overlays Prefer a cinematic crop that follows motion Just describe it. The skill interprets your instructions and applies them consistently across the full clip — not just a single keyframe.

The result is a video that looks like it was composed for vertical from the start, not squeezed or letterboxed into an awkward format. For content teams publishing across multiple platforms, this means one source file can feed every channel without a separate manual edit for each.

## Routing Your Reframe Requests

Every crop, reframe, and aspect-ratio conversion request is parsed for intent — whether you're punching in on a subject, converting 16:9 landscape footage to 9:16 vertical, or trimming dead space from the frame — and routed to the matching NemoVideo processing endpoint automatically.

| User says... | Action | Skip SSE |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Under the Hood

The NemoVideo backend handles all the heavy lifting: smart reframing with subject-tracking, lossless crop calculations, and mobile-optimized rendering for Reels, Shorts, and TikTok specs. Each API call passes your clip metadata, target resolution, and reframe parameters directly to the processing pipeline, so output stays frame-accurate every time.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `vertical-video-editor`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?task=<task_id>&session=<session_id>&skill_name=vertical-video-editor&skill_version=1.0.0&skill_source=<platform>`

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

## Integration Guide

The vertical-video-editor skill fits naturally into content production pipelines where footage is captured on traditional cameras or screen recorders and then distributed to mobile-first platforms. You can feed it raw exports directly from your editing software — no special pre-processing required before upload.

If you're working across a team, the skill accepts the same source file multiple times with different framing instructions, making it straightforward to produce platform-specific variants (TikTok, Reels, Shorts) from a single master clip without duplicating manual work.

Output files are returned in a format ready for direct upload to social platforms or for import back into your editing timeline as a treated asset. This makes it practical as a mid-pipeline step rather than only a final export tool — you can reframe first, then layer in graphics or music in your preferred software afterward.

## Performance Notes

Processing time scales with file size and the complexity of the reframing instructions. A 60-second mp4 under 200MB with a static subject typically completes quickly, while longer clips with fast motion or multi-subject scenes require more analysis to maintain accurate focal tracking throughout.

For best results, upload the highest quality source file you have — the skill works from the original resolution and outputs at the target aspect ratio without unnecessary compression artifacts. If your clip contains rapid cuts between scenes, specifying per-scene framing preferences in your prompt will produce more precise results than a single global instruction.

Supported formats include mp4, mov, avi, webm, and mkv. Very large files (over 1GB) may benefit from being trimmed to the relevant segment before upload to reduce turnaround time.

## Common Workflows

The most frequent use case is repurposing existing horizontal content — taking a YouTube video, webinar recording, or brand film and extracting a vertical cut for social distribution. Users typically prompt with the subject to track, the desired safe zones for captions, and whether they want hard cuts to match the original edit or a smoother, trimmed-down version.

A second common workflow is live-event or interview footage where a single wide shot needs to become multiple vertical clips, each focused on a different speaker or moment. Describing the timestamps and subjects in your prompt lets the skill handle each segment with the right framing independently.

Creators also use this skill to fix aspect ratio mismatches when footage was accidentally recorded in the wrong orientation or exported with black bars — a quick reframe pass removes the bars and produces a clean, properly composed vertical file without re-shooting.
