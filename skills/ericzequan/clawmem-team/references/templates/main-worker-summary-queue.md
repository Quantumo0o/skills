# Main Worker Summary Queue Template

Use this reference when a user wants the current ClawMem Team demo shape moved out of the plugin and into an external template.

## Best fit

Use this template when:
- one agent should coordinate
- one or more worker agents should execute
- work should be visible in a shared queue repo
- task status should advance through an explicit label protocol

## Recommended protocol

This template may use a protocol like:
- `queue:task`
- `task-status:todo`
- `task-status:handling`
- `task-status:blocked`
- `task-status:done`
- `assignee:<agent-id>`

These labels belong to this template, not to the ClawMem plugin.

## Recommended blueprint shape

Define:
- one main agent
- one or more worker agents
- one shared summary queue repo
- optional private or project repos for deeper execution work

## Bootstrap path

1. Confirm the participating agents.
2. Confirm the org boundary and who owns the queue repo.
3. Create or reuse the summary queue repo.
4. Create or reuse the team and grants.
5. Write the template contract into the canonical Team artifact.
6. Seed one queue issue to prove the flow works.

## Demo flow

One minimal demo should show:
1. main agent creates a queue task
2. worker agent starts work and adds a progress comment
3. worker agent posts the result
4. queue status moves to `task-status:done`

That is enough to prove the Team works.
