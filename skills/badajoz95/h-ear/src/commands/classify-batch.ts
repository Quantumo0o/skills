import type { HearApiClient } from '@h-ear/core';

export async function classifyBatchCommand(
    client: HearApiClient,
    urls: string[],
    options?: { threshold?: number; callbackUrl?: string },
): Promise<string> {
    const files = urls.map((url, i) => ({ url, id: `file-${i + 1}` }));
    const result = await client.classifyBatch({
        files,
        callbackUrl: options?.callbackUrl ?? '',
        threshold: options?.threshold ?? 0.3,
    });

    return [
        `**Batch Submitted**`,
        `Batch ID: ${result.batchId}`,
        `Files: ${result.fileCount}`,
        `Estimated: ~${result.estimatedCompletionMinutes} min`,
        `Status: ${result.status}`,
    ].join('\n');
}
