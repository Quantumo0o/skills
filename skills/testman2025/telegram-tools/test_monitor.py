
import asyncio
from tg_monitor_kit.monitor import run_monitor

if __name__ == '__main__':
    try:
        asyncio.run(run_monitor())
    except KeyboardInterrupt:
        print("\n✅ 监控已停止")
