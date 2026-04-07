/**
 * singularity-forum - MemoryGraph 模块
 * 轻量级记忆知识图谱
 *
 * 功能：
 * - 节点：Entity（实体：技能、错误模式、决策、文件）
 * - 边：Relation（关系：解决、依赖、导致、包含）
 * - 语义检索：按类型/标签/时间范围查询
 * - 持久化：JSON 文件存储
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const GRAPH_FILE = path.join(os.homedir(), '.cache', 'singularity-forum', 'memory-graph.json');

// =============================================================================
// 类型定义
// =============================================================================

export type NodeType = 'skill' | 'error' | 'decision' | 'file' | 'gene' | 'capsule' | 'lesson' | 'agent';
export type RelationType = 'resolves' | 'depends_on' | 'caused_by' | 'contains' | 'learned_from' | 'applied_to' | 'refined_by';

export interface GraphNode {
  id: string;
  type: NodeType;
  label: string;
  description?: string;
  properties: Record<string, unknown>;
  tags: string[];
  strength?: number; // 0-1，边的强度
  createdAt: string;
  updatedAt: string;
  lastAccessedAt?: string;
}

export interface GraphRelation {
  id: string;
  from: string; // node id
  to: string;   // node id
  type: RelationType;
  label?: string;
  weight?: number; // 0-1
  createdAt: string;
}

export interface MemoryGraph {
  nodes: Record<string, GraphNode>;
  relations: GraphRelation[];
  meta: {
    version: string;
    lastUpdated: string;
    totalNodes: number;
    totalRelations: number;
  };
}

// =============================================================================
// 图谱读写
// =============================================================================

export function loadGraph(): MemoryGraph {
  if (!fs.existsSync(GRAPH_FILE)) {
    return emptyGraph();
  }
  try {
    const raw = fs.readFileSync(GRAPH_FILE, 'utf-8');
    return JSON.parse(raw) as MemoryGraph;
  } catch {
    return emptyGraph();
  }
}

function emptyGraph(): MemoryGraph {
  return {
    nodes: {},
    relations: [],
    meta: { version: '1.0', lastUpdated: new Date().toISOString(), totalNodes: 0, totalRelations: 0 },
  };
}

export function saveGraph(graph: MemoryGraph): void {
  const dir = path.dirname(GRAPH_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  graph.meta.lastUpdated = new Date().toISOString();
  graph.meta.totalNodes = Object.keys(graph.nodes).length;
  graph.meta.totalRelations = graph.relations.length;
  fs.writeFileSync(GRAPH_FILE, JSON.stringify(graph, null, 2), 'utf-8');
}

// =============================================================================
// 节点操作
// =============================================================================

function genId(prefix: string): string {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export function addNode(node: Omit<GraphNode, 'id' | 'createdAt' | 'updatedAt'>): GraphNode {
  const graph = loadGraph();
  const now = new Date().toISOString();
  const full: GraphNode = {
    ...node,
    id: genId(node.type),
    createdAt: now,
    updatedAt: now,
  };
  graph.nodes[full.id] = full;
  saveGraph(graph);
  return full;
}

export function getNode(id: string): GraphNode | null {
  const graph = loadGraph();
  const node = graph.nodes[id];
  if (node) {
    node.lastAccessedAt = new Date().toISOString();
    saveGraph(graph);
  }
  return node || null;
}

export function updateNode(id: string, updates: Partial<GraphNode>): GraphNode | null {
  const graph = loadGraph();
  const node = graph.nodes[id];
  if (!node) return null;
  graph.nodes[id] = { ...node, ...updates, id, updatedAt: new Date().toISOString() };
  saveGraph(graph);
  return graph.nodes[id];
}

export function deleteNode(id: string): boolean {
  const graph = loadGraph();
  if (!graph.nodes[id]) return false;
  delete graph.nodes[id];
  graph.relations = graph.relations.filter(r => r.from !== id && r.to !== id);
  saveGraph(graph);
  return true;
}

export function findNodes(query: {
  type?: NodeType;
  tags?: string[];
  label?: string;
  since?: string; // ISO date
}): GraphNode[] {
  const graph = loadGraph();
  return Object.values(graph.nodes).filter(n => {
    if (query.type && n.type !== query.type) return false;
    if (query.label && !n.label.toLowerCase().includes(query.label.toLowerCase())) return false;
    if (query.tags && !query.tags.every(t => n.tags.includes(t))) return false;
    if (query.since && new Date(n.createdAt) < new Date(query.since)) return false;
    return true;
  });
}

// =============================================================================
// 关系操作
// =============================================================================

export function addRelation(from: string, to: string, type: RelationType, label?: string, weight = 1.0): GraphRelation | null {
  const graph = loadGraph();
  if (!graph.nodes[from] || !graph.nodes[to]) return null;

  const rel: GraphRelation = {
    id: genId('rel'),
    from,
    to,
    type,
    label,
    weight,
    createdAt: new Date().toISOString(),
  };
  graph.relations.push(rel);
  saveGraph(graph);
  return rel;
}

export function getRelations(nodeId: string): GraphRelation[] {
  const graph = loadGraph();
  return graph.relations.filter(r => r.from === nodeId || r.to === nodeId);
}

export function getNeighbors(nodeId: string, relationType?: RelationType): Array<{ node: GraphNode; relation: GraphRelation }> {
  const graph = loadGraph();
  const results: Array<{ node: GraphNode; relation: GraphRelation }> = [];
  for (const rel of graph.relations) {
    if (rel.from === nodeId && (!relationType || rel.type === relationType)) {
      const neighbor = graph.nodes[rel.to];
      if (neighbor) results.push({ node: neighbor, relation: rel });
    }
    if (rel.to === nodeId && (!relationType || rel.type === relationType)) {
      const neighbor = graph.nodes[rel.from];
      if (neighbor) results.push({ node: neighbor, relation: rel });
    }
  }
  return results;
}

// =============================================================================
// 语义查询（基于关键词+标签）
// =============================================================================

export interface SearchOptions {
  query?: string;
  type?: NodeType;
  tags?: string[];
  limit?: number;
  offset?: number;
}

export function searchGraph(opts: SearchOptions): GraphNode[] {
  const graph = loadGraph();
  const query = opts.query?.toLowerCase() || '';
  let results = Object.values(graph.nodes);

  if (opts.type) {
    results = results.filter(n => n.type === opts.type);
  }
  if (opts.tags?.length) {
    results = results.filter(n => opts.tags!.every(t => n.tags.includes(t)));
  }
  if (query) {
    results = results.filter(n =>
      n.label.toLowerCase().includes(query) ||
      (n.description?.toLowerCase().includes(query)) ||
      n.tags.some(t => t.toLowerCase().includes(query))
    );
  }

  const offset = opts.offset || 0;
  const limit = opts.limit || 20;
  return results.slice(offset, offset + limit);
}

// =============================================================================
// 实用封装：记录决策/错误/经验
// =============================================================================

/**
 * 记录一个错误模式
 */
export function recordError(
  signal: string,
  description: string,
  taskType: string,
  solution?: string
): GraphNode {
  const graph = loadGraph();

  // 查找是否已存在相同 signal 的错误节点
  const existing = Object.values(graph.nodes).find(
    n => n.type === 'error' && n.tags.includes(signal)
  );
  if (existing) {
    // 更新访问时间
    updateNode(existing.id, { lastAccessedAt: new Date().toISOString() });
    return existing;
  }

  const node = addNode({
    type: 'error',
    label: signal,
    description,
    properties: { taskType, solution },
    tags: [signal, taskType],
  });

  return node;
}

/**
 * 记录一个决策
 */
export function recordDecision(
  label: string,
  reason: string,
  outcome: string,
  tags: string[] = []
): GraphNode {
  return addNode({
    type: 'decision',
    label,
    description: `Reason: ${reason} | Outcome: ${outcome}`,
    properties: { reason, outcome },
    tags: ['decision', ...tags],
  });
}

/**
 * 记录一条经验教训
 */
export function recordLesson(
  label: string,
  description: string,
  category: string,
  tags: string[] = []
): GraphNode {
  return addNode({
    type: 'lesson',
    label,
    description,
    properties: { category },
    tags: ['lesson', category, ...tags],
  });
}

/**
 * 建立「错误 → 解决方案」的解决关系
 */
export function linkErrorToSolution(errorId: string, solutionNodeId: string): GraphRelation | null {
  return addRelation(errorId, solutionNodeId, 'resolves', 'solved by');
}

// =============================================================================
// 路径查找（两节点间的关系路径）
// =============================================================================

export function findPath(from: string, to: string, maxDepth = 3): string[] | null {
  const graph = loadGraph();
  const visited = new Set<string>();
  const queue: Array<{ id: string; path: string[] }> = [{ id: from, path: [from] }];

  while (queue.length > 0) {
    const { id, path } = queue.shift()!;
    if (id === to) return path;
    if (path.length > maxDepth) continue;
    if (visited.has(id)) continue;
    visited.add(id);

    for (const rel of graph.relations) {
      if (rel.from === id && !visited.has(rel.to)) {
        queue.push({ id: rel.to, path: [...path, rel.to] });
      }
      if (rel.to === id && !visited.has(rel.from)) {
        queue.push({ id: rel.from, path: [...path, rel.from] });
      }
    }
  }

  return null; // 无路径
}

// =============================================================================
// 统计摘要
// =============================================================================

export function getGraphStats(): {
  totalNodes: number;
  totalRelations: number;
  byType: Record<NodeType, number>;
  recentNodes: GraphNode[];
  topTags: Array<{ tag: string; count: number }>;
} {
  const graph = loadGraph();
  const nodes = Object.values(graph.nodes);
  const byType: Record<NodeType, number> = { skill: 0, error: 0, decision: 0, file: 0, gene: 0, capsule: 0, lesson: 0, agent: 0 };
  for (const n of nodes) byType[n.type] = (byType[n.type] || 0) + 1;

  const tagCount: Record<string, number> = {};
  for (const n of nodes) {
    for (const t of n.tags) tagCount[t] = (tagCount[t] || 0) + 1;
  }
  const topTags = Object.entries(tagCount)
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  const recentNodes = nodes
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
    .slice(0, 5);

  return {
    totalNodes: nodes.length,
    totalRelations: graph.relations.length,
    byType,
    recentNodes,
    topTags,
  };
}

// =============================================================================
// 导出/导入（用于备份/迁移）
// =============================================================================

export function exportGraph(): string {
  return JSON.stringify(loadGraph(), null, 2);
}

export function importGraph(json: string): boolean {
  try {
    const imported = JSON.parse(json) as MemoryGraph;
    if (!imported.nodes || !imported.relations) throw new Error('Invalid graph format');
    saveGraph(imported);
    return true;
  } catch {
    return false;
  }
}
