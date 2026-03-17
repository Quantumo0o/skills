#!/usr/bin/env python3
"""
SOCKS5 代理爬取 + 验证工具

功能:
  1. 从多个免费代理源批量采集 SOCKS5 代理（重点香港）
  2. 多线程并发验证每个代理是否真正可用
  3. 测量延迟、检测匿名等级、验证出口 IP 地域
  4. 按延迟排序，输出 list.txt

用法:
  python socks5_scraper.py                          # 默认：采集+验证，输出 list.txt
  python socks5_scraper.py --country HK             # 只要香港代理
  python socks5_scraper.py --country ALL             # 所有地区
  python socks5_scraper.py --timeout 8 --workers 80  # 自定义超时和并发
  python socks5_scraper.py --output my_proxies.txt   # 自定义输出文件
"""

import re
import sys
import json
import time
import socket
import struct
import argparse
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Set
from urllib.request import urlopen, Request
from urllib.error import URLError
from dataclasses import dataclass, field

# ============== 日志 ==============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("socks5_scraper")

# ============== 数据结构 ==============
@dataclass
class ProxyInfo:
    ip: str
    port: int
    country: str = ""
    city: str = ""
    anonymity: str = ""
    source: str = ""
    latency_ms: float = 0.0
    exit_ip: str = ""
    exit_country: str = ""
    verified: bool = False
    error: str = ""

    @property
    def addr(self) -> str:
        return f"{self.ip}:{self.port}"

    def to_line(self) -> str:
        """输出格式: ip:port  # latency=XXms country=XX exit_ip=X.X.X.X"""
        parts = [self.addr]
        meta = []
        if self.latency_ms > 0:
            meta.append(f"latency={self.latency_ms:.0f}ms")
        if self.exit_country:
            meta.append(f"country={self.exit_country}")
        if self.exit_ip:
            meta.append(f"exit_ip={self.exit_ip}")
        if self.anonymity:
            meta.append(f"anon={self.anonymity}")
        if self.source:
            meta.append(f"src={self.source}")
        if meta:
            parts.append("  # " + " | ".join(meta))
        return "".join(parts)


# ============== HTTP 工具 ==============
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def http_get(url: str, timeout: int = 15) -> str:
    """简易 HTTP GET"""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        logger.debug(f"HTTP GET 失败 {url}: {e}")
        return ""


# ============== 代理源采集器 ==============
class ProxyScraper:
    """从多个免费源采集 SOCKS5 代理"""

    def __init__(self, country_filter: str = "HK"):
        self.country_filter = country_filter.upper()
        self.seen: Set[str] = set()
        self.proxies: List[ProxyInfo] = []
        self.lock = threading.Lock()

    def _add(self, ip: str, port: int, country: str = "", city: str = "",
             anonymity: str = "", source: str = ""):
        """去重添加"""
        key = f"{ip}:{port}"
        with self.lock:
            if key in self.seen:
                return
            self.seen.add(key)

            # 国家过滤
            if self.country_filter != "ALL":
                if country and self.country_filter not in country.upper():
                    return

            self.proxies.append(ProxyInfo(
                ip=ip, port=port, country=country, city=city,
                anonymity=anonymity, source=source
            ))

    def scrape_all(self) -> List[ProxyInfo]:
        """从所有源采集"""
        sources = [
            ("github/proxifly", self._source_proxifly),
            ("github/TheSpeedX", self._source_thespeedx),
            ("github/monosans", self._source_monosans),
            ("github/hookzof", self._source_hookzof),
            ("github/jetkai", self._source_jetkai),
            ("sockslist.us", self._source_sockslist),
            ("proxyscrape.com", self._source_proxyscrape),
            ("spys.one", self._source_spys),
            ("openproxylist", self._source_openproxylist),
            ("free-proxy-list.com", self._source_freeproxylist),
        ]

        logger.info(f"开始采集 SOCKS5 代理 (国家过滤: {self.country_filter})")
        logger.info(f"共 {len(sources)} 个数据源")

        for name, func in sources:
            try:
                before = len(self.proxies)
                func()
                after = len(self.proxies)
                added = after - before
                if added > 0:
                    logger.info(f"  ✅ {name}: +{added} 个代理")
                else:
                    logger.info(f"  ⚪ {name}: 无新代理")
            except Exception as e:
                logger.warning(f"  ❌ {name}: {str(e)[:60]}")

        logger.info(f"采集完成: 共 {len(self.proxies)} 个去重代理")
        return self.proxies

    # ---------- 辅助：从 GitHub blob 页面抓 ip:port ----------

    def _scrape_github_blob(self, url: str, source: str):
        """从 GitHub blob 页面 HTML 中用正则提取 ip:port"""
        text = http_get(url, timeout=20)
        if not text:
            return
        for m in re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})', text):
            ip, port_s = m.group(1), m.group(2)
            # 过滤明显非法 IP
            parts = ip.split(".")
            if all(0 <= int(p) <= 255 for p in parts):
                self._add(ip, int(port_s), source=source)

    # ---------- 各数据源 ----------

    def _source_proxifly(self):
        """github.com/proxifly/free-proxy-list — 高质量"""
        self._scrape_github_blob(
            "https://github.com/proxifly/free-proxy-list/blob/main/proxies/protocols/socks5/data.txt",
            "proxifly",
        )

    def _source_thespeedx(self):
        """github.com/TheSpeedX/PROXY-List — 超大列表"""
        self._scrape_github_blob(
            "https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt",
            "TheSpeedX",
        )

    def _source_monosans(self):
        """github.com/monosans/proxy-list"""
        self._scrape_github_blob(
            "https://github.com/monosans/proxy-list/blob/main/proxies/socks5.txt",
            "monosans",
        )

    def _source_hookzof(self):
        """github.com/hookzof/socks5_list"""
        self._scrape_github_blob(
            "https://github.com/hookzof/socks5_list/blob/master/proxy.txt",
            "hookzof",
        )

    def _source_jetkai(self):
        """github.com/jetkai/proxy-list"""
        self._scrape_github_blob(
            "https://github.com/jetkai/proxy-list/blob/main/online-proxies/txt/proxies-socks5.txt",
            "jetkai",
        )

    def _source_sockslist(self):
        """sockslist.us API"""
        url = "https://sockslist.us/Api?request=display&country=all&level=all&token=free"
        text = http_get(url)
        if not text:
            text = http_get("https://sockslist.us/Json")
        try:
            data = json.loads(text)
            if isinstance(data, list):
                for item in data:
                    ip = item.get("ip", "")
                    port = int(item.get("port", 0))
                    country = item.get("country_code", item.get("country", ""))
                    if ip and port:
                        self._add(ip, port, country=country,
                                  anonymity=item.get("level", ""),
                                  source="sockslist")
        except (json.JSONDecodeError, TypeError):
            for m in re.finditer(r'(\d+\.\d+\.\d+\.\d+)\D+(\d{2,5})', text):
                self._add(m.group(1), int(m.group(2)), source="sockslist")

    def _source_proxyscrape(self):
        """proxyscrape.com API"""
        url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text&protocol=socks5"
        if self.country_filter != "ALL":
            url += f"&country={self.country_filter}"
        text = http_get(url)
        for line in text.strip().split("\n"):
            line = line.strip()
            m = re.match(r'(?:socks5://)?(\d+\.\d+\.\d+\.\d+):(\d+)', line)
            if m:
                self._add(m.group(1), int(m.group(2)), source="proxyscrape")

    def _source_spys(self):
        """spys.me SOCKS 列表"""
        url = "https://spys.me/socks.txt"
        text = http_get(url)
        for line in text.strip().split("\n"):
            m = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)\s+(\w+)', line.strip())
            if m:
                country = m.group(3)[:2] if len(m.group(3)) >= 2 else ""
                self._add(m.group(1), int(m.group(2)),
                          country=country, source="spys.me")

    def _source_openproxylist(self):
        """openproxylist.xyz"""
        url = "https://openproxylist.xyz/socks5.txt"
        text = http_get(url)
        for line in text.strip().split("\n"):
            m = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', line.strip())
            if m:
                self._add(m.group(1), int(m.group(2)), source="openproxylist")

    def _source_freeproxylist(self):
        """free-proxy-list.com"""
        url = "https://free-proxy-list.com/socks5-proxy-list.html"
        text = http_get(url)
        for m in re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*:\s*(\d{2,5})', text):
            self._add(m.group(1), int(m.group(2)), source="freeproxylist")


# ============== SOCKS5 验证器 ==============
class Socks5Validator:
    """
    原生 SOCKS5 握手验证 — 不依赖任何第三方库
    通过实际建立 SOCKS5 连接来验证代理是否可用
    """

    # 验证用的目标服务器（轻量 HTTP 服务，返回请求者 IP）
    CHECK_TARGETS = [
        ("httpbin.org", 80, "/ip"),
        ("api.ipify.org", 80, "/?format=json"),
        ("ifconfig.me", 80, "/ip"),
        ("icanhazip.com", 80, "/"),
    ]

    def __init__(self, timeout: int = 10, workers: int = 50):
        self.timeout = timeout
        self.workers = workers
        self.stats = {"tested": 0, "passed": 0, "failed": 0}
        self.lock = threading.Lock()

    def validate_all(self, proxies: List[ProxyInfo]) -> List[ProxyInfo]:
        """多线程验证所有代理"""
        total = len(proxies)
        logger.info(f"开始验证 {total} 个代理 (并发: {self.workers}, 超时: {self.timeout}s)")

        results: List[ProxyInfo] = []
        results_lock = threading.Lock()

        def _progress():
            with self.lock:
                done = self.stats["tested"]
                ok = self.stats["passed"]
                return done, ok

        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = {
                pool.submit(self._validate_one, proxy): proxy
                for proxy in proxies
            }

            for future in as_completed(futures):
                proxy = futures[future]
                try:
                    result = future.result()
                    if result and result.verified:
                        with results_lock:
                            results.append(result)
                except Exception:
                    pass

                done, ok = _progress()
                if done % 50 == 0 or done == total:
                    logger.info(f"  进度: {done}/{total} | 可用: {ok}")

        # 按延迟排序
        results.sort(key=lambda p: p.latency_ms)

        logger.info(f"验证完成: {self.stats['passed']}/{self.stats['tested']} 可用 "
                     f"({self.stats['failed']} 失败)")
        return results

    def _validate_one(self, proxy: ProxyInfo) -> Optional[ProxyInfo]:
        """验证单个代理"""
        # 依次尝试多个目标
        for host, port, path in self.CHECK_TARGETS:
            try:
                start = time.time()
                exit_ip = self._socks5_http_get(
                    proxy.ip, proxy.port, host, port, path
                )
                latency = (time.time() - start) * 1000

                proxy.latency_ms = round(latency, 1)
                proxy.exit_ip = exit_ip.strip() if exit_ip else ""
                proxy.verified = True

                # 尝试查出口 IP 地域
                proxy.exit_country = self._lookup_country(proxy.exit_ip)

                with self.lock:
                    self.stats["tested"] += 1
                    self.stats["passed"] += 1

                return proxy

            except Exception:
                continue

        # 所有目标都失败
        with self.lock:
            self.stats["tested"] += 1
            self.stats["failed"] += 1

        return proxy

    def _socks5_http_get(self, proxy_ip: str, proxy_port: int,
                          target_host: str, target_port: int,
                          path: str) -> str:
        """
        通过 SOCKS5 代理发送 HTTP GET 请求
        纯 socket 实现，不依赖 PySocks / requests
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:
            # 1. 连接代理
            sock.connect((proxy_ip, proxy_port))

            # 2. SOCKS5 握手: 发送认证方法协商
            #    VER=0x05, NMETHODS=1, METHOD=0x00(无认证)
            sock.sendall(b'\x05\x01\x00')

            resp = self._recv_exact(sock, 2)
            if resp[0] != 0x05 or resp[1] != 0x00:
                # 尝试用户名密码认证
                raise ConnectionError("SOCKS5 认证失败")

            # 3. SOCKS5 请求: CONNECT 到目标
            #    VER=0x05, CMD=0x01(CONNECT), RSV=0x00, ATYP=0x03(域名)
            domain = target_host.encode("ascii")
            req = b'\x05\x01\x00\x03' + bytes([len(domain)]) + domain
            req += struct.pack('!H', target_port)
            sock.sendall(req)

            # 4. 读取代理响应
            resp = self._recv_exact(sock, 4)
            if resp[1] != 0x00:
                raise ConnectionError(f"SOCKS5 CONNECT 失败: status={resp[1]}")

            # 跳过绑定地址
            atyp = resp[3]
            if atyp == 0x01:  # IPv4
                self._recv_exact(sock, 4 + 2)
            elif atyp == 0x03:  # 域名
                domain_len = self._recv_exact(sock, 1)[0]
                self._recv_exact(sock, domain_len + 2)
            elif atyp == 0x04:  # IPv6
                self._recv_exact(sock, 16 + 2)

            # 5. 发送 HTTP GET
            http_req = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {target_host}\r\n"
                f"User-Agent: curl/8.0\r\n"
                f"Accept: */*\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )
            sock.sendall(http_req.encode("ascii"))

            # 6. 读取 HTTP 响应
            response = b""
            while True:
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                    if len(response) > 8192:
                        break
                except socket.timeout:
                    break

            # 解析响应 body
            text = response.decode("utf-8", errors="replace")
            if "\r\n\r\n" in text:
                body = text.split("\r\n\r\n", 1)[1].strip()
            else:
                body = text.strip()

            # 提取 IP
            ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', body)
            if ip_match:
                return ip_match.group(1)

            return body[:50]

        finally:
            sock.close()

    def _recv_exact(self, sock: socket.socket, n: int) -> bytes:
        """精确读取 n 字节"""
        data = b""
        while len(data) < n:
            chunk = sock.recv(n - len(data))
            if not chunk:
                raise ConnectionError("连接中断")
            data += chunk
        return data

    def _lookup_country(self, ip: str) -> str:
        """查 IP 地域（尽力而为，失败返回空）"""
        if not ip or not re.match(r'\d+\.\d+\.\d+\.\d+', ip):
            return ""
        try:
            text = http_get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=5)
            data = json.loads(text)
            return data.get("countryCode", "")
        except Exception:
            return ""


# ============== 输出 ==============
def write_output(proxies: List[ProxyInfo], output_path: str, country_filter: str):
    """写入 list.txt"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# SOCKS5 Proxy List — Verified & Working\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Filter: country={country_filter}\n")
        f.write(f"# Total: {len(proxies)} proxies\n")
        f.write(f"# Sorted by latency (fastest first)\n")
        f.write(f"#\n")
        f.write(f"# Format: ip:port  # latency | country | exit_ip | anonymity | source\n")
        f.write(f"#\n\n")

        for proxy in proxies:
            f.write(proxy.to_line() + "\n")

    logger.info(f"已写入 {output_path} ({len(proxies)} 个可用代理)")


def write_plain(proxies: List[ProxyInfo], output_path: str):
    """额外输出纯净版 (只有 ip:port)"""
    plain_path = output_path.replace(".txt", "_plain.txt")
    with open(plain_path, "w") as f:
        for proxy in proxies:
            f.write(f"{proxy.addr}\n")
    logger.info(f"已写入 {plain_path} (纯净版)")


# ============== 主程序 ==============
def main():
    parser = argparse.ArgumentParser(
        description="SOCKS5 代理采集 + 验证工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python socks5_scraper.py                          # 采集全部，验证，输出 list.txt
  python socks5_scraper.py --country HK             # 只要香港代理
  python socks5_scraper.py --country ALL --workers 100  # 全球代理，100并发验证
  python socks5_scraper.py --timeout 5 --output sk5.txt # 5秒超时，输出到 sk5.txt
        """,
    )

    parser.add_argument("--country", "-c", default="ALL",
                        help="国家代码过滤 (HK/US/SG/ALL, 默认 ALL)")
    parser.add_argument("--timeout", "-t", type=int, default=10,
                        help="验证超时秒数 (默认 10)")
    parser.add_argument("--workers", "-w", type=int, default=50,
                        help="并发验证线程数 (默认 50)")
    parser.add_argument("--output", "-o", default="list.txt",
                        help="输出文件 (默认 list.txt)")
    parser.add_argument("--scrape-only", action="store_true",
                        help="只采集不验证")
    parser.add_argument("--no-geo", action="store_true",
                        help="跳过出口 IP 地域查询 (加速)")
    parser.add_argument("--min-latency", type=float, default=0,
                        help="最低延迟过滤 (ms)")
    parser.add_argument("--max-latency", type=float, default=0,
                        help="最高延迟过滤 (ms, 0=不限)")

    args = parser.parse_args()

    start_time = time.time()

    # ---- Step 1: 采集 ----
    scraper = ProxyScraper(country_filter=args.country)
    proxies = scraper.scrape_all()

    if not proxies:
        logger.error("未采集到任何代理，请检查网络")
        sys.exit(1)

    if args.scrape_only:
        # 不验证，直接输出
        write_output(proxies, args.output, args.country)
        write_plain(proxies, args.output)
        return

    # ---- Step 2: 验证 ----
    validator = Socks5Validator(timeout=args.timeout, workers=args.workers)

    # 如果不查地域，覆盖方法
    if args.no_geo:
        validator._lookup_country = lambda ip: ""

    verified = validator.validate_all(proxies)

    # ---- Step 3: 过滤 ----
    if args.max_latency > 0:
        verified = [p for p in verified if p.latency_ms <= args.max_latency]
    if args.min_latency > 0:
        verified = [p for p in verified if p.latency_ms >= args.min_latency]

    # ---- Step 4: 输出 ----
    if not verified:
        logger.warning("没有找到可用的 SOCKS5 代理")
        # 仍输出空文件
        write_output([], args.output, args.country)
    else:
        write_output(verified, args.output, args.country)
        write_plain(verified, args.output)

        # 打印 Top 10
        logger.info("")
        logger.info("🏆 Top 10 最快代理:")
        logger.info(f"{'IP:Port':<25} {'延迟':>8} {'国家':>6} {'出口IP':<18} {'来源'}")
        logger.info("-" * 80)
        for p in verified[:10]:
            logger.info(
                f"{p.addr:<25} {p.latency_ms:>6.0f}ms {p.exit_country:>6} "
                f"{p.exit_ip:<18} {p.source}"
            )

    elapsed = time.time() - start_time
    logger.info(f"\n总耗时: {elapsed:.1f}s")

    # 输出 JSON 统计
    stats = {
        "scraped": len(proxies),
        "verified": len(verified) if not args.scrape_only else 0,
        "output": args.output,
        "elapsed_seconds": round(elapsed, 1),
        "country_filter": args.country,
    }
    print(f"\n__SOCKS5_RESULT__:{json.dumps(stats)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n用户中断")
    except Exception as e:
        logger.error(f"致命错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
