# XSS Scanner Skill

**Skill Name:** `xss-scanner`  
**Category:** Security / Auditing  
**Price:** Free (v1) / $15 Pro  
**Author:** EdgeIQ Labs  
**OpenClaw Compatible:** Yes — Python 3, pure stdlib, WSL + Windows

---

## What It Does

Scans web applications for reflected XSS and DOM-based vulnerabilities using 24+ crafted payloads across multiple injection contexts. Designed for **authorized security auditing of applications you own or have explicit written permission to test**.

> ⚠️ **Legal Notice:** Only scan targets you own or have explicit written permission to audit. Unauthorized scanning is illegal. This tool is for defensive security professionals and researchers.

---

## Features

- **24 XSS Payloads** — script tags, event handlers, attribute injection, URL/encoding bypasses
- **6 Context Modes** — `html_body`, `html_attr`, `js_string`, `comment`, `css`, `url_param`
- **Smart Filtering** — skips JSON/XML API responses to reduce false positives
- **Concurrent Scanning** — configurable worker threads (default: 5)
- **Crawl Mode** — auto-discovers links up to a configurable depth
- **Pure Python** — no nmap, no external dependencies, works on WSL + Windows

---

## Installation

```bash
# Copy the scanner directory into your OpenClaw skills folder
cp -r /home/guy/.openclaw/workspace/apps/xss-scanner ~/.openclaw/skills/xss-scanner
```

---

## Usage

### Basic Scan (single URL)

```bash
python3 /path/to/scanner.py https://example.com
```

### With Crawl Depth

```bash
python3 /path/to/scanner.py https://example.com --depth 2 --max-urls 30
```

### Intense Scan (full port coverage + external links)

```bash
python3 /path/to/scanner.py https://example.com --depth 3 --max-urls 50 --workers 10 --follow-external
```

### As OpenClaw Discord Command

In `#xss-scanner` channel:
```
!xss https://example.com
!xss https://example.com --depth 3 --workers 10
!xss https://example.com --follow-external
```

---

## Parameters

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--depth` | int | 2 | Crawl depth (links discovered beyond this depth are not followed) |
| `--max-urls` | int | 50 | Maximum URLs to scan before stopping |
| `--workers` | int | 5 | Concurrent worker threads |
| `--follow-external` | flag | False | Follow links to external domains (default: off) |

---

## Payload Context Detection

The scanner automatically detects the response context and applies relevant payloads:

| Context | Detected When | Payload Strategy |
|---------|--------------|-----------------|
| `html_body` | Plain HTML in response body | Script tags, event handlers |
| `html_attr` | Inside an HTML attribute | Quote/attribute injection |
| `js_string` | Inside a JavaScript string | Escape + inject |
| `comment` | Inside an HTML comment | Break out of comment |
| `css` | Inside a CSS context | Style injection |
| `url_param` | Parameter value reflected in URL | URL-encoded XSS |

---

## Output Example

```
🛑 XSS Vulnerability Found
URL:    https://target.com/search?q=test
Method: GET | Param: q
Context: html_body
Payload: <script>alert(1)</script>
Evidence: <script>alert(1)</script> reflected in HTML body
Severity: HIGH — confirmed executable script injection
---
Vulnerabilities found: 1
Scan duration: 12.4s | URLs scanned: 14
```

---

## Pro Version Features ($15/mo via ClawHub)

- Full crawl with external link following
- Export results as JSON + CSV
- Slack/Telegram delivery of scan reports
- Scheduled recurring scans with diff reports
- Priority support and configuration help

---

## Architecture

- **Language:** Python 3 (pure stdlib)
- **Dependencies:** None (no nmap, no httpx, no bs4)
- **Supported Platforms:** Linux/WSL, Windows, macOS
- **Concurrency:** `concurrent.futures.ThreadPoolExecutor`
- **Crawl Strategy:** BFS with configurable depth and URL deduplication

---

## Legal & Ethical Use

This tool is for:
- Security researchers auditing bug bounty targets with authorization
- Penetration testers assessing client applications
- Developers testing their own applications
- Defensive security teams auditing internal infrastructure

This tool must NOT be used:
- Against targets without explicit written permission
- On production systems without authorization
- For any unauthorized access or testing

---

## Support

Open an issue at: https://github.com/YOUR_GITHUB/xss-scanner  
Documentation: https://edgeiq.netlify.app/docs/xss-scanner
