# openclaw-murf-tts

OpenClaw speech-provider plugin that calls Murf's streaming TTS endpoint `/v1/speech/stream` to synthesize speech in OpenClaw workspaces. [Murf AI](https://murf.ai) provides AI voice generation for applications, media, and assistants. Configure the **FALCON** model for low latency (~130 ms) or **GEN2** for higher-fidelity output instead of running your own TTS stack.

## Install

ClawHub is the preferred path: the OpenClaw CLI resolves the package from the registry first, then falls back to npm.

```bash
openclaw plugins install @sanchitasunil/openclaw-murf-tts
```

```bash
npm install @sanchitasunil/openclaw-murf-tts
```

`openclaw` is a peer dependency; your gateway or workspace already supplies it.

## Quick start

1. Create a Murf API key in the [Murf API dashboard](https://murf.ai/api/dashboard) (see also [Generating API key](https://help.murf.ai/generating-api-key)).
2. Set `MURF_API_KEY` in the environment your OpenClaw gateway runs under (or put `apiKey` in config; see below).
3. Add a minimal `messages.tts` block and enable the plugin. Example `openclaw.json` (JSON5 is also supported):

```json
{
  "messages": {
    "tts": {
      "provider": "murf",
      "providers": {
        "murf": {}
      }
    }
  },
  "plugins": {
    "enabled": true,
    "entries": {
      "murf": { "enabled": true }
    }
  }
}
```

With only `{}` under `murf`, the provider uses defaults and reads the key from `MURF_API_KEY`.

4. Restart the gateway: `openclaw gateway restart`.
5. Verify: `/tts status`.

## Configuration reference

Provider settings live under `messages.tts.providers.murf`. You may also use a flat `murf` object at the top level of the config file; both normalize to the same provider block.

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| **apiKey** | string | *(none)* | Murf API key. **Required** for synthesis unless `MURF_API_KEY` is set in the environment (same value). Never commit real keys. |
| voiceId | string | `en-US-natalie` | Murf voice identifier. |
| model | string | `FALCON` | `FALCON` (low latency) or `GEN2` (studio quality). |
| locale | string | `en-US` | BCP-47 locale (e.g. `en-US`). |
| style | string | `Conversation` | Speaking style (e.g. `Conversation`, `Newscast`). |
| rate | number | `0` | Speech rate from `-50` to `50` (`0` = normal). |
| pitch | number | `0` | Pitch from `-50` to `50` (`0` = normal). |
| region | string | `global` | Regional API host (e.g. `global`, `us-east`, `eu-central`). |
| format | string | `MP3` | Output container: `MP3`, `WAV`, `OGG`, or `FLAC`. Voice-note targets override this per model (FALCON → MP3, GEN2 → OGG). |
| sampleRate | number | `24000` (FALCON), `44100` (GEN2) | Sample rate in Hz. Allowed values: `8000`, `16000`, `24000`, `44100`, `48000`. |

Talk mode can overlay `talk.providers.murf` (and related resolve hooks) on top of the base TTS config. In-message directive tokens can override `voiceId`, `model`, `style`, `rate`, `pitch`, `locale`, and `format` when your OpenClaw policy allows it.

## Voices

- In OpenClaw, list catalog voices with: `openclaw tts voices` (with the Murf provider selected and a valid key).
- Browse and pick IDs from Murf's [voice offering](https://murf.ai/api) / product UI if you prefer a visual catalog.

For programmatic use inside a checkout of this repo, `src/test-api.ts` re-exports `createListVoicesFn` from `src/list-voices.ts`: supply a Falcon client factory, then call the returned `listVoices` with `apiKey` and optional `providerConfig` (same fields as above). Keys resolve in order: request `apiKey`, then config `apiKey`, then `MURF_API_KEY`. The npm tarball's main entry is the OpenClaw plugin only.

## Channel-specific notes

### Discord voice

`channels.discord.voice.tts` can override `messages.tts` for Discord-only voice playback (provider, provider block, auto mode, etc.). Use it when you want Murf settings or another provider only in Discord voice channels without changing global TTS defaults.

### Telephony

For telephony targets, OpenClaw expects **LINEAR16** audio at **8000 Hz**. The host pipeline typically forces that format for PSTN-style channels regardless of your Murf `format` and `sampleRate` settings in `messages.tts.providers.murf`.

## Troubleshooting

| Symptom | What to try |
| ------- | ----------- |
| Plugin not loading | Run `openclaw plugins list`, confirm `@sanchitasunil/openclaw-murf-tts` is installed and the plugin entry is enabled; restart the gateway. |
| 401 Unauthorized | Check `MURF_API_KEY` for leading/trailing whitespace or a stale key; confirm the key is active in the [Murf API dashboard](https://murf.ai/api/dashboard). |
| Audio not playing in Telegram / WhatsApp | Voice-note style delivery depends on `voiceCompatible` and codec support; a **format** your channel cannot play will fail or silent-fail. Try `MP3` and align `sampleRate` with what the channel expects. |
| Rate limited | The client retries HTTP **429** and **5xx** with exponential backoff (three attempts). If issues persist, check quota and usage on the Murf side. |

## Development

```bash
git clone https://github.com/sanchitasunil/openclaw-murf-tts.git
cd openclaw-murf-tts
pnpm install
pnpm build
pnpm test
```

Live integration tests in `tests/live/murf.live.test.ts` call the real Murf API. They run only when **`MURF_LIVE_TEST=1`** and a non-empty **`MURF_API_KEY`** are both set; otherwise that file’s suite is skipped. Example:

```bash
MURF_LIVE_TEST=1 MURF_API_KEY=your_key pnpm exec vitest run tests/live/murf.live.test.ts
```

