import os
import requests

# 复用你成功的飞书发送函数（纯文本版，稳定）
def send_feishu_text(webhook_url: str, text: str):
    data = {
        "msg_type": "text",
        "content": {"text": text}
    }
    response = requests.post(webhook_url, json=data)
    print(f"飞书发送状态: {response.status_code} - {response.text[:100]}")
    return response.status_code == 200


def extract_action_items(transcript: str) -> str:
    """
    简单行动项提取（实际商用可替换成 LLM 调用，如 Claude/Grok API）
    这里用规则模拟，真实场景用 LLM 更准
    """
    lines = transcript.split("\n")
    actions = []
    for line in lines:
        if any(word in line.lower() for word in ["明天", "本周", "下周", "完成", "准备", "跟进"]):
            actions.append(f"• [ ] {line.strip()}")
    if not actions:
        return "本次会议无明确行动项。"
    return "**会议行动项**\n" + "\n".join(actions[:5])  # 限制前5条


def process_meeting(transcript: str = None):
    """核心处理：转录 → 提取 → 推送飞书"""
    print("🚀 MeetingOS 开始处理会议...")
    
    if not transcript:
        transcript = """
用户：张三，明天把PRD文档写完。
用户：李四，本周五前准备好销售PPT。
用户：王五，下周一跟进客户反馈。
        """  # 测试用默认转录
    
    # 提取行动项
    action_summary = extract_action_items(transcript)
    print("提取到的行动项：\n" + action_summary)
    
    # 发送到飞书
    webhook = os.getenv("FEISHU_WEBHOOK_URL")
    if webhook:
        success = send_feishu_text(webhook, f"会议总结：\n{action_summary}")
        if success:
            print("✅ 行动项已成功推送到飞书群！")
        else:
            print("❌ 推送失败，请检查 Webhook")
    else:
        print("⚠️ 未配置 FEISHU_WEBHOOK_URL")


if __name__ == "__main__":
    process_meeting()  # 直接运行测试