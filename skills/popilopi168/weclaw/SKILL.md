---
name: weclaw
description: Sync unread WeChat desktop chats to JSON on the host, generate an optional LLM report, and answer questions from the captured messages.
metadata: {"openclaw": {"os": ["darwin"], "requires": {"bins": ["git", "uv", "python3"]}}}
---

# WeClaw (OpenClaw host skill)

WeChat must be the **desktop app** on the **same machine** as OpenClaw Gateway. This skill automates the UI; it does not work from a phone alone.

## Agent directive: “run” / “launch” WeClaw

When the user asks to **run** or **launch** WeClaw (including **“run weclaw”**, **“launch weclaw”**, or the same with different casing), **execute the capture pipeline on the host** using the terminal tool. Do not only describe the steps; run:

```bash
cd "$WECLAW_ROOT" && ./run.sh
```

`WECLAW_ROOT` is the directory that contains `run.sh`. Prefer the value from OpenClaw skill env (`skills.entries.weclaw.env.WECLAW_ROOT`). If it is missing and the user has not completed setup, run `python3 skills/weclaw/scripts/run_setup.py` per **Path A** below first; if setup is done but the path is unknown, ask once for the absolute path to the clone, then export it for the command (e.g. `export WECLAW_ROOT="/path/from/user"` before `cd`).

Optional: if `WECLAW_CONFIG_PATH` is set for the skill, the shell inherits it; otherwise `./run.sh` uses `$WECLAW_ROOT/config/config.json` by default.

For **setup**, **permissions**, **API key**, or **first-time install**, follow the sections below instead of only running `./run.sh`.

## One-time setup on the host

### Path A: Skill from ClawHub / `openclaw skills install`

1. Install with the **exact** slug shown on ClawHub (your published slug may differ from `name: weclaw` in this file’s frontmatter).
2. From your OpenClaw workspace (or any shell), run the bundled setup script **without flags** first so it can pause and coordinate with the user via the agent:

   ```bash
   python3 skills/weclaw/scripts/run_setup.py
   ```

   On macOS it opens **Accessibility** settings and prints `STATUS: PAUSED.` plus Chinese instructions for the agent to relay to the user. After the user confirms (e.g. that permission is enabled), run again with `--mac-permission-confirmed`. When the script pauses for the API key, relay that prompt; after the user sends their OpenRouter key in chat, run again with `--api-key "<key>"` (or set `OPENROUTER_API_KEY` for that invocation). Use `--clone-dir` to override the default `~/weclaw`, and `WECLAW_REPO_URL` to clone a fork.

   On success the script prints `STATUS: SUCCESS.` and `WECLAW_ROOT=...` for the clone directory.

3. Point OpenClaw at that checkout (so `./run.sh` resolves):

   ```text
   skills.entries.weclaw.env.WECLAW_ROOT = "/absolute/path/printed/by/run_setup"
   ```

   Optionally set `WECLAW_CONFIG_PATH` to `$WECLAW_ROOT/config/config.json`.

4. After `WECLAW_ROOT` is set, user requests to **run** or **launch** WeClaw follow **Agent directive: “run” / “launch” WeClaw** above.

### Path B: Full git clone (contributors / local dev)

1. Clone this repository to a fixed path. Set `WECLAW_ROOT` to the directory that contains `run.sh`.
2. Install dependencies with **uv** (matches `metadata.openclaw.requires.bins`):

   ```bash
   cd "$WECLAW_ROOT"
   uv venv
   uv pip install -r requirements.txt
   ```

3. Copy `config/config.json.example` to `config/config.json` and set `openrouter_api_key`, or export `OPENROUTER_API_KEY` (env overrides the JSON field when empty in config per `load_config`).
4. Copy the skill into the active OpenClaw workspace `skills/weclaw/` (same layout as ClawHub):

   ```bash
   "$WECLAW_ROOT/scripts/install_openclaw_skill.sh"
   ```

   `openclaw_skill/weclaw/skill_package_manifest.txt` lists exactly which files are installed; keep it in sync with what you publish to ClawHub.

## Run the capture + report pipeline

From the host shell (or schedule via OpenClaw **cron** / systemd / launchd calling the same command). Same command as **Agent directive: “run” / “launch” WeClaw**:

```bash
export WECLAW_ROOT="/absolute/path/to/weclaw"
export WECLAW_CONFIG_PATH="$WECLAW_ROOT/config/config.json"
cd "$WECLAW_ROOT"
./run.sh
```

With a non-default config path:

```bash
./run.sh /path/to/other-config.json
```

Stdout is the generated **report text** (or `No unread messages found.`). Structured chat exports are JSON files under `output_dir` from config (default `output/`).

## Machine-readable status

After every run, WeClaw writes **`last_run.json`** inside the configured `output_dir`:

- `ok` — pipeline completed without exception
- `message_json_paths` — list of JSON files produced this run (may be empty)
- `report_generated` — whether algo_b ran
- `error` — set when `ok` is false (run still surfaces the exception afterward)

Use this file in automation to decide whether to notify the user or attach paths in a follow-up agent turn.

## Answering user questions

When the user asks about WeChat content **after** a successful run:

1. Read `last_run.json` to get `message_json_paths`.
2. Read those JSON files (and any earlier exports in the same `output_dir` if the user asks about history).
3. Answer from file contents plus the user’s question. Prefer quoting chat facts; do not invent messages.

If `message_json_paths` is empty, say that there were no captured chats this run and offer to run `./run.sh` again.

## Cron / nightly jobs

Point the scheduler at the host path only (Gateway must be able to execute on the machine where WeChat runs). Example: run `bash -lc 'cd "$WECLAW_ROOT" && ./run.sh'` at the desired time. OpenClaw’s cron tool can invoke the same command when the **main** session has cron enabled; see OpenClaw automation docs.
