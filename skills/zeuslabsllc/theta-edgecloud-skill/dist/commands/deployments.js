import { edgecloudControllerClient } from '../clients/edgecloudController.js';
export const deployments = {
    listStandard: (cfg, category) => edgecloudControllerClient.listStandardTemplates(cfg, category),
    listCustom: (cfg, projectId) => edgecloudControllerClient.listCustomTemplates(cfg, projectId),
    listVm: (cfg) => edgecloudControllerClient.listVmTypes(cfg),
    create: (cfg, payload) => cfg.dryRun ? { dryRun: true, payload } : edgecloudControllerClient.createDeployment(cfg, payload),
    list: (cfg, projectId) => edgecloudControllerClient.listDeployments(cfg, projectId),
    stop: (cfg, projectId, shard, suffix) => cfg.dryRun ? { dryRun: true } : edgecloudControllerClient.stopDeployment(cfg, projectId, shard, suffix),
    delete: (cfg, projectId, shard, suffix) => cfg.dryRun ? { dryRun: true } : edgecloudControllerClient.deleteDeployment(cfg, projectId, shard, suffix)
};
