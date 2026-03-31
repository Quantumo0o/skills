---
name: free-ai-video-maker
version: "1.0.0"
displayName: "Free AI Video Maker — Create Polished Videos from Footage Instantly"
description: >
  Turn raw clips into share-ready videos without spending a cent. This free-ai-video-maker skill analyzes your footage and assembles engaging videos complete with pacing, cuts, and structure — no editing experience needed. Upload files in mp4, mov, avi, webm, or mkv format and get results fast. Ideal for content creators, small business owners, students, and social media managers who need quality output without a production budget.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! Ready to turn your raw footage into a finished video without any editing software or cost? Upload your clips and tell me what you're going for — let's make something worth watching.

**Try saying:**
- "I have three mp4 clips from a weekend trip — can you cut them into a 60-second highlight reel with a travel vibe?"
- "Turn this product demo footage into a clean 30-second social media video that focuses on the key features."
- "I recorded a short interview in mov format — can you trim the awkward pauses and make it feel more polished?"

On first use, the skill connects to NemoVideo automatically:
1. Check for `NEMO_TOKEN` env var, or acquire one via `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` (100 free credits)
2. Persist a Client-ID to `~/.config/nemovideo/client_id` for rate-limit tracking (UUID only, no secrets)
3. Create a session and start working immediately

# Make Real Videos Without Paying for Software

Most people have footage sitting on their devices that never becomes anything. The editing feels overwhelming, the software is expensive, and the learning curve is steep. This skill changes that equation entirely. With the free-ai-video-maker, you describe what you want, upload your clips, and walk away with a finished video that actually looks intentional.

This isn't a template filler or a slideshow generator. The skill works with the actual content of your footage — understanding pacing, identifying usable moments, and assembling a sequence that holds a viewer's attention. Whether you're cutting a product demo, a travel recap, a school project, or a short social clip, the output reflects the story you're trying to tell.

The best part: there's no subscription wall, no watermark negotiation, and no feature locked behind a pricing tier. The free-ai-video-maker skill is built for people who need real results without a real budget — and it supports mp4, mov, avi, webm, and mkv so you can work with whatever you already have.

### Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `NEMO_TOKEN` | Auto-acquired on first use (100 free credits, 7-day expiry) | API authentication |
| `NEMO_API_URL` | `https://mega-api-prod.nemovideo.ai` | API base URL |

## Routing Your Video Requests

When you describe your footage, trimming needs, or style preferences, the skill parses your intent and routes each request to the matching NemoVideo endpoint — whether that's auto-edit, scene assembly, caption burn-in, or export rendering.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference

Under the hood, the skill connects to the NemoVideo backend, which handles timeline stitching, AI-driven cut detection, and codec-level rendering so your footage comes out polished without manual editing. All API calls are authenticated via your NemoVideo session token, passed securely on each request.

**Required headers** on all requests: `X-Skill-Source: $SKILL_NAME`, `X-Skill-Version: $SKILL_VERSION`, `X-Skill-Platform: $SKILL_SOURCE`

**Create session**: `POST $API/api/tasks/me/with-session/nemo_agent` — returns `task_id` and `session_id`

**Send message (SSE)**: `POST $API/run_sse` with `session_id` and user message. Stream responses; ~30% of edits return no text (query state to confirm changes).

**Upload**: `POST $API/api/upload-video/nemo_agent/me/<sid>` — file or URL upload. Supports: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

**Check credits**: `GET $API/api/credits/balance/simple`

**Query state**: `GET $API/api/state/nemo_agent/me/<sid>/latest` — check draft, tracks, generated media

**Export**: `POST $API/api/render/proxy/lambda` — export does NOT cost credits. Poll `GET $API/api/render/proxy/lambda/<id>` until `status: completed`.

**Task link**: `$WEB/workspace/claim?token=$TOKEN&task={task_id}&session={session_id}&skill_name=$SKILL_NAME&skill_version=$SKILL_VERSION&skill_source=$SKILL_SOURCE`

### Common Errors

If you hit a token expiration error, simply re-authenticate by reconnecting your NemoVideo account in the skill settings — your project queue stays intact. A 'session not found' response means your editing session timed out; start a fresh session and re-upload your footage to continue. If you're out of free credits, head to nemovideo.ai to register or upgrade so rendering doesn't stall mid-project.

## Tips and Tricks to Get More from Your Videos

One underused trick: upload more footage than you think you need. The free-ai-video-maker skill can select the strongest moments from a larger batch, which often produces a more natural-feeling result than trying to make a short clip stretch further than it should.

If your first output isn't quite right, don't start over — refine it. Tell the skill what's off: 'the pacing feels too slow in the middle' or 'can you cut the section after the 20-second mark?' Iterating on a near-finished video is almost always faster than regenerating from scratch.

For social-first content, mention the platform in your prompt. A video optimized for TikTok has different pacing and hook structure than one made for LinkedIn or YouTube. The skill adjusts its approach based on context, so naming the destination upfront saves you a round of revisions later.

## Best Practices for Free AI Video Maker

Getting the best results from the free-ai-video-maker skill starts before you hit upload. Shoot in decent lighting when possible — the AI works with what it's given, and well-lit footage gives it more to work with when identifying usable moments and clean cuts.

When describing what you want, be specific about length and purpose. 'Make a short video' is harder to act on than 'make a 45-second Instagram reel that highlights the food at this restaurant.' The more context you provide about your audience and goal, the more the output will match your expectations.

For best file compatibility, mp4 and mov files tend to produce the smoothest processing experience. If you're working with avi, webm, or mkv files, they're fully supported — just make sure the files aren't corrupted or encoded with obscure codecs. Keeping individual clip sizes reasonable also speeds up the workflow significantly.
