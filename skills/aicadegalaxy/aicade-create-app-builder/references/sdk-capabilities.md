# aicade SDK Capabilities

Use this reference when deciding which platform modules to mention in the final prompt.

## Core Usage Order

1. Create an `AicadeSDK` instance
2. Call `init(...)`
3. Call `waitForReady()`
4. Retrieve modules with `getModule(...)`
5. Reuse module instances
6. Subscribe to events when state sync is needed

## Common Modules

- `Application`: app metadata and lifecycle
- `Ticket`: access control, subscription, play/payment gate
- `AppScore`: score and leaderboard
- `AicadeCurrency`: point or platform currency operations
- `AIChat`: AI chat sessions and messages
- `AICoinMarket`: market assistant and streaming messages
- `Token`: token balance and swap
- `NftOwner`: NFT ownership and avatar
- `LocalStorageTools`: app-scoped storage instead of browser `localStorage`

## Prompt Guidance

Only include the modules the app actually needs.

Typical prompt reminders:

- use `LocalStorageTools` instead of `localStorage`
- initialize with `init(...)` then `waitForReady()`
- display wallet or balance only if the app needs that capability
- include score, currency, token, AI chat, NFT, or payment constraints only when those modules are in scope
