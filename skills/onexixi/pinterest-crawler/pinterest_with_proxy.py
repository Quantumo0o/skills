#!/usr/bin/env python3
"""
Pinterest 一键爬虫 — 流式代理验证 + 即时爬取

核心逻辑:
  1. 从 18 个免费源并发采集 SOCKS5 代理 (10万+)
  2. 随机打乱, 分小批 (每批200) 并发 curl 测 Pinterest
  3. 第一个能通的代理 → 立刻开始爬图, 不等其他验证完成
  4. 爬图过程中代理挂了 → 立刻从下一批未验证的里找新代理
  5. 输出 list.txt (所有验证通过的代理)

用法:
  python pinterest_with_proxy.py --keyword "cute cats" --count 50
  python pinterest_with_proxy.py --keyword "logo design" --count 100 --batch-size 300
  python pinterest_with_proxy.py --proxy-file list.txt --keyword "cats" --count 30
"""

import os, sys, re, json, time, random, asyncio, hashlib, sqlite3
import signal, struct, socket, subprocess, threading, argparse, logging
from datetime import datetime
from urllib.parse import quote
from urllib.request import urlopen, Request
from dataclasses import dataclass
from typing import List, Set, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("pinterest")

STOP_FLAG = False
def _sig(s, f):
    global STOP_FLAG; STOP_FLAG = True; logger.warning("Ctrl+C 安全停止中...")
signal.signal(signal.SIGINT, _sig)

# ╔═══════════════════════════════════════════════════╗
# ║  CONFIG                                           ║
# ╚═══════════════════════════════════════════════════╝
@dataclass
class Config:
    keyword: str = ""
    target_count: int = 100
    max_depth: int = 2
    click_count: int = 5
    scroll_times: int = 4
    min_delay: float = 0.8
    max_delay: float = 2.0
    scroll_delay: float = 1.2
    download_dir: str = "./pinterest_images"
    db_file: str = "./pinterest_history.db"
    headless: bool = True
    timeout: int = 25000
    # 代理
    proxy_timeout: int = 6
    proxy_workers: int = 200
    batch_size: int = 200           # 每批验证多少个
    proxy_file: str = ""
    user_agent: str = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    @classmethod
    def from_dict(cls, d):
        v = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: d[k] for k in d if k in v})

    def validate(self):
        e = []
        if not self.keyword.strip(): e.append("keyword 不能为空")
        if self.target_count < 1: e.append("target_count >= 1")
        return e


# ╔═══════════════════════════════════════════════════╗
# ║  PART 1: 代理采集 — 18 源并发                     ║
# ╚═══════════════════════════════════════════════════╝
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def _http_get(url, timeout=20):
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except: return ""

def _extract_ips(text):
    out = []
    for m in re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})', text):
        ip, port = m.group(1), int(m.group(2))
        if all(0 <= int(p) <= 255 for p in ip.split(".")) and 1 <= port <= 65535:
            out.append(f"{ip}:{port}")
    return out

def scrape_all_proxies() -> List[str]:
    """从所有免费源并发采集 SOCKS5 代理, 返回去重随机打乱列表"""
    seen = set(); results = []; lock = threading.Lock()

    urls = [
        ("proxifly", "https://github.com/proxifly/free-proxy-list/blob/main/proxies/protocols/socks5/data.txt"),
        ("TheSpeedX", "https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt"),
        ("monosans", "https://github.com/monosans/proxy-list/blob/main/proxies/socks5.txt"),
        ("hookzof", "https://github.com/hookzof/socks5_list/blob/master/proxy.txt"),
        ("jetkai", "https://github.com/jetkai/proxy-list/blob/main/online-proxies/txt/proxies-socks5.txt"),
        ("roosterkid", "https://github.com/roosterkid/openproxylist/blob/main/SOCKS5_RAW.txt"),
        ("MuRongPIG", "https://github.com/MuRongPIG/Proxy-Master/blob/main/socks5.txt"),
        ("prxchk", "https://github.com/prxchk/proxy-list/blob/main/socks5.txt"),
        ("zloi-user", "https://github.com/zloi-user/hideip.me/blob/main/socks5.txt"),
        ("ErcinDeworken", "https://github.com/ErcinDedeworken/proxy-list/blob/main/proxies/socks5.txt"),
        ("raw-proxifly", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt"),
        ("raw-TheSpeedX", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"),
        ("raw-monosans", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt"),
        ("proxyscrape", "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text&protocol=socks5"),
        ("sockslist", "https://sockslist.us/Api?request=display&country=all&level=all&token=free"),
        ("spys.me", "https://spys.me/socks.txt"),
        ("openproxylist", "https://openproxylist.xyz/socks5.txt"),
        ("freeproxyworld", "https://www.freeproxy.world/?type=socks5&anonymity=&country=&speed=&port=&page=1"),
    ]

    logger.info(f"采集 SOCKS5 代理 ({len(urls)} 源并发)...")

    def _fetch(name, url):
        text = _http_get(url)
        if not text: return
        ips = _extract_ips(text)
        added = 0
        with lock:
            for addr in ips:
                if addr not in seen:
                    seen.add(addr); results.append(addr); added += 1
        if added > 0:
            logger.info(f"  ✅ {name}: +{added}")

    with ThreadPoolExecutor(max_workers=len(urls)) as pool:
        list(pool.map(lambda x: _fetch(*x), urls))

    random.shuffle(results)
    logger.info(f"采集完成: {len(results)} 个去重代理 (已随机打乱)\n")
    return results


# ╔═══════════════════════════════════════════════════╗
# ║  PART 2: 流式代理池 — 小批验证, 即拿即用           ║
# ╚═══════════════════════════════════════════════════╝

class ProxyPool:
    """
    流式代理池:
    - 小批量从未验证列表中取代理
    - 并发 curl --socks5 测 Pinterest
    - 通过的立刻可用, 不等整批完成
    - 爬虫随时可以要下一个可用代理
    """

    def __init__(self, raw_list: List[str], batch_size=200,
                 timeout=6, workers=200,
                 test_url="https://www.pinterest.com/"):
        self.raw = raw_list
        self.raw_idx = 0
        self.batch_size = batch_size
        self.timeout = timeout
        self.workers = workers
        self.test_url = test_url
        self.valid: List[Tuple[str, float]] = []   # (addr, latency_ms)
        self.valid_idx = 0
        self.lock = threading.Lock()
        self.total_tested = 0
        self.total_passed = 0

    @property
    def has_more_raw(self): return self.raw_idx < len(self.raw)

    @property
    def remaining_raw(self): return len(self.raw) - self.raw_idx

    def _test_one(self, addr: str) -> Optional[Tuple[str, float]]:
        """curl --socks5 测试单个代理"""
        try:
            t0 = time.time()
            r = subprocess.run(
                ["curl", "-s", "-I", "--socks5", addr,
                 "--connect-timeout", str(self.timeout),
                 "--max-time", str(self.timeout + 2),
                 "-o", "/dev/null", "-w", "%{http_code}",
                 self.test_url],
                capture_output=True, text=True, timeout=self.timeout + 5)
            ms = (time.time() - t0) * 1000
            code = r.stdout.strip()
            if code and code != "000":
                return (addr, round(ms, 1))
        except: pass
        return None

    def validate_batch(self) -> int:
        """验证下一批, 通过的加入 valid, 返回本批通过数"""
        end = min(self.raw_idx + self.batch_size, len(self.raw))
        batch = self.raw[self.raw_idx:end]
        self.raw_idx = end
        if not batch: return 0

        bn = self.raw_idx // self.batch_size
        logger.info(f"🔍 验证批次 #{bn}: {len(batch)} 个 "
                     f"(已测={self.total_tested} 可用={self.total_passed} 未测={self.remaining_raw})")

        passed = 0
        with ThreadPoolExecutor(max_workers=min(self.workers, len(batch))) as pool:
            futs = {pool.submit(self._test_one, a): a for a in batch}
            for f in as_completed(futs):
                self.total_tested += 1
                res = f.result()
                if res:
                    with self.lock:
                        self.valid.append(res)
                        self.total_passed += 1
                        passed += 1
                    logger.info(f"  ✅ {res[0]} — {res[1]:.0f}ms (总可用={self.total_passed})")

        logger.info(f"  批次结果: {passed}/{len(batch)} 通过\n")
        return passed

    def get_next_valid(self) -> Optional[str]:
        """取下一个可用代理, 没有则自动验证下一批, 全用完返回 None"""
        while True:
            with self.lock:
                if self.valid_idx < len(self.valid):
                    addr = self.valid[self.valid_idx][0]
                    self.valid_idx += 1
                    return addr
            if not self.has_more_raw:
                return None
            self.validate_batch()

    def save_list(self, path: str):
        with self.lock:
            sv = sorted(self.valid, key=lambda x: x[1])
        with open(path, "w") as f:
            f.write(f"# Pinterest SOCKS5 可用代理 — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"# 共 {len(sv)} 个 | 已测 {self.total_tested} | 按延迟排序\n\n")
            for addr, lat in sv:
                f.write(f"{addr}  # {lat:.0f}ms\n")
        logger.info(f"💾 list.txt 已保存: {path} ({len(sv)} 个可用代理)")


# ╔═══════════════════════════════════════════════════╗
# ║  PART 3: Pinterest 爬虫                           ║
# ╚═══════════════════════════════════════════════════╝

COLLECT_PINS_JS = """
() => {
    const pins = []; const seen = new Set();
    document.querySelectorAll('a[href*="/pin/"]').forEach(link => {
        const img = link.querySelector('img[src*="pinimg.com"]');
        if (!img) return;
        const src = img.src;
        if (seen.has(src) || src.includes('75x75')) return;
        seen.add(src);
        const match = link.href.match(/\\/pin\\/(\\d+)/);
        if (!match) return;
        let likes = 0;
        const p = link.closest('[data-test-id="pin"]')
                || link.closest('[data-test-id="pinWrapper"]')
                || link.parentElement?.parentElement?.parentElement;
        if (p) {
            const nums = (p.innerText||'').match(/(\\d+\\.?\\d*)\\s*[KkMm]?/g)||[];
            for (const n of nums) {
                let v = parseFloat(n);
                if (n.toLowerCase().includes('k')) v*=1000;
                if (n.toLowerCase().includes('m')) v*=1000000;
                if (v > likes && v < 1e7) likes = Math.round(v);
            }
        }
        pins.push({ pin_id: match[1], image_url: src, detail_url: link.href, likes });
    });
    if (!pins.length) {
        document.querySelectorAll('img[src*="pinimg.com"]').forEach((img,i) => {
            const src = img.src;
            if (seen.has(src)||src.includes('75x75')) return; seen.add(src);
            pins.push({ pin_id:'img_'+i+'_'+Date.now(), image_url:src, detail_url:'', likes:0 });
        });
    }
    return pins;
}
"""

class DeduplicationDB:
    def __init__(self, p):
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        self.p = p; self._init(); self._uc=set(); self._hc=set(); self._pc=set(); self._load()
    def _init(self):
        c=sqlite3.connect(self.p)
        c.execute("CREATE TABLE IF NOT EXISTS dl(id INTEGER PRIMARY KEY,url TEXT,"
            "nurl TEXT UNIQUE,hash TEXT,pid TEXT,kw TEXT,fn TEXT,likes INT DEFAULT 0,"
            "depth INT DEFAULT 0,ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        c.execute("CREATE INDEX IF NOT EXISTS i1 ON dl(nurl)")
        c.execute("CREATE INDEX IF NOT EXISTS i2 ON dl(hash)")
        c.execute("CREATE INDEX IF NOT EXISTS i3 ON dl(pid)")
        c.commit(); c.close()
    def _load(self):
        c=sqlite3.connect(self.p)
        for r in c.execute("SELECT nurl,hash,pid FROM dl"):
            if r[0]: self._uc.add(r[0])
            if r[1]: self._hc.add(r[1])
            if r[2]: self._pc.add(r[2])
        c.close()
    @staticmethod
    def _n(u):
        for s in ['75x75','236x','474x','564x','736x','originals']:
            u=u.replace(f'/{s}/','/N/')
        return u.split('?')[0]
    def url_ok(self,u): return self._n(u) in self._uc
    def hash_ok(self,h): return h in self._hc
    def pin_ok(self,p): return p in self._pc
    def add(self,url,h,pid,kw,fn,likes=0,depth=0):
        n=self._n(url); c=sqlite3.connect(self.p)
        try:
            c.execute("INSERT OR IGNORE INTO dl(url,nurl,hash,pid,kw,fn,likes,depth)"
                " VALUES(?,?,?,?,?,?,?,?)",(url,n,h,pid,kw,fn,likes,depth))
            c.commit(); self._uc.add(n)
            if h: self._hc.add(h)
            if pid: self._pc.add(pid)
        finally: c.close()
    @property
    def count(self): return len(self._uc)


class Crawler:
    def __init__(self, config: Config, proxy_pool: ProxyPool):
        self.cfg = config
        self.pool = proxy_pool
        self.dedup = DeduplicationDB(config.db_file)
        self.dl = 0; self.skip = 0; self.fail = 0
        self.visited_pins: Set[str] = set()
        self.visited_urls: Set[str] = set()
        self.save_dir = ""
        self.current_proxy = ""

    async def start(self) -> Dict[str, Any]:
        global STOP_FLAG
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            logger.error("pip install playwright && playwright install chromium")
            return {"error": "playwright not installed"}

        kw = re.sub(r'[^\w]', '_', self.cfg.keyword)[:30]
        self.save_dir = os.path.join(self.cfg.download_dir,
            f"{kw}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(self.save_dir, exist_ok=True)

        logger.info("="*60)
        logger.info(f"🚀 关键词: {self.cfg.keyword} | 目标: {self.cfg.target_count} 张")
        logger.info(f"   保存: {self.save_dir}")
        logger.info("="*60)

        async with async_playwright() as pw:
            while self.dl < self.cfg.target_count and not STOP_FLAG:
                proxy_addr = self.pool.get_next_valid()
                if not proxy_addr:
                    logger.error("所有代理用完了"); break

                self.current_proxy = proxy_addr
                logger.info(f"\n🌐 尝试代理: {proxy_addr}")

                try:
                    finished = await self._run_with_proxy(pw, proxy_addr)
                    if finished or self.dl >= self.cfg.target_count:
                        break
                except Exception as e:
                    logger.warning(f"💀 代理挂了: {str(e)[:60]}, 换下一个...")
                    continue

        stats = {"keyword": self.cfg.keyword, "downloaded": self.dl,
                 "skipped": self.skip, "failed": self.fail,
                 "db_total": self.dedup.count, "save_dir": self.save_dir,
                 "proxy_used": self.current_proxy}
        logger.info("="*60)
        logger.info(f"📊 完成! 下载={self.dl} 跳过={self.skip} 失败={self.fail}")
        logger.info(f"   目录: {self.save_dir}")
        logger.info("="*60)
        print(f"\n__RESULT__:{json.dumps(stats, ensure_ascii=False)}")
        return stats

    async def _run_with_proxy(self, pw, proxy_addr) -> bool:
        browser = await pw.chromium.launch(
            headless=self.cfg.headless,
            args=['--disable-blink-features=AutomationControlled',
                  '--disable-dev-shm-usage', '--no-sandbox'],
            proxy={"server": f"socks5://{proxy_addr}"})
        try:
            ctx = await browser.new_context(
                viewport={"width":1920,"height":1080}, user_agent=self.cfg.user_agent)
            await ctx.add_init_script(
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
                "window.chrome={runtime:{}};")
            page = await ctx.new_page()
            page.set_default_timeout(self.cfg.timeout)

            url = f"https://www.pinterest.com/search/pins/?q={quote(self.cfg.keyword)}"
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            await asyncio.sleep(3)

            img_n = await page.evaluate('()=>document.querySelectorAll("img[src*=pinimg]").length')
            if img_n == 0:
                logger.warning(f"代理 {proxy_addr} 页面没图, 跳过")
                return False

            logger.info(f"✅ 页面OK! {img_n} 张图")
            await self._crawl_page(page, proxy_addr, 0)
            return True
        except Exception as e:
            logger.warning(f"爬取中断: {str(e)[:60]}")
            return False
        finally:
            try: await browser.close()
            except: pass

    async def _crawl_page(self, page, proxy_addr, depth):
        global STOP_FLAG
        if STOP_FLAG or self.dl >= self.cfg.target_count: return

        for _ in range(self.cfg.scroll_times):
            if STOP_FLAG or self.dl >= self.cfg.target_count: break
            await page.evaluate("()=>window.scrollBy({top:window.innerHeight*0.8,behavior:'smooth'})")
            await asyncio.sleep(self.cfg.scroll_delay)

        pins = await self._collect(page)
        logger.info(f"  {'[搜索]' if depth==0 else f'[深度{depth}]'} {len(pins)} 个新图")
        if not pins: return

        pins.sort(key=lambda x: x.get("likes",0), reverse=True)
        for pin in pins:
            if STOP_FLAG or self.dl >= self.cfg.target_count: break
            await self._download(pin, proxy_addr, depth)
            await asyncio.sleep(random.uniform(self.cfg.min_delay, self.cfg.max_delay))

        if not STOP_FLAG and self.dl < self.cfg.target_count and depth < self.cfg.max_depth:
            await self._explore(page, pins, proxy_addr, depth)

    async def _collect(self, page):
        try:
            result = await page.evaluate(COLLECT_PINS_JS)
            out = []
            for it in result:
                pid = it["pin_id"]
                if pid in self.visited_pins or self.dedup.pin_ok(pid): continue
                self.visited_pins.add(pid); out.append(it)
            return out
        except: return []

    async def _download(self, pin, proxy_addr, depth):
        global STOP_FLAG
        if STOP_FLAG: return
        url = pin["image_url"]
        if self.dedup.url_ok(url): self.skip+=1; return
        try:
            import requests
            hd = url
            for s in ['75x75','236x','474x','564x','736x']:
                if s in hd: hd=hd.replace(s,'originals'); break
            px = {"http":f"socks5h://{proxy_addr}","https":f"socks5h://{proxy_addr}"}
            resp = requests.get(hd, headers={"User-Agent":self.cfg.user_agent,
                "Referer":"https://www.pinterest.com/"}, proxies=px, timeout=12)
            resp.raise_for_status()
            if "image" not in resp.headers.get("content-type",""): self.fail+=1; return
            h = hashlib.md5(resp.content).hexdigest()
            if self.dedup.hash_ok(h): self.skip+=1; return
            ext=".jpg"
            for e in [".png",".gif",".webp"]:
                if e in hd.lower(): ext=e; break
            dtag = f"d{depth}" if depth>0 else "s"
            likes = pin.get("likes",0)
            fn = f"{pin['pin_id']}_{likes}likes_{dtag}{ext}"
            with open(os.path.join(self.save_dir, fn), "wb") as f: f.write(resp.content)
            self.dedup.add(hd, h, pin["pin_id"], self.cfg.keyword, fn, likes, depth)
            self.dl += 1
            logger.info(f"  ✅ [{self.dl}/{self.cfg.target_count}] {fn}")
        except: self.fail+=1

    async def _explore(self, page, pins, proxy_addr, cur_depth):
        global STOP_FLAG
        wu = [p for p in pins if p.get("detail_url","").startswith("http")]
        wu.sort(key=lambda x: x.get("likes",0), reverse=True)
        n = min(self.cfg.click_count, len(wu))
        if n==0: return
        logger.info(f"🔍 探索 {n} 个推荐...")
        for pin in wu[:n]:
            if STOP_FLAG or self.dl >= self.cfg.target_count: break
            u = pin["detail_url"]
            if u in self.visited_urls: continue
            self.visited_urls.add(u)
            try:
                await page.goto(u, wait_until="domcontentloaded", timeout=15000)
                await asyncio.sleep(1.5)
                for _ in range(2):
                    if STOP_FLAG: break
                    await page.evaluate("()=>window.scrollBy({top:window.innerHeight*0.8,behavior:'smooth'})")
                    await asyncio.sleep(0.8)
                await self._crawl_page(page, proxy_addr, cur_depth+1)
            except: pass
            await asyncio.sleep(random.uniform(0.5, 1.2))
        if not STOP_FLAG and self.dl < self.cfg.target_count:
            try:
                await page.goto(f"https://www.pinterest.com/search/pins/?q={quote(self.cfg.keyword)}",
                    wait_until="domcontentloaded", timeout=15000)
                await asyncio.sleep(2)
            except: pass


# ╔═══════════════════════════════════════════════════╗
# ║  MAIN                                             ║
# ╚═══════════════════════════════════════════════════╝

def parse_args():
    p = argparse.ArgumentParser(description="Pinterest 一键爬虫 (流式代理)")
    p.add_argument("--params", default="")
    p.add_argument("--keyword", "-k", default="")
    p.add_argument("--count", "-n", type=int, default=100)
    p.add_argument("--max-depth", type=int, default=2)
    p.add_argument("--click-count", type=int, default=5)
    p.add_argument("--scroll-times", type=int, default=4)
    p.add_argument("--headless", action="store_true", default=True)
    p.add_argument("--no-headless", dest="headless", action="store_false")
    p.add_argument("--download-dir", default="./pinterest_images")
    p.add_argument("--db-file", default="./pinterest_history.db")
    p.add_argument("--proxy-timeout", type=int, default=6)
    p.add_argument("--proxy-workers", type=int, default=200)
    p.add_argument("--batch-size", type=int, default=200)
    p.add_argument("--proxy-file", default="")
    a = p.parse_args()
    if a.params: return Config.from_dict(json.loads(a.params))
    return Config(keyword=a.keyword, target_count=a.count, max_depth=a.max_depth,
        click_count=a.click_count, scroll_times=a.scroll_times, headless=a.headless,
        download_dir=a.download_dir, db_file=a.db_file, proxy_timeout=a.proxy_timeout,
        proxy_workers=a.proxy_workers, batch_size=a.batch_size, proxy_file=a.proxy_file)

async def main():
    cfg = parse_args()
    errs = cfg.validate()
    if errs:
        for e in errs: logger.error(e)
        sys.exit(1)

    t0 = time.time()

    # Step 1: 代理列表
    if cfg.proxy_file and os.path.exists(cfg.proxy_file):
        logger.info(f"从文件加载: {cfg.proxy_file}")
        with open(cfg.proxy_file) as f:
            raw = [l.split("#")[0].strip() for l in f if l.strip() and not l.startswith("#")]
        raw = [p for p in raw if re.match(r'\d+\.\d+\.\d+\.\d+:\d+', p)]
        random.shuffle(raw)
        logger.info(f"加载 {len(raw)} 个")
    else:
        raw = scrape_all_proxies()

    if not raw: logger.error("没有代理"); sys.exit(1)

    # Step 2: 流式代理池
    pool = ProxyPool(raw, batch_size=cfg.batch_size,
                     timeout=cfg.proxy_timeout, workers=cfg.proxy_workers)

    # Step 3: 验证第一批
    pool.validate_batch()
    # 第一批没过? 再来两批
    for _ in range(2):
        if pool.total_passed > 0 or not pool.has_more_raw: break
        pool.validate_batch()

    if pool.total_passed == 0:
        logger.error("前几批都没可用代理, 检查网络"); sys.exit(1)

    # Step 4: 开始爬 (挂了自动从池里取下一个)
    crawler = Crawler(cfg, pool)
    await crawler.start()

    # Step 5: 保存 list.txt
    list_path = os.path.join(os.path.dirname(cfg.download_dir) or ".", "list.txt")
    pool.save_list(list_path)

    logger.info(f"\n⏱ 总耗时: {time.time()-t0:.0f}s")

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: logger.info("用户中断")
    except Exception as e:
        logger.error(f"错误: {e}"); import traceback; traceback.print_exc(); sys.exit(1)
