---
name: hbm-memory-system
description: |
  HBM Memory System - A comprehensive local memory management system for OpenClaw.
  Includes five core memory banks, semantic search, RAG optimization, and heartbeat recall.
  Use when user mentions memory, recall, HBM, memory banks, or needs to manage personal memory system.
---

# HBM Memory System Skill

This skill provides guidance for managing the HBM (Human Brain Model) memory system in OpenClaw.

## Overview

The HBM project is a modular memory system consisting of five core memory banks:

1. **Goals Memory Bank** (`memory/目标记忆库/GOALS.md`) - Tracks user goals (completed/ongoing/pending)
2. **Session Memory Bank** (`memory/会话记忆库/YYYY-MM-DD.md`) - Daily conversation summaries
3. **Version Memory Bank** (`memory/版本记忆库/CHANGELOG.md`) - System change and upgrade records
4. **Experience Memory Bank** (`memory/经验记忆库/TIPS.md`) - Technical problem-solving experiences
5. **Emotion Memory Bank** (`memory/情感记忆库/DAILY_EMOTIONS.md`) - User emotion and habit tracking

Additional components:
- **Semantic Search Database** (`memory/语义搜索_db/`) - ChromaDB vector database for natural language queries
- **Heartbeat Recall System** (`memory/心跳回忆/`) - Human-like interaction mechanism
- **RAG Optimization** - Retrieval Augmented Generation combining memory banks with AI generation

## How to Use

### Accessing Memory Banks

Use the following commands to read memory banks:

```bash
# View today's session record
cat memory/会话记忆库/$(date +%Y-%m-%d).md

# View current goals
cat memory/目标记忆库/GOALS.md

# View technical experiences
cat memory/经验记忆库/TIPS.md

# View emotion records
cat memory/情感记忆库/DAILY_EMOTIONS.md

# View version history
cat memory/版本记忆库/CHANGELOG.md
```

### Using Semantic Search

The semantic search system allows natural language queries across all memory banks:

```bash
# Use the memory_search tool (via OpenClaw)
memory_search "query about previous work"

# Then use memory_get to retrieve specific snippets
memory_get "path/to/memory/file.md" from=10 lines=5
```

### Heartbeat Recall System

The heartbeat recall system provides human-like interaction by occasionally asking memory-related questions:

- Trigger conditions: Daily conversations, task completion, 3-day unmentioned goals
- Frequency: Limited to 3 times per day (excluding holidays)
- Style: Uses single ❤️ emoji, concise and focused

### RAG Optimization

The RAG system enhances responses by retrieving relevant information from memory banks:

- Token limit control: Configurable result count and deduplication
- Speed optimization: Memory caching mechanism
- Log management: Monthly automatic compression

## Maintenance Tasks

### Daily Tasks (see HEARTBEAT.md)

- Check if yesterday's session record was generated
- Check for version logs needing archiving
- Check memory banks for user feedback areas
- Check for overdue goals requiring reminders
- Check for unrecorded emotional fluctuations

### Weekly Tasks

- Review weekly experiences every Sunday
- Clean temporary files
- Check storage space

### Monthly Tasks

- Archive old session records (keep last 3 months)
- Backup memory data
- Generate monthly memory review report

## Scripts

The `scripts/local_memory_system_v2.py` script provides command-line utilities for managing the memory system:

```bash
# Start interactive interface
python3 scripts/local_memory_system_v2.py

# Add new experience
add_exp "Problem description" "Solution details" --highlight

# Add new goal
add_goal "New goal" "Background reason" "Temporary solution"

# Semantic search
search "keywords"
```

## Important Notes

- **Privacy**: Memory banks contain personal data. Do not share in group chats.
- **Security**: Never record passwords or API keys in memory files.
- **Backup**: Regular backups are recommended (automated via cron).
- **Token Management**: Be mindful of token usage when retrieving large memory sections.

## References

- `MEMORY.md` - Complete memory system overview
- `HEARTBEAT.md` - Periodic task checklist
- `memory/` - Directory structure and data files

---
*This skill is part of the HBM project, designed to make OpenClaw more personalized and context-aware.*