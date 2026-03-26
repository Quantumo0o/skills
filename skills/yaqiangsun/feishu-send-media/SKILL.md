---
name: feishu-send-media
description: |
  Send images, files, audio, video and other media to Feishu users or chats. Use when user asks to send, share, or transfer media files via Feishu direct message or group chat.
---

# Feishu Send Media

Send media files (images, documents, audio, video) directly to Feishu users or chats using the `message` tool.

## Sending Media

### Basic File Send

Use the `message` tool with `action: send` and `path` parameter:

```json
{
  "action": "send",
  "target": "ou_xxx",  // user open_id or chat_id
  "path": "/path/to/file.pdf"
}
```

**Supported types:**
- Images: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`
- Documents: `.doc`, `.docx`, `.pdf`, `.txt`, `.rtf`
- Audio: `.mp3`, `.wav`, `.m4a`
- Video: `.mp4`, `.mov`

**Parameters:**
- `target`: User `open_id` (e.g., `ou_3ac66d1ad7b8c1xxxxxxxxxxxxxxs`) or chat ID
- `path`: Absolute path to local file
- Optional `filename`: Override display name

### Sending to Group Chats

Use chat_id as target:

```json
{
  "action": "send",
  "target": "oc_xxx",  // group chat ID
  "path": "/path/to/file.pdf"
}
```

### Inline Images

For images to display inline in the message (not as attachments), use the `image` parameter with base64:

```json
{
  "action": "send",
  "target": "ou_xxx",
  "image": "data:image/png;base64,..."
}
```

## High-Reliability Workflow (Recommended)

**Follow these steps exactly for maximum success rate:**

### Step 1: Copy file to workspace
```bash
cp /source/path/to/file.png ~/.openclaw/workspace/
```
Always use workspace directory (`~/.openclaw/workspace/`), never use desktop or downloads directly.

### Step 2: Verify file exists
```bash
ls -la ~/.openclaw/workspace/filename.*
```
If file doesn't exist, abort and report error.

### Step 3: Get absolute path
```bash
readlink -f ~/.openclaw/workspace/filename.png
```
Use the absolute path (e.g., `/Users/casia/.openclaw/workspace/filename.png`)

### Step 4: Send with message tool
```json
{
  "action": "send",
  "target": "ou_xxx",
  "path": "/Users/casia/.openclaw/workspace/filename.png"
}
```

### Step 5: Verify response
Check the tool response for `"messageId"` field. If present, the send was successful. If error, try fallback method.

## Fallback Methods

### Fallback 1: Use base64 for images
If path method fails, convert image to base64:
```bash
base64 -i ~/.openclaw/workspace/filename.png
```
Then send with:
```json
{
  "action": "send",
  "target": "ou_xxx",
  "image": "data:image/png;base64,<base64_string>"
}
```

### Fallback 2: Upload to Feishu drive first
If both above fail, upload to Feishu cloud drive, then send the file link.

## Error Handling

- **File not found**: Always copy to workspace first
- **Permission denied**: Check file permissions with `ls -la`
- **File too large**: For files >20MB, use Feishu drive instead
- **Unknown error**: Try base64 fallback or upload to drive

## Quick Reference

| File Type | Best Method | Fallback |
|-----------|-------------|----------|
| Images (<5MB) | path → base64 | - |
| Documents | path | Upload to drive |
| Audio/Video | path | Upload to drive |
| Large files | Upload to drive | - |

**Golden Rule**: Always copy to workspace first, then send from there.