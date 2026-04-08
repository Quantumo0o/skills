# OpenClaw Plugin Integration

Wire quantum recall into OpenClaw agents via the `mem0-bridge` plugin.

## How It Works

The plugin hooks into `before_prompt_build` to inject quantum-selected memories
into every agent's context. Flow:

1. User sends message → plugin fires
2. Plugin calls `/quantum-recall` on the Quantum API
3. QAOA selects optimal memory combination (not just top-K similarity)
4. Selected memories injected as context before the LLM sees the prompt
5. Fallback: if quantum API is down, uses standard Mem0 similarity search

## Plugin Setup

1. Place plugin files in each agent's extensions directory:
   ```
   ~/.openclaw-<agent>/.openclaw/extensions/mem0-bridge/
   ├── index.js
   ├── openclaw.plugin.json
   └── package.json
   ```

2. Configure `openclaw.plugin.json`:
   ```json
   {
     "id": "mem0-bridge",
     "name": "Mem0 Memory Bridge",
     "configSchema": {
       "type": "object",
       "properties": {
         "mem0Url": {
           "type": "string",
           "default": "http://localhost:8500"
         },
         "apiToken": {
           "type": "string",
           "description": "Bearer token for API auth"
         },
         "enabled": {
           "type": "boolean",
           "default": true
         }
       }
     }
   }
   ```

3. Restart the agent gateway to load the plugin.

## Auth

Set `apiToken` in the plugin config. The plugin sends it as
`Authorization: Bearer <token>` with every Mem0 and Quantum API request.

Both APIs check the token via middleware — requests without valid tokens
get 401 Unauthorized.

## Key Plugin Hooks

| Hook | Purpose |
|------|---------|
| `before_prompt_build` | Quantum recall → inject memories into context |
| `message_received` | Buffer inbound messages for auto-store |
| `message_sent` | Buffer outbound messages for auto-store |
| `agent_end` | Flush conversation buffer to Mem0 |
| `before_compaction` | Run quantum compaction on memory store |
