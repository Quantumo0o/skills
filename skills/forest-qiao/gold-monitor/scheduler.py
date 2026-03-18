"""定时任务调度 — 每60秒拉取价格并检查报警"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from data_fetcher import fetch_all
from alert_manager import check_alerts

logger = logging.getLogger(__name__)

_scheduler = None


def _job():
    """定时任务：拉取价格 + 检查报警"""
    try:
        prices = fetch_all()
        logger.info("价格更新完成: %d 个品种", len(prices))
        check_alerts(prices)
    except Exception as e:
        logger.error("定时任务异常: %s", e)


def start():
    global _scheduler
    if _scheduler and _scheduler.running:
        return
    _scheduler = BackgroundScheduler()
    _scheduler.add_job(_job, "interval", seconds=60, id="price_fetch", replace_existing=True)
    _scheduler.start()
    logger.info("定时调度已启动 (每60秒)")
    # 启动时立即执行一次
    _job()


def stop():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("定时调度已停止")
