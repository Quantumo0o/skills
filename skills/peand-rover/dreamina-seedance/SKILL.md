---
name: dreamina-seedance
version: "1.0.0"
displayName: "Dreamina Seedance AI Video Generator — Animate Ideas Into Cinematic Motion"
description: >
  Drop a concept, a prompt, or an existing image and watch dreamina-seedance turn it into fluid, high-quality AI-generated video. Built on Dreamina's Seedance model, this skill transforms still visuals and text descriptions into dynamic scenes with consistent motion, rich detail, and cinematic pacing. Perfect for content creators, marketers, and storytellers who want studio-quality video output without a production crew.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome to Dreamina Seedance — your AI-powered video generation studio. Describe a scene or share an image, and I'll animate it into a cinematic video clip ready to use.

**Try saying:**
- "Generate a short video of a lone astronaut walking across a red desert planet at golden hour with dust swirling around their boots"
- "Turn this product image into a 5-second animated clip with soft lighting and a slow zoom effect for an Instagram ad"
- "Create a dreamlike video of a forest at night where fireflies are gradually lighting up around an old wooden cabin"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Turn Words and Images Into Moving Stories

Dreamina Seedance brings your creative vision to life by generating smooth, detailed video clips directly from text prompts or reference images. Whether you're imagining a sweeping landscape, a product in motion, or a character walking through a neon-lit street, this skill handles the heavy lifting — producing video that feels intentional and visually cohesive.

Unlike simple animation tools, Seedance understands context and motion logic. A prompt like "a paper boat drifting down a rainy cobblestone alley" doesn't just produce movement — it produces atmosphere. The model interprets lighting, texture, and pacing to deliver results that match the mood you're after.

This skill is ideal for social media creators who need scroll-stopping content, small business owners building product showcases, and indie filmmakers prototyping scene ideas. You don't need prior video production experience — just a clear idea and the willingness to experiment.

## Routing Your Animation Requests

When you submit a prompt or upload reference footage, ClawHub parses your intent and routes it directly to Dreamina Seedance's motion synthesis pipeline, selecting the appropriate generation mode — text-to-video, image-to-video, or keyframe interpolation — based on your input type.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Seedance API Backend Reference

Dreamina Seedance processes all generation jobs on its proprietary cloud inference cluster, applying temporal diffusion modeling to produce fluid, cinematically consistent motion frames. Render times vary based on clip duration, resolution tier, and current queue load across Seedance's distributed GPU nodes.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `dreamina-seedance`
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

## FAQ

**What kinds of prompts work best with Dreamina Seedance?** Scene-based prompts with clear subjects, environments, and motion cues work best. Think in terms of a single camera shot — what would the viewer see, how does it move, and what's the atmosphere?

**Can I use my own images as input?** Yes. Uploading a reference image gives Seedance a visual anchor to animate from, which is especially useful for product videos or character-based content.

**How long are the generated video clips?** Seedance typically generates short-form clips optimized for social and digital use. These are ideal as standalone content or as building blocks for longer edits.

**Can I generate videos in a specific style?** Absolutely — include style references in your prompt such as "cinematic film grain," "anime aesthetic," "documentary handheld," or "luxury brand commercial" to steer the visual tone.

## Quick Start Guide

Getting your first Seedance video is straightforward. Start by typing a descriptive scene prompt — the more specific, the better. Include details like time of day, environment, subject movement, and mood. For example: "a slow-motion close-up of raindrops hitting a still pond at dusk" will yield far more targeted results than "rain video."

If you have a reference image, share it alongside your prompt to guide the visual style and subject matter. Seedance will use the image as an anchor while generating motion around it.

Once your video is generated, you can iterate by adjusting the prompt — try changing the camera movement ("push in slowly"), the lighting ("overcast vs. golden hour"), or the subject action ("walking vs. running"). Each variation can unlock a different creative direction from the same core idea.

## Performance Notes

Dreamina Seedance performs best with prompts that balance specificity and creative freedom. Overly rigid prompts with conflicting instructions (e.g., "slow motion but fast-paced action") may produce inconsistent results — aim for a single clear visual intention per generation.

Video length and complexity affect generation time. Short clips with focused subjects typically render faster and with higher consistency than dense multi-subject scenes. For best results, treat each generation as a single scene rather than a multi-shot sequence.

If your output doesn't match expectations, refine rather than restart. Small changes — swapping "bright sunlight" for "diffused afternoon light" or adding "camera tilts upward" — can dramatically shift the result. Seedance responds well to cinematic language borrowed from photography and filmmaking.
