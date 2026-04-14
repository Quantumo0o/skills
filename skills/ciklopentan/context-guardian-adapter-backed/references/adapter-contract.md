# External Adapter Contract

This contract defines the external execution layer required for `adapter-backed` mode.
The adapter may be a plugin, wrapper, middleware layer, or sidecar.
It must live outside OpenClaw core patches.

## Required capabilities

The adapter must provide all of these:
- durable state read
- durable state write
- summary read
- summary write
- pressure provider
- stop/halt path
- resume entrypoint

## Required hook points

The adapter must implement these hook points:
- `before_major_action`
- `after_major_action`
- `after_state_mutation`
- `before_destructive_action`
- `on_failure`
- `on_resume`
- `on_stop_signal`

## Required behavior

Run this order exactly:

1. load latest durable state
2. load latest summary
3. read pressure
4. if critical -> checkpoint + summary + halt
5. build working bundle
6. allow exactly one checkpointable major action
7. persist state
8. refresh summary when required
9. continue or stop explicitly

## Semantic rules

- The adapter owns the authoritative storage path configuration.
- The adapter must not depend on transient prompt state as the sole continuity source.
- The adapter must not depend on ephemeral container layers as the sole continuity source.
- The adapter must surface halt and completion as explicit signals, not hidden log lines.
- The adapter must resume from the latest durable state, not from guessed chat reconstruction.
- The adapter must downgrade to `advisory` if any required capability is missing.

## Pressure rules

- Pressure must be numeric in range `0.0` to `1.0`.
- Pressure must come from the host or adapter instrumentation layer.
- Production adapters must not ask the model to estimate its own pressure.

## Resume rules

The resume entrypoint must:
- load the latest durable state
- load the latest summary
- verify schema version
- verify `next_action`
- rebuild the working bundle from durable artifacts
- continue only if constraints still hold

## Failure rules

On failure, the adapter must:
- write updated state
- append event/log entry
- refresh summary when the plan changed or ambiguity increased
- stop instead of guessing when recovery confidence is low
