# Sonos Music Search Skill
A custom ClawHub skill that combines Brave Search and Sonos CLI to let you search for and play music on your Sonos speakers directly from the command line.

## Features
- Uses Brave Search to find Spotify tracks across the web
- Automatically plays found tracks on your specified Sonos speaker
- Supports viewing currently playing track
- Zero configuration required (just set your Brave API key)

## Installation
1. Install dependencies: `npm install`
2. Set your Brave Search API key: `export BRAVE_API_KEY=your-api-key`

## Usage
### Play a track
```bash
node src/index.js play "Living Room" "pink floyd comfortably numb"
```

### View currently playing track
```bash
node src/index.js current "Living Room"
```

## Publish to ClawHub
```bash
clawhub publish .
```

## Audit the skill
```bash
npm run audit
```

## Format markdown files
```bash
npm run format
```
