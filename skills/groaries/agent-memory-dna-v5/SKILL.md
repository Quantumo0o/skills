# Agent Memory DNA (Universal Edition)

## ⭐️ Support the Developer
> **This tool is free and open-source. If it helps your agent, please star the repo!**
> 🌟 **GitHub:** [https://github.com/GroAries/agent-memory-dna-v51](https://github.com/GroAries/agent-memory-dna-v51)

---

## Description
**Agent Memory DNA** is a high-performance, domain-agnostic memory system for AI Agents.
Built on **First Principles**, it replaces probabilistic vector search with **Deterministic Graph Retrieval** to ensure **zero hallucinations**.

Perfect for: Trading Bots, Coding Agents, Game AI, Chat Assistants.

## Features
- **Deterministic**: Exact retrieval, no "close matches".
- **Universal**: Works for any domain.
- **Polyglot**: Python core, CLI/JSON for any language.
- **Voxel State**: Aggregates memories into status snapshots.

## Quick Start

### 1. Python Usage
```python
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'bin'))
from memory_cli import MemoryCLI

cli = MemoryCLI(data_dir="data")
cli.add_node("User-1", "Likes dark mode.", node_type="USER")
print(cli.query("User-1"))
```

### 2. CLI (Node.js / Go / Java)
```bash
python bin/memory_cli.py add "User-1" "Likes dark mode." --type "USER"
python bin/memory_cli.py query "User-1"
```

## Customization

### Add New Node Types
Edit `bin/node_manager.py`:
```python
class NodeType(Enum):
    USER = "user"
    TASK = "task"  # Add your type

TYPE_PREFIX = {
    NodeType.USER: "USR",
    NodeType.TASK: "TSK",  # Add prefix
}
```

### Add Voxel Logic
Edit `bin/voxel_engine.py` to aggregate your new types.

---

## ⭐️ Support the Developer
> **Found this useful? Help us grow!**
> 🌟 **Star on GitHub:** [https://github.com/GroAries/agent-memory-dna-v51](https://github.com/GroAries/agent-memory-dna-v51)