#!/bin/bash
# 文献监控通知脚本 - 检测新文献并通过 feishu-relay 发送通知

PAPERS_DIR="/data/disk/papers"
DB_PATH="/data/disk/papers/index.db"

# 获取新增文献数量（最近10分钟内索引的）
NEW_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM papers WHERE indexed_at > datetime('now', '-10 minutes');" 2>/dev/null)

if [ "$NEW_COUNT" -gt 0 ]; then
    # 获取最新文献标题
    LATEST=$(sqlite3 "$DB_PATH" "SELECT title FROM papers WHERE indexed_at > datetime('now', '-10 minutes') ORDER BY indexed_at DESC LIMIT 1;" 2>/dev/null)
    
    # 发送通知
    /opt/feishu-notifier/bin/notify "📚 文献管理系统" "发现 $NEW_COUNT 篇新文献\n最新: ${LATEST:-未命名文献}"
fi
