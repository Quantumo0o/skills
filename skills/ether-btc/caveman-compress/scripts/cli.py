#!/usr/bin/env python3
"""CLI entrypoint for caveman-compress skill."""

import sys
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: caveman-compress <filepath> [--dry-run]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    # Import and run
    sys.path.insert(0, str(Path(__file__).parent))
    from compress import compress

    try:
        compress(filepath, dry_run=dry_run)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
