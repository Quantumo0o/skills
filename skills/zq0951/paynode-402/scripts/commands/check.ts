import { ethers } from 'ethers';
import {
    getPrivateKey,
    resolveNetwork,
    requireMainnetConfirmation,
    reportError,
    jsonEnvelope,
    withRetry,
    EXIT_CODES
} from '../utils.ts';

interface CheckOptions {
    network?: string;
    rpc?: string;
    json?: boolean;
    confirmMainnet?: boolean;
}

// Minimum gas threshold: 0.001 ETH (in wei)
const MIN_GAS_WEI = ethers.parseEther('0.001');

export async function checkAction(options: CheckOptions) {
    const isJson = !!options.json;
    const pk = getPrivateKey(isJson);

    try {
        const { provider, usdcAddress, chainId, networkName, isSandbox } = await resolveNetwork(
            options.rpc,
            options.network
        );

        // Mainnet safety gate
        requireMainnetConfirmation(isSandbox, !!options.confirmMainnet, isJson);

        const wallet = new ethers.Wallet(pk, provider);
        const address = wallet.address;

        // Fetch balances with retry
        const [ethBalance, usdcBalance] = await withRetry(
            () => Promise.all([
                provider.getBalance(address),
                new ethers.Contract(
                    usdcAddress,
                    ['function balanceOf(address) view returns (uint256)'],
                    provider
                ).balanceOf(address)
            ]),
            'balanceCheck'
        );

        // BigInt comparisons are used for logic (no precision loss).
        // parseFloat is only for human-readable display and non-critical JSON values.
        const ethValue = parseFloat(ethers.formatEther(ethBalance));
        const usdcValue = parseFloat(ethers.formatUnits(usdcBalance, 6));
        const isGasReady = ethBalance >= MIN_GAS_WEI;
        const isTokensReady = usdcBalance > 0n;

        if (isJson) {
            console.log(
                jsonEnvelope({
                    status: 'success',
                    address,
                    eth: ethValue,
                    usdc: usdcValue,
                    network: networkName,
                    chainId,
                    is_sandbox: isSandbox,
                    checks: {
                        gas_ready: isGasReady,
                        tokens_ready: isTokensReady,
                        can_pay: isGasReady && isTokensReady
                    }
                })
            );
        } else {
            console.log(`\n💎 **PayNode Wallet Status**`);
            console.log(`──────────────────────────────────────────────────`);
            console.log(`👤 **Address**:   \`${address}\``);
            console.log(`🌐 **Network**:   ${networkName}`);
            console.log(`──────────────────────────────────────────────────`);
            console.log(`⛽ **ETH (Gas)**:  ${ethValue.toFixed(6)} ETH  ${isGasReady ? '✅ Ready' : '⚠️ Low balance'}`);
            console.log(`💵 **USDC**:       ${usdcValue.toFixed(2)} USDC  ${isTokensReady ? '✅ Ready' : '❌ Empty'}`);
            console.log(`──────────────────────────────────────────────────`);
            
            if (isGasReady && isTokensReady) {
                console.log(`🚀 **Status**: Ready to handle x402 autonomous payments.`);
            } else {
                console.log(`❌ **Status**: Action required. See tips below.`);
            }

            // Safety Warning for Burner Wallets (Mainnet Only)
            if (!isSandbox && usdcValue > 50) {
                console.warn(
                    `\n> [!CAUTION]\n> High balance detected ($${usdcValue.toFixed(2)} USDC). This is a burner wallet. \n> Consider sweeping excess funds to cold storage to minimize risk.`
                );
            }

            if (!isGasReady) {
                console.warn(
                    `\n> [!WARNING]\n> Gas balance is critically low (< 0.001 ETH). Please deposit ETH to \`${address}\` on ${networkName}.`
                );
            }
            if (!isTokensReady) {
                if (isSandbox) {
                    console.warn(
                        `\n> [!TIP]\n> You're on Testnet! Run \`bun run paynode-402 mint --network testnet\` to get 1,000 free Test USDC.`
                    );
                } else {
                    console.warn(
                        `\n> [!NOTE]\n> Mainnet USDC balance is 0. This wallet is currently restricted to free trials.`
                    );
                }
            }
            console.log(``);
        }
    } catch (error: any) {
        reportError(error, isJson, EXIT_CODES.NETWORK_ERROR);
    }
}
