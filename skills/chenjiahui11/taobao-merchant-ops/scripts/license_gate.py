#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import platform
import time
import uuid
from pathlib import Path
from typing import Any


LICENSE_PREFIX = "TMO1"
MASTER_SECRET = os.environ.get(
    "TMO_MASTER_SECRET", "715aff55c00443469726f2007efd244ddb01d28f91dd7d9771586c12f0ef5755"
)


def _b64u_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64u_decode(text: str) -> bytes:
    pad = "=" * ((4 - len(text) % 4) % 4)
    return base64.urlsafe_b64decode((text + pad).encode("ascii"))


def machine_fingerprint() -> str:
    node = platform.node() or ""
    system = platform.system() or ""
    machine = platform.machine() or ""
    mac = str(uuid.getnode())
    raw = f"{node}|{system}|{machine}|{mac}".encode("utf-8", errors="ignore")
    return hashlib.sha256(raw).hexdigest()[:24]


def _sign_payload(payload_b64: str) -> str:
    sig = hmac.new(
        MASTER_SECRET.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return _b64u_encode(sig[:18])


def parse_and_verify_key(card_key: str) -> dict[str, Any]:
    parts = (card_key or "").strip().split(".")
    if len(parts) != 3:
        raise ValueError("卡密格式错误")
    prefix, payload_b64, sig = parts
    if prefix != LICENSE_PREFIX:
        raise ValueError("卡密前缀错误")
    if not hmac.compare_digest(_sign_payload(payload_b64), sig):
        raise ValueError("卡密签名无效")
    payload = json.loads(_b64u_decode(payload_b64).decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("卡密载荷类型错误")
    return payload


def _activation_seal(data: dict[str, Any]) -> str:
    body = {k: v for k, v in data.items() if k != "seal"}
    text = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _b64u_encode(
        hmac.new(MASTER_SECRET.encode("utf-8"), text.encode("utf-8"), hashlib.sha256).digest()[:18]
    )


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _derive_expire_ts(payload: dict[str, Any], activated_at: int) -> int:
    if payload.get("exp") is not None:
        return int(payload["exp"])
    if payload.get("days") is not None:
        return activated_at + int(payload["days"]) * 86400
    plan = str(payload.get("plan") or "").lower().strip()
    days_map = {"day": 1, "month": 30, "year": 365}
    return activated_at + days_map.get(plan, 1) * 86400


def _fmt_ts(ts: int) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts)))


def ensure_license(license_file: Path, key_from_cli: str = "") -> dict[str, Any]:
    now = int(time.time())
    fp = machine_fingerprint()
    act = _load_json(license_file)
    if act:
        if str(act.get("seal") or "") != _activation_seal(act):
            raise SystemExit("授权文件已损坏或被篡改，请重新激活。")
        if str(act.get("machine_fp") or "") != fp:
            raise SystemExit("授权绑定到其他机器，请使用本机卡密重新激活。")
        if int(act.get("expires_at") or 0) <= now:
            raise SystemExit(f"卡密已过期（到期时间: {_fmt_ts(int(act.get('expires_at') or 0))}）")
        return act

    key = (key_from_cli or "").strip()
    if not key:
        print("未发现授权文件，请输入卡密（支持日卡/月卡/年卡）：")
        key = input("Card Key: ").strip()
    if not key:
        raise SystemExit("未输入卡密，已退出。")

    payload = parse_and_verify_key(key)
    nbf = int(payload.get("nbf") or 0)
    if nbf and now < nbf:
        raise SystemExit(f"卡密未到生效时间（生效时间: {_fmt_ts(nbf)}）")

    expires_at = _derive_expire_ts(payload, now)
    if expires_at <= now:
        raise SystemExit("卡密已过期，无法激活。")

    act = {
        "version": 1,
        "key": key,
        "plan": str(payload.get("plan") or "custom"),
        "machine_fp": fp,
        "activated_at": now,
        "expires_at": int(expires_at),
    }
    act["seal"] = _activation_seal(act)
    _save_json(license_file, act)
    print(f"授权激活成功，方案: {act['plan']}，到期: {_fmt_ts(act['expires_at'])}")
    return act

