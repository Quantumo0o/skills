---
name: feishu-relay
description: Unified Feishu notification system with automatic discovery, message queue, and reliable delivery. Use when user needs to send notifications via Feishu (Lark) with automatic system registration.
---

# Feishu Relay

Unified Feishu notification system with automatic discovery, message queue, and reliable delivery.

## Features

- **Unified Notification Entry** - All systems use the same `notify` command
- **Automatic System Discovery** - New systems auto-register upon deployment
- **SQLite Message Queue** - Reliable message storage and delivery
- **Automatic Retry** - 3 retry attempts on failure
- **systemd Service Integration** - Background resident service
- **Smart Type Recognition** - Auto-detect website/service/skill/task
- **Framework Detection** - Auto-detect Next.js/Django/Flask/Node/Go/Rust

## Quick Start

```bash
# Install
sudo ./install-v2.sh

# Send notification
notify "Title" "Content"

# List registered systems
feishu-relay-register list
```

## Auto Discovery

New systems deployed to these directories will be auto-discovered:

| Path | Type |
|------|------|
| `/opt/*` | service |
| `/var/www/*` | website |
| `/data/*` | data |
| `/home/*` | user |

## Configuration

Edit `/opt/feishu-notifier/config/feishu.env`:

```
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_USER_ID=ou_xxx
FEISHU_RECEIVE_ID_TYPE=open_id
```

## Commands

```bash
notify "Title" "Content"                  # Send instant notification
feishu-relay-register list                # List all systems
feishu-relay-register status              # Show status
feishu-relay-register scan                # Trigger manual scan
```

## Documentation

- [Auto Discovery](docs/auto-discovery.md)
- [Architecture](ARCHITECTURE.md)

## License

MIT
