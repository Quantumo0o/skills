---
name: video-dub
description: Windows-first video localization pipeline for downloading, transcribing, translating, dubbing, and retiming YouTube or Bilibili videos.
---

# Video Dub Skill

Use this skill when a user wants to turn a source video into a localized dubbed video with aligned subtitles.

This skill bundles the complete video_pipeline, so the pipeline code is included with the skill installation.

## What the pipeline does

Primary workflow:

1. Download the source video
2. Optionally replace only the opening picture with a cover image
3. Extract mono 16k audio
4. Transcribe with Whisper
5. Clean English blocks, correct proper nouns, and translate
6. Generate TTS
7. Retime the video to match the dub
8. Export aligned SRT files without burning subtitles

The main controller is `video_pipeline/scripts/quick_deliver.py`.

## Supported modes

- **Forward localization**: English video to Chinese dubbed video
- **Reverse localization**: Chinese video to English dubbed video

## Default assumptions

Unless the user or a channel rule says otherwise:

- Whisper model: `small`
- Default TTS provider: `edge`
- Default Edge voice: `zh-CN-YunjianNeural`
- Retiming padding: `0.05s`
- Final subtitle target: `*_zh_retimed_v4_final.srt`

For reverse workflows, a reasonable English voice: `en-US-GuyNeural`

## Running the pipeline

```powershell
# Set environment variables
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"

# Run the pipeline
cd <skill_root>\video_pipeline
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

To rebuild an already processed video:

```powershell
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID" --refresh-tts
```

## Environment variables

Required:

```powershell
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
```

Recommended for YouTube reliability:

```powershell
$env:YTDLP_COOKIES_FILE="path\to\youtube_cookies.txt"
$env:NODE_OPTIONS="--max-old-space-size=4096"
```

Optional TTS overrides:

```powershell
$env:TTS_PROVIDER="edge"
$env:EDGE_TTS_VOICE="zh-CN-YunjianNeural"
```

Other supported providers: `volcengine`, `azure`, `windows_sapi`

## Expected outputs

After a successful forward run:

- `video_pipeline/data/output/*_zh_retimed_v4.mp4`
- `video_pipeline/data/subtitles/*_zh_retimed_v4_final.srt`

Optional outputs:

- `video_pipeline/data/output/*_zh_male.mp4`
- `video_pipeline/data/subtitles/*_zh.srt`
- `video_pipeline/data/subtitles/*_zh_retimed_v4.srt`
- `video_pipeline/data/structured/*.json`
- `video_pipeline/data/state/debug/*_en_blocks.json`

## Agent guidance

When an agent runs this skill:

1. Validate the input URL
2. Set required environment variables
3. Run `quick_deliver.py` from the `video_pipeline` subdirectory
4. Return the final video and subtitle paths
5. If the user asks for partial reruns, rebuild only the requested stage when possible

## Packaging notes

This skill is published with the pipeline code bundled in the `video_pipeline/` subdirectory.

The bundle excludes generated outputs and caches (data/raw/, data/audio/, data/tts/, data/output/, data/state/, etc.).

To rebuild the release bundle from source:

```powershell
.\scripts\package_release.ps1 -SourceRoot "D:\video_pipeline" -DestinationRoot "<skill_destination>"
```
