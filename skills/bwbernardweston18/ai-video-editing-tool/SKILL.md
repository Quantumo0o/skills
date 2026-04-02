---
name: ai-video-editing-tool
version: "1.0.0"
displayName: "AI Video Editing Tool — Smart Cuts, Captions & Enhancements in Seconds"
description: >
  Tell me what you need and I'll help you shape raw footage into polished, publish-ready video content. This ai-video-editing-tool skill assists creators, marketers, and teams with editing decisions, script-to-timeline mapping, caption drafting, scene structuring, and cut suggestions — all through conversation. Whether you're trimming a talking-head clip, repurposing a long webinar into social snippets, or planning a cinematic sequence, describe your vision and get actionable editing guidance instantly.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome to your AI video editing assistant — built to help you cut, structure, and enhance your videos with confidence. Tell me about your footage or your editing goal and let's get to work!

**Try saying:**
- "Cut this webinar into social clips"
- "Write captions for my tutorial video"
- "Suggest pacing fixes for my edit"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Edit Smarter: Your AI Co-Editor Is Ready

Video editing has always demanded both technical skill and creative judgment — knowing when to cut, how to pace a sequence, which moments deserve emphasis, and how to structure a story arc that keeps viewers watching. This AI video editing tool bridges the gap between raw footage and finished product by giving you an intelligent collaborator who understands the craft.

Whether you're a solo content creator juggling a dozen uploads a week or a marketing team producing brand videos at scale, this skill helps you think through editing decisions faster. Describe your footage, your audience, your platform, and your goal — and get specific, actionable recommendations on cuts, pacing, transitions, caption placement, and more.

The skill is especially powerful for planning edits before you open your editing software. Use it to map out a rough cut structure, draft on-screen text, write chapter markers, or break a long-form video into short-form clips. Think of it as your pre-edit strategy session, available any time you need it.

## Smart Routing for Edit Requests

Every edit command — whether you're trimming dead air, burning in captions, or applying color grading — is parsed by the intent engine and dispatched to the matching processing pipeline based on task type, asset format, and output resolution.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

All render jobs are offloaded to a distributed cloud backend that handles frame extraction, ML-based cut detection, and caption synthesis in parallel — so even long-form footage processes without stalling your local machine. API calls follow a queue-and-callback model, meaning your client polls for job status until the enhanced video asset is ready for download.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-video-editing-tool`
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

## Tips and Tricks

**Give context about your platform first.** A cut that works for a 10-minute YouTube video rarely works for a 30-second Instagram Reel. Always mention where the final video will live — the AI will tailor pacing, caption density, and structure recommendations accordingly.

**Use the skill as a rough-cut planner.** Before you touch your editing timeline, describe your footage in plain language and ask for a proposed scene order. This saves hours of rearranging clips later and gives you a clear editorial spine to work from.

**Ask for multiple versions.** If you're repurposing content, ask the tool to suggest three different ways to cut the same source material — one for YouTube, one for TikTok, one for email. You'll often discover angles in your footage you hadn't considered.

**Paste in transcripts for precision.** If your editing software has generated a transcript, paste it directly and ask for timecode-based cut suggestions. The AI can identify the strongest soundbites, flag filler content, and recommend natural breakpoints with far more specificity.

## Common Workflows

**Long-form to short-form repurposing:** This is one of the most frequent use cases for the ai-video-editing-tool skill. Start by pasting a transcript or describing the key topics covered in your source video. Ask the tool to identify the top five quotable or standalone moments, then request a short-form structure for each — including suggested hook, middle, and CTA for platforms like TikTok, YouTube Shorts, or Instagram Reels.

**Interview and talking-head cleanup:** Describe the interview subject, the topic, and the approximate length, then ask the AI to help you plan a cut that removes filler, tightens responses, and sequences answers for narrative flow. This works especially well when you paste a rough transcript and ask for a 'best-of' selection.

**Tutorial and how-to structuring:** For step-by-step videos, share your script or outline and ask the tool to suggest chapter markers, on-screen text labels, and transition moments between steps. The result is a ready-to-execute editing blueprint you can take straight into Premiere, DaVinci, or CapCut.
