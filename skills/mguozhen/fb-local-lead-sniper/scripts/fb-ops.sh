#!/bin/bash
# fb-local-lead-sniper — Main entry point
# Usage: fb-ops.sh <action> [options]
# Actions: join, engage, post, bait, analyze, warm, status

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/cdp-helpers.sh"
source "$SCRIPT_DIR/join.sh"
source "$SCRIPT_DIR/engage.sh"
source "$SCRIPT_DIR/post.sh"
source "$SCRIPT_DIR/analyze.sh"

usage() {
    cat << 'EOF'
fb-local-lead-sniper — Facebook Local Group Lead Generation

Usage: fb-ops.sh <action> [options]

Actions:
  join      Join local groups
              --city CITY     Target city (default: Austin)
              --count N       Number of groups (default: 5)
              --query Q       Custom search query

  engage    Like and comment on posts
              --likes N       Number of likes (default: 20)
              --comments N    Number of comments (default: 8)
              --groups G      Comma-separated group slugs

  post      Post a life update on profile
              --text TEXT     Post text (or auto from templates)

  bait      Post a recommendation request in a group
              --group URL     Group URL
              --trade TRADE   Trade type (plumber, electrician, etc.)
              --template TPL  Template: urgent|research|newcomer|complaint|poll

  analyze   Analyze replies on a bait post
              --url URL       Post URL to analyze

  warm      Full warm-up cycle
              --city CITY     Target city
              --intensity I   normal (default) or double

  status    Check account status and pending posts

Examples:
  fb-ops.sh join --city Austin --count 5
  fb-ops.sh warm --city Houston --intensity double
  fb-ops.sh bait --group "https://facebook.com/groups/xxx" --trade plumber
  fb-ops.sh analyze --url "https://facebook.com/groups/xxx/posts/yyy"
EOF
}

# Parse named arguments
parse_args() {
    CITY="Austin"; COUNT=5; QUERY=""; LIKES=20; COMMENTS=8; GROUPS=""
    TEXT=""; GROUP_URL=""; TRADE="plumber"; TEMPLATE="research"
    POST_URL=""; INTENSITY="normal"

    while [ $# -gt 0 ]; do
        case "$1" in
            --city)      CITY="$2"; shift 2 ;;
            --count)     COUNT="$2"; shift 2 ;;
            --query)     QUERY="$2"; shift 2 ;;
            --likes)     LIKES="$2"; shift 2 ;;
            --comments)  COMMENTS="$2"; shift 2 ;;
            --groups)    GROUPS="$2"; shift 2 ;;
            --text)      TEXT="$2"; shift 2 ;;
            --group)     GROUP_URL="$2"; shift 2 ;;
            --trade)     TRADE="$2"; shift 2 ;;
            --template)  TEMPLATE="$2"; shift 2 ;;
            --url)       POST_URL="$2"; shift 2 ;;
            --intensity) INTENSITY="$2"; shift 2 ;;
            *)           shift ;;
        esac
    done
}

# Main
ACTION="${1:-help}"
shift || true
parse_args "$@"

case "$ACTION" in
    help|-h|--help)
        usage
        exit 0
        ;;
    join|engage|post|bait|analyze|warm|status)
        cdp_check || exit 1
        fb_open || exit 1
        trap fb_close EXIT
        ;;
    *)
        echo "Unknown action: $ACTION"
        usage
        exit 1
        ;;
esac

case "$ACTION" in
    join)
        do_join "$CITY" "$COUNT" "$QUERY"
        ;;
    engage)
        do_like "$LIKES" "$GROUPS"
        human_delay 5 10
        do_comment "$COMMENTS" "$GROUPS"
        ;;
    post)
        do_life_post "$TEXT"
        ;;
    bait)
        if [ -z "$GROUP_URL" ]; then
            echo "Error: --group URL required for bait action"
            exit 1
        fi
        do_bait_post "$GROUP_URL" "$TRADE" "$TEMPLATE"
        ;;
    analyze)
        if [ -z "$POST_URL" ]; then
            echo "Error: --url required for analyze action"
            exit 1
        fi
        do_analyze "$POST_URL"
        ;;
    warm)
        if [ "$INTENSITY" = "double" ]; then
            LIKES=40; COMMENTS=16; COUNT=10
        fi
        do_like "$LIKES" "$GROUPS"
        human_delay 5 10
        do_comment "$COMMENTS" "$GROUPS"
        human_delay 5 10
        do_join "$CITY" "$COUNT" "$QUERY"
        # Post life update in afternoon/evening
        HOUR=$(date +%H)
        if [ "$HOUR" -ge 15 ] || [ "$HOUR" -le 9 ]; then
            human_delay 5 10
            do_life_post "$TEXT"
        fi
        ;;
    status)
        do_status
        ;;
esac

log "Done."
