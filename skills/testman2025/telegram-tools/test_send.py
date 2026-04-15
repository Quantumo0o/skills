
import asyncio
import os
import shutil
import uuid
from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config

async def test_send():
    cfg = load_config()
    # 使用临时会话避免锁冲突
    original_session = cfg.session_file
    temp_session = f"{original_session.rsplit('.', 1)[0]}_test_{uuid.uuid4().hex[:8]}.session"
    shutil.copy2(original_session, temp_session)
    cfg.session_file = temp_session
    try:
        client = build_client(cfg)
        await client.start()
        print("客户端已连接，正在发送测试消息到Saved Messages...")
        # 发送测试消息
        await client.send_message('me', "✅ 测试消息：TG工具推送功能验证", link_preview=False)
        print("✅ 测试消息已成功发送，请检查收藏会话")
        await client.disconnect()
    except Exception as e:
        print(f"❌ 发送失败，错误信息：{str(e)}")
    finally:
        # 清理临时文件
        if os.path.exists(temp_session):
            os.remove(temp_session)
        if os.path.exists(f"{temp_session}-journal"):
            os.remove(f"{temp_session}-journal")

if __name__ == "__main__":
    asyncio.run(test_send())
