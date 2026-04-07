#!/usr/bin/env bash
# MCU Persona Distiller — 构建脚本
# 用法: ./build.sh <character-slug>
# 例: ./build.sh thanos

set -e

SLUG=$1
if [ -z "$SLUG" ]; then
  echo "用法: $0 <character-slug>"
  echo "例: $0 thanos"
  exit 1
fi

CONFIG_DIR="$(cd "$(dirname "$0")/.." && pwd)/config/characters"
TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)/templates"
OUTPUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/output"

CHAR_CONFIG="$CONFIG_DIR/${SLUG}.json"

if [ ! -f "$CHAR_CONFIG" ]; then
  echo "❌ 配置文件不存在: $CHAR_CONFIG"
  exit 1
fi

# 解析 JSON（使用 Python 更可靠）
python3 - <<'PYEOF'
import json
import sys
import os
import re

slug = sys.argv[1]
config_path = f"config/characters/{slug}.json"

with open(config_path, 'r', encoding='utf-8') as f:
    char = json.load(f)

slug = char['slug']
output_dir = f"output/{slug}"
os.makedirs(output_dir, exist_ok=True)

# 读取基础模板
with open('templates/base-SKILL.md', 'r', encoding='utf-8') as f:
    skill_tpl = f.read()

# 填充 SKILL.md 模板
skill_md = skill_tpl.format(
    slug=slug,
    displayName=char['displayName'],
    mcuName=char['mcuName'],
    description=char.get('description', ''),
    sourceMovies=', '.join(char.get('sourceMovies', [])),
    keyTraits=', '.join(char.get('keyTraits', [])),
    dimensions_table=build_dimensions_table(char.get('dimensions', {})),
    confidence_table=build_confidence_table(char.get('confidence', {})),
    disclaimer=get_disclaimer(char)
)

with open(f'{output_dir}/SKILL.md', 'w', encoding='utf-8') as f:
    f.write(skill_md)

# 复制配置文件
import shutil
shutil.copy(config_path, f'{output_dir}/manifest.json')

print(f"✅ 构建完成: {output_dir}/")

def build_dimensions_table(dims):
    rows = []
    mapping = {
        'personality': ('性格画像', 'personality.md'),
        'interaction': ('沟通风格', 'interaction.md'),
        'memory': ('关键记忆', 'memory.md'),
        'procedure': ('决策方法论', 'procedure.md')
    }
    for k, (label, fname) in mapping.items():
        status = '✅' if dims.get(k) else '❌'
        rows.append(f'| {status} | [{label}]({fname}) |')
    header = '| 维度 | 文件 |\n|---|---|'
    return header + '\n' + '\n'.join(rows)

def build_confidence_table(conf):
    rows = []
    labels = {
        'very-high': '极高',
        'high': '高',
        'medium': '中',
        'low': '低'
    }
    for k, v in conf.items():
        label = labels.get(v, v)
        rows.append(f'| {k} | {label} |')
    header = '| 维度 | 置信度 |\n|---|---|\n'
    return header + '\n'.join(rows)

def get_disclaimer(char):
    lines = [
        '> ⚠️ **免责声明：** 本 Skill 仅基于漫威电影宇宙（MCU）公开影视资料生成。',
        f'> {char["mcuName"]} 是虚构角色，不涉及任何现实人物隐私。',
        '> 本产出物仅供学习研究参考，不代表漫威娱乐、迪士尼或任何官方立场。'
    ]
    return '\n'.join(lines)

PYEOF

echo "📦 输出目录: output/${SLUG}/"
ls -la "output/${SLUG}/"
