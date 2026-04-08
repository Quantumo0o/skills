# Murf Falcon TTS

High-quality text-to-speech for OpenClaw via [Murf AI](https://murf.ai).

## What it does

Adds the **murf** speech provider to your OpenClaw workspace. Every outbound message (or inbound, depending on your `auto` setting) is synthesized into natural-sounding audio using Murf's Falcon or GEN2 models.

- **FALCON** -- low latency (~130 ms), conversational quality, 24 kHz default
- **GEN2** -- studio quality, higher fidelity, 44.1 kHz default
- **150+ voices** across 35 languages
- **12 regional endpoints** for low-latency routing

## Setup

1. Get a Murf API key from the [Murf API dashboard](https://murf.ai/api/dashboard).
2. Set `MURF_API_KEY` in your environment.
3. Add to your OpenClaw config:

```json
{
  "messages": {
    "tts": {
      "provider": "murf",
      "providers": {
        "murf": {
          "voiceId": "en-US-natalie"
        }
      }
    }
  }
}
```

4. Restart the gateway: `openclaw gateway restart`
5. Verify: `/tts status`

## Configuration

| Field | Default | Description |
|-------|---------|-------------|
| apiKey | `MURF_API_KEY` env | Murf API key |
| voiceId | `en-US-natalie` | Voice identifier |
| model | `FALCON` | `FALCON` or `GEN2` |
| locale | `en-US` | BCP-47 locale |
| style | `Conversation` | Speaking style |
| rate | `0` | Speech rate (-50 to 50) |
| pitch | `0` | Pitch (-50 to 50) |
| region | `global` | API region |
| format | `MP3` | `MP3`, `WAV`, `OGG`, `FLAC` |
| sampleRate | `24000` / `44100` | Sample rate in Hz |

## In-message directives

```
@tts voiceid=en-US-jackson model=GEN2 style=Newscast rate=10
```

## Regions

`au`, `ca`, `eu-central`, `global`, `in`, `jp`, `kr`, `me`, `sa-east`, `uk`, `us-east`, `us-west`

## Links

- [Murf AI](https://murf.ai)
- [Murf API docs](https://murf.ai/api/docs)
- [npm package](https://www.npmjs.com/package/openclaw-murf-tts)
- [GitHub](https://github.com/sanchitasunil/openclaw-murf-tts)
