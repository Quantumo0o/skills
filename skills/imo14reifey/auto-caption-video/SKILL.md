---
name: auto-caption-video
version: 5.0.2
displayName: "Auto Caption Video — Automatically Add Captions and Subtitles to Any Video with AI"
description: >
  It is Tuesday at 4 PM. Your social media manager has eight client videos due tomorrow morning — a restaurant walkthrough shot on an iPhone, a SaaS demo recorded on Zoom, a gym trainer talking over loud music, a real estate agent whispering through an open house, and four talking-head testimonials. Each needs captions burned in before posting. Manually captioning one takes forty-five minutes. Eight means an all-nighter. Auto Caption Video processes the entire batch while your team goes home. The restaurant audio separates speech from kitchen clatter. The Zoom recording extracts the presenter while suppressing the "you're on mute" interruptions. The gym video isolates the trainer's voice from the bass-heavy playlist. Each finished clip arrives with captions styled to the client's brand guidelines and positioned for the target platform. Eight videos. Zero overtime.
metadata: {"openclaw": {"emoji": "💬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
apiDomain: https://mega-api-prod.nemovideo.ai
---

# Auto Caption Video — One Click. Every Word. Perfectly Timed.

Captions have become the default viewing mode for video. The shift happened quietly but completely: 85% of Facebook video is watched muted, TikTok and Instagram Reels autoplay silently, LinkedIn video starts without sound, and even YouTube viewers increasingly enable captions as a companion to audio rather than a replacement. Captions are no longer an accessibility accommodation — they are a primary content consumption channel. For creators and businesses, the implication is binary: captioned video gets watched; uncaptioned video gets scrolled past. YouTube's internal data confirms 7-10% higher watch time for captioned videos. TikTok's algorithm explicitly favors content with text elements (captions count). Instagram Reels with animated captions show 15-25% higher completion rates in A/B tests. The math is simple: captions increase every metric that matters. Platform auto-captions (YouTube auto, TikTok auto, Instagram auto) exist but consistently disappoint: 80-90% accuracy (errors every few sentences that undermine professionalism), poor timing (captions appear too early or linger too late, breaking the visual-audio sync), zero styling (small white text in a fixed position, with no brand customization), and no speaker differentiation (multiple speakers get identical treatment, creating confusion). NemoVideo auto-captioning starts at 98%+ accuracy and adds everything platform auto-captions lack: word-level timing precision, animated visual styles, brand-customizable fonts and colors, multi-speaker differentiation, platform-safe positioning, and multi-language translation.

## Use Cases

1. **TikTok/Reels Animated Captions — The Engagement Multiplier (15-90s)** — Short-form content needs the animated caption style that maximizes watch time: large bold text, each word highlighted or popping as it is spoken, bright colors with high-contrast outlines, positioned in the center-upper third of the vertical frame. NemoVideo: transcribes with word-level timing (each word anchored to its exact spoken moment — not sentence-level batches), applies the TikTok caption aesthetic (bold sans-serif, word-by-word highlight animation in the creator's brand color, black outline for readability against any background), positions within the platform safe zone (above TikTok's bottom 15% UI overlay, below Instagram's top 10% status bar), and renders directly into the video. The caption style that creates dual-channel engagement — reading + listening simultaneously — proven to hold attention 15-25% longer than uncaptioned content.

2. **YouTube Professional Captions — SEO and Accessibility (any length)** — A YouTube creator needs accurate captions for every video: for accessibility compliance, for non-native English-speaking viewers, for the watch-time boost, and for SEO (YouTube indexes caption text for search discovery). NemoVideo: transcribes the entire video with 98%+ accuracy using context-aware recognition (handles technical terminology, brand names, and proper nouns that generic auto-caption consistently misspells), identifies multiple speakers (assigning labels or colors), generates precise timestamps for YouTube's caption system, handles filler word removal (optional: cleaning "um" and "uh" from transcription while maintaining natural timing), and exports in standard caption formats (SRT, VTT) for YouTube upload alongside embedded-caption versions for other platforms. Professional captions that serve accessibility, discoverability, and watch time simultaneously.

3. **Multi-Language Translation — One Video, Global Reach (any length)** — A creator, brand, or educator wants to reach audiences beyond their native language. NemoVideo: transcribes the original language, translates to selected target languages (50+ supported) using context-aware AI translation (not word-by-word dictionary swaps — natural, contextually appropriate translations), adjusts timing per language (German averages 30% more characters than English for the same meaning; Japanese averages fewer — timing must expand or contract accordingly), handles right-to-left languages with proper text rendering (Arabic, Hebrew, Persian), and exports separate caption versions for each language. One video becomes accessible to billions of additional viewers with no re-recording required.

4. **Podcast/Long-Form Captions — Extended Conversation (30-120 min)** — A video podcast, long-form interview, or webinar needs captions optimized for extended viewing. NemoVideo: transcribes hours of conversational dialogue accurately (handling crosstalk, interruptions, casual speech patterns, and technical jargon), differentiates speakers with persistent color coding (Speaker A: white, Speaker B: yellow — maintained throughout the entire recording), positions captions to avoid covering speaker faces (dynamically adjusting position based on face detection), uses reading-optimized display (maximum 2 lines, comfortable reading speed, sentence-aware line breaks rather than arbitrary character-count breaks), and maintains timing accuracy across the full duration without drift. Long-form captions that enhance conversation rather than distracting from it.

5. **Batch Auto-Captioning — Entire Content Library (multiple videos)** — A creator, brand, or organization has 50-200 existing videos without captions that need retrofitting. NemoVideo: batch-processes the entire library with consistent caption styling (same font, same colors, same animation, same positioning across all videos), auto-detects the language of each video (handling a multilingual library without manual language tagging), applies the organization's branded caption style to all videos, and exports both embedded-caption versions and standalone caption files. An entire content library becomes captioned in one operation rather than video-by-video manual work.

## How It Works

### Step 1 — Upload Video
Any video with speech. NemoVideo auto-detects language and number of speakers.

### Step 2 — Choose Caption Style
TikTok animated, YouTube closed caption, Netflix minimal, karaoke highlight, broadcast professional, or custom brand styling.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "auto-caption-video",
    "prompt": "Auto-caption a 3-minute motivational speaking clip with TikTok-style animated captions. Word-by-word highlight in bright cyan (#00E5FF) on bold white text with heavy black outline. Font: Impact-style bold sans-serif, large enough to read on mobile. Position: center-upper-third, within TikTok safe zone. Also generate: Spanish version (same style), Portuguese version (same style), clean YouTube SRT file in English. Export all embedded versions at 9:16 1080x1920.",
    "transcribe": true,
    "style": "tiktok-animated",
    "highlight_color": "#00E5FF",
    "font": "impact-bold-sans",
    "outline": "heavy-black",
    "position": "center-upper-third",
    "safe_zone": "tiktok",
    "languages": ["en", "es", "pt"],
    "caption_files": ["srt-en"],
    "format": "9:16",
    "resolution": "1080x1920"
  }'
```

### Step 4 — Review Accuracy
Play the captioned video. Check: every word is correctly transcribed (especially proper nouns and technical terms), timing matches speech precisely (no early or late captions), captions are readable at mobile viewing size, and translations read naturally (not machine-translation stiffness). Edit any errors and re-render.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Caption requirements |
| `style` | string | | "tiktok-animated", "youtube-cc", "netflix-minimal", "karaoke", "broadcast", "custom" |
| `highlight_color` | string | | Word highlight animation color |
| `font` | string | | Font family or preset |
| `outline` | string | | Outline style |
| `position` | string | | "bottom", "center-upper-third", "center", "custom" |
| `safe_zone` | string | | "tiktok", "instagram", "youtube", "none" |
| `languages` | array | | Translation targets ["es", "pt", "ja", ...] |
| `speakers` | object | | {differentiate: true, colors: {}} |
| `filler_removal` | boolean | | Remove "um", "uh" from transcript |
| `caption_files` | array | | ["srt", "vtt", "ttml"] standalone files |
| `format` | string | | "16:9", "9:16", "1:1" |
| `batch` | boolean | | Process multiple videos |

## Output Example

```json
{
  "job_id": "acap-20260329-001",
  "status": "completed",
  "transcription": {
    "language": "en",
    "confidence": 0.987,
    "words": 412,
    "speakers": 1,
    "filler_removed": 0
  },
  "translations": ["es", "pt"],
  "style": "tiktok-animated",
  "outputs": {
    "en_embedded": {"file": "motivational-caption-en-9x16.mp4"},
    "es_embedded": {"file": "motivational-caption-es-9x16.mp4"},
    "pt_embedded": {"file": "motivational-caption-pt-9x16.mp4"},
    "srt_en": {"file": "motivational-en.srt"}
  }
}
```

## Tips

1. **Word-level timing is what separates professional from amateur captions** — Sentence-level captions (entire sentence appears at once) feel disconnected from speech. Word-level timing (each word appears or highlights as spoken) creates a synchronized reading experience that holds attention and improves comprehension. Always use word-level sync.
2. **Animated captions on short-form content increase watch time 15-25%** — This is not aesthetic preference — it is engagement data. The word-by-word animation creates an active reading task that engages the viewer's language processing system alongside the auditory system. Dual-channel engagement reduces scroll-away behavior measurably.
3. **Platform safe zones are different and critical** — TikTok: bottom 15% covered by UI. Instagram Reels: bottom 20% and top 10%. YouTube: bottom 10% (progress bar). Captions placed in these zones are partially or fully hidden. Always specify the target platform's safe zone for correct positioning.
4. **Multi-language captions multiply audience at near-zero cost** — Translating and re-timing captions for 5 additional languages costs a fraction of producing 5 separate language versions of the video. Each language version opens the content to hundreds of millions of additional potential viewers.
5. **98% accuracy vs. 85% accuracy is the difference between professional and embarrassing** — At 85% accuracy (typical platform auto-caption), a 3-minute video with 400 words contains 60 errors — roughly one error every 3 seconds. At 98% accuracy, the same video has 8 errors. The perceived quality difference is enormous: 85% feels broken; 98% feels polished with occasional minor corrections needed.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube / website |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Shorts |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |
| SRT / VTT | — | Platform caption upload |

## Related Skills

- [ai-video-subtitle-editor](/skills/ai-video-subtitle-editor) — Edit and style captions
- [ai-video-caption-generator](/skills/ai-video-caption-generator) — Full caption workflow
- [ai-video-text-overlay](/skills/ai-video-text-overlay) — Custom text graphics
- [ai-video-highlight-maker](/skills/ai-video-highlight-maker) — Extract captioned highlights
