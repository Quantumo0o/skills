#!/usr/bin/env python3
"""
Pinterest 批量爬取工具

支持一次性传入多个关键词，依次爬取。

用法:
  python batch_crawl.py --params '{
    "keywords": ["cute cats", "landscape photography", "logo design"],
    "target_count": 50,
    "headless": true
  }'

  python batch_crawl.py --keywords "cute cats" "landscape" --target-count 30 --headless
"""

import os
import sys
import json
import asyncio
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Any

# 将当前目录加入 path 以便导入主爬虫
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pinterest_crawler import CrawlConfig, PinterestAutoCrawler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("batch_crawl")


async def batch_crawl(
    keywords: List[str],
    base_config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """批量爬取多个关键词，返回每个关键词的统计结果"""

    results = []

    for i, kw in enumerate(keywords, 1):
        logger.info("=" * 60)
        logger.info(f"📦 批量任务 [{i}/{len(keywords)}]: {kw}")
        logger.info("=" * 60)

        # 合并关键词到配置
        cfg_dict = {**base_config, "keyword": kw}
        config = CrawlConfig.from_dict(cfg_dict)

        errors = config.validate()
        if errors:
            logger.error(f"配置校验失败: {errors}")
            results.append({"keyword": kw, "error": errors})
            continue

        crawler = PinterestAutoCrawler(config)
        stats = await crawler.start()
        results.append(stats)

        logger.info(f"✅ [{kw}] 完成: 下载 {stats.get('downloaded', 0)} 张\n")

    # 汇总
    total_dl = sum(r.get("downloaded", 0) for r in results if "error" not in r)
    total_skip = sum(r.get("skipped", 0) for r in results if "error" not in r)
    total_fail = sum(r.get("failed", 0) for r in results if "error" not in r)

    summary = {
        "batch_size": len(keywords),
        "total_downloaded": total_dl,
        "total_skipped": total_skip,
        "total_failed": total_fail,
        "details": results,
    }

    logger.info("=" * 60)
    logger.info("📊 批量爬取汇总")
    logger.info("=" * 60)
    logger.info(f"  关键词数    : {len(keywords)}")
    logger.info(f"  总下载      : {total_dl}")
    logger.info(f"  总跳过      : {total_skip}")
    logger.info(f"  总失败      : {total_fail}")
    logger.info("=" * 60)

    print(f"\n__BATCH_RESULT_JSON__:{json.dumps(summary, ensure_ascii=False)}")
    return results


def main():
    parser = argparse.ArgumentParser(description="Pinterest 批量爬取")

    parser.add_argument(
        "--params",
        type=str,
        default="",
        help='JSON 参数，包含 keywords 数组，如 \'{"keywords":["cats","dogs"],"target_count":50}\'',
    )
    parser.add_argument(
        "--keywords", "-k", nargs="+", default=[], help="关键词列表 (空格分隔)"
    )
    parser.add_argument("--target-count", "-n", type=int, default=50)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--click-count", type=int, default=5)
    parser.add_argument("--scroll-times", type=int, default=5)
    parser.add_argument("--download-dir", type=str, default="./pinterest_images")
    parser.add_argument("--db-file", type=str, default="./pinterest_history.db")
    parser.add_argument("--headless", action="store_true", default=False)
    parser.add_argument("--proxy", type=str, default="")

    args = parser.parse_args()

    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            sys.exit(1)
        keywords = params.pop("keywords", [])
        base_config = params
    else:
        keywords = args.keywords
        base_config = {
            "target_count": args.target_count,
            "max_depth": args.max_depth,
            "click_count": args.click_count,
            "scroll_times": args.scroll_times,
            "download_dir": args.download_dir,
            "db_file": args.db_file,
            "headless": args.headless,
            "proxy": args.proxy,
        }

    if not keywords:
        logger.error("请提供至少一个关键词 (--keywords 或 JSON 中的 keywords)")
        sys.exit(1)

    asyncio.run(batch_crawl(keywords, base_config))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("用户中断")
    except Exception as e:
        logger.error(f"致命错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
