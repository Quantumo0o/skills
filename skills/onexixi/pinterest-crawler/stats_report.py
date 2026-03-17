#!/usr/bin/env python3
"""
Pinterest 爬取统计报告工具

用法:
  python stats_report.py --db ./pinterest_history.db
  python stats_report.py --db ./pinterest_history.db --keyword "cute cats"
  python stats_report.py --db ./pinterest_history.db --output report.json
"""

import os
import sys
import json
import sqlite3
import argparse
from collections import Counter
from datetime import datetime


def generate_report(db_path: str, keyword: str = "", output: str = "") -> dict:
    """生成爬取统计报告"""
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 基础统计
    where = ""
    params = ()
    if keyword:
        where = "WHERE keyword = ?"
        params = (keyword,)

    cur.execute(f"SELECT COUNT(*) FROM downloaded {where}", params)
    total = cur.fetchone()[0]

    cur.execute(f"SELECT SUM(likes) FROM downloaded {where}", params)
    total_likes = cur.fetchone()[0] or 0

    cur.execute(f"SELECT AVG(likes) FROM downloaded {where}", params)
    avg_likes = round(cur.fetchone()[0] or 0, 1)

    cur.execute(f"SELECT MAX(likes) FROM downloaded {where}", params)
    max_likes = cur.fetchone()[0] or 0

    # 按关键词分组
    cur.execute(
        "SELECT keyword, COUNT(*) as cnt FROM downloaded GROUP BY keyword ORDER BY cnt DESC"
    )
    by_keyword = [{"keyword": r[0], "count": r[1]} for r in cur.fetchall()]

    # 按深度分组
    cur.execute(
        f"SELECT depth, COUNT(*) as cnt FROM downloaded {where} GROUP BY depth ORDER BY depth",
        params,
    )
    by_depth = [{"depth": r[0], "count": r[1]} for r in cur.fetchall()]

    # 按日期分组
    cur.execute(
        f"SELECT DATE(created_at) as d, COUNT(*) as cnt FROM downloaded {where} "
        "GROUP BY d ORDER BY d DESC LIMIT 30",
        params,
    )
    by_date = [{"date": r[0], "count": r[1]} for r in cur.fetchall()]

    # Top 10 高赞图片
    cur.execute(
        f"SELECT pin_id, filename, likes, keyword, depth FROM downloaded {where} "
        "ORDER BY likes DESC LIMIT 10",
        params,
    )
    top_liked = [
        {
            "pin_id": r[0],
            "filename": r[1],
            "likes": r[2],
            "keyword": r[3],
            "depth": r[4],
        }
        for r in cur.fetchall()
    ]

    # 文件类型分布
    cur.execute(f"SELECT filename FROM downloaded {where}", params)
    ext_counter = Counter()
    for (fname,) in cur.fetchall():
        if fname:
            ext = os.path.splitext(fname)[1].lower()
            ext_counter[ext] += 1
    by_ext = [{"ext": k, "count": v} for k, v in ext_counter.most_common()]

    conn.close()

    report = {
        "generated_at": datetime.now().isoformat(),
        "db_path": db_path,
        "filter_keyword": keyword or "(all)",
        "summary": {
            "total_images": total,
            "total_likes": total_likes,
            "avg_likes": avg_likes,
            "max_likes": max_likes,
            "unique_keywords": len(by_keyword),
        },
        "by_keyword": by_keyword,
        "by_depth": by_depth,
        "by_date": by_date,
        "by_extension": by_ext,
        "top_liked": top_liked,
    }

    # 打印摘要
    print("=" * 60)
    print("📊 Pinterest 爬取统计报告")
    print("=" * 60)
    print(f"  数据库      : {db_path}")
    print(f"  筛选关键词  : {keyword or '全部'}")
    print(f"  总图片数    : {total}")
    print(f"  总点赞数    : {total_likes}")
    print(f"  平均点赞    : {avg_likes}")
    print(f"  最高点赞    : {max_likes}")
    print(f"  关键词数    : {len(by_keyword)}")
    print()

    if by_keyword:
        print("📁 按关键词:")
        for item in by_keyword[:10]:
            print(f"    {item['keyword']:<30} {item['count']} 张")
        print()

    if by_depth:
        print("🔄 按深度:")
        for item in by_depth:
            label = "搜索页" if item["depth"] == 0 else f"深度 {item['depth']}"
            print(f"    {label:<30} {item['count']} 张")
        print()

    if top_liked:
        print("🔥 Top 10 高赞:")
        for i, item in enumerate(top_liked, 1):
            print(f"    {i:>2}. {item['pin_id']} - {item['likes']} likes ({item['keyword']})")
        print()

    print("=" * 60)

    # 输出 JSON
    if output:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 报告已保存: {output}")

    # 也输出到 stdout 便于解析
    print(f"\n__REPORT_JSON__:{json.dumps(report, ensure_ascii=False)}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Pinterest 爬取统计报告")
    parser.add_argument("--db", required=True, help="数据库文件路径")
    parser.add_argument("--keyword", default="", help="筛选关键词")
    parser.add_argument("--output", "-o", default="", help="输出 JSON 报告路径")
    args = parser.parse_args()

    generate_report(args.db, args.keyword, args.output)


if __name__ == "__main__":
    main()
