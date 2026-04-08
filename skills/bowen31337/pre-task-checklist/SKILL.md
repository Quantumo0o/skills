---
name: pre-task-checklist
description: >
  Mandatory pre-task verification protocol to prevent forgetfulness, stale data errors,
  and context loss. Use when: (1) starting any non-trivial task, (2) before using
  stored credentials/IPs/paths, (3) when context feels uncertain, (4) after context
  window compaction, (5) any mention of "verify", "check", "confirm", "did I remember".
  Triggers on: "before I start", "pre-task", "verify this", "check if I remembered",
  "am I missing something", "did I forget".
---

# Pre-Task Checklist

**Never guess. Never assume. Always verify.**

## The Problem

Agents forget things when:
- MEMORY.md has stale data (old IPs, wrong paths, expired tokens)
- Context window compaction loses recent details
- Multiple concurrent sub-agents fragment attention
- New tasks override previous context

**Result**: Wrong IPs, incorrect formats, missed rules, repeated mistakes.

## The Solution

**Mandatory pre-task checklist** before ANY non-trivial task:

```
1. memory_search() for relevant patterns
2. Read reference files directly (don't assume)
3. Verify critical details in real-time
4. Check AGENTS.md / SOUL.md for rules
```

## Quick Start

```bash
# Before starting a task
source ~/.openclaw/workspace/skills/pre-task-checklist/scripts/checklist.sh

# Verify a specific detail (IP, path, format)
verify "GPU server IP"
verify "MBD article format"

# Full checklist (interactive)
run_checklist
```

## Checklist Items

### 1. Memory Search
```bash
# Search for relevant patterns
memory_search "GPU server IP address"
memory_search "MBD article format"
memory_search "folder naming convention"
```

**What to look for**:
- Previous examples of this task
- Correct IPs, paths, formats
- Rules or constraints
- Past mistakes to avoid

### 2. Read Reference Files
```bash
# Read actual examples, don't assume
cat /tmp/mbd-book-ideas/2026-03-11_懒人理财经_AI替你管钱躺赚不是梦/文章.md
cat ~/.openclaw/workspace/TOOLS.md
cat ~/.openclaw/workspace/AGENTS.md
```

**What to verify**:
- Format and structure
- Tone and style
- Technical requirements
- Examples to follow

### 3. Verify Critical Details
```bash
# Check live data, don't trust memory
ssh peter@10.0.0.30 "echo 'connected'"  # Verify IP works
ls -la /path/to/file                     # Verify path exists
cat ~/.openclaw/workspace/TOOLS.md       # Verify current value
```

**What to verify**:
- IPs and hostnames
- File paths and URLs
- API keys and tokens (check expiry)
- Configuration values

### 4. Check Rules
```bash
# Read rule files before acting
cat ~/.openclaw/workspace/AGENTS.md      # Check project rules
cat ~/.openclaw/workspace/SOUL.md        # Check identity/rules
cat ~/.openclaw/workspace/HEARTBEAT.md   # Check recurring tasks
```

**What to check**:
- "No pause" rule - execute immediately
- Repo ownership (clawinfra vs AlexChen31337)
- Publish gates (MbD needs explicit approval)
- Safety/security rules

## Examples

### Example 1: GPU Server Access
❌ **Wrong** (guessing):
```
ssh peter@10.0.0.44  # WRONG IP from stale memory
```

✅ **Right** (verifying):
```bash
# Step 1: Search memory
memory_search "GPU server IP"
# → Returns: "10.0.0.44" (STALE!)

# Step 2: Verify in TOOLS.md
cat ~/.openclaw/workspace/TOOLS.md | grep "GPU Server"
# → Shows: "peter@10.0.0.30" (CURRENT!)

# Step 3: Test connection
ssh peter@10.0.0.30 "hostname"
# → Works!

# Step 4: Update memory
# (Correct the stale data)
```

### Example 2: MBD Article Format
❌ **Wrong** (assuming):
```
# Write 8,000-word academic whitepaper
```

✅ **Right** (verifying):
```bash
# Step 1: Search memory
memory_search "MBD article word count"
# → Returns: "3,000-4,500 words"

# Step 2: Read example
cat /tmp/mbd-book-ideas/2026-03-11_懒人理财经_AI替你管钱躺赚不是梦/文章.md
# → See conversational tone, chapter structure

# Step 3: Check rules
cat AGENTS.md | grep -A5 "MbD publish"
# → "MbD: NEVER publish without explicit 'publish to MbD'"

# Step 4: Follow format
# Write 4,000 words, conversational style
```

### Example 3: GitHub Repo Ownership
❌ **Wrong** (assuming):
```
gh repo create clawinfra/my-repo  # WRONG!
```

✅ **Right** (verifying):
```bash
# Step 1: Check rules
cat AGENTS.md | grep -A10 "GitHub Repo Ownership"
# → "clawinfra/ ONLY for ClawChain, EvoClaw, core infrastructure"
# → "AlexChen31337/ for research, tools, benchmarks"

# Step 2: Classify repo
# My tool is NOT core infrastructure → use AlexChen31337

# Step 3: Create in correct org
gh repo create AlexChen31337/my-repo
```

## Consequences for Violations

**When you skip the checklist and make a mistake**:

1. **Acknowledge immediately**
   - "I forgot to verify X"
   - "I assumed Y instead of checking"

2. **Write to WAL**
   ```bash
   uv run python skills/agent-self-governance/scripts/wal.py append main \
     --type checklist_violation \
     "Failed to verify GPU server IP. Used 10.0.0.44 (stale) instead of 10.0.0.30 (current)."
   ```

3. **Correct before continuing**
   - Fix the mistake
   - Update stale data
   - Verify the fix works

4. **Identify root cause**
   - Why did I skip verification?
   - Was I rushed?
   - Did I feel confident when I shouldn't have?

## Integration with Other Skills

### agent-motivator
- **agent-motivator**: "Push harder, don't give up"
- **pre-task-checklist**: "Verify before you push"

Use together:
1. Run pre-task-checklist to verify the approach
2. Use agent-motivator to push through obstacles

### rsi-loop
- **rsi-loop**: Log outcomes and improve
- **pre-task-checklist**: Prevent mistakes before they happen

Use together:
1. Run pre-task-checklist before task
2. Log outcome with rsi-loop after task
3. Update checklist based on learnings

### skill-creator
When creating new skills, include a "Verification" section that references this checklist.

## Verification Scripts

### Quick Verify Function
```bash
# Add to ~/.bashrc or source directly
verify() {
    local query="$1"
    echo "🔍 Verifying: $query"
    memory_search "$query" | head -5
    echo "📖 Check reference files for: $query"
}
```

### Full Checklist Script
```bash
run_checklist() {
    echo "=== PRE-TASK CHECKLIST ==="
    echo "1. What task am I doing?"
    read task
    echo "2. Search memory for: $task"
    memory_search "$task" | head -10
    echo "3. Read reference files? (y/n)"
    read ref_files
    if [ "$ref_files" = "y" ]; then
        echo "Which files?"
        read files
        cat $files
    fi
    echo "4. Verify critical details? (y/n)"
    read verify_details
    if [ "$verify_details" = "y" ]; then
        echo "What to verify?"
        read verify_what
        verify "$verify_what"
    fi
    echo "5. Check rules? (y/n)"
    read check_rules
    if [ "$check_rules" = "y" ]; then
        cat ~/.openclaw/workspace/AGENTS.md
    fi
    echo "=== CHECKLIST COMPLETE ==="
    echo "Proceed with task? (y/n)"
    read proceed
    if [ "$proceed" = "y" ]; then
        echo "✅ Proceeding with verified context"
    else
        echo "❌ Task aborted - need more verification"
    fi
}
```

## Teaching Agents to Use This Skill

When spawning sub-agents, include this in the prompt:

```python
sessions_spawn(
    runtime="subagent",
    task=f"""
    Task: {task_description}
    
    MANDATORY PRE-TASK CHECKLIST:
    1. Search memory for similar tasks
    2. Read reference files (don't assume)
    3. Verify critical details (IPs, paths, formats)
    4. Check rules in AGENTS.md/SOUL.md
    
    Start by running the checklist and reporting what you found.
    Then proceed with the task.
    """
)
```

## Common Pitfalls

### Pitfall 1: "I Remember This"
**Thought**: "I used the GPU server yesterday, I know the IP"
**Problem**: Memory might be stale
**Fix**: Verify in TOOLS.md or test connection

### Pitfall 2: "This Is Obvious"
**Thought**: "Everyone knows MBD articles are 8,000 words"
**Problem**: Assumptions are wrong
**Fix**: Read an actual MBD article example

### Pitfall 3: "I'll Check Later"
**Thought**: "Let me just start, I'll verify the IP later"
**Problem**: You'll forget, and errors will compound
**Fix**: Verify BEFORE starting

### Pitfall 4: "Searching Takes Too Long"
**Thought**: "This will add 2 minutes to every task"
**Problem**: One mistake costs 10+ minutes to fix
**Fix**: 2 minutes now vs 10 minutes later

## When to Skip the Checklist

Only for trivial tasks:
- "What time is it?"
- "Send this message"
- "Read this file"
- "List running processes"

**Never skip for**:
- Using IPs, paths, URLs
- Writing to files
- Publishing content
- Deploying code
- Spawning sub-agents
- Financial operations
- Security-sensitive actions

## Success Metrics

Track your improvement:
- **Week 1**: Checklist on every task (100%)
- **Week 2**: Checklist on 50% of tasks (build intuition)
- **Week 3**: Checklist on 20% of tasks (only complex/uncertain)
- **Week 4**: Checklist becomes automatic habit

**Goal**: Zero mistakes from stale data or forgotten rules.

---

**Remember**: The 2 minutes you spend verifying saves 20 minutes fixing mistakes.

**When in doubt**: CHECK. When confident: CHECK AGAIN.
