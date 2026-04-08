#!/bin/bash
# Unit tests for fb-local-lead-sniper
# Tests script loading, argument parsing, template loading, and helper functions
# Does NOT require CDP or Facebook (mocked where needed)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../templates" && pwd)"

PASS=0
FAIL=0

assert_eq() {
    local desc="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc (expected='$expected', got='$actual')"
        FAIL=$((FAIL + 1))
    fi
}

assert_contains() {
    local desc="$1" needle="$2" haystack="$3"
    if echo "$haystack" | grep -q "$needle"; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc (expected to contain '$needle')"
        FAIL=$((FAIL + 1))
    fi
}

assert_file_exists() {
    local desc="$1" path="$2"
    if [ -f "$path" ]; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc (file not found: $path)"
        FAIL=$((FAIL + 1))
    fi
}

assert_nonzero() {
    local desc="$1" value="$2"
    if [ -n "$value" ] && [ "$value" != "0" ]; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc (value is empty or zero)"
        FAIL=$((FAIL + 1))
    fi
}

# ========== Test 1: File structure ==========
echo "=== Test: File Structure ==="
assert_file_exists "SKILL.md exists" "$(dirname "$SCRIPT_DIR")/SKILL.md"
assert_file_exists "fb-ops.sh exists" "$SCRIPT_DIR/fb-ops.sh"
assert_file_exists "cdp-helpers.sh exists" "$SCRIPT_DIR/cdp-helpers.sh"
assert_file_exists "join.sh exists" "$SCRIPT_DIR/join.sh"
assert_file_exists "engage.sh exists" "$SCRIPT_DIR/engage.sh"
assert_file_exists "post.sh exists" "$SCRIPT_DIR/post.sh"
assert_file_exists "analyze.sh exists" "$SCRIPT_DIR/analyze.sh"

# ========== Test 2: Templates valid JSON ==========
echo ""
echo "=== Test: Template JSON Validity ==="
for tpl in comments.json life-posts.json bait-posts.json dm-scripts.json; do
    assert_file_exists "$tpl exists" "$TEMPLATE_DIR/$tpl"
    if python3 -c "import json;json.load(open('$TEMPLATE_DIR/$tpl'))" 2>/dev/null; then
        echo "  PASS: $tpl is valid JSON"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $tpl is invalid JSON"
        FAIL=$((FAIL + 1))
    fi
done

# ========== Test 3: Template content ==========
echo ""
echo "=== Test: Template Content ==="

comment_count=$(python3 -c "import json;print(len(json.load(open('$TEMPLATE_DIR/comments.json'))))")
assert_nonzero "comments.json has entries" "$comment_count"

life_count=$(python3 -c "import json;print(len(json.load(open('$TEMPLATE_DIR/life-posts.json'))))")
assert_nonzero "life-posts.json has entries" "$life_count"

bait_trades=$(python3 -c "import json;d=json.load(open('$TEMPLATE_DIR/bait-posts.json'));print(len(d))")
assert_nonzero "bait-posts.json has trade categories" "$bait_trades"

bait_has_general=$(python3 -c "import json;d=json.load(open('$TEMPLATE_DIR/bait-posts.json'));print('yes' if 'general' in d else 'no')")
assert_eq "bait-posts.json has 'general' category" "yes" "$bait_has_general"

bait_templates=$(python3 -c "import json;d=json.load(open('$TEMPLATE_DIR/bait-posts.json'));print(len(d.get('general',{})))")
assert_nonzero "general has template types" "$bait_templates"

dm_keys=$(python3 -c "import json;d=json.load(open('$TEMPLATE_DIR/dm-scripts.json'));print(','.join(sorted(d.keys())))")
assert_contains "dm-scripts has warm_intro" "warm_intro" "$dm_keys"
assert_contains "dm-scripts has cta" "cta" "$dm_keys"
assert_contains "dm-scripts has follow_up" "follow_up" "$dm_keys"

# ========== Test 4: Script sourcing (syntax check) ==========
echo ""
echo "=== Test: Script Syntax ==="
for script in cdp-helpers.sh join.sh engage.sh post.sh analyze.sh; do
    if bash -n "$SCRIPT_DIR/$script" 2>/dev/null; then
        echo "  PASS: $script syntax OK"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $script has syntax errors"
        FAIL=$((FAIL + 1))
    fi
done

# fb-ops.sh needs args to not error, just check syntax
if bash -n "$SCRIPT_DIR/fb-ops.sh" 2>/dev/null; then
    echo "  PASS: fb-ops.sh syntax OK"
    PASS=$((PASS + 1))
else
    echo "  FAIL: fb-ops.sh has syntax errors"
    FAIL=$((FAIL + 1))
fi

# ========== Test 5: Help output ==========
echo ""
echo "=== Test: CLI Help ==="
help_output=$(bash "$SCRIPT_DIR/fb-ops.sh" help 2>&1 || true)
assert_contains "help shows usage" "Usage" "$help_output"
assert_contains "help shows join action" "join" "$help_output"
assert_contains "help shows warm action" "warm" "$help_output"
assert_contains "help shows bait action" "bait" "$help_output"
assert_contains "help shows analyze action" "analyze" "$help_output"

# ========== Test 6: cdp-helpers function definitions ==========
echo ""
echo "=== Test: Helper Functions ==="
source "$SCRIPT_DIR/cdp-helpers.sh"

# Test human_delay function exists
if type human_delay &>/dev/null; then
    echo "  PASS: human_delay function defined"
    PASS=$((PASS + 1))
else
    echo "  FAIL: human_delay function not defined"
    FAIL=$((FAIL + 1))
fi

# Test log function
log_output=$(log "test message" 2>&1)
assert_contains "log includes timestamp" ":" "$log_output"
assert_contains "log includes message" "test message" "$log_output"

# Test fb_check_rate_limit exists
if type fb_check_rate_limit &>/dev/null; then
    echo "  PASS: fb_check_rate_limit function defined"
    PASS=$((PASS + 1))
else
    echo "  FAIL: fb_check_rate_limit function not defined"
    FAIL=$((FAIL + 1))
fi

# ========== Test 7: Bait template rendering ==========
echo ""
echo "=== Test: Bait Template Rendering ==="
rendered=$(python3 -c "
import json, random
data = json.load(open('$TEMPLATE_DIR/bait-posts.json'))
tpl = data['general']['urgent'][0]
print(tpl.replace('{trade}', 'plumber'))
" 2>/dev/null)
assert_contains "rendered bait has trade name" "plumber" "$rendered"
assert_contains "rendered bait is a question" "?" "$rendered"

# ========== Test 8: SKILL.md metadata ==========
echo ""
echo "=== Test: SKILL.md Metadata ==="
skill_content=$(cat "$(dirname "$SCRIPT_DIR")/SKILL.md")
assert_contains "SKILL.md has name" "fb-local-lead-sniper" "$skill_content"
assert_contains "SKILL.md has description" "Facebook local group" "$skill_content"
assert_contains "SKILL.md has version" "1.0.0" "$skill_content"
assert_contains "SKILL.md has web-access requirement" "web-access" "$skill_content"

# ========== Summary ==========
echo ""
echo "================================"
echo "  Results: $PASS passed, $FAIL failed"
echo "================================"

[ $FAIL -eq 0 ] && exit 0 || exit 1
