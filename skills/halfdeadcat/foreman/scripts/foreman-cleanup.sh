#!/usr/bin/env bash
# Clean up completed foreman worker status files
STATUS_DIR="${HOME}/.openclaw/workspace/.foreman"

if [ ! -d "$STATUS_DIR" ]; then
  echo "No foreman status directory."
  exit 0
fi

cleaned=0
for f in "$STATUS_DIR"/*.json; do
  [ -f "$f" ] || continue
  status=$(python3 -c "import json; print(json.load(open('$f')).get('status',''))" 2>/dev/null)
  if [ "$status" = "done" ] || [ "$status" = "error" ]; then
    rm "$f"
    cleaned=$((cleaned + 1))
  fi
done

echo "Cleaned $cleaned completed worker(s)."
