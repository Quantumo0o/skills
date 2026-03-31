# Setup — CWork Skill Package

## Installation

```bash
clawhub install cms-cwork
```

## Initialization

Call `setup()` before using any Skill:

```typescript
import { setup } from 'cms-cwork/shared/setup.js';

setup({
  apiKey: 'your-key',  // From: 玄关工作台 → 系统设置 → 开放平台
});
```

## External Endpoints

All API calls go to one domain only:

- `sg-al-cwork-web.mediportal.com.cn` — CWork collaboration platform API
- No third-party services. No LLM endpoints. No data forwarded elsewhere.

## Required Config

- `apiKey` — User's CWork AppKey (required). Injected via `setup()`, stored in memory only, never written to disk or env.

## Optional Config

- `baseUrl` — Override API base URL (default: production)
- `sseTimeout` — SSE timeout in ms (default: 60000)
- `paginationDefault` — Default page size (default: 20)

## Security & Privacy

- `apiKey` is stored in a module-level variable, not in `process.env`
- The key is only sent to `sg-al-cwork-web.mediportal.com.cn` as an HTTP header
- LLM credentials are never embedded — caller injects `llmClient`
- No file writes without explicit user confirmation
