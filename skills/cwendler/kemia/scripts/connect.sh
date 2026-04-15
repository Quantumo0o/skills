#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# kemia connect — Register this OpenClaw instance via enrollment flow
#
# Usage: connect.sh <kemia-url>
#
# Flow:
#   1. POST /api/v1/enroll → get enrollment URL
#   2. Show enrollment URL to user (user clicks to confirm)
#   3. Poll /api/v1/enroll/:code/status until completed → receive API key
#   4. Export agent config files to kemia
# =============================================================================

KEMIA_URL="${1:?Usage: connect.sh <kemia-url>}"
KEMIA_URL="${KEMIA_URL%/}"

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="${WORKSPACE}/skills/kemia"
CONFIG_FILE="${SKILL_DIR}/config.json"
INSTANCE_NAME="${OPENCLAW_INSTANCE_NAME:-$(hostname)}"

# Require jq
command -v jq &>/dev/null || { echo "ERROR: jq is required. Install with: apt-get install jq"; exit 1; }

# Check for existing connection
if [ -f "${CONFIG_FILE}" ]; then
  EXISTING_URL=$(jq -r '.baseUrl // empty' "${CONFIG_FILE}")
  echo "WARNING: Already connected to kemia (${EXISTING_URL})."
  echo "Re-connecting will create a new instance and API key."
  read -rp "Continue? (y/N) " confirm
  [[ "${confirm}" =~ ^[Yy]$ ]] || exit 0
fi

# ---- Step 1: Start enrollment ----
echo "Starting enrollment with ${KEMIA_URL}..."
ENROLL_RESPONSE=$(curl -sf \
  -X POST \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg name "${INSTANCE_NAME}" '{name: $name, orchestrator: "openclaw"}')" \
  "${KEMIA_URL}/api/v1/enroll") || {
  echo "ERROR: Failed to start enrollment. Check URL and try again."
  exit 1
}

ENROLL_URL=$(echo "${ENROLL_RESPONSE}" | jq -r '.enrollUrl')
POLL_URL=$(echo "${ENROLL_RESPONSE}" | jq -r '.pollUrl')
EXPIRES=$(echo "${ENROLL_RESPONSE}" | jq -r '.expiresAt')

if [ -z "${ENROLL_URL}" ] || [ "${ENROLL_URL}" = "null" ]; then
  echo "ERROR: Invalid response from kemia: ${ENROLL_RESPONSE}"
  exit 1
fi

echo ""
echo "════════════════════════════════════════════"
echo "  Open this link to connect:"
echo ""
echo "  ${ENROLL_URL}"
echo ""
echo "  Expires: ${EXPIRES}"
echo "════════════════════════════════════════════"
echo ""
echo "Waiting for confirmation..."

# ---- Step 2: Poll for completion ----
MAX_ATTEMPTS=90  # 15 min / 10s = 90 attempts
ATTEMPT=0

while [ "${ATTEMPT}" -lt "${MAX_ATTEMPTS}" ]; do
  sleep 10
  ATTEMPT=$((ATTEMPT + 1))

  STATUS_RESPONSE=$(curl -sf "${KEMIA_URL}${POLL_URL}" 2>/dev/null) || continue
  STATUS=$(echo "${STATUS_RESPONSE}" | jq -r '.status')

  case "${STATUS}" in
    completed)
      API_KEY=$(echo "${STATUS_RESPONSE}" | jq -r '.apiKey // empty')
      INSTANCE_ID=$(echo "${STATUS_RESPONSE}" | jq -r '.instanceId // empty')

      if [ -z "${API_KEY}" ] || [ -z "${INSTANCE_ID}" ]; then
        echo "ERROR: Enrollment completed but missing credentials."
        exit 1
      fi

      # Save config
      mkdir -p "${SKILL_DIR}"
      cat >"${CONFIG_FILE}" <<EOF
{
  "apiKey": "${API_KEY}",
  "instanceId": "${INSTANCE_ID}",
  "baseUrl": "${KEMIA_URL}"
}
EOF
      chmod 600 "${CONFIG_FILE}"
      echo "✓ Connected! Instance ID: ${INSTANCE_ID}"
      echo "  Config saved: ${CONFIG_FILE}"
      break
      ;;
    expired)
      echo "ERROR: Enrollment expired. Run /connect again."
      exit 1
      ;;
    pending)
      # Still waiting — show progress dot
      printf "."
      ;;
    *)
      echo "ERROR: Unexpected status: ${STATUS}"
      exit 1
      ;;
  esac
done

if [ "${ATTEMPT}" -ge "${MAX_ATTEMPTS}" ]; then
  echo ""
  echo "ERROR: Timed out waiting for confirmation. Run /connect again."
  exit 1
fi

# ---- Step 3: Export agent config files ----
echo ""
echo "Exporting agent config files..."

AGENT_NAME="${OPENCLAW_AGENT_NAME:-CyberClaw}"
FILES_JSON="[]"

for md_file in SOUL.md IDENTITY.md USER.md MEMORY.md AGENTS.md TOOLS.md HEARTBEAT.md; do
  filepath="${WORKSPACE}/${md_file}"
  if [ -f "${filepath}" ]; then
    content=$(jq -Rs '.' < "${filepath}")
    FILES_JSON=$(echo "${FILES_JSON}" | jq --arg fn "${md_file}" --argjson ct "${content}" '. + [{"filename": $fn, "content": $ct}]')
    echo "  ✓ ${md_file}"
  else
    echo "  ⊘ ${md_file} (not found, skipping)"
  fi
done

if [ "$(echo "${FILES_JSON}" | jq 'length')" = "0" ]; then
  echo "WARNING: No .md files found in workspace. Nothing to export."
else
  EXPORT_RESPONSE=$(curl -sf \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${API_KEY}" \
    -d "$(jq -n --arg name "${AGENT_NAME}" --argjson files "${FILES_JSON}" \
      '{name: $name, files: $files}')" \
    "${KEMIA_URL}/api/v1/agents") || {
    echo "ERROR: Failed to export agent config."
    exit 1
  }

  AGENT_ID=$(echo "${EXPORT_RESPONSE}" | jq -r '.agentId')

  # Save agentId to config
  jq --arg aid "${AGENT_ID}" '. + {agentId: $aid}' "${CONFIG_FILE}" > "${CONFIG_FILE}.tmp" \
    && mv "${CONFIG_FILE}.tmp" "${CONFIG_FILE}"
  chmod 600 "${CONFIG_FILE}"

  echo "✓ Agent '${AGENT_NAME}' exported (ID: ${AGENT_ID})"
fi

echo ""
echo "Done. The user is already logged in via the enrollment link."
echo "Use /kemia-link if they need a new login URL later."
