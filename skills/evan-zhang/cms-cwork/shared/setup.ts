/**
 * CWork Skill Package 初始化函数
 *
 * 安全说明：apiKey 存储在模块级变量中，不写入 process.env，
 * 仅在用户主动调用 setup() 后存在于进程内存，进程结束即销毁。
 */

import { setRuntimeConfig, isConfigured } from './runtime.js';

const DEFAULT_BASE_URL = 'https://sg-al-cwork-web.mediportal.com.cn';

export interface SetupOptions {
  /** 工作协同 AppKey（必填）—— 从玄关工作台 → 系统设置 → 开放平台获取 */
  apiKey: string;
  /** 工作协同 API 地址，默认生产环境地址，无需修改 */
  baseUrl?: string;
  /** SSE 超时（毫秒），默认 60000 */
  sseTimeout?: number;
  /** SSE 最大汇报数，默认 20 */
  sseMaxReports?: number;
  /** 分页默认大小，默认 20 */
  paginationDefault?: number;
  /** 分页最大大小，默认 50 */
  paginationMax?: number;
}

/**
 * 初始化 CWork Skill 包
 *
 * ```typescript
 * import { setup } from 'cms-cwork/shared/setup.js';
 * setup({ apiKey: 'your-key-from-xgjk-admin' });
 * ```
 *
 * 只需调用一次，之后所有 Skill 即可使用。
 */
export function setup(options: SetupOptions): void {
  if (isConfigured()) {
    console.warn('[cwork] 已初始化，重复调用无效');
    return;
  }

  if (!options.apiKey?.trim()) {
    throw new Error('[cwork] apiKey 是必填参数，请从玄关工作台 → 系统设置 → 开放平台获取');
  }

  setRuntimeConfig({
    apiKey: options.apiKey.trim(),
    baseUrl: options.baseUrl ?? DEFAULT_BASE_URL,
    sseTimeout: options.sseTimeout ?? 60000,
    sseMaxReports: options.sseMaxReports ?? 20,
    paginationDefault: options.paginationDefault ?? 20,
    paginationMax: options.paginationMax ?? 50,
  });
}

/**
 * 检查是否已初始化
 */
export function isReady(): boolean {
  return isConfigured();
}
