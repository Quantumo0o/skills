import type { HearApiClient } from '@h-ear/core';
import { formatClassifySubmitted, formatClassifyResult } from '../formatter.js';

/** Default gateway webhook receiver — OpenClaw routes results back to the user's channel. */
const GATEWAY_CALLBACK = 'https://gateway.openclaw.ai/webhooks/h-ear';

/** Async submit — returns immediately with job ID. Results delivered via callbackUrl. */
export async function classifyCommand(
    client: HearApiClient,
    url: string,
    options?: { threshold?: number; callbackUrl?: string },
): Promise<string> {
    const accepted = await client.submitClassify({
        url,
        threshold: options?.threshold ?? 0.3,
        callbackUrl: options?.callbackUrl ?? GATEWAY_CALLBACK,
    });
    return formatClassifySubmitted(accepted);
}

/** Sync classify — submits, polls until complete, returns formatted result. */
export async function classifySyncCommand(
    client: HearApiClient,
    url: string,
    options?: { threshold?: number },
    onProgress?: (msg: string) => void,
): Promise<string> {
    const result = await client.classify(
        { url, threshold: options?.threshold ?? 0.3 },
        onProgress,
    );
    return formatClassifyResult(result);
}
