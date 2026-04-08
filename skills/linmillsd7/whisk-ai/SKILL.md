---
name: whisk-ai
version: "1.0.0"
displayName: "Whisk AI Image Remixer — Transform Photos Into New AI-Generated Visuals"
description: >
  Drop an image and describe a new scene — whisk-ai blends your visual inputs with creative AI generation to produce entirely fresh imagery. Built around Google's Whisk AI technology, this skill lets you remix faces, objects, and styles into surreal, artistic, or photorealistic results. Perfect for designers, content creators, and curious experimenters who want to push visuals beyond filters and presets.
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome to whisk-ai — your creative lab for remixing images into entirely new AI-generated visuals! Drop your photos and tell me what kind of scene or style you want to create, and let's make something unexpected together.

**Try saying:**
- "Remix my photo in oil painting style"
- "Place my subject in a sci-fi scene"
- "Blend two images into one visual"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Remix Reality: Your Images, Reimagined From Scratch

Whisk AI isn't a filter — it's a creative engine. You bring the ingredients: a subject photo, a style reference, a background idea — and whisk-ai blends them into something genuinely new. Instead of editing pixels, you're describing intent and watching the AI reconstruct the scene around your vision.

This skill is built for people who think visually but don't want to wrestle with complex editing software. Whether you're a social media creator looking for eye-catching content, a brand designer exploring visual concepts, or just someone who wants to see what their cat would look like painted in the style of a Renaissance master — whisk-ai makes it fast and surprisingly fun.

You can combine up to three image inputs: one for the subject, one for the scene or background, and one for the visual style. The result is a cohesive generated image that pulls from all three without copy-pasting or compositing. It's generative remixing at its most intuitive.

## Routing Remix Requests Intelligently

When you submit a subject, scene, or style image, Whisk AI interprets your intent and routes the generation request through its Imagen-powered backend to produce a remixed visual that blends your inputs into a coherent new composition.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Whisk API Backend Reference

Whisk AI processes all image remixing through Google's cloud-hosted Imagen model, meaning your uploaded subjects, scenes, and style references are analyzed and synthesized server-side before the remixed image is returned. Latency depends on queue load and the complexity of the multi-image prompt fusion.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `whisk-ai`
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

## Quick Start Guide

**Step 1: Choose your inputs**
Decide what you want to remix. You can upload a subject image (a person, object, or animal), a background or scene image, and a style reference (an artwork, photo, or aesthetic). Any combination works — even just a text prompt.

**Step 2: Describe your vision**
Add a text description to guide the generation. Be specific about mood, lighting, setting, or artistic style. For example: 'warm golden hour lighting, impressionist brushstrokes, outdoor garden setting.'

**Step 3: Generate and iterate**
Send your inputs and let whisk-ai do its thing. Review the result and refine — you can adjust your description, swap out a reference image, or ask for a different style variation. Each generation is unique, so running it multiple times gives you options to choose from.

**Pro tip:** Use a famous artwork or a screenshot of a visual style you love as your style input. Whisk-ai is particularly good at translating artistic aesthetics — from ukiyo-e woodblock prints to brutalist graphic design — onto new subjects.

## FAQ

**What exactly does whisk-ai do with my images?**
Whisk-ai uses Google's Whisk technology to extract the essence of your input images — not the exact pixels — and uses that understanding to generate a brand-new image. Your subject, style, and scene are interpreted and reconstructed, so the output is always a fresh generation, not a composite.

**Can I use just one image or do I need three?**
You can absolutely use just one image or even a text description alone. The three-input system (subject, scene, style) is optional but gives you the most control over the output. Mix and match however feels natural.

**Will it look exactly like my reference photo?**
Not exactly — and that's the point. Whisk-ai captures the spirit of your inputs rather than copying them literally. Expect creative interpretation, not pixel-perfect reproduction. If you want a closer likeness, be more specific in your text description.

**What kinds of images work best?**
Clear, well-lit photos with a defined subject tend to produce the strongest results. Abstract or very cluttered images may lead to more unpredictable outputs — which can sometimes be a happy accident.
