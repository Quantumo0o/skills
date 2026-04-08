#!/usr/bin/env python3
# 模拟 Skill 内部调用

import subprocess
import sys

def notify_skill_complete(task_name, result):
    """Skill 完成任务后调用通知"""
    subprocess.run([
        "/opt/feishu-notifier/bin/notify",
        f"✅ Skill完成: {task_name}",
        f"处理结果: {result}"
    ], check=False)

def notify_skill_error(task_name, error):
    """Skill 出错时调用通知"""
    subprocess.run([
        "/opt/feishu-notifier/bin/notify",
        f"❌ Skill错误: {task_name}",
        f"错误信息: {error}"
    ], check=False)

# 模拟执行
if __name__ == "__main__":
    notify_skill_complete("文献下载", "成功下载 5 篇文献")
    print("Skill 通知已发送")
