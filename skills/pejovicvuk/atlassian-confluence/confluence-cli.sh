#!/bin/bash
set -euo pipefail

# ============================================================================
# confluence-cli.sh — Confluence Cloud REST API wrapper
#
# Dependencies: curl, python3
# Env vars: ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN
# Outputs: JSON to stdout, errors to stderr
# ============================================================================

for var in ATLASSIAN_URL ATLASSIAN_EMAIL ATLASSIAN_API_TOKEN; do
    if [ -z "${!var:-}" ]; then
        echo "{\"error\": \"Missing env var: $var\"}" >&2
        exit 1
    fi
done

AUTH="$ATLASSIAN_EMAIL:$ATLASSIAN_API_TOKEN"
BASE="$ATLASSIAN_URL/wiki"

# --- HTTP helpers ---
cf_get() {
    local response http_code body
    response=$(curl -s -w "\n%{http_code}" -u "$AUTH" -H "Accept: application/json" "$1")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        echo "{\"error\": \"HTTP $http_code\", \"url\": \"$1\"}" >&2
        exit 1
    fi
    echo "$body"
}

cf_post() {
    local response http_code body
    response=$(curl -s -w "\n%{http_code}" -u "$AUTH" \
        -X POST -H "Content-Type: application/json" -H "Accept: application/json" \
        "$1" -d "$2")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        echo "{\"error\": \"HTTP $http_code\", \"url\": \"$1\", \"response\": $body}" >&2
        exit 1
    fi
    echo "$body"
}

cf_put() {
    local response http_code body
    response=$(curl -s -w "\n%{http_code}" -u "$AUTH" \
        -X PUT -H "Content-Type: application/json" -H "Accept: application/json" \
        "$1" -d "$2")
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    if [ "$http_code" -ge 400 ]; then
        echo "{\"error\": \"HTTP $http_code\", \"url\": \"$1\", \"response\": $body}" >&2
        exit 1
    fi
    echo "$body"
}

urlencode() {
    python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$1"
}

# --- Commands ---

cmd_spaces() {
    cf_get "$BASE/api/v2/spaces?limit=25" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'id':s.get('id'),
    'key':s.get('key'),
    'name':s.get('name'),
    'type':s.get('type'),
    'status':s.get('status')
} for s in d.get('results',[])],indent=2))
"
}

cmd_pages() {
    local space_id="${1:?Usage: confluence-cli.sh pages SPACE_ID [limit]}"
    local limit="${2:-25}"
    cf_get "$BASE/api/v2/spaces/$space_id/pages?limit=$limit" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'id':p.get('id'),
    'title':p.get('title'),
    'status':p.get('status'),
    'parentId':p.get('parentId'),
    'authorId':p.get('authorId'),
    'created':p.get('createdAt'),
    'url':p.get('_links',{}).get('webui')
} for p in d.get('results',[])],indent=2))
"
}

cmd_get_page() {
    local page_id="${1:?Usage: confluence-cli.sh get PAGE_ID}"
    cf_get "$BASE/api/v2/pages/$page_id?body-format=storage" | python3 -c "
import sys,json
d=json.load(sys.stdin)
body_html=d.get('body',{}).get('storage',{}).get('value','')
# Strip HTML tags for readable text
import re
body_text=re.sub(r'<[^>]+>','',body_html).strip()
print(json.dumps({
    'id':d.get('id'),
    'title':d.get('title'),
    'status':d.get('status'),
    'spaceId':d.get('spaceId'),
    'parentId':d.get('parentId'),
    'version':(d.get('version')or{}).get('number'),
    'body_text':body_text[:3000],
    'body_html':body_html[:5000],
    'created':d.get('createdAt'),
    'url':d.get('_links',{}).get('webui')
},indent=2))
"
}

cmd_children() {
    local page_id="${1:?Usage: confluence-cli.sh children PAGE_ID}"
    cf_get "$BASE/api/v2/pages/$page_id/children?limit=25" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'id':p.get('id'),
    'title':p.get('title'),
    'status':p.get('status'),
    'url':p.get('_links',{}).get('webui')
} for p in d.get('results',[])],indent=2))
"
}

cmd_search() {
    local cql="${1:?Usage: confluence-cli.sh search \"CQL query\" [limit]}"
    local limit="${2:-10}"
    cf_get "$BASE/rest/api/content/search?cql=$(urlencode "$cql")&limit=$limit" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({
    'total':d.get('totalSize',d.get('size',0)),
    'results':[{
        'id':r.get('id'),
        'title':r.get('title'),
        'type':r.get('type'),
        'space':(r.get('space')or{}).get('key'),
        'url':r.get('_links',{}).get('webui')
    } for r in d.get('results',[])]
},indent=2))
"
}

cmd_create_page() {
    local space_id="" title="" parent_id="" body=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --space) space_id="$2"; shift 2;;
            --title) title="$2"; shift 2;;
            --parent) parent_id="$2"; shift 2;;
            --body) body="$2"; shift 2;;
            *) echo "{\"error\":\"Unknown flag: $1\"}" >&2; exit 1;;
        esac
    done
    [ -z "$space_id" ] || [ -z "$title" ] && { echo '{"error":"Required: --space SPACE_ID --title TEXT"}' >&2; exit 1; }

    local payload
    payload=$(python3 -c "
import json
p={'spaceId':'$space_id','status':'current','title':json.loads($(python3 -c "import json;print(json.dumps(json.dumps('$title')))"))}
parent='$parent_id'
if parent:p['parentId']=parent
body='$body'
if body:p['body']={'representation':'storage','value':body}
else:p['body']={'representation':'storage','value':'<p></p>'}
print(json.dumps(p))
")
    cf_post "$BASE/api/v2/pages" "$payload" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({
    'id':d.get('id'),
    'title':d.get('title'),
    'url':d.get('_links',{}).get('webui')
},indent=2))
"
}

cmd_update_page() {
    local page_id="${1:?Usage: confluence-cli.sh update PAGE_ID --title TEXT --body HTML}"
    shift
    local title="" body=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --title) title="$2"; shift 2;;
            --body) body="$2"; shift 2;;
            *) echo "{\"error\":\"Unknown flag: $1\"}" >&2; exit 1;;
        esac
    done

    # Get current version first
    local current_version
    current_version=$(cf_get "$BASE/api/v2/pages/$page_id" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(d.get('version',{}).get('number',1))
")
    local new_version=$((current_version + 1))

    local payload
    payload=$(python3 -c "
import json
p={'id':'$page_id','status':'current','version':{'number':$new_version,'message':'Updated by agent'}}
t='$title'
if t:p['title']=t
else:
    # must include title, fetch it
    p['title']=json.loads($(cf_get "$BASE/api/v2/pages/$page_id" | python3 -c "import sys,json;print(json.dumps(json.load(sys.stdin).get('title','Untitled')))"))
b='''$body'''
if b:p['body']={'representation':'storage','value':b}
print(json.dumps(p))
")
    cf_put "$BASE/api/v2/pages/$page_id" "$payload" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({
    'id':d.get('id'),
    'title':d.get('title'),
    'version':(d.get('version')or{}).get('number'),
    'url':d.get('_links',{}).get('webui')
},indent=2))
"
}

cmd_labels() {
    local page_id="${1:?Usage: confluence-cli.sh labels PAGE_ID}"
    cf_get "$BASE/rest/api/content/$page_id/label" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps([{
    'name':l.get('name'),
    'prefix':l.get('prefix')
} for l in d.get('results',[])],indent=2))
"
}

cmd_add_labels() {
    local page_id="${1:?Usage: confluence-cli.sh add-labels PAGE_ID \"label1,label2\"}"
    local labels_str="${2:?Usage: confluence-cli.sh add-labels PAGE_ID \"label1,label2\"}"
    local payload
    payload=$(python3 -c "
import json
labels='$labels_str'.split(',')
print(json.dumps([{'prefix':'global','name':l.strip()} for l in labels]))
")
    cf_post "$BASE/rest/api/content/$page_id/label" "$payload" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(json.dumps({'labels':[l.get('name') for l in d.get('results',d if isinstance(d,list) else [])]},indent=2))
"
}

# --- Dispatch ---
CMD="${1:-help}"; shift || true
case "$CMD" in
    spaces)      cmd_spaces;;
    pages)       cmd_pages "$@";;
    get)         cmd_get_page "$@";;
    children)    cmd_children "$@";;
    search)      cmd_search "$@";;
    create)      cmd_create_page "$@";;
    update)      cmd_update_page "$@";;
    labels)      cmd_labels "$@";;
    add-labels)  cmd_add_labels "$@";;
    help|--help|-h)
        echo "Usage: confluence-cli.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  spaces                       List all spaces"
        echo "  pages SPACE_ID [limit]       List pages in a space"
        echo "  get PAGE_ID                  Get page content"
        echo "  children PAGE_ID             List child pages"
        echo "  search \"CQL\" [limit]         Search with CQL"
        echo "  create --space ID --title TEXT [--parent ID] [--body HTML]"
        echo "  update PAGE_ID [--title TEXT] [--body HTML]"
        echo "  labels PAGE_ID               Get page labels"
        echo "  add-labels PAGE_ID \"l1,l2\"   Add labels to page"
        echo ""
        echo "Env: ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN";;
    *) echo "{\"error\":\"Unknown command: $CMD\"}" >&2; exit 1;;
esac