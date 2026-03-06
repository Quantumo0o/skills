import { loadConfig } from '../config.js';
import { deployments } from '../commands/deployments.js';
import { healthCheck } from '../commands/health.js';
import { inference } from '../commands/inference.js';
import { ondemand } from '../commands/ondemand.js';
import { video } from '../commands/video.js';
import { resolveThetaOnDemandToken } from './secretResolver.js';
function coerceBool(value, fallback) {
    if (value === undefined)
        return fallback;
    const normalized = value.trim().toLowerCase();
    if (['1', 'true', 'yes', 'on'].includes(normalized))
        return true;
    if (['0', 'false', 'no', 'off'].includes(normalized))
        return false;
    return fallback;
}
function coerceInt(value, fallback, min, max) {
    if (!value)
        return fallback;
    const parsed = Number.parseInt(value, 10);
    if (!Number.isFinite(parsed))
        return fallback;
    return Math.min(Math.max(parsed, min), max);
}
async function buildRuntimeConfig(ctx) {
    const base = loadConfig();
    const env = ctx.env ?? {};
    const onDemandApiToken = await resolveThetaOnDemandToken(ctx, base.onDemandApiToken);
    return {
        ...base,
        dryRun: coerceBool(env.THETA_DRY_RUN, base.dryRun),
        edgecloudApiKey: env.THETA_EC_API_KEY ?? base.edgecloudApiKey,
        edgecloudProjectId: env.THETA_EC_PROJECT_ID ?? base.edgecloudProjectId,
        videoSaId: env.THETA_VIDEO_SA_ID ?? base.videoSaId,
        videoSaSecret: env.THETA_VIDEO_SA_SECRET ?? base.videoSaSecret,
        inferenceEndpoint: env.THETA_INFERENCE_ENDPOINT ?? base.inferenceEndpoint,
        onDemandApiToken,
        httpTimeoutMs: coerceInt(env.THETA_HTTP_TIMEOUT_MS, base.httpTimeoutMs, 1000, 120000),
        httpMaxRetries: coerceInt(env.THETA_HTTP_MAX_RETRIES, base.httpMaxRetries, 0, 6),
        httpRetryBackoffMs: coerceInt(env.THETA_HTTP_RETRY_BACKOFF_MS, base.httpRetryBackoffMs, 25, 10000)
    };
}
function requireFields(args, fields) {
    for (const field of fields) {
        if (!(field in args) || args[field] === undefined || args[field] === null || args[field] === '') {
            throw new Error(`Missing required field: ${field}`);
        }
    }
}
const commandRegistry = {
    'theta.health': {
        schema: { command: 'theta.health', description: 'EdgeCloud health check via controller VM listing', required: [] },
        handler: (cfg) => healthCheck(cfg)
    },
    'theta.inference.models': {
        schema: { command: 'theta.inference.models', description: 'List models from dedicated inference endpoint', required: [] },
        handler: (cfg, args) => inference.models(cfg, args.endpoint)
    },
    'theta.inference.chat': {
        schema: { command: 'theta.inference.chat', description: 'Run chat completion on dedicated inference endpoint', required: ['body'] },
        handler: (cfg, args) => inference.chat(cfg, args.body, args.endpoint)
    },
    'theta.ondemand.listServices': {
        schema: { command: 'theta.ondemand.listServices', description: 'List supported on-demand services', required: [] },
        handler: () => ondemand.listServices()
    },
    'theta.ondemand.infer': {
        schema: { command: 'theta.ondemand.infer', description: 'Create on-demand infer request', required: ['service', 'payload'] },
        handler: (cfg, args) => ondemand.infer(cfg, args.service, args.payload)
    },
    'theta.ondemand.status': {
        schema: { command: 'theta.ondemand.status', description: 'Get on-demand infer request status', required: ['requestId'] },
        handler: (cfg, args) => ondemand.status(cfg, args.requestId)
    },
    'theta.ondemand.inputPresignedUrls': {
        schema: { command: 'theta.ondemand.inputPresignedUrls', description: 'Create presigned URLs for on-demand inputs', required: ['service'] },
        handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, args.service)
    },
    'theta.ondemand.pollUntilDone': {
        schema: { command: 'theta.ondemand.pollUntilDone', description: 'Poll on-demand request until terminal state', required: ['requestId'] },
        handler: (cfg, args) => ondemand.pollUntilDone(cfg, args.requestId, args.options)
    },
    'theta.deployments.list': {
        schema: { command: 'theta.deployments.list', description: 'List deployments for project', required: ['projectId'] },
        handler: (cfg, args) => deployments.list(cfg, args.projectId)
    },
    'theta.deployments.listVm': {
        schema: { command: 'theta.deployments.listVm', description: 'List EdgeCloud VM types', required: [] },
        handler: (cfg) => deployments.listVm(cfg)
    },
    'theta.video.list': {
        schema: { command: 'theta.video.list', description: 'List videos for service account', required: ['serviceAccountId'] },
        handler: (cfg, args) => video.videoList(cfg, args.serviceAccountId, args.page ?? 1, args.number ?? 10)
    },
};
const onDemandTokenCommands = new Set([
    'theta.ondemand.infer',
    'theta.ondemand.status',
    'theta.ondemand.inputPresignedUrls',
    'theta.ondemand.pollUntilDone'
]);
export const thetaRuntimeCommandSchemas = Object.fromEntries(Object.entries(commandRegistry).map(([cmd, reg]) => [cmd, reg.schema]));
export function listThetaRuntimeCommands() {
    return Object.keys(commandRegistry).sort();
}
export async function executeThetaRuntimeCommand(args, ctx = {}) {
    const registration = commandRegistry[args.command];
    if (!registration) {
        throw new Error(`Unsupported theta runtime command: ${args.command}`);
    }
    requireFields(args, registration.schema.required);
    const cfg = await buildRuntimeConfig(ctx);
    if (onDemandTokenCommands.has(args.command) && !cfg.dryRun && !cfg.onDemandApiToken) {
        throw new Error('THETA_ONDEMAND_API_TOKEN missing (runtime secret/env resolver)');
    }
    return registration.handler(cfg, args);
}
