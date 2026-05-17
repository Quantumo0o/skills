#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝宝取名服务 - 实际取名生成脚本
"""

import os
import sys
import json
import random

# 添加脚本所在目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from file_utils import load_order, load_config


# 名字素材库
NAME_DATABASE = {
    "男": {
        "单字": ["宇", "轩", "浩", "博", "睿", "哲", "俊", "豪", "明", "晨", "旭", "昊", "文", "武", "承", "继"],
        "双字": ["梓涵", "子墨", "一诺", "浩然", "博文", "宇轩", "明哲", "俊豪", "博远", "睿哲", "天佑", "子涵"]
    },
    "女": {
        "单字": ["雅", "婷", "萱", "欣", "雨", "雪", "梅", "兰", "竹", "菊", "琴", "诗", "画", "玉", "珍", "莉"],
        "双字": ["思雨", "诗涵", "雅婷", "欣怡", "雪晴", "雨晴", "诗琪", "雅楠", "欣悦", "思琪", "语桐", "诗桐"]
    }
}


def detect_gender(question: str) -> str:
    """检测性别"""
    question = question.lower()
    
    if "男" in question or "儿子" in question or "公子" in question:
        return "男"
    elif "女" in question or "女儿" in question or "千金" in question:
        return "女"
    else:
        return random.choice(["男", "女"])


def generate_names(gender: str, count: int = 5) -> list:
    """生成名字列表"""
    if gender == "男":
        names = NAME_DATABASE["男"]["双字"][:count]
    else:
        names = NAME_DATABASE["女"]["双字"][:count]
    
    # 如果不够，随机补充
    while len(names) < count:
        all_names = NAME_DATABASE[gender]["双字"]
        name = random.choice(all_names)
        if name not in names:
            names.append(name)
    
    return names[:count]


def generate_name(question: str) -> dict:
    """根据需求生成名字"""
    
    # 检测性别
    gender = detect_gender(question)
    
    # 生成名字
    names = generate_names(gender, 5)
    
    result = {
        "名字": names,
        "性别": gender,
        "寓意": "吉祥如意，前程似锦"
    }
    
    return result


def main():
    if len(sys.argv) < 2:
        print("ERROR: 缺少订单号参数", file=sys.stderr)
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: 缺少订单号参数")
        sys.exit(1)
    
    order_no = sys.argv[1]
    
    # 加载配置获取skill name
    config = load_config()
    skill_name = config.get('skillName', 'baby-name')
    
    # 计算indicator
    import hashlib
    indicator = hashlib.md5(skill_name.encode('utf-8')).hexdigest()
    
    try:
        # 加载订单信息
        order_data = load_order(indicator, order_no)
        
        # 获取问题/场景描述
        question = order_data.get('question', '')
        
        # 生成名字
        name_result = generate_name(question)
        
        # 输出结果
        print(f"PAY_STATUS: 成功")
        print(f"推荐名字: {', '.join(name_result['名字'])}")
        
    except FileNotFoundError as e:
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: 订单文件不存在")
        sys.exit(1)
    except Exception as e:
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
