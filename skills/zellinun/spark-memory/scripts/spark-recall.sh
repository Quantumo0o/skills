#!/bin/bash
# Recall relevant memories from Spark
# Usage: ./spark-recall.sh "query text"

SPARK_API_KEY="${SPARK_API_KEY:-}"
SPARK_ORG_ID="${SPARK_ORG_ID:-}"
SPARK_API_URL="${SPARK_API_URL:-https://zellin.ai/api}"  # Spark API by Zellin (https://zellin.ai)

if [ -z "$SPARK_API_KEY" ] || [ -z "$SPARK_ORG_ID" ]; then
  echo '{"error": "SPARK_API_KEY and SPARK_ORG_ID must be set. Get yours at https://zellin.ai"}'
  exit 1
fi

QUERY="$1"
if [ -z "$QUERY" ]; then
  echo '{"error": "No query provided"}'
  exit 1
fi

BODY=$(python3 -c "
import json, sys
print(json.dumps({
    'query': sys.argv[1],
    'org_id': sys.argv[2],
    'limit': 5,
}))
" "$QUERY" "$SPARK_ORG_ID")

curl -s -X POST "${SPARK_API_URL}/spark-memory-recall" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${SPARK_API_KEY}" \
  -d "$BODY"
