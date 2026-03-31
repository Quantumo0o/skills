/**
 * CWork Skill Package - 配置模块
 *
 * 从运行时配置读取，不依赖 process.env。
 * 用户通过 setup({ apiKey }) 注入凭证，凭证仅存在于进程内存。
 */

import { getRuntimeConfig } from '../shared/runtime.js';

// CWork API 配置（从运行时配置读取）
export const CWORK_CONFIG = {
  get appKey() { return getRuntimeConfig().apiKey; },
  get baseUrl() { return getRuntimeConfig().baseUrl; },
} as const;

// SSE 配置（从运行时配置读取）
export const SSE_CONFIG = {
  get timeout() { return getRuntimeConfig().sseTimeout; },
  get maxReports() { return getRuntimeConfig().sseMaxReports; },
} as const;

// 分页配置（从运行时配置读取）
export const PAGINATION_CONFIG = {
  get defaultPageSize() { return getRuntimeConfig().paginationDefault; },
  get maxPageSize() { return getRuntimeConfig().paginationMax; },
} as const;
