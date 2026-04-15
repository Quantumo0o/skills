#!/usr/bin/env python3
"""
Cross-platform network scanner — no nmap required.
Works on WSL/Linux and Windows via Python sockets only.
Supports: host discovery, port scanning, service fingerprinting.
"""

import socket
import concurrent.futures
import struct
import random
import time
import ipaddress
import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── Data structures ──────────────────────────────────────────────────────────

@dataclass
class HostResult:
    ip: str
    hostname: Optional[str] = None
    is_alive: bool = False
    rtt_ms: Optional[float] = None
    ports: dict = field(default_factory=dict)  # port -> service info
    os_hints: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

@dataclass
class ScanResult:
    target: str
    scan_type: str  # "host-discovery" | "port-scan" | "full"
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    hosts: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    duration_s: float = 0.0

    def to_dict(self):
        return asdict(self)

# ─── Config ────────────────────────────────────────────────────────────────────

QUICK_PORTS     = [21, 22, 23, 25, 80, 443, 445, 3389, 8080]
COMMON_PORTS    = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
                   993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
TOP_PORTS_100   = [80, 443, 22, 21, 25, 3389, 110, 445, 139, 53, 135, 3306,
                   8080, 1723, 111, 995, 993, 5900, 1025, 587, 8888, 199, 1720,
                   465, 548, 113, 81, 38292, 3311, 3333, 49152, 1900, 3986,
                   13, 1027, 2000, 5666, 646, 2049, 88, 106, 2001, 3141, 4000,
                   5104, 5190, 3000, 543, 544, 5107, 144, 7, 389, 8000, 8008,
                   49154, 997, 1001, 5009, 5051, 5060, 5108, 5357, 49155, 1026,
                   6379, 6600, 6646, 7070, 7400, 7434, 7443, 8009, 8081, 8098]

HOST_DISCOVERY_PORTS = [80, 443, 22, 445, 3389, 21, 25, 8080]

TIMEOUT_DEFAULT = 1.5
TIMEOUT_UDP     = 2.0
MAX_THREADS      = 100
MAX_THREADS_HOST = 50

# ─── Platform helpers ──────────────────────────────────────────────────────────

def is_wsl() -> bool:
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except (FileNotFoundError, PermissionError):
        pass
    try:
        import ctypes
        ctypes.cdll.LoadLibrary("ntdll.dll")
        return False
    except OSError:
        return True

def get_local_networks() -> list:
    """Return local network prefixes (CIDR) for host discovery.
    Returns /24 subnets for detected interfaces, limited to 4 to avoid
    scanning huge ranges (e.g. Docker/WSL bridge networks)."""
    networks = []
    try:
        import subprocess
        result = subprocess.run(["ip", "-4", "addr", "show"],
                                capture_output=True, text=True, timeout=5)
        for line in result.stdout.split("\n"):
            if "inet " in line:
                ip = line.split("inet ")[1].split("/")[0]
                prefix = int(line.split("inet ")[1].split("/")[1].split()[0])
                # Skip link-local and loopback
                if ip.startswith(("127.", "169.254.")):
                    continue
                # Limit to /24 or smaller for practicality
                if prefix > 24:
                    prefix = 24
                try:
                    net = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
                    networks.append(str(net))
                except ValueError:
                    continue
    except Exception:
        pass

    if not networks:
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            networks.append(f"{local_ip.rsplit('.', 1)[0]}.0/24")
        except Exception:
            pass

    # Dedupe and limit to 4 networks max
    networks = list(dict.fromkeys(networks))[:4]
    return networks

# ─── Core scanning ─────────────────────────────────────────────────────────────

def probe_host(ip: str, timeout: float = TIMEOUT_DEFAULT) -> tuple[bool, Optional[float]]:
    """TCP probe — connect to multiple common ports. Returns (alive, rtt_ms)."""
    ports = HOST_DISCOVERY_PORTS
    start = time.perf_counter()
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((ip, port))
            sock.close()
            rtt = (time.perf_counter() - start) * 1000
            return True, round(rtt, 2)
        except (socket.timeout, socket.error, OSError):
            continue
    # Fallback: ICMP-like using UDP (may need admin)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.sendto(b"\x08\x00\x00\x00\x00\x00", (ip, 1))
        sock.close()
        rtt = (time.perf_counter() - start) * 1000
        return True, round(rtt, 2)
    except Exception:
        pass
    return False, None

def resolve_host(target: str) -> list[str]:
    """Resolve a target to a list of IPs. Handles IP, CIDR, hostname, URL."""
    ips = []
    target = target.strip().rstrip("/")
    # Strip protocol
    if "://" in target:
        target = target.split("://", 1)[1].split("/")[0]
    # IP range
    try:
        if "/" in target:
            network = ipaddress.ip_network(target, strict=False)
            return [str(h) for h in network.hosts()]
    except ValueError:
        pass
    # Single IP or hostname
    try:
        ipaddress.ip_address(target)
        return [target]
    except ValueError:
        pass
    # Hostname
    try:
        result = socket.getaddrinfo(target, None, socket.AF_INET)
        return sorted(set(r[4][0] for r in result))
    except socket.gaierror:
        return [target]  # Return as-is, let scan handle failure
    return [target]

def resolve_hostname(ip: str) -> Optional[str]:
    """Reverse DNS lookup."""
    try:
        name, _, _ = socket.gethostbyaddr(ip)
        return name
    except Exception:
        return None

def scan_port(ip: str, port: int, timeout: float = TIMEOUT_DEFAULT) -> Optional[dict]:
    """Attempt TCP connection to a port. Returns service info if open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        start = time.perf_counter()
        result = sock.connect_ex((ip, port))
        rtt = (time.perf_counter() - start) * 1000
        if result == 0:
            sock.close()
            banner = grab_banner(ip, port, timeout)
            return {
                "port": port,
                "state": "open",
                "rtt_ms": round(rtt, 2),
                "service": guess_service(port),
                "banner": banner
            }
        sock.close()
    except Exception:
        pass
    return None

def grab_banner(ip: str, port: int, timeout: float = 3.0) -> Optional[str]:
    """Grab service banner."""
    known_banners = {
        80:  b"HEAD / HTTP/1.0\r\n\r\n",
        443: b"HEAD / HTTP/1.0\r\n\r\n",
        8080: b"HEAD / HTTP/1.0\r\n\r\n",
    }
    probes = known_banners.get(port, b"")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        if probes:
            sock.send(probes)
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        if banner:
            return banner[:200]
    except Exception:
        pass
    return None

def guess_service(port: int) -> str:
    """Guess service name from port number."""
    try:
        return socket.getservbyport(port)
    except OSError:
        SERVICE_MAP = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
            53: "dns", 80: "http", 110: "pop3", 111: "rpcbind",
            135: "msrpc", 139: "netbios-ssn", 143: "imap",
            443: "https", 445: "microsoft-ds", 993: "imaps",
            995: "pop3s", 1433: "mssql", 1521: "oracle",
            1723: "pptp", 3306: "mysql", 3389: "rdp",
            5432: "postgresql", 5900: "vnc", 5901: "vnc",
            6379: "redis", 8080: "http-proxy", 8443: "https-alt",
            8888: "http-alt", 27017: "mongodb",
        }
        return SERVICE_MAP.get(port, f"port-{port}")

def tcp_connect_scan(ip: str, ports: list[int], timeout: float = TIMEOUT_DEFAULT,
                     workers: int = MAX_THREADS) -> dict:
    """Concurrent TCP connect scan."""
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_port, ip, p, timeout): p for p in ports}
        for fut in concurrent.futures.as_completed(futures):
            port = futures[fut]
            try:
                res = fut.result()
                if res:
                    results[port] = res
            except Exception:
                pass
    return results

def discover_hosts(targets: list[str], timeout: float = TIMEOUT_DEFAULT,
                   workers: int = MAX_THREADS_HOST) -> list[HostResult]:
    """Host discovery — ping/probe each target."""
    all_ips = set()
    for t in targets:
        all_ips.update(resolve_host(t))

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(probe_host, ip, timeout): ip for ip in sorted(all_ips)}
        for fut in concurrent.futures.as_completed(futures):
            ip = futures[fut]
            try:
                alive, rtt = fut.result()
                hostname = resolve_hostname(ip) if alive else None
                results.append(HostResult(ip=ip, hostname=hostname,
                                          is_alive=alive, rtt_ms=rtt))
            except Exception as e:
                results.append(HostResult(ip=ip, is_alive=False))
    return results

def full_scan(targets: list[str], depth: str = "normal",
              timeout: float = TIMEOUT_DEFAULT) -> ScanResult:
    """
    Full scan: host discovery + port scan + service detection.
    depth: quick | normal | intense
    """
    start = time.perf_counter()
    scan_type = f"full-{depth}"
    errors = []

    # Choose port list
    port_map = {
        "quick":   QUICK_PORTS,
        "normal":  COMMON_PORTS,
        "intense": TOP_PORTS_100,
    }
    ports = port_map.get(depth, COMMON_PORTS)

    # 1. Host discovery
    hosts = discover_hosts(targets, timeout=timeout)
    alive_hosts = [h for h in hosts if h.is_alive]

    # 2. Port scan + service detection on alive hosts
    for h in alive_hosts:
        h.ports = tcp_connect_scan(h.ip, ports, timeout=timeout)

    # 3. OS hints based on open ports
    for h in alive_hosts:
        open_ports = list(h.ports.keys())
        h.os_hints = os_guess(open_ports)

    duration = time.perf_counter() - start
    return ScanResult(
        target=", ".join(targets),
        scan_type=scan_type,
        hosts=[h for h in hosts if h.is_alive],
        errors=errors,
        duration_s=round(duration, 2)
    )

def os_guess(open_ports: list[int]) -> list[str]:
    """Crude OS fingerprinting based on open port patterns."""
    hints = []
    if 3389 in open_ports and 445 in open_ports:
        hints.append("Windows (RDP + SMB)")
    elif 22 in open_ports and 80 in open_ports:
        hints.append("Linux/Unix (SSH + HTTP)")
    elif 445 in open_ports and 139 in open_ports and 3389 in open_ports:
        hints.append("Windows Server")
    elif 80 in open_ports or 443 in open_ports or 8080 in open_ports:
        hints.append("Web-facing host")
    if 21 in open_ports:
        hints.append("FTP server")
    if 23 in open_ports:
        hints.append("Telnet (insecure!)")
    if 3306 in open_ports or 5432 in open_ports or 6379 in open_ports:
        hints.append("Database server")
    return hints


def get_gateway_ip() -> Optional[str]:
    """Detect default gateway IP."""
    try:
        import subprocess
        result = subprocess.run(["ip", "route", "show", "default"],
                               capture_output=True, text=True, timeout=5)
        for line in result.stdout.strip().split("\n"):
            if line.startswith("default via"):
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == "via" and i + 1 < len(parts):
                        return parts[i + 1]
    except Exception:
        pass
    return None


def get_local_ip() -> Optional[str]:
    """Get the local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

# ─── Formatters ────────────────────────────────────────────────────────────────

def format_discord(results: list[HostResult], target: str,
                   scan_type: str, duration: float) -> str:
    """Format scan results for Discord — compact, color-coded with emojis."""
    lines = [
        f"**🔍 Scan Report — `{target}`**",
        f"> Type: `{scan_type}` | Duration: `{duration:.1f}s`",
        ""
    ]
    if not results:
        lines.append("> _No live hosts detected._")
        return "\n".join(lines)

    for h in results:
        emoji = "🟢" if h.is_alive else "⚫"
        rtt_str = f" `{h.rtt_ms}ms`" if h.rtt_ms else ""
        host_str = f"**{emoji} {h.ip}**"
        if h.hostname:
            host_str += f" — `{h.hostname}`"
        host_str += rtt_str
        lines.append(host_str)

        if h.os_hints:
            hints = " · ".join(f"`{p}`" for p in h.os_hints[:3])
            lines.append(f"   └ OS: {hints}")

        if h.ports:
            port_lines = []
            for p_info in sorted(h.ports.values(), key=lambda x: x["port"])[:10]:
                port = p_info["port"]
                service = p_info.get("service", "unknown")
                state = p_info["state"]
                banner = p_info.get("banner", "")
                banner_str = f" — {banner[:60]}" if banner else ""
                port_lines.append(f"  `{port:>5}` {service:<12} {state}{banner_str}")
            if len(h.ports) > 10:
                port_lines.append(f"  _...and `{len(h.ports) - 10}` more ports_")
            lines.extend(port_lines)
        lines.append("")  # blank line between hosts

    return "\n".join(lines).strip()

def format_json(result: ScanResult) -> str:
    return json.dumps(result.to_dict(), indent=2)

# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Network Scanner")
    parser.add_argument("target", nargs="?", help="IP, CIDR, hostname, or URL")
    parser.add_argument("--depth", choices=["quick", "normal", "intense"], default="normal",
                        help="Scan depth (default: normal)")
    parser.add_argument("--timeout", type=float, default=TIMEOUT_DEFAULT,
                        help=f"Socket timeout seconds (default: {TIMEOUT_DEFAULT})")
    parser.add_argument("--format", choices=["discord", "json", "simple"], default="discord",
                        help="Output format")
    parser.add_argument("--local", action="store_true",
                        help="Scan all local network ranges (full /24 per interface, slow)")
    parser.add_argument("--local-scan", action="store_true",
                        help="Fast local scan: gateway + nearby IPs")
    args = parser.parse_args()

    targets = []
    if args.local:
        targets = get_local_networks()
    elif args.local_scan:
        local_ip = get_local_ip()
        gateway = get_gateway_ip()
        targets = []
        if local_ip:
            subnet = ".".join(local_ip.split(".")[:3])
            # Gateway
            if gateway:
                targets.append(gateway)
            # Local host
            targets.append(local_ip)
            # Common low-numbered addresses on subnet
            for i in [1, 2, 3, 100, 101, 254]:
                ip = f"{subnet}.{i}"
                if ip != local_ip and ip != gateway:
                    targets.append(ip)
        targets = list(dict.fromkeys(targets))
    elif args.target:
        targets = [args.target]
    else:
        print("Error: specify a target or use --local / --local-scan")
        sys.exit(1)

    if not targets:
        print("No targets specified.")
        sys.exit(1)

    result = full_scan(targets, depth=args.depth, timeout=args.timeout)

    if args.format == "discord":
        print(format_discord(result.hosts, result.target, result.scan_type, result.duration_s))
    elif args.format == "json":
        print(format_json(result))
    else:
        for h in result.hosts:
            print(f"{h.ip} [{h.rtt_ms}ms] {h.hostname or ''}")
            for p, info in sorted(h.ports.items()):
                print(f"  {p}/{info['service']} {info['state']}")

if __name__ == "__main__":
    main()
