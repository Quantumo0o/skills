---
name: gif-cog
description: "Create animated GIFs from text or images. Reaction GIFs, product loops, cinemagraphs, social media animations. Seamless looping, platform-optimized sizes. Use for GIFs, short animations, or looping visuals. Outputs: GIF, MP4. Powered by CellCog."
metadata:
  openclaw:
    emoji: "🎞️"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---

# GIF Cog - From Idea to Perfect Loop

CellCog creates GIFs end-to-end — not a video-to-GIF converter, but a full creation pipeline from text or image to optimized, looping GIF.

---

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

**Read the cellcog skill first** for SDK setup. This skill shows you what's possible.

**OpenClaw agents (fire-and-forget — recommended for long tasks):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",  # OpenClaw only
    task_label="my-task",
    chat_mode="agent",  # See cellcog skill for all modes
)
```

**All other agents (blocks until done):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
```

See the **cellcog** mothership skill for complete SDK API reference — delivery modes, timeouts, file handling, and more.

---

## What CellCog Has Internally

CellCog handles the full GIF creation pipeline using its internal models and tools:

1. **Image Generation Models** — Creates the starting frame (and optionally end frame) from text descriptions or enhances reference images. Supports photorealistic, cartoon, pixel art, and other styles.
2. **AI Video Animation Models** — Animates the frame(s) into a 4-12 second video with motion, camera movement, and physics. Supports seamless loops by using the same image as first and last frame.
3. **ffmpeg Processing** — Converts animated video to optimized GIF with intelligent palette generation, frame rate control, and file size optimization.

The agent orchestrates: **generate visual → animate → optimize to GIF**. Both the GIF and the higher-quality MP4 source are delivered.

---

## What You Can Create

- Reaction GIFs (custom expressions, emotions, memes)
- Product & e-commerce GIFs (360° rotations, feature highlights, before/after)
- Cinemagraphs (still photo with subtle motion — steam, rain, flickering light)
- Social media animations (announcements, seasonal, branded)
- Animated art & illustrations (pixel art, isometric, abstract loops)
- UI/UX demo GIFs (micro-interactions, loading animations)

---

## Output Specifications

| Feature | Details |
|---------|---------|
| **Duration** | 1-6 seconds (shorter is better for GIFs) |
| **Loop Types** | Seamless, boomerang (ping-pong), one-shot |
| **Aspect Ratios** | 1:1, 16:9, 9:16, 4:3, custom |
| **Frame Rate** | 10-20 FPS (optimized per use case) |
| **Color Depth** | Up to 256 colors (intelligent palette) |
| **Output** | GIF (primary) + MP4 source (bonus) |

### Platform Size Limits

| Platform | Max Size | Recommended Width |
|----------|----------|-------------------|
| Discord | 8 MB | 400px |
| Twitter/X | 15 MB | 480px |
| Slack | 20 MB | 400px |
| WhatsApp | 6 MB | 400px |
| Email | 1 MB | 300px |

---

## Chat Mode

**Use `chat_mode="agent"`** for all GIF work.
