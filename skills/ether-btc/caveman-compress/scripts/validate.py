#!/usr/bin/env python3
"""Structural validators for caveman-compressed output."""

import re
from pathlib import Path


def has_code_blocks(text: str) -> bool:
    """Check if text contains code blocks."""
    return "```" in text


def has_urls(text: str) -> bool:
    """Check if text contains URLs."""
    return bool(re.search(r"https?://\S+", text))


def has_inline_code(text: str) -> bool:
    """Check if text contains inline code."""
    return "`" in text


def has_file_paths(text: str) -> bool:
    """Check if text contains file paths."""
    return bool(re.search(r"~?/[\w/.\-]+", text))


def is_technically_intact(original: str, compressed: str) -> bool:
    """Verify technical substance preserved. Returns True if intact, False otherwise."""
    checks = [
        ("code blocks", has_code_blocks(original) == has_code_blocks(compressed)),
        ("URLs", has_urls(original) == has_urls(compressed)),
        ("inline code", has_inline_code(original) == has_inline_code(compressed)),
        ("file paths", has_file_paths(original) == has_file_paths(compressed)),
    ]

    failed = [name for name, passed in checks if not passed]
    if failed:
        print(f"⚠️  Validation failed: {', '.join(failed)}", file=sys.stderr)
        return False
    return True


def is_caveman_compressed(text: str) -> bool:
    """Check if text looks compressed (heuristic). Returns True if compressed, False otherwise."""
    article_count = len(re.findall(r"\b(a|an|the)\b", text.lower()))
    word_count = len(text.split())
    ratio = article_count / max(word_count, 1)
    return ratio < 0.05  # Less than 5% articles


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: validate.py <original> <compressed>", file=sys.stderr)
        sys.exit(1)

    original = Path(sys.argv[1]).read_text(encoding="utf-8")
    compressed = Path(sys.argv[2]).read_text(encoding="utf-8")

    intact = is_technically_intact(original, compressed)
    if not intact:
        sys.exit(1)

    compressed_ok = is_caveman_compressed(compressed)
    if not compressed_ok:
        print("⚠️  Output doesn't look compressed (high article ratio)", file=sys.stderr)
        sys.exit(1)

    print("✓ Validation passed")
