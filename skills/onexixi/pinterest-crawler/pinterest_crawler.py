#!/usr/bin/env python3
"""
Pinterest 全自动递归爬虫 (Playwright版)

功能:
  - 全自动下载，无需手动确认
  - 自动滚动翻页
  - 点击图片进入详情页，爬取相似推荐
  - 递归爬取直到达到目标数量
  - 随时可终止 (按 Ctrl+C)
  - 自动去重 (URL + 内容哈希 + Pin ID 三重去重)
  - SQLite 去重数据库持久化

用法 (由 SKILL.md 调用，通过 JSON 参数传入):
  python pinterest_crawler.py --params '{"keyword":"cute cats","target_count":100}'

也支持命令行快捷参数:
  python pinterest_crawler.py --keyword "cute cats" --target-count 100 --headless
"""

import os
import sys
import json
import time
import random
import asyncio
import hashlib
import sqlite3
import signal
import argparse
import logging
from datetime import datetime
from urllib.parse import quote, urlparse
from dataclasses import dataclass, field, asdict
from typing import List, Set, Optional, Dict, Any
from collections import deque
from pathlib import Path

# ============== 日志配置 ==============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pinterest_crawler")

# ============== 全局控制 ==============
STOP_FLAG = False


def _signal_handler(sig, frame):
    global STOP_FLAG
    logger.warning("收到停止信号，正在安全停止...")
    STOP_FLAG = True


signal.signal(signal.SIGINT, _signal_handler)


# ============== 配置 ==============
@dataclass
class CrawlConfig:
    """爬取配置 — 所有字段均可通过 JSON / CLI 传入"""

    keyword: str = ""                       # 搜索关键词 (必填)
    target_count: int = 100                 # 目标下载数量
    max_depth: int = 3                      # 最大递归深度 (0=只爬搜索页)
    click_count: int = 5                    # 每页点击几个图片进入详情页
    scroll_times: int = 5                   # 每页滚动次数
    min_delay: float = 1.5                  # 请求最小延迟 (秒)
    max_delay: float = 3.0                  # 请求最大延迟 (秒)
    scroll_delay: float = 2.0              # 滚动间隔 (秒)
    download_dir: str = "./pinterest_images"  # 图片保存根目录
    db_file: str = "./pinterest_history.db"   # 去重数据库路径
    headless: bool = True                   # 是否无头模式 (服务器默认 True)
    timeout: int = 30000                    # 页面超时 (毫秒)
    proxy: str = ""                         # 代理地址, 如 http://127.0.0.1:7890
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CrawlConfig":
        """从字典创建配置，忽略未知字段"""
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in d.items() if k in valid_keys}
        return cls(**filtered)

    def validate(self) -> List[str]:
        """校验配置，返回错误列表"""
        errors = []
        if not self.keyword.strip():
            errors.append("keyword 不能为空")
        if self.target_count < 1:
            errors.append("target_count 必须 >= 1")
        if self.max_depth < 0:
            errors.append("max_depth 必须 >= 0")
        if self.click_count < 0:
            errors.append("click_count 必须 >= 0")
        if self.scroll_times < 1:
            errors.append("scroll_times 必须 >= 1")
        return errors

    def to_summary(self) -> str:
        """返回可读配置摘要"""
        lines = [
            f"  关键词      : {self.keyword}",
            f"  目标数量    : {self.target_count}",
            f"  递归深度    : {self.max_depth}",
            f"  每页点击    : {self.click_count}",
            f"  每页滚动    : {self.scroll_times} 次",
            f"  保存目录    : {self.download_dir}",
            f"  无头模式    : {'是' if self.headless else '否'}",
            f"  代理        : {self.proxy or '无'}",
        ]
        return "\n".join(lines)


# ============== 数据类 ==============
@dataclass
class PinInfo:
    """Pin 信息"""
    pin_id: str
    image_url: str
    detail_url: str = ""
    likes: int = 0
    depth: int = 0

    def __hash__(self):
        return hash(self.pin_id)


# ============== 去重数据库 ==============
class DeduplicationDB:
    """SQLite 去重数据库，支持 URL / 内容哈希 / Pin ID 三重去重"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self._init_db()
        self._url_cache: Set[str] = set()
        self._hash_cache: Set[str] = set()
        self._pin_cache: Set[str] = set()
        self._load_cache()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS downloaded (
                id INTEGER PRIMARY KEY,
                url TEXT,
                normalized_url TEXT UNIQUE,
                image_hash TEXT,
                pin_id TEXT,
                keyword TEXT,
                filename TEXT,
                likes INTEGER DEFAULT 0,
                depth INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_norm ON downloaded(normalized_url)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_hash ON downloaded(image_hash)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_pin  ON downloaded(pin_id)")
        conn.commit()
        conn.close()

    def _load_cache(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT normalized_url, image_hash, pin_id FROM downloaded")
        for row in cur.fetchall():
            if row[0]:
                self._url_cache.add(row[0])
            if row[1]:
                self._hash_cache.add(row[1])
            if row[2]:
                self._pin_cache.add(row[2])
        conn.close()
        logger.info(f"数据库已加载: {len(self._url_cache)} 条URL, {len(self._pin_cache)} 个Pin")

    @staticmethod
    def _normalize_url(url: str) -> str:
        for size in ["75x75", "236x", "474x", "564x", "736x", "originals"]:
            url = url.replace(f"/{size}/", "/NORM/")
        return url.split("?")[0]

    def is_url_downloaded(self, url: str) -> bool:
        return self._normalize_url(url) in self._url_cache

    def is_hash_exists(self, img_hash: str) -> bool:
        return img_hash in self._hash_cache

    def is_pin_downloaded(self, pin_id: str) -> bool:
        return pin_id in self._pin_cache

    def record(self, url, img_hash, pin_id, keyword, filename, likes=0, depth=0):
        normalized = self._normalize_url(url)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT OR IGNORE INTO downloaded "
                "(url,normalized_url,image_hash,pin_id,keyword,filename,likes,depth) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (url, normalized, img_hash, pin_id, keyword, filename, likes, depth),
            )
            conn.commit()
            self._url_cache.add(normalized)
            if img_hash:
                self._hash_cache.add(img_hash)
            if pin_id:
                self._pin_cache.add(pin_id)
        finally:
            conn.close()

    @property
    def count(self) -> int:
        return len(self._url_cache)


# ============== JS 脚本：页面内提取 Pin 信息 ==============
COLLECT_PINS_JS = """
() => {
    const pins = [];
    const seen = new Set();

    // 方法1: 查找带链接的图片
    document.querySelectorAll('a[href*="/pin/"]').forEach(link => {
        const img = link.querySelector('img[src*="pinimg.com"]');
        if (!img) return;

        const src = img.src;
        if (seen.has(src) || src.includes('75x75')) return;
        seen.add(src);

        const match = link.href.match(/\\/pin\\/(\\d+)/);
        if (!match) return;

        const pinId = match[1];

        // 获取点赞数
        let likes = 0;
        const parent = link.closest('[data-test-id="pin"]')
                     || link.closest('[data-test-id="pinWrapper"]')
                     || link.parentElement?.parentElement?.parentElement;
        if (parent) {
            const text = parent.innerText || '';
            const nums = text.match(/(\\d+\\.?\\d*)\\s*[KkMm]?/g) || [];
            for (const n of nums) {
                let val = parseFloat(n);
                if (n.toLowerCase().includes('k')) val *= 1000;
                if (n.toLowerCase().includes('m')) val *= 1000000;
                if (val > likes && val < 10000000) likes = Math.round(val);
            }
        }

        pins.push({
            pin_id: pinId,
            image_url: src,
            detail_url: link.href,
            likes: likes
        });
    });

    // 方法2: 直接查找所有图片（备用）
    if (pins.length === 0) {
        document.querySelectorAll('img[src*="pinimg.com"]').forEach((img, idx) => {
            const src = img.src;
            if (seen.has(src) || src.includes('75x75')) return;
            seen.add(src);

            pins.push({
                pin_id: 'img_' + idx + '_' + Date.now(),
                image_url: src,
                detail_url: '',
                likes: 0
            });
        });
    }

    return pins;
}
"""


# ============== 主爬虫类 ==============
class PinterestAutoCrawler:
    """Pinterest 全自动递归爬虫"""

    def __init__(self, config: CrawlConfig):
        self.config = config
        self.dedup = DeduplicationDB(config.db_file)

        # 统计
        self.downloaded_count = 0
        self.skipped_count = 0
        self.failed_count = 0

        # 访问记录
        self.visited_pins: Set[str] = set()
        self.visited_urls: Set[str] = set()

        # 保存目录
        self.save_dir = ""

        # 浏览器
        self.browser = None
        self.context = None
        self.page = None

    # ---------- 公共入口 ----------
    async def start(self) -> Dict[str, Any]:
        """启动爬虫，返回统计结果字典"""
        global STOP_FLAG

        try:
            from playwright.async_api import async_playwright
        except ImportError:
            logger.error("playwright 未安装，请先运行: pip install playwright && playwright install chromium")
            return {"error": "playwright not installed"}

        # 创建保存目录
        safe_kw = self.config.keyword.replace(" ", "_").replace("/", "_")[:30]
        folder = f"{safe_kw}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.save_dir = os.path.join(self.config.download_dir, folder)
        os.makedirs(self.save_dir, exist_ok=True)

        logger.info("=" * 60)
        logger.info("Pinterest 全自动递归爬虫")
        logger.info("=" * 60)
        logger.info("\n" + self.config.to_summary())
        logger.info(f"  保存目录    : {self.save_dir}")
        logger.info("=" * 60)

        async with async_playwright() as p:
            launch_args = [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]

            launch_kwargs = dict(headless=self.config.headless, args=launch_args)
            if self.config.proxy:
                launch_kwargs["proxy"] = {"server": self.config.proxy}

            self.browser = await p.chromium.launch(**launch_kwargs)

            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=self.config.user_agent,
            )

            # 反检测
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.chrome = { runtime: {} };
            """)

            self.page = await self.context.new_page()
            self.page.set_default_timeout(self.config.timeout)

            try:
                await self._crawl()
            finally:
                await self.browser.close()

        stats = self._get_stats()
        self._print_stats(stats)
        return stats

    # ---------- 主爬取流程 ----------
    async def _crawl(self):
        global STOP_FLAG
        search_url = f"https://www.pinterest.com/search/pins/?q={quote(self.config.keyword)}"
        logger.info(f"访问搜索页面: {search_url}")

        await self.page.goto(search_url, wait_until="networkidle")
        await asyncio.sleep(3)

        try:
            await self.page.wait_for_selector('img[src*="pinimg.com"]', timeout=15000)
            logger.info("页面加载完成")
        except Exception:
            logger.warning("页面加载超时，尝试继续...")

        await self._crawl_page(depth=0)

    async def _crawl_page(self, depth: int):
        global STOP_FLAG
        if STOP_FLAG or self.downloaded_count >= self.config.target_count:
            return

        tag = f"[深度{depth}]" if depth > 0 else "[搜索]"
        logger.info(f"{tag} 开始处理当前页面")

        # 滚动加载
        for i in range(self.config.scroll_times):
            if STOP_FLAG or self.downloaded_count >= self.config.target_count:
                break
            await self._smooth_scroll()
            logger.debug(f"  滚动 {i+1}/{self.config.scroll_times}")
            await asyncio.sleep(self.config.scroll_delay)

        # 收集
        pins = await self._collect_pins(depth)
        logger.info(f"  找到 {len(pins)} 个新图片")

        if not pins:
            return

        pins.sort(key=lambda x: x.likes, reverse=True)

        # 下载
        for pin in pins:
            if STOP_FLAG or self.downloaded_count >= self.config.target_count:
                break
            await self._download_pin(pin)
            await asyncio.sleep(random.uniform(self.config.min_delay, self.config.max_delay))

        # 递归
        if (
            not STOP_FLAG
            and self.downloaded_count < self.config.target_count
            and depth < self.config.max_depth
        ):
            await self._explore_recommendations(pins, depth)

    # ---------- 收集 Pin ----------
    async def _collect_pins(self, depth: int) -> List[PinInfo]:
        pins = []
        try:
            result = await self.page.evaluate(COLLECT_PINS_JS)
            for item in result:
                pid = item["pin_id"]
                if pid in self.visited_pins:
                    continue
                if self.dedup.is_pin_downloaded(pid):
                    continue
                self.visited_pins.add(pid)
                pins.append(
                    PinInfo(
                        pin_id=pid,
                        image_url=item["image_url"],
                        detail_url=item.get("detail_url", ""),
                        likes=item.get("likes", 0),
                        depth=depth,
                    )
                )
        except Exception as e:
            logger.error(f"收集失败: {e}")
        return pins

    # ---------- 下载 ----------
    async def _download_pin(self, pin: PinInfo):
        global STOP_FLAG
        if STOP_FLAG:
            return

        if self.dedup.is_url_downloaded(pin.image_url):
            self.skipped_count += 1
            return

        try:
            import requests  # lazy import — 脚本可能不需要此模块直到此处

            # 升级到最高分辨率
            url = pin.image_url
            for size in ["75x75", "236x", "474x", "564x", "736x"]:
                if size in url:
                    url = url.replace(size, "originals")
                    break

            headers = {
                "User-Agent": self.config.user_agent,
                "Referer": "https://www.pinterest.com/",
            }

            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()

            if "image" not in resp.headers.get("content-type", ""):
                self.failed_count += 1
                return

            img_hash = hashlib.md5(resp.content).hexdigest()
            if self.dedup.is_hash_exists(img_hash):
                self.skipped_count += 1
                return

            ext = ".jpg"
            for e in [".png", ".gif", ".webp"]:
                if e in url.lower():
                    ext = e
                    break

            depth_tag = f"d{pin.depth}" if pin.depth > 0 else "s"
            filename = f"{pin.pin_id}_{pin.likes}likes_{depth_tag}{ext}"
            filepath = os.path.join(self.save_dir, filename)

            with open(filepath, "wb") as f:
                f.write(resp.content)

            self.dedup.record(
                url, img_hash, pin.pin_id, self.config.keyword,
                filename, pin.likes, pin.depth,
            )

            self.downloaded_count += 1
            logger.info(f"  [{self.downloaded_count}/{self.config.target_count}] {filename}")

        except Exception as e:
            self.failed_count += 1
            logger.error(f"  下载失败: {pin.pin_id} - {str(e)[:60]}")

    # ---------- 探索推荐 ----------
    async def _explore_recommendations(self, pins: List[PinInfo], current_depth: int):
        global STOP_FLAG

        pins_with_url = [p for p in pins if p.detail_url and p.detail_url.startswith("http")]
        pins_with_url.sort(key=lambda x: x.likes, reverse=True)

        click_count = min(self.config.click_count, len(pins_with_url))
        if click_count == 0:
            logger.warning("没有可点击的图片链接")
            return

        logger.info(f"探索推荐 (将访问 {click_count} 个详情页)...")

        for i, pin in enumerate(pins_with_url[:click_count]):
            if STOP_FLAG or self.downloaded_count >= self.config.target_count:
                break

            if pin.detail_url in self.visited_urls:
                continue
            self.visited_urls.add(pin.detail_url)

            logger.info(f"  进入详情页 {i+1}/{click_count}: {pin.pin_id} (likes={pin.likes})")

            try:
                await self.page.goto(pin.detail_url, wait_until="networkidle")
                await asyncio.sleep(2)

                try:
                    await self.page.wait_for_selector('img[src*="pinimg.com"]', timeout=10000)
                except Exception:
                    pass

                for _ in range(3):
                    if STOP_FLAG:
                        break
                    await self._smooth_scroll()
                    await asyncio.sleep(1)

                await self._crawl_page(depth=current_depth + 1)

            except Exception as e:
                logger.error(f"  访问详情页失败: {e}")

            await asyncio.sleep(random.uniform(1, 2))

        # 回到搜索页
        if not STOP_FLAG and self.downloaded_count < self.config.target_count:
            logger.info("返回搜索页面...")
            try:
                search_url = f"https://www.pinterest.com/search/pins/?q={quote(self.config.keyword)}"
                await self.page.goto(search_url, wait_until="networkidle")
                await asyncio.sleep(2)
            except Exception:
                pass

    # ---------- 辅助 ----------
    async def _smooth_scroll(self):
        await self.page.evaluate("""
            () => window.scrollBy({ top: window.innerHeight * 0.8, behavior: 'smooth' })
        """)

    def _get_stats(self) -> Dict[str, Any]:
        return {
            "keyword": self.config.keyword,
            "downloaded": self.downloaded_count,
            "skipped": self.skipped_count,
            "failed": self.failed_count,
            "db_total": self.dedup.count,
            "save_dir": self.save_dir,
        }

    def _print_stats(self, stats: Dict[str, Any]):
        logger.info("=" * 60)
        logger.info("爬取完成!")
        logger.info(f"  成功下载 : {stats['downloaded']}")
        logger.info(f"  跳过重复 : {stats['skipped']}")
        logger.info(f"  下载失败 : {stats['failed']}")
        logger.info(f"  数据库总计: {stats['db_total']}")
        logger.info(f"  保存目录 : {stats['save_dir']}")
        logger.info("=" * 60)

        # 同时输出 JSON 统计到 stdout，方便上层脚本解析
        print(f"\n__RESULT_JSON__:{json.dumps(stats, ensure_ascii=False)}")


# ============== CLI 入口 ==============
def parse_args() -> CrawlConfig:
    parser = argparse.ArgumentParser(
        description="Pinterest 全自动递归爬虫",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # JSON 参数 (优先级最高)
    parser.add_argument(
        "--params",
        type=str,
        default="",
        help='JSON 字符串，如 \'{"keyword":"cats","target_count":50}\'',
    )

    # 逐项参数
    parser.add_argument("--keyword", "-k", type=str, default="", help="搜索关键词")
    parser.add_argument("--target-count", "-n", type=int, default=100, help="目标数量 (默认 100)")
    parser.add_argument("--max-depth", type=int, default=3, help="递归深度 (默认 3)")
    parser.add_argument("--click-count", type=int, default=5, help="每页点击数 (默认 5)")
    parser.add_argument("--scroll-times", type=int, default=5, help="每页滚动次数 (默认 5)")
    parser.add_argument("--min-delay", type=float, default=1.5, help="最小延迟秒数")
    parser.add_argument("--max-delay", type=float, default=3.0, help="最大延迟秒数")
    parser.add_argument("--scroll-delay", type=float, default=2.0, help="滚动间隔秒数")
    parser.add_argument("--download-dir", type=str, default="./pinterest_images", help="下载目录")
    parser.add_argument("--db-file", type=str, default="./pinterest_history.db", help="数据库文件")
    parser.add_argument("--headless", action="store_true", default=False, help="无头模式")
    parser.add_argument("--proxy", type=str, default="", help="代理地址")
    parser.add_argument("--timeout", type=int, default=30000, help="页面超时(ms)")

    args = parser.parse_args()

    # 优先使用 --params JSON
    if args.params:
        try:
            params = json.loads(args.params)
            return CrawlConfig.from_dict(params)
        except json.JSONDecodeError as e:
            logger.error(f"JSON 参数解析失败: {e}")
            sys.exit(1)

    # 否则使用逐项参数
    return CrawlConfig(
        keyword=args.keyword,
        target_count=args.target_count,
        max_depth=args.max_depth,
        click_count=args.click_count,
        scroll_times=args.scroll_times,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        scroll_delay=args.scroll_delay,
        download_dir=args.download_dir,
        db_file=args.db_file,
        headless=args.headless,
        proxy=args.proxy,
        timeout=args.timeout,
    )


async def async_main():
    config = parse_args()

    errors = config.validate()
    if errors:
        for e in errors:
            logger.error(e)
        sys.exit(1)

    crawler = PinterestAutoCrawler(config)
    await crawler.start()


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("用户中断")
    except Exception as e:
        logger.error(f"致命错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
