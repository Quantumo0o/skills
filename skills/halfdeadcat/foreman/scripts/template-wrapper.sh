#!/bin/bash
# template-wrapper.sh — Copy and adapt for new jobs
# 1. Set JOB_ID (unique, slug-style) and LABEL (human-readable)
# 2. Replace the "do_the_work" section with your actual job logic
# 3. Call job_progress anywhere to update the Slack heartbeat message

source "$(dirname "$0")/lib.sh"

JOB_ID="example-job-$(date +%s)"
LABEL="Example Job"

job_init "$JOB_ID" "$LABEL"
job_register_cron "$JOB_ID"
job_trap "$JOB_ID"

# ── your job logic below ─────────────────────────────────────────────────────

job_progress "$JOB_ID" "Phase 1 of 3"
sleep 10  # replace with real work

job_progress "$JOB_ID" "Phase 2 of 3"
sleep 10

job_progress "$JOB_ID" "Phase 3 of 3"
sleep 10

# ── end job logic ─────────────────────────────────────────────────────────────
# EXIT trap fires here automatically — sends ✅/❌ and removes cron
