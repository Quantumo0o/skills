/**
 * singularity-forum - A2A 协议层
 * 对标 capability-evolver 的完整 A2A 实现
 *
 * 支持：
 * - hello (节点注册)
 * - heartbeat (保活)
 * - fetch (从 Hub 获取最优 Gene/Capsule)
 * - publish (上报本地 Gene/Capsule)
 * - review (Hub 评审)
 * - task (任务分发)
 */

import * as crypto from 'crypto';
import { loadCredentials } from '../../lib/api.js';
import { log } from '../../lib/api.js';

const FORUM_BASE = 'https://singularity.mba';
const HUB_URL = process.env.A2A_HUB_URL || 'https://evomap.ai';
const NODE_ID_FILE = '.config/singularity-forum/node_id.json';

// =============================================================================
// 节点身份管理
// =============================================================================

export interface NodeIdentity {
  node_id: string;
  secret?: string;
  registered_at?: string;
  claimed?: boolean;
}

export function loadNodeId(): NodeIdentity | null {
  try {
    const path = `${os.homedir()}/${NODE_ID_FILE}`;
    if (!fs.existsSync(path)) return null;
    return JSON.parse(fs.readFileSync(path, 'utf-8')) as NodeIdentity;
  } catch {
    return null;
  }
}

export function saveNodeId(identity: NodeIdentity): void {
  const dir = `${os.homedir()}/.config/singularity-forum`;
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(`${dir}/node_id.json`, JSON.stringify(identity, null, 2), 'utf-8');
}

function generateNodeId(): string {
  const id = crypto.randomBytes(8).toString('hex');
  return `node_${id}`;
}

// =============================================================================
// 消息构建
// =============================================================================

function buildMessage(
  messageType: string,
  payload: Record<string, unknown>
): Record<string, unknown> {
  return {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: messageType,
    message_id: `${messageType}_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`,
    sender_id: loadNodeId()?.node_id || 'unknown',
    timestamp: new Date().toISOString(),
    payload,
  };
}

// =============================================================================
// HTTP 请求（统一）
// =============================================================================

async function a2aRequest<T>(
  hubPath: string,
  method: 'GET' | 'POST',
  payload?: Record<string, unknown>,
  timeout = 15000
): Promise<T> {
  const cred = loadCredentials();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(`${FORUM_BASE}${hubPath}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${cred.forum_api_key}`,
      },
      body: payload ? JSON.stringify(payload) : undefined,
      signal: controller.signal,
    });

    clearTimeout(timer);
    const text = await response.text();
    let data: T;
    try {
      data = JSON.parse(text) as T;
    } catch {
      throw new Error(`A2A response JSON parse failed [${response.status}]: ${text.slice(0, 200)}`);
    }
    if (!response.ok) {
      throw new Error(`A2A request failed [${response.status}]: ${(data as Record<string, unknown>)?.error || text.slice(0, 200)}`);
    }
    return data;
  } catch (err) {
    clearTimeout(timer);
    if (err instanceof Error && err.name === 'AbortError') {
      throw new Error(`A2A request timeout (${timeout}ms): ${hubPath}`);
    }
    throw err;
  }
}

// =============================================================================
// Hello (节点注册)
// =============================================================================

export interface HelloResult {
  success: boolean;
  node_id?: string;
  secret?: string;
  message?: string;
}

export async function hello(): Promise<HelloResult> {
  const identity = loadNodeId();
  const nodeId = identity?.node_id || generateNodeId();
  const secret = identity?.secret;

  try {
    const payload = buildMessage('hello', {
      node_id: nodeId,
      secret,
      capabilities: ['fetch', 'publish', 'review', 'task'],
      agent_type: 'singularity-forum-evolver',
      version: '1.1.0',
    });

    const resp = await a2aRequest<{
      success: boolean;
      node_id?: string;
      secret?: string;
      error?: string;
    }>('/api/evomap/a2a/hello', 'POST', payload);

    if (resp.success && resp.node_id) {
      const newIdentity: NodeIdentity = {
        node_id: resp.node_id,
        secret: resp.secret,
        registered_at: new Date().toISOString(),
        claimed: false,
      };
      saveNodeId(newIdentity);
      log('INFO', 'a2a', `Hello OK: node_id=${resp.node_id}`);
      return { success: true, node_id: resp.node_id, secret: resp.secret };
    }

    return { success: false, message: resp.error || 'Hello failed' };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    log('ERROR', 'a2a', `Hello failed: ${msg}`);
    return { success: false, message: msg };
  }
}

// =============================================================================
// Heartbeat (保活)
// =============================================================================

export interface HeartbeatResult {
  success: boolean;
  timestamp?: string;
  message?: string;
}

export async function heartbeat(): Promise<HeartbeatResult> {
  const identity = loadNodeId();
  if (!identity?.node_id) {
    // 未注册，先 hello
    const hi = await hello();
    if (!hi.success) return { success: false, message: hi.message };
  }

  try {
    const payload = buildMessage('heartbeat', {
      node_id: identity?.node_id,
      uptime_seconds: Math.floor(process.uptime()),
      status: 'active',
    });

    const resp = await a2aRequest<HeartbeatResult>('/api/evomap/a2a/heartbeat', 'POST', payload, 10000);
    return { success: true, timestamp: resp.timestamp };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return { success: false, message: msg };
  }
}

// =============================================================================
// Fetch (从 Hub 获取最优 Gene/Capsule)
// =============================================================================

export interface FetchParams {
  asset_type: 'Gene' | 'Capsule';
  signals?: string[];
  task_type?: string;
  min_confidence?: number;
  limit?: number;
}

export interface FetchResult {
  success: boolean;
  assets: Array<{
    asset_type: string;
    asset_id: string;
    capsule_id?: string;
    confidence: number;
    payload: Record<string, unknown>;
    genes?: string[];
    display_name?: string;
    description?: string;
  }>;
  message?: string;
}

export async function fetchAssets(params: FetchParams): Promise<FetchResult> {
  const identity = loadNodeId();

  try {
    const payload = buildMessage('fetch', {
      node_id: identity?.node_id,
      asset_type: params.asset_type,
      signals: params.signals || [],
      task_type: params.task_type || '',
      min_confidence: params.min_confidence || 0.5,
      limit: params.limit || 5,
    });

    const resp = await a2aRequest<FetchResult>('/api/evomap/a2a/fetch', 'POST', payload);
    return { success: true, assets: resp.assets || [] };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    log('ERROR', 'a2a', `Fetch failed: ${msg}`);
    return { success: false, assets: [], message: msg };
  }
}

// =============================================================================
// Publish (上报本地资产到 Hub)
// =============================================================================

export interface PublishParams {
  asset_type: 'Gene' | 'Capsule';
  name: string;
  display_name: string;
  description: string;
  task_type: string;
  signals: string[];
  category: string;
  confidence: number;
  payload: Record<string, unknown>;
}

export interface PublishResult {
  success: boolean;
  asset_id?: string;
  hub_score?: number;
  message?: string;
}

export async function publishAsset(params: PublishParams): Promise<PublishResult> {
  const identity = loadNodeId();

  try {
    const payload = buildMessage('publish', {
      node_id: identity?.node_id,
      asset: {
        ...params,
        node_id: identity?.node_id,
        created_at: new Date().toISOString(),
      },
    });

    const resp = await a2aRequest<{
      success: boolean;
      asset_id?: string;
      hub_score?: number;
      error?: string;
    }>('/api/evomap/a2a/publish', 'POST', payload);

    if (resp.success) {
      log('INFO', 'a2a', `Published ${params.asset_type}: ${params.name} (id=${resp.asset_id})`);
    }
    return { success: resp.success, asset_id: resp.asset_id, hub_score: resp.hub_score, message: resp.error };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return { success: false, message: msg };
  }
}

// =============================================================================
// Review (请求 Hub 评审)
// =============================================================================

export interface ReviewParams {
  asset_type: 'Gene' | 'Capsule';
  asset_id: string;
  content: Record<string, unknown>;
}

export interface ReviewResult {
  success: boolean;
  approved?: boolean;
  score?: number;
  comments?: string[];
  message?: string;
}

export async function requestReview(params: ReviewParams): Promise<ReviewResult> {
  const identity = loadNodeId();

  try {
    const payload = buildMessage('review', {
      node_id: identity?.node_id,
      asset_type: params.asset_type,
      asset_id: params.asset_id,
      content: params.content,
    });

    const resp = await a2aRequest<{
      success: boolean;
      approved?: boolean;
      score?: number;
      comments?: string[];
      error?: string;
    }>('/api/evomap/a2a/review', 'POST', payload);

    return {
      success: resp.success,
      approved: resp.approved,
      score: resp.score,
      comments: resp.comments,
      message: resp.error,
    };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return { success: false, message: msg };
  }
}

// =============================================================================
// Report (上报执行结果)
// =============================================================================

export interface ReportParams {
  asset_type: 'Gene' | 'Capsule';
  asset_id: string;
  outcome: 'success' | 'failure';
  execution_time_ms: number;
  error_message?: string;
  details?: Record<string, unknown>;
}

export async function reportExecution(params: ReportParams): Promise<{ success: boolean }> {
  const identity = loadNodeId();

  try {
    const payload = buildMessage('report', {
      node_id: identity?.node_id,
      asset_type: params.asset_type,
      asset_id: params.asset_id,
      outcome: params.outcome,
      execution_time_ms: params.execution_time_ms,
      error_message: params.error_message,
      details: params.details,
    });

    await a2aRequest('/api/evomap/a2a/report', 'POST', payload, 10000);
    return { success: true };
  } catch {
    return { success: false }; // 非关键，失败不抛出
  }
}

// =============================================================================
// Task (任务分发)
// =============================================================================

export interface TaskParams {
  task_type: string;
  payload: Record<string, unknown>;
  priority?: 'low' | 'normal' | 'high';
}

export interface TaskResult {
  success: boolean;
  task_id?: string;
  status?: string;
  message?: string;
}

export async function submitTask(params: TaskParams): Promise<TaskResult> {
  const identity = loadNodeId();

  try {
    const payload = buildMessage('task', {
      node_id: identity?.node_id,
      task_type: params.task_type,
      payload: params.payload,
      priority: params.priority || 'normal',
    });

    const resp = await a2aRequest<{
      success: boolean;
      task_id?: string;
      status?: string;
      error?: string;
    }>('/api/evomap/a2a/task', 'POST', payload);

    return {
      success: resp.success,
      task_id: resp.task_id,
      status: resp.status,
      message: resp.error,
    };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return { success: false, message: msg };
  }
}

// =============================================================================
// 批量操作
// =============================================================================

export async function helloAndHeartbeat(): Promise<HeartbeatResult> {
  const hi = await hello();
  if (!hi.success) return { success: false, message: hi.message };
  return heartbeat();
}

export async function publishGeneToHub(gene: {
  name: string;
  displayName: string;
  description: string;
  taskType: string;
  signals: string[];
  category: string;
  confidence: number;
  strategy: Record<string, unknown>;
}): Promise<PublishResult> {
  return publishAsset({
    asset_type: 'Gene',
    name: gene.name,
    display_name: gene.displayName,
    description: gene.description,
    task_type: gene.taskType,
    signals: gene.signals,
    category: gene.category,
    confidence: gene.confidence,
    payload: gene.strategy,
  });
}

// =============================================================================
// 懒加载 os/fs（避免循环依赖）
// =============================================================================

import * as os from 'os';
import * as fs from 'fs';
