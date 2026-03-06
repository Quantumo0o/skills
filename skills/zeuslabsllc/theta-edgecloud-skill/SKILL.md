---
name: theta-edgecloud-skill
description: Runtime-safe Theta EdgeCloud cloud API scaffold (deployment, inference, video, on-demand) with dry-run safety.
metadata:
  openclaw:
    primaryEnv: THETA_EC_API_KEY
    requires:
      env:
        - THETA_EC_API_KEY
        - THETA_EC_PROJECT_ID
        - THETA_INFERENCE_ENDPOINT
        - THETA_INFERENCE_AUTH_USER
        - THETA_INFERENCE_AUTH_PASS
        - THETA_ONDEMAND_API_TOKEN
        - THETA_VIDEO_SA_ID
        - THETA_VIDEO_SA_SECRET
        - THETA_DRY_RUN
        - THETA_HTTP_TIMEOUT_MS
        - THETA_HTTP_MAX_RETRIES
        - THETA_HTTP_RETRY_BACKOFF_MS
---

# Theta EdgeCloud Skill (Cloud API Runtime)

This runtime artifact is scoped to cloud API operations only.

## Security behavior (explicit)
- Runtime command handlers do not execute local shell commands.
- Runtime does not read local files for upload operations.
- Runtime does not call localhost/default local RPC endpoints.
- Runtime secret resolution uses OpenClaw secret provider first, then env fallback (for `THETA_ONDEMAND_API_TOKEN`).
- Paid/mutating operations are user-triggered and can be gated by `THETA_DRY_RUN=1`.

## What is wired
- EdgeCloud deployment controller API
- Dedicated inference endpoint (OpenAI-compatible)
- Theta Video API
- Theta On-demand Model API (`ondemand.thetaedgecloud.com`)

## Runtime-only package
This ClawHub artifact is a dist/docs bundle intended for transparent inspection and low scanner surface.

## Env knobs (selected)
- `THETA_DRY_RUN`
- `THETA_EC_API_KEY`
- `THETA_EC_PROJECT_ID`
- `THETA_INFERENCE_ENDPOINT`
- `THETA_ONDEMAND_API_TOKEN`
- `THETA_HTTP_TIMEOUT_MS`
- `THETA_HTTP_MAX_RETRIES`
- `THETA_HTTP_RETRY_BACKOFF_MS`
