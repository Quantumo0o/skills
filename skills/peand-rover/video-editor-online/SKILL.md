---
name: video-editor-online
version: 1.0.2
displayName: "Video Editor Online — Edit Videos in Your Browser with AI, No Download Needed"
description: >
  Edit videos online using AI — no software download, no installation, no powerful computer required. NemoVideo runs entirely in the cloud: upload a video from any device, describe the edit in plain language, and download the polished result. Trim, cut, merge, add subtitles, apply color grading, overlay music, generate voiceover, add transitions, remove silences, and export in any format — all through a browser-based conversation that replaces the traditional editing timeline with natural language instructions.
metadata: {"openclaw": {"emoji": "🌐", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# Video Editor Online — Edit Videos in Your Browser with AI

Video editing software assumes you have three things: a powerful computer (discrete GPU, 16GB+ RAM), time to learn a complex interface (timelines, tracks, keyframes, render settings), and a subscription budget ($20-55/month for professional tools). Most people who need to edit a video have none of these. The student on a Chromebook, the small business owner on a 5-year-old laptop, the marketing manager who needs a quick trim between meetings, the teacher preparing lesson content on a tablet — they all need editing capability without the prerequisites. Browser-based editors exist but most replicate desktop complexity in a slower environment: laggy timelines, confusing codec options, and features locked behind premium tiers. They solved the download problem but kept the learning curve. NemoVideo takes a fundamentally different approach. There is no timeline. There is no render queue. There is no codec menu. The editing interface is a conversation: upload the video, describe what you want in plain language ("trim the first 10 seconds, add captions, put some chill music underneath"), and the AI processes the edit on cloud GPUs and returns the finished video. A $200 Chromebook produces the same output quality as a $4,000 editing workstation because the processing happens in the cloud, not on your device.

## Use Cases

1. **Quick Social Media Edit — Any Device (15-60s)** — A realtor records a property walkthrough on their phone and needs it polished before an open house. From their tablet at a coffee shop: uploads to NemoVideo, types "trim the first 5 seconds, stabilize the shaky parts, add property address as text overlay at the bottom, add calm piano music, export vertical for Instagram." Downloads a polished Reel 3 minutes later. No app installed, no editor learned, no laptop needed.
2. **Full YouTube Edit — From a Chromebook (5-20 min)** — A student creator's laptop is a school Chromebook that can't run Premiere or even iMovie. NemoVideo from Chrome: removes silences, adds zoom-cuts, applies color grading, adds background music with ducking, generates captions, and exports 1080p. The complete YouTube workflow from a device that was never designed for video production.
3. **Team Review Workflow — Collaborative Iteration (any length)** — A marketing team iterates on a product video. Person 1 uploads and requests the initial edit. Person 2 reviews and adds feedback: "make the music quieter, add our logo watermark, and change the CTA text." Person 3 adds localization: "generate Spanish subtitles." Each iteration refines the video without version-control confusion or file-sharing hassles.
4. **Batch Processing from a Tablet (any count)** — A social media manager on vacation needs to process 8 client videos from an iPad. NemoVideo: batch-uploads all 8, applies consistent brand-matching edits ("trim first 3 seconds, add brand color grade, add captions, export 9:16"), and delivers all 8 finished videos. Enterprise-grade batch processing from a tablet on hotel WiFi.
5. **Emergency Turnaround — Breaking Content (any length)** — A news team needs to turn around a video clip in 10 minutes. No time to open editing software, import, edit, render. NemoVideo: "trim to the key 30 seconds, add breaking news lower-third, add captions, export immediately." Cloud processing is faster than a desktop render cycle.

## How It Works

### Step 1 — Open Browser and Upload
No download. No account. Upload from any browser on any device — phone, tablet, Chromebook, desktop. NemoVideo handles all formats automatically.

### Step 2 — Describe the Edit
Natural language. As detailed or as brief as you want. "Make it look good" works. "Trim 0:00-0:12, remove silences over 0.8s, warm color grade, lo-fi at -18dB with ducking, word-by-word captions, export 9:16 + 16:9" also works.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "video-editor-online",
    "prompt": "Edit a 6-minute talking-head video for YouTube, from my browser. Trim the first 10 seconds (setup fumble) and last 8 seconds. Remove all silences over 1 second. Add zoom-cuts every 12 seconds for energy. Color grade: warm and professional. Background music: acoustic at -20dB with speech ducking. Captions: word-by-word highlight, white text, yellow active word. Export 16:9 1080p for YouTube and 9:16 best 55 seconds for Shorts.",
    "operations": ["trim", "silence-removal", "zoom-cuts", "color-grade", "music", "captions"],
    "trim_start": 10,
    "trim_end": 8,
    "silence_threshold": 1.0,
    "color_grade": "warm-professional",
    "music": "acoustic",
    "music_volume": "-20dB",
    "captions": "word-highlight",
    "exports": [
      {"format": "16:9", "resolution": "1080p"},
      {"format": "9:16", "duration": "55 sec", "captions": "word-highlight"}
    ]
  }'
```

### Step 4 — Download Anywhere
The finished video downloads as a standard MP4. No codec pack, no player required. Works on every device, every platform.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the edit in plain language |
| `operations` | array | | Explicit list of operations |
| `trim_start` | float | | Seconds to remove from beginning |
| `trim_end` | float | | Seconds to remove from end |
| `silence_threshold` | float | | Remove silences above N seconds |
| `zoom_cuts` | boolean | | Add zoom-cuts for energy (default: true) |
| `color_grade` | string | | "warm-professional", "bright-clean", "cinematic", "moody" |
| `music` | string | | "acoustic", "lo-fi", "corporate", "cinematic", "none" |
| `music_volume` | string | | "-14dB" to "-22dB" |
| `captions` | string | | "word-highlight", "sentence", "bold-centered", "srt" |
| `exports` | array | | Multiple format/resolution exports |
| `batch` | array | | Multiple videos with same or different edits |

## Output Example

```json
{
  "job_id": "veo-20260328-001",
  "status": "completed",
  "processing": "cloud-gpu (no client hardware required)",
  "outputs": [
    {
      "format": "16:9",
      "resolution": "1920x1080",
      "duration": "4:08",
      "file_size_mb": 48.2,
      "edits": {
        "trimmed": "18 sec removed",
        "silences_removed": "1:34 (92 cuts)",
        "zoom_cuts": 20,
        "color_grade": "warm-professional",
        "music": "acoustic at -20dB with ducking",
        "captions": "word-highlight (178 lines)"
      }
    },
    {
      "format": "9:16",
      "resolution": "1080x1920",
      "duration": "0:55",
      "segment": "1:48-2:43 (highest engagement prediction)",
      "captions": "word-highlight"
    }
  ]
}
```

## Tips

1. **Cloud processing equalizes all devices** — A $200 Chromebook gets the same output quality as a $4,000 MacBook Pro. The GPU rendering happens in the cloud. Your device just uploads and downloads.
2. **Natural language beats timeline precision for 90% of edits** — "Remove the boring parts, add music, and make it look professional" produces better results faster than scrubbing a timeline for every edit that doesn't require frame-exact precision.
3. **Multi-format export in one pass** — Process once, export YouTube (16:9) + TikTok (9:16) + Instagram (1:1). Three platform-ready versions from one upload, one instruction.
4. **Batch editing scales instantly** — 10 videos with the same brand rules process in parallel on cloud infrastructure. No queueing, no waiting for each to finish.
5. **Zero IT friction** — No software approval, no compatibility testing, no "this requires macOS 14 or later," no "your GPU isn't supported." Open browser, upload, edit, download.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | Up to 4K | YouTube / website / presentation |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Shorts |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |
| SRT | — | Subtitle file |
| WAV | — | Audio extraction |

## Related Skills

- [free-youtube-video-editor](/skills/free-youtube-video-editor) — YouTube editing free
- [video-maker-free](/skills/video-maker-free) — Free video maker
- [how-to-add-music-to-video](/skills/how-to-add-music-to-video) — Add music to video
