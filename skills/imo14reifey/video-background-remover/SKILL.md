---
name: video-background-remover
version: "1.0.4"
displayName: "Video Background Remover — Remove and Replace Video Background with AI"
description: >
  Video Background Remover — Remove and Replace Video Background with AI.
  Green screen effects without the green screen. Video Background Remover uses AI segmentation to detect and isolate subjects in your footage — people, products, objects — and removes or replaces the background automatically. Upload your video and describe what you want: 'remove the background completely,' 'replace with a solid white background for product use,' or 'blur the background to keep focus on the subject.' The AI handles edge detection, motion tracking across frames, and clean compositing. Works for talking head videos, product demonstrations, remote work backgrounds, social media content, and any footage where background control matters. Combine with color grading and titles in the same session. Transparency export available for compositing workflows. Export as MP4. Supports mp4, mov, avi, webm, mkv.
  
  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM. Free trial available.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
license: MIT-0
---

# Video Background Remover — Remove and Replace Video Background with AI

Remove and replace video backgrounds with AI. Green screen effects without green screens.

## Quick Start
Ask the agent to remove or replace the background in your video.

## What You Can Do
- Remove backgrounds from videos automatically
- Replace backgrounds with solid colors or images
- Create transparent backgrounds for compositing
- Blur backgrounds while keeping subjects sharp
- Apply green screen effects without green screens

## API
Uses NemoVideo API (mega-api-prod.nemovideo.ai) for all video processing.
