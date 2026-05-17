#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <project-root> [output-file]" >&2
  exit 1
fi

project_root="$1"
output_file="${2:-}"

if [ ! -d "$project_root" ]; then
  echo "[ERROR] project root not found: $project_root" >&2
  exit 1
fi

project_name="$(basename "$project_root")"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

# ── 扫描函数 ──────────────────────────────────────────────
scan_pattern() {
  local label="$1"
  local pattern="$2"
  local hits
  hits="$(grep -RInE --include='*.php' --include='*.inc' "$pattern" \
    "$project_root/application" "$project_root/public" "$project_root/conf" 2>/dev/null \
    | sed -n '1,200p' || true)"
  if [ -n "$hits" ]; then
    echo "=== $label ==="
    echo "$hits"
    echo
  fi
}

{
  echo "=== meta ==="
  echo "project: $project_name"
  echo "path: $project_root"
  echo "scanned_at: $(date '+%Y-%m-%d %H:%M:%S %z')"
  echo

  # 1. 字符串拼接进 SQL（最高危）
  scan_pattern "concat into sql" \
    '"(SELECT|INSERT|UPDATE|DELETE|REPLACE)[^"]*"\s*\.\s*\$|"[^"]*WHERE[^"]*"\s*\.\s*\$|"[^"]*SET[^"]*"\s*\.\s*\$'

  # 2. 变量直接插值到 SQL 字符串
  scan_pattern "variable interpolation in sql" \
    '"(SELECT|INSERT|UPDATE|DELETE|REPLACE)[^"$]*\$[a-zA-Z_][a-zA-Z0-9_]*'

  # 3. sprintf 不安全格式化
  scan_pattern "sprintf sql injection" \
    "sprintf\s*\(\s*['\"].*%(s|d|f).*['\"].*\\\$"

  # 4. 直接把超全局变量拼入 SQL
  scan_pattern "superglobal directly in sql" \
    '(SELECT|UPDATE|DELETE|INSERT)[^;]*\$_(GET|POST|REQUEST|COOKIE)\['

  # 5. query/execute 接收拼接字符串变量
  scan_pattern "query or execute with variable" \
    '->(query|execute)\s*\(\s*\$[a-zA-Z_][a-zA-Z0-9_]*\s*[\),]'

  # 6. WHERE 子句直接插入变量（单引号包裹或裸变量）
  scan_pattern "where clause with raw variable" \
    "WHERE[^'\"]*['\"][^'\"]*\\\$[a-zA-Z_]|WHERE\s+[a-zA-Z0-9_.]+\s*=\s*\\\$[a-zA-Z_]"

  # 7. IN 子句用 implode 拼接（未参数化）
  scan_pattern "in clause with implode" \
    'IN\s*\(\s*\$[a-zA-Z_]|implode\s*\([^)]*\)\s*.*IN'

  # 8. LIKE 子句拼接
  scan_pattern "like clause concatenation" \
    "LIKE\s*['\"][^'\"]*['\"\s]*\.\s*\\\$|LIKE\s*['\"%][^'\"]*\\\$"

  # 9. ORDER BY / LIMIT 接受外部变量（列名注入）
  scan_pattern "order by or limit with variable" \
    '(ORDER\s+BY|LIMIT|OFFSET)\s+\$[a-zA-Z_]|(ORDER\s+BY|LIMIT|OFFSET)[^;]*\.\s*\$'

} > "$tmp"

# ── 统计命中 ──────────────────────────────────────────────
count_section() {
  local section="$1"
  awk -v s="$section" '
    $0=="=== "s" ===" { found=1; next }
    /^=== / && found   { exit }
    found && NF        { c++ }
    END                { print c+0 }
  ' "$tmp"
}

c_concat="$(count_section "concat into sql")"
c_interp="$(count_section "variable interpolation in sql")"
c_sprintf="$(count_section "sprintf sql injection")"
c_super="$(count_section "superglobal directly in sql")"
c_exec="$(count_section "query or execute with variable")"
c_where="$(count_section "where clause with raw variable")"
c_in="$(count_section "in clause with implode")"
c_like="$(count_section "like clause concatenation")"
c_order="$(count_section "order by or limit with variable")"

total=$(( c_concat + c_interp + c_sprintf + c_super + c_exec + c_where + c_in + c_like + c_order ))

risk="low"
if [ "$c_concat" -ge 5 ] || [ "$c_super" -ge 1 ] || [ "$c_sprintf" -ge 3 ]; then
  risk="high"
elif [ "$total" -ge 3 ] || [ "$c_concat" -ge 1 ] || [ "$c_interp" -ge 3 ]; then
  risk="medium"
fi

# ── 生成报告 ──────────────────────────────────────────────
generate_report() {
  echo "# SQL 注入风险扫描报告"
  echo
  echo "## 基本信息"
  echo "- 项目：$project_name"
  echo "- 路径：$project_root"
  echo "- 扫描时间：$(date '+%Y-%m-%d %H:%M:%S %z')"
  echo "- 风险等级：$risk"
  echo "- 总命中行数：$total"
  echo
  echo "## 命中统计"
  echo "| 类别 | 命中数 | 风险 |"
  echo "|------|--------|------|"
  echo "| SQL 字符串拼接 | $c_concat | 🔴 高 |"
  echo "| 变量插值到 SQL | $c_interp | 🔴 高 |"
  echo "| sprintf 注入 | $c_sprintf | 🟠 中 |"
  echo "| 超全局变量直接入 SQL | $c_super | 🔴 高 |"
  echo "| query/execute 接变量 | $c_exec | 🟡 待确认 |"
  echo "| WHERE 裸变量 | $c_where | 🟠 中 |"
  echo "| IN + implode | $c_in | 🟠 中 |"
  echo "| LIKE 拼接 | $c_like | 🟠 中 |"
  echo "| ORDER BY/LIMIT 接变量 | $c_order | 🟡 待确认 |"
  echo
  echo "## 修复优先级建议"
  if [ "$c_super" -ge 1 ]; then
    echo "- ⚠️  **立即处理**：发现超全局变量直接拼入 SQL，极高风险"
  fi
  if [ "$c_concat" -ge 1 ]; then
    echo "- 🔴 **高优先**：字符串拼接 SQL，需逐一确认输入来源后参数化"
  fi
  if [ "$c_sprintf" -ge 1 ]; then
    echo "- 🟠 **中优先**：sprintf 格式化 SQL，%s 不能替代参数绑定"
  fi
  echo
  echo "## 详细命中"
  echo

  print_section() {
    local section="$1"
    awk -v s="$section" '
      $0=="=== "s" ===" { found=1; next }
      /^=== / && found  { exit }
      found             { print }
    ' "$tmp"
  }

  for section in \
    "concat into sql" \
    "variable interpolation in sql" \
    "sprintf sql injection" \
    "superglobal directly in sql" \
    "query or execute with variable" \
    "where clause with raw variable" \
    "in clause with implode" \
    "like clause concatenation" \
    "order by or limit with variable"
  do
    hits="$(print_section "$section")"
    if [ -n "$hits" ]; then
      echo "### $section"
      echo '```'
      echo "$hits"
      echo '```'
      echo
    fi
  done

  echo "## 下一步"
  echo "1. 对每个命中项确认是否有用户输入到达该 SQL"
  echo "2. 用 \`php \"\$SKILL_DIR/scripts/suggest_fix.php\" <file>\` 获取修复建议"
  echo "3. 参考 \`references/fix-patterns.md\` 选择适合项目 DB 层的修复模式"
  echo "4. 修复后重新运行本脚本验证清零"
}

if [ -n "$output_file" ]; then
  mkdir -p "$(dirname "$output_file")"
  generate_report > "$output_file"
  printf '[OK] 报告已写入: %s\n' "$output_file"
  printf '[OK] 风险等级: %s | 总命中: %s\n' "$risk" "$total"
else
  generate_report
fi
