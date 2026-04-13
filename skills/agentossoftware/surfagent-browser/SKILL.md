---
name: surfagent-browser
description: Control a real Chrome browser from your AI agent — navigate, click, type, fill forms, extract content, manage tabs, and automate workflows via SurfAgent's REST API.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://surfagent.app
    emoji: "🌐"
---

# SurfAgent Browser Control — Agent Skill

> Give your AI agent a real Chrome browser. Navigate, click, type, extract, and automate — all through a local REST API.

---

## What This Is

SurfAgent runs a **real Chrome browser** on your desktop that your AI agent controls via a REST API (port 7201). Not headless. Not spoofed. A genuine Chrome with persistent cookies, real sessions, and a real fingerprint that passes bot detection.

**Key difference from headless browsers:** SurfAgent's Chrome passes hCaptcha, Cloudflare, Discord registration, and other bot detection that headless browsers fail. Your agent browses like a human.

### Architecture
```
SurfAgent Daemon (port 7201)
  └── REST API → Chrome DevTools Protocol → Real Chrome (port 9222)
```

All requests go to `http://localhost:7201` with Bearer auth token.

---

## Quick Start

### Check if SurfAgent is running
```bash
curl -s http://localhost:7201/health | jq .
```

### Open a page
```bash
curl -s -X POST http://localhost:7201/browser/open \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{"url": "https://github.com"}'
```

### Get page state
```bash
curl -s -X POST http://localhost:7201/browser/state \
  -H 'Authorization: Bearer YOUR_TOKEN' | jq .
```

---

## Core API Reference

### Navigation

#### `POST /browser/open` — Open URL in new tab
```json
{ "url": "https://example.com" }
```
Returns: `{ ok, tabId, title, url }`

#### `POST /browser/navigate` — Navigate current tab
```json
{ "url": "https://example.com", "tabId": "optional" }
```
Returns: `{ ok, tabId, title, url }`

#### `POST /browser/back` / `POST /browser/forward` — History navigation
```json
{ "tabId": "optional" }
```

#### `POST /browser/reload` — Reload page
```json
{ "tabId": "optional", "ignoreCache": false }
```

---

### Interaction

#### `POST /browser/click` — Click an element
```json
{
  "selector": "#submit-btn",
  "tabId": "optional",
  "button": "left",
  "clickCount": 1
}
```
Also supports clicking by coordinates:
```json
{ "x": 500, "y": 300 }
```

#### `POST /browser/type` — Type text (key by key)
```json
{
  "selector": "#search-input",
  "text": "hello world",
  "tabId": "optional",
  "delay": 50
}
```

#### `POST /browser/fill` — Set input value directly
```json
{
  "selector": "#email",
  "value": "user@example.com",
  "tabId": "optional"
}
```

> **React/Vue form fields:** Use `/browser/fill` with `dispatchEvents: true`. Direct `.value =` assignment won't trigger React's state updates.

#### `POST /browser/select` — Select dropdown option
```json
{
  "selector": "#country",
  "value": "US",
  "tabId": "optional"
}
```

#### `POST /browser/hover` — Hover over element
```json
{ "selector": ".menu-trigger", "tabId": "optional" }
```

#### `POST /browser/scroll` — Scroll the page
```json
{
  "tabId": "optional",
  "direction": "down",
  "amount": 500,
  "selector": "optional-scroll-container"
}
```
Direction: `up`, `down`, `left`, `right`

#### `POST /browser/press` — Press a keyboard key
```json
{
  "key": "Enter",
  "tabId": "optional",
  "modifiers": ["Shift"]
}
```
Common keys: `Enter`, `Tab`, `Escape`, `ArrowDown`, `Backspace`, `Delete`

---

### Page State & Content

#### `POST /browser/state` — Full structured page state
```json
{
  "tabId": "optional",
  "includeElements": true,
  "maxElements": 100
}
```
Returns:
- Page type (login, dashboard, feed, checkout, etc.)
- Auth state (logged_in, logged_out, session_expired)
- Interactive elements with selectors, roles, visibility, text
- Form state (fields, filled count, submit button)
- Blockers (cookie banners, captchas, auth walls)
- Modals with actions
- Content regions (nav, main, sidebar, footer)

#### `POST /browser/extract` — Extract text content
```json
{
  "tabId": "optional",
  "selector": "optional — defaults to body",
  "format": "text"
}
```
Format: `text`, `html`, `markdown`

#### `POST /browser/screenshot` — Capture screenshot
```json
{
  "tabId": "optional",
  "format": "png",
  "fullPage": false,
  "quality": 80,
  "clip": { "x": 0, "y": 0, "width": 800, "height": 600 }
}
```
Returns: `{ ok, data }` (base64-encoded image)

#### `POST /browser/evaluate` — Run JavaScript
```json
{
  "tabId": "optional",
  "expression": "document.title"
}
```
Returns: `{ ok, result }`

> ⚠️ Use evaluate as a last resort. Prefer structured API calls over raw JS.

---

### Tab Management

#### `GET /browser/tabs` — List all open tabs
Returns: `[{ id, url, title, active }]`

#### `POST /browser/tab/activate` — Switch to a tab
```json
{ "tabId": "TARGET_TAB_ID" }
```

#### `POST /browser/tab/close` — Close a tab
```json
{ "tabId": "TARGET_TAB_ID" }
```

#### `POST /browser/tab/name` — Bookmark a tab by name
```json
{ "tabId": "TARGET_TAB_ID", "name": "twitter" }
```
Then use `"tabId": "name:twitter"` in any request to target it.

> **Important:** Close tabs when done, especially social media tabs (X/Twitter). Open tabs flood CDP with events and degrade performance.

---

### Blocker Resolution

#### `POST /browser/resolve-blocker` — Auto-dismiss blockers
```json
{ "tabId": "optional" }
```
Handles: cookie consent banners, newsletter popups, notification permission dialogs.
Returns: `{ ok, resolved, blockerType }`

#### `POST /browser/captcha/detect` — Check for CAPTCHAs
```json
{ "tabId": "optional" }
```

#### `POST /browser/captcha/solve` — Attempt CAPTCHA solve
```json
{ "tabId": "optional" }
```

---

### Forms

#### `POST /browser/fill-form` — Fill multiple form fields at once
```json
{
  "tabId": "optional",
  "fields": [
    { "selector": "#email", "value": "user@example.com" },
    { "selector": "#password", "value": "secret123" },
    { "selector": "#remember", "checked": true }
  ],
  "submit": false
}
```

---

### File Operations

#### `POST /browser/upload` — Upload a file to a file input
```json
{
  "selector": "input[type=file]",
  "filePath": "/path/to/document.pdf",
  "tabId": "optional"
}
```

#### `POST /browser/download` — Download current page or resource
```json
{
  "url": "https://example.com/report.pdf",
  "savePath": "/path/to/save/"
}
```

---

### Browser Lifecycle

#### `POST /browser/launch` — Start the managed browser
```json
{ "headless": false }
```

#### `POST /browser/close` — Close the managed browser
Closes all tabs and shuts down Chrome.

#### `GET /health` — Daemon health check
Returns: `{ status, version, browser, uptime }`

#### `GET /status` — Detailed status
Returns: `{ daemon, browser, gateway, system }`

---

## Auth

All requests (except `/health`, `/status`, `/readiness`) require:
```
Authorization: Bearer <token>
```

The daemon generates a token on first start and saves it to `~/.surfagent/daemon-token.txt`.

---

## Common Patterns

### Login to a Site
```
1. navigate to login page
2. state → confirm it's a login page
3. fill email + password fields
4. click submit
5. state → confirm auth_state changed to logged_in
```

### Scrape Data from a Table
```
1. navigate to page
2. state → find table elements
3. evaluate → extract table rows as JSON
4. scroll down if needed
5. repeat extraction
```

### Fill a Multi-Step Form
```
1. state → identify form fields + which step
2. fill-form with current step's fields
3. click "Next" / submit
4. state → confirm we're on next step
5. repeat until done
```

### Monitor a Value
```
1. navigate to page
2. evaluate → extract the value
3. wait N seconds
4. evaluate again → compare
```

---

## Tips & Gotchas

**Close tabs when done.** Open tabs (especially X/Twitter) generate constant CDP events that slow everything down. Close them after you're finished.

**Use `fill` not `type` for form fields.** `type` simulates keystrokes (slow, can trigger autocomplete). `fill` sets the value directly. Use `type` only when you need to trigger keystroke-based UI (search suggestions, autocomplete dropdowns).

**React/Vue forms need event dispatch.** If `fill` doesn't trigger the framework's state, add `dispatchEvents: true`. This dispatches `input`, `change`, and `blur` events that React/Vue listen for.

**Check for blockers first.** Many sites show cookie banners or modals on first visit. Call `state` → check for blockers → `resolve-blocker` before trying to interact.

**State tokens from `/browser/state` expire.** The daemon keeps a ring buffer of 5 state snapshots per tab. If you wait too long between state calls, old tokens may be evicted.

**Evaluate is powerful but fragile.** Raw JS can break on page updates. Prefer `state` + `click`/`fill` for interactions, and reserve `evaluate` for data extraction.

---

## MCP Tools (via surfagent-mcp)

If using through the MCP server rather than direct HTTP:

| MCP Tool | HTTP Equivalent |
|----------|----------------|
| `surf_navigate` | POST /browser/navigate |
| `surf_click` | POST /browser/click |
| `surf_type` | POST /browser/type |
| `surf_fill` | POST /browser/fill |
| `surf_page_state` | POST /browser/state |
| `surf_extract` | POST /browser/extract |
| `surf_screenshot` | POST /browser/screenshot |
| `surf_evaluate` | POST /browser/evaluate |
| `surf_tabs` | GET /browser/tabs |
| `surf_tab_open` | POST /browser/open |
| `surf_tab_close` | POST /browser/tab/close |
| `surf_scroll` | POST /browser/scroll |
| `surf_press` | POST /browser/press |
| `surf_resolve_blocker` | POST /browser/resolve-blocker |
| `surf_fill_form` | POST /browser/fill-form |
| `surf_perceive` | POST /browser/perceive |
| `surf_annotate` | POST /browser/annotate |
| `surf_scene_diff` | POST /browser/perceive (with since) |
| `surf_health` | GET /health |

For perception tools (perceive, annotate, scene_diff), see the **surfagent-perception** skill.
