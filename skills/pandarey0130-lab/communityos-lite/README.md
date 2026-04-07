# CommunityOS Telegram Bot

Simple Telegram Bot management with LLM and knowledge base.

## Features

- 🤖 **Bot Management** - Create, edit, delete Telegram bots
- 🔑 **Global LLM Config** - Unified LLM settings for all bots
- 📚 **Text Knowledge Base** - Paste text directly, bot answers within scope
- 💬 **Auto Reply** - Bot auto-replies in groups without group config
- 🔒 **DM Control** - Toggle Allow DM to control private chat

## Quick Start

```bash
# Clone
git clone https://github.com/pandarey0130-lab/communityOS-Lite.git
cd communityOS-Lite

# Install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your tokens (optional if you set keys in Lite UI)
# LLM key for Lite UI is stored in admin/data/llm_config.json (gitignored).
# First run: copy admin/data/llm_config.example.json to admin/data/llm_config.json, then set api_key in the UI or file — never commit real keys.

# Run（无需设置 PYTHONPATH，在仓库根目录执行即可）
python admin/app.py
```

Visit: http://127.0.0.1:8877/lite

Optional smoke test (no server on port needed):

```bash
python scripts/smoke_lite.py
```

（`smoke_lite.py` 只校验本机 FastAPI 路由与 `/lite` 页面，**不会**请求 Telegram 或 LLM 外网。）

## How to Use

1. Go to **@BotFather** in Telegram → Create new bot → Copy token
2. Paste token in Lite UI → Click Save
3. Configure **LLM** in Lite (API key + provider) → Save
4. (Optional) Paste knowledge text → Bot answers only within this scope
5. Invite bot to Telegram group → **Done!**
6. Chat in group (or DM) → Bot replies when it receives your text  
   **Groups:** If the bot never sees ordinary group messages, read **Telegram group privacy** below.

## Telegram group privacy (Group Privacy)

Telegram controls **which group messages** your bot receives. This is **not** a CommunityOS Lite bug. **New bots default to privacy ON.**

| Setting | What the bot usually receives in groups |
|--------|----------------------------------------|
| **Privacy ON** (default) | Typically only: **`/` commands**, messages that are a **reply to the bot**, or messages that **@mention the bot’s username** |
| **Privacy OFF** | **Normal group text** is delivered too — needed for Lite’s **auto-reply on plain chat** (`passive_qa`) |

**Private chats** are unaffected: DMs still reach the bot when **Allow DM** is on.

### Turn off group privacy (when you want auto-reply to normal group messages)

1. Open Telegram and go to **`@BotFather`**
2. Send **`/mybots`**
3. Tap **your bot** (the one you created in BotFather)
4. **Bot Settings** → **Group Privacy**
5. Choose **Turn off** / **Disable** (i.e. disable privacy so the bot can read ordinary group messages)

You do **not** need to change the token in Lite. If nothing changes immediately, send a **new** message in the group and confirm the bot is still a member and not restricted.

### Common pitfalls

- **`passive_qa` is on but the bot stays silent in groups** — With privacy **ON**, Telegram may never send plain group messages to your server, so Lite never sees them.
- **You only want replies when @mentioned** — Leave privacy **ON**; @mentions and commands still generate updates.

### Security note

With privacy **OFF**, the bot receives **many** group messages. Protect your **token** and run the Lite admin UI **locally** only (see project docs).

## LLM Providers

| Provider | Default Model | Notes |
|----------|---------------|-------|
| MiniMax | MiniMax-2.7 | Free tier available |
| OpenAI | GPT-4o | Paid |
| Anthropic | Claude 3.5 Sonnet | Paid |
| DeepSeek | DeepSeek Chat | Cheap |

## Architecture

```
admin/
  app.py      - FastAPI backend
  lite.html   - Simple UI
bot_engine/
  manager.py  - Bot instance manager
  bot_instance.py - Individual bot logic
  llm/        - LLM provider implementations
admin/data/
  bots.json, llm_config.json - Runtime config (fill via Lite UI; not committed with secrets)
```

## License

MIT
