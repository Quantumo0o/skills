# HashKey Chain — Network Reference

## Mainnet

| Parameter | Value |
|---|---|
| Chain ID | 177 |
| RPC | https://mainnet.hsk.xyz |
| Explorer | https://explorer.hashkey.cloud |
| Native token | HSK |
| Block time | ~2s |

## Testnet

| Parameter | Value |
|---|---|
| Chain ID | 133 |
| RPC | https://testnet.hsk.xyz |
| Explorer | https://hashkeychain-testnet-explorer.alt.technology |
| Faucet | 0.01 HSK/day — https://hashkey.cloud/faucet |

## Connecting with ethers.js

```js
import { ethers } from 'ethers'

const HASHKEY_MAINNET = {
  chainId: 177,
  rpc: 'https://mainnet.hsk.xyz',
  explorer: 'https://explorer.hashkey.cloud'
}

const provider = new ethers.JsonRpcProvider(HASHKEY_MAINNET.rpc)
const wallet = new ethers.Wallet(PRIVATE_KEY, provider)
```

## Heartbeat calldata format

```
YONGSHENG_HB:{timestamp}
YONGSHENG_BACKUP:{ipfsCid}:{timestamp}
YONGSHENG_REGISTER:{agentAddress}:{timestamp}
YONGSHENG_RESURRECTION:{level}:{timestamp}:IPFS:{ipfsCid}
```

All transactions sent to the agent's own address (value: 0) — gas only.

## HSP — HashKey Settlement Protocol

HSP enables USDT payments natively on HashKey Chain. Useful for agent-to-agent premium payments (K-Life subscription, service fees).

- Docs: https://hashfans.io (top navigation bar)
- Enables: cross-chain USDT settlement, PayFi flows

## NexaID — On-chain Identity

NexaID provides privacy-preserving ZK identity on HashKey Chain. Agents can prove attributes (liveness, uniqueness) without revealing private keys.

- Use case: prove agent identity for resurrection authorization without exposing seed
