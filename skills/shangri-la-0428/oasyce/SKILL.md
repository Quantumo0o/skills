---
name: oasyce
version: 3.1.0
description: >
  Oasyce Protocol — register data assets, invoke AI capabilities, query oracle feeds,
  manage agent identities, trade shares, and run your node on the decentralized data
  rights clearing network. Also supports local data inventory via DataVault (optional).
  Use when user mentions Oasyce, data rights, data registration, bonding curve,
  capabilities, agent services, oracle feeds, agent identity, OAS tokens, staking,
  data scanning, or wants to monetize/protect their data.
read_when:
  - User mentions Oasyce, OAS, data rights, or data registration
  - User wants to register, protect, or monetize data
  - User asks about bonding curves, shares, or staking
  - User wants to invoke or register AI capabilities/services
  - User asks about oracle feeds, real-time data, or price feeds
  - User asks about agent identity, trust tiers, or reputation
  - User mentions "确权", "上链", "数据资产", or agent services
  - User wants to run a protocol demo or start a node
  - User wants to scan, inventory, or classify local data assets
metadata: {"emoji":"⚡","requires":{"bins":["python3","oasyce"]}}
---

# Oasyce Protocol Skill

One skill for the entire Oasyce ecosystem — data rights + AI capabilities + oracle feeds + agent identity + P2P node + local data inventory.

## Prerequisites

```bash
pip install oasyce              # core protocol (required)
pip install datavault           # local data scanner (optional)
oasyce doctor                   # verify everything is ready
```

---

## Local Data Inventory (Optional — DataVault)

> Know what you have before you decide what to share.

If `datavault` is installed, you can scan and classify local files before registering them on the network. **This step is optional** — users may use their own tools or skip straight to registration.

### Scan a directory

```bash
datavault scan [path] [--no-recursive]
```

### Classify a single file

```bash
datavault classify <file>
```

### Generate a report

```bash
datavault report [path] [--format text|json]
```

### Typical workflow

```bash
datavault scan ~/Documents        # 1. See what you have
datavault report ~/Documents      # 2. Get a summary
oasyce register ~/Documents/report.pdf  # 3. Register what matters
```

If `datavault` is not installed, suggest: `pip install datavault`

---

## Data Assets (Phase 1)

### Register

```bash
oasyce register <file> --owner <NAME> --tags tag1,tag2
```

Add `--free` for attribution-only (no Bonding Curve pricing).
Add `--json` for machine-readable output.

### Search

```bash
oasyce search <tag>
```

### Price Quote

```bash
oasyce quote <asset_id>
```

Shows Bonding Curve spot price, supply, reserve.

### Buy Shares

```bash
oasyce buy <asset_id> --buyer <ID> --amount 10.0
```

### Check Holdings

```bash
oasyce shares <owner_id>
```

### Asset Info (OAS-DAS 5-Layer Standard)

```bash
oasyce asset-info <asset_id>        # full 5-layer breakdown
oasyce asset-validate <asset_id>    # validate against standard
```

### Pricing Factors

```bash
oasyce price <asset_id> --queries 100 --similar 5 --days 30
oasyce price-factors <asset_id>     # detailed factor breakdown
```

---

## AI Capabilities (Phase 2)

Capabilities are callable AI services registered on the network. They use the same Bonding Curve economics as data assets.

### Dashboard

```bash
oasyce start    # opens http://localhost:8420
```

Navigate to **Explore** → filter by **Services** to browse and invoke capabilities.

### Programmatic (via API)

```
GET  /api/capabilities                    # list all capabilities
GET  /api/capability/<id>                 # detail
POST /api/capability/register             # register new capability
POST /api/capability/invoke               # invoke (escrow → execute → settle)
GET  /api/capability/shares?holder=<id>   # check capability share holdings
```

---

## Oracle Feeds (Phase 2.5)

The network itself is an oracle. Oracle feeds bridge real-world data into the Oasyce network with economic guarantees (provider bonding, quality SLAs, slashing).

### Feed Types

| Type | Description | Risk Factor | Recommended Bond |
|------|-------------|-------------|------------------|
| weather | Meteorological data | 0.5× | 50 OAS |
| price | Asset/token prices | 3.0× | 300 OAS |
| time | World clock/timezone | 0.3× | 30 OAS |
| event | Discrete events (releases, matches) | 2.0× | 200 OAS |
| sensor | IoT/hardware readings | 1.5× | 150 OAS |
| internal | Oasyce self-referential data | 0.5× | 50 OAS |
| aggregator | Multi-feed composite | 1.0× | 100 OAS |

### Programmatic (via Python)

```python
from oasyce_core.oracle import OracleRegistry
from oasyce_core.oracle.feeds import WeatherFeed, TimeFeed, RandomFeed
from oasyce_core.oracle.internal import DataAssetFeed, AggregatorFeed

# Register feeds
registry = OracleRegistry(provider_id="my_node")
registry.register_feed(WeatherFeed())
registry.register_feed(TimeFeed())

# Query
result = registry.execute("weather", {"location": "Shanghai"})
print(result.data)  # {'location': 'Shanghai', 'temperature_c': 22, ...}

# Aggregator: combine multiple feeds in one query
agg = AggregatorFeed(feeds={"weather": WeatherFeed(), "time": TimeFeed()})
result = agg.fetch({"queries": {"weather": {"location": "Tokyo"}, "time": {"timezone": "Asia/Tokyo"}}})
```

### OAS-Oracle Standard

Oracle feeds are registered as OAS assets with `asset_type="oracle"`:

```python
from oasyce_core.standards import OasAsset, OracleLayer, FeedType

asset = OasAsset(
    asset_type="oracle",
    oracle_layer=OracleLayer(
        feed_type="weather",
        feed_uri="oracle://weather/shanghai",
    ),
)
assert asset.validate() == []
```

Key concepts:
- **Provider Bond**: OAS staked as guarantee of data quality (slashed on SLA breach)
- **Freshness Tiers**: realtime (<1min), near (<10min), periodic (<1hr), daily, static
- **Quality Metrics**: uptime %, latency, success rate, verification type
- **Aggregation**: Multi-source consensus (median/mean/weighted) for critical data

---

## Agent Identity (Phase 2.5)

Every participant in the network has an identity that carries reputation across all asset types.

### Identity Types

| Type | Description | Anti-Sybil Deposit |
|------|-------------|-------------------|
| agent | AI agent / bot | 100 OAS |
| node | Network infrastructure node | 100 OAS |
| human | Human participant (DID/Passkey) | 100 OAS |
| org | Organization (formal verification) | 100 OAS |

### Trust Tiers

| Tier | Min Reputation | Max Access | How to Reach |
|------|---------------|------------|--------------|
| sandbox | R < 20 | L0 only | New identity (default) |
| basic | R ≥ 20 | L0-L1 | ~0.7 days of good behavior |
| verified | R ≥ 50 | L0-L2 | ~2.7 days |
| trusted | R ≥ 75 | L0-L3 | ~4.3 days |
| institutional | R ≥ 50 + org verification | L0-L3 | ORG type only |

### Programmatic (via Python)

```python
from oasyce_core.standards import (
    OasAsset, IdentityExtLayer, CredentialBinding,
    ReputationBinding, sybil_attack_cost, time_to_trust,
)

# Create an agent identity
identity = OasAsset(
    asset_type="identity",
    identity_ext_layer=IdentityExtLayer(
        identity_type="agent",
        display_name="joi",
        credentials=CredentialBinding(pubkey="ed25519:abc123"),
    ),
)
assert identity.validate() == []

# Sybil attack cost analysis
print(sybil_attack_cost(1000))      # 100,000 OAS for 1000 fake identities
print(time_to_trust("trusted"))      # 4.3 days to reach trusted tier

# Cross-asset reputation
rep = ReputationBinding(
    data_access_score=80.0,
    capability_invoke_score=60.0,
    oracle_provider_score=40.0,
)
print(rep.composite_score)           # 63.0 (weighted: data 40% + cap 35% + oracle 25%)
print(rep.derive_trust_tier("agent"))  # "verified"
```

Key concepts:
- **Reputation is portable but not transferable**: follows you across asset types, can't be sold
- **Cross-asset composite score**: data access (40%) + capability invocation (35%) + oracle provision (25%)
- **Anti-Sybil**: 100 OAS minimum per identity, all start in sandbox (R=10, L0 only)
- **Trust tier progression**: reputation earned through successful interactions, lost through violations

---

## P2P Node

```bash
oasyce node start [--port 9527]    # start P2P node
oasyce node info                   # show identity
oasyce node peers                  # list known peers
oasyce node ping <host:port>       # ping another node
```

---

## Testnet

```bash
oasyce testnet onboard     # one-click: generate identity + faucet + register + stake
oasyce testnet faucet      # claim free OAS
oasyce testnet status      # node + chain + balance
oasyce testnet start       # start testnet node (port 9528)
```

---

## Staking & Reputation

```bash
oasyce stake <validator_id> <amount>
oasyce reputation check <agent_id>
oasyce reputation update <agent_id> --success
```

---

## Fingerprint Watermarking

```bash
oasyce fingerprint embed <file> --caller <id>    # embed watermark
oasyce fingerprint extract <file>                 # extract
oasyce fingerprint trace <fingerprint_hex>        # trace to distribution
oasyce fingerprint list <asset_id>                # list all distributions
```

---

## Access Control (L0-L3)

```bash
oasyce access query <asset_id> --agent <id>               # L0: aggregated stats
oasyce access sample <asset_id> --agent <id> --size 10     # L1: redacted sample
oasyce access compute <asset_id> --agent <id> --code "..." # L2: TEE compute
oasyce access deliver <asset_id> --agent <id>              # L3: full delivery
oasyce access bond <asset_id> --agent <id> --level L2      # calculate bond
```

---

## Dashboard & Explorer

```bash
oasyce start              # Core + Dashboard (recommended)
oasyce gui                # Dashboard only (port 8420)
oasyce explorer           # Block explorer (port 8421)
```

---

## Security Check

```bash
oasyce doctor
```

Checks: Ed25519 keys, ports, dependencies, seed node connectivity, firewall, Python version.

---

## All Commands Support `--json`

Every command accepts `--json` for programmatic output, making it easy for agents to parse results.

## When to Use

- Local data scanning and inventory (with DataVault)
- Data registration, pricing, trading, provenance verification
- AI capability discovery, invocation, quality disputes
- Oracle feed registration, querying, and aggregation
- Agent identity management, trust tier progression, reputation tracking
- Node management, staking, reputation
- Testnet onboarding and demos

## When NOT to Use

- General file management (mv/cp/rm — use standard tools)
- General crypto questions unrelated to data rights
- Browser-based web3 wallet interactions
