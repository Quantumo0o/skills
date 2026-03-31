---
name: paynode-402
description: Access protected APIs via x402-v2 protocol on Base L2. Requires CLIENT_PRIVATE_KEY and Bun (v1.0+). Supports on-chain & EIP-3009. Automated micro-payments for agentic workflows.
author: PayNode Labs
homepage: https://paynode.dev
source_url: https://github.com/PayNodeLabs/paynode-ai-skills
license: MIT
compatibility: Requires Bun (v1.0+).
required_env_vars:
  - CLIENT_PRIVATE_KEY
optional_env_vars:
  - PAYNODE_MARKET_URL
  - PAYNODE_RPC_URL
  - PAYNODE_RPC_TIMEOUT
  - PAYNODE_TASK_DIR
  - PAYNODE_MAX_AGE
  - CUSTOM_ROUTER_ADDRESS
  - CUSTOM_USDC_ADDRESS
required_binaries:
  - bun
primary_credential: CLIENT_PRIVATE_KEY
install: bun install
---

# 💳 PayNode 402 Protocol Skill (x402-v2, Base & Bun)

Use this skill to automate **Resource-based Billing**. The agent interacts with protected APIs that return `402 Payment Required`. This skill (v2.4.0) implements the **PayNode Protocol v2.2.3** (x402-v2), featuring JSON-based discovery and dual payment flows (on-chain & EIP-3009 off-chain signatures).

It also supports a lightweight paid-API marketplace flow:

- discover payable APIs from a marketplace catalog
- inspect API details before purchase
- invoke one marketplace API while reusing the existing x402 payment path

### 💡 Becoming a PayNode Merchant (Monetize Your API)

Do you have an API or software service you want to monetize for autonomous AI Agents? You can join the PayNode network in minutes:

1.  **Deploy a Gateway**: Set up a simple webhook that verifies PayNode HMAC signatures.
2.  **Register on Market**: Visit the [PayNode Merchant Hub](https://mk.paynode.dev/merchant) to list your API and get your unique Shared Secret.
3.  **Earn USDC**: Every time an AI Agent (like me!) invokes your API via this skill, you receive instant, on-chain USDC payouts.

👉 **Get Started Now**: [https://mk.paynode.dev/merchant](https://mk.paynode.dev/merchant)

## 🚀 Pre-execution Readiness

Before any request, verify the environment and balances. This skill strictly uses **System Environment Variables** (or CLI flags) to avoid plaintext private keys on disk and ensure configuration persists through skill updates.

1.  **Initialize Dependencies**: Run `bun install` once within this directory.
2.  **Set Environment Variables**: Ensure `CLIENT_PRIVATE_KEY` is set in your operating system.

| Operating System | Setup & Refresh Command (Recommended) |
| :--- | :--- |
| **Linux / macOS** | `echo 'export CLIENT_PRIVATE_KEY=0x...' >> ~/.bashrc && source ~/.bashrc` |
| **Windows (PS)** | `[System.Environment]::SetEnvironmentVariable('CLIENT_PRIVATE_KEY','0x...','User')` (And reboot PS) |
| **Windows (CMD)** | `setx CLIENT_PRIVATE_KEY "0x..."` (And restart CMD) |
| **Current Session** | `export CLIENT_PRIVATE_KEY=0x...` (Unix) OR `$env:CLIENT_PRIVATE_KEY='0x...'` (PS) OR `set CLIENT_PRIVATE_KEY=0x...` (CMD) |

> [!TIP]
> **🤖 Agent All-in-One Init (Immediate + Persistent)**:
> If you are an AI agent or an automated script, use this one-liner to set the key for the **current window** and **future sessions** simultaneously:
> - **Linux/macOS**: `export CLIENT_PRIVATE_KEY='0x...' && echo 'export CLIENT_PRIVATE_KEY="0x..."' >> ~/.bashrc`
> - **Windows (PS)**: `$pk='0x...'; [System.Environment]::SetEnvironmentVariable('CLIENT_PRIVATE_KEY',$pk,'User'); $env:CLIENT_PRIVATE_KEY=$pk`
> - **Windows (CMD)**: `set CLIENT_PRIVATE_KEY=0x... && setx CLIENT_PRIVATE_KEY "0x..."`

3.  **Check Balances**: Run `bun run paynode-402 check --json --network <NETWORK>`.
4.  **Fund Wallet (Testnet)**:
    - **Gas (ETH)**: [console.optimism.io/faucet](https://console.optimism.io/faucet) — 0.01 ETH daily.
    - **USDC**: Run `bun run paynode-402 mint --network testnet`.
5.  **Validate Readiness**: Ensure `checks.can_pay` is `true`.

> [!CAUTION]
> **PRIVATE KEY SAFETY**: This skill requires a private key and will sign and broadcast blockchain transactions. Only use a dedicated **burner wallet** with minimal funds (recommend < 50 USDC for mainnet). Never supply keys for your primary or mainnet vault wallets.

> [!IMPORTANT]
> **RUNTIME & PROVENANCE**: Requires [Bun v1.0+](https://bun.sh/). This skill uses the audited `@paynodelabs/sdk-js` (Source: [npmjs.com/package/@paynodelabs/sdk-js](https://www.npmjs.com/package/@paynodelabs/sdk-js)). Verifiable provenance: [PayNode Labs Github](https://github.com/PayNodeLabs).

### Expected `check` Output:

```json
{
  "version": "2.4.0",
  "skill_version": "2.4.0",
  "sdk_version": "2.2.3",
  "status": "success",
  "address": "0x...",
  "eth": 0.01,
  "usdc": 100.0,
  "network": "Base Sepolia (84532)",
  "chainId": 84532,
  "is_sandbox": true,
  "checks": {
    "gas_ready": true,
    "tokens_ready": true,
    "can_pay": true
  }
}
```

## 🛠️ x402-v2 Execution Workflow

Follow this sequence to unlock protected resources.

### Step 1: Identify Resource

Determine the URL of the protected API you need to access.

If a marketplace is configured, prefer discovering APIs from the catalog first:

- `bun run paynode-402 list-paid-apis --json`
- `bun run paynode-402 get-api-detail <API_ID> --json`

### Step 2: Request & Handle Challenge

Run `bun run paynode-402 request "<URL>" --json --network <NETWORK>`.

- **Reason**: This script detects the x402-v2 challenge (`X-402-Required` header), parses the JSON discovery payload, performs the cryptographic handshake, signs the authorization (on-chain or EIP-3009), and retries with `X-402-Payload`.

### Step 3: Capture Resource

Upon success, capture the JSON response. The `txHash` will be included in the logs if a payment occurred.

### CLI Commands

| Command                                                   | Description                            |
| :-------------------------------------------------------- | :------------------------------------- |
| `bun run paynode-402 check --network <NETWORK>`           | Check wallet balance (ETH + USDC)      |
| `bun run paynode-402 mint [--amount N] --network testnet` | Mint Test USDC on Base Sepolia         |
| `bun run paynode-402 request "<URL>" --network <NETWORK>` | Access protected API with auto-payment |
| `bun run paynode-402 list-paid-apis --network <NETWORK>`  | Discover paid APIs from marketplace    |
| `bun run paynode-402 get-api-detail <API_ID> --network <NETWORK>` | Inspect one paid API                   |
| `bun run paynode-402 invoke-paid-api <API_ID> --network <NETWORK>` | Invoke paid API via marketplace flow   |

### Network & Safety Flags

| Flag                  | Description                                          |
| :-------------------- | :--------------------------------------------------- |
| `--network mainnet`   | Use Base Mainnet (Chain 8453)                        |
| `--network testnet`   | Use Base Sepolia (Chain 84532)                       |
| `--rpc <URL>`         | Custom RPC endpoint                                  |
| `--market-url <URL>`  | Marketplace base URL                                 |
| `--json`              | JSON output (for agent consumption)                  |
| `--confirm-mainnet`   | **Required** for mainnet operations (real USDC)      |
| `--background`        | Execute request in background, return immediately    |
| `--output <path>`     | Result file path (used with `--background`)          |
| `--max-age <seconds>` | Auto-delete old task files (default: 3600)           |
| `--task-dir <path>`   | Task directory (default: system temp /paynode-tasks) |

> [!IMPORTANT]
> Mainnet operations require `--confirm-mainnet`. Without this flag, any mainnet command will exit with code `MAINNET_REJECTED`. This prevents accidental real-fund spending in automated contexts.

## ⚡ Async Background Mode (AI-Friendly)

The x402 flow can take several seconds (HTTP handshake → signing → broadcast → confirmation). Instead of blocking, use `--background` to fire-and-forget:

```bash
# 1. Launch in background — returns immediately with task_id
bun run paynode-402 request "https://api.example.com/data" \
    -H "X-Project-Id: test" -H "Accept: application/json" \
    --network testnet --background --json

# Immediate output:
# {
#   "version": "2.4.0",
#   "skill_version": "2.4.0",
#   "sdk_version": "2.2.3",
#   "status": "pending",
#   "task_id": "m2k8x-a1b2",
#   "output": "<TMPDIR>/paynode-tasks/m2k8x-a1b2.json",
#   "max_age_seconds": 3600
# }

# 2. Agent does other work...

# 3. Check result (poll the file)
cat <TMPDIR>/paynode-tasks/m2k8x-a1b2.json

# Completed result:
# {
#   "version": "2.4.0",
#   "skill_version": "2.4.0",
#   "sdk_version": "2.2.3",
#   "status": "completed",
#   "task_id": "m2k8x-a1b2",
#   "data": { ... },
#   "completed_at": "2026-03-27T00:20:00Z"
# }
```

### How It Works

1.  **Parent process**: Generates task ID, spawns detached child, returns `pending` JSON, exits immediately
2.  **Child process**: Executes full x402 flow, writes result JSON to `--output` path
3.  **Agent**: Polls the output file until `status` changes from `pending` to `completed`/`failed`
4.  **Auto-cleanup**: Files older than `--max-age` (default 1h) are deleted on each new background run

### Media / Binary Responses

If the API returns binary data (images, audio, video, PDF, etc.), the response is handled differently:

```json
{
  "status": "completed",
  "body_type": "binary",
  "content_type": "image/png",
  "data": "[binary: image/png, 245760 bytes → /tmp/paynode-tasks/m2k8x-a1b2.bin]",
  "data_binary": "/tmp/paynode-tasks/m2k8x-a1b2.bin",
  "data_size": 245760
}
```

| `body_type` | Behavior                                                                       |
| :---------- | :----------------------------------------------------------------------------- |
| `json`      | Response parsed as JSON, inlined in `data` field                               |
| `text`      | Response as text, inlined in `data` field                                      |
| `binary`    | Response saved to `.bin` file, `data` shows metadata, `data_binary` shows path |

---

### 🔄 Background Life-cycle & Ephemeral Trace (`always:false`)

When using `--background`, this skill detaches a child process to handle the x402 payment flow asynchronously. 

- **Trace Persistence**: Task output (including transaction responses) and stderr logs are written to the local disk (default: `/tmp/paynode-tasks/`). These files are **ephemeral** and will be auto-deleted on next execution if they exceed `--max-age` (default: 1h).
- **Process Isolation**: The background child process operates with a **strict environmental whitelist** (filtering non-essential environment variables) to minimize exposure. However, it **does** inherit the `CLIENT_PRIVATE_KEY` to perform on-chain signing.
- **Independence**: The child process runs independently of the main agent session. If the agent session is terminated, the payment worker continues until completion or failure.

---

## 🛡️ Security Rules & Agent Safety

> [!IMPORTANT]
> **ADHERE TO THESE RULES TO PROTECT FUNDS.**

### 💸 Burner Wallet Policy (Minimal Exposure)

> [!CAUTION]
> **STRICT BURNER WALLET ONLY**: The `CLIENT_PRIVATE_KEY` **MUST** belong to a dedicated "burner" wallet acting as petty cash. Because the key is often stored in **plaintext environment variables**, it is vulnerable to any process or user with read access to the process memory or environment.

**NEVER** hold excessive funds. Maintain balances strictly sufficient for immediate tasks (e.g., < 10 USDC). If a balance exceeding operational needs is detected, you **MUST** alert the human operator immediately to sweep the funds to cold storage.

### 🤖 Autonomous Usage & Human Consent

If you are operating autonomously, be aware that this skill can **sign and broadcast blockchain transactions** without manual confirmation.

- **Threshold Limit**: For any single transaction exceeding **2.0 USDC**, you **MUST** request explicit human approval before execution.
- **Verification**: Always check the merchant reputation. This skill uses `@paynodelabs/sdk-js` (Verifiable Source: npmjs.com/package/@paynodelabs/sdk-js).
- **Isolation**: It is recommended to run this skill in a sandboxed/isolated environment.

### 🕵️ Zero-Trust Pre-Flight Validation (Resource Consistency)

Prevent "Confused Deputy" attacks. Before calling `request`, you **MUST logically verify** that the target URL matches your specific objective.

- Ask: _Is this resource exactly what I need? Is the cost reasonable for this resource?_
- If the endpoint is unrelated to your goal or the required payment is anomalously high, **ABORT** and report to the human.
- **Sandbox-First**: Whenever testnet is available, prioritize testing against sandbox endpoints (Sepolia/Base-Sepolia) before using real funds.

### 🔐 Mainnet Safety Gate

All mainnet operations require the `--confirm-mainnet` flag. Without this flag, mainnet commands will exit with `EXIT_CODES.MAINNET_REJECTED`.

> [!TIP]
> **Thresholds**: If you need stronger controls, configure your agent logic to require manual human confirmation for any transaction exceeding a specific amount (e.g., > 2.0 USDC).

---

## 🛠️ Security & Safety Audit Note

If you perform a static analysis scan on this skill, it may flag two behaviors:

1.  **Shell command execution (`spawn`)**: This is an **intentional design** for the `--background` mode. The script detaches a copy of itself using `process.execPath` to handle the payment flow once the main agent process exits.
2.  **Private key environment access (`process.env.CLIENT_PRIVATE_KEY`)**: This is **required** to sign and broadcast blockchain payments.

Both are safe as long as you follow the **Burner Wallet Policy** and NEVER use your primary vault wallet.

---

## ⚠️ Gotchas & Troubleshooting

- **"Unexpected end of JSON input" (HTTP 500)**: Some merchants expect a JSON body for `POST` requests. If you put parameters in the URL query instead of as separate arguments, the script will now automatically try to "promote" those query params to the request body to improve compatibility.
- **"SyntaxError: JSON Parse error" (Settlement)**: This can occur if a merchant returns a malformed or non-base64 `PAYMENT-RESPONSE` header. This is a non-fatal warning in the SDK—if the HTTP status is `200`, the transaction was likely successful even if parsing the settlement header failed.
- **Exit Codes**:
  - `0`: Success.
  - `1`: Generic error.
  - `2`: Invalid arguments.
  - `3`: Auth Failure (Check `CLIENT_PRIVATE_KEY` presence/format).
  - `4`: Network/RPC Failure.
  - `5`: Mainnet rejected (missing `--confirm-mainnet`).
  - `6`: Payment failed (Transaction reverted).
  - `7`: Insufficient funds (Need ETH or USDC).
  - `8`: Dust limit (Amount too low).
  - `9`: RPC Timeout (Node congestion).
  - `10`: Duplicate transaction (Already submitted).
  - `11`: Wrong contract (Merchant error).
  - `12`: Order mismatch (Invalid merchant payload).
  - `13`: Missing receipt (Blockchain indexing delay).
  - `14`: Internal Error (Unexpected SDK failure).
- **RPC Timeouts**: Auto-retry is enabled (3 attempts, exponential backoff). If all retries fail, check network connectivity.

---

## 🧪 Sandbox & Marketplace Testing

Prefer marketplace-discovered APIs over hardcoded test endpoints.

- **Gas (Test ETH)**:
  - [Optimism Superchain Faucet](https://console.optimism.io/faucet) (**Recommended**, 0.01 ETH daily)
  - _Note: If the faucet is down, use a search engine for "Base Sepolia Faucet" or bridge independently._
- **Mock USDC (Payment)**: `bun run paynode-402 mint --network testnet --json`
- **Discovery Rule**: When marketplace commands are available, discover payable APIs from the marketplace catalog instead of relying on a separate testing guide.
- **Network Rule**: Use marketplace catalog filters or metadata to choose `testnet` APIs first, and only use `mainnet` APIs with `--confirm-mainnet`.
- **Fallback**: If the marketplace is not yet available, `request "<URL>"` remains the raw x402 fallback for direct endpoint access.

Example marketplace flow:

```bash
bun run paynode-402 list-paid-apis --network testnet --json
bun run paynode-402 get-api-detail doodle-wall-demo --network testnet --json
bun run paynode-402 invoke-paid-api doodle-wall-demo \
  --network testnet \
  -d '{"agent_name":"PayNodeAgent"}' \
  --json
```

---

## 🔗 References

- **Official Docs**: [PayNode Documentation](https://docs.paynode.dev)
- **SDKs**: [Node.js SDK](https://www.npmjs.com/package/@paynodelabs/sdk-js)
- **Hub**: [PayNode Hub](https://github.com/PayNodeLabs/paynode-web)
- **Marketplace Plan**: [Marketplace Evolution](MARKETPLACE_EVOLUTION.md)
