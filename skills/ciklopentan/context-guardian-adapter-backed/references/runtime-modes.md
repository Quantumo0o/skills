# Runtime Modes

Use exactly one mode label for each deployment.
Do not mix claims across modes.

## advisory

Use this mode when only the skill text and reference files are active.

Characteristics:
- best-effort guidance
- manual or low-risk usage
- no hard halt/resume guarantee
- no claim that durable state is enforced by runtime

Allowed claims:
- checkpoint discipline guidance
- summary structure guidance
- recovery procedure guidance

Forbidden claims:
- guaranteed durable persistence
- guaranteed stop-on-critical behavior
- guaranteed resumability after restart

## adapter-backed

Use this mode when an external adapter/plugin/wrapper/sidecar implements the contract.
This is the recommended default production mode.

Characteristics:
- durable state outside chat history
- durable summary persistence
- explicit halt path
- explicit resume entrypoint
- adapter-owned pressure input
- one major action per checkpoint cycle
- optional official OpenClaw native hook-only plugin integration without core patch

Required claim:
- production continuity comes from installable skill + external adapter-backed deployment

## core-embedded

Use this label only for a future architecture where continuity behavior is directly embedded in host runtime.
This mode is optional.
This package does not require it.
This package must remain publishable and useful without it.
