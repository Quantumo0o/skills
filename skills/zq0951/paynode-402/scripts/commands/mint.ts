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

interface MintOptions {
    network?: string;
    rpc?: string;
    json?: boolean;
    confirmMainnet?: boolean;
    amount?: string;
}

export async function mintAction(options: MintOptions) {
    const isJson = !!options.json;
    const pk = getPrivateKey(isJson);

    try {
        const { provider, usdcAddress, chainId, networkName, isSandbox } = await resolveNetwork(
            options.rpc,
            options.network || 'testnet'
        );

        if (!isSandbox) {
            throw new Error(`Minting is only supported on Sepolia. Current ChainID: ${chainId}`);
        }

        const wallet = new ethers.Wallet(pk, provider);
        const mintAmountStr = options.amount || '1000';

        // Gas check
        const balance = await provider.getBalance(wallet.address);
        if (balance === 0n && !isJson) {
            console.warn(`\n> [!WARNING]\n> Gas balance is 0 ETH. The mint transaction will fail.`);
            console.warn(`> Please deposit a small amount of ETH to \`${wallet.address}\` on ${networkName}.`);
        }

        if (!isJson) {
            console.error(`💰 Connecting to ${networkName}...`);
            console.error(`🔗 Minting ${mintAmountStr} USDC for address: ${wallet.address}`);
        }

        const abi = ['function mint(address to, uint256 amount) external'];
        const usdc = new ethers.Contract(usdcAddress, abi, wallet);

        const amount = ethers.parseUnits(mintAmountStr.toString(), 6);

        if (!isJson) console.error('⏳ Sending mint transaction...');
        const tx = await withRetry(
            () => usdc.mint(wallet.address, amount),
            'mint'
        );

        if (!isJson) console.error('⏳ Waiting for confirmation...');
        const receipt: any = await withRetry(
            () => tx.wait(),
            'mintConfirm'
        );

        if (!receipt || receipt.status !== 1) {
            throw new Error('Transaction reverted or failed.');
        }

        if (isJson) {
            console.log(
                jsonEnvelope({
                    status: 'success',
                    txHash: tx.hash,
                    address: wallet.address,
                    amount: mintAmountStr,
                    token: 'MockUSDC',
                    network: networkName
                })
            );
        } else {
            console.log(`\n✅ **Success!**`);
            console.log(`──────────────────────────────────────────────────`);
            console.log(`💰 **Minted**:      ${mintAmountStr} Test USDC`);
            console.log(`🌐 **Network**:     ${networkName}`);
            console.log(`🔗 **Tx Hash**:     \`${tx.hash}\``);
            console.log(`──────────────────────────────────────────────────`);
            console.log(`🚀 **Your wallet (\`${wallet.address}\`) is now funded and ready for testing.**`);
            console.log(``);
        }
    } catch (error: any) {
        reportError(error, isJson, EXIT_CODES.NETWORK_ERROR);
    }
}
