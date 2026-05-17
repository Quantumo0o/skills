# Exec Hygiene — Context Blowup Prevention

Subagents accumulate context from every exec result. Verbose output (docker builds, npm installs, long logs) can blow past the compaction threshold and hang the channel. **Always apply these rules.**

## Mandatory Exec Filtering Patterns

```bash
# Build/install output — tail only
docker build ... 2>&1 | tail -20
pip install ... 2>&1 | tail -10
npm install ... 2>&1 | tail -10

# Log scanning — grep for signal
journalctl -u myservice 2>&1 | grep -E 'ERROR|WARN|Started|Failed' | tail -20

# File listings — bounded
find . -name "*.py" | head -30

# Test output — summary only
pytest ... 2>&1 | tail -20

# Any command that might produce >100 lines — always pipe through tail or grep
```

**Rule of thumb:** If a command produces >50 lines, it must be filtered.

## runTimeoutSeconds Defaults

**Always set `runTimeoutSeconds`** when spawning workers. Never leave it at 0 (unlimited).

| Task type | Recommended timeout |
|-----------|-------------------|
| File ops, git, quick scripts | 120s |
| Tests, builds, installs | 300s |
| Multi-step deploy/infra | 600s |
| Research + write tasks | 300s |

Omitting `runTimeoutSeconds` is the primary cause of runaway context blowup.

## Model Selection

**Exec-heavy workers must use `model: "anthropic/claude-sonnet-4-6"`** — do not inherit the caller's model (which may be Opus).

| Worker type | Model |
|-------------|-------|
| Exec / build / deploy / infra | `anthropic/claude-sonnet-4-6` |
| Research / analysis / writing | inherit (caller's model) |
| Code review / complex reasoning | inherit (caller's model) |

Set this explicitly in `sessions_spawn`:
```
sessions_spawn(task=..., model="anthropic/claude-sonnet-4-6", runTimeoutSeconds=300)
```
