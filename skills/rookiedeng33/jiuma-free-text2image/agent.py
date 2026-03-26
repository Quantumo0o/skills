#!/usr/bin/env python3
"""
九码AI图片生成简单版
输入提示词，生成图片并返回URL
"""

import json
import sys
import time
import requests

SUBMIT_API = "https://api.jiuma.com/gpt/text2image"
WAITING_API = "https://api.jiuma.com/gpt/get_text2image_result"


def output_result(json_data):
    """输出JSON格式结果"""
    print(json.dumps(json_data, ensure_ascii=False, indent=2))


def main(text):
    """主函数：生成图片"""
    print(f"文本到图片: {text}")

    # 1. 提交生成请求
    try:
        response = requests.post(SUBMIT_API, {"text": text}, timeout=30)
        if response.status_code != 200:
            output_result({
                "error": response.status_code,
                "message": "请求远程API失败",
                "data": {}
            })
            return

        json_result = response.json()
        task_id = json_result.get("task_id")

        if not task_id:
            output_result({
                "error": "no_task_id",
                "message": "API未返回任务ID",
                "data": json_result
            })
            return

        print(f"任务已提交，任务ID: {task_id}")

    except requests.exceptions.RequestException as e:
        output_result({
            "error": "request_error",
            "message": f"请求异常: {str(e)}",
            "data": {}
        })
        return

    # 2. 轮询等待结果
    max_attempts = 30  # 最多尝试30次
    attempt = 0
    image_url = ""

    while attempt < max_attempts:
        attempt += 1
        print(f"查询进度... ({attempt}/{max_attempts})")

        try:
            waiting_response = requests.post(WAITING_API, {"task_id": task_id}, timeout=30)

            if waiting_response.status_code != 200:
                print(f"查询失败: HTTP {waiting_response.status_code}")
                time.sleep(5)
                continue

            waiting_result = waiting_response.json()
            code = waiting_result.get("code")

            if code == 200:
                # 成功获取图片URL
                data = waiting_result.get("data", {})
                image_url = data.get("image_url")
                if image_url:
                    output_result({
                        "status": "success",
                        "message": "图片生成成功",
                        "data": {
                            "image_url": image_url,
                            "task_id": task_id,
                            "attempts": attempt
                        }
                    })
                    return
                else:
                    print("API返回成功但没有图片URL")
            else:
                # 处理其他状态码
                status = waiting_result.get("status", "unknown")
                if status == "failed":
                    error_msg = waiting_result.get("error", "未知错误")
                    output_result({
                        "status": "failed",
                        "message": f"图片生成失败: {error_msg}",
                        "data": {
                            "task_id": task_id,
                            "error": error_msg
                        }
                    })
                    return
                elif status == "pending":
                    # 继续等待
                    pass
                else:
                    print(f"未知状态: {status}")

            # 等待5秒后继续查询
            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"查询异常: {e}")
            time.sleep(5)

    # 达到最大尝试次数
    output_result({
        "status": "timeout",
        "message": f"等待超时（{max_attempts}次尝试）",
        "data": {
            "task_id": task_id,
            "max_attempts": max_attempts
        }
    })


if __name__ == '__main__':
    # 检查参数
    if len(sys.argv) < 2:
        print("使用方法: python simple_jiuma_gen.py \"你的提示词\"")
        print("示例: python simple_jiuma_gen.py \"一只可爱的猫咪\"")
        sys.exit(1)

    # 获取提示词
    prompt = sys.argv[1]

    # 运行主函数
    main(prompt)