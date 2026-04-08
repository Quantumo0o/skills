#!/bin/bash
# Facebook engagement — likes and comments
# Usage: source cdp-helpers.sh first, then call do_like / do_comment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/cdp-helpers.sh"

# Load comments from template file
load_comments() {
    local tpl="$SCRIPT_DIR/../templates/comments.json"
    if [ -f "$tpl" ]; then
        python3 -c "import json;[print(c) for c in json.load(open('$tpl'))]" 2>/dev/null
    else
        # Fallback defaults
        echo "This is awesome, thanks for sharing!"
        echo "Love this! Great community"
        echo "Really helpful, appreciate the post!"
        echo "Wow thats great, thanks!"
        echo "So cool! Love seeing this"
        echo "Thanks for posting, very useful!"
        echo "Great stuff, appreciate it!"
        echo "So helpful, thank you!"
        echo "Amazing, thanks for sharing this"
        echo "Good to know, thanks for the heads up!"
        echo "Really nice, love this community"
        echo "Awesome post, thanks!"
    fi
}

do_like() {
    local target_count="${1:-20}"
    local groups_str="${2:-}"
    log "Liking posts (target: $target_count)..."

    local total=0

    # Like on main feed first
    fb_navigate "https://www.facebook.com/"
    sleep 2

    for round in $(seq 1 5); do
        fb_scroll 1200
        sleep 3
        local count
        count=$(fb_eval_value '(function(){var b=document.querySelectorAll("[aria-label=\"Like\"]"),n=0;for(var i=0;i<b.length;i++){try{b[i].click();n++}catch(e){}}return n})()')
        total=$((total + ${count:-0}))
        human_delay 2 4
    done

    # Like in groups
    local groups
    if [ -n "$groups_str" ]; then
        IFS=',' read -ra groups <<< "$groups_str"
    else
        groups=("EventsAustin" "austintexasgroup" "SouthAustinTxNeighbors")
    fi

    for g in "${groups[@]}"; do
        [ $total -ge $target_count ] && break
        fb_navigate "https://www.facebook.com/groups/$g/"
        sleep 3
        fb_dismiss_dialogs

        for r in 1 2 3; do
            fb_scroll 1000
            sleep 2
            local count
            count=$(fb_eval_value '(function(){var b=document.querySelectorAll("[aria-label=\"Like\"]"),n=0;for(var i=0;i<b.length;i++){try{b[i].click();n++}catch(e){}}return n})()')
            total=$((total + ${count:-0}))
            human_delay 1 3
        done
        human_delay 3 6
    done

    log "Likes complete: $total"
    echo "$total"
}

do_comment() {
    local target_count="${1:-8}"
    local groups_str="${2:-}"
    log "Commenting on posts (target: $target_count)..."

    # Load comment pool
    local -a comment_pool
    mapfile -t comment_pool < <(load_comments)
    local pool_size=${#comment_pool[@]}

    local total=0
    local groups
    if [ -n "$groups_str" ]; then
        IFS=',' read -ra groups <<< "$groups_str"
    else
        groups=("EventsAustin" "austintexasgroup" "SouthAustinTxNeighbors")
    fi

    for g in "${groups[@]}"; do
        [ $total -ge $target_count ] && break
        fb_navigate "https://www.facebook.com/groups/$g/"
        sleep 4
        fb_dismiss_dialogs
        fb_scroll 600
        sleep 3

        local per_group=$(( (target_count - total + ${#groups[@]} - 1) / ${#groups[@]} ))
        [ $per_group -gt 3 ] && per_group=3

        for ci in $(seq 0 $((per_group - 1))); do
            [ $total -ge $target_count ] && break
            local comment="${comment_pool[$(( RANDOM % pool_size ))]}"

            # Click Comment button
            local clicked
            clicked=$(fb_eval_value "(function(){var b=Array.from(document.querySelectorAll('[aria-label=\"Leave a comment\"],[aria-label=\"Comment\"],[aria-label=\"Write a comment\"]'));if(b.length<=$ci)return'none';b[$ci].click();return'ok'})()")
            [ "$clicked" = "none" ] && break
            sleep 2

            # Type comment
            fb_eval "(function(){var eds=document.querySelectorAll('[role=\"textbox\"][contenteditable=\"true\"]');for(var e of eds){var l=(e.getAttribute('aria-label')||'').toLowerCase();if(l.includes('comment')||l.includes('reply')){e.focus();document.execCommand('insertText',false,'$comment');return'ok'}}return'no'})()" > /dev/null 2>&1
            sleep 1

            # Press Enter to send
            fb_eval '(function(){var eds=document.querySelectorAll("[role=\"textbox\"][contenteditable=\"true\"]");for(var e of eds){var l=(e.getAttribute("aria-label")||"").toLowerCase();if(l.includes("comment")||l.includes("reply")){e.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",code:"Enter",keyCode:13,bubbles:true}));return"ok"}}return"no"})()' > /dev/null 2>&1

            total=$((total + 1))
            log "  Comment #$total: $comment"
            human_delay 8 15
        done
        human_delay 3 6
    done

    log "Comments complete: $total"
    echo "$total"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    cdp_check || exit 1
    fb_open || exit 1
    trap fb_close EXIT
    action="${1:-like}"
    shift || true
    case "$action" in
        like) do_like "$@" ;;
        comment) do_comment "$@" ;;
        *) echo "Usage: $0 like|comment [count] [groups]" ;;
    esac
fi
