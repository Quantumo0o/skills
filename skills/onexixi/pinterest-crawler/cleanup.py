#!/usr/bin/env python3
"""
Pinterest 图片清理/导出工具

功能:
  - 按点赞数筛选图片 (只保留高赞)
  - 按分辨率过滤 (去掉太小的图)
  - 导出图片到指定目录 (扁平化 / 按关键词分文件夹)
  - 清理数据库中的无效记录

用法:
  python cleanup.py --source ./pinterest_images --export ./curated --min-likes 10
  python cleanup.py --source ./pinterest_images --export ./curated --min-size 500 --group-by-keyword
  python cleanup.py --db ./pinterest_history.db --cleanup-db
"""

import os
import sys
import json
import shutil
import sqlite3
import hashlib
import argparse
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("cleanup")


def get_image_dimensions(filepath: str) -> tuple:
    """获取图片尺寸 (width, height)，不依赖 PIL 的简单方法"""
    try:
        # 尝试用 PIL
        from PIL import Image
        with Image.open(filepath) as img:
            return img.size
    except ImportError:
        # 没有 PIL 则返回 (0, 0)，跳过分辨率过滤
        return (0, 0)
    except Exception:
        return (0, 0)


def filter_and_export(
    source_dir: str,
    export_dir: str,
    min_likes: int = 0,
    min_size: int = 0,
    group_by_keyword: bool = False,
    db_path: str = "",
):
    """筛选并导出图片"""
    if not os.path.isdir(source_dir):
        logger.error(f"源目录不存在: {source_dir}")
        sys.exit(1)

    os.makedirs(export_dir, exist_ok=True)

    exported = 0
    skipped_likes = 0
    skipped_size = 0
    skipped_other = 0

    # 遍历所有图片
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

    for root, dirs, files in os.walk(source_dir):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in image_exts:
                continue

            filepath = os.path.join(root, fname)

            # 解析文件名中的 likes: {pin_id}_{likes}likes_{depth}.{ext}
            likes = 0
            try:
                parts = fname.rsplit(".", 1)[0].split("_")
                for p in parts:
                    if p.endswith("likes"):
                        likes = int(p.replace("likes", ""))
                        break
            except (ValueError, IndexError):
                pass

            # 点赞过滤
            if min_likes > 0 and likes < min_likes:
                skipped_likes += 1
                continue

            # 分辨率过滤
            if min_size > 0:
                w, h = get_image_dimensions(filepath)
                if w > 0 and h > 0 and min(w, h) < min_size:
                    skipped_size += 1
                    continue

            # 确定目标路径
            if group_by_keyword:
                # 从父目录名提取关键词
                parent = os.path.basename(root)
                keyword_part = "_".join(parent.split("_")[:-2])  # 去掉时间戳
                dest_dir = os.path.join(export_dir, keyword_part or "misc")
                os.makedirs(dest_dir, exist_ok=True)
                dest = os.path.join(dest_dir, fname)
            else:
                dest = os.path.join(export_dir, fname)

            # 避免覆盖
            if os.path.exists(dest):
                base, ext_ = os.path.splitext(dest)
                dest = f"{base}_{hashlib.md5(filepath.encode()).hexdigest()[:6]}{ext_}"

            shutil.copy2(filepath, dest)
            exported += 1

    logger.info("=" * 60)
    logger.info("📦 导出完成")
    logger.info("=" * 60)
    logger.info(f"  导出图片    : {exported}")
    logger.info(f"  跳过(低赞)  : {skipped_likes}")
    logger.info(f"  跳过(太小)  : {skipped_size}")
    logger.info(f"  跳过(其他)  : {skipped_other}")
    logger.info(f"  导出目录    : {export_dir}")
    logger.info("=" * 60)

    result = {
        "exported": exported,
        "skipped_likes": skipped_likes,
        "skipped_size": skipped_size,
        "export_dir": export_dir,
    }
    print(f"\n__CLEANUP_JSON__:{json.dumps(result, ensure_ascii=False)}")
    return result


def cleanup_db(db_path: str):
    """清理数据库中文件已不存在的记录"""
    if not os.path.exists(db_path):
        logger.error(f"数据库不存在: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM downloaded")
    before = cur.fetchone()[0]

    # 找到所有带文件路径的记录，检查文件是否存在
    # 注意：数据库只存了 filename 没有完整路径，所以只能清理明显无效的
    cur.execute("DELETE FROM downloaded WHERE url IS NULL OR url = ''")
    cur.execute("DELETE FROM downloaded WHERE normalized_url IS NULL OR normalized_url = ''")

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM downloaded")
    after = cur.fetchone()[0]

    removed = before - after
    logger.info(f"数据库清理: 移除 {removed} 条无效记录 (之前 {before}, 现在 {after})")

    # VACUUM 压缩
    cur.execute("VACUUM")
    conn.commit()
    conn.close()

    logger.info("数据库已压缩")


def main():
    parser = argparse.ArgumentParser(description="Pinterest 图片清理/导出工具")

    parser.add_argument("--source", type=str, default="", help="图片源目录")
    parser.add_argument("--export", type=str, default="", help="导出目录")
    parser.add_argument("--min-likes", type=int, default=0, help="最低点赞数")
    parser.add_argument("--min-size", type=int, default=0, help="最小边长(像素)")
    parser.add_argument("--group-by-keyword", action="store_true", help="按关键词分文件夹")
    parser.add_argument("--db", type=str, default="", help="数据库路径")
    parser.add_argument("--cleanup-db", action="store_true", help="清理数据库无效记录")

    args = parser.parse_args()

    if args.cleanup_db and args.db:
        cleanup_db(args.db)

    if args.source and args.export:
        filter_and_export(
            source_dir=args.source,
            export_dir=args.export,
            min_likes=args.min_likes,
            min_size=args.min_size,
            group_by_keyword=args.group_by_keyword,
            db_path=args.db,
        )

    if not args.source and not args.cleanup_db:
        parser.print_help()


if __name__ == "__main__":
    main()
