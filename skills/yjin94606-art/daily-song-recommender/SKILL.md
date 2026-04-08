---
name: daily-song-recommender
version: "1.1.0"
description: AI-powered daily song recommendation skill. Searches the web for fresh music recommendations based on user's style preferences. Triggered when user says "recommend a song", "what should I listen to today", "play some rock", "I'm into jazz lately", "random song", "new music recommendations", etc. Supports all genres: POP, Rock, Jazz, Classical, Electronic, Folk, Rap, J-Pop, K-Pop, Chinese, Indie, etc. AI searches the internet for the latest and trending songs matching the user's taste.
---

# Daily Song Recommender 🎵

AI-powered music recommendation that searches the web for fresh recommendations!

## How It Works

1. **User expresses music preference** (or asks for random recommendation)
2. **AI searches the web** for latest/trending songs matching that style
3. **AI presents** 3-5 personalized recommendations with links and reasons

## Trigger Examples

- "recommend a song"
- "what should I listen to today"
- "play some rock music"
- "I'm into jazz lately, any suggestions?"
- "new indie rock recommendations"
- "K-pop suggestions please"
- "surprise me with something"
- "what's trending in pop music"

## Recommendation Process

### Step 1: Understand Preference

Ask clarifying questions if needed:
- "What genre are you in the mood for?"
- "Any specific decade or style?"
- "Do you prefer vocals or instrumental?"

### Step 2: Web Search

Use `web_search` tool to find current recommendations:

```
Query: "best rock songs 2024 recommendations"
Query: "top jazz albums suggestions"
Query: "new K-pop songs trending"
```

### Step 3: Present Recommendations

Format output like this:

```
🎵 Today's Recommendations

1. 【Song/Album Name】
   Artist: xxx
   Why it's great: xxx
   🔗 Listen: [link]

2. 【Song/Album Name】
   Artist: xxx
   Why it's great: xxx
   🔗 Listen: [link]

3. 【Song/Album Name】
   Artist: xxx
   Why it's great: xxx
   🔗 Listen: [link]

---
💡 Sources: [where recommendations came from]
```

## Search Query Templates

| Genre | Search Query Examples |
|-------|----------------------|
| POP | "top pop songs 2024 recommendations", "best new pop music" |
| Rock | "best rock songs 2024", "new rock music recommendations" |
| Jazz | "best jazz albums 2024", "new jazz music suggestions" |
| Classical | "best classical music 2024", "contemporary classical recommendations" |
| Electronic | "best electronic music 2024", "top EDM tracks" |
| Folk/Indie | "best indie folk 2024", "new acoustic music" |
| Rap/Hip-Hop | "best rap songs 2024", "top hip-hop releases" |
| J-Pop | "best J-pop 2024", "trending Japanese music" |
| K-Pop | "best K-pop 2024", "new Korean music releases" |
| Chinese | "best Chinese songs 2024", "new Mandopop releases" |
| Vintage | "best classic songs all time", "timeless music recommendations" |
| Chill | "best chill music 2024", "relaxing ambient playlists" |

## Tips

- Always search for **current/recent** recommendations when possible
- Include release year in search for freshness
- Check multiple sources for variety
- Provide direct links to streaming platforms when found
- Give 3-5 recommendations per session
- Mix well-known artists with emerging ones for discovery
