"""
SDK 客户端初始化公共模块。

环境变量要求:
  FSOPENAPI_SERVER_PUBLIC_KEY  - 服务端公钥 (PEM 或纯 base64)
  FSOPENAPI_CLIENT_PRIVATE_KEY - 客户端私钥 (PEM 或纯 base64)
  FSOPENAPI_BASE_URL           - 网关地址 (可选, 默认 https://openapi.fosunxcz.com)
  FSOPENAPI_API_KEY            - API Key (可选, 也可通过 --api-key 传入)
"""

import base64
import json
import os
import sys

_WORKSPACE_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))


def _parse_env_file(text):
    """解析 .env 文件内容，支持多行 PEM 密钥。"""
    result = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        key, sep, val = line.partition("=")
        if not sep:
            i += 1
            continue
        key, val = key.strip(), val.strip()
        if val.startswith("-----BEGIN "):
            pem_lines = [val]
            i += 1
            while i < len(lines):
                pem_line = lines[i].rstrip()
                pem_lines.append(pem_line)
                if pem_line.strip().startswith("-----END "):
                    i += 1
                    break
                i += 1
            val = "\n".join(pem_lines)
        else:
            i += 1
        if key:
            result[key] = val
    return result


_PEM_WRAPPERS = {
    "FSOPENAPI_CLIENT_PRIVATE_KEY": ("-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----"),
    "FSOPENAPI_SERVER_PUBLIC_KEY": ("-----BEGIN PUBLIC KEY-----", "-----END PUBLIC KEY-----"),
}


def _ensure_pem(key_name, value):
    """将各种密钥格式统一为标准 PEM。

    支持三种输入:
      1. 完整 PEM（已有头尾标记）→ 原样返回
      2. 整个 PEM 被 base64 编码了一次 → 解码后得到完整 PEM
      3. 纯密钥 base64（无头尾）→ 补全 PEM 头尾
    """
    value = value.strip()
    if not value or value.startswith("-----BEGIN "):
        return value
    wrapper = _PEM_WRAPPERS.get(key_name)
    if not wrapper:
        return value
    # 尝试 base64 解码，看是否是对完整 PEM 做了一次编码
    try:
        decoded = base64.b64decode(value).decode("utf-8")
        if decoded.strip().startswith("-----BEGIN "):
            return decoded.strip()
    except Exception:
        pass
    # 纯密钥 base64，补全 PEM 头尾
    begin, end = wrapper
    raw = value.replace("\n", "").replace("\r", "").replace(" ", "")
    lines = [raw[i:i+64] for i in range(0, len(raw), 64)]
    return begin + "\n" + "\n".join(lines) + "\n" + end


def _try_load_credentials():
    """从 fosun.env 加载凭证到环境变量（支持多行 PEM 密钥和纯 base64）。"""
    p = os.path.join(_WORKSPACE_ROOT, "fosun.env")
    if not os.path.isfile(p):
        return False
    with open(p) as f:
        entries = _parse_env_file(f.read())
    for key, val in entries.items():
        if not os.environ.get(key):
            os.environ[key] = _ensure_pem(key, val)
    return True


def get_client(api_key=None, base_url=None):
    """返回已初始化的 SDKClient 实例。"""
    _try_load_credentials()

    try:
        from fsopenapi import SDKClient
    except ImportError:
        print("错误：fsopenapi SDK 未安装。请先在既有环境中执行:", file=sys.stderr)
        print("  /Users/admin/.openclaw/workspace/.venv-fosun/bin/pip install -e /Users/admin/.openclaw/workspace/skills/fosun_skills/fosun-sdk-setup/openapi-sdk", file=sys.stderr)
        print("禁止新建虚拟环境；请复用 workspace .venv-fosun", file=sys.stderr)
        sys.exit(1)

    resolved_base_url = base_url or os.getenv("FSOPENAPI_BASE_URL", "https://openapi-sit.fosunxcz.com")
    resolved_api_key = api_key or os.getenv("FSOPENAPI_API_KEY")

    if not resolved_api_key:
        print("错误: 缺少 API Key。请通过 --api-key 参数或 FSOPENAPI_API_KEY 环境变量提供。", file=sys.stderr)
        sys.exit(1)

    return SDKClient(resolved_base_url, resolved_api_key)


def get_sub_account_id(client):
    """获取第一个子账户 ID。"""
    accounts = client.account.list_accounts()
    data = accounts.get("data", accounts)
    subs = data.get("subAccounts", [])
    if not subs:
        print("错误: 未找到子账户。", file=sys.stderr)
        sys.exit(1)
    return subs[0]["subAccountId"]


def dump_json(data):
    """格式化输出 JSON。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def add_common_args(parser):
    """添加所有脚本共用的 CLI 参数。"""
    parser.add_argument("--api-key", help="Fosun API Key (或设置 FSOPENAPI_API_KEY 环境变量)")
    parser.add_argument("--base-url", help="网关地址 (或设置 FSOPENAPI_BASE_URL 环境变量)")
    parser.add_argument("--sub-account-id", help="子账户 ID (不传则自动获取第一个)")
