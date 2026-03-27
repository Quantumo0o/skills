#!/usr/bin/env python3
"""
ABA-智能查询 - LinkFox Skill
调用 aba/intelligentQuery 接口

用法:
  python aba_query.py '{"analysisDescription": "筛选美国站，关键词gift在过去12周的搜索热度排名", "region": "US"}'
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


API_URL = "https://test-tool-gateway.linkfox.com/aba/intelligentQuery"


def get_api_key():
    """获取 API Key，缺失时友好提示。"""
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "尚未配置 API Key，请先完成授权：\n"
            "1. 访问 https://yxgb3sicy7.feishu.cn/wiki/GIkkweGghiyzkqkRXQKc2n0Tnre 获取 Key\n"
            "2. 设置环境变量: export LINKFOXAGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api(params: dict) -> dict:
    """调用工具网关 API。"""
    api_key = get_api_key()
    data = json.dumps(params).encode("utf-8")

    req = Request(
        API_URL,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-Skill/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"连接失败: {e.reason}"}


def main():
    if len(sys.argv) < 2:
        print("用法: aba_query.py '<JSON参数>'", file=sys.stderr)
        print(
            '示例: aba_query.py \'{"analysisDescription": "筛选美国站，关键词gift在过去12周的搜索热度排名", "region": "US"}\'',
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"参数格式错误: {e}", file=sys.stderr)
        sys.exit(1)

    result = call_api(params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
