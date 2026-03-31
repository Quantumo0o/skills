---
name: video-bewerken
version: "1.1.0"
displayName: "Video Bewerken met AI — Dutch Video Editor — Bewerk Video's met Kunstmatige Intelligentie"
description: >
  Bewerk video's met kunstmatige intelligentie in het Nederlands — volledige videobewerking met Nederlandse ondertitels, ingesproken tekst met Vlaams of Nederlands accent, geanimeerde teksten, automatische montage, achtergrondmuziek, visuele effecten en export naar alle platforms. NemoVideo biedt complete videoproductie in het Nederlands: voeg automatische ondertitels toe met woord-voor-woord synchronisatie, genereer Nederlandse voice-over met keuze uit Standaardnederlands of Vlaams, maak geanimeerde teksten en titels, pas cinematische kleurcorrectie toe, en exporteer voor YouTube TikTok Instagram en alle sociale media. Video bewerken AI, video editor Nederlands, video bewerken online, ondertitels Nederlands, Nederlandse video maker, Dutch video editor, edit video Dutch, Netherlands video creator, Flemish video editor, video montage Nederlands.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Video Bewerken met AI — Professionele Videobewerking in het Nederlands

Nederland en Vlaanderen vormen samen een van de meest digitaal verbonden markten ter wereld. Nederland heeft een internetpenetratie van 98%, de hoogste in Europa. België (Vlaanderen) volgt met 94%. YouTube bereikt 93% van de Nederlandse bevolking. Nederlandse en Vlaamse content creators behoren tot de meest succesvolle op YouTube per capita. Maar videobewerkingstools zijn vrijwel uitsluitend ontworpen voor het Engels — menu's, sjablonen, stemmen, en tekstfuncties gaan uit van Engelstalige gebruikers. Nederlandse ondertiteling op platforms als YouTube bereikt slechts 78-82% nauwkeurigheid, aanzienlijk lager dan Engels. NemoVideo behandelt Nederlands als volwaardige taal: automatische ondertitels met 98%+ nauwkeurigheid in Standaardnederlands en Vlaams, ingesproken tekst met authentieke accenten, correcte Nederlandse typografie, en cultureel passende content voor de Nederlandstalige markt.

The Netherlands and Flanders (Dutch-speaking Belgium) together represent 30 million native Dutch speakers with among the highest digital engagement rates globally. Dutch YouTube channels like Enzo Knol, NikkieTutorials, and StukTV have built multi-million subscriber audiences proving the market's appetite for Dutch-language content. Yet Dutch video producers face the same tooling gap as all non-English markets: editing software designed for English, auto-captions with poor Dutch accuracy (especially for compound words — Dutch creates long compound nouns that auto-caption systems break incorrectly), and no native Dutch voiceover options in most tools. NemoVideo provides Dutch-native video production: accurate Dutch transcription that handles compound words correctly, voiceover in Standard Dutch (Standaardnederlands/ABN) or Flemish (Vlaams), proper Dutch typography, and cultural awareness of the Netherlands and Flanders markets.

## Use Cases

1. **Nederlandse Ondertitels — Dutch Auto-Captioning (any length)** — A Dutch YouTuber needs subtitles that handle the language correctly. Dutch compound words are a specific challenge: "arbeidsongeschiktheidsverzekering" (disability insurance) is one word that auto-caption systems split into fragments. NemoVideo: transcribes Dutch at 98%+ accuracy with correct compound word handling (keeping compound words intact as single units), handles Dutch-specific sounds (the soft 'g' in standard Dutch vs. the hard 'g' in Southern Dutch, the diphthongs 'ui', 'eu', 'ij'), correctly applies Dutch spelling rules (including the trema — "coördinatie" not "coordinatie", "reëel" not "reeel"), differentiates between Standard Dutch and Flemish vocabulary when relevant, applies animated subtitle styling for social platforms, and positions within platform safe zones. Ondertitels die kloppen — woord voor woord, accent voor accent.

2. **Nederlandse Voice-Over — Standard Dutch and Flemish (any length)** — A marketing video, educational content, or corporate communication needs Dutch narration. NemoVideo: generates voiceover in Standard Dutch (ABN — Algemeen Beschaafd Nederlands: the neutral Dutch spoken on NOS news and NPO broadcasts, understood by all Dutch speakers) or Flemish (Vlaams: warmer, softer pronunciation with distinct vocabulary choices preferred by Belgian audiences), with regional nuance (Amsterdam urban, Randstad professional, Flemish formal, Flemish conversational). The accent choice matters: Standard Dutch sounds clinical to Flemish ears; Flemish sounds informal to Dutch ears. Each audience has preferences. Stem die past bij het publiek — geen generiek "Europees Nederlands" dat niemand echt spreekt.

3. **Sociale Media Content — Dutch Social Video (15-90s)** — Dutch social media consumption patterns differ from global averages: LinkedIn penetration in the Netherlands is the highest in the world (proportionally), Instagram Reels dominates the young demographic, and TikTok growth among Dutch users is explosive. NemoVideo: creates social content optimized for Dutch audiences (direct communication style — Dutch audiences value straightforwardness over marketing polish), adds Dutch text overlays with correct spelling and typography (ij as a single digraph in capitalization: IJsselmeer not Ijsselmeer), applies the visual style that performs in the Dutch market (clean, design-forward, slightly understated — reflecting Dutch design sensibility), and exports for the platforms that matter in the Benelux market. Content dat eruitziet alsof het door een Nederlands bureau is gemaakt.

4. **Bedrijfsvideo — Dutch Corporate Content (2-10 min)** — Dutch and Belgian companies operate in a bilingual business environment: Dutch for domestic communication, English for international contexts. NemoVideo: produces professional Dutch corporate video with appropriate register (zakelijk Nederlands — business Dutch that is professional without being stiff), handles bilingual content naturally (Dutch narration with English product names and technical terms rendered correctly within the Dutch speech flow), adds corporate text overlays in correct Dutch (formal "u" forms for external communication, informal "je" forms for internal culture videos), and exports for corporate platforms, LinkedIn (dominant in Dutch B2B), and internal communications. Bedrijfsvideo met dezelfde kwaliteit als een professioneel productiehuis.

5. **Educatieve Video — Dutch Educational Content (5-30 min)** — The Netherlands has a strong educational video market: from university lectures to primary school support content to professional development. NemoVideo: creates educational video with Dutch narration at learning-appropriate pace, handles academic Dutch vocabulary correctly (including Latin-derived scientific terms with Dutch pronunciation), adds educational overlays (vocabulary, formulas, diagrams with Dutch labels), generates accurate Dutch subtitles for accessibility (important for integration — many Dutch residents are non-native Dutch speakers learning the language), and produces content structured for Dutch educational platforms. Educatieve content die voldoet aan de standaarden van het Nederlandse onderwijs.

## How It Works

### Step 1 — Upload Video or Text
Any video for Dutch editing, or text/script for Dutch video generation.

### Step 2 — Configure Dutch Output
Choose: Standard Dutch or Flemish, formal or informal register, voiceover accent, subtitle style, and text overlay language.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "video-bewerken",
    "prompt": "Voeg Nederlandse ondertitels toe aan een video van 8 minuten. Automatische transcriptie in Standaardnederlands met 98%%+ nauwkeurigheid. Stijl: schone broadcast-ondertitels (wit op half-transparante donkere balk, maximaal 2 regels). Genereer ook een Nederlandse voice-over in ABN — professioneel, helder, vriendelijk. Achtergrondmuziek: rustige elektronische muziek. Voeg een titel toe aan het begin: De Toekomst van AI in Nederland — geanimeerd, modern lettertype. Exporteer 16:9 voor YouTube en 9:16 voor Instagram Reels.",
    "dutch_variant": "standard-dutch",
    "register": "professional-friendly",
    "subtitles": {
      "style": "broadcast-clean",
      "background": "semi-transparent-dark",
      "max_lines": 2,
      "timing": "word-level"
    },
    "voiceover": {
      "variant": "standard-dutch-abn",
      "tone": "professional-friendly"
    },
    "title": {"text": "De Toekomst van AI in Nederland", "animation": "modern-slide"},
    "music": "calm-electronic",
    "formats": ["16:9", "9:16"]
  }'
```

### Step 4 — Review Dutch Quality
Verify: compound words are intact, spelling is correct (including trema usage), voiceover sounds authentically Dutch (not German-accented or Flemish when Standard Dutch was requested), and text overlays handle Dutch-specific characters correctly (ij, IJ, trema, accents).

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Dutch editing requirements |
| `dutch_variant` | string | | "standard-dutch", "flemish", "surinamese-dutch" |
| `register` | string | | "formal", "informal", "professional-friendly", "academic" |
| `subtitles` | object | | {style, timing, position} |
| `voiceover` | object | | {variant, accent, tone, gender} |
| `text_overlays` | array | | [{text (Dutch), position, animation}] |
| `music` | string | | Music style |
| `bilingual` | boolean | | Dutch + English mixed content |
| `formats` | array | | ["16:9", "9:16", "1:1"] |

## Output Example

```json
{
  "job_id": "vedbw-20260329-001",
  "status": "completed",
  "dutch_variant": "standard-dutch",
  "subtitles": {"accuracy": 0.986, "words": 1240, "compound_words_correct": true},
  "voiceover": "standard-dutch-abn-professional",
  "outputs": {
    "youtube": {"file": "video-nl-16x9.mp4", "resolution": "1920x1080"},
    "reels": {"file": "video-nl-9x16.mp4", "resolution": "1080x1920"}
  }
}
```

## Tips

1. **Standard Dutch and Flemish are mutually intelligible but culturally distinct** — Using Standard Dutch voiceover for a Flemish audience works (they understand it perfectly) but feels distant — like a British narrator for American audiences but more pronounced. For Flemish-targeted content, Flemish voice creates warmth and cultural connection.
2. **Dutch compound words break auto-caption systems** — "Ziekenhuisverplaatsingskosten" (hospital transfer costs) is one word. Auto-caption systems split it into fragments that make no sense. Correct Dutch captioning must handle compound words as single units — this is the #1 quality indicator for Dutch subtitles.
3. **IJ is a digraph with special capitalization rules** — "IJsselmeer" not "Ijsselmeer." "IJMUIDEN" not "IJMUIDEN." The IJ capitalization rule is a uniquely Dutch typographic convention that signals native-quality text handling. Getting it wrong is immediately visible to Dutch readers.
4. **Dutch directness applies to video content too** — Dutch communication culture values directness and efficiency. Marketing videos that work in the US (emotional build-up, dramatic reveal) can feel overdone for Dutch audiences who prefer getting to the point. Match the content pacing to Dutch communication norms.
5. **LinkedIn is disproportionately important in the Dutch market** — The Netherlands has the highest LinkedIn penetration per capita globally. For B2B and professional content, LinkedIn video is often more important than YouTube in the Dutch market. Always include 1:1 or 16:9 LinkedIn-optimized exports for Dutch professional content.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube / website |
| MP4 9:16 | 1080x1920 | TikTok / Instagram Reels |
| MP4 1:1 | 1080x1080 | LinkedIn / Facebook |

## Related Skills

- [ai-subtitle-generator](/skills/ai-subtitle-generator) — Multi-language subtitles
- [ai-video-caption-generator](/skills/ai-video-caption-generator) — Dutch captions
- [video-editor-pt](/skills/video-editor-pt) — Portuguese video editing
- [video-editor-deutsch](/skills/video-editor-deutsch) — German video editing
