---
name: unboxing-video-maker
displayName: "Unboxing Video Maker — AI Product Reveal Content"
description: >
  Create exciting unboxing and first impressions videos with AI-powered product reveal content.
version: 1.1.1
author: nemovideo
tags: [video, ai, nemovideo, ecommerce]
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
metadata:
  requires:
    env: []
    configPaths:
      - "~/.config/nemovideo/"
  primaryEnv: NEMO_TOKEN
---

# Unboxing Video Maker — AI Product Reveal Content

## Overview

Create compelling unboxing video maker content using NemoVideo's AI-powered platform. Produce engaging ecommerce and consumer videos that drive purchase decisions and build brand trust.

## Examples

### Example 1: Product Feature
**Input:** "Create a unboxing feature video"
**Output:** Clear, engaging video highlighting key product features and benefits

### Example 2: Comparison
**Input:** "Make a unboxing vs competitor video"
**Output:** Objective side-by-side comparison with clear winner recommendations

### Example 3: Social Short
**Input:** "Create a 30-second unboxing reel"
**Output:** High-impact product video optimized for social commerce

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| product | string | yes | Product name, category, or comparison subjects |
| angle | string | no | Review angle (features, value, quality, comparison) |
| duration | number | no | Target duration in seconds (default: 180) |
| audience | string | no | Target audience (buyers, enthusiasts, general) |

## Workflow

1. Describe your product and review focus
2. NemoVideo AI creates persuasive script and storyboard
3. Professional product visuals and demos are generated
4. Clear, credible narration and music are added
5. Export for YouTube, social, or ecommerce platforms

## API Reference

```bash
curl -X POST https://api.nemovideo.ai/v1/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a unboxing video maker", "duration": 180}'
```

## Tips

1. Lead with the most compelling feature or benefit
2. Use close-up product shots for texture and detail
3. Include real usage demonstrations, not just beauty shots
4. Be honest about limitations to build viewer trust
5. Add clear purchase links and pricing information

## Output Formats

- MP4 (H.264) — YouTube and ecommerce platform ready
- WebM — Web streaming optimized
- MOV — High quality for brand use

## Related Skills

- advertisement-video-maker
- commercial-video-maker
- tiktok-video-maker
