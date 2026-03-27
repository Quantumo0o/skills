#!/bin/bash
#
# Good-Memory 安装脚本
# 将 Good-Memory 的启动指令注入到所有 Agent 的 AGENTS.md
# 用法: bash install.sh
#

set -e

SKILL_DIR="/root/.openclaw/workspace/skills/good-memory"
OPENCLAW_BASE="/root/.openclaw"
AGENTS_BASE="${OPENCLAW_BASE}/agents"

# 查找所有 AGENTS.md
echo "=== Good-Memory 安装脚本 ==="
echo ""

TEMPLATE=$(mktemp)
agent_count=0

for agent_dir in "${AGENTS_BASE}"/*/; do
    [[ -d "$agent_dir" ]] || continue
    agent_name="$(basename "$agent_dir")"

    # 为每个 agent 生成对应的模板（替换 AGENT_NAME）
    sed "s/AGENT_NAME/${agent_name}/g" << 'TEMPLATE_END' > "$TEMPLATE"
## Good-Memory 会话记忆恢复

每次 session 启动时（收到第一条消息前），执行以下命令恢复上下文：

```bash
bash /root/.openclaw/workspace/skills/good-memory/scripts/maintenance.sh detect "AGENT_NAME" "$INBOUND_CHAT_ID"
```

> 注意：如果 AGENTS.md 中已有 Good-Memory 相关指令，不会重复添加。
TEMPLATE_END

    GM_BLOCK="$(cat "$TEMPLATE")"

    # 优先找 agent/ 子目录（tuwen/xiangmu/guwen 的结构）
    agents_md="$agent_dir/agent/AGENTS.md"
    # fallback 到根目录（main 的结构）
    if [[ ! -f "$agents_md" ]]; then
        agents_md="$agent_dir/AGENTS.md"
    fi
    # fallback 到 workspace 根目录（main agent 的情况）
    if [[ ! -f "$agents_md" && -f "${OPENCLAW_BASE}/workspace/AGENTS.md" ]]; then
        agents_md="${OPENCLAW_BASE}/workspace/AGENTS.md"
    fi

    if [[ ! -f "$agents_md" ]]; then
        echo "[跳过] $agent_name: 未找到 AGENTS.md"
        continue
    fi

    # 检查是否已有 Good-Memory 指令
    if grep -q "good-memory\|Good-Memory\|maintenance.sh detect" "$agents_md" 2>/dev/null; then
        echo "[已安装] $agent_name: Good-Memory 指令已存在"
        continue
    fi

    echo "[注入] $agent_name: $agents_md"

    # 在文件最开头插入
    printf '%s\n\n' "$GM_BLOCK" | cat - "$agents_md" > "${agents_md}.new" && mv "${agents_md}.new" "$agents_md"

    agent_count=$((agent_count + 1))
done

rm -f "$TEMPLATE"

echo ""
echo "=== 安装完成 ==="
echo "已处理 $agent_count 个 Agent"
echo ""
echo "说明："
echo "- 已添加 Good-Memory 指令的 agent，session 启动时会自动执行 detect"
echo "- 如果 detect 返回 RESET_DETECTED，agent 会自动恢复上一段会话记忆"
echo "- 请确保 maintenance.sh 有执行权限: chmod +x ${SKILL_DIR}/scripts/*.sh"
