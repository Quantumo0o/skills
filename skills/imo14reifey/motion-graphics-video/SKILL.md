---
name: motion-graphics-video
displayName: "Motion Graphics Video Maker — AI Animated Design"
description: >
  Create stunning motion graphics and animated design videos with AI-powered visual content.
version: 1.0.1
author: nemovideo
tags: [video, ai, nemovideo, animation]
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
metadata:
  requires:
    env: []
    configPaths:
      - "~/.config/nemovideo/"
  primaryEnv: NEMO_TOKEN
---

# Motion Graphics Video Maker — AI Animated Design

## Overview

Create stunning motion graphics video content using NemoVideo's AI-powered platform. Produce visually spectacular animated and motion design videos that captivate audiences with technical artistry.

## Examples

### Example 1: Brand Animation
**Input:** "Create a motion graphics brand animation"
**Output:** Professional branded animation with smooth motion and visual polish

### Example 2: Explainer
**Input:** "Make a motion graphics explainer video"
**Output:** Engaging animated explainer using dynamic visuals to communicate concepts

### Example 3: Social Short
**Input:** "Create a 15-second motion graphics loop"
**Output:** Eye-catching animated loop perfect for social media and advertising

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| concept | string | yes | Animation concept, message, or visual idea |
| style | string | no | Style (minimal, bold, playful, corporate, cinematic) |
| duration | number | no | Target duration in seconds (default: 30) |
| color_scheme | string | no | Color palette preference |

## Workflow

1. Describe your animation concept and visual direction
2. NemoVideo AI creates dynamic script and storyboard
3. Beautiful animations and motion graphics are generated
4. Synchronized audio and sound design are added
5. Export in optimal format for your platform

## API Reference

```bash
curl -X POST https://api.nemovideo.ai/v1/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a motion graphics video", "duration": 30}'
```

## Tips

1. Keep animations purposeful — motion should guide attention
2. Use easing curves for natural, professional-feeling motion
3. Maintain consistent visual language throughout
4. Design for sound-off viewing with clear visual storytelling
5. Export at highest quality for best scaling flexibility

## Output Formats

- MP4 (H.264) — All platforms ready
- WebM — Web streaming optimized
- MOV — High quality for post-production

## Related Skills

- explainer-animation-video
- whiteboard-video-maker
- digital-art-video
