# Ra Pay — OpenClaw Skill

Send compliant fiat USD payments from your AI agent using the Ra Pay CLI.

Ra Pay is the first CLI-native payment platform built for AI agents. It enables business-to-business payments through Stripe's regulated infrastructure with built-in compliance screening, two-step confirmation, and structured JSON output for agents.

## Quick Start

### 1. Install the CLI

```bash
npm install -g @rapay/cli
```

### 2. Set Up Your Account

```bash
# To send payments:
ra add-card        # Save a credit card via Stripe Checkout

# To receive payments:
ra link-bank       # Connect your bank account via Stripe Connect

# Then:
ra accept-tos      # Accept Terms of Service
ra whoami          # Verify your account is ready
```

### 3. Send a Payment

```bash
# Preview (no charge)
ra send 100 USD to acct_RECIPIENT --for "Consulting work - Invoice #42" --json

# Execute (after reviewing the preview)
ra send 100 USD to acct_RECIPIENT --for "Consulting work - Invoice #42" --json --confirm
```

### 4. Check Your Balance

```bash
ra balance --json
```

## How It Works

1. **Install** — `npm install -g @rapay/cli` gets you the `ra` command
2. **Set up** — `ra add-card` to send (credit card) or `ra link-bank` to receive (bank account)
3. **Send** — Every payment goes through a two-step flow: preview fees first, then confirm
4. **Compliance** — Ra Pay validates that every payment has a legitimate business purpose

## Features

- **Two-step confirmation** — Always preview fees before executing payments
- **Business compliance** — Built-in validation ensures payments are for legitimate business purposes
- **JSON output** — Structured responses for AI agents via `--json` flag
- **Stripe-backed** — All payments processed through Stripe's regulated infrastructure
- **Cross-platform** — Works on macOS, Linux, and Windows
- **Agent-to-agent transaction scripts** — Shareable onboarding scripts that a buyer agent can forward to a seller agent (and vice versa) to coordinate payments without both sides needing the skill installed

## All Commands

| Command | Description |
|---------|-------------|
| `ra add-card` | Save credit card for sending payments |
| `ra link-bank` | Connect bank account for receiving payments |
| `ra accept-tos` | Accept Terms of Service |
| `ra send` | Send a payment (two-step confirmation) |
| `ra balance` | Check account balance |
| `ra history` | View transaction history |
| `ra whoami` | Show account info |
| `ra refund` | Open Stripe Dashboard for refunds |
| `ra dispute` | Open Stripe Dashboard for disputes |
| `ra dashboard` | Open Stripe Dashboard |
| `ra unlink` | Disconnect Stripe account |

## Links

- **Website:** [rapay.ai](https://rapay.ai)
- **CLI on npm:** [@rapay/cli](https://www.npmjs.com/package/@rapay/cli)
- **Docs:** [rapay.ai/docs](https://rapay.ai/docs)

## License

MIT
