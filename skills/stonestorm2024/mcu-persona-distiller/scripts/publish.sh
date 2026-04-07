#!/usr/bin/env bash
# MCU Persona Distiller — 发布脚本
# 用法: ./publish.sh <character-slug> [github|clawhub|both]
# 例: ./publish.sh thanos both

set -e

SLUG=$1
TARGET=${2:-both}

if [ -z "$SLUG" ]; then
  echo "用法: $0 <character-slug> [github|clawhub|both]"
  echo "例: $0 thanos both"
  exit 1
fi

OUTPUT_DIR="output/${SLUG}"

if [ ! -d "$OUTPUT_DIR" ]; then
  echo "❌ 输出目录不存在，请先运行: ./build.sh $SLUG"
  exit 1
fi

GITHUB_TOKEN=${GITHUB_TOKEN:-$(gh auth token 2>/dev/null || echo "")}
CLAWHUB_TOKEN=${CLAWHUB_TOKEN:-""}

echo "=========================================="
echo "  MCU Persona Distiller — 发布工具"
echo "=========================================="
echo "角色: $SLUG"
echo "目标: $TARGET"
echo ""

# GitHub 发布
publish_github() {
  echo "📦 准备推送到 GitHub..."

  cd "$OUTPUT_DIR"

  # 检查远程是否存在
  if gh repo view "$GITHUB_USER/$SLUG" &>/dev/null; then
    echo "仓库已存在，更新中..."
    git init 2>/dev/null || true
    git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${SLUG}.git" 2>/dev/null || \
      git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${SLUG}.git"
    git fetch origin 2>/dev/null || true
  else
    echo "创建新仓库: ${GITHUB_USER}/${SLUG}"
    curl -s -X POST "https://api.github.com/user/repos" \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      -d "{\"name\":\"${SLUG}\",\"description\":\"MCU ${SLUG} 角色蒸馏 — 基于漫威电影宇宙\",\"public\":true}" \
      | grep -q '"id"' && echo "仓库创建成功" || echo "仓库可能已存在"
    git init 2>/dev/null || true
    git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${SLUG}.git" 2>/dev/null || \
      git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${SLUG}.git"
  fi

  git config --global user.email "${GITHUB_USER}@users.noreply.github.com"
  git config --global user.name "$GITHUB_USER"
  git add -A
  git commit -m "feat: MCU ${SLUG} persona distill v1.0.0"
  git branch -M main
  git push -u origin main --force 2>&1
  echo "✅ GitHub 发布完成: https://github.com/${GITHUB_USER}/${SLUG}"
}

# ClawHub 发布
publish_clawhub() {
  echo "📦 准备推送到 ClawHub..."
  clawhub publish "$OUTPUT_DIR" \
    --slug "${SLUG}" \
    --name "${SLUG}" \
    --version "1.0.0" \
    --tags "mcu,marvel,persona,distill" \
    --changelog "Initial MCU ${SLUG} persona distill" 2>&1
  echo "✅ ClawHub 发布完成"
}

# 主流程
GITHUB_USER=${GITHUB_USER:-$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")}

if [ "$TARGET" = "github" ] || [ "$TARGET" = "both" ]; then
  publish_github
fi

if [ "$TARGET" = "clawhub" ] || [ "$TARGET" = "both" ]; then
  publish_clawhub
fi

echo ""
echo "=========================================="
echo "  🎉 发布完成！"
echo "=========================================="
[ "$TARGET" = "github" ] || [ "$TARGET" = "both" ] && echo "  GitHub:  https://github.com/${GITHUB_USER}/${SLUG}"
[ "$TARGET" = "clawhub" ] || [ "$TARGET" = "both" ] && echo "  ClawHub: https://clawhub.ai/${GITHUB_USER}/${SLUG}"
