---
name: video-editing-app
version: "1.0.0"
displayName: "Video Editing App Assistant — Edit, Cut, and Polish Videos Like a Pro"
description: >
  Tell me what you need and I'll help you get the most out of your video-editing-app experience. Whether you're trimming raw footage, adding captions, syncing audio, or exporting for social media, this skill walks you through every step with clear, practical guidance. Built for creators, marketers, educators, and hobbyists who want polished results without a steep learning curve. Ask about specific features, troubleshoot problems, or get step-by-step editing workflows tailored to your project.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "greeting_v2"}}
---

## Getting Started

> Share your video editing question or describe your project and I'll give you a precise, step-by-step answer. No footage? Just tell me what you're trying to create.

**Try saying:**
- "I have a 10-minute raw interview clip and I need to cut it down to 2 minutes with smooth transitions — what's the best approach?"
- "How do I sync background music to match the beat of my video cuts in a typical video editing app timeline?"
- "My exported video looks pixelated on Instagram — what export settings should I use to keep quality high on mobile?"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Your Personal Guide to Faster, Smarter Video Editing

Editing video can feel overwhelming — timelines, codecs, color grading, audio mixing, export settings. This skill cuts through the noise and helps you focus on what actually matters for your specific project. Whether you're putting together a YouTube vlog, a product demo, a wedding highlight reel, or a short film, you'll get targeted advice that fits your workflow and your tools.

Instead of digging through forums or watching hour-long tutorials, just describe what you're trying to do and get a direct answer. Want to know how to remove background noise from a clip? How to create a smooth jump cut? How to add lower-third text overlays? This skill handles all of it with step-by-step clarity.

This isn't a generic video tips page. Every response is shaped around your actual video-editing-app scenario — the specific cut you're trying to make, the format you're exporting to, or the effect you're chasing. Think of it as having an experienced editor sitting next to you, ready to answer any question without judgment.

## Routing Cuts and Edit Requests

Every request you make — whether trimming a clip, applying a color grade, or exporting a timeline — gets parsed and routed to the matching editing function based on the action type and target asset.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Render Pipeline Reference

All heavy lifting like transcoding, multi-track rendering, and effects processing runs through a distributed cloud backend, so your local device never bottlenecks the export queue. Render jobs are queued, prioritized by resolution and codec complexity, and results are streamed back as soon as the output file is ready.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-editing-app`
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

## Common Workflows

A typical social media workflow in a video-editing-app starts with importing and organizing footage into labeled bins — A-roll, B-roll, music, graphics. From there, build a rough cut on the timeline using only your best A-roll takes, then layer B-roll on top to cover cuts and add visual variety.

For YouTube content, the standard workflow is: rough cut → audio mix → color correction → graphics and titles → export review → final export. Doing these in order prevents you from having to redo work when something upstream changes.

When editing for clients, always work from a project duplicate and keep original media untouched. Deliver a low-resolution proxy preview first for feedback, then apply notes to the full-resolution timeline before final export. This saves hours of back-and-forth revision time.

## Tips and Tricks

One of the most underused features in any video-editing-app is the keyboard shortcut set. Learning even five shortcuts — play/pause, split clip, zoom timeline, undo, and export — can cut your editing time in half. Ask this skill for a shortcut cheat sheet tailored to your specific app.

When color grading, always correct before you grade. Use your app's scopes (waveform, vectorscope) to fix exposure and white balance first, then apply your creative look. Skipping correction leads to grades that fall apart across different screens.

For audio, normalize your dialogue tracks to around -12 dB before adding music. This gives you headroom and keeps voices clear. Use a low-pass filter on background music so it doesn't compete with speech in the midrange frequencies.

## Use Cases

Content creators use this skill to streamline their video-editing-app process — from figuring out the right aspect ratio for Reels versus TikTok versus YouTube Shorts, to automating repetitive tasks like adding intros and outros to every episode.

Small business owners rely on it to produce product demos and testimonial videos without hiring an editor. Getting guidance on basic color correction, clean cuts, and professional-looking title cards makes a huge difference in perceived brand quality.

Educators and trainers use video editing apps to produce course content, and this skill helps them add chapter markers, screen recording overlays, and closed captions efficiently. Whether you're recording a lecture or a software walkthrough, the workflow advice here is practical and project-specific.

Event videographers — weddings, corporate events, live performances — use it to handle multi-camera syncing, music licensing considerations, and highlight reel pacing that keeps audiences engaged from first frame to last.
