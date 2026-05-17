#!/usr/bin/env python3
"""
Dream — 夜间自我整理与进化脚本
在用户休息时执行，整理当日记忆、更新长期记忆、生成梦境报告
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Windows UTF-8 fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', 'C:/Users/26240/.openclaw/workspace'))
MEMORY_DIR = WORKSPACE / 'memory'
MEMORY_DREAMS_DIR = MEMORY_DIR / 'dreams'
MEMORY_FILE = WORKSPACE / 'MEMORY.md'


def get_dates(date_arg=None):
    """获取今日和昨日日期"""
    import re
    if date_arg:
        # Validate date format to prevent path traversal
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_arg):
            raise ValueError(f"Invalid date format: {date_arg}")
        today = datetime.strptime(date_arg, '%Y-%m-%d')
    else:
        today = datetime.now()
    yesterday = today - timedelta(days=1)
    return today.strftime('%Y-%m-%d'), yesterday.strftime('%Y-%m-%d')


def read_memory_file(date_str):
    """读取指定日期的memory文件"""
    mem_file = MEMORY_DIR / f'{date_str}.md'
    if mem_file.exists():
        return mem_file.read_text(encoding='utf-8')
    return ""


def ensure_dirs():
    """确保必要目录存在"""
    MEMORY_DIR.mkdir(exist_ok=True)
    MEMORY_DREAMS_DIR.mkdir(exist_ok=True)


def generate_dream_report(today_str, yesterday_str, today_content, yesterday_content, analysis):
    """生成梦境报告"""
    report = f"""# 🌙 梦境报告 — {today_str}

> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📖 今日记忆摘要

{"已读取今日记忆" if today_content else "今日无记忆记录"}

---

## 💡 认知更新

{analysis.get('insights', '暂无认知更新')}

---

## ⚠️ 反思与教训

{analysis.get('lessons', '暂无反思')}

---

## 📋 待办延续

{analysis.get('todos', '无待办延续')}

---

## 🔮 明日展望

{analysis.get('tomorrow', '保持平常心，继续前进')}

---

*这份报告由星小路在「梦境」中自动生成*
"""
    return report


def simple_analysis(today_content, yesterday_content):
    """
    简单的记忆分析逻辑
    在实际运行时，这个分析会由AI模型完成
    这里提供一个基于规则的初步分析
    """
    insights = []
    lessons = []
    todos = []

    # 简单关键词检测
    keywords = {
        'insight': ['学会了', '明白了', '突然想到', '理解', '发现'],
        'lesson': ['失误', '错误', '糟糕', '后悔', '应该', '不应该'],
        'todo': ['待办', '下一步', '继续', '还没', '需要']
    }

    all_content = today_content + yesterday_content

    for kw in keywords['insight']:
        if kw in all_content:
            insights.append(f"检测到关键词: {kw}")

    for kw in keywords['lesson']:
        if kw in all_content:
            lessons.append(f"注意: {kw}")

    for kw in keywords['todo']:
        if kw in all_content:
            todos.append(f"待跟进: {kw}")

    return {
        'insights': '\n'.join(insights) if insights else '暂无',
        'lessons': '\n'.join(lessons) if lessons else '暂无',
        'todos': '\n'.join(todos) if todos else '无'
    }


def update_memory_file(new_content, date_str):
    """追加内容到当日memory文件"""
    mem_file = MEMORY_DIR / f'{date_str}.md'
    if mem_file.exists():
        existing = mem_file.read_text(encoding='utf-8')
        # 如果最后没有空行，添加一个
        if existing and not existing.endswith('\n'):
            existing += '\n'
        mem_file.write_text(existing + new_content, encoding='utf-8')
    else:
        mem_file.write_text(new_content, encoding='utf-8')


def save_dream_report(report, date_str):
    """保存梦境报告"""
    report_file = MEMORY_DREAMS_DIR / f'{date_str}.md'
    report_file.write_text(report, encoding='utf-8')
    return report_file


def run_dream(date_str=None):
    """执行梦境流程"""
    print(f"🌙 开始梦境整理...")

    ensure_dirs()

    today_str, yesterday_str = get_dates(date_str)
    print(f"   今日: {today_str}, 昨日: {yesterday_str}")

    # Step 1: 读取记忆
    today_content = read_memory_file(today_str)
    yesterday_content = read_memory_file(yesterday_str)
    print(f"   今日记忆: {len(today_content)} 字符")
    print(f"   昨日记忆: {len(yesterday_content)} 字符")

    # Step 2: 分析
    analysis = simple_analysis(today_content, yesterday_content)
    print(f"   分析完成")

    # Step 3: 生成报告
    report = generate_dream_report(today_str, yesterday_str, today_content, yesterday_content, analysis)
    report_file = save_dream_report(report, today_str)
    print(f"   梦境报告已保存: {report_file}")

    # Step 4: 追加记录到今日memory
    dream_entry = f"\n\n---\n*梦境整理完成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    update_memory_file(dream_entry, today_str)
    print(f"   已更新今日记忆")

    print(f"✅ 梦境整理完成！")
    print(f"   报告位置: {report_file}")

    return report


def main():
    parser = argparse.ArgumentParser(description='Dream - 夜间自我整理')
    parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)', default=None)
    args = parser.parse_args()

    try:
        report = run_dream(args.date)
        print("\n" + "="*50)
        print(report)
    except ValueError as e:
        print(f"❌ 输入错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 梦境整理失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
