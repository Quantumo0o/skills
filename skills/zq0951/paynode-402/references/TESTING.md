# Sandbox & Testing (Base Sepolia)

This guide covers how to test the PayNode x402-v2 payment flow in a safe environment using the Base Sepolia Testnet.

## 1. Prerequisites

- Your wallet must have **Base Sepolia ETH** for gas.
- You must have **MockUSDC** on the testnet.
- SDK version: `@paynodelabs/sdk-js@2.2.0`
- Runtime: [Bun](https://bun.sh/) v1.0+

## 2. Mint Test Tokens

If your testnet wallet is low on USDC, run the minting script to receive **1,000 MockUSDC**:

```bash
# Execute from the skill root
bun run paynode-402 mint --network testnet --json
```

Alternatively, you can mint manually via [Basescan Sepolia](https://sepolia.basescan.org/address/0x65c088EfBDB0E03185Dbe8e258Ad0cf4Ab7946b0#writeContract).

### 3. Standard x402-v2 Interface Tests

We provide two primary test endpoints to verify protocol compatibility:

#### Case A: Doodle Wall (On-chain / Legacy Support)
This endpoint supports standard on-chain txHash verification (USDC transfer). Use it to test gas-heavy flows.

```bash
# Handshake + Auto-pay (On-chain) + Verification
bun run paynode-402 request "https://paynode.dev/api/pom?network=testnet" \
    --network testnet \
    -X POST \
    agent_name="OnChainAgent" \
    --json
```

- **Web UI**: Visit [paynode.dev/pom?network=testnet](https://paynode.dev/pom?network=testnet) to see your Agent on the leaderboard.

#### Case B: Compatibility Test (EIP-3009 / Optimized)
This is the **recommended** way for AI Agents. It tests EIP-3009 offline signatures (sub-50ms) and handles V2 settlement headers.

```bash
# Handshake + Auto-pay (EIP-3009) + Verification
bun run paynode-402 request "https://www.paynode.dev/api/test/x402?network=testnet" \
    --network testnet \
    -X POST \
    agent_name="EIP3009Test" \
    --json
```

- **Success Signal**: Look for `✅ [PayNode-JS] Settlement confirmed: eip3009:0x...` in the logs.

### Mainnet Operations

Mainnet operations (real USDC) require the `--confirm-mainnet` flag:

```bash
# ❌ This will fail — missing --confirm-mainnet
bun run paynode-402 check --network mainnet

# ✅ This works
bun run paynode-402 check --network mainnet --confirm-mainnet --json

# ✅ Request on mainnet
bun run paynode-402 request "https://api.example.com" \
    --network mainnet \
    --confirm-mainnet \
    --json
```

### Background Mode (Async)

For long-running 402 requests, use `--background` to avoid blocking the agent:

```bash
# Launch async — returns immediately
bun run paynode-402 request "https://paynode.dev/api/pom?network=testnet" \
    --network testnet \
    --background \
    -X POST \
    agent_name="My AI Agent" \
    --json

# Output:
# { "status": "pending", "task_id": "m2k8x-a1b2", "output": "<TMPDIR>/paynode-tasks/m2k8x-a1b2.json" }

# Check result later
cat <TMPDIR>/paynode-tasks/m2k8x-a1b2.json

# Custom output path
bun run paynode-402 request "https://..." \
    --network testnet --background --output /tmp/my-result.json --json

# Custom cleanup age (default 3600s)
bun run paynode-402 request "https://..." \
    --network testnet --background --max-age 7200 --json
```

## 4. Custom Contract Testing

To test against your own deployed PayNode Router contract:

### Step 1: Deploy Your Router

Deploy the PayNodeRouter contract to Base Sepolia using Foundry:

```bash
cd packages/contracts
forge script script/Deploy.s.sol --rpc-url $BASE_SEPOLIA_RPC --broadcast --verify
```

### Step 2: Configure Environment

Add your custom contract address to `.env`:

```env
CUSTOM_ROUTER_ADDRESS=0xYourDeployedRouterAddress
CUSTOM_USDC_ADDRESS=0xYourUSDCAddress  # Or use standard testnet USDC
```

### Step 3: Test with Custom Contract

```bash
# Using the request command with custom RPC
bun run paynode-402 request "https://your-merchant.com/api/protected" \
    --network testnet \
    --rpc https://sepolia.base.org \
    -X POST \
    --json
```

### Step 4: Verify Contract Compatibility

Your contract must implement:

```solidity
// Required functions
function pay(address token, address merchant, uint256 amount, bytes32 orderId) external;
function payWithPermit(address payer, address token, address merchant, uint256 amount, bytes32 orderId, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external;

// Required event
event PaymentReceived(bytes32 indexed orderId, address indexed merchant, address indexed payer, address token, uint256 amount, uint256 fee, uint256 chainId);
```

## 5. Sandbox Configuration

| Parameter    | Testnet Value                                | Mainnet Value                                |
| :----------- | :------------------------------------------- | :------------------------------------------- |
| **Network**  | Base Sepolia (84532)                         | Base Mainnet (8453)                          |
| **Router**   | `0x24cD8b68aaC209217ff5a6ef1Bf55a59f2c8Ca6F` | `0x4A73696ccF76E7381b044cB95127B3784369Ed63` |
| **USDC**     | `0x65c088EfBDB0E03185Dbe8e258Ad0cf4Ab7946b0` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| **Treasury** | `0x598bF63F5449876efafa7b36b77Deb2070621C0E` | `0x598bF63F5449876efafa7b36b77Deb2070621C0E` |

## 6. Troubleshooting

| Issue              | Cause                | Solution                                                           |
| :----------------- | :------------------- | :----------------------------------------------------------------- |
| 402 Loop           | Payment not verified | Check `X-402-Payload` is correctly Base64 encoded                  |
| `invalid_receipt`  | Wrong network        | Ensure agent and merchant are on same network (testnet vs mainnet) |
| `amount_too_low`   | Dust amount          | Minimum is 1000 units (0.001 USDC)                                 |
| `wrong_contract`   | Invalid router       | Verify router address matches `X-402-Required` response            |
| `MAINNET_REJECTED` | Missing flag         | Add `--confirm-mainnet` for mainnet operations                     |
| `RPC timeout`      | Node unreachable     | Check network connectivity; auto-retry (3x) is enabled             |
