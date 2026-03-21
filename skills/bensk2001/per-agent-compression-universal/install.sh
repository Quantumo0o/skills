#!/bin/bash
# Per-Agent Memory Compression Skill - Universal Installer v1.3.2
# Auto-discovers agents and registers compression tasks with full feature set

set -e

echo "🎯 Installing Per-Agent Memory Compression Skill (Universal) v1.2.1"
echo ""

# 1. Pre-checks
echo "🔍 Running pre-installation checks..."

if ! command -v openclaw &> /dev/null; then
  echo "❌ openclaw CLI not found in PATH"
  exit 1
fi

if ! openclaw agents list --json &> /dev/null; then
  echo "❌ openclaw agents list failed - is Gateway running?"
  exit 1
fi

echo "✅ Pre-checks passed"
echo ""

# 2. Discover agents with workspaces
AGENTS_JSON=$(openclaw agents list --json 2>&1)

AGENTS=$(echo "$AGENTS_JSON" | jq -r '.[] | select(.workspace != null) | "\(.id)=\(.workspace)"' 2>/dev/null)
if [ -z "$AGENTS" ]; then
  echo "❌ No agents with workspace found"
  exit 1
fi

echo "📋 Discovered agents:"
echo "$AGENTS" | while IFS='=' read -r id ws; do
  echo "  ✅ $id → $ws"
done
echo ""

# 3. Define domain context for known agents
declare -A DOMAIN_CONTEXT
DOMAIN_CONTEXT[main]="general (main agent - overall user context)"
DOMAIN_CONTEXT[hrbp]="HR/work-related (hrbp agent - professional, career, organizational development)"
DOMAIN_CONTEXT[parenting]="Parenting/family (parenting agent - children, education, family dynamics)"
DOMAIN_CONTEXT[decoration]="Renovation/decoration (decoration agent - construction, materials, project management)"
# Default for unknown agents
DOMAIN_CONTEXT[default]="agent-specific (adapt based on agent's identity and role)"

# 4. Staggered schedule offsets (minutes from 03:00 Sunday)
OFFSETS=(0 30 60 90 120 150 180 210 240 270)

INDEX=0
TASK_IDS=()
echo "$AGENTS" | while IFS='=' read -r agent_id workspace; do
  OFFSET=${OFFSETS[$INDEX]}
  INDEX=$((INDEX + 1))
  
  HOUR=$((3 + OFFSET / 60))
  MINUTE=$((OFFSET % 60))
  CRON="${MINUTE} ${HOUR} * * 0"
  
  TASK_NAME="per_agent_compression_${agent_id}"
  
  # Check if task exists
  if openclaw cron list --json 2>/dev/null | jq -e --arg name "$TASK_NAME" '.jobs[] | select(.name == $name)' >/dev/null; then
    echo "  ⚠️  Task $TASK_NAME already exists, skipping"
    continue
  fi
  
  echo "  📝 Creating: $TASK_NAME ($CRON)"
  
  # Determine domain context
  DOMAIN="${DOMAIN_CONTEXT[$agent_id]:-$DOMAIN_CONTEXT[default]}"
  
  # Two-step message setting to bypass CLI length limit
  # MSG_SHORT: concise but includes all essential logic (~500 chars)
  # MSG_FULL: complete reference (used via edit after add)
  MSG_SHORT="AUTONOMOUS: Weekly per-agent memory consolidation for '$agent_id'.\n\nWorkspace: $workspace\nDAILY_NOTES_DIR: {WORKSPACE}/memory\nPROCESSED_DIR: {WORKSPACE}/memory/processed\nSTATE_FILE: {WORKSPACE}/memory/.compression_state.json\nTARGET_FILES: USER.md, IDENTITY.md, SOUL.md, MEMORY.md\n\nDOMAIN_CONTEXT: \"$DOMAIN\"\n\nEXECUTION:\n1) Pre-check paths; init state\n2) List YYYY-MM-DD.md (<7d, not processed), sort oldest, limit 5\n3) For each: read, extract factual info, dedupe (same date), append to targets with date header (### [YYYY-MM-DD])\n4) Move to processed/, update state\n5) Announce summary (processed, remaining)\n\nIMPORTANT: Extract ONLY factual/explicit info. Append only. Continue on error. Full spec in README.\n\nExecute without waiting."
  
  MSG_FULL="AUTONOMOUS: Weekly per-agent memory consolidation for '$agent_id'.\n\nWorkspace: $workspace\nDAILY_NOTES_DIR: {WORKSPACE}/memory\nPROCESSED_DIR: {WORKSPACE}/memory/processed\nSTATE_FILE: {WORKSPACE}/memory/.compression_state.json\nTARGET_FILES: USER.md, IDENTITY.md, SOUL.md, MEMORY.md\n\nDOMAIN_CONTEXT: \"$DOMAIN\"\n\nEXECUTION PLAN:\n1) Pre-check paths (workspace, memory/, targets)\n2) Load/init state (JSON: last_compressed_date, processed_notes set)\n3) List daily notes: memory/YYYY-MM-DD.md, date < today-7, not in processed_notes\n4) Sort by date (oldest first), limit to 5 notes per run\n5) For each note:\n   - Read note content\n   - Extract: preferences, decisions, personal info, facts\n   - Dedupe: if same date already in target, skip\n   - Append to targets:\n     * USER.md → under \"## Personal Info / Preferences\", header \"### [YYYY-MM-DD]\"\n     * IDENTITY.md → under \"## Notes\" (create if missing), header \"### [YYYY-MM-DD]\"\n     * SOUL.md → under \"## Principles\" or \"## Boundaries\" (contextual), header \"### [YYYY-MM-DD]\"\n     * MEMORY.md → under \"## Key Learnings\" (create if missing), format \"- [YYYY-MM-DD] <summary>\"\n6) Move processed note to memory/processed/ (create dir if needed)\n7) Update state: add note date to processed_notes, update last_compressed_date\n8) Save state file (JSON)\n9) Clean working buffer if needed\n10) Announce summary: processed count, remaining old notes count\n\nIMPORTANT:\n- Extract ONLY factual/explicit info from notes\n- Append only; never modify existing content\n- Continue on error (log and proceed to next note)\n- See skill README for full details and troubleshooting\n\nExecute without waiting."
  
  if openclaw cron add \
    --name "$TASK_NAME" \
    --cron "$CRON" \
    --tz "Asia/Shanghai" \
    --agent "main" \
    --message "$MSG_SHORT" \
    --timeout 1200 \
    --session "isolated" \
    --announce 2>&1; then
    
    # Get the job ID of the just-created task
    JOB_ID=$(openclaw cron list --json 2>&1 | jq -r --arg name "$TASK_NAME" '.jobs[] | select(.name == $name) | .id')
    
    if [ -n "$JOB_ID" ]; then
      echo "  ✨ Enriching task with full execution plan (job ID: ${JOB_ID:0:8}...)"
      if openclaw cron edit "$JOB_ID" --message "$MSG_FULL" 2>&1; then
        echo "  ✅ Task enriched"
      else
        echo "  ⚠️  Warning: Failed to enrich task message. Task may lack full details. Check README for complete spec."
      fi
    else
      echo "  ⚠️  Warning: Could not retrieve job ID for enrichment."
    fi
    
    TASK_IDS+=("$TASK_NAME")
  else
    echo "    ❌ Failed to create task $TASK_NAME"
  fi
done

echo ""
echo "✅ Installation complete!"
echo ""
if [ ${#TASK_IDS[@]} -gt 0 ]; then
  echo "📋 Created ${#TASK_IDS[@]} task(s):"
  for tid in "${TASK_IDS[@]}"; do
    echo "   - $tid"
  done
  echo ""
  echo "💡 Note: Task messages are concise but contain all essential logic."
  echo "💡 For full execution plan details, see: /root/.openclaw/workspace/skills/per-agent-compression-universal/README.md"
  echo "💡 Verify: openclaw cron list | grep per_agent_compression"
  echo "💡 Uninstall: ./uninstall.sh"
else
  echo "⚠️  No new tasks were created (all may already exist)"
fi
