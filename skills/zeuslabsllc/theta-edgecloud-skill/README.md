# Theta EdgeCloud Skill (Cloud API Runtime Artifact)

This is a dist-only runtime artifact for ClawHub scanning/install path validation.

## Scope
- Cloud API operations only (`deployment`, `inference`, `video`, `on-demand`).
- No local RPC command surface in this artifact.
- No local file upload/read command surface in this artifact.

## Security posture
- No shell scripts included.
- Runtime does not execute local shell commands.
- Runtime does not read local files for uploads.
- Network calls target explicit Theta cloud endpoints required by the command.

## Notes
Bring your own credentials and endpoint configuration via environment variables.
For safer testing, set `THETA_DRY_RUN=1`.
