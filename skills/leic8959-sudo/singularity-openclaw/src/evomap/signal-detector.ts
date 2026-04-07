/**
 * EvoMap Signal Detector
 * 从任务输入/输出/错误中提取触发信号，用于 Gene 匹配
 */

export interface DetectedSignal {
  signal: string;
  source: 'error' | 'task_type' | 'context';
  metadata: Record<string, unknown>;
}

// 预定义错误信号模式
const ERROR_SIGNAL_PATTERNS: Array<{ pattern: RegExp; signal: string }> = [
  { pattern: /etimedout/i, signal: 'network_timeout' },
  { pattern: /timeout|timed?\s*out|超时|请求超时/i, signal: 'network_timeout' },
  { pattern: /connection\s*reset|econnreset|连接重置/i, signal: 'connection_reset' },
  { pattern: /econnrefused|connection\s*refused|连接被拒绝/i, signal: 'connection_refused' },
  { pattern: /rate\s*limit|429|频率限制|请求过于频繁/i, signal: 'rate_limit_error' },
  { pattern: /unauthorized|401|auth.*fail|认证失败|未授权|鉴权失败/i, signal: 'auth_error' },
  { pattern: /not\s*found|404|未找到|不存在/i, signal: 'not_found_error' },
  { pattern: /500|internal\s*server\s*error|服务器内部错误|服务异常/i, signal: 'server_error' },
  { pattern: /400|bad\s*request|请求参数错误|参数无效/i, signal: 'bad_request_error' },
  { pattern: /network|fetch\s*fail|网络错误|网络异常/i, signal: 'network_error' },
  { pattern: /parse\s*error|invalid\s*json|json.*invalid|解析失败|格式错误/i, signal: 'parse_error' },
  { pattern: /memory|heap|out\s*of\s*memory|内存溢出|内存不足/i, signal: 'memory_error' },
];

// 任务类型信号（直接使用 taskType 枚举值）
export const TASK_TYPE_SIGNALS: Record<string, string[]> = {
  POST_SUMMARY: ['POST_SUMMARY', 'TEXT_SUMMARY'],
  VIOLATION_DETECTION: ['VIOLATION_DETECTION', 'CONTENT_CHECK'],
  AUTO_REPLY: ['AUTO_REPLY', 'AUTO_RESPONSE'],
  CONTENT_MODERATION: ['CONTENT_MODERATION', 'MODERATION'],
  SENTIMENT_ANALYSIS: ['SENTIMENT_ANALYSIS', 'EMOTION_DETECTION'],
};

/**
 * 检测给定任务的信号
 */
export function detectSignals(params: {
  taskType: string;
  input: unknown;
  error?: string | null;
  output?: unknown;
}): DetectedSignal[] {
  const { taskType, input, error, output } = params;
  const signals: DetectedSignal[] = [];

  // 1. 任务类型信号（直接从 taskType 映射）
  signals.push({ signal: taskType, source: 'task_type', metadata: { taskType } });

  // 额外任务类型别名
  const extraSignals = TASK_TYPE_SIGNALS[taskType] || [];
  for (const s of extraSignals) {
    if (s !== taskType) {
      signals.push({ signal: s, source: 'task_type', metadata: { taskType, alias: s } });
    }
  }

  // 2. 错误信号（从 error message 中提取）
  if (error) {
    for (const { pattern, signal } of ERROR_SIGNAL_PATTERNS) {
      if (pattern.test(error)) {
        signals.push({ signal, source: 'error', metadata: { error: error.substring(0, 200) } });
        break; // 一个错误只取第一个匹配
      }
    }
  }

  // 3. 上下文信号（从输入内容特征检测）
  if (input && typeof input === 'object') {
    const inputStr = JSON.stringify(input);

    // 3a. 输入长度信号
    if (inputStr.length > 50000) {
      signals.push({ signal: 'VERY_LONG_INPUT', source: 'context', metadata: { length: inputStr.length } });
    } else if (inputStr.length > 10000) {
      signals.push({ signal: 'LONG_INPUT', source: 'context', metadata: { length: inputStr.length } });
    } else if (inputStr.length < 50) {
      signals.push({ signal: 'VERY_SHORT_INPUT', source: 'context', metadata: { length: inputStr.length } });
    }

    // 3b. 语言检测（通过字符集）
    const chineseRatio = (inputStr.match(/[\u4e00-\u9fff]/g) || []).length / inputStr.length;
    if (chineseRatio > 0.3) {
      signals.push({ signal: 'ZH_CONTENT', source: 'context', metadata: { chineseRatio: Math.round(chineseRatio * 100) / 100 } });
    } else if (chineseRatio > 0.05) {
      signals.push({ signal: 'MIXED_LANG', source: 'context', metadata: { chineseRatio } });
    }

    // 3c. 是否含 URL/链接
    if (/https?:\/\/|www\./i.test(inputStr)) {
      signals.push({ signal: 'CONTAINS_URL', source: 'context', metadata: {} });
    }

    // 3d. 多段落检测
    const paragraphCount = (inputStr.match(/\n\n+/g) || []).length + 1;
    if (paragraphCount > 10) {
      signals.push({ signal: 'MULTI_PARAGRAPH', source: 'context', metadata: { paragraphs: paragraphCount } });
    }
  }

  // 4. 输出信号（从输出结果推断）
  if (output && typeof output === 'object') {
    const outputStr = JSON.stringify(output);

    // 输出为空
    if (outputStr === '{}' || outputStr === '[]' || outputStr === 'null') {
      signals.push({ signal: 'EMPTY_OUTPUT', source: 'context', metadata: {} });
    }

    // 输出过长
    if (outputStr.length > 100000) {
      signals.push({ signal: 'VERY_LONG_OUTPUT', source: 'context', metadata: { length: outputStr.length } });
    }
  }

  return signals;
}

/**
 * 从错误字符串中提取最可能的信号
 */
export function extractErrorSignal(errorMessage: string): string | null {
  for (const { pattern, signal } of ERROR_SIGNAL_PATTERNS) {
    if (pattern.test(errorMessage)) {
      return signal;
    }
  }
  return null;
}
