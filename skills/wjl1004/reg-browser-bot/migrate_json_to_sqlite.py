#!/usr/bin/env python3
"""
migrate_json_to_sqlite.py - JSON 数据迁移到 SQLite

Phase B 新增:
- 将现有 JSON 文件中的账号数据迁移到 SQLite
- 将现有采集数据迁移到 SQLite
- 支持回滚（保留原始 JSON 文件）

用法:
    python migrate_json_to_sqlite.py [--accounts] [--data] [--all] [--dry-run]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目路径
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from models import DatabaseManager, Account, CollectedData, Task, get_database


def migrate_accounts(db: DatabaseManager, accounts_dir: Path, dry_run: bool = False) -> dict:
    """
    迁移账号 JSON 文件到 SQLite

    Args:
        db: 数据库管理器
        accounts_dir: 账号目录
        dry_run: 是否仅模拟迁移

    Returns:
        迁移统计信息
    """
    stats = {"total": 0, "success": 0, "skipped": 0, "failed": 0}

    for f in accounts_dir.iterdir():
        if not (f.suffix == '.json'
                and not f.stem.endswith('_cookies')
                and not f.stem.endswith('_export')
                and not f.stem.endswith('_session')):
            continue

        stats["total"] += 1
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                account_data = json.load(fp)

            name = account_data.get('name', f.stem)
            if not name:
                name = f.stem

            # 转换为 Account dataclass
            account = Account(
                name=name,
                platform=account_data.get('platform', 'unknown'),
                username=account_data.get('username', ''),
                password_encrypted=account_data.get('password', ''),
                login_url=account_data.get('login_url', ''),
                cookies=account_data.get('cookies', []),
                headers=account_data.get('headers', {}),
                user_data=account_data.get('user_data', {}),
                created_at=account_data.get('created', ''),
                updated_at=account_data.get('updated_at', ''),
                last_login=account_data.get('last_used', ''),
                status=account_data.get('status', 'active')
            )

            if dry_run:
                print(f"  [DRY-RUN] 会迁移账号: {name} ({account.platform})")
            else:
                db.save_account(account)
                print(f"  ✓ 迁移账号: {name} ({account.platform})")

            stats["success"] += 1

        except json.JSONDecodeError as e:
            print(f"  ✗ JSON 解析失败 {f.name}: {e}")
            stats["failed"] += 1
        except Exception as e:
            print(f"  ✗ 迁移失败 {f.name}: {e}")
            stats["failed"] += 1

    return stats


def migrate_collected_data(db: DatabaseManager, data_dir: Path, dry_run: bool = False) -> dict:
    """
    迁移采集数据 JSON 文件到 SQLite

    Args:
        db: 数据库管理器
        data_dir: 数据目录
        dry_run: 是否仅模拟迁移

    Returns:
        迁移统计信息
    """
    stats = {"total": 0, "success": 0, "skipped": 0, "failed": 0}

    if not data_dir.exists():
        print(f"  数据目录不存在: {data_dir}")
        return stats

    for f in sorted(data_dir.iterdir()):
        if not f.suffix == '.json':
            continue

        # 跳过非采集数据文件（如配置文件）
        name = f.stem
        if name in ['config', 'settings', 'state']:
            stats["skipped"] += 1
            continue

        stats["total"] += 1
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)

            # 判断是否为采集数据文件
            if not isinstance(data, list):
                # 单条数据，包装为列表
                items = [data] if isinstance(data, dict) else []
            else:
                items = data

            # 提取平台和关键词（从文件名）
            platform = 'unknown'
            keyword = ''
            parts = name.rsplit('_', 1)
            if len(parts) == 2:
                potential_platform = parts[0]
                if potential_platform in ['taobao', 'jd', 'douyin', 'xiaohongshu', 'weibo']:
                    platform = potential_platform
                    keyword = parts[1]
                else:
                    keyword = parts[1]

            # 创建 CollectedData
            collected = CollectedData(
                id=f"migrated_{datetime.now().strftime('%Y%m%d%H%M%S')}_{stats['total']}",
                task_id=name,
                account_name='default',
                platform=platform,
                keyword=keyword,
                items=items,
                count=len(items),
                raw_data=json.dumps(data) if not isinstance(data, list) else None,
                created_at=datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                               if hasattr(f.stat(), 'st_mtime') else datetime.now().isoformat()
            )

            if dry_run:
                print(f"  [DRY-RUN] 会迁移采集数据: {name} ({len(items)} 条)")
            else:
                db.save_collected_data(collected)
                print(f"  ✓ 迁移采集数据: {name} ({len(items)} 条)")

            stats["success"] += 1

        except json.JSONDecodeError as e:
            print(f"  ✗ JSON 解析失败 {f.name}: {e}")
            stats["failed"] += 1
        except Exception as e:
            print(f"  ✗ 迁移失败 {f.name}: {e}")
            stats["failed"] += 1

    return stats


def migrate_tasks(db: DatabaseManager, scheduler_dir: Path, dry_run: bool = False) -> dict:
    """
    迁移任务调度数据到 SQLite

    Args:
        db: 数据库管理器
        scheduler_dir: 调度器配置目录
        dry_run: 是否仅模拟迁移

    Returns:
        迁移统计信息
    """
    stats = {"total": 0, "success": 0, "skipped": 0, "failed": 0}

    jobs_file = scheduler_dir / "jobs.json"
    if not jobs_file.exists():
        print(f"  任务配置文件不存在: {jobs_file}")
        stats["skipped"] = 0
        return stats

    try:
        with open(jobs_file, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)

        for job_id, task_data in tasks_data.items():
            stats["total"] += 1
            try:
                task = Task(
                    id=job_id,
                    name=task_data.get('name', job_id),
                    type=task_data.get('trigger_type', 'interval'),
                    status='completed' if task_data.get('last_run_time') else 'pending',
                    account_name='default',
                    params={},
                    result=None,
                    error=None,
                    created_at=task_data.get('next_run_time', ''),
                    started_at=None,
                    completed_at=task_data.get('last_run_time', ''),
                    retry_count=0,
                    max_retries=3
                )

                if dry_run:
                    print(f"  [DRY-RUN] 会迁移任务: {task.name}")
                else:
                    db.save_task(task)
                    print(f"  ✓ 迁移任务: {task.name}")

                stats["success"] += 1

            except Exception as e:
                print(f"  ✗ 迁移失败 {job_id}: {e}")
                stats["failed"] += 1

    except Exception as e:
        print(f"  ✗ 读取任务配置失败: {e}")
        stats["failed"] = stats.get("total", 0)

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='JSON 数据迁移到 SQLite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --all              # 迁移所有数据
  %(prog)s --accounts         # 仅迁移账号
  %(prog)s --data             # 仅迁移采集数据
  %(prog)s --tasks            # 仅迁移任务
  %(prog)s --all --dry-run    # 模拟迁移（不实际写入）
        """
    )
    parser.add_argument('--accounts', action='store_true', help='迁移账号数据')
    parser.add_argument('--data', action='store_true', help='迁移采集数据')
    parser.add_argument('--tasks', action='store_true', help='迁移任务数据')
    parser.add_argument('--all', action='store_true', help='迁移所有数据')
    parser.add_argument('--dry-run', action='store_true', help='模拟迁移（不实际写入）')

    args = parser.parse_args()

    # 默认迁移所有
    migrate_all = args.all or not (args.accounts or args.data or args.tasks)

    # 确定数据库路径
    db_path = os.path.expanduser("~/.config/reg-browser-bot/reg-browser-bot.db")
    db = DatabaseManager(db_path=db_path)

    # 确定目录
    base_dir = Path.home() / ".openclaw"
    accounts_dir = base_dir / "accounts"
    data_dir = base_dir / "data"
    scheduler_dir = base_dir / "scheduler"

    print("=" * 60)
    print("JSON → SQLite 数据迁移工具 (Phase B)")
    print("=" * 60)
    print(f"数据库: {db_path}")
    print(f"账号目录: {accounts_dir}")
    print(f"数据目录: {data_dir}")
    print(f"任务目录: {scheduler_dir}")
    print()

    if args.dry_run:
        print("⚠ DRY-RUN 模式：仅显示将要执行的操作，不实际写入\n")

    all_stats = {}

    if migrate_all or args.accounts:
        print("【迁移账号】")
        if not accounts_dir.exists():
            print(f"  账号目录不存在: {accounts_dir}")
        else:
            all_stats["accounts"] = migrate_accounts(db, accounts_dir, args.dry_run)
        print()

    if migrate_all or args.data:
        print("【迁移采集数据】")
        all_stats["data"] = migrate_collected_data(db, data_dir, args.dry_run)
        print()

    if migrate_all or args.tasks:
        print("【迁移任务数据】")
        all_stats["tasks"] = migrate_tasks(db, scheduler_dir, args.dry_run)
        print()

    # 汇总
    print("=" * 60)
    print("迁移汇总")
    print("=" * 60)

    total_success = 0
    total_failed = 0
    for key, stats in all_stats.items():
        label = {"accounts": "账号", "data": "采集数据", "tasks": "任务"}[key]
        print(f"  {label}: 成功 {stats['success']}, 失败 {stats['failed']}, "
              f"跳过 {stats.get('skipped', 0)}, 总计 {stats['total']}")
        total_success += stats['success']
        total_failed += stats['failed']

    print()
    if args.dry_run:
        print("⚠ 这是 DRY-RUN 模式，未实际写入任何数据")
        print("  移除 --dry-run 参数以执行实际迁移")
    else:
        print("✓ 迁移完成！原始 JSON 文件已保留")
        print(f"  数据库位置: {db_path}")

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
