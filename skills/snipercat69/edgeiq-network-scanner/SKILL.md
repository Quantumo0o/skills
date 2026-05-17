# Network Scanner Skill

**Skill Name:** `network-scanner`  
**Category:** Security / Reconnaissance  
**Price:** Free (v1) / $20 Pro  
**Author:** EdgeIQ Labs  
**OpenClaw Compatible:** Yes — Python 3, pure stdlib, WSL + Windows

---

## What It Does

Performs comprehensive network reconnaissance: host discovery, TCP port scanning, service banner grabbing, and OS fingerprinting — **without nmap**. Pure Python sockets, works on WSL/Linux and Windows.

Designed for **authorized security auditing of networks you own or have explicit written permission to scan**.

> ⚠️ **Legal Notice:** Only scan networks you own or have explicit written permission to audit. Unauthorized scanning is illegal. This tool is for defensive security professionals, penetration testers, and network administrators.

---

## Features

- **Host Discovery** — ICMP ping sweep + TCP connect probe (works through firewalls)
- **Port Scanning** — TCP connect scan with configurable depth (quick/normal/intense)
- **Banner Grabbing** — Identify services and versions running on open ports
- **OS Fingerprinting** — RTT-based OS detection heuristics
- **Pure Python** — No nmap required, no external dependencies
- **Cross-Platform** — WSL/Linux + Windows compatible
- **Concurrent Scanning** — Multi-threaded for speed

---

## Installation

```bash
# Copy the scanner directory into your OpenClaw skills folder
cp -r /home/guy/.openclaw/workspace/apps/network-scanner ~/.openclaw/skills/network-scanner
```

---

## Usage

### Quick Scan (9 ports)

```bash
python3 /path/to/scanner.py 192.168.1.0/24 quick
```

### Normal Scan (20 ports)

```bash
python3 /path/to/scanner.py 192.168.1.0/24 normal
```

### Intense Scan (100 ports)

```bash
python3 /path/to/scanner.py 192.168.1.0/24 intense
```

### Single Host

```bash
python3 /path/to/scanner.py 10.0.0.1 normal
```

### As OpenClaw Discord Command

In `#net-scan` channel:
```
!net 192.168.1.0/24 normal
!net 10.0.0.1 intense
!net local quick
!net scanme.nmap.org normal
```

---

## Scan Depth Levels

| Level | Ports Scanned | Best For |
|-------|--------------|----------|
| `quick` | 9 | Fast local discovery |
| `normal` | 20 | General reconnaissance |
| `intense` | 100 | Full vulnerability assessment |

---

## Output Example

```
🔍 Network Scan Results
Target: 10.5.1.0/28 | Mode: normal | Duration: 18.3s
────────────────────────────────────────
[+] 10.5.1.1    alive  rtt: 1.2ms   os: linux/unix
    ├── 80/http    nginx  (likely reverse proxy)
    ├── 443/https  nginx  (TLS certificate available)
    └── 8080/http   nginx  (alt http)

[+] 10.5.1.13   alive  rtt: 8.7ms   os: windows
    ├── 80/http     Apache/Coyote 1.1
    └── 443/https   OpenSSL

Hosts found: 2 | Ports scanned: 20 | Errors: 0
```

---

## Pro Version Features ($20/mo via ClawHub)

- Autonomous subnet mapping (auto-discover gateway + expand scan)
- Full /16 Class-B scanning with progress tracking
- CVE correlation (auto-check discovered services against CVE database)
- Slack/Telegram delivery of scan reports
- Scheduled periodic scans with delta comparison
- Priority support and configuration help

---

## Architecture

- **Language:** Python 3 (pure stdlib)
- **Dependencies:** None (`socket`, `concurrent.futures`, `struct`, `random`)
- **Supported Platforms:** Linux/WSL, Windows, macOS
- **Concurrency:** `concurrent.futures.ThreadPoolExecutor`
- **Scan Types:** ICMP ping sweep, TCP connect scan, banner grab, OS fingerprint

---

## Legal & Ethical Use

This tool is for:
- Network administrators auditing their own infrastructure
- Penetration testers assessing client networks with authorization
- Bug bounty researchers (with program approval)
- Security researchers studying their own networks

This tool must NOT be used:
- Against networks without explicit written permission
- On public infrastructure you don't own
- For any unauthorized access or reconnaissance

---

## Support

Open an issue at: https://github.com/YOUR_GITHUB/network-scanner  
Documentation: https://edgeiq.netlify.app/docs/network-scanner
