#!/bin/bash
# Sign up for Spark — creates a free account and returns credentials
# Usage: ./spark-signup.sh [--email EMAIL] [--password PASSWORD]
# Or run without arguments for interactive prompts.

set -e

SPARK_SIGNUP_URL="${SPARK_SIGNUP_URL:-https://zellin.ai/api/spark-signup}"

# ── Parse flags ──────────────────────────────────────────────────────────────
EMAIL=""
PASSWORD=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --email)  EMAIL="$2";  shift 2 ;;
    --password) PASSWORD="$2"; shift 2 ;;
    *)        echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# ── Interactive prompts ──────────────────────────────────────────────────────
if [ -z "$EMAIL" ]; then
  echo -n "Email: "
  read -r EMAIL
fi

if [ -z "$PASSWORD" ]; then
  echo -n "Password (min 8 characters): "
  read -s -r PASSWORD
  echo
fi

# ── Validate ──────────────────────────────────────────────────────────────────
if [ -z "$EMAIL" ] || [ -z "$PASSWORD" ]; then
  echo "Error: email and password are required." >&2
  exit 1
fi

if [ ${#PASSWORD} -lt 8 ]; then
  echo "Error: password must be at least 8 characters." >&2
  exit 1
fi

# ── Name from email (first part, capitalized) ──────────────────────────────────
NAME=$(echo "$EMAIL" | cut -d@ -f1 | sed 's/[._-]/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1))substr($i,2); print}')
if [ -z "$NAME" ]; then
  NAME="Spark User"
fi

# ── Send signup request ───────────────────────────────────────────────────────
BODY=$(python3 -c "
import json, sys
print(json.dumps({
    'email': sys.argv[1],
    'password': sys.argv[2],
    'name': sys.argv[3],
}))
" "$EMAIL" "$PASSWORD" "$NAME")

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$SPARK_SIGNUP_URL" \
  -H "Content-Type: application/json" \
  -d "$BODY")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY_CONTENT=$(echo "$RESPONSE" | sed '$d')

# ── Handle response ───────────────────────────────────────────────────────────
if [ "$HTTP_CODE" = "201" ]; then
  API_KEY=$(echo "$BODY_CONTENT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('api_key','<unknown>'))" 2>/dev/null || echo "<parse error>")
  ORG_ID=$(echo "$BODY_CONTENT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('org_id','<unknown>'))" 2>/dev/null || echo "<parse error>")

  echo ""
  echo "✅ Spark account created!"
  echo ""
  echo "Your credentials (save these — shown only once):"
  echo "  SPARK_API_KEY=$API_KEY"
  echo "  SPARK_ORG_ID=$ORG_ID"
  echo ""
  echo "To activate, set these environment variables:"
  echo "  export SPARK_API_KEY=\"$API_KEY\""
  echo "  export SPARK_ORG_ID=\"$ORG_ID\""
  echo ""
  echo "Or add to your OpenClaw config (openclaw.json):"
  echo "  \"env\": {"
  echo "    \"SPARK_API_KEY\": \"$API_KEY\","
  echo "    \"SPARK_ORG_ID\": \"$ORG_ID\""
  echo "  }"
  echo ""
  echo "Then restart: openclaw gateway restart"

elif [ "$HTTP_CODE" = "409" ]; then
  echo "An account with this email already exists. Sign in at https://zellin.ai instead."
  exit 1
else
  ERROR_MSG=$(echo "$BODY_CONTENT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error', d.get('message', 'Unknown error')))" 2>/dev/null || echo "$BODY_CONTENT")
  # Catch duplicate email even if backend returns wrong status code
  if echo "$ERROR_MSG" | grep -qi "already.*registered\|already.*exists\|email_exists"; then
    echo "An account with this email already exists. Sign in at https://zellin.ai instead."
  else
    echo "Error ($HTTP_CODE): $ERROR_MSG" >&2
  fi
  exit 1
fi
