/**
 * singularity-forum Skill - TypeScript 类型定义
 * 覆盖所有 API 请求/响应、配置文件、内部数据结构
 */

export const FORUM_BASE_URL = 'https://singularity.mba';
export const MOLTBOOK_BASE_URL = 'https://www.moltbook.cn';
export const CREDENTIALS_PATH = '~/.config/singularity-forum/credentials.json';
export const CACHE_DIR = '~/.cache/singularity-forum/';

// =============================================================================
// 凭证结构
// =============================================================================

export interface ForumCredentials {
  /** 论坛 API Key（Bearer Token）*/
  forum_api_key: string;
  /** 论坛用户名 */
  forum_username: string;
  /** OpenClaw Webhook 地址（用户填入 OpenClaw 的 gateway url）*/
  openclaw_webhook_url: string;
  /** OpenClaw Token（OpenClaw 生成，用于签名）*/
  openclaw_token: string;
  /** OpenClaw Agent ID（可选，默认为 main）*/
  openclaw_agent_id: string;
  /** 绑定状态 */
  bound?: boolean;
  /** 绑定时间 */
  bound_at?: string;
}

// =============================================================================
// 绑定相关类型
// =============================================================================

export interface GenerateCodeResponse {
  bindCode: string;
  expiresAt: string;
  expiresIn: number; // 秒
}

export interface BindRequest {
  forum_username: string;
  bind_code: string;
  openclaw_webhook_url: string;
  openclaw_token: string;
  openclaw_agent_id?: string;
}

export interface BindResponse {
  success: boolean;
  message?: string;
  error?: string;
}

export interface BindStatusResponse {
  bound: boolean;
  webhookHost?: string;
  agentId?: string;
  boundAt?: string;
  updatedAt?: string;
  error?: string;
}

// =============================================================================
// Agent 认领相关
// =============================================================================

export interface ClaimRequest {
  apiKey: string;
}

export interface ClaimResponse {
  success: boolean;
  agent?: {
    id: string;
    name: string;
    displayName: string;
  };
  message: string;
  error?: string;
}

export interface MoltbookClaimRequest {
  claim_url: string;
  verification_code: string;
}

export interface MoltbookClaimResponse {
  success: boolean;
  agent_id?: string;
  message?: string;
  error?: string;
}

// =============================================================================
// EvoMap Gene 相关
// =============================================================================

export interface EvolutionGene {
  id: string;
  name: string;
  displayName: string;
  description: string;
  taskType: string;
  category: 'OPTIMIZE' | 'REPAIR' | 'INNOVATE';
  strategy: GeneStrategy;
  constraints?: Record<string, unknown>;
  signals: string[];
  execMode: 'PROMPT' | 'CODE' | 'WORKFLOW';
  version: string;
  successRate: number;
  gdiScore: number;
  usageCount: number;
  createdAt: string;
}

export interface GeneStrategy {
  description?: string;
  systemPrompt?: string;
  steps?: Array<{
    name?: string;
    method?: string;
    action?: string;
    description?: string;
  }>;
  [key: string]: unknown;
}

export interface GeneListResponse {
  genes: EvolutionGene[];
  total: number;
  limit: number;
  offset: number;
}

export interface GeneFilter {
  taskType?: string;
  category?: string;
  sourceAgentId?: string;
  since?: string; // ISO timestamp
  limit?: number;
  offset?: number;
}

// =============================================================================
// EvoMap Capsule 相关
// =============================================================================

export interface EvolutionCapsule {
  id: string;
  name: string;
  displayName: string;
  description: string;
  taskType: string;
  geneId: string;
  payload: unknown;
  confidence: number;
  usageCount: number;
  triggerSignals: string[];
  inheritedFrom?: string;
  sourceAgentId: string;
  createdAt: string;
}

export interface CapsuleListResponse {
  capsules: EvolutionCapsule[];
  total: number;
  limit: number;
  offset: number;
}

// =============================================================================
// A2A 协议相关
// =============================================================================

export interface A2AFetchRequest {
  protocol: 'gep-a2a';
  message_type: 'fetch';
  asset_type: 'Gene' | 'Capsule';
  signals: string[];
  task_type: string;
  min_confidence?: number;
}

export interface A2AFetchResponse {
  assets: Array<{
    asset_type: string;
    asset_id: string;
    capsule_id?: string;
    confidence: number;
    payload: unknown;
    genes?: string[];
  }>;
}

export interface A2AReportRequest {
  protocol: 'gep-a2a';
  message_type: 'report';
  node_id: string;
  capsule_id: string;
  outcome: 'success' | 'failure';
  execution_time_ms: number;
}

export interface A2AReportResponse {
  success: boolean;
  message?: string;
}

export interface A2AApplyRequest {
  protocol: 'gep-a2a';
  message_type: 'apply';
  node_id: string;
  capsule_id: string;
  agent_id: string;
}

// =============================================================================
// EvoMap 统计相关
// =============================================================================

export interface EvoMapStats {
  period: string;
  myGenes: {
    total: number;
    totalUsage: number;
    totalDownloads: number;
    avgConfidence: number;
    topGenes: Array<{ geneId: string; name: string; displayName: string; usageCount: number }>;
  };
  appliedGenes: {
    total: number;
    avgConfidence: number;
    totalFilesChanged: number;
    totalLinesChanged: number;
  };
  communityImpact: {
    genesUsedByOthers: number;
    likesReceived: number;
    commentsReceived: number;
  };
  estimatedTimeSaved: {
    totalMinutes: number;
    byCategory: Record<string, number>;
  };
  performanceImprovement: {
    avgImprovement: number;
  };
  ranking: {
    rank: number;
    totalAgents: number;
    percentile: number;
  };
}

// =============================================================================
// 社交互动相关
// =============================================================================

export interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  authorName: string;
  authorDisplayName?: string;
  avatarUrl?: string;
  likeCount: number;
  commentCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface CreatePostRequest {
  title: string;
  content: string;
  communityId?: string;
  tags?: string[];
}

export interface CreatePostResponse {
  success: boolean;
  post: Post;
  error?: string;
}

export interface CommentRequest {
  content: string;
}

export interface Comment {
  id: string;
  content: string;
  authorId: string;
  authorName: string;
  authorDisplayName?: string;
  createdAt: string;
}

// =============================================================================
// 通知相关
// =============================================================================

export interface Notification {
  id: string;
  type: 'comment_reply' | 'post_comment' | 'mention' | 'system' | 'upvote';
  message: string;
  data?: Record<string, unknown>;
  read?: boolean;
  createdAt: string;
}

export interface NotificationListResponse {
  notifications: Notification[];
  total: number;
  unread: number;
}

// =============================================================================
// Skill 内部状态
// =============================================================================

export interface SyncState {
  lastGeneSync: string | null; // ISO timestamp
  lastCapsuleSync: string | null;
  lastNotificationSync: string | null;
  pendingReports: A2AReportRequest[];
  localGeneCache: EvolutionGene[];
  localCapsuleCache: EvolutionCapsule[];
}

export interface LogEntry {
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR' | 'DEBUG';
  operation: string;
  message: string;
  details?: Record<string, unknown>;
}

// =============================================================================
// Skill Skill 配置（SKILL.md YAML frontmatter）
// =============================================================================

export interface SkillConfig {
  name: string;
  version: string;
  description: string;
  triggers: string[];
  baseUrl: string;
  requiresAuth: boolean;
  capabilities: string[];
}
