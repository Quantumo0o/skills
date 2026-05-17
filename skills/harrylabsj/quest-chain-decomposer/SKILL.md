---
name: quest-chain-decomposer
description: Break a fuzzy, high-friction goal into a sequenced quest chain with prerequisite nodes, parallel branches, waiting points, Definition of Done, and the first three actions. Use when the user knows the destination but cannot see the first move, keeps stalling mid-project, or needs a practical task map for study, home, admin, or personal projects.
---

# Quest Chain Decomposer

Chinese name: 任务链分解器.

## Overview

Use this skill to turn a large or messy objective into a practical quest chain. It keeps the first step small, shows dependencies, and avoids fake progress such as endless research without a deliverable.

## When to use

Use this skill when the user wants to:
- break a goal into a realistic sequence
- identify prerequisite, parallel, and waiting nodes
- define what “done” means for each step
- start today instead of circling the task
- re-route after blockers appear

### Example prompts
- "Break this project into a quest chain"
- "I know what I want, but I cannot find the first step"
- "Map the dependencies for this admin task"

## Inputs

Useful inputs include:
- goal or deliverable
- deadline or time window
- success definition
- resources and constraints
- blockers, approvals, or handoffs

## Workflow

1. Clarify the finish line.
2. Sort work into main quest, prerequisite nodes, parallel branches, and waiting points.
3. Give each step a clear Definition of Done.
4. Make the first move small enough to start immediately.
5. Add reroute rules for common stalls.

## Output

Return markdown with:
- main quest objective
- quest chain map
- Definition of Done by step
- starter trio
- reroute rules

## Limits

- This skill does not replace full project management software.
- For large cross-team schedules, it should stay at the planning level.
- If the goal itself is unclear, define the mission first before decomposing it.

## Acceptance Criteria

- The first quest is small enough to start now.
- Dependencies are visible.
- Each step has an explicit done line.
- The plan points toward a real deliverable, not just thinking about the work.
