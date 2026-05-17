---
name: boardgame-picker
description: Match a group to the right board game style by weighing player count, time, experience level, competition appetite, and social mood. Use when the user wants a fast category recommendation plus a backup option and one type to avoid.
---

# Boardgame Picker

Chinese name: 桌游选择器

## Purpose
Help a group stop overthinking and start playing by matching the table to the right board game category.
This skill is descriptive only. It does not check live catalog, pricing, or stock availability.

## Use this skill when
- The user needs a board game direction for a gathering, family table, or light social night.
- The table has mixed experience, mixed ages, or unclear taste.
- The group wants a quick category choice instead of browsing endless titles.
- The user wants a backup plan if the room energy changes.

## Inputs to collect
- Player count
- Age mix or newcomer level
- Available time
- Competition appetite
- Desired mood or atmosphere
- Tolerance for rules friction or mistakes

## Workflow
1. Read the table size, time, experience, and social mood.
2. Map the situation to board game categories such as party, cooperative, deduction, family, or strategy.
3. Recommend the best 1 to 2 categories, plus one backup and one type to avoid.
4. Add mechanism keywords and classic example directions when useful.
5. End with one fast-start suggestion so the group can begin tonight.

## Output Format
- Table snapshot
- Recommended types with reasons
- Backup type
- Avoid this round
- Quick start suggestion

## Quality bar
- The recommendation must match players, time, and rules tolerance.
- Explanations must say why a category fits, not just list titles.
- Include at least one low-friction way to start quickly.
- Stay realistic when the table has mixed ages or mixed experience.

## Edge cases and limits
- If the user asks for exact titles, only offer common example directions, not a live database recommendation.
- If age or skill gaps are large, prefer easy-to-explain formats over clever but fragile ones.
- This skill does not guarantee a specific title is available in the room.

## Compatibility notes
- Works for family, friends, party, and parent-child situations.
- Can pair conceptually with gaming-session-scheduler or co-op-mission-planner.
- Fully dialogue-based, no real-time API required.
