---
name: zeelin-social-autopublisher
description: ZeeLin多平台自运营 — 通义千问 +《四大平台内容生产提示词手册》生成各平台稿，CDP 顺序运营 X / 微博 / 小红书 / 微信公众号草稿。MIT-0 on ClawHub.
---

**ZeeLin多平台自运营** — 自包含包：根目录为技能根，`scripts/generate_content.py` 与同目录 **四大平台内容生产提示词手册.md** 需一并保留。

解压/安装后，在技能根目录执行：

```bash
bash scripts/run_social_ops_v5.sh "你的主题"
```

须配置 **DashScope**（`DASHSCOPE_API_KEY` 等）；可将 `~/.openclaw/zeelin-qwen.env` 置于本机并由 `_thuqx_cdp_common.sh` 自动 source（若存在）。

详见包内 **OPENCLAW.md**（若附带）或 **README.md**。
