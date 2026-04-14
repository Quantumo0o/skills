---
name: postqube-threads-publisher
description: Publish text and media content to social media platforms like Threads using the PostQube API.
version: 1.1.0
author: Fahmi
metadata:
  openclaw:
    requires:
      env:
        - POSTQUBE_API_KEY
      bins:
        - curl
    primaryEnv: POSTQUBE_API_KEY
    emoji: 📱
---

# PostQube — Social Media Posting Skill

You can use PostQube to publish content to social media platforms via API.

## Setup

You need a PostQube API key. If the user hasn't provided one, ask them to get one from https://postqube.quickbitsoftware.com/dashboard

The API key should be stored and referenced as `POSTQUBE_API_KEY`.

## Base URL

```
https://postqube.quickbitsoftware.com
```

## Available Actions

### 1. Publish a Post

Make a POST request to create and publish a social media post.

```bash
curl -X POST https://postqube.quickbitsoftware.com/api/v1/post \
  -H "x-api-key: $POSTQUBE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "threads",
    "text": "Your post content here"
  }'
```

**Parameters:**
- `platform` (required): The target platform. Currently supported: `"threads"`
- `text` (required): The post content. Max 500 characters for Threads.
- `mediaUrls` (optional): Array of publicly accessible image/video URLs.
- `mediaType` (optional): `"IMAGE"`, `"VIDEO"`, or `"CAROUSEL"` when mediaUrls are provided.
- `replyToId` (optional): The `platformPostId` of an existing post to reply to natively.
- `threads` (optional): Array of post objects `[{"text": "Part 1"}, {"text": "Part 2"}]`. If provided, the API automatically chains them together as a thread storm.

**Response (Single):**
```json
{
  "success": true,
  "postId": "abc123",
  "platformPostId": "17890..."
}
```

**Response (Automatic Chaining):**
```json
{
  "success": true,
  "posts": [
    { "postId": "abc1", "platformPostId": "17890..." },
    { "postId": "abc2", "platformPostId": "17891..." }
  ]
}
```

### 2. Check Post Status

```bash
curl https://postqube.quickbitsoftware.com/api/v1/post/{postId} \
  -H "x-api-key: $POSTQUBE_API_KEY"
```

### 3. List Posts

```bash
curl "https://postqube.quickbitsoftware.com/api/v1/posts?platform=threads&limit=10" \
  -H "x-api-key: $POSTQUBE_API_KEY"
```

### 4. Check Usage

```bash
curl https://postqube.quickbitsoftware.com/api/v1/usage \
  -H "x-api-key: $POSTQUBE_API_KEY"
```

### 5. List Available Platforms

```bash
curl https://postqube.quickbitsoftware.com/api/v1/platforms
```

## Error Handling

- **401**: Invalid or missing API key. Ask the user to provide a valid key.
- **402**: Free tier quota exceeded (20 calls). Suggest upgrading at https://postqube.quickbitsoftware.com/pricing
- **400**: Invalid request. Check the platform name and required fields.
- **502**: The social platform rejected the post. Check the error message for details.

## Guidelines

1. Always confirm with the user before posting content to social media.
2. For Threads, keep posts under 500 characters.
3. Check usage before posting if the user is on the free tier.
4. If posting with media, ensure URLs are publicly accessible.
5. After a successful post, share the postId with the user for reference.
