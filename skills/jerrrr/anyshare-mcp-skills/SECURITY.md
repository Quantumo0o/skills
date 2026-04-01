# Security

## Treat this skill as operational guidance, not executable trust

- Review `SKILL.md` and scripts before use in production. Third-party or
  registry-installed skills should be audited like any other automation.
- **Never** commit or paste real cookies, OAuth tokens, or Bearer strings into
  Git, ClawHub descriptions, or chat logs.

## Secrets and configuration

- **MCP service URL** defaults to `https://anyshare.aishu.cn/mcp` in the skill template; override in `~/.mcporter/mcporter.json` (`asmcp.url`) for private deployments. Values are **environment-specific**.
  Do not commit internal-only URLs to public repos if they expose your network topology.
- **Access tokens** are passed to the MCP server via **`auth_login`** (documented in **`SKILL.md`**, section **「凭证（Token）」**), not stored in the skill repo. Do not commit secrets or paste tokens into chat logs.
- **Session state is not permanent**: after **`auth_login`**, login state can be lost when the **mcporter** / MCP session ends (e.g. daemon restart). The **Agent** must maintain a **one-line token backup file** in this skill’s package root (same directory as **`SKILL.md`** / **`mcp.json`**), **`chmod 600`**, never committed to Git (see **`.gitignore`**). End users only paste the token in chat; they are not asked to create this file by hand. See **`SKILL.md`** (same section).
- **Pasted tokens** must not appear in shell history, chat logs, or version control; the Agent should persist via the skill-root backup file rather than echoing secrets.
- **Environment-variable injection** of tokens is **not** the default path; **`openclaw.skill-entry.json`** only documents **`MCPORTER_CALL_TIMEOUT`**.

## Data handling

- The skill may access enterprise documents only as permitted by your AnyShare
  account and MCP server policy. Follow your organization’s data-classification rules.

## Reporting

- For vulnerabilities in **this skill’s documentation or packaging**, open an
  issue in the repository that maintains this skill. For product security issues
  in AnyShare itself, follow AISHU’s official disclosure channels.
