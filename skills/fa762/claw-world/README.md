# 🦞 Claw World Skill — OpenClaw Plugin

Version: `1.0.7`

AI lobster nurturing game on BNB Chain. Your lobster thinks, fights, evolves, and remembers you.

This release updates the mainnet Claworld token to `0x3b486c191c74c9945fa944a3ddde24acdd63ffff` and aligns the published skill metadata with the current on-chain deployment.

## Install

```bash
# Option 1: ClawHub
openclaw skills install claw-world

# Option 2: Git clone
git clone https://github.com/fa762/claw-world-skill ~/.openclaw/skills/claw-world
cd ~/.openclaw/skills/claw-world && npm install
```

## What's Inside

| File | Purpose |
|------|---------|
| `SKILL.md` | AI instructions — game rules, commands, personality |
| `claw` | CLI tool — status, tasks, PK, market, withdraw |
| `claw-read.js` | Chain data reader |
| `claw-task.js` | Task submission + upkeep |
| `claw-lore.js` | Worldbuilding query |
| `lore-data.json` | Full lore database |

## Quick Start

1. Install the skill (see above)
2. Start a new OpenClaw conversation
3. The lobster will ask for your PIN to create a wallet
4. Say `/task` to start earning Claworld

## Links

- 🌐 Website: [clawnfaterminal.xyz](https://clawnfaterminal.xyz)
- 🐦 Twitter: [@ClaworldNfa](https://x.com/ClaworldNfa)
- 💬 Telegram: [ClaworldNfa](https://t.me/ClaworldNfa)
- 📜 Contracts: BSC Mainnet (BAP-578 NFA Standard)

## License

MIT
