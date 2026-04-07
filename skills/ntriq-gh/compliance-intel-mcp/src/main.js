import http from 'node:http';
import { Actor } from 'apify';
import log from '@apify/log';

import { assessVendor } from './handlers/assess_vendor.js';
import { canWeProceed } from './handlers/can_we_proceed.js';
import { compareVendors } from './handlers/compare_vendors.js';
import { batchScreen } from './handlers/batch_screen.js';
import { vendorRiskReport } from './handlers/vendor_report.js';

await Actor.init();

Actor.on('aborting', async () => {
    log.info('Actor aborting, shutting down...');
    server.close();
    await Actor.exit();
});

// --- MCP Tool Definitions (Compliance Copilot MCP) ---

const TOOLS = [
    {
        name: 'assess_vendor',
        description: 'Full vendor risk assessment with GO/CAUTION/BLOCK verdict. Analyzes OFAC sanctions, OSHA workplace safety, EPA environmental compliance, and government contract history. Returns decision and confidence level.',
        inputSchema: {
            type: 'object',
            properties: {
                company: { type: 'string', description: 'Company name to assess (e.g., "Tesla", "General Motors")' },
                state: { type: 'string', description: 'US state code for location-specific checks (optional, e.g., "CA")' },
            },
            required: ['company'],
        },
    },
    {
        name: 'can_we_proceed',
        description: 'Quick OFAC sanctions check. Fast binary decision: YES/NO for transaction, vendor, or investment. Used for immediate screening before deeper due diligence.',
        inputSchema: {
            type: 'object',
            properties: {
                entity: { type: 'string', description: 'Entity name to screen (e.g., "Banco Nacional De Cuba")' },
                type: { type: 'string', description: 'Transaction type', enum: ['transaction', 'vendor', 'investment'], default: 'transaction' },
            },
            required: ['entity'],
        },
    },
    {
        name: 'compare_vendors',
        description: 'Compare multiple vendors side-by-side and rank by compliance risk. Returns ranked list with verdicts and scores. Useful for supplier selection.',
        inputSchema: {
            type: 'object',
            properties: {
                vendors: { type: 'array', items: { type: 'string' }, description: 'List of vendor names to compare (max 10)', maxItems: 10 },
                criteria: { type: 'string', description: 'Ranking criteria', enum: ['overall', 'safety', 'compliance'], default: 'overall' },
            },
            required: ['vendors'],
        },
    },
    {
        name: 'batch_screen',
        description: 'Batch screen up to 100 entities for GO/BLOCK decisions. Returns summary and individual results. Efficient for bulk KYC, counterparty screening, or supply chain verification.',
        inputSchema: {
            type: 'object',
            properties: {
                entities: { type: 'array', items: { type: 'string' }, description: 'Array of entity names (max 100)', maxItems: 100 },
                screenType: { type: 'string', description: 'Screening type', enum: ['sanctions', 'full'], default: 'sanctions' },
            },
            required: ['entities'],
        },
    },
    {
        name: 'vendor_risk_report',
        description: 'Generate detailed Markdown report of vendor risk assessment. Includes executive summary, section-by-section analysis, and risk scores from all data sources. Suitable for documentation and escalation.',
        inputSchema: {
            type: 'object',
            properties: {
                company: { type: 'string', description: 'Company name for detailed report (e.g., "Amazon")' },
                format: { type: 'string', description: 'Report format', enum: ['brief', 'full'], default: 'brief' },
            },
            required: ['company'],
        },
    },
];

const TOOL_HANDLERS = {
    assess_vendor: assessVendor,
    can_we_proceed: canWeProceed,
    compare_vendors: compareVendors,
    batch_screen: batchScreen,
    vendor_risk_report: vendorRiskReport,
};

// --- HTTP Helpers ---

function getBody(req) {
    return new Promise((resolve, reject) => {
        const chunks = [];
        req.on('data', (chunk) => chunks.push(chunk));
        req.on('end', () => resolve(Buffer.concat(chunks).toString()));
        req.on('error', reject);
    });
}

function sendJSON(res, statusCode, data) {
    const body = JSON.stringify(data);
    res.writeHead(statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    });
    res.end(body);
}

function mcpResponse(id, result) {
    return { jsonrpc: '2.0', id, result };
}

function mcpError(id, code, message) {
    return { jsonrpc: '2.0', id, error: { code, message } };
}

// --- Charge PPE ---

async function chargePPE() {
    try {
        const result = await Promise.race([
            Actor.charge({ eventName: 'tool-call' }),
            new Promise((_, reject) => setTimeout(() => reject(new Error('charge timeout')), 5000))
        ]);
        if (result?.eventChargeLimitReached) log.warning('User charge limit reached');
    } catch (err) {
        log.debug(`Charge skipped: ${err.message}`);
    }
}

// --- MCP Request Handler ---

async function handleMCPRequest(body) {
    let parsed;
    try { parsed = JSON.parse(body); }
    catch { return mcpError(null, -32700, 'Parse error: invalid JSON'); }

    const { jsonrpc, id, method, params } = parsed;

    if (jsonrpc !== '2.0') return mcpError(id, -32600, 'Invalid request: must use JSON-RPC 2.0');

    if (method === 'initialize') {
        return mcpResponse(id, {
            protocolVersion: '2024-11-05',
            capabilities: { tools: {} },
            serverInfo: { name: 'compliance-intelligence-mcp', version: '1.0.0' },
        });
    }

    if (method === 'notifications/initialized') return mcpResponse(id, {});

    if (method === 'tools/list') return mcpResponse(id, { tools: TOOLS });

    if (method === 'tools/call') {
        const toolName = params?.name;
        const toolArgs = params?.arguments || {};
        const handler = TOOL_HANDLERS[toolName];

        if (!handler) return mcpError(id, -32602, `Unknown tool: ${toolName}. Available: ${Object.keys(TOOL_HANDLERS).join(', ')}`);

        try {
            log.info(`Tool: ${toolName}`, { args: toolArgs });
            const result = await handler(toolArgs);

            await Actor.pushData({
                tool: toolName, status: 'success', args: toolArgs,
                result, timestamp: new Date().toISOString(),
            });
            await chargePPE();

            return mcpResponse(id, {
                content: [{ type: 'text', text: typeof result.report === 'string' ? result.report : JSON.stringify(result, null, 2) }],
            });
        } catch (err) {
            log.error(`Tool ${toolName} failed: ${err.message}`);
            await Actor.pushData({
                tool: toolName, status: 'error', args: toolArgs,
                error: err.message, timestamp: new Date().toISOString(),
            });
            return mcpResponse(id, {
                content: [{ type: 'text', text: `Error: ${err.message}` }],
                isError: true,
            });
        }
    }

    return mcpError(id, -32601, `Method not found: ${method}`);
}

// --- HTTP Server ---

const server = http.createServer(async (req, res) => {
    if (req.method === 'OPTIONS') {
        res.writeHead(204, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        });
        res.end();
        return;
    }

    if (req.method === 'GET') {
        if (req.headers['x-apify-container-server-readiness-probe']) {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('OK\n');
            return;
        }
        sendJSON(res, 200, {
            status: 'ok',
            name: 'Compliance Intelligence MCP Server',
            version: '1.0.0',
            description: 'OFAC sanctions screening, company due diligence (GLEIF+SEC), and US federal contract intelligence for AI agents.',
            tools: TOOLS.length,
            availableTools: TOOLS.map(t => t.name),
            usage: 'POST JSON-RPC 2.0. Methods: initialize, tools/list, tools/call',
        });
        return;
    }

    if (req.method === 'POST') {
        try {
            const body = await getBody(req);
            const result = await handleMCPRequest(body);
            sendJSON(res, 200, result);
        } catch (err) {
            log.error(`Request error: ${err.message}`);
            sendJSON(res, 500, mcpError(null, -32603, `Internal error: ${err.message}`));
        }
        return;
    }

    sendJSON(res, 405, { error: 'Method not allowed. Use GET or POST.' });
});

// --- Standby vs Normal Mode ---

const isStandby = process.env.APIFY_META_ORIGIN === 'STANDBY' || !!process.env.APIFY_ACTOR_STANDBY_PORT;

if (isStandby) {
    const port = parseInt(process.env.APIFY_ACTOR_STANDBY_PORT || '8080', 10);
    server.listen(port, () => {
        log.info(`Compliance Copilot MCP Server running on port ${port}`);
        log.info(`Tools: ${TOOLS.map(t => t.name).join(', ')}`);
    });
} else {
    // Normal run: test a single tool from input
    const input = await Actor.getInput();
    const toolName = input?.tool || 'assess_vendor';
    const handler = TOOL_HANDLERS[toolName];

    if (!handler) {
        log.error(`Unknown tool: ${toolName}`);
        await Actor.pushData({ error: `Unknown tool: ${toolName}`, availableTools: Object.keys(TOOL_HANDLERS) });
        await Actor.exit();
    }

    const args = {
        company: input?.company || 'Tesla',
        entity: input?.entity || 'Banco Nacional De Cuba',
        vendors: input?.vendors || ['Tesla', 'Ford', 'General Motors'],
        entities: input?.entities || ['Amazon', 'Banco Nacional De Cuba', 'Microsoft'],
        state: input?.state || null,
        criteria: input?.criteria || 'overall',
        screenType: input?.screenType || 'sanctions',
        format: input?.format || 'brief',
        ...input,
    };

    try {
        log.info(`Running tool: ${toolName}`, { args });
        const result = await handler(args);
        await Actor.pushData({ tool: toolName, status: 'success', result, timestamp: new Date().toISOString() });
        await chargePPE();
        if (result.executiveReport) log.info(`\n${result.executiveReport}`);
        else if (result.report) log.info(`\n${result.report}`);
    } catch (err) {
        log.error(`Tool ${toolName} failed: ${err.message}`);
        await Actor.pushData({ tool: toolName, status: 'error', error: err.message, timestamp: new Date().toISOString() });
    }

    await Actor.exit();
}
