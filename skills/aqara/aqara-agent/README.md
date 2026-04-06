# Aqara Agent

Aqara Home **AI Agent skill**: homes, rooms, devices, scenes, automations, and energy statistics through the **Aqara Open API**, with natural language on the agent side and **`scripts/aqara_open_api.py`** on the wire.

**Canonical spec:** [`SKILL.md`](SKILL.md) (workflow, **Must** / **Forbidden**, routing, errors, **Out of Scope**). This file is an index only and does not override it.

## What It Covers

- **Space:** homes, rooms, `home_id` selection  
- **Devices:** query, status, logs, base info; control via `post_device_control`  
- **Scenes:** list, run, detail, execution logs  
- **Automations:** list, detail, toggle, execution logs  
- **Energy:** consumption / cost–style statistics (device, room, or home)

Example intents: *“How many lights are at home?”*, *“Turn off the living room AC.”*, *“Run the Movie scene.”*, *“What automations do I have?”*, *“Check automation execution in the bedroom for the last three days.”*

## Repository Layout

| Path | Role |
|------|------|
| [`SKILL.md`](SKILL.md) | Normative instructions for hosts and models |
| [`README.md`](README.md) | This file |
| [`assets/login_reply_prompt.json`](assets/login_reply_prompt.json) | Locales, **`official_open_login_url`**, **`login_url_policy`** |
| [`assets/user_account.example.json`](assets/user_account.example.json) | Template for session JSON |
| [`assets/user_account.json`](assets/user_account.json) | Live credentials + `home_id` / `home_name` (**sensitive**) |
| [`scripts/aqara_open_api.py`](scripts/aqara_open_api.py) | CLI + `AqaraOpenAPI` client |
| [`scripts/save_user_account.py`](scripts/save_user_account.py) | Persist `aqara_api_key` / home selection |
| [`scripts/runtime_utils.py`](scripts/runtime_utils.py) | Shared helpers |
| [`scripts/requirements.txt`](scripts/requirements.txt) | Python dependencies |

### `references/` (procedures + bash examples)

| Doc | Topic |
|-----|--------|
| [`aqara-account-manage.md`](references/aqara-account-manage.md) | Login, token save, re-auth, logout |
| [`home-space-manage.md`](references/home-space-manage.md) | Homes, rooms, selecting a home |
| [`devices-inquiry.md`](references/devices-inquiry.md) | Lists, status, logs |
| [`devices-control.md`](references/devices-control.md) | Control commands and bounds |
| [`scene-manage.md`](references/scene-manage.md) | Scenes |
| [`automation-manage.md`](references/automation-manage.md) | Automations |
| [`energy-statistic.md`](references/energy-statistic.md) | Energy / cost stats |

## Setup

1. **Python** 3 with `pip`.

2. **Install deps** (run from **this** directory — the folder that contains `scripts/`):

   ```bash
   pip install -r scripts/requirements.txt
   ```

3. **API host** (optional): default is production (`agent.aqara.com`); for test, e.g.:

   ```bash
   export AQARA_OPEN_HOST=agent-test.aqara.cn
   ```

4. **Session file:** start from [`assets/user_account.example.json`](assets/user_account.example.json) → `assets/user_account.json`, then follow [`references/aqara-account-manage.md`](references/aqara-account-manage.md) for login and [`references/home-space-manage.md`](references/home-space-manage.md) for home selection.

5. **Login URL:** agents **must** show users **exactly** the string in `login_reply_prompt.json` → **`official_open_login_url`** (read **`login_url_policy`**). **Forbidden** invent Open Platform / `sns-auth` / OAuth-style URLs.

6. **After pasting `aqara_api_key`:** run `save_user_account.py` and **`get_homes`** as **two separate** shell runs (no `&&` chain); see account + home-space references.

## CLI

```bash
python3 scripts/aqara_open_api.py <method_name> [json_body]
```

Use **only** method names that appear on `AqaraOpenAPI` and in the bash examples inside `references/*.md`. `get_*` → no JSON body; `post_*` → optional JSON object.

Optional env: `AQARA_OPEN_HTTP_TIMEOUT`, `AQARA_OPEN_API_URL` (see [`SKILL.md`](SKILL.md)).

## Security and Sharing

- Treat **`assets/user_account.json`** as secret; do not commit or ship it in public bundles.  
- Distribute **`user_account.example.json`** plus docs; recipients create their own `user_account.json` after login.

## Limitations

Cameras, door-unlock flows, authoring new scenes/automations from scratch, shortcuts, weather, and entertainment are out of scope for this wrapper. Full list: [`SKILL.md`](SKILL.md) → **Out of Scope**.
