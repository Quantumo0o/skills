---
name: ai-lip-sync-video
version: "1.0.0"
displayName: "AI Lip Sync Video — Sync Any Audio to On-Screen Speakers Automatically"
description: >
  Drop a video and a new audio track, and watch mouths move in perfect sync — no studio, no reshoots required. This ai-lip-sync-video skill analyzes facial movements frame-by-frame and remaps lip motion to match any spoken audio you provide. Ideal for dubbing content into new languages, replacing flubbed dialogue, or animating static images with voiceovers. Works with influencer clips, explainer videos, and localized marketing content.
metadata: {"openclaw": {"emoji": "🎙️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome! I can sync any audio track to a speaker's lip movements in your video — no reshoots, no manual editing. Upload your video and audio file to get started.

**Try saying:**
- "Sync Spanish audio to my video"
- "Replace dialogue in this clip"
- "Animate lips to my voiceover"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Make Any Mouth Move to Any Voice

Reshooting a scene just because the audio didn't land right is expensive and time-consuming. This skill removes that bottleneck entirely. Upload your existing video footage alongside a new audio file — whether it's a translated voiceover, a cleaner take, or a fully synthesized voice — and the AI will remap the speaker's lip movements to match the new audio precisely.

The technology works by detecting the facial region in each frame, mapping phoneme patterns from the audio onto the visible mouth shape, and blending the result back into the original video. The surrounding face, background, and body remain untouched. The output looks natural rather than patched.

Content creators use this to localize videos for international audiences without hiring on-camera talent in every language. Marketers use it to swap spokesperson dialogue after a product change. Educators use it to update course videos without re-recording entire lessons. If your video has a talking face and you have audio that needs to match it, this skill handles the rest.

## Routing Sync Requests Intelligently

Each lip sync request is parsed for audio source, target video, and speaker detection parameters before being dispatched to the appropriate processing pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Rendering API Reference

The backend leverages a frame-accurate phoneme alignment engine that maps audio waveforms to facial landmark keypoints in real time, ensuring natural mouth shape transitions across every speaker detected on screen. Rendered frames are composited and returned as a lossless or compressed output depending on your export settings.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-lip-sync-video`
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

## Use Cases

The most common use case is video localization — taking a single piece of content and making it feel native in multiple languages without filming separate versions. Marketing teams, YouTube creators, and online educators use this to expand reach into Spanish, French, Portuguese, and other language markets with minimal overhead.

A second popular use case is dialogue correction. If an on-camera presenter misspoke a product name, a statistic, or a key term, the entire scene doesn't need to be reshot. Record the corrected line, upload both files, and the fix is applied invisibly.

Animators and social media creators also use this skill to bring static portraits or illustrated characters to life. Pair a headshot or a drawn character image with any audio clip, and the output is an animated, lip-synced video ready for reels, explainers, or presentations. It's particularly useful for creating spokesperson content when live filming isn't an option.

## Performance Notes

Lip sync quality depends heavily on the source video. Footage where the speaker's face is clearly visible, well-lit, and facing mostly forward will produce the sharpest results. Heavy side angles, partial face obstructions (like hands or microphones in front of the mouth), or low-resolution video can reduce accuracy in the mouth region.

Audio clarity matters equally. Clean, noise-free recordings with clear phoneme separation give the model the best signal to work from. Heavily compressed audio, background music mixed into the voiceover, or very fast speech patterns may result in slightly less precise mouth timing.

For longer videos, processing time scales with duration. Clips under two minutes typically process fastest. If you're working with a longer piece, consider splitting it into segments for quicker turnaround and easier review.

## Troubleshooting

If the lip sync output looks off or unnatural, the most common cause is a mismatch in speech pace between the original video and the replacement audio. If your new voiceover is significantly faster or slower than the original performance, the model has less room to create convincing mouth movement. Try adjusting the audio pacing before uploading.

If the face detection seems to miss the speaker entirely — for instance, the background changes but the mouth doesn't — check that the face is not too small in the frame or obscured by on-screen graphics and overlays. Removing lower-third text or graphic overlays before processing can help.

Unexpected artifacts around the mouth area are usually caused by very low source video resolution or heavy video compression. Re-exporting the source file at a higher bitrate before uploading often resolves this. If issues persist, share a short test clip (under 15 seconds) so the problem can be isolated quickly.
