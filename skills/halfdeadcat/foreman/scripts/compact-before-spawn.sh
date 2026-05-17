#!/usr/bin/env bash
# compact-before-spawn.sh — Compact the current session before spawning a sub-agent.
#
# Detects which gateway the current session lives in, checks line count,
# and trims the session transcript if above threshold. Then reloads the
# session via the Chat Completions API so the gateway picks up the compacted file.
#
# Usage:
#   bash skills/foreman/scripts/compact-before-spawn.sh <session-key>
#
# Example:
#   bash skills/foreman/scripts/compact-before-spawn.sh "agent:main:slack:direct:u0am4blbuuw"
#
# Exit codes:
#   0 — compaction performed (or not needed)
#   1 — error (session not found, trim failed, etc.)

set -euo pipefail

export PATH="/home/swabby/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export XDG_RUNTIME_DIR="/run/user/$(id -u)"

SESSION_KEY="${1:-}"
MEMORY_DIR="$HOME/repos/swabby-brain/memory/private"
STATE_FILE="$HOME/.openclaw/transcript-maintenance-state.json"
KEEP_PAIRS=8           # Keep last 8 user/assistant exchange pairs after compaction
MIN_LINES=20           # Only compact if session is longer than this

log() { echo "[compact-before-spawn] $*" >&2; }

if [[ -z "$SESSION_KEY" ]]; then
    log "ERROR: session key required as first argument"
    exit 1
fi

# --- Determine gateway from session key ---
if [[ "$SESSION_KEY" == *":slack:"* ]]; then
    GATEWAY="slack"
    SESSIONS_DIR="$HOME/.openclaw-slack/agents/main/sessions"
    PORT=18789
    TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw-slack/openclaw.json')).get('gateway',{}).get('auth',{}).get('token',''))" 2>/dev/null)
elif [[ "$SESSION_KEY" == *":discord:"* ]]; then
    GATEWAY="discord"
    SESSIONS_DIR="$HOME/.openclaw-discord/agents/main/sessions"
    PORT=18790
    TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw-discord/openclaw.json')).get('gateway',{}).get('auth',{}).get('token',''))" 2>/dev/null)
else
    log "ERROR: cannot determine gateway from session key: $SESSION_KEY"
    exit 1
fi

# --- Find session JSONL file ---
# Session ID is stored in sessions.json, keyed by session key
SESSION_ID=$(python3 -c "
import json, sys
try:
    d = json.load(open('$SESSIONS_DIR/sessions.json'))
    sess = d.get('sessions', d)
    entry = sess.get('$SESSION_KEY', {})
    print(entry.get('sessionId', ''))
except Exception as e:
    print('', file=sys.stderr)
" 2>/dev/null)

if [[ -z "$SESSION_ID" ]]; then
    log "ERROR: session ID not found for key: $SESSION_KEY"
    exit 1
fi

JSONL_FILE="$SESSIONS_DIR/${SESSION_ID}.jsonl"

if [[ ! -f "$JSONL_FILE" ]]; then
    log "ERROR: session JSONL not found: $JSONL_FILE"
    exit 1
fi

LINE_COUNT=$(wc -l < "$JSONL_FILE")
SIZE_KB=$(( $(stat -c%s "$JSONL_FILE" 2>/dev/null || echo 0) / 1024 ))

log "Session: $SESSION_KEY → $SESSION_ID"
log "Lines: $LINE_COUNT | Size: ${SIZE_KB}KB"

if (( LINE_COUNT <= MIN_LINES )); then
    log "Session is small ($LINE_COUNT lines) — no compaction needed"
    exit 0
fi

log "Compacting: trimming to last $KEEP_PAIRS exchange pairs..."

# Run transcript-trim.py
if python3 /home/swabby/bin/transcript-trim.py \
    "$JSONL_FILE" "$SESSION_ID" "$GATEWAY" "$MEMORY_DIR" "$STATE_FILE" "$KEEP_PAIRS" 2>&1; then
    log "Trim successful"
else
    TRIM_EXIT=$?
    if [[ $TRIM_EXIT -eq 1 ]]; then
        log "Trim skipped (file already small or clean)"
        exit 0
    fi
    log "ERROR: trim failed with exit code $TRIM_EXIT"
    exit 1
fi

# --- Reload session in gateway ---
log "Reloading session in $GATEWAY gateway..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "http://127.0.0.1:${PORT}/v1/chat/completions" \
    -H "Authorization: Bearer $TOKEN" \
    -H "x-openclaw-session-key: $SESSION_KEY" \
    -H "Content-Type: application/json" \
    --max-time 10 \
    -d '{
      "model": "openclaw",
      "messages": [{"role": "user", "content": "[session compacted before sub-agent spawn]"}],
      "stream": false
    }' 2>/dev/null || echo "000")

if [[ "$HTTP_CODE" == "200" ]] || [[ "$HTTP_CODE" == "201" ]]; then
    log "Session reloaded successfully (HTTP $HTTP_CODE)"
elif [[ "$HTTP_CODE" == "000" ]]; then
    log "WARNING: reload request timed out or failed — gateway will reload on next turn"
else
    log "WARNING: reload returned HTTP $HTTP_CODE — gateway will reload on next turn"
fi

log "Compaction complete. Session ready for sub-agent spawn."
exit 0
