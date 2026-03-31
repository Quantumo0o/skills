---
name: ai-video-color-grading
version: "1.0.0"
displayName: "AI Video Color Grading — Professional Color Correction and Grading with AI"
description: >
  Professional color correction and color grading for any video with AI — transform flat raw footage into cinematic, branded, or mood-specific visuals. NemoVideo analyzes your footage and applies: exposure correction, white balance adjustment, contrast optimization, color temperature tuning, saturation control, highlight and shadow recovery, skin tone preservation, and cinematic look presets. Match the look of any film, maintain consistency across multi-camera shoots, batch-grade entire video libraries, and create signature visual styles. AI color grading, video color correction, cinematic color grade, color grading tool, video color filter, professional color correction AI, LUT generator.
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Video Color Grading — Make Every Frame Look Like It Was Shot by a Cinematographer

Color grading is the invisible art that separates amateur video from professional production. The same footage — identical composition, identical lighting, identical subject — looks completely different after color grading. Warm tones communicate comfort, nostalgia, and trust. Cool tones communicate technology, precision, and modernity. Desaturated tones communicate drama, seriousness, and weight. High-contrast grading communicates energy and boldness. The color grade is the emotional filter through which the viewer experiences every frame. Professional colorists charge $100-500 per hour. A 10-minute video takes 2-4 hours to grade manually in DaVinci Resolve. A multi-camera project requires matching colors across sources — adding hours of node-by-node adjustment. Consistency across a content library (every video matching the same look) requires saving and maintaining custom LUTs, adjusting for different lighting conditions, and reviewing every export. NemoVideo grades video through natural language. Describe the look you want — "warm cinematic like a Wes Anderson film" or "clean professional corporate" or "moody blue-toned thriller" — and the AI applies: technical correction (exposure, white balance, noise reduction) followed by creative grading (color temperature, contrast curve, saturation mapping, highlight/shadow tinting, and skin tone protection). Professional color grading from a description.

## Use Cases

1. **YouTube Creator — Signature Look Across All Videos (any length)** — A creator shoots on different cameras, in different locations, with different lighting — every video looks slightly different. NemoVideo: establishes a signature grade ("warm-clean: slight warm tone, lifted shadows, gentle contrast, natural skin preservation"), applies it consistently to every video regardless of source camera or lighting conditions, and maintains the look across an entire channel library. Viewers develop subconscious brand recognition — the color grade becomes part of the creator's visual identity.

2. **Multi-Camera Match — Wedding/Event Videography (multiple sources)** — A wedding was shot on 3 cameras: a Sony (neutral color science), a Canon (warm skin tones), and a GoPro (action cam with aggressive processing). Cut together without grading, the video jumps between three different color worlds at every camera switch. NemoVideo: analyzes the color characteristics of each source, creates a unified grade that brings all three cameras into the same visual space (matched white balance, matched exposure, matched contrast), preserves the best qualities of each (Canon's skin tones applied to all three), and exports with invisible camera transitions. Three cameras look like one.

3. **Cinematic Grade — Film Look for Any Footage (any length)** — A filmmaker shoots on a consumer camera but wants a cinematic look. NemoVideo applies: lifted blacks (the signature "film" look — shadows never reach true black), subtle halation on highlights (the glow that film grain creates on bright areas), reduced saturation with specific color shifts (teal shadows, orange highlights — the most popular cinematic color combination), gentle film grain overlay (texture that adds organic feeling), and controlled contrast curve (mid-tones compressed for that "filmic" latitude). Phone footage or consumer camera footage with the visual character of high-end cinema cameras.

4. **Brand Consistency — Corporate Video Library (batch)** — A corporation has 50 training and marketing videos produced over 3 years by different teams. Some are warm, some cold, some overexposed, some dark. NemoVideo batch-grades the entire library: normalizes exposure and white balance across all 50 videos, applies the brand's visual standard (specific color temperature, contrast level, saturation range), ensures skin tones look healthy and consistent, and exports the entire graded library. Fifty videos that previously looked like they came from fifty different companies now look like one cohesive collection.

5. **Mood Transformation — Same Scene, Different Feeling (any length)** — A real estate video was shot on an overcast day. The listing looks gray and uninviting. NemoVideo: warms the color temperature (makes overcast feel like golden hour), lifts brightness (makes rooms feel airier and more spacious), enhances green in outdoor shots (makes landscaping look lush), brightens windows (makes natural light feel abundant), and applies a "warm inviting home" grade. The same listing that looked depressing in raw footage now looks like a dream home. Color grading does not change what was filmed — it changes how it feels.

## How It Works

### Step 1 — Upload Video
Any footage: phone, consumer camera, professional camera, screen recording, drone, action cam. NemoVideo handles any source quality.

### Step 2 — Describe the Look
Natural language: "warm and inviting like a coffee shop commercial" or "cold and dramatic like a thriller" or "clean corporate with brand blue tones." Or choose a preset: cinematic, warm-clean, cool-modern, vintage-film, vibrant-social.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-color-grading",
    "prompt": "Apply cinematic color grading to a 10-minute short film. Style: warm cinematic with teal shadows and orange highlights. Lifted blacks (no true black — darkest value around 10%%). Subtle film grain (fine, not distracting). Slightly desaturated overall but with enhanced skin warmth. Highlight roll-off should feel smooth and organic (not digital clipping). Maintain consistent grade across all scenes (indoor and outdoor). Preserve natural skin tones even in stylized scenes.",
    "grade_style": "cinematic-teal-orange",
    "corrections": {
      "exposure": "auto-normalize",
      "white_balance": "auto-correct",
      "noise_reduction": "subtle"
    },
    "creative": {
      "shadows": "teal-shifted",
      "highlights": "warm-orange",
      "blacks": "lifted-10pct",
      "saturation": "reduced-15pct",
      "skin_tones": "protected-warm",
      "grain": "fine-subtle",
      "highlight_rolloff": "smooth-organic"
    },
    "consistency": "match-across-scenes",
    "format": "16:9"
  }'
```

### Step 4 — Review and Refine
Preview the graded footage. Compare before/after. Adjust: "make the shadows more blue," "increase the warmth slightly," "reduce the grain." Each refinement applies instantly.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the visual look you want |
| `grade_style` | string | | "cinematic-teal-orange", "warm-clean", "cool-modern", "vintage-film", "vibrant-social", "moody-dark", "corporate-clean" |
| `corrections` | object | | {exposure, white_balance, noise_reduction} — technical fixes |
| `creative` | object | | {shadows, highlights, blacks, saturation, skin_tones, grain, contrast} |
| `consistency` | string | | "match-across-scenes", "match-to-reference", "per-scene-auto" |
| `reference` | string | | Reference image or film name to match |
| `skin_tones` | string | | "protected" (default), "stylized", "warm", "cool" |
| `batch` | boolean | | Grade multiple videos with same look |
| `export_lut` | boolean | | Export the grade as a reusable LUT file |
| `format` | string | | "16:9", "9:16", "1:1" |

## Output Example

```json
{
  "job_id": "avcg-20260328-001",
  "status": "completed",
  "source_duration": "10:22",
  "grade_applied": "cinematic-teal-orange",
  "corrections": {
    "exposure_adjusted": "3 scenes normalized",
    "white_balance_corrected": "2 scenes (indoor tungsten → neutral)",
    "noise_reduction": "applied to 1 low-light scene"
  },
  "creative_grade": {
    "shadows": "teal-shifted (#1A3A4A)",
    "highlights": "warm-orange (#FFB088)",
    "blacks_lifted": "10%%",
    "saturation": "-15%% overall, skin +5%%",
    "grain": "fine (opacity 8%%)"
  },
  "consistency": "matched across 12 scenes",
  "output": {
    "file": "short-film-graded.mp4",
    "resolution": "1920x1080",
    "before_after_preview": "comparison-strip.png"
  }
}
```

## Tips

1. **Correction before creativity** — Always fix technical issues first (exposure, white balance, noise) before applying creative grading. A warm cinematic grade on underexposed footage with wrong white balance produces muddy results. Clean footage grades beautifully.
2. **Skin tone protection is non-negotiable** — Creative grading that makes skin look green, gray, or unnaturally saturated immediately looks amateur. Always enable skin tone protection — it allows aggressive grading on the environment while keeping faces natural.
3. **Lifted blacks are the simplest path to "cinematic"** — True black in video looks digital and harsh. Lifting the black point to 5-10% (so the darkest value is dark gray, not black) immediately creates the film-like latitude that audiences associate with cinema. One adjustment, dramatic effect.
4. **Consistency across a channel builds brand recognition** — When every video has the same color grade, viewers recognize your content by its visual feel before reading the title. The grade becomes your visual signature — as distinctive as a logo.
5. **The same footage can tell different stories through grading** — Warm grade: happy, inviting, trustworthy. Cool grade: professional, technological, precise. Desaturated: dramatic, serious, documentary. The color grade is not decoration — it is a narrative tool that shapes the viewer's emotional response to every frame.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube / cinema / website |
| MP4 9:16 | 1080x1920 | Social media |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |
| LUT (.cube) | — | Reusable grade for editing software |
| PNG | — | Before/after comparison strip |

## Related Skills

- [ai-video-splitter](/skills/ai-video-splitter) — Video splitting
- [ai-video-trimmer](/skills/ai-video-trimmer) — Video trimming
- [video-editor-ai](/skills/video-editor-ai) — AI video editing
