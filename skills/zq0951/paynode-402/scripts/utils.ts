import { ethers } from '@paynodelabs/sdk-js';
import * as dotenv from 'dotenv';
import { tmpdir } from 'os';
import { join, dirname } from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import pkg from '../package.json';

// --- Environment (System Only) ---
// [SECURITY] This skill strictly uses system environment variables for better update persistence 
// and to avoid plaintext private keys on disk. .env files are no longer supported.
if (!process.env.CLIENT_PRIVATE_KEY) {
    // We don't exit here because some commands like 'check' or 'mint' provide their own helpful setup tips.
    // getPrivateKey() will handle the final enforcement.
}

/**
 * Centralized Configuration Loader
 * [SECURITY] Consolidates environment variable access for better auditing.
 */
export const GLOBAL_CONFIG = {
    MARKETPLACE_URL: process.env.PAYNODE_MARKET_URL || 'https://mk.paynode.dev',
    PRIVATE_KEY: process.env.CLIENT_PRIVATE_KEY,
    CUSTOM_ROUTER: process.env.CUSTOM_ROUTER_ADDRESS,
    CUSTOM_USDC: process.env.CUSTOM_USDC_ADDRESS,
    RPC_URL_OVERRIDE: process.env.PAYNODE_RPC_URL || process.env.RPC_URL,
    RPC_TIMEOUT: Number(process.env.PAYNODE_RPC_TIMEOUT) || 15_000
};

/**
 * Skill version for JSON output metadata. 
 */
export const SKILL_VERSION = pkg.version;
export const SDK_VERSION = '2.2.3'; // Bundled default

/**
 * Shared base options for all CLI commands.
 */
export interface BaseCliOptions {
    json?: boolean;
    network?: string;
    rpc?: string;
    rpcTimeout?: number;
    confirmMainnet?: boolean;
    dryRun?: boolean;
    marketUrl?: string;
}


/**
 * Network configuration object.
 */
export interface NetworkConfig {
    provider: ethers.JsonRpcProvider;
    chainId: number;
    isSandbox: boolean;
    rpcUrl: string;
    rpcUrls: string[];
    usdcAddress: string;
    routerAddress: string;
    networkName: string;
}

/**
 * CLI config from parsed arguments (CAC managed, but kept here for type reference).
 */
export interface CliConfig {
    isJson: boolean;
    isHelp: boolean;
    isDryRun: boolean;
    confirmMainnet: boolean;
    background: boolean;
    output?: string;
    maxAge?: number;
    taskDir?: string;
    taskId?: string;
    rpcUrl?: string;
    network?: string;
    marketUrl?: string;
    method?: string;
    data?: string;
    headers?: Record<string, string>;
    params: string[];
}

/**
 * Standardized Exit Codes 
 */
export const EXIT_CODES = {
    SUCCESS: 0,
    GENERIC_ERROR: 1,
    INVALID_ARGS: 2,
    AUTH_FAILURE: 3,
    NETWORK_ERROR: 4,
    MAINNET_REJECTED: 5,
    PAYMENT_FAILED: 6,
    INSUFFICIENT_FUNDS: 7,
    DUST_LIMIT: 8,
    RPC_TIMEOUT: 9,
    DUPLICATE_TRANSACTION: 10,
    WRONG_CONTRACT: 11,
    ORDER_MISMATCH: 12,
    MISSING_RECEIPT: 13,
    INTERNAL_ERROR: 14
} as const;

export const DEFAULT_TIMEOUT_MS = 15_000;
const MAX_RETRIES = 3;

/**
 * Executes an async operation with exponential backoff retry.
 */
export async function withRetry<T>(
    fn: () => Promise<T>,
    label: string,
    maxRetries = MAX_RETRIES
): Promise<T> {
    let lastError: Error | null = null;
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            return await fn();
        } catch (error: any) {
            lastError = error;
            if (!isTransientError(error) || attempt >= maxRetries - 1) throw error;
            const backoffMs = Math.pow(2, attempt) * 1000 * (0.5 + Math.random());
            console.error(`⚠️ [${label}] ${error.message}. Retry #${attempt + 1} (of ${maxRetries - 1}) in ${Math.round(backoffMs)}ms...`);
            await new Promise(resolve => setTimeout(resolve, backoffMs));
        }
    }
    throw lastError || new Error(`${label} failed after ${maxRetries} retries`);
}

function isTransientError(error: any): boolean {
    const msg = (error?.message || '').toLowerCase();
    const code = error?.code || '';

    // --- Error Unwrap ---
    // Extract the deepest cause if it's an RpcError wrapping another error
    const details = error?.details;
    const detailMsg = details
        ? (details.message || (typeof details === 'string' ? details : JSON.stringify(details))).toLowerCase()
        : '';

    // Never retry if it's a known non-transient failure
    const isNonRetryableCode = [
        'CALL_EXCEPTION',
        'INVALID_ARGUMENT',
        'UNSUPPORTED_OPERATION',
        'ACTION_REJECTED',
        'INSUFFICIENT_FUNDS'
    ].includes(code);

    if (
        isNonRetryableCode ||
        msg.includes('insufficient funds') ||
        msg.includes('execution reverted') ||
        detailMsg.includes('insufficient funds') ||
        detailMsg.includes('execution reverted')
    ) {
        return false;
    }

    const isRetryableCode = [
        'NETWORK_ERROR',
        'SERVER_ERROR',
        'TIMEOUT',
        'UNKNOWN_ERROR',
        'rpc_error'
    ].includes(code);

    return (
        isRetryableCode ||
        msg.includes('timeout') ||
        msg.includes('network') ||
        msg.includes('fetch failed') ||
        msg.includes('econnrefused') ||
        msg.includes('econnreset') ||
        msg.includes('socket hang up') ||
        detailMsg.includes('timeout') ||
        detailMsg.includes('network')
    );
}

export const DEFAULT_TASK_DIR = process.env.PAYNODE_TASK_DIR || join(tmpdir(), 'paynode-tasks');
export const DEFAULT_MAX_AGE_SECONDS = Number(process.env.PAYNODE_MAX_AGE) || 3600;

export function generateTaskId(): string {
    const ts = Date.now().toString(36);
    const rand = Math.random().toString(36).substring(2, 6);
    return `${ts}-${rand}`;
}

export function maskAddress(address: string): string {
    if (!address || address.length < 10) return address;
    return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
}

export function isInlineContent(contentType: string): boolean {
    const ct = (contentType || '').split(';')[0].trim().toLowerCase();
    return (
        ct.startsWith('text/') ||
        ct === 'application/json' ||
        ct === 'application/javascript' ||
        ct === 'application/xml' ||
        ct === 'application/x-www-form-urlencoded'
    );
}

export function cleanupOldTasks(taskDir: string, maxAgeSeconds: number): number {
    try {
        if (!fs.existsSync(taskDir)) return 0;
        const now = Date.now();
        const cutoff = now - maxAgeSeconds * 1000;
        let cleaned = 0;
        for (const file of fs.readdirSync(taskDir)) {
            if (file.startsWith('.')) continue;
            const fullPath = join(taskDir, file);
            try {
                const stat = fs.statSync(fullPath);
                // mtimeMs can be updated by reads (depending on mount options), 
                // birthtimeMs is creation. Use the minimum or birthtime for safe cleanup.
                const effectiveTime = Math.min(stat.mtimeMs, stat.birthtimeMs || stat.mtimeMs);
                if (effectiveTime < cutoff) {
                    fs.unlinkSync(fullPath);
                    cleaned++;
                }
            } catch { /* skip */ }
        }
        return cleaned;
    } catch { return 0; }
}


/**
 * Validates existence and format of CLIENT_PRIVATE_KEY.
 */
export function getPrivateKey(isJson: boolean): string {
    const pk: string | undefined = GLOBAL_CONFIG.PRIVATE_KEY;
    if (!pk || typeof pk !== 'string') {
        reportError('CLIENT_PRIVATE_KEY not found in environment. Please set it as a system environment variable.', isJson, EXIT_CODES.AUTH_FAILURE);
    }
    const pkRegex = /^0x[0-9a-fA-F]{64}$/;
    if (!pkRegex.test(pk)) {
        reportError('Invalid CLIENT_PRIVATE_KEY format. Must be 0x-prefixed 64-hex chars.', isJson, EXIT_CODES.AUTH_FAILURE);
    }
    return pk;
}

/**
 * Validates mainnet access.
 */
export function requireMainnetConfirmation(isSandbox: boolean, confirmMainnet: boolean, isJson: boolean): void {
    if (isSandbox) return;
    if (!confirmMainnet) {
        reportError(
            'Mainnet operation requires --confirm-mainnet flag (real USDC).',
            isJson,
            EXIT_CODES.MAINNET_REJECTED
        );
    }
}

/**
 * Resolves network configuration with multi-RPC failover.
 */
export async function resolveNetwork(providedRpcUrl?: string, network?: string, timeoutMs = DEFAULT_TIMEOUT_MS): Promise<NetworkConfig> {
    const {
        PAYNODE_ROUTER_ADDRESS,
        PAYNODE_ROUTER_ADDRESS_SANDBOX,
        BASE_USDC_ADDRESS,
        BASE_USDC_ADDRESS_SANDBOX,
        BASE_RPC_URLS,
        BASE_RPC_URLS_SANDBOX
    } = await import('@paynodelabs/sdk-js');

    const networkAlias = (network || '').toLowerCase();
    const isTestnetRequest =
        networkAlias === 'testnet' ||
        networkAlias === 'sepolia' ||
        networkAlias === 'base-sepolia' ||
        networkAlias === '84532' ||
        networkAlias === 'base-testnet';

    const effectiveRpcUrl = providedRpcUrl || GLOBAL_CONFIG.RPC_URL_OVERRIDE;
    const sdkRpcUrls = (isTestnetRequest ? (BASE_RPC_URLS_SANDBOX || []) : (BASE_RPC_URLS || []));
    const rpcUrls: string[] = effectiveRpcUrl ? [effectiveRpcUrl] : sdkRpcUrls;
    let lastError: Error | null = null;
    let provider: ethers.JsonRpcProvider | null = null;
    let chainId: bigint | null = null;
    let activeRpcUrl: string | null = null;

    for (const url of rpcUrls) {
        try {
            const tempProvider = new ethers.JsonRpcProvider(url, undefined, { staticNetwork: true, batchMaxCount: 1 });
            const networkInfo = await Promise.race([
                tempProvider.getNetwork(),
                new Promise<never>((_, reject) => setTimeout(() => reject(new Error('RPC timeout')), timeoutMs))
            ]);
            provider = tempProvider;
            chainId = networkInfo.chainId;
            activeRpcUrl = url;
            break;
        } catch (error: any) {
            lastError = error;
            if (rpcUrls.length > 1) console.error(`⚠️ [resolveNetwork] RPC ${url} failed: ${error.message}.`);
        }
    }

    if (!provider || !chainId || !activeRpcUrl) {
        throw new Error(`Failed to connect to any RPC in [${rpcUrls.join(', ')}]: ${lastError?.message}`);
    }

    const isSandbox = chainId === 84532n;
    const networkName = isSandbox ? 'Base Sepolia (84532)' : 'Base L2 (8453)';
    const customRouter = GLOBAL_CONFIG.CUSTOM_ROUTER;
    const customUsdc = GLOBAL_CONFIG.CUSTOM_USDC;

    return {
        provider,
        chainId: Number(chainId),
        isSandbox,
        rpcUrl: activeRpcUrl,
        rpcUrls,
        usdcAddress: customUsdc || (isSandbox ? BASE_USDC_ADDRESS_SANDBOX : BASE_USDC_ADDRESS),
        routerAddress: customRouter || (isSandbox ? PAYNODE_ROUTER_ADDRESS_SANDBOX : PAYNODE_ROUTER_ADDRESS),
        networkName
    };
}

export function jsonEnvelope(data: Record<string, any>): string {
    return JSON.stringify({
        version: SKILL_VERSION,
        skill_version: SKILL_VERSION,
        sdk_version: SDK_VERSION,
        ...data
    }, null, 2);
}

export function reportError(err: string | Error | any, isJson: boolean, defaultCode: number = EXIT_CODES.GENERIC_ERROR): never {
    let message = typeof err === 'string' ? err : (err?.message || 'An unknown error occurred');
    let exitCode = defaultCode;
    let errorCode: string | undefined;

    const isPayNodeException = err?.name === 'PayNodeException' ||
        (err?.code && typeof err.code === 'string' && (
            err.code.startsWith('paynode_') ||
            err.code.startsWith('x402_') ||
            (err.code === 'rpc_error' && err?.message?.toLowerCase().includes('paynode'))
        ));
    if (isPayNodeException) {
        errorCode = err.code;

        // --- Defensive Unwrap ---
        // If SDK masks a specific blockchain error as a generic 'rpc_error', try to recover it from details.
        if (errorCode === 'rpc_error' && err.details) {
            const detailMsg = (err.details.message || JSON.stringify(err.details)).toLowerCase();
            if (detailMsg.includes('insufficient funds') || detailMsg.includes('execution reverted')) {
                errorCode = 'insufficient_funds';
                message = 'Insufficient funds for transaction gas or payment. Please verify ETH/USDC balances.';
            } else if (detailMsg.includes('user rejected')) {
                errorCode = 'transaction_failed';
                message = 'Transaction was rejected by the wallet.';
            }
        }

        switch (errorCode) {
            case 'insufficient_funds': exitCode = EXIT_CODES.INSUFFICIENT_FUNDS; break;
            case 'amount_too_low': exitCode = EXIT_CODES.DUST_LIMIT; break;
            case 'rpc_error': exitCode = EXIT_CODES.RPC_TIMEOUT; break;
            case 'transaction_failed': exitCode = EXIT_CODES.PAYMENT_FAILED; break;
            case 'token_not_accepted': exitCode = EXIT_CODES.INVALID_ARGS; break;
            case 'invalid_receipt': exitCode = EXIT_CODES.PAYMENT_FAILED; break;
            case 'wrong_contract': exitCode = EXIT_CODES.WRONG_CONTRACT; break;
            case 'order_mismatch': exitCode = EXIT_CODES.ORDER_MISMATCH; break;
            case 'duplicate_transaction': exitCode = EXIT_CODES.DUPLICATE_TRANSACTION; break;
            case 'missing_receipt': exitCode = EXIT_CODES.MISSING_RECEIPT; break;
            case 'transaction_not_found': exitCode = EXIT_CODES.NETWORK_ERROR; break;
            case 'internal_error': exitCode = EXIT_CODES.INTERNAL_ERROR; break;
            default: exitCode = defaultCode;
        }
    }

    if (isJson) {
        console.log(jsonEnvelope({ status: 'error', message, exitCode, errorCode, details: err?.details }));
    } else {
        const prefix = isPayNodeException ? `🛑 [PayNode-${errorCode}]` : `❌ ERROR:`;
        console.error(`${prefix} ${message} (Code: ${exitCode})`);
        if (errorCode === 'insufficient_funds') {
            console.error(`💡 Tip: Use 'bun run paynode-402 check' to verify ETH/USDC balances.`);
            console.error(`💡 Faucet (Testnet): [console.optimism.io/faucet](https://console.optimism.io/faucet)`);
        } else if (errorCode === 'amount_too_low') {
            const min = err?.details?.minimum || 1000;
            console.error(`💡 Tip: Minimum requirement is ${min} units.`);
        }
    }
    process.exit(exitCode);
}
