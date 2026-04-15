#!/usr/bin/env python3
"""
Discord command wrapper for the XSS scanner.
Usage: python3 discord_xss_command.py <command>

Commands:
  !xss <url> [--depth n] [--max-urls n]   Scan a URL
  !xss help                             Show help
"""

import subprocess
import sys

SCRIPT_PATH = "/home/guy/.openclaw/workspace/apps/xss-scanner/scanner.py"

HELP_TEXT = """
**`!xss <url> [--depth n] [--max-urls n]`** — Scan a URL for XSS vulnerabilities

**Options:**
• `--depth n`   — Crawl depth (default: 2, max recommended: 3)
• `--max-urls n` — Max URLs to crawl (default: 20)
• `--workers n`  — Concurrent workers (default: 15)

**Examples:**
  `!xss https://example.com/page?id=1`
  `!xss https://example.com --depth 1 --max-urls 5`
  `!xss https://example.com --follow-external`

**Note:** Scan only targets you own or have permission to test.
Always scan responsibly.
"""

def run_scan(args_str: str) -> str:
    args = args_str.strip().split()
    if not args or args[0] == "help":
        return HELP_TEXT.strip()

    cmd = ["python3", SCRIPT_PATH]
    target = args[0]
    cmd.append(target)

    # Handle optional flags
    if "--depth" in args:
        idx = args.index("--depth")
        cmd.extend(["--depth", args[idx + 1]])
    if "--max-urls" in args:
        idx = args.index("--max-urls")
        cmd.extend(["--max-urls", args[idx + 1]])
    if "--workers" in args:
        idx = args.index("--workers")
        cmd.extend(["--workers", args[idx + 1]])
    if "--follow-external" in args:
        cmd.append("--follow-external")

    cmd.extend(["--format", "discord"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        out = result.stdout.strip()
        if not out:
            err = result.stderr.strip()
            return f"```\n{err or 'No output'}\n```"
        return out
    except subprocess.TimeoutExpired:
        return "⏱ Scan timed out after 5 minutes."
    except Exception as e:
        return f"⚠ Error: {e}"

if __name__ == "__main__":
    input_str = sys.argv[1] if len(sys.argv) > 1 else ""
    print(run_scan(input_str))
