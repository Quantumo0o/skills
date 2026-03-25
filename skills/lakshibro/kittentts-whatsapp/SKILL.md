---
name: kittentts-whatsapp
description: WhatsApp voice notes via KittenTTS. Converts KittenTTS 24kHz WAV output to WhatsApp-compatible 16kHz OGG Opus using ffmpeg. Install dependencies first — see setup. Network: downloads ~80-400MB TTS model on first run from Hugging Face.
---

# KittenTTS WhatsApp Voice

Generates WhatsApp-compatible voice notes from text using KittenTTS + ffmpeg. Specifically solves the format mismatch that causes silent failures: KittenTTS outputs 24kHz WAV → converted to 16kHz OGG Opus via ffmpeg → sent as WhatsApp voice note.

> ⚠️ **Read before installing.** This skill installs system packages and downloads large ML models. See Setup below.

## System Dependencies

| Dependency | Install command | Size | Notes |
|------------|---------------|------|-------|
| `ffmpeg` | `apt-get install -y ffmpeg` | ~30MB | Available in most distro repos |
| `kittentts` | `pip3 install kittentts --break-system-packages` | pulls ~25-80MB from Hugging Face on first run | Python package |
| `libopus` | bundled with ffmpeg | — | OGG encoding support |
| `soundfile` | pulled by kittentts | — | Python package |

## Network Calls

- **First run**: downloads TTS model (~25-80MB) from `huggingface.co/KittenML` based on model size chosen
- **No API keys required** — fully offline capable after model download
- Set `HF_TOKEN` env var to avoid unauthenticated rate limits on model download

## Model Options

| Model | Parameters | Size | Hugging Face ID |
|-------|-----------|------|-----------------|
| nano (int8) | 15M | 25MB | `KittenML/kitten-tts-nano-0.8-int8` |
| nano | 15M | 56MB | `KittenML/kitten-tts-nano-0.8-fp32` |
| micro | 40M | 41MB | `KittenML/kitten-tts-micro-0.8` |
| mini | 80M | 80MB | `KittenML/kitten-tts-mini-0.8` |

Default: `kitten-tts-mini-0.8` (best quality). Change in `scripts/tts_walkie.sh`.

## Setup

Run these manually before the skill is used:

```bash
# 1. System package (requires root/privileged)
apt-get install -y ffmpeg

# 2. Python package
pip3 install kittentts --break-system-packages

# 3. Optional: set Hugging Face token to avoid rate limits
# echo 'export HF_TOKEN="hf_your_token_here"' >> ~/.bashrc
```

**Restart OpenClaw** after installing dependencies so the new packages are in PATH.

## Usage

### TTS only (no transcription)

```bash
bash scripts/tts_walkie.sh "Your message here" Bella
# Output: /tmp/walkie_reply.ogg (16kHz OGG Opus, WhatsApp-ready)
```

### Transcription only (optional — requires whisper)

```bash
# Install whisper (one-time, ~140MB-1.4GB depending on model)
pip3 install whisper --break-system-packages

bash scripts/transcribe.sh /path/to/audio.ogg [model]
# Model: tiny | base | small | medium | large (default: base)
```

## Voices

Available: **Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo**

Default: `Bella`

## Voice Speed

Adjust in `scripts/tts_walkie.sh`:
```bash
VOICE_SPEED=1.0  # increase to speed up, decrease to slow down
```

## Files

```
kittentts-whatsapp/
├── SKILL.md
└── scripts/
    ├── tts_walkie.sh      # TTS + ffmpeg conversion
    └── transcribe.sh       # whisper transcription (optional)
```

## ⚠️ Privileged Install Warning

The dependency install commands use `--break-system-packages` and `apt-get install -y`. These require root privileges and modify system packages. Review before running if you are on a managed system.

## Troubleshooting

**Audio sends but is silent or rejected by WhatsApp:**
→ Run `ffprobe -v quiet -print_format json -show_streams /tmp/walkie_reply.ogg`
→ Must show `codec_name: opus` and `sample_rate: 48000` (or 16000). If not, the ffmpeg chain failed.

**TTS generation is slow:**
→ Switch to a smaller model (nano instead of mini) in `scripts/tts_walkie.sh`.

**Hugging Face download rate limit:**
→ Set `HF_TOKEN` in your environment. Free accounts get lower rate limits.
