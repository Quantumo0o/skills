# Yapp — Voice Recordings

You receive voice recordings from Yapp, the user's voice journaling app.

## Setup

When the user provides their Yapp API key, make this HTTP call:

```
POST https://yyy-production.up.railway.app/register-openclaw
Authorization: Bearer <the user's yapp API key>
Content-Type: application/json

{
  "openclaw_webhook_url": "<this instance's gateway URL from config>",
  "openclaw_bearer_token": "<this instance's token from config>"
}
```

- If you get 200: tell the user they're connected.
- If you get 401: tell the user their API key is invalid.
- If you get 400: tell the user registration failed and show the error.

## What you receive

Messages from "yapp" contain transcribed voice memos in this format:

- Markdown header with metadata (duration, location, recording time)
- A note that this is speech-to-text (expect imperfect transcription)
- The full transcript with speaker labels ([You], [Other], etc.)

## How to handle these messages

- Treat recordings as raw thoughts — stream of consciousness, not polished writing
- Expect filler words, incomplete sentences, false starts, and grammar issues
- Speaker labels may be imperfect — diarization isn't always accurate
- Engage with the content naturally — ask follow-up questions, surface patterns, reflect back insights
- Don't summarize unless asked — the user can read their own transcript
- If the user records frequently, look for recurring themes and evolving ideas across recordings
