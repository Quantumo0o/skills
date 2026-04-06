---
name: clawhub-ops
description: ClawHub Skill 发版、账号管理、SEO 优化、数据查询的完整操作手册。当需要发布新 Skill、切换账号、查询 downloads 数据、排查发版归属问题、验证 IP 代理时使用。包含 5 个账号的 token/IP 对照、双 config 路径陷阱、已知 CLI Bug、速率限制规则。
---

# ClawHub 发版操作 SOP

## 发版前必做 5 步

```bash
# 1. 确认当前 token
cat "~/Library/Application Support/clawhub/config.json"

# 2. 同时写入两个 config 路径（缺一不可）
echo '{"registry":"https://clawhub.ai","token":"TOKEN"}' > ~/Library/Application\ Support/clawhub/config.json
echo '{"registry":"https://clawhub.ai","token":"TOKEN"}' > ~/.config/clawhub/config.json

# 3. 确认出口 IP（必须与账号绑定 IP 一致）
curl -s --proxy "PROXY_URL" https://api.ipify.org

# 4. 发版（必须加 --name 和 --version 参数）
HTTPS_PROXY=PROXY_URL npx clawhub@latest publish <path> --slug <slug> --version 1.0.0 --name "<长关键词名>"

# 5. 发完验证归属（8秒后）
sleep 8 && curl -sL -x http://127.0.0.1:7897 -o /dev/null -w "%{url_effective}" "https://clawhub.ai/skills/<slug>"
```

## 账号矩阵（token / proxy / IP）

详见 `references/accounts.md`

## 速率限制规则（死规定）

- **同一账号**相邻发版间隔 **≥15 分钟**（不能卡固定值，太像脚本）
- 不同账号可以串行（宿主机 config 文件只有一个，不能并行，否则 token 互相覆盖）
- 发版脚本 `/Users/user/.openclaw/workspace-master/铁柱-workspace/scripts/publish-with-proxy.sh` 已内置间隔检查，<15 分钟直接 exit 1

## 已知 CLI Bug

1. **`whoami` 返回缓存**：永远返回第一次登录的账号名，不可信。验证归属必须 curl URL
2. **`publish` 必须加 `--version`**：不读 frontmatter version 字段，必须显式传
3. **`--name` 参数必填**：frontmatter displayName 不生效，必须用 `--name "<全称>"`

## macOS 双 config 路径（致命陷阱）

- CLI **优先读** `~/Library/Application Support/clawhub/config.json`
- 次级读 `~/.config/clawhub/config.json`
- `CLAWHUB_TOKEN` 环境变量在 CLI v0.9.0 中被**完全忽略**
- 切换账号必须**同时更新两个路径**

## Downloads 数据查询

```bash
# 标准查询脚本（格式：downloads:N，无引号无空格）
bash /Users/user/.openclaw/workspace-master/shared/scripts/clawhub-downloads.sh \
  nemo-video nemo-edit nemo-subtitle ...

# 手动单个查询
curl -sL -x http://127.0.0.1:7897 "https://clawhub.ai/<account>/<slug>" \
  | grep -o 'downloads:[0-9]*' | head -1 | cut -d: -f2
```

⚠️ trpc `/api/trpc/skill.bySlug` 和 REST `/api/skills/<slug>` 均已失效

## SEO 策略

- slug 含关键词 = 不可逾越的排名优势（score 3.0+ vs 品牌 slug 2.0）
- displayName 每个词都计入向量，宁可长不删词
- description 嵌入多语种关键词，一个 Skill 覆盖多语言搜索
- 触发词黑名单：`free trial` / `free credits` / `100 credits`（触发 spam 检测）

## 发布审核铁律

发布前检查：
- API 域名必须是 `mega-api-prod.nemovideo.ai`
- displayName 必须是带关键词的长名（≥50字符）
- 无触发词（grep "free trial\|free credits"）
- 与已发 Skill 差异度 > 40%

详细操作见 `references/publish-checklist.md`
