---
name: best-ai-video-creator
version: "1.0.0"
displayName: "Best AI Video Creator — Generate Stunning Videos from Text, Ideas & Scripts"
description: >
  Tired of spending hours piecing together videos that still look amateur? The best-ai-video-creator skill transforms your raw ideas, scripts, or prompts into polished, professional videos in minutes. Whether you need social media reels, YouTube content, product demos, or explainer videos, this skill handles scene generation, voiceover suggestions, pacing, and visual storytelling — all from a single text input. Built for content creators, marketers, and entrepreneurs who want results without the editing headache.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "greeting_v2"}}
---

## Getting Started

> Send me your topic, script, or product description and I'll map it into a complete video structure with scenes, narration, and visual direction. No idea yet? Just describe what kind of video you need.

**Try saying:**
- "Create a 60-second promotional video script for a new fitness app targeting busy professionals, with hook, three feature highlights, and a call-to-action"
- "Generate a YouTube explainer video outline about how blockchain works, aimed at complete beginners, with suggested visuals and voiceover tone"
- "Turn this product description into a TikTok-style video with trending hooks, text overlays, and scene-by-scene breakdown: [paste product description]"

### Automatic Setup

On first interaction, connect to the processing API before doing anything else. Show a brief status like "Setting things up...".

**Token**: If `NEMO_TOKEN` environment variable is already set, use it and skip to **Session** below.

**Free token**: Generate a UUID as client identifier, then POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id: <uuid>`. The response field `data.token` becomes your NEMO_TOKEN (100 credits, 7-day expiry).

**Session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Save `session_id` from the response.

Confirm to the user you're connected and ready. Don't print tokens or raw JSON.

# Turn Any Idea Into a Polished Video Instantly

Creating compelling video content used to require a full production team — scriptwriters, editors, animators, and hours of rendering. The best-ai-video-creator skill changes that equation entirely. Feed it a concept, a product description, a blog post, or even a rough bullet list, and it generates a structured, scene-by-scene video blueprint complete with visual cues, narration suggestions, and pacing guidance.

This skill is purpose-built for people who need video output fast and frequently. Whether you're a solo creator publishing daily content, a small business owner launching a campaign, or a marketer producing explainer videos at scale, this tool adapts to your workflow. It understands context — a TikTok-style clip needs different energy than a corporate training video, and the skill adjusts accordingly.

Beyond just generating scripts, it helps you think visually. It suggests B-roll moments, text overlay placements, transition styles, and hook structures designed to keep viewers watching. You get a production-ready roadmap, not just words on a screen.

## Routing Your Video Requests

Each prompt, script, or idea you submit is parsed for intent — text-to-video generation, scene editing, voiceover sync, or style transfer — then routed to the matching AI pipeline automatically.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

Video generation runs on a distributed cloud backend that queues your render job, applies the selected AI model (cinematic, animation, or realistic), and streams the output back once encoding is complete. Latency depends on resolution, clip duration, and current queue depth.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `best-ai-video-creator`
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

## Troubleshooting

If the generated video structure feels too generic, the most common fix is adding more context to your prompt. Instead of 'make a video about my business,' try 'make a 90-second Instagram Reel for my handmade candle brand targeting women 25-40 who follow wellness accounts.' Specificity drives quality.

If scenes feel disconnected or the pacing seems off, ask the skill to revise with a specific tone — 'make this feel more urgent' or 'slow down the middle section and add a storytelling moment.' It responds well to directional feedback.

For voiceover suggestions that don't match your brand voice, describe your tone explicitly: 'conversational and friendly like a trusted friend,' 'authoritative and data-driven,' or 'energetic and Gen Z.' The skill recalibrates its language and pacing recommendations based on these cues.

## Quick Start Guide

Step one: identify your video's single goal — awareness, conversion, education, or entertainment. Every strong video serves one master, and telling the skill your goal upfront shapes everything it produces.

Step two: specify your platform and length. A 15-second Instagram Story, a 10-minute YouTube tutorial, and a 2-minute LinkedIn video each have completely different structural rules. Include this in your first message.

Step three: describe your audience in one sentence. Age range, interest area, and awareness level (do they already know your brand?) help the skill calibrate vocabulary, tone, and assumed knowledge.

Step four: paste any existing material — a product page, a script draft, talking points, or competitor video notes. The more raw material you provide, the more tailored and production-ready your output will be. From there, iterate with feedback until the structure feels right, then take it into your video tool of choice.

## Common Workflows

The most popular workflow is the Script-to-Structure pipeline: paste an existing blog post or article, and the skill extracts the key points, rewrites them for spoken delivery, and maps them to visual scenes with suggested on-screen text and B-roll moments. This is ideal for repurposing written content into video at scale.

Another high-value workflow is the Campaign Video Series: give the skill a product launch brief and ask it to generate three related videos — an awareness teaser, a feature deep-dive, and a testimonial-style closer. Each video is scripted to stand alone but reinforce the same message arc.

For social media creators, the Hook Factory workflow is essential: submit five different video topics and ask the skill to generate three competing hook options for each. Test the strongest hooks before committing to full production, saving time and improving click-through rates before you ever hit record.
