#!/bin/bash
# Record an episode to Spark memory
# Usage: ./spark-record.sh "content" [episode_type] [importance]
# episode_type: observation|action|conversation|user_feedback|tool_result|entity_interaction
# importance: 1-10 (default: 5)

SPARK_API_KEY="${SPARK_API_KEY:-}"
SPARK_ORG_ID="${SPARK_ORG_ID:-}"
SPARK_API_URL="${SPARK_API_URL:-https://zellin.ai/api}"  # Spark API by Zellin (https://zellin.ai)

if [ -z "$SPARK_API_KEY" ] || [ -z "$SPARK_ORG_ID" ]; then
  echo '{"error": "SPARK_API_KEY and SPARK_ORG_ID must be set. Get yours at https://zellin.ai"}'
  exit 1
fi

CONTENT="$1"
EPISODE_TYPE="${2:-observation}"
IMPORTANCE="${3:-5}"

if [ -z "$CONTENT" ]; then
  echo '{"error": "No content provided"}'
  exit 1
fi

BODY=$(python3 -c "
import json, sys
print(json.dumps({
    'org_id': sys.argv[1],
    'content': sys.argv[2],
    'episode_type': sys.argv[3],
    'importance_score': int(sys.argv[4]),
}))
" "$SPARK_ORG_ID" "$CONTENT" "$EPISODE_TYPE" "$IMPORTANCE")

curl -s -X POST "${SPARK_API_URL}/spark-memory-record" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${SPARK_API_KEY}" \
  -d "$BODY"
