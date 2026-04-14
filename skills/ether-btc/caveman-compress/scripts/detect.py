#!/usr/bin/env python3
"""File type detection for caveman-compress."""

import sys
from pathlib import Path


def is_backup_file(path: str) -> bool:
    """Check if path is a backup file (.original.md)."""
    return Path(path).name.endswith(".original.md")


def is_markdown_file(path: str) -> bool:
    """Check if path is a markdown file."""
    return Path(path).suffix == ".md"


def is_workspace_file(path: str) -> bool:
    """Check if path is a workspace file (vs results/)."""
    abs_path = Path(path).resolve()
    workspace = Path.home() / ".openclaw" / "workspace"
    try:
        abs_path.relative_to(workspace)
        return True
    except ValueError:
        return False


def is_safe_to_compress(path: str) -> bool:
    """Check if file is safe to compress (not results/, not backup)."""
    return (
        is_markdown_file(path)
        and not is_backup_file(path)
        and is_workspace_file(path)
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: detect.py <filepath>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not is_safe_to_compress(filepath):
        print(f"⚠️  File not safe to compress: {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Safe to compress: {filepath}")
