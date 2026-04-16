# video_pipeline

A Windows-first pipeline for YouTube/Bilibili video localization: download, transcribe, translate, dub, and retime videos.

## Quick Start

```powershell
# Install dependencies
cd video_pipeline
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Set required environment variables
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
$env:YTDLP_COOKIES_FILE="path\to\youtube_cookies.txt"  # Optional, for reliable YouTube downloads

# Run the pipeline
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## What the Pipeline Does

1. Download the source video
2. Optionally replace the intro with a cover image
3. Extract mono 16k audio
4. Transcribe with Whisper
5. Translate English blocks to Chinese, correct proper nouns
6. Generate Chinese TTS
7. Retime the video to match the dub
8. Export the final retimed video and aligned SRT

## Outputs

- `data/output/*_zh_retimed_v4.mp4` - final dubbed video
- `data/subtitles/*_zh_retimed_v4_final.srt` - final subtitle file

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | Yes | DeepSeek API key for translation |
| `YTDLP_COOKIES_FILE` | No | Path to YouTube cookies.txt for reliable downloads |
| `NODE_OPTIONS` | No | Set to `--max-old-space-size=4096` if YouTube shows JavaScript challenges |

## Default Settings

- Whisper model: `small`
- TTS provider: `edge` (no API key needed)
- Edge voice: `zh-CN-YunjianNeural`
- Retime padding: `0.05s`

## Directory Structure

```
video_pipeline/
  scripts/
    quick_deliver.py    # Main entry point
    download.py
    prepare_video.py
    extract_audio.py
    transcribe.py
    enrich_subtitles.py
    dub_video.py
    retime_video.py
    add_subtitles.py
    services/
  data/
    channel_rules.json   # Per-channel configuration
    proper_nouns.json    # Proper noun glossary
    raw/
    output/
    ...
  requirements.txt
```

## For Agents

When an AI agent runs this pipeline, it should:

1. Set required environment variables
2. Run `scripts/quick_deliver.py`
3. Return paths to:
   - `data/output/*_zh_retimed_v4.mp4`
   - `data/subtitles/*_zh_retimed_v4_final.srt`

See SKILL.md for full agent guidance.
