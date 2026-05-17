#!/bin/bash
# foreman/scripts/monitor.sh — Generic 5-min heartbeat for any shell job
export PATH="${HOME}/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
# Invoked by cron: monitor.sh <job_id>
# Reads status file at $JOBS_DIR/<job_id>.json

JOBS_DIR="${JOBS_DIR:-/tmp/swabby-jobs}"

# Alerting — configurable via env vars, backward-compatible with SLACK_TO/SLACK_CHANNEL
FOREMAN_ALERT_TARGET="${FOREMAN_ALERT_TARGET:-${SLACK_TO:-}}"
FOREMAN_ALERT_CHANNEL="${FOREMAN_ALERT_CHANNEL:-${SLACK_CHANNEL:-slack}}"

job_id="$1"
[ -z "$job_id" ] && exit 1

pid_file="$JOBS_DIR/$job_id.pid"
json_file="$JOBS_DIR/$job_id.json"

_alert() {
    openclaw message send \
        --channel "$FOREMAN_ALERT_CHANNEL" \
        --target "$FOREMAN_ALERT_TARGET" \
        -m "$1" 2>/dev/null || true
}

# If PID file is gone, job already exited cleanly — remove our cron and quit
if [ ! -f "$pid_file" ]; then
    monitor="$(dirname "$0")/monitor.sh"
    crontab -l 2>/dev/null | grep -v "monitor.sh $job_id" | crontab -
    exit 0
fi

pid=$(cat "$pid_file")

# Process still alive?
if ! kill -0 "$pid" 2>/dev/null; then
    # Dead but cleanup didn't run (crash) — alert and remove cron
    _alert "⚠️ *$job_id* — process $pid died unexpectedly (no clean exit)"
    monitor="$(dirname "$0")/monitor.sh"
    crontab -l 2>/dev/null | grep -v "monitor.sh $job_id" | crontab -
    rm -f "$pid_file" "$json_file"
    exit 0
fi

# Still alive — read status and report
if [ -f "$json_file" ]; then
    label=$(python3 -c "import json; d=json.load(open('$json_file')); print(d.get('label', '$job_id'))" 2>/dev/null || echo "$job_id")
    progress=$(python3 -c "import json; d=json.load(open('$json_file')); print(d.get('progress', '...'))" 2>/dev/null || echo "...")
    started=$(python3 -c "import json,time; d=json.load(open('$json_file')); elapsed=int(time.time())-d['started']; print(f'{elapsed//60}m {elapsed%60}s')" 2>/dev/null || echo "?")
    _alert "⏳ *$label* — $progress (running ${started})"
else
    _alert "⏳ *$job_id* — still running (pid $pid)"
fi
