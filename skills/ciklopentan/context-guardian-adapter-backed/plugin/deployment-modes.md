# Deployment Modes

## Plugin wrapper

Recommended when the host can call a local adapter command around major actions.
This is the preferred OpenClaw path for this package.

## Sidecar

Recommended when orchestration or container boundaries make direct hooks awkward.
The sidecar still owns durable storage and the same adapter contract.

## Middleware wrapper

Recommended when an existing task runner already has well-defined entry and exit points.

## Selection rule

If multiple paths are possible, choose the smallest external adapter that can provide:
- durable state read/write
- summary read/write
- pressure input
- halt path
- resume entrypoint

Do not choose a path that requires patching OpenClaw core if an external adapter path can satisfy the contract.
