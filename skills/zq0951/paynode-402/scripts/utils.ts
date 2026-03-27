import { ethers } from 'ethers';
import * as dotenv from 'dotenv';
import { tmpdir } from 'os';
import { join, dirname } from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

// --- Environment Loading (Refined) ---
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Standard priority: CWD .env first, then Skill Root fallback
if (fs.existsSync('.env')) {
    dotenv.config();
} else {
    dotenv.config({ path: join(__dirname, '../.env') });
}

/**
 * Skill version for JSON output metadata. 
 */
export const SKILL_VERSION = '2.2.0';

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

const DEFAULT_TIMEOUT_MS = 10_000;
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
            const backoffMs = Math.pow(2, attempt) * 1000;
            console.error(`⚠️ [${label}] ${error.message}. Retry #${attempt + 1} (of ${maxRetries - 1}) in ${backoffMs}ms...`);
            await new Promise(resolve => setTimeout(resolve, backoffMs));
        }
    }
    throw lastError || new Error(`${label} failed after ${maxRetries} retries`);
}

function isTransientError(error: any): boolean {
    const msg = (error?.message || '').toLowerCase();
    const code = error?.code;
    
    // --- Error Unwrap ---
    // Extract the deepest cause if it's an RpcError wrapping another error
    const details = error?.details;
    const detailMsg = details 
        ? (details.message || (typeof details === 'string' ? details : JSON.stringify(details))).toLowerCase()
        : '';

    // Never retry if it's a known non-transient failure
    if (
        msg.includes('insufficient funds') || 
        msg.includes('execution reverted') ||
        detailMsg.includes('insufficient funds') ||
        detailMsg.includes('execution reverted') ||
        code === 'CALL_EXCEPTION' ||
        code === 'INVALID_ARGUMENT' ||
        code === 'UNSUPPORTED_OPERATION' ||
        code === 'ACTION_REJECTED'
    ) {
        return false;
    }

    return (
        msg.includes('timeout') ||
        msg.includes('network') ||
        msg.includes('fetch failed') ||
        msg.includes('econnrefused') ||
        msg.includes('econnreset') ||
        msg.includes('socket hang up') ||
        code === 'NETWORK_ERROR' ||
        code === 'SERVER_ERROR' ||
        code === 'TIMEOUT' ||
        code === 'rpc_error' ||
        detailMsg.includes('timeout') ||
        detailMsg.includes('network')
    );
}

export function maskString(str: string, visiblePrefix = 6, visibleSuffix = 4): string {
    if (!str || str.length <= visiblePrefix + visibleSuffix) return '********';
    return `${str.substring(0, visiblePrefix)}...${str.substring(str.length - visibleSuffix)}`;
}

export const DEFAULT_TASK_DIR = join(tmpdir(), 'paynode-tasks');
export const DEFAULT_MAX_AGE_SECONDS = 3600;

export function generateTaskId(): string {
    const ts = Date.now().toString(36);
    const rand = Math.random().toString(36).substring(2, 6);
    return `${ts}-${rand}`;
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
                if (stat.mtimeMs < cutoff) {
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
    const pk = process.env.CLIENT_PRIVATE_KEY;
    if (!pk) {
        reportError('CLIENT_PRIVATE_KEY not found in environment. Check .env file.', isJson, EXIT_CODES.AUTH_FAILURE);
    }
    const pkRegex = /^0x[0-9a-fA-F]{64}$/;
    if (!pkRegex.test(pk!)) {
        reportError('Invalid CLIENT_PRIVATE_KEY format. Must be 0x-prefixed 64-hex chars.', isJson, EXIT_CODES.AUTH_FAILURE);
    }
    return pk!;
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
export async function resolveNetwork(rpcUrl?: string, network?: string): Promise<NetworkConfig> {
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

    let rpcUrls: string[] = rpcUrl ? [rpcUrl] : (isTestnetRequest ? BASE_RPC_URLS_SANDBOX : BASE_RPC_URLS);
    let lastError: Error | null = null;
    let provider: ethers.JsonRpcProvider | null = null;
    let chainId: bigint | null = null;

    for (const url of rpcUrls) {
        try {
            const tempProvider = new ethers.JsonRpcProvider(url, undefined, { staticNetwork: true, batchMaxCount: 1 });
            const networkInfo = await Promise.race([
                tempProvider.getNetwork(),
                new Promise<never>((_, reject) => setTimeout(() => reject(new Error('RPC timeout')), DEFAULT_TIMEOUT_MS))
            ]);
            provider = tempProvider;
            chainId = networkInfo.chainId;
            rpcUrl = url;
            break;
        } catch (error: any) {
            lastError = error;
            if (rpcUrls.length > 1) console.error(`⚠️ [resolveNetwork] RPC ${url} failed: ${error.message}.`);
        }
    }

    if (!provider || !chainId) {
        throw new Error(`Failed to connect to any RPC in [${rpcUrls.join(', ')}]: ${lastError?.message}`);
    }

    const isSandbox = chainId === 84532n;
    const networkName = isSandbox ? 'Base Sepolia (84532)' : 'Base L2 (8453)';
    const customRouter = process.env.CUSTOM_ROUTER_ADDRESS;
    const customUsdc = process.env.CUSTOM_USDC_ADDRESS;

    return {
        provider,
        chainId: Number(chainId),
        isSandbox,
        rpcUrl: rpcUrl!,
        rpcUrls,
        usdcAddress: customUsdc || (isSandbox ? BASE_USDC_ADDRESS_SANDBOX : BASE_USDC_ADDRESS),
        routerAddress: customRouter || (isSandbox ? PAYNODE_ROUTER_ADDRESS_SANDBOX : PAYNODE_ROUTER_ADDRESS),
        networkName
    };
}

export function jsonEnvelope(data: Record<string, any>): string {
    return JSON.stringify({ version: SKILL_VERSION, ...data }, null, 2);
}

export function reportError(error: string | Error | any, isJson: boolean, defaultCode: number = EXIT_CODES.GENERIC_ERROR) {
    let message = typeof error === 'string' ? error : (error?.message || 'An unknown error occurred');
    let exitCode = defaultCode;
    let errorCode: string | undefined;

    const isPayNodeException = error?.name === 'PayNodeException' || (error?.code && typeof error.code === 'string');
    if (isPayNodeException) {
        errorCode = error.code;

        // --- Defensive Unwrap ---
        // If SDK masks a specific blockchain error as a generic 'rpc_error', try to recover it from details.
        if (errorCode === 'rpc_error' && error.details) {
            const detailMsg = (error.details.message || JSON.stringify(error.details)).toLowerCase();
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
        console.log(jsonEnvelope({ status: 'error', message, exitCode, errorCode, details: error?.details }));
    } else {
        const prefix = isPayNodeException ? `🛑 [PayNode-${errorCode}]` : `❌ ERROR:`;
        console.error(`${prefix} ${message} (Code: ${exitCode})`);
        if (errorCode === 'insufficient_funds') {
            console.error(`💡 Tip: Use 'bun run paynode-402 check' to verify ETH/USDC balances.`);
        } else if (errorCode === 'amount_too_low') {
            const min = error?.details?.minimum || 1000;
            console.error(`💡 Tip: Minimum requirement is ${min} units.`);
        }
    }
    process.exit(exitCode);
}
