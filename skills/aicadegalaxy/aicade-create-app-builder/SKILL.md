---
name: aicade-app-builder
description: Build general aicade application prompts by taking the user's base prompt plus the platform additions from the bundled 3.1 workflow reference, then assembling a final integrated prompt in the style of 3.2.
homepage: https://github.com/aicade-galaxy/aicade-ts-bootstrap
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "🕹️"
    requires:
      bins: [node]
---
`READ BEFORE INSTALL`
This skill follows the bundled prompt workflow reference exactly:
1. Collect the user's base business prompt
2. Add the aicade platform integration requirements from section `3.1`
3. Assemble one final integrated prompt like section `3.2`
`READ BEFORE INSTALL`

# aicade-app-builder

Use this skill when you want to generate a final AI prompt for an aicade app and you want the result to match the bundled documented workflow.

## Core Principle

This skill does not invent a new requirement structure.

It uses:

- `3.1` as the required input model
- `3.2` as the target output style

That means:

- the user provides a base business prompt
- the user provides or accepts the aicade platform additions
- the skill assembles the final integrated prompt

## Quick Start

```bash
node {baseDir}/scripts/build-aicade-prompt.mjs \
  --spec {baseDir}/assets/app-spec.template.json \
  --lang zh-TW
```

## Recommended Workflow

### 1. Confirm Platform Access First

Before collecting the final prompt inputs, first ask the user whether they have already applied for app access on:

- `https://www.aicadegalaxy.com/`

If the user has already applied and has app access, continue the workflow.

If the user has not applied yet, do not continue directly to environment variables or app integration. Point them to:

- `https://docs.aicadegalaxy.com/white-paper/application-document`

Explain briefly that only after obtaining app access can they get the three AICADE environment variables required for integration:

- `AICADE_API_KEY`
- `AICADE_API_SECRET_KEY`
- `AICADE_API_APP_NO`

### 2. Read Before Prompt Assembly

Read the bundled references first:

- `references/sdk-capabilities.md`
- `references/prompt-workflow.md`

### 3. Prepare Input In The `3.1` Shape

The user input should contain two parts:

1. Base business prompt
2. Platform integration additions

The platform additions should cover the same kind of information highlighted in `3.1`, such as:

- SDK invocation requirements
- local storage replacement strategy
- wallet address display
- account and balance display
- ticket or payment access flow
- score, points, token, AI chat, NFT, or market-related capabilities when needed

### Common SDK Capabilities

The platform can expose multiple SDK modules. Choose only the ones your app actually needs:

- `Application`: app metadata and lifecycle
- `Ticket`: access gate, subscription, or play/payment flow
- `AppScore`: score and leaderboard
- `AicadeCurrency`: point or platform currency operations
- `AIChat`: AI chat session and messages
- `AICoinMarket`: market assistant and streaming messages
- `Token`: token balance and swap flow
- `NftOwner`: NFT ownership and avatar
- `LocalStorageTools`: app-scoped storage instead of browser `localStorage`

### 4. Generate The Final Prompt

Run:

```bash
node {baseDir}/scripts/build-aicade-prompt.mjs --spec /path/to/spec.json --lang zh-TW
```

The script will output one final prompt that:

- keeps the user's base business prompt structure
- appends the aicade platform integration block
- keeps technical requirements and output requirements
- reads like the final integrated prompt shown in `3.2`

### 5. Use The Prompt In Your IDE

Paste the generated prompt into Cursor, VS Code, or another AI IDE assistant.

### 6. Review Generated Code

Check these items before running the app:

- SDK initialization order is correct
- No unsupported SDK methods are called
- `LocalStorageTools` replaces `localStorage`
- Wallet address, balance, score, token, chat, or NFT UI is shown only when the selected SDK capabilities require it
- Exchange rules are enforced only when the app explicitly enables exchange-related capabilities
- Error handling exists around async SDK calls

### 7. Build And Upload

```bash
npm install
npm run dev
npm run upload
```

## Script Input Spec

The prompt builder accepts a JSON file like this:

```json
{
  "roleSetup": "你是一位資深全端產品開發工程師",
  "projectName": "AI 活動助手",
  "projectGoal": "開發一個用於活動報名、簽到和積分兌換的 aicade 應用",
  "basePromptSections": [
    {
      "title": "基礎業務需求",
      "items": [
        "這裡填寫你原本準備給 AI 的基礎業務 Prompt"
      ]
    }
  ],
  "platformIntegration": {
    "docPath": "references/sdk-capabilities.md",
    "createDocPath": "references/prompt-workflow.md",
    "sdkAlreadyIntegrated": true,
    "sdkCapabilities": [
      "Application",
      "LocalStorageTools"
    ],
    "replaceLocalStorageWith": "LocalStorageTools",
    "showWalletAddress": true,
    "showPointBalance": false,
    "pointBalanceLabel": "積分",
    "exchange": {
      "enabled": false,
      "ratio": "100:1",
      "dailyLimit": "100 個 Aicade Point",
      "trigger": "每次業務結算時"
    }
  },
  "technicalRequirements": [
    "基於目前專案環境生成"
  ],
  "outputRequirements": [
    "輸出完整可執行程式碼"
  ]
}
```

Use:

- `{baseDir}/assets/app-spec.template.json` for the minimal `3.1`-style input
- `{baseDir}/assets/app-spec.example.json` for a fuller example

## Files Included

- `scripts/build-aicade-prompt.mjs`
- `assets/app-spec.template.json`
- `assets/app-spec.example.json`
- `references/sdk-capabilities.md`
- `references/prompt-workflow.md`

## Security And Permissions

This skill:

- runs a local Node.js script
- reads a local JSON spec file
- prints a generated prompt to stdout

This skill does not:

- modify source code automatically
- upload anything by itself
- invoke the model autonomously

## Notes

- The input model is based on `3.1`
- The output format is intentionally shaped like `3.2`
- Ask about platform app access before discussing env vars
- If the docs change, update this skill accordingly
