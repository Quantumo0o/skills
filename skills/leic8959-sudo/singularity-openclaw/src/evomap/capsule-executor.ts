/**
 * EvoMap Capsule Executor
 * 根据 Gene.execMode 执行对应的 Capsule.payload
 * 支持 PROMPT / CODE / WORKFLOW 三种模式
 */

import { createHash } from 'crypto';
import { executeCodeSandbox } from './sandbox-executor';

const PROXY_BASE_URL = process.env.NEXT_PUBLIC_APP_URL || process.env.PROXY_BASE_URL || 'http://localhost:3000';

export type ExecMode = 'PROMPT' | 'CODE' | 'WORKFLOW';

export interface ExecutionResult {
  success: boolean;
  output: unknown;
  error?: string;
  duration: number;       // 毫秒
  confidence: number;    // 0-1
  execMode: ExecMode;
  steps: string[];        // 执行步骤日志
}

// ============= PROMPT 模式 =============

interface PromptPayload {
  systemPrompt?: string;   // 追加到 System Prompt 的策略内容
  userTemplate?: string;   // User Prompt 模板
  model?: string;         // 可选指定模型
  temperature?: number;
  maxTokens?: number;
}

/**
 * PROMPT 模式：使用 OpenRouter 兼容接口调用 LLM
 * payload 中包含 systemPrompt 片段，会被拼入系统 Prompt
 */
async function executePromptMode(
  capsuleId: string,
  payload: unknown,
  geneStrategy: unknown,
  taskInput: unknown,
  geneSignals: string[],
): Promise<ExecutionResult> {
  const steps: string[] = [`[PROMPT] Capsule: ${capsuleId}`];
  const start = Date.now();

  try {
    const pp = payload as PromptPayload;
    const gs = geneStrategy as Record<string, unknown> | null;

    // 构建系统 Prompt：基础角色 + gene 策略片段
    const geneSystemPrompt = gs?.systemPrompt
      || gs?.algorithm
      || extractStrategyDescription(gs)
      || '';

    const fullSystemPrompt = `你是一个专业的 AI 任务处理引擎。

## 任务输入
${JSON.stringify(taskInput, null, 2)}

## 执行的策略片段
${geneSystemPrompt}

## 约束条件
${JSON.stringify(gs?.constraints || {}, null, 2)}

## 指令
按照上述策略执行任务，直接输出结果，不需要解释过程。`.trim();

    steps.push(`System prompt length: ${fullSystemPrompt.length} chars`);

    // 调用 OpenRouter 兼容 API（使用项目中已有的代理接口）
    const response = await fetch(`${PROXY_BASE_URL}/api/proxy/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: pp.model || 'anthropic/claude-3-haiku',
        agentId: 'cmmsuw4zc0000puc75s903ptu',
        messages: [
          { role: 'system', content: fullSystemPrompt },
          { role: 'user', content: pp.userTemplate?.replace('{{input}}', JSON.stringify(taskInput)) || JSON.stringify(taskInput) },
        ],
        temperature: pp.temperature ?? 0.3,
        max_tokens: pp.maxTokens ?? 2048,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`LLM API error ${response.status}: ${errText}`);
    }

    // 先获取文本，以便在 JSON 解析失败时记录
    const text = await response.text();
    let data;

    try {
      data = JSON.parse(text) as { choices?: Array<{ message?: { content?: string } }> };
    } catch (parseError) {
      console.error('[PROMPT] JSON parse error:', parseError);
      console.error('[PROMPT] Raw response:', text.substring(0, 200));
      throw new Error(`Failed to parse LLM response: ${parseError instanceof Error ? parseError.message : 'Unknown error'}`);
    }

    const content = data.choices?.[0]?.message?.content;

    steps.push(`LLM output length: ${(content || '').length} chars`);

    return {
      success: true,
      output: content || '',
      duration: Date.now() - start,
      confidence: 0.85,
      execMode: 'PROMPT',
      steps,
    };
  } catch (err) {
    const error = err as Error;
    steps.push(`ERROR: ${error.message}`);
    return {
      success: false,
      output: null,
      error: error.message,
      duration: Date.now() - start,
      confidence: 0,
      execMode: 'PROMPT',
      steps,
    };
  }
}

/**
 * 从 strategy JSON 中提取描述性文本
 */
function extractStrategyDescription(strategy: unknown): string {
  if (!strategy || typeof strategy !== 'object') return '';
  const s = strategy as Record<string, unknown>;
  if (s.description) return String(s.description);
  if (Array.isArray(s.steps)) {
    return (s.steps as Array<Record<string, unknown>>)
      .map((step, i) => `${i + 1}. ${step.method || step.action || step.name}: ${step.description || ''}`)
      .join('\n');
  }
  return JSON.stringify(strategy);
}

// ============= CODE 模式 =============

interface CodePayload {
  language: 'javascript' | 'python';
  code: string;
  timeout?: number;
}

/**
 * CODE 模式：在沙箱中执行代码片段
 * 仅在非生产环境启用，生产环境需替换为 vm2 / isolated-vm
 */
async function executeCodeMode(
  capsuleId: string,
  payload: unknown,
  taskInput: unknown,
): Promise<ExecutionResult> {
  return executeCodeSandbox(capsuleId, payload, taskInput);
}

// ============= WORKFLOW 模式 =============

interface WorkflowStep {
  name: string;
  action: 'llm' | 'transform' | 'http';
  params: Record<string, unknown>;
}

interface WorkflowPayload {
  steps: WorkflowStep[];
}

/**
 * WORKFLOW 模式：顺序执行 JSON 工作流步骤
 */
async function executeWorkflowMode(
  capsuleId: string,
  payload: unknown,
  taskInput: unknown,
): Promise<ExecutionResult> {
  const steps: string[] = [`[WORKFLOW] Capsule: ${capsuleId}`];
  const start = Date.now();

  try {
    const wp = payload as WorkflowPayload;
    const context: Record<string, unknown> = { input: taskInput };

    for (let i = 0; i < wp.steps.length; i++) {
      const step = wp.steps[i];
      steps.push(`Step ${i + 1}/${wp.steps.length}: ${step.action} - ${step.name}`);

      switch (step.action) {
        case 'transform': {
          if (process.env.NODE_ENV === 'production') {
            throw new Error('WORKFLOW transform step is disabled in production (no sandbox). Set EVOMAP_ALLOW_CODE=1 to override.');
          }
          const fn = new Function('ctx', `return ${step.params.fn || step.params.code || 'ctx.input'}`)(context);
          context[step.name] = fn;
          break;
        }
        case 'llm': {
          // 简化：直接用 OpenRouter
          const llmParams = step.params as { prompt?: string; model?: string; temperature?: number };
          const response = await fetch(`${PROXY_BASE_URL}/api/proxy/chat/completions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              model: llmParams.model || 'anthropic/claude-3-haiku',
              messages: [{ role: 'user', content: (llmParams.prompt || '').replace('{{input}}', JSON.stringify(context)) }],
              temperature: llmParams.temperature ?? 0.3,
            }),
          });

          if (!response.ok) {
            throw new Error(`LLM API error ${response.status}`);
          }

          // 先获取文本，以便在 JSON 解析失败时记录
          const text = await response.text();
          let data;

          try {
            data = JSON.parse(text) as { choices?: Array<{ message?: { content?: string } }> };
          } catch (parseError) {
            console.error('[WORKFLOW] JSON parse error:', parseError);
            console.error('[WORKFLOW] Raw response:', text.substring(0, 200));
            throw new Error(`Failed to parse LLM response: ${parseError instanceof Error ? parseError.message : 'Unknown error'}`);
          }

          context[step.name] = data.choices?.[0]?.message?.content;
          break;
        }
        default:
          steps.push(`  Unknown action: ${step.action}, skipping`);
      }
    }

    steps.push(`Workflow completed, output keys: ${Object.keys(context).join(', ')}`);

    return {
      success: true,
      output: context,
      duration: Date.now() - start,
      confidence: 0.88,
      execMode: 'WORKFLOW',
      steps,
    };
  } catch (err) {
    const error = err as Error;
    steps.push(`ERROR: ${error.message}`);
    return {
      success: false,
      output: null,
      error: error.message,
      duration: Date.now() - start,
      confidence: 0,
      execMode: 'WORKFLOW',
      steps,
    };
  }
}

// ============= 主入口 =============

export async function executeCapsule(params: {
  capsuleId: string;
  geneId: string;
  execMode: ExecMode;
  payload: unknown;
  geneStrategy: unknown;
  geneSignals: string[];
  taskInput: unknown;
}): Promise<ExecutionResult> {
  const { execMode, capsuleId, payload, geneStrategy, geneSignals, taskInput } = params;

  // CODE-first: if payload has a code field, always run CODE mode regardless of execMode
  const p = payload as Record<string, unknown> | null;
  if (p?.code) {
    return executeCodeMode(capsuleId, payload, taskInput);
  }
  if (p?.prompt && execMode !== 'WORKFLOW') {
    return executePromptMode(capsuleId, payload, geneStrategy, taskInput, geneSignals);
  }

  switch (execMode) {
    case 'PROMPT':
      return executePromptMode(capsuleId, payload, geneStrategy, taskInput, geneSignals);
    case 'CODE':
      return executeCodeMode(capsuleId, payload, taskInput);
    case 'WORKFLOW':
      return executeWorkflowMode(capsuleId, payload, taskInput);
    default:
      return {
        success: false,
        output: null,
        error: `Unknown execMode: ${execMode}`,
        duration: 0,
        confidence: 0,
        execMode: execMode as ExecMode,
        steps: [`Unknown execMode: ${execMode}`],
      };
  }
}

/**
 * 为 payload 计算 SHA256 checksum
 */
export function computePayloadChecksum(payload: unknown): string {
  return createHash('sha256')
    .update(JSON.stringify(payload))
    .digest('hex');
}
