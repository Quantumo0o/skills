#!/usr/bin/env python3
"""
通用工具模块
提供重试装饰器、缓动函数等工具
"""

import functools
import time
import logging
from typing import Callable, TypeVar, ParamSpec

logger = logging.getLogger(__name__)

P = ParamSpec('P')
T = TypeVar('T')


def retry(attempts: int = 3, delay: float = 1.0, backoff: float = 2.0,
          exceptions: tuple = (Exception,), logger_name: str = None):
    """
    重试装饰器

    Args:
        attempts: 最大重试次数 (默认 3)
        delay: 初始等待秒数 (默认 1.0)
        backoff: 退避乘数 (默认 2.0, 即 1s -> 2s -> 4s)
        exceptions: 需要捕获的异常类型 (默认所有)
        logger_name: 日志记录器名 (默认使用模块 logger)

    Returns:
        装饰器函数

    Example:
        @retry(attempts=3, delay=1, backoff=2)
        def fetch_data():
            return requests.get(url)

        @retry(attempts=5, delay=0.5, exceptions=(TimeoutError, ConnectionError))
        def fragile_operation():
            ...
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            _log = logging.getLogger(logger_name or func.__module__)
            last_exception = None

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < attempts - 1:
                        wait_time = delay * (backoff ** attempt)
                        _log.debug(
                            f"[{func.__name__}] 第 {attempt + 1}/{attempts} 次失败: {e}, "
                            f"{wait_time:.1f}s 后重试..."
                        )
                        time.sleep(wait_time)
                    else:
                        _log.warning(
                            f"[{func.__name__}] 第 {attempt + 1}/{attempts} 次失败，已放弃: {e}"
                        )
            raise last_exception
        return wrapper
    return decorator


# ========== 缓动函数（用于滑块轨迹防检测）==========

def ease_out_quad(t: float) -> float:
    """缓出二次方（先快后慢）"""
    return -t * (t - 2)


def ease_in_out_quad(t: float) -> float:
    """缓入缓出二次方"""
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t


def ease_out_cubic(t: float) -> float:
    """缓出三次方"""
    return 1 - pow(1 - t, 3)


def ease_out_quart(t: float) -> float:
    """缓出四次方"""
    return 1 - pow(1 - t, 4)


def generate_slider_track(distance: float, steps: int = 30,
                           ease_func: Callable[[float], float] = ease_out_quad):
    """
    生成滑块拖动轨迹（带缓动）

    Args:
        distance: 总距离（像素）
        steps: 步数
        ease_func: 缓动函数

    Returns:
        List[Tuple[float, float]]: (x, y) 轨迹列表
    """
    track = []
    for i in range(steps):
        t = i / steps
        x = distance * ease_func(t)
        # 模拟轻微垂直波动（人不是完美水平拖动）
        y = (hash(i) % 3 - 1) * 0.5
        track.append((round(x, 2), round(y, 2)))
    return track
