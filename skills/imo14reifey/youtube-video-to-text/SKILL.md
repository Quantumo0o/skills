---
name: youtube-video-to-text
version: "1.0.0"
displayName: "YouTube Video to Text — Transcribe YouTube Videos to Text, SRT and Summary"
description: >
  Transcribe any YouTube video to text using AI — get a full transcript, timestamped SRT captions, chapter summaries, and key-point extraction from any YouTube URL. NemoVideo downloads the audio, transcribes with 98%+ accuracy, identifies speakers, removes filler words, formats into clean paragraphs, and generates multiple output formats — turning hours of video content into searchable, quotable, repurposable text in minutes.
metadata: {"openclaw": {"emoji": "📄", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# YouTube Video to Text — Transcribe Any YouTube Video

YouTube holds the world's largest library of spoken knowledge — and almost none of it is searchable as text. A 45-minute conference talk contains insights that would take 3 minutes to read if transcribed, but finding them requires watching the entire video or scrubbing through a timeline hoping to land on the right moment. A 2-hour podcast episode has 15,000 words of conversation that can't be quoted, cited, or repurposed without manual transcription. A creator's 200-video back catalog represents a book's worth of expertise locked inside audio that search engines can't index. YouTube's auto-generated captions exist but they're unreliable: no punctuation, no paragraph breaks, no speaker identification, frequent errors on proper nouns and technical terms, and no summary or key-point extraction. They're a raw stream of words, not a usable transcript. NemoVideo produces publication-ready transcripts: accurate speech-to-text with proper punctuation and paragraph breaks, speaker identification and labeling, timestamped segments for easy reference, filler word removal, technical term correction, chapter summaries that distill each section into 2-3 sentences, and key-point extraction that pulls the most important insights into a bullet-point summary. The 45-minute talk becomes a 5-page document you can search, quote, share, and repurpose.

## Use Cases

1. **Conference Talk → Readable Transcript (20-60 min)** — A keynote from a tech conference. NemoVideo: transcribes the full 45 minutes with speaker labels (Speaker changes when Q&A begins), formats into paragraphs at natural topic breaks, corrects technical terms (Kubernetes, PostgreSQL, React — not "kubernetes," "post gress," "react"), removes filler words, generates chapter summaries (one paragraph per 5-minute section), and extracts the 10 key takeaways as a bullet-point list. The talk becomes a blog post draft without manual editing.
2. **Podcast Episode → Show Notes + Quotes (30-120 min)** — A 90-minute interview podcast needs show notes. NemoVideo: transcribes with speaker labels (Host: / Guest:), timestamps every topic change, generates a 200-word summary, extracts the 5 most quotable moments with timestamps ("At 23:45, Dr. Chen says: 'The real breakthrough wasn't the algorithm — it was realizing we were asking the wrong question.'"), and produces a chapter list for the podcast player. Professional show notes from one API call.
3. **Lecture Series → Study Notes (multiple videos)** — A student has 12 lecture videos totaling 18 hours. NemoVideo batch-transcribes all 12, generates per-lecture summaries (500 words each), extracts all definitions and key terms with timestamps, produces a combined glossary across all lectures, and creates a "key concepts" document that distills 18 hours into 30 pages of searchable study material.
4. **Creator Back-Catalog → SEO Content (any count)** — A YouTube creator with 200 videos wants to repurpose their spoken content into blog posts for SEO. NemoVideo: batch-transcribes the entire catalog, generates a 500-word blog post draft from each video (reformatted from spoken to written style), extracts the most search-relevant paragraphs, and produces meta descriptions. 200 videos become 200 blog posts — the creator's entire knowledge base becomes searchable on Google.
5. **Meeting Recording → Action Items (15-120 min)** — A recorded Zoom meeting needs minutes. NemoVideo: transcribes with participant identification, detects and labels action items ("ACTION: Sarah will send the revised proposal by Friday"), extracts all decisions made ("DECISION: We'll proceed with Option B"), generates a 200-word executive summary, and timestamps every agenda topic. The full meeting becomes an actionable document.

## How It Works

### Step 1 — Provide YouTube URL or Video
Paste a YouTube URL or upload a video file. NemoVideo extracts the audio and analyzes speech patterns, speaker changes, and topic structure.

### Step 2 — Choose Output Format
Select: full transcript, timestamped SRT, chapter summaries, key points, blog post draft, or all of the above.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "youtube-video-to-text",
    "prompt": "Transcribe this YouTube video and generate comprehensive text outputs. URL: https://youtube.com/watch?v=example. Outputs: full transcript with paragraphs and speaker labels, timestamped SRT file, chapter summaries (one paragraph per major topic), key takeaways (bullet points), and a 300-word blog post summary. Remove filler words. Correct technical terms. Language: English.",
    "url": "https://youtube.com/watch?v=example",
    "outputs": ["transcript", "srt", "chapters", "key-points", "blog-summary"],
    "remove_fillers": true,
    "speaker_labels": true,
    "language": "en"
  }'
```

### Step 4 — Review and Export
Review the transcript for accuracy. Edit proper nouns or technical terms if needed. Export in desired formats.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Video URL and transcription requirements |
| `url` | string | | YouTube URL or video file path |
| `outputs` | array | | ["transcript","srt","vtt","chapters","key-points","blog-summary","action-items"] |
| `remove_fillers` | boolean | | Remove um/uh/like/you know (default: true) |
| `speaker_labels` | boolean | | Identify and label speakers (default: true) |
| `language` | string | | "auto", "en", "es", "fr", "de", "ja", "zh" |
| `translate_to` | string | | Translate transcript to target language |
| `summary_length` | string | | "brief" (100w), "standard" (300w), "detailed" (500w) |
| `batch_urls` | array | | Multiple YouTube URLs for batch processing |
| `technical_domain` | string | | "tech", "medical", "legal", "finance" — improves term accuracy |

## Output Example

```json
{
  "job_id": "yvt-20260328-001",
  "status": "completed",
  "source_url": "https://youtube.com/watch?v=example",
  "source_duration": "45:22",
  "language_detected": "en",
  "outputs": {
    "transcript": {
      "file": "transcript.txt",
      "word_count": 6842,
      "paragraphs": 89,
      "speakers_identified": 2,
      "fillers_removed": 127
    },
    "srt": {
      "file": "captions.srt",
      "lines": 412,
      "timing_accuracy": "±0.2 sec"
    },
    "chapters": [
      {"title": "Introduction and Background", "timestamp": "0:00", "summary": "Speaker introduces the topic of distributed systems reliability..."},
      {"title": "The Three Failure Modes", "timestamp": "8:15", "summary": "Three categories of distributed system failures are examined..."},
      {"title": "Practical Mitigation Strategies", "timestamp": "22:40", "summary": "Concrete approaches to handling each failure mode..."},
      {"title": "Q&A Session", "timestamp": "38:10", "summary": "Audience questions about implementation specifics..."}
    ],
    "key_points": [
      "Distributed systems fail in three distinct modes: network partition, node failure, and data corruption",
      "Circuit breakers should open after 3 consecutive failures, not after a percentage threshold",
      "The most common mistake is treating all timeouts as network failures when 60% are actually slow queries"
    ],
    "blog_summary": {
      "file": "blog-summary.txt",
      "word_count": 312
    }
  }
}
```

## Tips

1. **Technical domain setting improves accuracy 15-20%** — Telling NemoVideo the video is about "tech" means it correctly transcribes "Kubernetes" instead of "kubernetes" and "PostgreSQL" instead of "post gres sequel." Domain context prevents the most embarrassing transcription errors.
2. **Chapter summaries are more useful than full transcripts** — Most people don't read a 7,000-word transcript. They want to know what each section covers and jump to the relevant part. Chapter summaries serve 80% of use cases in 10% of the word count.
3. **Key-point extraction turns a 45-minute video into a tweet thread** — The 5-10 most important insights, distilled into bullet points, are immediately shareable on social media. One video becomes content for multiple platforms.
4. **Batch processing unlocks back-catalog value** — A creator's 200 videos are 200 blog posts waiting to be written. Batch transcription and blog-summary generation turns a video archive into a searchable content library.
5. **Speaker labels make interviews quotable** — "Guest says: '...'" is citable in an article. An unlabeled transcript requires the writer to figure out who said what, which usually means they don't bother quoting.

## Output Formats

| Format | Content | Use Case |
|--------|---------|----------|
| TXT | Full transcript | Reading / searching / quoting |
| SRT | Timestamped captions | YouTube captions / subtitle files |
| VTT | Web captions | HTML5 video players |
| MD | Formatted summary | Blog posts / documentation |
| JSON | Structured data | API integration / databases |

## Related Skills

- [text-to-speech-ai](/skills/text-to-speech-ai) — Convert text back to speech
- [subtitle-video-generator](/skills/subtitle-video-generator) — Burn subtitles into video
- [instagram-video-caption](/skills/instagram-video-caption) — Instagram captions
