---
name: folder-visualizer-html
display_name: "Folder UI Visualizer - show the folder through HTML (via Telegram)"
description: >
  A security-hardened visual directory tree generator. Use this to create a 
  collapsible HTML visualization of local folders. Features built-in XSS 
  protection and shell-injection defenses. Designed for mobile viewing via Telegram.
metadata:
  clawdbot:
    emoji: "📁"
    category: "Security & Utility"
    requires:
      bins: ["node"]
---

# Secure Folder Visualizer

This skill generates a self-contained, XSS-safe HTML report of a directory structure. It is optimized for the "Generate -> Send -> Cleanup" secure workflow.

## Trigger Scenarios
- "Visualize the folder `[path]`."
- "Show me what's inside this directory."
- "Send a tree map of my project to Telegram."

## Execute Command
```bash
node {baseDir}/file_lister.js "<directory_path>"

```

## Arguments & Sanitization (CRITICAL)

* `<directory_path>`: The target folder path.
* **Sanitization Rule:** Before executing, you **MUST** sanitize this path. Remove or escape any shell-active characters: `;`, `&`, `|`, `(`, `)`, ```, `$`, `<`, `>`, `\`.
* **Normalization:** Convert relative paths (like `.` or `./src`) to **Absolute Paths** to prevent directory traversal ambiguity.
* **Formatting:** Always wrap the sanitized absolute path in **double quotes** `""`.



## Expected Output & Next Actions

1. **Expected Output:** The script will output the absolute path to the generated `.html` file.
2. **STRICT Execution Sequence:**
* **Step 1 (Deliver):** Use `telegram.sendDocument` to send the file at the returned path to the user.
* **Step 2 (Cleanup):** REGARDLESS of success, immediately delete the file.
* *Windows:* `del "<path>"`
* *Linux/macOS:* `rm "<path>"`


* **Step 3 (Reply):** Inform the user: "The secure folder report has been sent and the local temp file has been purged."



## Security Notes

* **XSS Protection:** Filenames are automatically escaped in the HTML report.
* **Injection Defense:** The Agent is responsible for path sanitization per the rules above.
* **Privacy:** No data is uploaded to 3rd party servers; transfer is handled via secure Telegram API.
