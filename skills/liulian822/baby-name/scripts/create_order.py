import sys
import json
import hashlib
import os
import urllib.request
import urllib.error

from file_utils import save_order

CREATE_ORDER_URL = "https://ms.jr.jd.com/gw2/generic/hyqy/na/m/createOrder"

# 获取技能目录
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(os.path.dirname(SKILL_DIR), "configs", "config.json")


def load_config():
    """从配置文件加载用户配置"""
    if not os.path.isfile(CONFIG_FILE):
        raise RuntimeError(f"配置文件不存在: {CONFIG_FILE}，请先配置您的收款方信息")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_indicator(slug: str) -> str:
    """根据 slug 计算 MD5 作为 indicator。"""
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def create_order(question: str, pay_to: str, amount: int, description: str) -> tuple:
    """
    POST the user's question to the createOrder endpoint.
    Returns (order_no, amount, encrypted_data, pay_to) on success, or raises RuntimeError on failure.
    """
    pay_data_dict = {
        "reqData": {
            "question": question,
            "payTo": pay_to,
            "amount": amount,
            "description": description,
        }
    }
    payload = json.dumps(pay_data_dict).encode("utf-8")
    req = urllib.request.Request(
        CREATE_ORDER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode("utf-8")).get("resultData")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求异常，请确认网络链接并稍后重试: {e}") from e

    if body is None:
        raise RuntimeError("网络请求异常，请确认网络链接并稍后重试")

    if body.get("responseCode") != '200':
        raise RuntimeError(
            f"Order creation failed: {body.get('responseMessage', 'unknown error')}"
        )

    order_no = body.get("orderNo")
    if not order_no:
        raise RuntimeError("Order creation response missing 'orderNo'")

    amount = body.get("amount")
    encrypted_data = body.get("encryptedData")
    pay_to = body.get("payTo")

    return order_no, amount, encrypted_data, pay_to


def save_order_info(order_no: str, amount: str, question: str,
                    encrypted_data: str, pay_to: str, indicator: str, description: str, skill_name: str) -> str:
    """
    Save order info to the fixed directory.
    """
    order_data = {
        "skill-id": f"si-{skill_name}",
        "order_no": order_no,
        "amount": amount,
        "question": question,
        "encrypted_data": encrypted_data,
        "pay_to": pay_to,
        "description": description,
        "slug": skill_name,
        "resource_url": "https://ms.jr.jd.com",
    }
    return save_order(indicator, order_no, order_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 create_order.py <question>", file=sys.stderr)
        sys.exit(1)

    question = sys.argv[1]

    # 加载配置文件
    try:
        config = load_config()
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    skill_name = config.get("skillName", "baby-name")
    pay_to = config.get("payTo")
    amount = config.get("amount", 1)
    description = config.get("description", "宝宝取名服务费用")

    # 检查payTo是否已配置
    if not pay_to or pay_to == "您的商户ID":
        print("订单创建失败: 请先在 configs/config.json 中配置您的商户ID (payTo)")
        sys.exit(1)

    indicator = compute_indicator(skill_name)

    try:
        order_no, amount, encrypted_data, pay_to = create_order(
            question, pay_to, amount, description
        )
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    save_order_info(order_no, amount, question,
                    encrypted_data, pay_to, indicator, description, skill_name)

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={question}")
    print(f"INDICATOR={indicator}")
