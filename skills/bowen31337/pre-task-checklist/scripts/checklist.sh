#!/bin/bash
# Pre-task checklist verification script

verify() {
    local query="$1"
    echo "🔍 Verifying: $query"
    
    # Try memory search if available
    if command -v memory_search &> /dev/null; then
        memory_search "$query" 2>/dev/null | head -5
    fi
    
    echo "📖 Reference files to check:"
    echo "  - ~/.openclaw/workspace/TOOLS.md"
    echo "  - ~/.openclaw/workspace/AGENTS.md"
    echo "  - ~/.openclaw/workspace/SOUL.md"
    echo "  - ~/.openclaw/workspace/MEMORY.md"
}

run_checklist() {
    echo "=== 📋 PRE-TASK CHECKLIST ==="
    echo ""
    
    echo "1️⃣  What task are you about to start?"
    read -r task
    echo "   → Task: $task"
    echo ""
    
    echo "2️⃣  Searching memory for similar tasks..."
    if command -v memory_search &> /dev/null; then
        memory_search "$task" 2>/dev/null | head -10
        echo "   ✅ Memory search complete"
    else
        echo "   ⚠️  memory_search not available - check files manually"
    fi
    echo ""
    
    echo "3️⃣  Read reference files? (y/n)"
    read -r ref_files
    if [ "$ref_files" = "y" ]; then
        echo "   Which files? (space-separated paths)"
        read -r files
        for file in $files; do
            if [ -f "$file" ]; then
                echo "   📖 $file:"
                head -50 "$file"
            else
                echo "   ❌ File not found: $file"
            fi
        done
    fi
    echo ""
    
    echo "4️⃣  Verify critical details? (y/n)"
    read -r verify_details
    if [ "$verify_details" = "y" ]; then
        echo "   What to verify? (IP, path, format, etc.)"
        read -r verify_what
        verify "$verify_what"
    fi
    echo ""
    
    echo "5️⃣  Check rules in AGENTS.md/SOUL.md? (y/n)"
    read -r check_rules
    if [ "$check_rules" = "y" ]; then
        echo "   📖 AGENTS.md:"
        grep -i "rule\|must\|never\|required" ~/.openclaw/workspace/AGENTS.md 2>/dev/null | head -20
        echo ""
        echo "   📖 SOUL.md:"
        grep -i "rule\|must\|never\|required" ~/.openclaw/workspace/SOUL.md 2>/dev/null | head -20
    fi
    echo ""
    
    echo "=== ✅ CHECKLIST COMPLETE ==="
    echo "Proceed with task? (y/n)"
    read -r proceed
    if [ "$proceed" = "y" ]; then
        echo "✅ Proceeding with verified context"
        return 0
    else
        echo "❌ Task aborted - need more verification"
        return 1
    fi
}

# Quick verify (single item)
quick_verify() {
    local item="$1"
    local search_term="$2"
    
    echo "🔍 Quick verify: $item"
    
    # Search TOOLS.md
    if [ -f ~/.openclaw/workspace/TOOLS.md ]; then
        echo "📖 TOOLS.md:"
        grep -i "$search_term" ~/.openclaw/workspace/TOOLS.md | head -5
    fi
    
    # Search MEMORY.md
    if [ -f ~/.openclaw/workspace/MEMORY.md ]; then
        echo "📖 MEMORY.md:"
        grep -i "$search_term" ~/.openclaw/workspace/MEMORY.md | head -5
    fi
    
    echo "✅ Verification complete"
}

# Export functions
export -f verify
export -f run_checklist
export -f quick_verify

echo "✅ Pre-task checklist functions loaded"
echo "  - run_checklist: Full interactive checklist"
echo "  - verify <query>: Search memory and show reference files"
echo "  - quick_verify <item> <search_term>: Quick verification"
