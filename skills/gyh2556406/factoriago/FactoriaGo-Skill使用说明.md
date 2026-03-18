# FactoriaGo Skill 使用说明

> 版本：v1.0 | 适用平台：OpenClaw | 更新日期：2026-03-17

---

## 一、什么是 FactoriaGo Skill？

这个 Skill 让 OpenClaw AI 助理能够直接操作 [FactoriaGo](https://factoriago.com) 平台，帮助学术研究者完成论文修改与再投稿全流程，包括：

- 📋 分析审稿意见，生成结构化修改清单
- ✉️ 撰写逐条审稿回复信（Point-by-Point Response）
- 🤖 调用 AI 助手对话（Chat）
- 📁 管理项目、文件、修稿任务
- 🔧 LaTeX 编译验证

---

## 二、安装前提

### 1. 注册 FactoriaGo 账号

前往 👉 https://factoriago.com 注册（有免费版）

### 2. 配置 AI 模型 API Key

> ⚠️ **所有 AI 功能（审稿分析、Chat、修改建议）都需要先配置 API Key**

FactoriaGo 采用 BYOK 模式（Bring Your Own Key），需要你提供自己的 AI 服务 API Key。

**支持的 AI 提供商：**

| 提供商 | 推荐模型 | 适用场景 | 申请地址 |
|--------|---------|---------|---------|
| Anthropic | Claude Sonnet | 英文写作最佳 | https://console.anthropic.com/keys |
| OpenAI | GPT-4o | 通用 | https://platform.openai.com/api-keys |
| Google | Gemini 2.0 Flash | 速度快 | https://aistudio.google.com/app/apikey |
| Moonshot (Kimi) | kimi-k2 | 中文论文 | https://platform.moonshot.cn/console/api-keys |
| 智谱 (GLM) | GLM-4 Plus | 中文论文 | https://open.bigmodel.cn/usercenter/apikeys |
| MiniMax | MiniMax-Text | 中文论文 | https://platform.minimaxi.com/user-center/basic-information/interface-key |

**配置方式（二选一）：**

- **网页端**：登录 editor.factoriago.com → 右上角头像 → Settings → AI Model
- **通过 AI 助理**：直接告诉 OpenClaw 助理你的 Key，让它帮你配置

---

## 三、核心功能说明

### 功能 1：审稿意见分析

**触发方式：** 把审稿意见粘贴给 AI 助理，说"帮我分析这些审稿意见"

**AI 助理会做什么：**
1. 识别每一条具体问题（自动按 Reviewer 1 / Reviewer 2 分组）
2. 按重要程度分类：🔴 重要 / 🟡 次要 / 🟢 建议
3. 给出每条问题的修改建议和优先级
4. 自动调用 `POST /api/paper/:id/analyze` 将分析结果保存到项目

**示例指令：**
```
帮我分析这篇论文的审稿意见：
[粘贴审稿意见全文]
```

---

### 功能 2：撰写审稿回复信

**触发方式：** "帮我写审稿回复信" / "生成 Point-by-Point Response"

**三种语气模式：**
- **Collaborative**（默认）：感谢 + 解释 + 承认
- **Assertive**：有礼貌地坚持自己观点
- **Technical**：偏技术细节，适合方法类问题

**示例指令：**
```
帮我写审稿回复信，语气用 collaborative，
审稿人1说样本量不足，我已经把样本扩大到了200人
```

---

### 功能 3：AI Chat 对话

**触发方式：** "在 FactoriaGo 项目里问 AI..."

**能做什么：**
- 询问当前论文内容相关问题
- 让 AI 帮助修改某个段落
- 讨论修稿策略

**示例指令：**
```
在我的 FactoriaGo 项目 [项目ID] 里，
问 AI：如何优化论文的 Related Work 部分？
```

---

### 功能 4：项目与文件管理

| 操作 | 示例指令 |
|------|---------|
| 查看所有项目 | "列出我的 FactoriaGo 项目" |
| 查看项目文件 | "查看项目 [ID] 的文件列表" |
| 创建修稿任务 | "为项目 [ID] 创建修稿任务" |
| 查看修稿任务 | "查看项目 [ID] 的任务" |
| 编译 LaTeX | "编译项目 [ID]" |

---

## 四、完整使用流程（从收到审稿意见到提交修改稿）

```
① 收到期刊审稿意见
          ↓
② 告诉 AI 助理："帮我分析这些审稿意见" + 粘贴全文
          ↓
③ AI 助理生成结构化清单（重要/次要/建议 分类）
          ↓
④ 说："帮我在 FactoriaGo 项目 [ID] 创建修稿任务"
          ↓
⑤ 在 editor.factoriago.com 编辑 LaTeX 文件
   （可以随时问 AI："帮我修改第3段的表述"）
          ↓
⑥ 说："帮我写审稿回复信"
          ↓
⑦ 编译验证（"帮我编译项目 [ID]"）
          ↓
⑧ 下载 PDF + 回复信，提交到期刊
```

---

## 五、常见问题

**Q：AI 功能提示"未配置 API Key"怎么办？**

A：需要先配置 API Key。告诉助理你想用哪个 AI 提供商（推荐 Anthropic 或 OpenAI），然后把 Key 发给助理，让它帮你配置，或者直接在 editor.factoriago.com → Settings → AI Model 里填写。

**Q：项目 ID 在哪里找？**

A：登录 editor.factoriago.com 后，在项目列表里点击项目，URL 中的一串字母数字就是项目 ID（例如：`96efa8fe-83ee-4ff7-9552-0a6ac3847efd`）。也可以直接告诉助理"列出我的项目"，它会显示所有项目 ID。

**Q：需要本地安装什么吗？**

A：不需要。FactoriaGo 是全浏览器端平台，LaTeX 编译也在云端完成。

**Q：我的 API Key 安全吗？**

A：Key 在服务器端加密存储，读取时只返回末几位掩码（如 `••••••4wAA`），不会明文返回。

**Q：免费版有什么限制？**

A：免费版有 AI 调用次数限制（AI Chat、审稿分析均消耗配额）。付费版有更多配额和更大存储空间。

---

## 六、支持渠道

- **产品官网**：https://factoriago.com
- **编辑器入口**：https://editor.factoriago.com
- **问题反馈**：通过 FactoriaGo 官网联系 Factoria.AI 团队
