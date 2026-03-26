#!/bin/bash
SPARK_API_KEY="${SPARK_API_KEY:-}"
SPARK_ORG_ID="${SPARK_ORG_ID:-}"
SPARK_API_URL="${SPARK_API_URL:-https://zellin.ai/api}"

if [ -z "$SPARK_API_KEY" ] || [ -z "$SPARK_ORG_ID" ]; then
  echo '{"error": "SPARK_API_KEY and SPARK_ORG_ID must be set"}'
  exit 1
fi

SECTION="${1:-all}"

curl -s -X POST "${SPARK_API_URL}/spark-memory-insights" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${SPARK_API_KEY}" \
  -d "{\"org_id\": \"${SPARK_ORG_ID}\", \"section\": \"${SECTION}\"}"
