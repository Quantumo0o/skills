import { PayNodeAgentClient, RequestOptions } from '@paynodelabs/sdk-js';
import { join, parse } from 'path';
import { tmpdir } from 'os';
import { ethers } from 'ethers';
import fs from 'fs';
import { spawn } from 'child_process';
import {
    getPrivateKey,
    resolveNetwork,
    requireMainnetConfirmation,
    reportError,
    jsonEnvelope,
    withRetry,
    generateTaskId,
    isInlineContent,
    cleanupOldTasks,
    DEFAULT_TASK_DIR,
    DEFAULT_MAX_AGE_SECONDS,
    EXIT_CODES,
    SKILL_VERSION
} from '../utils.ts';

interface UnifiedRequestOptions {
    method?: string;
    data?: string;
    header?: string | string[];
    network?: string;
    rpc?: string;
    json?: boolean;
    confirmMainnet?: boolean;
    background?: boolean;
    dryRun?: boolean;
    output?: string;
    maxAge?: number;
    taskDir?: string;
    taskId?: string;
}

interface CoreResult {
    result: {
        url: string;
        method: string;
        http_status: number;
        content_type: string;
        body_type: 'json' | 'text' | 'binary';
        network: string;
        data: any;
        duration_ms: number;
        dry_run?: boolean;
        wallet?: string;
        message?: string;
        data_binary?: string;
        data_size?: number;
    };
    binaryBuffer?: Uint8Array;
    contentType: string;
}

// --- Background Launcher ---
function spawnBackground(url: string, args: string[], options: UnifiedRequestOptions) {
    const taskId = generateTaskId();
    const taskDir = options.taskDir || DEFAULT_TASK_DIR;
    const maxAge = options.maxAge || DEFAULT_MAX_AGE_SECONDS;
    const outputPath = options.output || join(taskDir, `${taskId}.json`);

    fs.mkdirSync(taskDir, { recursive: true });
    cleanupOldTasks(taskDir, maxAge);

    const originalArgs = process.argv.slice(2);
    const flagsToRemove = ['--background', '--json', '--task-id', '--output', '--dry-run'];
    const childArgs: string[] = [];
    
    for (let i = 0; i < originalArgs.length; i++) {
        const arg = originalArgs[i];
        if (flagsToRemove.includes(arg)) {
            // If flag takes an argument, skip both flag and value
            if ((arg === '--output' || arg === '--task-id') && i + 1 < originalArgs.length) {
                i++; 
            }
            continue;
        }
        childArgs.push(arg);
    }
    childArgs.push('--task-id', taskId, '--output', outputPath);

    const child = spawn(process.execPath, [process.argv[1], ...childArgs], {
        detached: true,
        stdio: 'ignore',
        env: process.env
    });
    child.unref();

    const pendingInfo = {
        status: 'pending',
        task_id: taskId,
        output_file: outputPath,
        task_dir: taskDir,
        max_age_seconds: maxAge,
        command: `cat ${outputPath}`,
        message: '🕒 x402 background request started. The wallet will automatically handle payments.'
    };

    if (options.json) {
        console.log(jsonEnvelope(pendingInfo));
    } else {
        console.log(`\n🚀 **Background Task Started**`);
        console.log(`- **Task ID**: \`${taskId}\``);
        console.log(`- **Output**: \`${outputPath}\``);
        console.log(`\nUse \`cat ${outputPath}\` to check progress.`);
    }
    process.exit(0);
}

// --- Core x402 Execution ---
async function executeCore(url: string, args: string[], options: UnifiedRequestOptions): Promise<CoreResult> {
    const isJson = !!options.json || !!options.taskId;
    const pk = getPrivateKey(isJson);
    const startTs = Date.now();

    const { rpcUrls, networkName, isSandbox } = await resolveNetwork(options.rpc, options.network);
    requireMainnetConfirmation(isSandbox, !!options.confirmMainnet, isJson);

    // Handle params (k=v)
    const kvParams: Record<string, string> = {};
    for (const p of args) {
        if (!p.includes('=')) continue;
        const [k, ...v] = p.split('=');
        kvParams[k.trim()] = v.join('=').trim();
    }

    const method = options.method?.toUpperCase() || (options.data || Object.keys(kvParams).length > 0 ? 'POST' : 'GET');

    // Headers parsing
    const headers: Record<string, string> = {};
    if (options.header) {
        const headerArray = Array.isArray(options.header) ? options.header : [options.header];
        for (const h of headerArray) {
            if (!h || !h.includes(':')) continue;
            const [k, ...v] = h.split(':');
            headers[k.trim()] = v.join(':').trim();
        }
    }

    // Auto-sniff JSON body for manual data
    if (options.data && !headers['Content-Type'] && !headers['content-type']) {
        try {
            JSON.parse(options.data);
            headers['Content-Type'] = 'application/json';
        } catch { /* ignore */ }
    }

    const requestOptions: RequestOptions = { method, headers };
    let targetUrl = url;

    if (method === 'GET') {
        const urlObj = new URL(url);
        for (const [k, v] of Object.entries(kvParams)) {
            urlObj.searchParams.append(k, v);
        }
        targetUrl = urlObj.toString();
    } else {
        if (options.data) {
            requestOptions.body = options.data;
        } else if (Object.keys(kvParams).length > 0) {
            requestOptions.json = kvParams;
        }
    }

    // Dry-run
    if (options.dryRun) {
        return {
            result: {
                url: targetUrl,
                method,
                http_status: 0,
                content_type: 'application/json',
                body_type: 'json',
                network: networkName,
                data: null,
                duration_ms: 0,
                dry_run: true,
                wallet: (new ethers.Wallet(pk)).address,
                message: 'Dry-run: request prepared but not sent.'
            },
            contentType: 'application/json'
        };
    }

    const client = new PayNodeAgentClient(pk, rpcUrls);
    const response = await withRetry(
        () => client.requestGate(targetUrl, requestOptions),
        'x402:requestGate'
    );

    const contentType = response.headers.get('content-type') || 'application/octet-stream';
    const httpStatus = response.status;
    let resultBody: any;
    let bodyType: 'json' | 'text' | 'binary' = 'text';
    let binaryBuffer: Uint8Array | undefined;

    if (isInlineContent(contentType)) {
        if (contentType.toLowerCase().includes('application/json')) {
            resultBody = await response.json();
            bodyType = 'json';
        } else {
            resultBody = await response.text();
            bodyType = 'text';
        }
    } else {
        const arrayBuf = await response.arrayBuffer();
        binaryBuffer = new Uint8Array(arrayBuf);
        bodyType = 'binary';
        resultBody = null;
    }

    return {
        result: {
            url: targetUrl,
            method,
            http_status: httpStatus,
            content_type: contentType,
            body_type: bodyType,
            network: networkName,
            data: resultBody,
            duration_ms: Date.now() - startTs
        },
        binaryBuffer,
        contentType
    };
}

// --- Persistence ---
async function executeAndWrite(url: string, args: string[], options: UnifiedRequestOptions) {
    const taskId = options.taskId || generateTaskId();
    const taskDir = options.taskDir || DEFAULT_TASK_DIR;
    const outputPath = options.output || join(taskDir, `${taskId}.json`);

    fs.mkdirSync(taskDir, { recursive: true });

    try {
        const { result, binaryBuffer, contentType } = await executeCore(url, args, options);
        
        if (binaryBuffer) {
            const { dir, name } = parse(outputPath);
            const binaryPath = join(dir, `${name}.bin`);
            fs.writeFileSync(binaryPath, binaryBuffer);
            result.data = `[binary: ${contentType}, ${binaryBuffer.length} bytes → ${binaryPath}]`;
            result.data_binary = binaryPath;
            result.data_size = binaryBuffer.length;
        }

        const finalOutput = {
            version: SKILL_VERSION,
            status: 'completed',
            task_id: taskId,
            ...result,
            completed_at: new Date().toISOString()
        };

        fs.writeFileSync(outputPath, JSON.stringify(finalOutput, null, 2));
    } catch (error: any) {
        const errorResult = {
            version: SKILL_VERSION,
            status: 'failed',
            task_id: taskId,
            error: error.message,
            errorCode: error?.code || 'internal_error',
            completed_at: new Date().toISOString()
        };
        fs.writeFileSync(outputPath, JSON.stringify(errorResult, null, 2));
    }
}

// --- Main Entry ---
export async function requestAction(url: string, args: string[], options: UnifiedRequestOptions) {
    if (options.background) {
        spawnBackground(url, args, options);
        return;
    }

    if (options.taskId) {
        await executeAndWrite(url, args, options);
        return;
    }

    const isJson = !!options.json;
    
    try {
        if (!isJson && !options.dryRun) {
            console.error(`🌐 x402 Request: ${url}...`);
        }

        const { result, binaryBuffer, contentType } = await executeCore(url, args, options);

        if (binaryBuffer) {
            const binPath = options.output
                ? join(parse(options.output).dir, `${parse(options.output).name}.bin`)
                : join(tmpdir(), `paynode-${Date.now().toString(36)}.bin`);

            fs.writeFileSync(binPath, binaryBuffer);
            result.data = `[binary: ${contentType}, ${binaryBuffer.length} bytes → ${binPath}]`;
            result.data_binary = binPath;
            result.data_size = binaryBuffer.length;
        }

        if (isJson) {
            console.log(jsonEnvelope({ status: 'success', ...result }));
        } else {
            if (result.dry_run) {
                console.log('🧪 DRY RUN PREPARED:');
                console.log(JSON.stringify(result, null, 2));
            } else {
                if (typeof result.data === 'object') {
                    console.log(JSON.stringify(result.data, null, 2));
                } else {
                    console.log(result.data);
                }
            }
        }
    } catch (error: any) {
        reportError(error, isJson, EXIT_CODES.NETWORK_ERROR);
    }
}

