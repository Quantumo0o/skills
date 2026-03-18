"""FastAPI 主应用 — 黄金监控面板"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

import data_fetcher
import alert_manager
import scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(title="黄金监控面板")
templates = Jinja2Templates(directory="templates")


class AlertRule(BaseModel):
    symbol: str
    condition: str  # price_above / price_below / change_pct_above / change_pct_below
    threshold: float
    note: str = ""


class WebhookConfig(BaseModel):
    url: str


class TestNotification(BaseModel):
    webhook_url: str = ""


# ─── 页面 ───

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ─── 数据 API ───

@app.get("/api/prices")
async def api_prices():
    return data_fetcher.get_cached_prices()


@app.get("/api/history/{symbol}")
async def api_history(symbol: str, period: str = "1mo"):
    return data_fetcher.get_history(symbol, period)


# ─── 报警 API ───

@app.get("/api/alerts")
async def api_get_alerts():
    return {
        "alerts": alert_manager.get_alerts(),
        "webhook_url": alert_manager.get_webhook_url(),
    }


@app.post("/api/alerts")
async def api_add_alert(rule: AlertRule):
    created = alert_manager.add_alert(rule.model_dump())
    return {"ok": True, "alert": created}


@app.delete("/api/alerts/{rule_id}")
async def api_delete_alert(rule_id: str):
    deleted = alert_manager.delete_alert(rule_id)
    return {"ok": deleted}


@app.post("/api/webhook")
async def api_set_webhook(config: WebhookConfig):
    alert_manager.set_webhook_url(config.url)
    return {"ok": True}


@app.post("/api/alerts/test")
async def api_test_notification(body: TestNotification):
    url = body.webhook_url or alert_manager.get_webhook_url()
    if not url:
        return {"ok": False, "message": "未配置飞书Webhook URL"}
    ok = alert_manager.send_test_notification(url)
    return {"ok": ok, "message": "发送成功" if ok else "发送失败"}


# ─── 启动/关闭 ───

@app.on_event("startup")
async def on_startup():
    scheduler.start()


@app.on_event("shutdown")
async def on_shutdown():
    scheduler.stop()


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
