---
name: lip-sync-video
version: "1.0.0"
displayName: "Lip Sync Video — Match Audio to Mouth Movements with Frame-Perfect Accuracy"
description: >
  Turn raw footage into polished lip-sync-video content where every word lands exactly when mouths move. This skill analyzes audio waveforms alongside facial motion to align dialogue, dubbing, or voiceovers to on-screen speakers — frame by frame. Ideal for content creators dubbing multilingual videos, animators syncing character speech, or marketers localizing ad campaigns without reshoots. No manual keyframing required.
metadata: {"openclaw": {"emoji": "🎤", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! Ready to sync your audio perfectly to on-screen mouth movements? Upload your video and audio files and tell me what you're working on — let's build your lip-sync video.

**Try saying:**
- "I have a talking-head video in English and a dubbed Spanish voiceover — sync the audio so the mouth movements match the new track."
- "Generate a lip-sync video from my animated character clip and this recorded dialogue file, matching phonemes to the mouth shape keyframes."
- "My corporate explainer video has a replaced voiceover that's slightly ahead of the speaker — fix the sync so it lines up naturally."

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Make Every Word Land on the Right Frame

Lip syncing used to mean hours of manual frame-stepping, nudging audio clips by milliseconds, and still ending up with a result that felt slightly off. This skill changes that by doing the heavy analytical work for you — detecting facial landmarks, reading phoneme timing from your audio track, and generating a synchronized output where speech and mouth movement feel genuinely connected.

Whether you're dubbing a tutorial into Spanish, animating a talking character for a short film, or replacing a voiceover in a corporate video without going back to the studio, this skill handles the alignment logic so you can focus on the creative side. It works with pre-recorded video clips and separate audio files, matching them together based on actual speech patterns rather than simple waveform peaks.

The result is a lip-sync-video that holds up under close viewing — no rubbery mouth delays, no audio that races ahead of the speaker. Creators working in social content, e-learning, animation, and localization have used this to cut sync time from hours to minutes while maintaining a professional finish.

## Routing Sync Requests Accurately

When you submit a lip sync job, your request is parsed for target audio track, source video, and phoneme alignment preferences before being dispatched to the appropriate processing pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Backend API Reference

The cloud processing backend handles frame-level phoneme detection and viseme mapping in real time, syncing jaw, lip, and cheek keyframes to audio waveforms at the millisecond level. All render jobs are queued through a distributed worker system that prioritizes frame-perfect alignment over raw speed.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `lip-sync-video`
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

**Multilingual dubbing:** Record or commission a translated voiceover at the same approximate pacing as the original. Feed both the original video and the new audio into the skill. The skill will retime phoneme boundaries in the dubbed track to match visible mouth movements without altering pitch or tone — preserving the natural sound of the new language.

**Animation lip sync:** Export your character animation as a video file with a silent or reference audio track. Submit it alongside the final recorded dialogue. The skill maps vowel and consonant sounds to frame ranges, which you can use directly as a finished render or import timing data back into your animation software.

**Voiceover replacement for localization:** When marketing teams need the same video in multiple regions, record each regional voiceover separately and run each one through the skill against the same master video. This produces region-specific lip-sync-video outputs from a single source asset — no reshoots, no re-editing the base timeline.

**Podcast or interview cleanup:** If a recorded interview has audio sync drift caused by encoding lag, submit the drifted video and the clean isolated audio track to realign the speaker's mouth movements to the corrected audio.

## Troubleshooting

**Audio and video lengths don't match:** If your dubbed audio track is longer or shorter than the original video, the skill will flag a duration mismatch. Trim or time-stretch your audio to roughly match the video length before submitting — a difference of more than 10% can reduce sync accuracy significantly.

**Mouth movements not detected:** This usually happens when the speaker's face is partially obscured, shot at a steep side angle, or the video resolution is too low. For best results, use footage where the speaker's lips are clearly visible and the video is at least 480p. Strong backlighting can also confuse facial landmark detection — try brightening the input clip if detection fails.

**Sync drifts mid-video:** Long videos with variable speech pacing sometimes show drift past the two-minute mark. Break the video into segments at natural pause points (scene cuts, pauses between sentences) and sync each segment independently, then reassemble. This maintains accuracy across longer content without degrading toward the end.

## Integration Guide

**Connecting your media files:** The skill accepts video files in MP4, MOV, and WebM formats, and audio in MP3, WAV, or AAC. For the cleanest sync results, export your audio at the same sample rate as the original video's embedded audio track — typically 44.1kHz or 48kHz. Mismatched sample rates are a common source of subtle timing errors.

**Working with ClawHub pipelines:** You can chain this skill with the ClawHub video trimmer or audio normalizer before running lip sync, ensuring your inputs are clean and level-matched before the alignment step runs. After sync, route the output to a caption generator or export node depending on your delivery format.

**Batch processing:** If you're localizing a video series into multiple languages, structure your inputs as paired sets — one video file mapped to one audio file per language — and submit them as a batch job. Label each pair clearly so outputs are returned with matching filenames. Avoid mixing different source videos in the same batch to prevent cross-mapping errors.

**Output formats:** The skill returns a synchronized video file in the same container format as your input. If you need frame-level timing metadata (for use in animation or subtitle workflows), request a JSON timing export alongside the video output when submitting your task.
