# HBM Memory System 🧠

> **Heartbeat-Memories** - Local memory and emotional intelligence system for OpenClaw

[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20|%20Windows%20|%20Linux-lightgrey)]()

## 🎯 What is HBM?

**HBM (Human Brain Model)** is a comprehensive local memory management system for OpenClaw that makes your AI assistant more personal, context-aware, and emotionally intelligent.

Unlike traditional AI assistants that forget everything after each session, HBM remembers your conversations, goals, emotions, and experiences - just like a human friend would.

## ✨ Key Features

### 🧠 Five Memory Banks System
| Memory Bank | What it Stores | Why it Matters |
|-------------|---------------|----------------|
| **Goals** | Your objectives, dreams, and tasks | Keeps you focused and tracks progress |
| **Sessions** | Daily conversation summaries | Maintains context and continuity |
| **Experiences** | Problem-solving knowledge | Learns from past challenges |
| **Emotions** | Your feelings and preferences | Understands your emotional patterns |
| **Version** | System changes and updates | Tracks evolution and improvements |

### ❤️ Heartbeat Recall
- **Proactive engagement**: AI occasionally asks about past memories with keyword hints
- **Natural interaction**: Feels like talking to a friend who remembers your stories
- **Emotional connection**: Builds deeper relationship through shared memories
- **Smart triggers**: Based on conversations, task completion, and special occasions

### 🔍 Semantic Search
- **Natural language queries**: Ask about anything in your memory using everyday language
- **Vector database**: Uses ChromaDB with sentence-transformers for accurate retrieval
- **Fast and local**: No API calls, no token costs, completely private

### 🚀 RAG Optimization
- **Enhanced responses**: AI answers are enriched with relevant memories
- **Token control**: Configurable result limits and deduplication (default: off)
- **Performance cache**: Memory caching for faster responses (default: off)

## 🛠️ Installation

### One-Command Installation (All Platforms)
```bash
# Recommended: Use the main installer script
python3 scripts/install_hbm.py
```

### Platform-Specific Installers
```bash
# macOS / Linux (using shell script)
chmod +x install.sh && ./install.sh

# Windows options:
# 1. Use Python (if installed):
#    python scripts\install_hbm.py
# 2. Use Git Bash or WSL to run the Linux installer
```

Or if downloaded from ClawHub:
```bash
# Navigate to the skill directory and run
cd /path/to/hbm-memory-system
python3 scripts/install_hbm.py
```

### Manual Installation
1. Ensure Python 3.8+ is installed
2. Install dependencies:
   ```bash
   pip install chromadb sentence-transformers pandas numpy requests tqdm
   ```
3. Download the pre-trained model:
   ```bash
   python3 scripts/local_memory_system_v2.py
   ```
4. The script will guide you through the rest

## 📖 Quick Start

### Using with OpenClaw
Once installed, the skill automatically activates when you mention:
- "memory", "recall", "remember"
- "HBM", "memory banks"
- "goals", "emotions", "experiences"
- Or ask about past conversations

### Command Line Interface
```bash
# Start interactive memory management
python3 scripts/local_memory_system_v2.py

# Available commands:
#   add_exp "Problem" "Solution" --highlight
#   add_goal "Goal" "Background" "Reason" "Temp Solution"
#   add_idea "Idea" "Context"
#   search "query"
#   list [memory_type]
```

### Direct File Access
```bash
# View today's conversation summary
cat memory/会话记忆库/$(date +%Y-%m-%d).md

# Check current goals
cat memory/目标记忆库/GOALS.md

# Review technical experiences
cat memory/经验记忆库/TIPS.md

# See emotional patterns
cat memory/情感记忆库/DAILY_EMOTIONS.md
```

## 🏗️ Architecture

```
hbm-memory-system/
├── 📁 memory/                    # Core memory storage
│   ├── 🎯 目标记忆库/           # Goals and objectives
│   ├── 💬 会话记忆库/           # Daily conversations
│   ├── 📚 经验记忆库/           # Technical experiences
│   ├── ❤️ 情感记忆库/           # Emotions and preferences
│   ├── 📦 版本记忆库/           # System version history
│   ├── 💝 心跳回忆/             # Heartbeat recall system
│   ├── 🔍 语义搜索_db/          # ChromaDB vector database
│   └── 🚀 RAG/                  # Retrieval Augmented Generation
├── 📁 scripts/                  # Management scripts
│   ├── install_hbm.py           # Cross-platform installer
│   └── local_memory_system_v2.py # Memory system CLI
├── 📁 references/               # Documentation
│   ├── MEMORY.md               # System navigation
│   ├── HEARTBEAT.md            # Periodic tasks
│   └── 心跳回忆机制.md         # Heartbeat recall details
├── 📄 SKILL.md                  # OpenClaw skill definition
├── 📄 README.md                 # This file
├── 📄 requirements.txt          # Python dependencies

```

## 🔧 Configuration

### Heartbeat Recall Settings
The system automatically configures heartbeat recall with sensible defaults:
- **Daily limit**: 3 proactive recalls per day
- **Minimum interval**: 60 minutes between recalls
- **Holiday mode**: Special occasions don't count toward daily limits
- **User control**: Unlimited when user initiates recall

### RAG Optimization Switches
All optimization features are optional and default to off:
- Token limit and deduplication: `OFF` by default
- Memory caching: `OFF` by default
- Log compression: `ON` (monthly automatic compression)

## 🌟 Real-World Examples

### Example 1: Goal Tracking
```
You: "I want to learn Python for data analysis"
AI: ❤️ "Hey, remember last week you mentioned wanting to learn Python? 
     How's that going? Found any good resources yet?"
```

### Example 2: Problem Solving
```
You: "My code has a bug with database connections"
AI: "Let me check our experience memory... 
     Found a similar issue from March. The solution was to check connection timeouts."
```

### Example 3: Emotional Support
```
AI: ❤️ "Noticed you seemed stressed about the project deadline yesterday. 
     Feeling any better today? Need help breaking it down?"
```

## 📊 System Requirements

- **Python**: 3.8 or higher
- **Memory**: 300MB RAM minimum (for ChromaDB)
- **Storage**: 500MB free space (for models and memory)
- **Platform**: macOS 10.15+, Windows 10+, Linux (Ubuntu 18.04+)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report bugs**: Open an issue with detailed description
2. **Suggest features**: Share your ideas for improvement
3. **Improve documentation**: Fix typos or add examples
4. **Share your experience**: Tell us how you're using HBM

### Development Setup
```bash
# Clone the repository
git clone [repository-url]

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python3 -m pytest tests/
```

## 📄 License

This skill is distributed through ClawHub and follows the platform's licensing policy.

## 🙏 Acknowledgments

- **OpenClaw Community** for the amazing AI assistant platform
- **ChromaDB** for the excellent vector database
- **Sentence-Transformers** for high-quality embedding models
- **All Contributors** who help make this project better

## 📞 Support

- **Documentation**: Check the `references/` directory
- **Issues**: Open a GitHub issue
- **Community**: Join the OpenClaw Discord server
- **Email**: [Your contact email]

---

**Made with ❤️ for the OpenClaw community**

*Last updated: April 15, 2026*