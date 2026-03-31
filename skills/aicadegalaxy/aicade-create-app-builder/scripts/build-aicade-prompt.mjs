#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const DEFAULT_LANG = "zh-TW";
const SUPPORTED_LANGS = new Set(["zh-TW", "en"]);

function printUsage(exitCode = 0) {
  console.log(`Usage:
  node build-aicade-prompt.mjs --spec <spec.json> [--lang zh-TW|en]

Options:
  --spec   Path to a JSON spec file
  --lang   Output language, default: ${DEFAULT_LANG}
  -h, --help
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = { lang: DEFAULT_LANG };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];

    if (current === "-h" || current === "--help") {
      printUsage(0);
    }

    if (current === "--spec") {
      args.spec = argv[index + 1];
      index += 1;
      continue;
    }

    if (current === "--lang") {
      args.lang = argv[index + 1];
      index += 1;
    }
  }

  if (!args.spec) {
    console.error("Missing required argument: --spec");
    printUsage(1);
  }

  if (!SUPPORTED_LANGS.has(args.lang)) {
    console.error(`Unsupported language: ${args.lang}`);
    printUsage(1);
  }

  return args;
}

function readJson(filePath) {
  const absolutePath = path.resolve(process.cwd(), filePath);
  const raw = fs.readFileSync(absolutePath, "utf8");
  return JSON.parse(raw);
}

function arrayify(value) {
  if (Array.isArray(value)) {
    return value
      .filter(Boolean)
      .map((item) => String(item).trim())
      .filter(Boolean);
  }

  if (typeof value === "string" && value.trim()) {
    return [value.trim()];
  }

  return [];
}

function normalizeSection(section) {
  if (!section || typeof section !== "object" || Array.isArray(section)) {
    return null;
  }

  const title = typeof section.title === "string" ? section.title.trim() : "";
  const items = arrayify(section.items);

  if (!title && items.length === 0) {
    return null;
  }

  return { title, items };
}

function sectionList(value) {
  if (!Array.isArray(value)) {
    return [];
  }

  return value.map(normalizeSection).filter(Boolean);
}

function toNumberedList(items, fallback) {
  if (!items.length) {
    return `1. ${fallback}`;
  }

  return items.map((item, index) => `${index + 1}. ${item}`).join("\n");
}

function renderBaseSections(sections, lang) {
  if (!sections.length) {
    return lang === "en"
      ? "Add the full base business prompt here."
      : "請補充完整的基礎業務 Prompt。";
  }

  return sections
    .map((section) => {
      if (!section.title) {
        return section.items.join("\n");
      }
      return `${section.title}：\n${section.items.join("\n")}`;
    })
    .join("\n\n");
}

function getPlatform(spec) {
  const value = spec.platformIntegration && typeof spec.platformIntegration === "object"
    ? spec.platformIntegration
    : {};
  const exchange = value.exchange && typeof value.exchange === "object" ? value.exchange : {};

  return {
    docPath:
      typeof value.docPath === "string" && value.docPath.trim()
        ? value.docPath.trim()
        : "references/sdk-capabilities.md",
    createDocPath:
      typeof value.createDocPath === "string" && value.createDocPath.trim()
        ? value.createDocPath.trim()
        : "references/prompt-workflow.md",
    sdkAlreadyIntegrated: value.sdkAlreadyIntegrated !== false,
    sdkCapabilities: arrayify(value.sdkCapabilities),
    replaceLocalStorageWith:
      typeof value.replaceLocalStorageWith === "string" && value.replaceLocalStorageWith.trim()
        ? value.replaceLocalStorageWith.trim()
        : "LocalStorageTools",
    showWalletAddress: value.showWalletAddress !== false,
    showPointBalance: value.showPointBalance !== false,
    pointBalanceLabel:
      typeof value.pointBalanceLabel === "string" && value.pointBalanceLabel.trim()
        ? value.pointBalanceLabel.trim()
        : "積分",
    exchangeEnabled: exchange.enabled === true,
    exchangeRatio:
      typeof exchange.ratio === "string" && exchange.ratio.trim()
        ? exchange.ratio.trim()
        : "100:1",
    dailyExchangeLimit:
      typeof exchange.dailyLimit === "string" && exchange.dailyLimit.trim()
        ? exchange.dailyLimit.trim()
        : "100 Aicade Point",
    exchangeTrigger:
      typeof exchange.trigger === "string" && exchange.trigger.trim()
        ? exchange.trigger.trim()
        : "",
    extraRequirements: arrayify(value.extraRequirements),
  };
}

function buildIntegrationRequirements(spec, lang) {
  const platform = getPlatform(spec);
  const capabilityLineZhTW = platform.sdkCapabilities.length
    ? `本應用計畫對接這些 SDK 能力：${platform.sdkCapabilities.join("、")}。`
    : "";
  const capabilityLineEn = platform.sdkCapabilities.length
    ? `This app is expected to integrate these SDK capabilities: ${platform.sdkCapabilities.join(", ")}.`
    : "";

  if (lang === "en") {
    return [
      ...(platform.sdkAlreadyIntegrated
        ? ["The `aicade-ts-sdk` library is already integrated in `package.json` and can be used directly."]
        : []),
      ...(capabilityLineEn ? [capabilityLineEn] : []),
      platform.createDocPath
        ? `Before development starts, read \`${platform.docPath}\` and \`${platform.createDocPath}\`.`
        : `Before development starts, read \`${platform.docPath}\`.`,
      "Integrate the SDK in the correct order with `init(...)` followed by `waitForReady()`.",
      `If local storage is needed (for example, if \`localStorage\` would normally be used), replace it with aicade-ts-sdk's \`${platform.replaceLocalStorageWith}\`.`,
      ...(platform.showWalletAddress ? ["Display the current user's wallet address at the top of the page."] : []),
      ...(platform.showPointBalance
        ? [`Display the account Aicade Point balance at the top and label it as "${platform.pointBalanceLabel}".`]
        : []),
      ...(platform.exchangeEnabled
        ? [
            platform.exchangeTrigger
              ? `At ${platform.exchangeTrigger}, convert business points or reward value into Aicade Point at a ${platform.exchangeRatio} ratio.`
              : `At the app's settlement step, convert business points or reward value into Aicade Point at a ${platform.exchangeRatio} ratio.`,
            `Limit each user to at most ${platform.dailyExchangeLimit} exchanged per day.`,
          ]
        : []),
      ...platform.extraRequirements,
    ];
  }

  return [
    ...(platform.sdkAlreadyIntegrated
      ? ["`aicade-ts-sdk` 的 lib 已整合在 `package.json` 中，可以直接使用。"]
      : []),
    ...(capabilityLineZhTW ? [capabilityLineZhTW] : []),
    platform.createDocPath
      ? `在開始開發時，需要先閱讀 \`${platform.docPath}\` 和 \`${platform.createDocPath}\`。`
      : `在開始開發時，需要先閱讀 \`${platform.docPath}\`。`,
    "開發時按 `init(...)` 和 `waitForReady()` 的順序接入 SDK。",
    `如果有本機儲存需求（例如需要使用 \`localStorage\`），則替換成 aicade-ts-sdk 的 \`${platform.replaceLocalStorageWith}\`。`,
    ...(platform.showWalletAddress ? ["頁面頂部需要顯示目前使用者錢包地址。"] : []),
    ...(platform.showPointBalance
      ? [`頁面頂部需要顯示帳戶 Aicade Point 餘額，顯示標籤為「${platform.pointBalanceLabel}」。`]
      : []),
    ...(platform.exchangeEnabled
      ? [
          platform.exchangeTrigger
            ? `${platform.exchangeTrigger}，按 ${platform.exchangeRatio} 的比例把業務積分或獎勵值兌換成 Aicade Point。`
            : `在業務結算時，按 ${platform.exchangeRatio} 的比例把業務積分或獎勵值兌換成 Aicade Point。`,
          `限制每位使用者每天最多兌換 ${platform.dailyExchangeLimit}。`,
        ]
      : []),
    ...platform.extraRequirements,
  ];
}

function normalizeSpec(spec, lang) {
  return {
    roleSetup: typeof spec.roleSetup === "string" && spec.roleSetup.trim() ? spec.roleSetup.trim() : "",
    projectName: typeof spec.projectName === "string" && spec.projectName.trim() ? spec.projectName.trim() : "",
    projectGoal: typeof spec.projectGoal === "string" && spec.projectGoal.trim() ? spec.projectGoal.trim() : "",
    basePromptSections: sectionList(spec.basePromptSections),
    technicalRequirements: arrayify(spec.technicalRequirements),
    outputRequirements: arrayify(spec.outputRequirements),
    integrationRequirements: buildIntegrationRequirements(spec, lang),
  };
}

function buildZhTW(spec) {
  const lines = [];
  lines.push(`角色設定：${spec.roleSetup || "你是一位精通 nodejs、npm、vite、typescript 和 web3 的資深應用開發工程師，擅長撰寫結構清晰、註解詳細、效能優化良好的網頁應用程式碼。"}`);

  if (spec.projectName) {
    lines.push(`\n專案名稱：${spec.projectName}`);
  }

  lines.push(`\n專案目標：${spec.projectGoal || "請基於目前專案環境開發一個完整的 aicade 應用。"}`);
  lines.push(`\n${renderBaseSections(spec.basePromptSections, "zh-TW")}`);
  lines.push(`\n\nts sdk 整合要求：\n${toNumberedList(spec.integrationRequirements, "正確接入 aicade-ts-sdk，並遵守平台限制。")}`);
  lines.push(`\n\n技術要求：\n${toNumberedList(spec.technicalRequirements, "基於目前專案環境進行擴充開發。")}`);

  if (spec.outputRequirements.length) {
    lines.push(`\n\n輸出要求：\n${toNumberedList(spec.outputRequirements, "輸出完整可執行程式碼。")}`);
  }

  return lines.join("");
}

function buildEn(spec) {
  const lines = [];
  lines.push(`Role setup: ${spec.roleSetup || "You are a senior application engineer proficient in nodejs, npm, vite, typescript, and web3. You specialize in producing clear, maintainable, well-commented, and performant web app code."}`);

  if (spec.projectName) {
    lines.push(`\nProject name: ${spec.projectName}`);
  }

  lines.push(`\nProject goal: ${spec.projectGoal || "Build a complete aicade application in the current project environment."}`);
  lines.push(`\n${renderBaseSections(spec.basePromptSections, "en")}`);
  lines.push(`\n\naicade TS SDK integration requirements:\n${toNumberedList(spec.integrationRequirements, "Integrate aicade-ts-sdk correctly and preserve platform constraints.")}`);
  lines.push(`\n\nTechnical requirements:\n${toNumberedList(spec.technicalRequirements, "Extend the current project environment instead of replacing it.")}`);

  if (spec.outputRequirements.length) {
    lines.push(`\n\nOutput requirements:\n${toNumberedList(spec.outputRequirements, "Provide complete runnable code.")}`);
  }

  return lines.join("");
}

function buildPrompt(spec, lang) {
  if (lang === "en") {
    return buildEn(spec);
  }

  return buildZhTW(spec);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const rawSpec = readJson(args.spec);
  const spec = normalizeSpec(rawSpec, args.lang);
  const prompt = buildPrompt(spec, args.lang);
  process.stdout.write(`${prompt}\n`);
}

main();
