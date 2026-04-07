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
git clone https://github.com/panda-community/community-os-skill.git
cd community-os-skill

# Install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your tokens

# Run
python admin/app.py
```

Visit: http://localhost:8878/lite

## How to Use

1. Go to **@BotFather** in Telegram → Create new bot → Copy token
2. Paste token in Lite UI → Click Save
3. (Optional) Paste knowledge text → Bot answers only within this scope
4. Invite bot to Telegram group → **Done!**
5. Chat in group → Bot auto-replies

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
config/
  bots.json   - Bot configurations
  llm_config.json - Global LLM settings
```

## License

MIT
