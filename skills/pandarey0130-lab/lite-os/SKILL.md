# CommunityOS Telegram Bot Skill

Simple Telegram Bot management with LLM and knowledge base.

## ⚠️ Security Notes

- **Local Only** - Runs on localhost (127.0.0.1), not exposed to internet
- **No Built-in Auth** - Admin UI has no authentication, only use locally
- **Credentials Required** - Needs Telegram bot tokens and LLM API keys (see below)

## Required Environment Variables

```bash
# Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN_XXX=your_bot_token

# LLM API Keys (at least one required)
MINIMAX_API_KEY=your_minimax_key     # Recommended - has free tier
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
DEEPSEEK_API_KEY=your_deepseek_key
```

## Features

- 🤖 **Bot Management** - Create, edit, delete Telegram bots
- 🔑 **Global LLM Config** - Unified LLM settings (MiniMax, OpenAI, Anthropic, DeepSeek)
- 📚 **Text Knowledge Base** - Paste text directly, bot answers within knowledge scope
- 💬 **Auto Reply** - Bot auto-replies in groups without group config
- 🔒 **DM Control** - Toggle Allow DM to control private chat

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/community-os

# Create venv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run
python admin/app.py
```

Then visit: http://localhost:8878/lite

## Architecture

- `admin/app.py` - FastAPI backend (no external dependencies)
- `admin/lite.html` - Simple UI
- `bot_engine/` - Bot runtime (self-contained, no harness dependency)
- `config/` - Configuration files

**Note:** This skill is self-contained. The `harness` referenced in some code is not required for the Lite version to work.
