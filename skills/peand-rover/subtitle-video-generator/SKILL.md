---
name: subtitle-video-generator
version: 1.2.2
displayName: "Subtitle Video Generator — Generate and Style Video Subtitles in Any Language with AI"
description: >
  Generate and style video subtitles in any language with AI — auto-transcribe speech to perfectly timed subtitles, translate across 50+ languages, apply trending visual styles from TikTok animated to Netflix broadcast, differentiate multiple speakers with color coding, position within platform-safe zones, and export with subtitles rendered into the video or as standalone subtitle files. NemoVideo delivers complete subtitle production: 98%+ transcription accuracy with context-aware speech recognition, word-level timing synchronization, animated subtitle styles, multi-speaker identification, WCAG accessibility compliance, and batch processing for entire video libraries. Subtitle video generator AI, generate subtitles for video, auto subtitle maker, video subtitle tool, AI subtitle creator, add subtitles to video, multilingual subtitle generator, subtitle styling tool, closed caption generator.
metadata: {"openclaw": {"emoji": "📝", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
apiDomain: https://mega-api-prod.nemovideo.ai
---

# Subtitle Video Generator — Every Language. Every Style. Every Platform. One Upload.

Subtitles have become the universal interface between video content and global audiences. They serve four distinct functions simultaneously: accessibility (making content usable for deaf and hard-of-hearing viewers), engagement (holding attention for the 85% watching muted on social media), reach (translating content to audiences in 50+ languages), and discoverability (providing text that search algorithms can index). Each function alone justifies subtitling every video. Together, they make subtitling the single highest-ROI post-production addition to any video content. The quality gap between auto-generated platform subtitles and professional subtitling is the space NemoVideo fills. Platform auto-captions deliver 80-85% accuracy — one error every 15-20 words, visible to viewers and damaging to credibility. Professional human subtitling achieves 99%+ accuracy at $3-8 per video minute with 24-48 hour turnaround. NemoVideo delivers 98%+ accuracy with word-level timing, full style customization, multi-language translation, speaker differentiation, and instant turnaround. The quality that previously required professional subtitling services, delivered at the speed and scale that modern content production demands.

## Use Cases

1. **Social Media Subtitles — Engagement-Optimized Styling (15-90s)** — Short-form content for TikTok, Instagram Reels, and YouTube Shorts needs the animated subtitle style that maximizes watch time. NemoVideo: transcribes with word-level timing accuracy, applies the platform-native animated style (large bold text, word-by-word highlight animation in the creator's brand color, high-contrast outline for readability), positions within the specific platform's safe zone (TikTok: above bottom 15%; Reels: above bottom 20%, below top 10%; Shorts: above bottom 10%), and exports with subtitles rendered directly into the video (essential for platforms where subtitle upload is limited or unreliable). The subtitle style proven to increase short-form completion rate by 15-25%.

2. **Corporate Multi-Language — Global Communications (any length)** — A corporation produces video content that needs to reach employees and customers across 15+ countries. NemoVideo: transcribes the source language, translates to all target languages using context-aware AI (understanding corporate terminology, product names, and industry jargon), adjusts subtitle timing per language (expanding for languages that require more words, contracting for languages that use fewer), handles bidirectional text for Arabic and Hebrew (proper RTL rendering with correct line breaking), applies consistent corporate subtitle styling across all languages (brand fonts, colors, positioning), and exports subtitle files compatible with the company's video hosting infrastructure (SRT for most platforms, VTT for web, TTML for broadcast). One video, global reach, consistent brand quality.

3. **Educational Subtitles — Learning-Optimized Display (any length)** — Educational content requires subtitles optimized for comprehension rather than entertainment: slower reading speed for complex material, technical term highlighting, and clear speaker identification for multi-person discussions. NemoVideo: adjusts reading speed based on content complexity (14 characters/second for dense technical content vs. 18 cps for conversational segments), optionally highlights technical vocabulary on first appearance (bold or different color for terms that may be unfamiliar), identifies speakers with persistent color differentiation (essential for panel discussions and multi-instructor courses), maintains sentence-aware line breaks (never splitting a phrase across lines in a way that disrupts comprehension), and generates WCAG 2.1 AA-compliant subtitles for institutional accessibility requirements. Subtitles that serve learning, not just consumption.

4. **Film and Documentary — Broadcast Standard Subtitling (any length)** — Independent filmmakers and documentary producers need subtitles meeting broadcast and festival technical specifications. NemoVideo: generates subtitles conforming to broadcast standards (2 lines maximum, 42 characters per line maximum, 1-second minimum display time, 15-17 characters per second reading speed), applies professional positioning (center-bottom, with vertical offset when on-screen text or graphics would be obscured), handles complex audio scenarios (overlapping dialogue, music with lyrics, background conversations, sound effects that need description for accessibility), creates both open subtitles (burned into video for festival screenings) and closed subtitles (as separate files for broadcast distribution), and exports in industry-standard formats (SRT, STL, EBU-TT, TTML, DFXP). Festival-submission-ready and broadcast-compliant subtitles.

5. **Batch Library Subtitling — Retrofit an Entire Catalog (multiple videos)** — A content library of 200+ videos has grown without consistent subtitling. Some have auto-generated captions, some have nothing, and none have translations. NemoVideo: batch-processes the entire library with consistent subtitle styling (same font, color, position, animation across all videos), auto-detects the spoken language per video (handling a multilingual library), transcribes or re-transcribes each video at 98%+ accuracy (replacing inaccurate existing auto-captions), generates translations for specified target languages across the entire library, and produces both embedded-subtitle video files and standalone subtitle files for each video. A subtitle-inconsistent library becomes a professionally subtitled catalog.

## How It Works

### Step 1 — Upload Video
Any video with speech in any language. Single video or batch upload. NemoVideo auto-detects language and speaker count.

### Step 2 — Configure Subtitle Output
Style (animated, broadcast, minimal, custom), languages (source + translation targets), positioning, speaker differentiation, and export formats.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "subtitle-video-generator",
    "prompt": "Generate professional subtitles for a 15-minute interview with two speakers. English source — translate to Spanish, French, and Mandarin. Style: clean broadcast (white text, semi-transparent dark background bar, 2 lines max). Speaker differentiation: interviewer in white, guest in light yellow. Word-level timing. Position: bottom-center, offset upward on frames where lower-third graphics appear. Export: embedded MP4 for each language at 16:9 + standalone SRT files for all 4 languages + one 9:16 English version with TikTok animated style for social clips.",
    "source_language": "en",
    "translations": ["es", "fr", "zh"],
    "style": {
      "preset": "broadcast-clean",
      "background": "semi-transparent-dark",
      "max_lines": 2,
      "timing": "word-level"
    },
    "speakers": {
      "differentiate": true,
      "interviewer": "#FFFFFF",
      "guest": "#FFFACD"
    },
    "position": {"base": "bottom-center", "avoid_lower_thirds": true},
    "exports": {
      "embedded_16x9": ["en", "es", "fr", "zh"],
      "srt_files": ["en", "es", "fr", "zh"],
      "social_9x16": {"language": "en", "style": "tiktok-animated"}
    }
  }'
```

### Step 4 — Review Accuracy and Timing
Play each language version. Verify: transcription accuracy (especially names, technical terms, numbers), timing synchronization, speaker identification correctness, translation naturalness, and line break logic. Edit and re-render any corrections.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Subtitle generation requirements |
| `source_language` | string | | Source audio language (auto-detect if omitted) |
| `translations` | array | | Target languages ["es", "fr", "zh", ...] |
| `style` | object | | {preset, font, color, background, max_lines, animation, timing} |
| `speakers` | object | | {differentiate, colors_per_role} |
| `position` | object | | {base, offset, avoid_graphics} |
| `reading_speed` | string | | "educational-slow", "standard", "fast" |
| `broadcast_compliance` | boolean | | Apply broadcast subtitle standards |
| `accessibility` | string | | "wcag-aa", "wcag-aaa" |
| `exports` | object | | {embedded, srt_files, vtt_files, social} |
| `batch` | boolean | | Process multiple videos |

## Output Example

```json
{
  "job_id": "subgen-20260329-001",
  "status": "completed",
  "source_language": "en",
  "confidence": 0.986,
  "speakers": 2,
  "word_count": 3240,
  "languages": ["en", "es", "fr", "zh"],
  "outputs": {
    "embedded": {
      "en": {"file": "interview-sub-en-16x9.mp4"},
      "es": {"file": "interview-sub-es-16x9.mp4"},
      "fr": {"file": "interview-sub-fr-16x9.mp4"},
      "zh": {"file": "interview-sub-zh-16x9.mp4"}
    },
    "srt_files": ["interview-en.srt", "interview-es.srt", "interview-fr.srt", "interview-zh.srt"],
    "social": {"file": "interview-tiktok-en-9x16.mp4", "style": "tiktok-animated"}
  }
}
```

## Tips

1. **98% accuracy is the professional credibility threshold** — At 85% (platform auto), viewers notice errors constantly and question content quality. At 98%, errors are rare enough that the subtitle feels professionally produced. The accuracy difference is the difference between undermining and reinforcing your credibility.
2. **Word-level timing creates synchronized reading that holds attention** — Sentence-level display (full sentence appears at once) disconnects reading from listening. Word-level timing (each word appears as spoken) synchronizes the two channels, creating engaged viewing that platform auto-captions cannot achieve.
3. **Speaker color coding is faster than speaker labels** — "John:" before each subtitle line wastes characters and reading time. White for John, yellow for Sarah communicates the same information through pre-attentive color processing — faster than reading a name label every time the speaker changes.
4. **Translation timing must expand and contract per language** — German averages 30% more characters than English. Japanese averages fewer. If subtitle display time does not adjust, German viewers cannot finish reading and Japanese viewers stare at completed subtitles. Per-language timing is essential for comfortable reading speed in every language.
5. **Batch subtitling eliminates the growing liability of uncaptioned content** — Every uncaptioned video is a missed accessibility obligation, a missed engagement opportunity, and a missed global reach opportunity. Batch processing converts an entire backlog in one operation, establishing the baseline for captioning all future content.

## Output Formats

| Format | Type | Use Case |
|--------|------|----------|
| MP4 (embedded) | Video | Social platforms, website, LMS |
| SRT | Subtitle file | YouTube, Vimeo, most platforms |
| VTT | Subtitle file | Web players, HTML5 video |
| TTML / DFXP | Subtitle file | Broadcast, streaming services |
| STL | Subtitle file | European broadcast |
| EBU-TT | Subtitle file | EBU broadcast standard |

## Related Skills

- [ai-subtitle-generator](/skills/ai-subtitle-generator) — Core subtitle generation
- [auto-caption-video](/skills/auto-caption-video) — Quick auto-captioning
- [ai-video-caption-generator](/skills/ai-video-caption-generator) — Full caption workflow
- [ai-video-text-overlay](/skills/ai-video-text-overlay) — Custom text overlays
