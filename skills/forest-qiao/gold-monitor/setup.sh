#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Check python3
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required but not found. Please install Python 3.8+."
  exit 1
fi

# Check pip
if ! python3 -m pip --version &>/dev/null; then
  echo "ERROR: pip is required but not found. Please install pip."
  exit 1
fi

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet

echo "Starting gold-monitor on http://127.0.0.1:8000 ..."
exec python3 app.py
