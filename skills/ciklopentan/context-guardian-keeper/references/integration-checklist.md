# Integration Checklist

- [ ] Identify the planner entry point.
- [ ] Identify the tool runner entry point.
- [ ] Identify any existing memory module.
- [ ] Load the latest task state at session start.
- [ ] Load the latest structured summary at session start.
- [ ] Rebuild the working bundle before each major model call.
- [ ] Update task state after each planner step.
- [ ] Update task state after each file write or code patch.
- [ ] Write a checkpoint before any destructive action.
- [ ] Write a checkpoint when context pressure enters warning/compress/critical levels.
- [ ] Stop autonomous execution at critical pressure if state confidence is low.
- [ ] Ask for confirmation instead of improvising when recovery confidence is low.
- [ ] Append an event log entry after each major action.
- [ ] Keep configuration and filesystem paths configurable.
- [ ] Keep the module framework-agnostic.
