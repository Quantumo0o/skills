import { edgecloudInferenceClient } from '../clients/edgecloudInference.js';
export const inference = {
    models: (cfg, endpoint) => edgecloudInferenceClient.listModels(cfg, endpoint),
    chat: (cfg, body, endpoint) => cfg.dryRun ? { dryRun: true, endpoint, body } : edgecloudInferenceClient.chat(cfg, body, endpoint)
};
