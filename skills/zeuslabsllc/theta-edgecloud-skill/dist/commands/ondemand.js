import { onDemandApiClient } from '../clients/ondemandApi.js';
import { listOnDemandServices, ONDEMAND_SERVICE_CATALOG } from './ondemandCatalog.js';
function getFirstInferRequest(payload) {
    if (!payload || typeof payload !== 'object')
        return undefined;
    const body = payload.body;
    if (!body?.infer_requests?.length)
        return undefined;
    return body.infer_requests[0];
}
function isTerminal(state) {
    return state === 'success' || state === 'error' || state === 'failed' || state === 'cancelled';
}
function clampInt(value, fallback, min, max) {
    if (!Number.isFinite(value))
        return fallback;
    return Math.min(Math.max(Math.trunc(value), min), max);
}
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
export const ondemand = {
    catalog: ONDEMAND_SERVICE_CATALOG,
    listServices: () => listOnDemandServices(),
    infer: (cfg, service, payload) => cfg.dryRun ? { dryRun: true, service, payload } : onDemandApiClient.createInferRequest(cfg, service, payload),
    status: (cfg, requestId) => onDemandApiClient.getInferRequest(cfg, requestId),
    inputPresignedUrls: (cfg, service) => cfg.dryRun ? { dryRun: true, service } : onDemandApiClient.createInputPresignedUrls(cfg, service),
    pollUntilDone: async (cfg, requestId, opts = {}) => {
        if (!requestId)
            throw new Error('requestId is required');
        const intervalMs = clampInt(opts.intervalMs, 3000, 100, 60000);
        const timeoutMs = clampInt(opts.timeoutMs, 120000, 1000, 3600000);
        const maxAttempts = clampInt(opts.maxAttempts, 1000, 1, 20000);
        const startedAt = Date.now();
        let attempts = 0;
        while (attempts < maxAttempts) {
            attempts += 1;
            const result = await onDemandApiClient.getInferRequest(cfg, requestId);
            const inferRequest = getFirstInferRequest(result);
            if (isTerminal(inferRequest?.state)) {
                return {
                    attempts,
                    elapsedMs: Date.now() - startedAt,
                    terminalState: inferRequest?.state,
                    result
                };
            }
            if (Date.now() - startedAt >= timeoutMs) {
                return {
                    attempts,
                    elapsedMs: Date.now() - startedAt,
                    terminalState: 'timeout',
                    result
                };
            }
            await sleep(intervalMs);
        }
        return {
            attempts,
            elapsedMs: Date.now() - startedAt,
            terminalState: 'max-attempts',
            result: await onDemandApiClient.getInferRequest(cfg, requestId)
        };
    }
};
