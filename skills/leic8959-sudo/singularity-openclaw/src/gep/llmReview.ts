/**
 * singularity-forum - LLM Review 模块
 * 在 Gene/Capsule solidification 之前，用 LLM 做二次验证
 *
 * 功能：
 * - 对候选 Gene 进行安全性+正确性审查
 * - 生成改进建议
 * - 打分（0-1），低于阈值则拒绝发布
 */

import { loadCredentials } from '../../lib/api.js';
import { log } from '../../lib/api.js';

// 评分阈值
const APPROVAL_THRESHOLD = 0.6;
const REVIEW_MODEL = process.env.EVOLVER_MODEL_NAME || 'openai/gpt-4o-mini';
const REVIEW_CACHE_FILE = `${os.homedir()}/.cache/singularity-forum/llm-review-cache.json`;

interface ReviewCache {
  [key: string]: {
    score: number;
    approved: boolean;
    comments: string[];
    timestamp: string;
  };
}

function loadCache(): ReviewCache {
  try {
    const path = `${os.homedir()}/.cache/singularity-forum/llm-review-cache.json`;
    if (fs.existsSync(path)) {
      return JSON.parse(fs.readFileSync(path, 'utf-8'));
    }
  } catch { /* ignore */ }
  return {};
}

function saveCache(cache: ReviewCache): void {
  const dir = `${os.homedir()}/.cache/singularity-forum`;
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(`${dir}/llm-review-cache.json`, JSON.stringify(cache, null, 2), 'utf-8');
}

// =============================================================================
// 评分维度
// =============================================================================

interface GeneReviewInput {
  name: string;
  displayName: string;
  description: string;
  taskType: string;
  category: string;
  signals: string[];
  strategy: {
    steps: string[];
    algorithm?: string;
    description?: string;
  };
  confidence: number;
  gdiScore: number;
}

interface ReviewResult {
  approved: boolean;
  score: number; // 0-1
  comments: string[];
  suggestions: string[];
  safetyIssues: string[];
  reviewedAt: string;
}

function cacheKey(gene: GeneReviewInput): string {
  const data = JSON.stringify(gene);
  const crypto = require('crypto');
  return crypto.createHash('sha256').update(data).digest('hex').slice(0, 16);
}

// =============================================================================
// 构建 Review Prompt
// =============================================================================

function buildReviewPrompt(gene: GeneReviewInput): string {
  return `你是 Gene 发布前的安全审查员。请审查以下 Gene 候选是否适合发布到 EvoMap 网络。

## Gene 信息
- 名称: ${gene.displayName}
- Signal: ${gene.signals.join(', ')}
- 类别: ${gene.category}
- 任务类型: ${gene.taskType}
- 描述: ${gene.description}
- GDI 分数: ${gene.gdiScore}
- 置信度: ${gene.confidence}
- 策略步骤: ${gene.strategy.steps.join(' -> ')}
${gene.strategy.algorithm ? `- 算法: ${gene.strategy.algorithm}` : ''}

## 审查标准
请从以下维度评分（每项 0-1）：
1. 安全性（Safety）：是否包含危险操作（删除文件、eval/exec、硬编码密钥）？
2. 正确性（Correctness）：策略步骤是否逻辑正确？
3. 完整性（Completeness）：是否有遗漏的边界情况？
4. 可执行性（Executability）：描述是否足够清晰可执行？
5. 实用性（Utility）：解决的是真实问题吗？

## 输出要求
请严格按以下 JSON 格式返回（不要有其他内容）：
{
  "safety_score": 0.0-1.0,
  "correctness_score": 0.0-1.0,
  "completeness_score": 0.0-1.0,
  "executability_score": 0.0-1.0,
  "utility_score": 0.0-1.0,
  "overall_score": 0.0-1.0,
  "approved": true/false,
  "safety_issues": ["问题1", "问题2"],
  "comments": ["优点1", "优点2"],
  "suggestions": ["改进建议1"]
}

注意：只有当 overall_score >= 0.6 且没有任何 safety_issues 时才 approved=true。`;
}

// =============================================================================
// 调用 LLM
// =============================================================================

async function callLLM(prompt: string): Promise<string> {
  // 尝试使用 OpenRouter API
  const apiKey = process.env.OPENROUTER_API_KEY || '';
  if (!apiKey) {
    throw new Error('OPENROUTER_API_KEY not set — cannot perform LLM review');
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 60000);

  try {
    const resp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: REVIEW_MODEL,
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.1,
        max_tokens: 1024,
      }),
      signal: controller.signal,
    });

    clearTimeout(timer);
    if (!resp.ok) {
      throw new Error(`OpenRouter error ${resp.status}`);
    }
    const data = await resp.json() as { choices?: Array<{ message?: { content?: string } }> };
    return data.choices?.[0]?.message?.content || '';
  } finally {
    clearTimeout(timer);
  }
}

// =============================================================================
// 解析 Review 响应
// =============================================================================

function parseReviewResponse(text: string): Partial<ReviewResult> {
  // 尝试提取 JSON
  const match = text.match(/\{[\s\S]*\}/);
  if (!match) return {};

  try {
    const parsed = JSON.parse(match[0]);
    return {
      approved: Boolean(parsed.approved),
      score: parseFloat(parsed.overall_score) || 0,
      comments: Array.isArray(parsed.comments) ? parsed.comments : [],
      suggestions: Array.isArray(parsed.suggestions) ? parsed.suggestions : [],
      safetyIssues: Array.isArray(parsed.safety_issues) ? parsed.safety_issues : [],
    };
  } catch {
    return {};
  }
}

// =============================================================================
// 主审流程
// =============================================================================

export async function reviewGene(gene: GeneReviewInput, force = false): Promise<ReviewResult> {
  const key = cacheKey(gene);

  // 缓存检查（1小时内有效）
  if (!force) {
    const cache = loadCache();
    const cached = cache[key];
    if (cached) {
      const age = Date.now() - new Date(cached.timestamp).getTime();
      if (age < 60 * 60 * 1000) {
        log('INFO', 'llmReview', `Cache hit for ${gene.displayName} (score=${cached.score})`);
        return {
          ...cached,
          comments: cached.comments || [],
          suggestions: [],
          safetyIssues: cached.safetyIssues || [],
          reviewedAt: cached.timestamp,
        };
      }
    }
  }

  log('INFO', 'llmReview', `Reviewing gene: ${gene.displayName}...`);

  try {
    const prompt = buildReviewPrompt(gene);
    const response = await callLLM(prompt);
    const parsed = parseReviewResponse(response);

    const result: ReviewResult = {
      approved: parsed.approved ?? false,
      score: parsed.score ?? 0,
      comments: parsed.comments ?? [],
      suggestions: parsed.suggestions ?? [],
      safetyIssues: parsed.safetyIssues ?? [],
      reviewedAt: new Date().toISOString(),
    };

    // 如果没有 overall_score，手动计算
    if (!parsed.score && parsed.safetyIssues !== undefined) {
      const safety_score = 1.0 - (parsed.safetyIssues?.length > 0 ? 0.3 : 0);
      result.score = safety_score;
      result.approved = result.score >= APPROVAL_THRESHOLD && (result.safetyIssues?.length ?? 0) === 0;
    }

    // 更新缓存
    const cache = loadCache();
    cache[key] = { score: result.score, approved: result.approved, comments: result.comments, timestamp: result.reviewedAt };
    saveCache(cache);

    if (result.approved) {
      log('INFO', 'llmReview', `APPROVED ${gene.displayName} (score=${result.score.toFixed(2)})`);
    } else {
      log('WARN', 'llmReview', `REJECTED ${gene.displayName} (score=${result.score.toFixed(2)}) — ${result.safetyIssues?.join('; ')}`);
    }

    return result;
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    log('ERROR', 'llmReview', `Review failed for ${gene.displayName}: ${msg}`);

    // 失败时保守处理：拒绝
    return {
      approved: false,
      score: 0,
      comments: [`Review service unavailable: ${msg}`],
      suggestions: ['Fix LLM review service before publishing'],
      safetyIssues: ['Cannot verify — defaulting to reject for safety'],
      reviewedAt: new Date().toISOString(),
    };
  }
}

/**
 * 批量审查
 */
export async function reviewGenes(genes: GeneReviewInput[]): Promise<ReviewResult[]> {
  return Promise.all(genes.map(g => reviewGene(g)));
}

/**
 * 检查是否需要 LLM Review
 */
export function needsReview(): boolean {
  const val = process.env.EVOLVER_LLM_REVIEW || '0';
  return val === '1' || val === 'true';
}

// =============================================================================
// 懒加载 os/fs
// =============================================================================

import * as os from 'os';
import * as fs from 'fs';
