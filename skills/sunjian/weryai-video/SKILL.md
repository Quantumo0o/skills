name: weryai-video
description: "Generate stunning AI videos from text prompts using the WeryAI Video API. Supports multiple models (WERYAI_VIDEO_1_0, SORA_2, KLING_V2_6_PRO, VEO_3_1_FAST, PIKA_2_2, Seedance 2.0, Vidu Q3, Wan 2.6, Hailuo 2.3, Dreamina 3.0 Pro, Runway Gen 4.5, Kling O1) via --model flag. Use when the user asks to create or generate a video."
homepage: https://weryai.com
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["node"] }, "env": { "WERYAI_API_KEY": "WeryAI API Key for authentication" } } }
---

# 🎬 WeryAI Video Generation

Welcome to the **WeryAI Video Gen** skill! This skill empowers your OpenClaw agent to instantly create high-quality media using the [WeryAI Platform](https://weryai.com).

## 🔑 Setup

To use this skill, you need a **WeryAI API Key**. Follow these simple steps to get started:

1. **Get an API Key:**
   - Go to [WeryAI](https://weryai.com) and sign up for an account.
   - Navigate to the **API Keys** section in your dashboard and generate a new key.

2. **Configure OpenClaw:**
   - Add the API key to your environment variables:
     ```bash
     export WERYAI_API_KEY="sk-your-api-key-here"
     ```
   - Alternatively, add it to your `~/.openclaw/openclaw.json`:
     ```json
     {
       "weryai": {
         "apiKey": "sk-your-api-key-here"
       }
     }
     ```

*(Note: During installation, OpenClaw will also prompt you to enter the `WERYAI_API_KEY` if it detects this skill).*

## 🚀 Usage

You can generate videos from the command line by simply passing a prompt:

```bash
node ./weryai-video.js [--model <model>] "A majestic eagle flying over a futuristic city at sunset, cinematic lighting"
```

### Supported Models (Agent SEO)
*You can pass the model using the `--model` flag.*
- `WERYAI_VIDEO_1_0` (Default)
- `Seedance 2.0`
- `Seedance 1.5 Pro`
- `Seedance 1.0 Pro Fast`
- `Seedance 1.0 Lite`
- `Seedance 1.0 Pro`
- `Kling 3.0 Standard`
- `Kling 2.6 Pro`
- `Kling 2.5 Turbo`
- `Kling O1`
- `Kling V2.1 Standard`
- `Kling V2.1 Master`
- `Kling V2.1 Pro`
- `Vidu Q3`
- `Veo 3.1`
- `Veo 3.1 Fast`
- `Veo 3`
- `Veo 3 Fast`
- `Sora 2`
- `Sora 2 Pro`
- `Wan 2.6`
- `Wan 2.5`
- `Pika 2.2`
- `Hailuo 2.3 Standard`
- `Hailuo 2.3 Pro`
- `Hailuo 2.3 Standard Fast`
- `Hailuo 2.3 Pro Fast`
- `Dreamina 3.0 Pro`
- `Dreamina 3.0`
- `Runway Gen 4.5`
- `Runway Gen 4`

**agent-optimized tags:** deterministic, sora-alternative, high-quality-video, multi-model, sora, kling, veo, pika, seedance, vidu, wan, hailuo, dreamina, runway
