#!/bin/bash
# Facebook posting — life updates and bait posts
# Usage: source cdp-helpers.sh first, then call do_life_post / do_bait_post

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/cdp-helpers.sh"

# Post a life update on personal profile
do_life_post() {
    local text="${1:-}"
    log "Posting life update..."

    if [ -z "$text" ]; then
        local tpl="$SCRIPT_DIR/../templates/life-posts.json"
        if [ -f "$tpl" ]; then
            text=$(python3 -c "import json,random;posts=json.load(open('$tpl'));print(random.choice(posts))" 2>/dev/null)
        fi
    fi

    if [ -z "$text" ]; then
        log "[FAIL] No post text provided and no templates found"
        return 1
    fi

    fb_navigate "https://www.facebook.com/me"
    sleep 4

    # Click "What's on your mind"
    fb_eval '(function(){var b=document.querySelectorAll("[role=\"button\"]");for(var x of b){if(x.innerText.includes("on your mind")){x.click();return"ok"}}return"none"})()' > /dev/null 2>&1
    sleep 3

    # Type the post — escape for JS
    local js_text
    js_text=$(python3 -c "import json;print(json.dumps('$text')[1:-1])" 2>/dev/null || echo "$text")

    fb_eval "(function(){var t=\"$js_text\";var eds=document.querySelectorAll('[role=\"textbox\"][contenteditable=\"true\"]');for(var e of eds){var l=(e.getAttribute('aria-label')||'').toLowerCase()+(e.getAttribute('aria-placeholder')||'').toLowerCase();if((l.includes('on your mind')||l.includes('create')||l.includes('post'))&&!l.includes('comment')){e.focus();document.execCommand('insertText',false,t);return'ok'}}if(eds.length>0){eds[eds.length-1].focus();document.execCommand('insertText',false,t);return'fb'}return'none'})()" > /dev/null 2>&1
    sleep 2

    # Click Post button
    fb_eval '(function(){var b=Array.from(document.querySelectorAll("[role=\"button\"]")).filter(function(x){return x.innerText.trim()==="Post"});if(b.length>0){b[b.length-1].click();return"posted"}return"none"})()' > /dev/null 2>&1
    sleep 5

    log "Life post published: ${text:0:60}..."
}

# Post a bait/recommendation request in a group
do_bait_post() {
    local group_url="$1"
    local trade="${2:-plumber}"
    local template="${3:-research}"
    log "Posting bait in group: $group_url (trade: $trade, template: $template)..."

    # Load bait template
    local tpl_file="$SCRIPT_DIR/../templates/bait-posts.json"
    local text
    if [ -f "$tpl_file" ]; then
        text=$(python3 -c "
import json
data=json.load(open('$tpl_file'))
trade_data=data.get('$trade', data.get('general',{}))
templates=trade_data.get('$template', trade_data.get('research',[]))
if isinstance(templates, list) and templates:
    import random; print(random.choice(templates))
elif isinstance(templates, str):
    print(templates)
else:
    print('')
" 2>/dev/null)
    fi

    if [ -z "$text" ]; then
        log "[FAIL] No bait template found for trade=$trade template=$template"
        return 1
    fi

    fb_navigate "$group_url"
    sleep 5
    fb_dismiss_dialogs

    # Click "Write something"
    fb_eval '(function(){var b=document.querySelectorAll("[role=\"button\"]");for(var x of b){if(x.innerText.includes("Write something")||x.innerText.includes("on your mind")){x.click();return"ok"}}return"none"})()' > /dev/null 2>&1
    sleep 3

    # Type the bait post
    local js_text
    js_text=$(python3 -c "import json;print(json.dumps('''$text''')[1:-1])" 2>/dev/null || echo "$text")

    fb_eval "(function(){var t=\"$js_text\";var eds=document.querySelectorAll('[role=\"textbox\"][contenteditable=\"true\"]');for(var e of eds){var l=(e.getAttribute('aria-label')||'').toLowerCase()+(e.getAttribute('aria-placeholder')||'').toLowerCase();if((l.includes('create')||l.includes('post')||l.includes('write'))&&!l.includes('comment')){e.focus();document.execCommand('insertText',false,t);return'ok'}}if(eds.length>0){eds[eds.length-1].focus();document.execCommand('insertText',false,t);return'fb'}return'none'})()" > /dev/null 2>&1
    sleep 2

    # Click Post
    fb_eval '(function(){var b=Array.from(document.querySelectorAll("[role=\"button\"]")).filter(function(x){return x.innerText.trim()==="Post"});if(b.length>0){b[b.length-1].click();return"posted"}return"none"})()' > /dev/null 2>&1
    sleep 5

    log "Bait post published in group"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    cdp_check || exit 1
    fb_open || exit 1
    trap fb_close EXIT
    action="${1:-life}"
    shift || true
    case "$action" in
        life) do_life_post "$@" ;;
        bait) do_bait_post "$@" ;;
        *) echo "Usage: $0 life|bait [args...]" ;;
    esac
fi
