#!/bin/bash
# CDP proxy helper functions for Facebook operations
# Requires: web-access CDP proxy running on localhost:3456

CDP="${CDP_PROXY_URL:-http://localhost:3456}"
FB_TAB=""

log() { echo "[$(date +%H:%M:%S)] $*"; }

# Check CDP proxy is running and responsive
cdp_check() {
    local targets
    targets=$(curl -s --max-time 5 "$CDP/targets" 2>/dev/null || echo "")
    if echo "$targets" | python3 -c "import sys,json;json.load(sys.stdin)" 2>/dev/null; then
        return 0
    fi
    log "[FAIL] CDP proxy not available at $CDP"
    log "  Make sure web-access skill is installed and Chrome has remote debugging enabled"
    log "  Run: CLAUDE_SKILL_DIR=~/.claude/skills/web-access node ~/.claude/skills/web-access/scripts/check-deps.mjs"
    return 1
}

# Open a new Facebook tab, verify login
fb_open() {
    local url="${1:-https://www.facebook.com/}"
    local result
    result=$(curl -s --max-time 15 "$CDP/new?url=$url" 2>/dev/null)
    FB_TAB=$(echo "$result" | python3 -c "import sys,json;print(json.load(sys.stdin).get('targetId',''))" 2>/dev/null)
    if [ -z "$FB_TAB" ]; then
        log "[FAIL] Could not open Facebook tab"
        return 1
    fi
    sleep 4

    local title
    title=$(curl -s "$CDP/info?target=$FB_TAB" | python3 -c "import sys,json;print(json.load(sys.stdin).get('title',''))" 2>/dev/null)
    if echo "$title" | grep -iq "log in"; then
        log "[FAIL] Not logged into Facebook. Please log in via Chrome first."
        fb_close
        return 1
    fi
    log "[OK] Facebook ready (tab: ${FB_TAB:0:8}...)"
    return 0
}

# Close the Facebook tab
fb_close() {
    [ -n "${FB_TAB:-}" ] && curl -s "$CDP/close?target=$FB_TAB" > /dev/null 2>&1
    FB_TAB=""
}

# Navigate to URL in current tab
fb_navigate() {
    local url="$1"
    curl -s "$CDP/navigate?target=$FB_TAB&url=$url" > /dev/null 2>&1
    sleep 4
}

# Scroll down
fb_scroll() {
    local amount="${1:-1000}"
    curl -s "$CDP/scroll?target=$FB_TAB&y=$amount" > /dev/null 2>&1
    sleep 2
}

# Execute JS and return value
fb_eval() {
    local js="$1"
    curl -s -X POST "$CDP/eval?target=$FB_TAB" -d "$js" 2>/dev/null
}

# Execute JS and extract value field
fb_eval_value() {
    local js="$1"
    fb_eval "$js" | python3 -c "import sys,json;print(json.load(sys.stdin).get('value',''))" 2>/dev/null
}

# Click element by CSS selector
fb_click() {
    local selector="$1"
    curl -s -X POST "$CDP/click?target=$FB_TAB" -d "$selector" > /dev/null 2>&1
}

# Take screenshot
fb_screenshot() {
    local file="${1:-/tmp/fb_screenshot.png}"
    curl -s "$CDP/screenshot?target=$FB_TAB&file=$file" > /dev/null 2>&1
    echo "$file"
}

# Dismiss common Facebook popups/dialogs
fb_dismiss_dialogs() {
    fb_eval '(function(){
        var c=document.querySelector("[aria-label=\"Close\"]");
        if(c)c.click();
        var ds=document.querySelectorAll("[role=\"dialog\"]");
        for(var d of ds){
            var txt=d.innerText||"";
            if(txt.includes("Got it")||txt.includes("Continue")||txt.includes("Not Now")){
                var btn=d.querySelector("[role=\"button\"]");
                if(btn)btn.click();
            }
        }
        return "ok";
    })()' > /dev/null 2>&1
    sleep 1
}

# Check if rate-limited
fb_check_rate_limit() {
    local result
    result=$(fb_eval_value '(function(){
        var ds=document.querySelectorAll("[role=\"dialog\"]");
        for(var d of ds){
            var t=d.innerText||"";
            if((t.includes("Can")||t.includes("can"))&&t.includes("Feature"))return"LIMITED";
        }
        return"ok";
    })()')
    [ "$result" = "LIMITED" ]
}

# Random delay between min and max seconds
human_delay() {
    local min="${1:-2}" max="${2:-5}"
    sleep $(( RANDOM % (max - min + 1) + min ))
}
