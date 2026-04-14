#!/usr/bin/env python3
"""Caveman compression orchestrator - MiniMax/DeepSeek fallback via subprocess + curl."""

import os
import sys
import json
import subprocess
from pathlib import Path

# Constants
MAX_FILE_SIZE = 500 * 1024  # 500KB


def read_file(path: str) -> str:
    """Read file content, raise if too large."""
    file_path = Path(path)
    if file_path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {file_path.stat().st_size} > {MAX_FILE_SIZE}")
    return file_path.read_text(encoding="utf-8")


def write_backup(path: str, content: str):
    """Write .original.md backup using atomic exclusive creation."""
    backup_path = Path(path).with_suffix(".md.original")
    try:
        backup_fd = os.open(str(backup_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        with os.fdopen(backup_fd, 'w') as f:
            f.write(content)
        print(f"✓ Backup created: {backup_path}")
    except FileExistsError:
        raise FileExistsError(f"Backup already exists: {backup_path}")


def compress_via_claude(content: str) -> str:
    """Primary: use claude CLI (desktop auth)."""
    prompt = f"""Compress this text into caveman-speak (~45% shorter). Keep all technical accuracy, code blocks, URLs, file paths exact. Drop articles, filler, hedging. Keep key substance.

Text:
{content}

Output only compressed text, no intro/outro."""

    try:
        result = subprocess.run(
            ["claude", "--print", prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def compress_via_openai_compat(
    base_url: str, api_key: str, model: str, content: str
) -> str | None:
    """Fallback: OpenAI-compatible endpoint via curl."""
    endpoint = f"{base_url.rstrip('/')}/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Compress text into caveman-speak (~45% shorter). Keep technical accuracy, code blocks, URLs, file paths exact. Drop articles, filler, hedging. Output only compressed text.",
            },
            {"role": "user", "content": content[:10000]},  # Limit context
        ],
        "max_tokens": 8000,
    }

    try:
        result = subprocess.run(
            [
                "curl",
                "-s",
                "-X",
                "POST",
                endpoint,
                "-H",
                f"Authorization: Bearer {api_key}",
                "-H",
                "Content-Type: application/json",
                "-d",
                json.dumps(payload),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            response = json.loads(result.stdout)
            return response["choices"][0]["message"]["content"].strip()
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as e:
        provider = base_url.split("//")[1].split(".")[0] if "//" in base_url else base_url
        print(f"[WARN] {provider} failed: {type(e).__name__} — {e}")
    return None


def compress(content: str, dry_run: bool = False) -> str:
    """Compress content via fallback chain."""
    if dry_run:
        print("[DRY RUN] Would compress via: claude → MiniMax → DeepSeek")
        return content

    # Try claude CLI first
    compressed = compress_via_claude(content)
    if compressed:
        print("✓ Compressed via claude CLI")
        return compressed

    # Try MiniMax
    minimax_url = os.environ.get("MINIMAX_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "http://127.0.0.1:8402"
    minimax_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if minimax_url and minimax_key:
        model = os.environ.get("COMPRESSION_MODEL", "MiniMax-M2.7")
        compressed = compress_via_openai_compat(
            minimax_url, minimax_key, model, content
        )
        if compressed:
            print(f"✓ Compressed via MiniMax ({model})")
            return compressed

    # Try DeepSeek
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    if deepseek_key:
        model = os.environ.get("COMPRESSION_MODEL", "deepseek-v3")
        compressed = compress_via_openai_compat(
            "https://api.deepseek.com", deepseek_key, model, content
        )
        if compressed:
            print(f"✓ Compressed via DeepSeek ({model})")
            return compressed

    raise RuntimeError("All compression methods failed (no API available)")


def main():
    if len(sys.argv) < 2:
        print("Usage: compress.py <filepath> [--dry-run]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    # Check feature flags
    if "AGENTS.md" in filepath and not os.environ.get("CAVEMAN_COMPRESS_AGENTS"):
        print("⚠️  AGENTS.md compression disabled (set CAVEMAN_COMPRESS_AGENTS=1)")
        sys.exit(0)
    if "HEARTBEAT.md" in filepath and not os.environ.get("CAVEMAN_COMPRESS_HEARTBEAT"):
        print("⚠️  HEARTBEAT.md compression disabled (set CAVEMAN_COMPRESS_HEARTBEAT=1)")
        sys.exit(0)
    if "MEMORY.md" in filepath and not os.environ.get("CAVEMAN_COMPRESS_MEMORY"):
        print("⚠️  MEMORY.md compression disabled (set CAVEMAN_COMPRESS_MEMORY=1)")
        sys.exit(0)

    try:
        content = read_file(filepath)
        compressed = compress(content, dry_run=dry_run)

        if not dry_run:
            if not is_technically_intact(content, compressed):
                print("[ERROR] Validation failed — compression may have lost content")
                return
            write_backup(filepath, content)
            Path(filepath).write_text(compressed, encoding="utf-8")
            print(f"✓ Compressed: {filepath}")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
