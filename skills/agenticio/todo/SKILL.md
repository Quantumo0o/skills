---
name: todo
description: Task and project management with priority-based organization and context-aware surfacing. Use when user mentions tasks, to-do lists, projects, commitments, deadlines, or prioritization. Captures tasks from any context, organizes by urgency/importance, surfaces work based on context and energy, tracks commitments to others, and maintains weekly review system. All data stored locally.
---

# Todo

Task and project system. Capture everything, do what matters.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All task data stored locally only**: `memory/todo/`
- **No external task apps** connected
- **No cloud sync** - pure local storage
- **No sharing** of tasks or projects
- User controls all data retention and deletion

### Data Structure
Tasks stored in your local workspace:
- `memory/todo/tasks.json` - All tasks and priorities
- `memory/todo/projects.json` - Project definitions and next actions
- `memory/todo/commitments.json` - Commitments to/from others
- `memory/todo/contexts.json` - Context definitions (energy, location, time)
- `memory/todo/reviews.json` - Weekly review history

## Core Workflows

### Capture Task
```
User: "Call the accountant before Thursday"
→ Use scripts/add_task.py --task "Call accountant" --deadline "2024-03-14" --context phone
→ Extract task, identify deadline, store for later
```

### Prioritize Tasks
```
User: "What should I work on now?"
→ Use scripts/what_next.py --energy high --time 120 --location desk
→ Surface tasks matching current context and energy
```

### Track Commitment
```
User: "I promised Sarah I'd send the report by Friday"
→ Use scripts/add_commitment.py --to "Sarah" --what "Send report" --deadline "2024-03-15"
→ Track commitment with deadline and reminder
```

### Weekly Review
```
User: "Run my weekly review"
→ Use scripts/weekly_review.py
→ Guide through closing completed, updating projects, capturing new items
```

### Close Day
```
User: "Close out my day"
→ Use scripts/close_day.py
→ Review what was done, capture loose ends, set up tomorrow
```

## Module Reference
- **Capture System**: See [references/capture.md](references/capture.md)
- **Priority Framework**: See [references/priority.md](references/priority.md)
- **Context & Energy**: See [references/context.md](references/context.md)
- **Commitments**: See [references/commitments.md](references/commitments.md)
- **Weekly Review**: See [references/weekly-review.md](references/weekly-review.md)
- **Projects vs Tasks**: See [references/projects.md](references/projects.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `add_task.py` | Capture new task |
| `what_next.py` | Surface right task for context |
| `add_commitment.py` | Track commitment to someone |
| `weekly_review.py` | Run weekly review |
| `close_day.py` | End-of-day routine |
| `complete_task.py` | Mark task complete |
| `add_project.py` | Create new project |
| `set_context.py` | Define context parameters |
