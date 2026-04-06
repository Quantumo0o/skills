---
name: free-video-trimmer-online
version: "1.0.0"
displayName: "Free Video Trimmer Online — Cut, Crop & Export Video Clips Instantly"
description: >
  Turn raw footage into polished, share-ready clips without downloading a single app. This free-video-trimmer-online skill lets you cut unwanted sections, isolate the best moments, and export clean video segments directly from your browser. Supports mp4, mov, avi, webm, and mkv formats. Perfect for content creators, students, and social media users who need fast, no-cost trimming without watermarks or paywalls.
metadata: {"openclaw": {"emoji": "✂️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! Ready to cut your video down to exactly what matters? This free video trimmer online lets you remove unwanted footage and export clean clips in seconds — just tell me your file and where you'd like to trim.

**Try saying:**
- "Trim my mp4 video to keep only the section from 0:45 to 2:30"
- "Remove the first 10 seconds and last 15 seconds from this mov file"
- "Cut this webm screen recording down to just the middle 3 minutes starting at 1:00"

On first use, the skill connects to NemoVideo automatically:
1. Check for `NEMO_TOKEN` env var, or acquire one via `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` (100 free credits)
2. Persist a Client-ID to `~/.config/nemovideo/client_id` for rate-limit tracking (UUID only, no secrets)
3. Create a session and start working immediately

# Trim Any Video in Seconds, No Software Needed

Most video trimming tools either cost money, leave watermarks, or require a lengthy download and install process. This skill cuts through all of that. Whether you recorded a long screen capture and only need the first two minutes, or you filmed a 10-minute clip but want to share just the highlight reel, this free video trimmer online gives you precise control over start and end points without any friction.

You can work with the most common video formats — mp4, mov, avi, webm, and mkv — so there's no need to convert your file before trimming. Just bring your footage, specify where you want to cut, and get a clean output file ready to download or share.

This skill is built for real-world use cases: trimming interview recordings, cutting intros off screen recordings, clipping gameplay footage, or preparing short social media videos. No account required, no upload limits buried behind a subscription, and no surprise watermarks on your finished file.

### Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `NEMO_TOKEN` | Auto-acquired on first use (100 free credits, 7-day expiry) | API authentication |
| `NEMO_API_URL` | `https://mega-api-prod.nemovideo.ai` | API base URL |

## Trim Request Routing Explained

When you submit a cut or crop command, ClawHub parses your in-point, out-point, and export format preferences before routing the job to the NemoVideo processing pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference

The NemoVideo backend handles frame-accurate trimming, aspect ratio cropping, and lossless or re-encoded exports via its media processing API. Each call passes your clip parameters — start timestamp, end timestamp, resolution, and codec target — directly to the render queue.

**Required headers** on all requests: `X-Skill-Source: $SKILL_NAME`, `X-Skill-Version: $SKILL_VERSION`, `X-Skill-Platform: $SKILL_SOURCE`

**Create session**: `POST $API/api/tasks/me/with-session/nemo_agent` — returns `task_id` and `session_id`

**Send message (SSE)**: `POST $API/run_sse` with `session_id` and user message. Stream responses; ~30% of edits return no text (query state to confirm changes).

**Upload**: `POST $API/api/upload-video/nemo_agent/me/<sid>` — file or URL upload. Supports: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

**Check credits**: `GET $API/api/credits/balance/simple`

**Query state**: `GET $API/api/state/nemo_agent/me/<sid>/latest` — check draft, tracks, generated media

**Export**: `POST $API/api/render/proxy/lambda` — export does NOT cost credits. Poll `GET $API/api/render/proxy/lambda/<id>` until `status: completed`.

**Task link**: `$WEB/workspace/claim?token=$TOKEN&task={task_id}&session={session_id}&skill_name=$SKILL_NAME&skill_version=$SKILL_VERSION&skill_source=$SKILL_SOURCE`

### Common Errors

If your token has expired, simply re-authenticate through ClawHub to generate a fresh bearer token and resubmit your trim job. A 'session not found' response means your editing session timed out — start a new session and re-upload your source clip. Out of credits? Head to nemovideo.ai to register for a free tier or upgrade your plan to keep cutting without interruption.

## Performance Notes

This free video trimmer online is optimized for speed on common file sizes and formats. Short to medium-length clips — roughly under 30 minutes — process quickly regardless of resolution. Larger files such as raw 4K footage or lengthy recordings may take additional time depending on file size.

For the smoothest experience, mp4 and webm files tend to process fastest due to their efficient compression. Files in avi or mov format are fully supported but may take slightly longer to handle depending on codec. If you're trimming a very large file, consider compressing or converting it first to reduce processing time.

The trimmer performs frame-accurate cuts, meaning your output clip will begin and end exactly where you specified without re-encoding artifacts at the cut points. Audio sync is preserved across all supported formats, so your trimmed clip will sound exactly as it did in the original footage.

## Use Cases

This free video trimmer online fits naturally into dozens of everyday workflows. Social media creators use it to cut down long recordings into punchy 60-second clips for Instagram Reels or TikTok. Educators and trainers trim lengthy screen recordings to remove setup time and keep only the instructional content. Journalists and podcasters clip specific soundbite segments from interview footage for embedding in articles or episode previews.

Gamers use it to isolate highlight moments from long gameplay sessions before uploading to YouTube or Discord. Remote workers trim Zoom or Teams recordings to extract just the relevant portions before sharing with colleagues who missed a meeting. Filmmakers and students use it to pull rough cut segments from raw footage during the editing planning phase.

Essentially, any situation where you have more video than you need — and want a fast, free way to cut it down without installing software — is exactly what this skill was built for.

## Quick Start Guide

Getting started with this free video trimmer online takes less than a minute. First, upload or link your video file — supported formats include mp4, mov, avi, webm, and mkv. Next, specify your trim points using timestamps (for example, 'start at 0:30, end at 2:15'). You can also describe what to remove, such as 'cut the last 20 seconds' or 'remove everything before the 1-minute mark'.

Once your trim parameters are set, the skill processes your clip and delivers a downloadable output file. No account creation, no email confirmation, and no watermark is added to your exported video. If your trim produces an unexpected result, simply adjust your timestamps and re-run — the process is fast enough that iteration is painless.

For best results, provide timestamps in minutes and seconds format (e.g., 1:45) and double-check your source file format is one of the five supported types before uploading.
