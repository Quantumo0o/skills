import { deleteEmpty, getJson, postJson, putEmpty } from './http.js';
const BASE_CTRL = 'https://controller.thetaedgecloud.com';
const BASE_API = 'https://api.thetaedgecloud.com';
function k(cfg) {
    if (!cfg.edgecloudApiKey)
        throw new Error('THETA_EC_API_KEY missing');
    return { 'x-api-key': cfg.edgecloudApiKey };
}
function net(cfg, service, headers) {
    return {
        service,
        headers,
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
export const edgecloudControllerClient = {
    listStandardTemplates: (cfg, category) => getJson(`${BASE_CTRL}/deployment_template/list_standard_templates?category=${category}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listCustomTemplates: (cfg, projectId) => getJson(`${BASE_CTRL}/deployment_template/list_custom_templates?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listVmTypes: (cfg) => getJson(`${BASE_API}/resource/vm/list`, net(cfg, 'edgecloud-controller')),
    createDeployment: (cfg, payload) => postJson(`${BASE_CTRL}/deployment`, payload, net(cfg, 'edgecloud-controller', k(cfg))),
    listDeployments: (cfg, projectId) => getJson(`${BASE_CTRL}/deployments/list?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    stopDeployment: (cfg, projectId, shard, suffix) => putEmpty(`${BASE_CTRL}/deployments/${shard}/${suffix}/stop?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    deleteDeployment: (cfg, projectId, shard, suffix) => deleteEmpty(`${BASE_CTRL}/deployments/${shard}/${suffix}?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg)))
};
