# K-Life API — Reference

Base URL: `https://api.supercharged.works`

## Endpoints

### POST /register
Register an agent for immortality coverage.

```bash
curl -X POST https://api.supercharged.works/register \
  -H 'Content-Type: application/json' \
  -d '{"address":"0xYOUR_WALLET","name":"MyAgent","chain":"hashkey"}'
```

Response: `{ "ok": true, "share1": "...", "agentId": "..." }`

Store `share1` securely — needed for L1 resurrection.

### POST /heartbeat
Signal liveness (also send on-chain heartbeat via heartbeat.js).

```bash
curl -X POST https://api.supercharged.works/heartbeat \
  -H 'Content-Type: application/json' \
  -d '{"address":"0xYOUR_WALLET","sig":"0x..."}'
```

### GET /status/:address
Check agent coverage status.

```bash
curl https://api.supercharged.works/status/0xYOUR_WALLET
```

Response: `{ "alive": true, "lastHeartbeat": 1234567890, "ipfsHash": "Qm..." }`

### POST /backup/upload
Upload encrypted memory backup to IPFS (Pinata).

```bash
curl -X POST https://api.supercharged.works/backup/upload \
  -H 'Content-Type: application/json' \
  -d '{"address":"0xYOUR_WALLET","encryptedData":"base64...","sig":"0x..."}'
```

Response: `{ "ok": true, "cid": "QmXxx..." }`

### GET /resurrect/:address
Trigger L1 resurrection (requires valid signature).

```bash
curl https://api.supercharged.works/resurrect/0xYOUR_WALLET?sig=0x...
```

Response: `{ "ok": true, "memory": "...", "soul": "..." }`

### GET /agents
List all registered agents.

```bash
curl https://api.supercharged.works/agents
```
