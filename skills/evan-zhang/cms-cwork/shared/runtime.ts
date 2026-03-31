/**
 * CWork Skill Package - 运行时配置存储
 *
 * 使用模块级变量存储用户提供的凭证，避免通过 process.env 传递。
 * 凭证仅存在于进程内存中，不写入环境变量，不持久化，不外泄。
 */

interface RuntimeConfig {
  apiKey: string;
  baseUrl: string;
  sseTimeout: number;
  sseMaxReports: number;
  paginationDefault: number;
  paginationMax: number;
}

let _config: RuntimeConfig | null = null;

export function setRuntimeConfig(config: RuntimeConfig): void {
  _config = config;
}

export function getRuntimeConfig(): RuntimeConfig {
  if (!_config) {
    throw new Error(
      '[cwork] 未初始化。请先调用 setup({ apiKey: "your-key" })\n' +
      '（apiKey 从玄关工作台 → 系统设置 → 开放平台获取）'
    );
  }
  return _config;
}

export function isConfigured(): boolean {
  return _config !== null;
}

export function resetConfig(): void {
  _config = null;
}
