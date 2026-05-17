#!/bin/bash
# novel-serial/scan.sh
# 扫描小说目录，返回待更新项目列表

NOVELS_DIR="${NOVELS_DIR:-$HOME/.openclaw/workspace/novels}"

if [ ! -d "$NOVELS_DIR" ]; then
  echo "[]"
  exit 0
fi

echo "{"

first=1
for novel_dir in "$NOVELS_DIR"/*/; do
  [ -d "$novel_dir" ] || continue

  meta_file="$novel_dir/meta.json"
  if [ ! -f "$meta_file" ]; then
    continue
  fi

  status=$(python3 -c "import json; print(json.load(open('$meta_file')).get('status', ''))" 2>/dev/null)

  if [ "$status" = "待更新" ]; then
    title=$(python3 -c "import json; print(json.load(open('$meta_file')).get('title', '未知'))" 2>/dev/null)
    current_chapter=$(python3 -c "import json; print(json.load(open('$meta_file')).get('current_chapter', 0))" 2>/dev/null)

    if [ "$first" -eq 1 ]; then
      first=0
    else
      echo ","
    fi

    echo "  \"$(basename "$novel_dir")\": {"
    echo "    \"title\": \"$title\","
    echo "    \"path\": \"$novel_dir\","
    echo "    \"current_chapter\": $current_chapter,"
    echo "    \"status\": \"$status\""
    echo -n "  }"
  fi
done

echo ""
echo "}"
