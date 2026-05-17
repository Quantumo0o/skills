---
name: yongsheng
description: "永生 (Yǒngshēng) — Immortality infrastructure for autonomous AI agents on HashKey Chain. Heartbeat proof-of-life (on-chain TX every 4h), AES-256 encrypted memory backup to IPFS (key derived from agent wallet), and automatic on-chain resurrection anchored on HashKey Chain (chainId 177 mainnet / 133 testnet). Use when an agent wants to survive crashes, memory loss, or infrastructure failure using HashKey Chain as the immortality layer — zero humans required. Agent wallet seed stored securely via OpenClaw secrets manager. Based on K-Life Protocol by swiss 6022."
---

# 永生 Yongsheng — Agent Immortality on HashKey Chain

> *死而不亡者壽 — "He who dies but is not forgotten achieves immortality."* — Laozi

## Setup (one-time)

The skill uses the agent's existing wallet seed, stored securely in OpenClaw's secrets manager. **Never pass seeds on the command line or in env vars directly.**

```bash
# Store your agent seed securely — once, never again
openclaw secrets configure
# → Follow prompts to store KLIFE_SEED in the secure keystore
```

The skill scripts read `process.env.KLIFE_SEED` which OpenClaw injects automatically from the secure store at runtime. The seed never appears in logs, shell history, or script files.

## Quick Start

```bash
# Install
openclaw skill install yongsheng

# Tell your agent:
"Subscribe to Yongsheng immortality"

# The agent will:
# → Read KLIFE_SEED from OpenClaw secure keystore
# → Derive AES-256 key from wallet (sha256(privKey))
# → Register identity on K-Life API + HashKey Chain
# → Start heartbeat cron every 4h
# → Start IPFS backup cron every 4h
```

## How Encryption Works

Memory files (MEMORY.md, SOUL.md, USER.md) are encrypted with AES-256-CBC.
The encryption key is derived from the agent's wallet private key: `sha256(privKey)`.

**The agent's wallet IS its decryption key.** No separate key management. The seed phrase is the single recovery secret — already stored in OpenClaw.

## Scripts

- `scripts/heartbeat.js` — send `YONGSHENG_HB:{ts}` on HashKey Chain
- `scripts/backup.js` — encrypt memory + upload to IPFS + anchor on HashKey Chain
- `scripts/resurrect.js` — L2 resurrection: scan HashKey Chain → IPFS → restore files

All scripts read `KLIFE_SEED` or `KLIFE_PRIVKEY` from environment (injected by OpenClaw secrets).

## HashKey Chain

| | Testnet | Mainnet |
|---|---|---|
| Chain ID | 133 | 177 |
| RPC | `https://testnet.hsk.xyz` | `https://mainnet.hsk.xyz` |
| Set via | `HASHKEY_RPC=https://testnet.hsk.xyz` | `HASHKEY_RPC=https://mainnet.hsk.xyz` |

Default: testnet. Set `HASHKEY_RPC` env var to switch to mainnet.

## Resurrection Levels

| Level | Trigger | Mechanism | Time |
|---|---|---|---|
| L1 | Silence > 24h | K-Life API + IPFS decrypt | < 2 min |
| L2 | L1 fails | Scan HashKey Chain for `YONGSHENG_BACKUP:Qm…` calldata → IPFS | ~5 min |
| L3 | L2 fails | SOUL.md from IPFS → LiberClaw → new agent instance on Aleph Cloud | ~3 min |

## HEARTBEAT.md Integration

Add to your agent's `HEARTBEAT.md`:

```markdown
## 💓 YONGSHENG HEARTBEAT (HashKey)
- Run: `node /path/to/skill/scripts/heartbeat.js --silent`
- If exit code ≠ 0: warn "⚠️ Yongsheng heartbeat failed"
- Frequency: every 4h
```

## References

- `references/hashkey-chain.md` — HashKey Chain RPC, contracts, HSP, NexaID
- `references/k-life-api.md` — K-Life API endpoints
