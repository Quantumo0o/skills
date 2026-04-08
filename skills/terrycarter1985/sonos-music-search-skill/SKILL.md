---
name: sonos-music-search
description: Search and play music on Sonos speakers using Brave Search to find Spotify tracks
emoji: 🔊
homepage: https://github.com/clawhub/sonos-music-search
author: Your Name
keywords: sonos, music, brave-search, spotify, speaker, audio
license: MIT
version: 1.0.0
minimumCliVersion: 1.0.0
---

# Sonos Music Search Skill

Search for and play music on your Sonos speakers directly from OpenClaw, powered by Brave Search.

## Features

- 🔍 Uses Brave Search to find Spotify tracks across the web
- 🔊 Automatically plays found tracks on your specified Sonos speaker
- 🎵 View currently playing track information
- 🚀 Zero configuration required (just set your Brave API key)

## Installation

```bash
clawhub install sonos-music-search
```

Set your Brave Search API key:
```bash
export BRAVE_API_KEY=your-api-key-here
```

Get your API key at: https://api.search.brave.com/

## Usage

### Play a track
```claw
sonos play "Living Room" "pink floyd comfortably numb"
```

### View currently playing
```claw
sonos current "Living Room"
```

## Requirements

- Sonos speaker(s) on the same network
- Brave Search API key
- Node.js 18+

## Changelog

### 1.0.0
- Initial release
- Brave Search integration
- Basic Sonos playback control
