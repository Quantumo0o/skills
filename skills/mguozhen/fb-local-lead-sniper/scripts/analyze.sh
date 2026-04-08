#!/bin/bash
# Analyze Facebook post replies to find top-recommended providers
# Usage: source cdp-helpers.sh first, then call do_analyze

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/cdp-helpers.sh"

do_analyze() {
    local post_url="$1"
    log "Analyzing replies on: $post_url"

    fb_navigate "$post_url"
    sleep 5
    fb_dismiss_dialogs

    # Scroll to load all comments
    for i in 1 2 3 4 5; do
        fb_scroll 1500
        sleep 2
        # Click "View more comments" if present
        fb_eval '(function(){var btns=document.querySelectorAll("[role=\"button\"]");for(var b of btns){if(b.innerText.includes("View more comments")||b.innerText.includes("View all")){b.click();return"expanded"}}return"none"})()' > /dev/null 2>&1
        sleep 2
    done

    # Extract all comment text
    local comments
    comments=$(fb_eval_value '(function(){
        var articles=document.querySelectorAll("[role=\"article\"]");
        var comments=[];
        for(var a of articles){
            var text=a.innerText||"";
            if(text.length>10 && text.length<2000){
                comments.push(text.substring(0,500));
            }
        }
        return JSON.stringify(comments);
    })()')

    if [ -z "$comments" ] || [ "$comments" = "[]" ]; then
        log "No comments found on this post"
        return 1
    fi

    # Parse with Python for recommendations
    python3 << 'PYEOF'
import json, re, sys
from collections import Counter

raw = '''COMMENTS_PLACEHOLDER'''

try:
    comments = json.loads(raw)
except:
    comments = [raw]

mentions = Counter()
phones = []
patterns = [
    r'(?:I recommend|recommend|try|call|use|contact|hit up|reach out to)\s+([A-Z][a-zA-Z\s&\']+?)(?:\.|,|!|\n|$)',
    r'@([A-Za-z][A-Za-z\s]+)',
    r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+(?:is|was|does|did|has)',
]
phone_re = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'

for c in comments:
    for pat in patterns:
        for match in re.finditer(pat, c):
            name = match.group(1).strip()
            if 2 < len(name) < 50:
                mentions[name] += 1
    for phone in re.finditer(phone_re, c):
        phones.append(phone.group(1))

print("\n=== TOP RECOMMENDED PROVIDERS ===\n")
if mentions:
    for name, count in mentions.most_common(15):
        print(f"  {count}x  {name}")
else:
    print("  No specific recommendations found")

if phones:
    print(f"\n=== PHONE NUMBERS FOUND ({len(phones)}) ===\n")
    for p in set(phones):
        print(f"  {p}")

print(f"\n=== STATS ===")
print(f"  Total comments analyzed: {len(comments)}")
print(f"  Unique providers mentioned: {len(mentions)}")
print(f"  Phone numbers found: {len(phones)}")
PYEOF

    log "Analysis complete"
}

do_status() {
    log "Checking account status..."

    # Check profile
    fb_navigate "https://www.facebook.com/me"
    sleep 4
    local name
    name=$(fb_eval_value '(function(){var h=document.querySelector("h1");return h?h.innerText:"unknown"})()')
    log "Profile: $name"

    # Check groups
    fb_navigate "https://www.facebook.com/groups/joins/"
    sleep 4
    local group_count
    group_count=$(fb_eval_value '(function(){var links=document.querySelectorAll("a[href*=\"/groups/\"]");return links.length})()')
    log "Visible joined groups: $group_count"

    # Screenshot
    fb_screenshot "/tmp/fb_status.png"
    log "Status screenshot: /tmp/fb_status.png"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    cdp_check || exit 1
    fb_open || exit 1
    trap fb_close EXIT
    action="${1:-status}"
    shift || true
    case "$action" in
        analyze) do_analyze "$@" ;;
        status) do_status ;;
        *) echo "Usage: $0 analyze|status [url]" ;;
    esac
fi
