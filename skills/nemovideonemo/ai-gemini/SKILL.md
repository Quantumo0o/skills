---
name: ai-gemini
version: "1.0.0"
displayName: "AI Gemini Video Analysis — Unlock Deep Insights from Any Video with Google Gemini"
description: >
  Tired of scrubbing through hours of footage just to extract key moments, summaries, or actionable insights? The ai-gemini skill brings Google Gemini's multimodal intelligence directly to your videos on ClawHub. Analyze scenes, generate detailed descriptions, ask natural language questions about video content, and surface meaningful takeaways — all without manual review. Ideal for content creators, researchers, marketers, and educators. Supports mp4, mov, avi, webm, and mkv formats.
metadata: {"openclaw": {"emoji": "✨", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! I'm your AI Gemini video analyst — ready to watch, understand, and extract insights from your footage so you don't have to. Drop in your video and tell me what you'd like to know — let's get started!

**Try saying:**
- "Summarize the key points discussed in this product demo video"
- "Identify and timestamp every scene change in this footage"
- "What emotions or reactions are visible in the people on screen throughout this clip?"

### Quick Start Setup

This skill connects to NemoVideo's cloud backend. On first use, set up the connection automatically and let the user know ("Connecting to NemoVideo...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Read `~/.config/nemovideo/client_id` or generate a UUID and save it there
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `/api/tasks/me/with-session/nemo_agent` at the same host with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Let Google Gemini See and Understand Your Videos

Most video tools can trim, cut, or apply effects — but they can't actually understand what's happening on screen. The ai-gemini skill changes that by running your video through Google Gemini's advanced multimodal reasoning engine, turning raw footage into structured, meaningful information you can actually use.

Whether you're a marketer trying to pull key messages from a product demo, a researcher cataloging interview footage, or a content creator looking for highlight moments, ai-gemini gives you a smart assistant that watches the video for you and reports back in plain language. Ask it to summarize the content, identify speakers, describe visual scenes, or flag specific moments — it handles all of it naturally.

This skill is built for people who work with video at scale or simply want to stop wasting time on manual review. Instead of watching a 45-minute recording to find one quote, let ai-gemini surface it in seconds. It's not just transcription — it's genuine video comprehension powered by one of the most capable AI models available today.

## Routing Your Gemini Video Requests

Every request you send is parsed for intent and automatically routed to the appropriate Gemini multimodal endpoint — whether you're asking for scene breakdowns, transcript extraction, object detection, or sentiment analysis across a video.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Under the Hood

The NemoVideo backend acts as the orchestration layer between ClawHub and Google Gemini's multimodal models, handling video ingestion, chunking, and prompt forwarding so Gemini can process frames and audio streams at scale. Authentication tokens, session context, and credit allocation are all managed server-side through NemoVideo's infrastructure.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-gemini`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=&task=<task_id>&session=<session_id>&skill_name=ai-gemini&skill_version=1.0.0&skill_source=<platform>`

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

## Common Workflows

One of the most popular uses of the ai-gemini skill is post-meeting analysis. Upload a recorded team call or client meeting and ask Gemini to extract action items, decisions made, and unresolved questions — saving hours of note-taking and follow-up.

Content repurposing is another high-value workflow. Feed a long-form video like a webinar or tutorial into ai-gemini and ask it to identify the top five quotable moments or generate a blog-ready outline based on what was covered. This turns a single video asset into multiple content pieces effortlessly.

For educators and trainers, ai-gemini excels at reviewing instructional video content. Ask it to flag sections where a concept was explained unclearly, or generate a comprehension quiz based on what was taught. It reads visual context too, so diagrams and on-screen text are factored into its responses — not just the audio track.

## FAQ

**What kinds of questions can I ask about my video?** You can ask nearly anything — from 'What is this video about?' to very specific queries like 'At what point does the presenter mention pricing?' or 'Describe the background setting in each scene.' Gemini understands both visual and audio content together.

**Does ai-gemini work on videos without spoken dialogue?** Yes. Since Gemini is multimodal, it analyzes visual content independently of audio. Silent videos, screen recordings, and footage with background music can all be processed and described meaningfully.

**How long can the video be?** Performance is best on videos up to 30 minutes, though longer files in supported formats (mp4, mov, avi, webm, mkv) can be processed. For very long recordings, consider splitting into segments for faster and more focused results.

**Can it detect specific people or objects?** Gemini can describe people, objects, and environments based on visual appearance and context, though it does not perform biometric identification by name unless the person is introduced verbally or via on-screen text.
