# Pre-Task Checklist Skill

**Mandatory verification protocol to prevent forgetfulness and stale data errors.**

## What It Does

Before starting any task, this skill ensures you:
1. ✅ Search memory for relevant patterns
2. ✅ Read reference files (don't assume)
3. ✅ Verify critical details (IPs, paths, formats)
4. ✅ Check rules in AGENTS.md/SOUL.md

## Why You Need It

**Without verification**:
- Use wrong IP address → connection fails
- Write wrong format → content rejected
- Forget rules → mistakes happen
- Waste time fixing preventable errors

**With verification**:
- Catch errors before they happen
- Build reliable knowledge base
- Save time (2 min verify vs 20 min fix)
- Consistent quality

## Quick Start

### Bash Functions
```bash
# Load functions
source ~/.openclaw/workspace/skills/pre-task-checklist/scripts/checklist.sh

# Quick verify
verify "GPU server IP"

# Full checklist
run_checklist

# Quick verify specific item
quick_verify "GPU server" "10.0.0"
```

### Python Script
```bash
# Quick verification
python3 ~/.openclaw/workspace/skills/pre-task-checklist/scripts/verify.py verify "GPU server"

# Verify IP connectivity
python3 ~/.openclaw/workspace/skills/pre-task-checklist/scripts/verify.py ip "peter@10.0.0.30"

# Full checklist (interactive)
python3 ~/.openclaw/workspace/skills/pre-task-checklist/scripts/verify.py
```

## Examples

### Example 1: Before Using GPU Server
```bash
# Step 1: Search memory
verify "GPU server IP"

# Step 2: Check TOOLS.md
cat ~/.openclaw/workspace/TOOLS.md | grep -A2 "GPU Server"

# Step 3: Test connection
ssh peter@10.0.0.30 "hostname"

# Step 4: Now use it
ssh peter@10.0.0.30 "nvidia-smi"
```

### Example 2: Before Writing MBD Article
```bash
# Step 1: Search memory
verify "MBD article format"

# Step 2: Read example
cat /tmp/mbd-book-ideas/2026-03-11_懒人理财经_AI替你管钱躺赚不是梦/文章.md

# Step 3: Check rules
cat ~/.openclaw/workspace/AGENTS.md | grep -A5 "MbD publish"

# Step 4: Now write
# (Write 4,000 words, conversational style)
```

### Example 3: Before Creating GitHub Repo
```bash
# Step 1: Search memory
verify "GitHub repo ownership"

# Step 2: Check rules
cat ~/.openclaw/workspace/AGENTS.md | grep -A10 "GitHub Repo Ownership"

# Step 3: Classify repo
# (Is it core ClawInfra? No → use AlexChen31337)

# Step 4: Create in correct org
gh repo create AlexChen31337/my-repo
```

## Integration with Other Skills

### agent-motivator
```bash
# 1. Verify approach (pre-task-checklist)
verify "deployment process"

# 2. Push through obstacles (agent-motivator)
# (when you hit errors, don't give up)
```

### rsi-loop
```bash
# 1. Pre-task: Verify everything
run_checklist

# 2. Post-task: Log outcome
uv run python skills/rsi-loop/scripts/rsi_cli.py log \
  --task my_task --success true --quality 5
```

## When to Use

**Always use for**:
- Using IPs, paths, URLs
- Writing to files
- Publishing content
- Deploying code
- Spawning sub-agents
- Financial operations
- Security-sensitive actions

**Skip for**:
- Trivial tasks (what time is it)
- Simple queries (list files)
- Read-only operations (cat file)

## Teaching Sub-Agents

When spawning sub-agents, include verification:

```python
sessions_spawn(
    runtime="subagent",
    task=f"""
    Task: {task_description}
    
    PRE-TASK CHECKLIST:
    1. Search memory for similar tasks
    2. Read reference files (don't assume)
    3. Verify critical details (IPs, paths, formats)
    4. Check rules in AGENTS.md/SOUL.md
    
    Start by running checklist and reporting what you found.
    Then proceed with task.
    """
)
```

## Success Metrics

- **Week 1**: 100% tasks use checklist (build habit)
- **Week 2**: 50% tasks use checklist (build intuition)
- **Week 3**: 20% tasks use checklist (complex/uncertain only)
- **Week 4**: Automatic (checklist is second nature)

**Goal**: Zero mistakes from stale data or forgotten rules.

## License

MIT License - Feel free to use and modify for your agents.
