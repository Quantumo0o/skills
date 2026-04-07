# CommunityOS Telegram Bot Skill

Simple Telegram Bot management without group configuration.

## Features

- 🤖 **Bot Management** - Create, edit, delete Telegram bots
- 🔑 **Global LLM Config** - Unified LLM settings for all bots (MiniMax, OpenAI, Anthropic, DeepSeek)
- 📚 **Text Knowledge Base** - Paste text directly, bot answers within knowledge scope
- 💬 **Auto Reply** - Bot auto-replies in groups without group config
- 🔒 **DM Control** - Toggle Allow DM to control private chat

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/community-os
source venv/bin/activate
python admin/app.py
```

Then visit: http://localhost:8878/lite

## Usage Flow

1. Go to @BotFather → Create bot → Copy token
2. Paste token in Lite → Save
3. (Optional) Paste knowledge text
4. Invite bot to Telegram group → Done!

## Configuration

Edit `.env` file:
```
TELEGRAM_BOT_TOKEN_PANDA=your_token_here
MINIMAX_API_KEY=your_key_here
```

## LLM Providers

| Provider | Default Model | Notes |
|----------|---------------|-------|
| MiniMax | MiniMax-2.7 | Free tier |
| OpenAI | GPT-4o | Paid |
| Anthropic | Claude 3.5 Sonnet | Paid |
| DeepSeek | DeepSeek Chat | Cheap |

## Files

- `admin/app.py` - FastAPI backend
- `admin/lite.html` - Simple UI
- `bot_engine/` - Bot runtime engine
- `config/` - Configuration files
