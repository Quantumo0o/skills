#!/usr/bin/env bash
# foreman-status.sh — Show status of all active work: shell jobs and agent tasks

AGENT_STATUS_DIR="${HOME}/.openclaw/workspace/.foreman"
JOBS_DIR="${JOBS_DIR:-/tmp/swabby-jobs}"

shown_any=0

# ── Section 1: Shell Jobs ─────────────────────────────────────────────────────
if [ -d "$JOBS_DIR" ] && [ -n "$(ls -A "$JOBS_DIR"/*.json 2>/dev/null)" ]; then
    echo "── Shell Jobs ────────────────────────────────────────────────────────"
    printf "%-24s %-5s  %-10s  %s\n" "LABEL" "PID" "ELAPSED" "PROGRESS"
    printf "%-24s %-5s  %-10s  %s\n" "----" "---" "-------" "--------"
    for f in "$JOBS_DIR"/*.json; do
        [ -f "$f" ] || continue
        python3 -c "
import json, time, os, sys
d = json.load(open('$f'))
label = d.get('label', '?')[:24]
pid = str(d.get('pid', '?'))
started = d.get('started', int(time.time()))
elapsed = int(time.time()) - started
em = elapsed // 60; es = elapsed % 60
elapsed_str = f'{em}m {es}s'
progress = str(d.get('progress', '...'))[:60]
print(f'{label:<24s} {pid:<5s}  {elapsed_str:<10s}  {progress}')
"
        shown_any=1
    done
    echo
fi

# ── Section 2: Agent Task Status Files ────────────────────────────────────────
if [ -d "$AGENT_STATUS_DIR" ] && [ -n "$(ls -A "$AGENT_STATUS_DIR"/*.json 2>/dev/null)" ]; then
    echo "── Agent Tasks ───────────────────────────────────────────────────────"
    printf "%-20s %-10s %5s  %s\n" "LABEL" "STATUS" "PCT" "STEP"
    printf "%-20s %-10s %5s  %s\n" "----" "------" "---" "----"
    for f in "$AGENT_STATUS_DIR"/*.json; do
        [ -f "$f" ] || continue
        python3 -c "
import json, sys
d = json.load(open('$f'))
label = d.get('label','?')[:20]
status = d.get('status','?')
pct = d.get('progress', 0)
pct_str = str(pct) if isinstance(pct, int) else '?'
step = d.get('step','')[:60]
q = d.get('question')
err = d.get('error')
extra = ''
if q: extra = f' ⚠️  Q: {q[:40]}'
if err: extra = f' ❌ {err[:40]}'
print(f'{label:<20s} {status:<10s} {pct_str:>3s}%  {step}{extra}')
"
        shown_any=1
    done
    echo
fi

if [ "$shown_any" -eq 0 ]; then
    echo "No active work (no shell jobs, no agent tasks)."
fi
