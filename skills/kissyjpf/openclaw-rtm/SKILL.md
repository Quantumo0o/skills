---
name: rtm-skill
description: Remember The Milk skill for OpenClaw
---

# Remember The Milk (RTM) Skill for OpenClaw

This skill integrates [Remember The Milk](https://www.rememberthemilk.com/) with OpenClaw, allowing you to manage your daily tasks directly from the command line.

## Obtaining API Credentials

Before using this skill, you need to obtain an API Key and a Shared Secret from Remember The Milk:

1. Go to the [Remember The Milk API Keys](https://www.rememberthemilk.com/services/api/keys.rtm) page.
2. Log in with your Remember The Milk account if prompted.
3. Apply for a new API Key by registering your application.
4. Once created, you will receive an **API Key** and a **Shared Secret**.
5. Set these values as environment variables before starting OpenClaw:

   ```bash
   export RTM_API_KEY="your-api-key-here"
   export RTM_SHARED_SECRET="your-shared-secret-here"
   ```

> [!IMPORTANT]
> Do NOT edit `index.js` to embed your API key/secret directly into the source files. Using environment variables ensures your credentials remain secure.

## Setup and Authorization

Before you can use the commands to manage your tasks, you need to authorize the skill with your Remember The Milk account.

> [!NOTE]
> When you authorize this application, an authentication token will be saved locally to `~/.rtm-token.json` in plaintext. Keep this file secure on trusted devices, and delete it if you uninstall the skill.

1.  **Start Authorization:**
    ```bash
    rtm auth
    ```
    This command will provide you with an authorization URL. Open this URL in your web browser and authorize the application.

2.  **Save Token:**
    After authorizing in the browser, run the following command with the `frob` provided.
    ```bash
    rtm token <frob>
    ```
    This will save your authentication token locally (`~/.rtm-token.json`) so you only need to do this once.

## Available Commands

Once authorized, you can use the following commands to interact with your tasks.

### List Tasks

List all your tasks (both incomplete and completed):

```bash
rtm list
```

This will fetch and display all your tasks along with their completion status (✅ or ⬜️), short IDs, lists (categories), priorities, due dates, tags, and notes. The short ID corresponds to the task's index in the list, which is used for completing or deleting tasks.

### Add a Task

Create a new task:

```bash
rtm add <task name>
```

Example: `rtm add Buy groceries`

### Add a Note

Add a note to an existing task using its short ID:

```bash
rtm note <id> <note text>
```

Example: `rtm note 1 Make sure to check the expiry dates`

*(Note: You must run `rtm list` before running this command so the short IDs are cached.)*

### Complete a Task

Mark a specific task as completed using its short ID (obtainable via `rtm list`):

```bash
rtm complete <id>
```

Example: `rtm complete 1`

*(Note: You must run `rtm list` before running this command so the short IDs are cached.)*

### Modify Task Properties

You can modify task properties using the following commands (all require the task ID from `rtm list`):

- **Due Date:** `rtm due <id> <date string>` (Leave date empty to delete the due date)
  - Example: `rtm due 1 tomorrow`
  - Delete due: `rtm due 1`
- **Start Date:** `rtm start <id> <date string>`
  - Example: `rtm start 1 next week`
- **Priority:** `rtm priority <id> <1|2|3|N>` (N is for none)
  - Example: `rtm priority 1 2`
- **Postpone:** `rtm postpone <id>` (Postpones the task's due date by 1 day)
  - Example: `rtm postpone 1`

### Delete a Task

Delete a specific task using its short ID:

```bash
rtm delete <id>
```

Example: `rtm delete 2`

*(Note: You must run `rtm list` before running this command so the short IDs are cached.)*
