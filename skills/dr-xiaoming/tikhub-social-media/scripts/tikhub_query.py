#!/usr/bin/env python3
"""TikHub API query helper. Handles auth, proxy, requests, and output formatting.

Usage:
    python3 tikhub_query.py <endpoint> [param=value ...] [--method POST] [--body '{}'] [--raw]

Examples:
    python3 tikhub_query.py /api/v1/douyin/web/fetch_search keyword=宁德时代
    python3 tikhub_query.py /api/v1/tiktok/web/fetch_user_profile secUid=MS4wLjABAAAA...
    python3 tikhub_query.py /api/v1/douyin/billboard/fetch_hot_search_list --method POST --body '{}'
    python3 tikhub_query.py /api/v1/hybrid/video_data url=https://v.douyin.com/xxx

Environment:
    TIKHUB_API_KEY  — API key (or set in .env next to SKILL.md)
    TIKHUB_PROXY    — HTTP proxy for requests (e.g. http://host:port)
                      Auto-detected from https_proxy/http_proxy if not set.
    TIKHUB_TIMEOUT  — Request timeout in seconds (default: 30)
"""

import sys, os, json, urllib.request, urllib.parse, urllib.error

BASE_URL = "https://api.tikhub.io"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

def get_api_key():
    """Get API key from env or .env file."""
    key = os.environ.get("TIKHUB_API_KEY")
    if key:
        return key
    env_path = os.path.join(SKILL_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("TIKHUB_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: TIKHUB_API_KEY not found. Set env var or create .env in skill root.", file=sys.stderr)
    sys.exit(1)

def get_proxy():
    """Get proxy URL. TikHub uses Cloudflare (172.67.x) which may need proxy."""
    proxy = os.environ.get("TIKHUB_PROXY")
    if proxy:
        return proxy
    # Check .env file
    env_path = os.path.join(SKILL_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("TIKHUB_PROXY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    # Auto-detect from standard env vars
    for var in ("https_proxy", "HTTPS_PROXY", "http_proxy", "HTTP_PROXY"):
        p = os.environ.get(var)
        if p:
            return p
    return None

def make_request(endpoint, params=None, method="GET", body=None, api_key=None):
    """Make API request and return parsed JSON."""
    url = f"{BASE_URL}{endpoint}"
    if params and method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "TikHub-Skill/1.0"
    }
    
    data = None
    if method == "POST":
        if body:
            data = body.encode("utf-8") if isinstance(body, str) else json.dumps(body).encode("utf-8")
        elif params:
            data = json.dumps(params).encode("utf-8")
    
    # Set up proxy handler
    proxy = get_proxy()
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({
            "https": proxy,
            "http": proxy
        })
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    timeout = int(os.environ.get("TIKHUB_TIMEOUT", "30"))
    
    try:
        with opener.open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(error_body)
        except:
            return {"code": e.code, "message": error_body}
    except Exception as e:
        return {"code": -1, "message": str(e)}

def print_summary(result):
    """Print a human-readable summary to stderr."""
    if not isinstance(result, dict):
        return
    code = result.get("code", "?")
    msg = result.get("message_zh") or result.get("message", "")
    cache = result.get("cache_url", "")
    
    if code != 200:
        print(f"\n⚠️  Code: {code} | {msg}", file=sys.stderr)
        return
    
    data = result.get("data")
    if isinstance(data, dict):
        # Try to count items from common response patterns
        for key in ("data", "items", "list", "aweme_list", "medias", "notes", 
                     "user_list", "comments", "statuses", "entries", "threads"):
            items = data.get(key)
            if isinstance(items, list):
                suffix = f" | Cache: {cache[:60]}..." if cache else ""
                print(f"\n✅ Success | Items ({key}): {len(items)}{suffix}", file=sys.stderr)
                return
        suffix = f" | Cache: {cache[:60]}..." if cache else ""
        print(f"\n✅ Success | Keys: {list(data.keys())[:8]}{suffix}", file=sys.stderr)
    elif isinstance(data, list):
        print(f"\n✅ Success | Items: {len(data)}", file=sys.stderr)
    else:
        print(f"\n✅ Success", file=sys.stderr)

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    
    endpoint = args[0]
    params = {}
    method = "GET"
    body = None
    raw = False
    
    i = 1
    while i < len(args):
        arg = args[i]
        if arg == "--method" and i + 1 < len(args):
            method = args[i + 1].upper()
            i += 2
        elif arg == "--body" and i + 1 < len(args):
            body = args[i + 1]
            i += 2
        elif arg == "--raw":
            raw = True
            i += 1
        elif "=" in arg:
            key, val = arg.split("=", 1)
            # Try to parse as number/bool
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            else:
                try:
                    val = int(val)
                except ValueError:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
            params[key] = val
            i += 1
        else:
            i += 1
    
    api_key = get_api_key()
    result = make_request(endpoint, params, method, body, api_key)
    
    if raw:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print_summary(result)

if __name__ == "__main__":
    main()
