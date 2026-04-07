#!/usr/bin/env python3
"""
Lite 冒烟：用 httpx ASGITransport（兼容 httpx 0.28+）验证核心路由。
运行：仓库根目录  python scripts/smoke_lite.py
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import httpx
from httpx import ASGITransport

from admin.app import app


async def _run() -> None:
    async with ASGITransport(app=app) as transport:
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
            r = await c.get("/lite")
            assert r.status_code == 200, r.status_code
            body = r.text
            assert "CommunityOS Lite" in body
            assert "main-tabs" in body

            r = await c.get("/api/health")
            assert r.status_code == 200
            assert r.json().get("ok") is True

            r = await c.get("/api/bots")
            assert r.status_code == 200
            j = r.json()
            assert j.get("ok") is True
            assert isinstance(j.get("bots"), list)

            r = await c.get("/api/dashboard")
            assert r.status_code == 200
            j = r.json()
            assert j.get("ok") is True
            assert "stats" in j

            r = await c.get("/api/llm-config")
            assert r.status_code == 200
            assert r.json().get("ok") is True


def main() -> None:
    asyncio.run(_run())
    print("smoke_lite: OK (/lite, /api/health, /api/bots, /api/dashboard, /api/llm-config)")


if __name__ == "__main__":
    main()
