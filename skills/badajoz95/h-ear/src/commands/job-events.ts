import type { HearApiClient } from '@h-ear/core';
import { formatJobEvents } from '../formatter.js';

export async function jobEventsCommand(
    client: HearApiClient,
    jobId: string,
    options?: { minConfidence?: number; category?: string; limit?: number; offset?: number; sort?: string },
): Promise<string> {
    const result = await client.getJobEvents(jobId, {
        minConfidence: options?.minConfidence,
        category: options?.category,
        limit: options?.limit ?? 20,
        offset: options?.offset ?? 0,
        sort: options?.sort,
    });
    return formatJobEvents(result);
}
