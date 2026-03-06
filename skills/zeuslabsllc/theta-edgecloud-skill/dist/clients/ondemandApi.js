import { getJson, postJson } from './http.js';
const BASE = 'https://ondemand.thetaedgecloud.com';
function h(cfg) {
    if (!cfg.onDemandApiToken)
        throw new Error('THETA_ONDEMAND_API_TOKEN missing');
    return {
        Authorization: `Bearer ${cfg.onDemandApiToken}`,
        'content-type': 'application/json'
    };
}
function net(cfg) {
    return {
        headers: h(cfg),
        service: 'theta-ondemand-api',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
export const onDemandApiClient = {
    createInferRequest: (cfg, service, payload) => postJson(`${BASE}/infer_request/${service}`, payload, net(cfg)),
    getInferRequest: (cfg, requestId) => getJson(`${BASE}/infer_request/${requestId}`, net(cfg)),
    createInputPresignedUrls: (cfg, service) => postJson(`${BASE}/infer_request/${service}/input_presigned_urls`, {}, net(cfg))
};
