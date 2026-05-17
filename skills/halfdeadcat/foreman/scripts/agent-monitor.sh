#!/usr/bin/env bash
# agent-monitor.sh — Foreman agent-task monitor
# Scans ~/.openclaw/workspace/.foreman/*.json for active tasks
# Sends Slack alerts for active/stale tasks, cleans up old completed tasks
# Runs every 2 min via cron

export PATH="/home/swabby/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

FOREMAN_DIR="${HOME}/.openclaw/workspace/.foreman"
STALE_THRESHOLD_MIN="${STALE_THRESHOLD_MIN:-10}"
CLEANUP_THRESHOLD_MIN="${CLEANUP_THRESHOLD_MIN:-60}"
SLACK_TARGET="${FOREMAN_ALERT_TARGET:-U0AM4BLBUUW}"
SLACK_CHANNEL="${FOREMAN_ALERT_CHANNEL:-slack}"
LOCK_FILE="/tmp/agent-monitor.lock"
STATE_FILE="/tmp/agent-monitor-state.json"

# Prevent overlapping runs
if [ -f "$LOCK_FILE" ]; then
    pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        echo "agent-monitor already running (pid=$pid), exiting"
        exit 0
    fi
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# Initialize state file if missing
if [ ! -f "$STATE_FILE" ]; then
    echo '{"alerted":{}}' > "$STATE_FILE"
fi

mkdir -p "$FOREMAN_DIR"

now=$(date +%s)

_alert() {
    local msg="$1"
    openclaw message send \
        --channel "$SLACK_CHANNEL" \
        --target "$SLACK_TARGET" \
        -m "$msg" 2>/dev/null || true
}

# Load stale-alert state (prevents re-alerting same task repeatedly)
_get_alerted() {
    python3 -c "
import json, sys
try:
    d = json.load(open('$STATE_FILE'))
    print(json.dumps(d.get('alerted', {})))
except:
    print('{}')
" 2>/dev/null || echo '{}'
}

_save_alerted() {
    local new_alerted="$1"
    python3 -c "
import json
state = {'alerted': json.loads('''$new_alerted''')}
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f)
" 2>/dev/null || true
}

alerted=$(_get_alerted)
new_alerted="$alerted"

for f in "$FOREMAN_DIR"/*.json; do
    [ -f "$f" ] || continue

    # Parse fields safely
    fields=$(python3 -c "
import json, sys, os
try:
    d = json.load(open('$f'))
    print(d.get('run_id','unknown'))
    print(d.get('label','unknown'))
    print(d.get('status','unknown'))
    print(d.get('step',''))
    print(d.get('progress',0))
    print(d.get('updated',''))
except Exception as e:
    print('unknown'); print('unknown'); print('unknown'); print(''); print(0); print('')
" 2>/dev/null) || continue

    run_id=$(echo "$fields" | sed -n '1p')
    label=$(echo "$fields" | sed -n '2p')
    status=$(echo "$fields" | sed -n '3p')
    step=$(echo "$fields" | sed -n '4p')
    progress=$(echo "$fields" | sed -n '5p')
    updated=$(echo "$fields" | sed -n '6p')

    # Convert ISO-8601 updated to epoch
    if [ -n "$updated" ]; then
        updated_epoch=$(python3 -c "
from datetime import datetime, timezone
ts = '$updated'.replace('Z', '+00:00')
try:
    dt = datetime.fromisoformat(ts)
    print(int(dt.timestamp()))
except:
    import os
    print(int(os.path.getmtime('$f')))
" 2>/dev/null) || updated_epoch=$(stat -c %Y "$f" 2>/dev/null || echo "$now")
    else
        updated_epoch=$(stat -c %Y "$f" 2>/dev/null || echo "$now")
    fi

    age_min=$(( (now - updated_epoch) / 60 ))

    if [ "$status" = "done" ] || [ "$status" = "error" ] || [ "$status" = "completed" ]; then
        # Clean up completed/errored tasks older than threshold
        if [ "$age_min" -ge "$CLEANUP_THRESHOLD_MIN" ]; then
            echo "Cleaning up old task: $label ($run_id) status=$status age=${age_min}min"
            rm -f "$f"
        fi
        continue
    fi

    # Active task (starting, running, blocked)
    stale_key="${run_id}_stale"
    already_stale_alerted=$(python3 -c "
import json
d = json.loads('''$alerted''')
print('yes' if '$stale_key' in d else 'no')
" 2>/dev/null || echo "no")

    if [ "$age_min" -ge "$STALE_THRESHOLD_MIN" ] && [ "$already_stale_alerted" = "no" ]; then
        # Send stale alert (once per task)
        msg="⚠️ [${label}]: STALE — ${status} - ${step} (${progress}%) — no update for ${age_min}min"
        echo "Sending stale alert: $msg"
        _alert "$msg"
        # Mark as alerted in new state
        new_alerted=$(python3 -c "
import json
d = json.loads('''$new_alerted''')
d['$stale_key'] = $now
print(json.dumps(d))
" 2>/dev/null || echo "$new_alerted")
    elif [ "$age_min" -lt 2 ]; then
        # Recently updated — send normal status (only if fresh)
        msg="🤖 [${label}]: ${status} - ${step} (${progress}%)"
        echo "Sending status: $msg"
        _alert "$msg"
    else
        echo "Task $label: status=$status age=${age_min}min (no alert needed)"
    fi
done

# Persist updated alert state
_save_alerted "$new_alerted"

echo "agent-monitor done at $(date)"
