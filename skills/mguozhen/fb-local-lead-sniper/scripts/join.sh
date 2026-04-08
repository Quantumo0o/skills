#!/bin/bash
# Join Facebook local groups by city
# Usage: source cdp-helpers.sh first, then call do_join

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/cdp-helpers.sh"

do_join() {
    local city="${1:-Austin}"
    local count="${2:-5}"
    local query="${3:-}"

    log "Joining $count groups in $city..."

    # Build search query
    if [ -z "$query" ]; then
        local queries=(
            "$city+community+group"
            "$city+neighbors+recommendations"
            "$city+local+business"
            "$city+homeowners+residents"
            "$city+moms+families"
        )
        query="${queries[$(( RANDOM % ${#queries[@]} ))]}"
    fi

    fb_navigate "https://www.facebook.com/search/groups/?q=$(echo "$query" | sed 's/ /+/g')"
    sleep 3

    local total=0
    for i in $(seq 1 "$count"); do
        local result
        result=$(fb_eval_value '(function(){
            var btns=Array.from(document.querySelectorAll("[role=\"button\"]")).filter(function(b){
                return b.innerText.trim()==="Join"&&b.offsetParent!==null;
            });
            if(btns[0]){btns[0].click();return"joined";}
            return"none";
        })()')

        if [ "$result" = "none" ]; then
            log "  No more Join buttons found"
            # Try scrolling for more
            fb_scroll 1500
            sleep 2
            result=$(fb_eval_value '(function(){
                var btns=Array.from(document.querySelectorAll("[role=\"button\"]")).filter(function(b){
                    return b.innerText.trim()==="Join"&&b.offsetParent!==null;
                });
                if(btns[0]){btns[0].click();return"joined";}
                return"none";
            })()')
            [ "$result" = "none" ] && break
        fi

        sleep 3

        # Handle questionnaire dialogs
        fb_eval '(function(){
            var ds=document.querySelectorAll("[role=\"dialog\"]");
            for(var d of ds){
                var t=d.innerText||"";
                if(t.includes("Answer")||t.includes("question")){
                    var c=d.querySelector("[aria-label=\"Close\"]");
                    if(c)c.click();
                }
            }
            return"ok";
        })()' > /dev/null 2>&1

        # Check rate limit
        if fb_check_rate_limit; then
            log "  Rate limited! Stopping joins."
            break
        fi

        total=$((total + 1))
        log "  Joined #$total"

        # Human-like delay 30-60s between joins
        local delay=$(( RANDOM % 31 + 30 ))
        [ $i -lt "$count" ] && sleep $delay
    done

    log "Join complete: $total groups"
    echo "$total"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    cdp_check || exit 1
    fb_open || exit 1
    trap fb_close EXIT
    do_join "$@"
fi
