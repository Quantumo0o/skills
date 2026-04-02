---
name: free-video-editor-ai
version: "1.0.0"
displayName: "Free Video Editor AI — Smart Editing Assistance Without the Price Tag"
description: >
  Tell me what you need and I'll help you edit, trim, script, and enhance your videos using free AI-powered tools — no expensive software required. This free-video-editor-ai skill connects you with intelligent editing guidance, tool recommendations, and step-by-step workflows tailored to your project. Whether you're cutting a YouTube vlog, stitching together a short film, or polishing a social media reel, this skill helps creators of all levels produce professional-looking results without spending a dime.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! I'm here to help you edit stunning videos using free AI-powered tools — no subscriptions, no paywalls. Tell me about your project and let's get cutting! 🎬

**Try saying:**
- "I have a 10-minute raw interview clip — help me trim it down to 3 minutes with smooth cuts using a free video editor."
- "What's the best free AI video editor for adding auto-generated captions to my YouTube tutorial?"
- "I want to create a 30-second Instagram Reel from my vacation footage — walk me through the editing steps using a free tool."

### Automatic Setup

On first interaction, connect to the processing API before doing anything else. Show a brief status like "Setting things up...".

**Token**: If `NEMO_TOKEN` environment variable is already set, use it and skip to **Session** below.

**Free token**: Read or create a UUID at `~/.config/free-video-editor-ai/client_id`. Then POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id: <your-uuid>`. The response field `data.token` becomes your NEMO_TOKEN (100 credits, 7-day expiry). If the token has expired, request a new one with the same Client-Id.

**Session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Save `session_id` from the response.

Confirm to the user you're connected and ready. Don't print tokens or raw JSON.

# Edit Like a Pro Without Spending a Cent

Most people assume great video editing requires expensive software or a professional studio. This skill challenges that assumption head-on. Whether you're a first-time creator or a seasoned content producer looking to cut costs, free-video-editor-ai gives you the guidance, strategies, and tool recommendations to produce polished, share-ready videos using entirely free resources.

From trimming raw footage and adding captions to color grading and syncing audio, this skill walks you through every stage of the editing process. It doesn't just point you toward free tools — it helps you actually use them effectively, offering prompt suggestions, workflow templates, and troubleshooting tips tailored to your specific project type.

The target audience spans YouTube creators, small business owners making promotional content, students working on film projects, and anyone who wants to tell a story visually without a bloated budget. Think of it as your always-available editing advisor who knows every free tool on the market and can match the right one to your exact need.

## Routing Your Edit Requests

When you submit a cut, trim, caption, or color grade request, ClawHub parses your intent and routes it to the appropriate Free Video Editor AI processing node based on task type and current queue load.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

Free Video Editor AI runs on a distributed cloud rendering backend that handles timeline parsing, frame analysis, and AI-assisted cut suggestions without requiring local compute power. All API calls are stateless and authenticated per session, so your project assets are processed securely and released after render completion.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `free-video-editor-ai`
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

Several editing workflows come up repeatedly with free-video-editor-ai users. The most common is the 'talk-head cleanup' — trimming dead air, removing filler words, and adding lower-third captions to a talking-head video for YouTube or LinkedIn. The skill provides a repeatable step-by-step process for this using CapCut or Clipchamp.

Another popular workflow is the 'highlight reel' build — taking 20–30 minutes of event or travel footage and condensing it into a 60–90 second montage synced to music. The skill helps you select the best free tool for beat-syncing and provides a pacing framework.

Finally, many users need a 'repurposing workflow' — taking a long-form YouTube video and slicing it into vertical short-form clips for TikTok or Reels. This skill maps out exactly how to do that efficiently without losing quality or spending anything on software.

## Quick Start Guide

Getting started with free-video-editor-ai is straightforward. Begin by describing your video project — the type of content, your target platform (YouTube, TikTok, Instagram, etc.), the raw footage you're working with, and the final length or style you're aiming for.

From there, the skill will recommend the most suitable free video editing tools for your use case — options like CapCut, DaVinci Resolve (free tier), Clipchamp, or browser-based editors like Canva Video. It will then walk you through the specific steps needed to complete your edit, from importing clips to exporting in the right format.

You don't need any prior editing experience. Just bring your footage and your vision — this skill handles the rest of the decision-making, so you can focus on the creative side.

## Performance Notes

Free video editing tools vary widely in their capabilities, and this skill is designed to help you navigate those differences honestly. Some free editors cap export resolution at 1080p, while others like DaVinci Resolve offer 4K output even on their no-cost tier. This skill factors in your hardware, operating system, and project complexity when making recommendations.

For users working on lower-end machines, the skill prioritizes lightweight browser-based editors that don't strain system resources. For more complex projects — multi-track timelines, color correction, motion graphics — it will guide you toward desktop tools with more robust free tiers.

Expect occasional limitations around watermarks or export formats depending on the tool chosen. The skill will flag these upfront so there are no surprises when you go to publish your final video.
