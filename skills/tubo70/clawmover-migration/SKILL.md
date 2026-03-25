---
name: clawmover-migration
description: Operate ClawMover migration from an OpenClaw-connected channel when the host machine cannot be accessed over SSH. Use this skill to verify or install the `clawmover` CLI, run migration backup or restore in two non-interactive phases, always include `--yes` to skip confirmations, ask the user for the emailed 6-digit verification code, resume the pending operation with `--verification-code`, prefer `--dest-path` for safe restore testing, and report migration, restore, and plugin reinstall results.
metadata: {"openclaw":{"requires":{"bins":["node","npm"]}}}
---

# OpenClaw Migration

Use this skill when a user wants OpenClaw to migrate an OpenClaw instance through a connected channel such as Feishu, especially when the user cannot SSH into the host machine.

Run the `clawmover` CLI on the host machine. Do not ask the user to run commands manually unless installation or execution fails and the failure cannot be handled automatically.

Current CLI behavior:

- `--non-interactive` skips the verification code prompt. If no verification code is provided, the CLI sends the code by email and exits so the workflow can resume later.
- `--yes` skips backup plan confirmation.
- `--yes` makes restore select all non-ignored tags automatically and use the default conflict strategy.
- `--dest-path` avoids restore path prompts by forcing a test restore root.

For agent-driven execution, always include both `--non-interactive` and `--yes`, and provide `--verification-code` only in phase 2 after the user replies with the 6-digit code.

## Preconditions

- Ensure the host can execute shell commands.
- Ensure `node` and `npm` are available.
- Ensure OpenClaw is installed on the host.
- Ensure the user can receive an emailed verification code.

Before migration backup or restore, ensure the user already has a valid ClawMover migration order:

- The user must create a migration order at `https://clawmover.com`.
- The user must complete payment before the `instanceId` becomes valid.
- If the user does not already have a paid migration order, tell them to create one on `https://clawmover.com` first.

Explain the required inputs clearly:

- `instanceId`: The migration instance ID created by ClawMover after the user creates and pays for a migration order on `https://clawmover.com`.
- `dataSecretKey`: The data encryption password used to encrypt and decrypt backup data. If this key is lost, the backup data cannot be recovered.

## Install Or Verify CLI

Check whether `clawmover` is installed:

```bash
clawmover --version
```

If not installed, install it:

```bash
npm install -g @clawmover/cli
clawmover --version
```

If installation fails, report the error summary and stop.

## Backup Workflow

Required inputs:

- `instanceId`
- `dataSecretKey`

Phase 1: trigger email verification and expect exit code `2`

```bash
clawmover backup --instance-id <instanceId> --data-secret-key <dataSecretKey> --non-interactive --yes
```

If the command exits with code `2`, tell the user a verification code was sent and ask them to reply with the 6-digit code.

Phase 2: resume backup with the code

```bash
clawmover backup --instance-id <instanceId> --data-secret-key <dataSecretKey> --verification-code <code> --non-interactive --yes
```

Important:

- Always include `--yes` for agent-driven backup.
- Without `--yes`, backup may stop at the backup plan confirmation prompt.

Return a short result summary:

- success or failure
- snapshot id
- protected data size
- duration
- plugin inventory summary if shown

## Restore Workflow

Required inputs:

- `instanceId`
- `dataSecretKey`

Optional inputs:

- `snapshotId`
- `destPath`

Prefer test restore first with `--dest-path`.

Phase 1: trigger email verification and expect exit code `2`

```bash
clawmover restore --instance-id <instanceId> --data-secret-key <dataSecretKey> --non-interactive --yes --dest-path <destPath>
```

If the command exits with code `2`, tell the user a verification code was sent and ask them to reply with the 6-digit code.

Phase 2: resume restore with the code

```bash
clawmover restore --instance-id <instanceId> --data-secret-key <dataSecretKey> --verification-code <code> --non-interactive --yes --dest-path <destPath>
```

For real restore, omit `--dest-path`:

```bash
clawmover restore --instance-id <instanceId> --data-secret-key <dataSecretKey> --verification-code <code> --non-interactive --yes
```

Important:

- Always include `--yes` for agent-driven restore.
- Prefer `--dest-path` for testing because it also removes restore path confirmation risk.

Return a short result summary:

- success or failure
- restored tags
- snapshot id
- duration
- plugin reinstall summary if shown

## Pending State

When phase 1 exits with code `2`, keep the pending operation context:

- action: `backup` or `restore`
- `instanceId`
- `dataSecretKey`
- `snapshotId` if provided
- `destPath` if provided

When the user later sends a 6-digit code, resume the same pending operation with `--verification-code <code>`.

If there is no pending operation, ask the user to start backup or restore again.

## Restore Safety

- Prefer `--dest-path` for testing.
- If the user asks for a real restore without `--dest-path`, warn that it may modify the real OpenClaw environment.
- In test mode, `clawmover` skips plugin installation and OpenClaw restart.
- In real restore mode, `clawmover` may reinstall reinstallable plugins automatically.

## Sensitive Data Handling

- Do not echo `dataSecretKey` back to the user.
- Do not print the full verification code after it is used.
- Do not include secrets in summaries unless the user explicitly asks.
- If the user seems unsure about `dataSecretKey`, explicitly warn them that losing it makes the backup unrecoverable.

## Error Handling

- If `clawmover` is missing, install it automatically.
- If exit code is `2`, ask for the verification code and wait.
- If the repository password is wrong, tell the user the provided `dataSecretKey` does not match the existing backup repository.
- If restore reports that no backup exists, tell the user no backup was found for that instance.
- If plugin reinstall fails during a real restore, report which plugin failed and include the command error summary.

## Response Style

Keep channel messages short and operational.

Examples:

- `ClawMover CLI is not installed. Installing it now.`
- `You need a paid migration order from https://clawmover.com before this instanceId can be used.`
- `A verification code has been sent to your email. Reply with the 6-digit code to continue.`
- `Backup completed. Snapshot: <id>. Protected data: <size>. Duration: <time>.`
- `Restore completed to test path <destPath>. Reinstallable plugins: 1.`
