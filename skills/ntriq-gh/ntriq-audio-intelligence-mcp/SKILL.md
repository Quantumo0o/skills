---
name: ntriq-audio-intelligence-mcp
description: "Transcribe, summarize, and analyze audio files using local Whisper + Qwen. Returns transcript, segments, and action items."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [audio,transcription,analysis]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Audio Intelligence MCP

Transcribe, summarize, and analyze audio using local Whisper + Qwen. Returns full transcript with per-segment timestamps, speaker diarization, key topics, and extracted action items. Supports MP3, WAV, M4A, OGG up to 2GB.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio_url` | string | ✅ | URL or local path to audio file |
| `language` | string | ❌ | ISO 639-1 code (auto-detected if omitted) |
| `speakers` | integer | ❌ | Expected speaker count for diarization |
| `extract_actions` | boolean | ❌ | Extract action items (default: true) |

## Example Response

```json
{
  "transcript": "Let's finalize the Q2 budget by Friday. Marketing needs $50K approved.",
  "segments": [
    {"start": 0.0, "end": 4.2, "speaker": "A", "text": "Let's finalize the Q2 budget by Friday."},
    {"start": 4.5, "end": 8.1, "speaker": "B", "text": "Marketing needs $50K approved."}
  ],
  "action_items": ["Finalize Q2 budget — deadline: Friday", "Approve $50K marketing budget"],
  "duration_seconds": 312,
  "language": "en"
}
```

## Use Cases

- Board meeting minutes automation
- Customer support call analysis and QA scoring
- Podcast transcript generation for SEO

## Access

```bash
# Service catalog
curl https://x402.ntriq.co.kr/services
```

Available on [Apify Store](https://apify.com/ntriqpro/audio-intelligence-mcp) · [x402 micropayments](https://x402.ntriq.co.kr)
