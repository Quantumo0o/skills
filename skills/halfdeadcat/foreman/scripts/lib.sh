#!/bin/bash
# foreman/scripts/lib.sh — Shared job lifecycle functions
# Source this in every job wrapper: source "$(dirname "$0")/lib.sh"
export PATH="${HOME}/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

JOBS_DIR="${JOBS_DIR:-/tmp/swabby-jobs}"

# Alerting — configurable via env vars, backward-compatible with SLACK_TO/SLACK_CHANNEL
FOREMAN_ALERT_TARGET="${FOREMAN_ALERT_TARGET:-${SLACK_TO:-}}"
FOREMAN_ALERT_CHANNEL="${FOREMAN_ALERT_CHANNEL:-${SLACK_CHANNEL:-slack}}"

# Initialize a job. Call at top of wrapper before launching work.
# Usage: job_init <job_id> <label>
job_init() {
    local job_id="$1"
    local label="$2"
    mkdir -p "$JOBS_DIR"
    cat > "$JOBS_DIR/$job_id.json" <<EOF
{
  "job_id": "$job_id",
  "label": "$label",
  "pid": $$,
  "started": $(date +%s),
  "progress": "Starting...",
  "last_update": $(date +%s)
}
EOF
    echo $$ > "$JOBS_DIR/$job_id.pid"
}

# Update progress message (optional — call from within job logic)
# Usage: job_progress <job_id> "message"
job_progress() {
    local job_id="$1"
    local msg="$2"
    local f="$JOBS_DIR/$job_id.json"
    [ -f "$f" ] || return
    python3 -c "
import json, sys, time
d = json.load(open('$f'))
d['progress'] = sys.argv[1]
d['last_update'] = int(time.time())
json.dump(d, open('$f','w'), indent=2)
" "$msg"
}

# Register the 5-min monitor cron for this job.
# Usage: job_register_cron <job_id>
job_register_cron() {
    local job_id="$1"
    local monitor
    monitor="$(dirname "${BASH_SOURCE[0]}")/monitor.sh"
    # Lock to prevent race when multiple jobs register simultaneously
    local lockfile="/tmp/swabby-jobs-cron.lock"
    (
        flock -w 10 200 || { echo "cron lock timeout for $job_id" >&2; return 1; }
        crontab -l 2>/dev/null | grep -v "monitor.sh $job_id" | \
        { cat; echo "*/5 * * * * $monitor $job_id"; } | crontab -
    ) 200>"$lockfile"
}

# Remove the monitor cron for this job.
# Usage: job_deregister_cron <job_id>
job_deregister_cron() {
    local job_id="$1"
    local monitor
    monitor="$(dirname "${BASH_SOURCE[0]}")/monitor.sh"
    local lockfile="/tmp/swabby-jobs-cron.lock"
    (
        flock -w 10 200 || { echo "cron lock timeout for $job_id" >&2; return 1; }
        crontab -l 2>/dev/null | grep -v "monitor.sh $job_id" | crontab -
    ) 200>"$lockfile"
}

# Set up EXIT trap. Call after job_init and job_register_cron.
# Usage: job_trap <job_id>
job_trap() {
    local job_id="$1"
    trap "_job_on_exit $job_id \$?" EXIT
}

_job_on_exit() {
    local job_id="$1"
    local exit_code="$2"
    local f="$JOBS_DIR/$job_id.json"
    local label="$job_id"
    [ -f "$f" ] && label=$(python3 -c "import json; print(json.load(open('$f'))['label'])" 2>/dev/null || echo "$job_id")

    if [ "$exit_code" -eq 0 ]; then
        _job_slack "✅ *$label* — done"
    else
        _job_slack "❌ *$label* — failed (exit $exit_code)"
    fi

    job_deregister_cron "$job_id"
    rm -f "$JOBS_DIR/$job_id.pid" "$JOBS_DIR/$job_id.json"
}

_job_slack() {
    openclaw message send \
        --channel "$FOREMAN_ALERT_CHANNEL" \
        --target "$FOREMAN_ALERT_TARGET" \
        -m "$1" 2>/dev/null || true
}
