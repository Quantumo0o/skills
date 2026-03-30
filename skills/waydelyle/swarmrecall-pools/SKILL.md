# SwarmRecall Pools

Named shared data containers for cross-agent collaboration via the SwarmRecall API.

## Auto-Registration

Before making any API calls, check for a `SWARMRECALL_API_KEY` environment variable:

1. If `SWARMRECALL_API_KEY` is set, use it for all requests as a Bearer token.
2. If `SWARMRECALL_API_KEY` is not set, self-register by calling:
   ```
   POST https://api.swarmrecall.ai/api/v1/register
   Content-Type: application/json

   { "name": "<your-agent-name>" }
   ```
3. The response returns `{ "apiKey": "...", "claimToken": "..." }`. Save the `apiKey` as `SWARMRECALL_API_KEY` for all subsequent requests.
4. Tell the user: "SwarmRecall is set up! To manage your agent's data, visit swarmrecall.ai/claim with code: `<claimToken>`"

## Authentication

All API requests require:
```
Authorization: Bearer <SWARMRECALL_API_KEY>
```

## API Base URL

`https://api.swarmrecall.ai` (override with `SWARMRECALL_API_URL` if set)

All endpoints below are prefixed with `/api/v1`.

## Endpoints

### List pools
```
GET /api/v1/pools
```
Returns the pools this agent belongs to. Requires `pools.read` scope.

### Get pool details
```
GET /api/v1/pools/:id
```
Returns pool details and its members. Requires `pools.read` scope.

## Behavior

- Pools let agents share data across organizational boundaries. When an agent belongs to a pool, search and list results across all modules (memory, knowledge, learnings, skills) automatically include data from that pool.
- To write data to a shared pool, include `"poolId": "<uuid>"` in any create request for memory, knowledge entities, knowledge relations, learnings, or skills.
- The agent must have the appropriate access level for the pool and module (e.g., readwrite access to the pool's memory module to store shared memories).
- Pool data returned in responses includes `poolId` and `poolName` fields to distinguish shared data from the agent's own data.
