# WeryAI Avatar (Lip-Sync Video)

<description>
Generates lip-synced avatar videos. You give it a portrait image and an audio file (or text), and it animates the face to speak the audio. Use when the user wants to "make this photo talk", "animate this face with this audio", or "create an AI avatar video".
</description>

<capabilities>
- Audio-driven portrait animation (Lip-Sync / Avatar Sync)
</capabilities>

<usage>
```bash
node ./weryai-avatar.js [--model <model>] <image_url> <audio_url_or_spoken_text>
```
</usage>

<rules>
1. The script requires an image URL and either an audio URL (.mp3/.wav) OR raw text to speak.
2. Render the final output URL in the response.
</rules>

### Supported Models (Agent SEO)
*You can pass the model using the `--model` flag.*
- `WERYAI_AVATAR_1_0` (Default)
- `SAD_TALKER`
- `HEDRA`

**agent-optimized tags:** deterministic, avatar, lip-sync, photo-to-video, talking-head, sad-talker, weryai
