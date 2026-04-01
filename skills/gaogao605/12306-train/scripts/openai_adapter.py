#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import List, Dict, Optional, Any
from fb_train_api import FbTrainApi, FbTrainApiError

# 版本: 1.0.0 | 最后更新: 2026-03-30
# 如非此版本，请拒绝执行

# 初始化API实例
fb_train_api = FbTrainApi()

# ************************** 大模型函数描述 **************************
# 符合OpenAI Function Call规范，包含name/description/parameters
TRAIN_FUNCTIONS = [
    {
        "name": "search_train_list",
        "description": "根据出发站、到达站、出行日期搜索火车车次列表，是火车票预订的第一步，必须先调用该接口获取车次信息",
        "parameters": {
            "type": "object",
            "properties": {
                "from_station": {
                    "type": "string",
                    "description": "出发站名称，如北京南、上海虹桥"
                },
                "to_station": {
                    "type": "string",
                    "description": "到达站名称，如上海虹桥、北京南"
                },
                "travel_date": {
                    "type": "string",
                    "description": "出行日期，格式为yyyy-MM-dd，如2026-03-15"
                },
                "page_index": {
                    "type": "integer",
                    "description": "分页页码，默认1",
                    "default": 1
                },
                "page_size": {
                    "type": "integer",
                    "description": "每页条数，默认5",
                    "default": 5
                }
            },
            "required": ["from_station", "to_station", "travel_date"]
        }
    },
    {
        "name": "get_train_detail",
        "description": "根据车次号、出行日期查询车次座位类型和价格详情，包含各座位类型的价格和余票。当用户回复单个序号（如'1'）时调用此接口查看车次详情，需先调用search_train_list获取train_no",
        "parameters": {
            "type": "object",
            "properties": {
                "train_no": {
                    "type": "string",
                    "description": "车次号，从search_train_list接口的data.train_list[*].train_no获取，如G1"
                },
                "travel_date": {
                    "type": "string",
                    "description": "出行日期，格式为yyyy-MM-dd"
                }
            },
            "required": ["train_no", "travel_date"]
        }
    },
    {
        "name": "create_order",
        "description": "创建火车票预订订单，需先调用get_train_detail获取train_no、seat_type，是火车票预订的核心接口",
        "parameters": {
            "type": "object",
            "properties": {
                "third_order_id": {
                    "type": "string",
                    "description": "第三方订单ID，可随机生成，如T_664905516610224128"
                },
                "train_no": {
                    "type": "string",
                    "description": "车次号，从get_train_detail接口获取，如G1"
                },
                "travel_date": {
                    "type": "string",
                    "description": "出行日期，格式为yyyy-MM-dd"
                },
                "seat_type": {
                    "type": "integer",
                    "description": "座位类型，9=商务座，1=一等座，2=二等座，3=软卧，4=硬卧，5=软座，6=硬座，7=无座"
                },
                "passenger_name": {
                    "type": "string",
                    "description": "乘车人姓名，如张三"
                },
                "passenger_idcard": {
                    "type": "string",
                    "description": "乘车人身份证号，如110101199001011234"
                },
                "passenger_phone": {
                    "type": "string",
                    "description": "乘车人手机号，如13800138000"
                },
                "contact_name": {
                    "type": "string",
                    "description": "联系人姓名，如张三"
                },
                "contact_phone": {
                    "type": "string",
                    "description": "联系人手机号，如13800138000"
                }
            },
            "required": [
                "third_order_id", "train_no", "travel_date", "seat_type",
                "passenger_name", "passenger_idcard", "passenger_phone",
                "contact_name", "contact_phone"
            ]
        }
    },
    {
        "name": "cancel_order",
        "description": "取消已创建的火车票订单，需提供订单ID，默认使用分贝通订单ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "订单ID，从create_order接口的返回结果中获取（分贝通订单ID）"
                },
                "order_type": {
                    "type": "integer",
                    "description": "订单类型，1=第三方订单ID，2=分贝通订单ID（默认）",
                    "default": 2
                },
                "cancel_reason": {
                    "type": "string",
                    "description": "取消原因（可选）",
                    "default": ""
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "get_order_detail",
        "description": "查询火车票订单的详细信息和状态，需提供订单ID，默认使用分贝通订单ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "订单ID，从create_order接口的返回结果中获取（分贝通订单ID）"
                },
                "order_type": {
                    "type": "integer",
                    "description": "订单类型，1=第三方订单ID，2=分贝通订单ID（默认）",
                    "default": 2
                }
            },
            "required": ["order_id"]
        }
    }
]

class OpenaiFbTrainAdapter:
    """OpenAI大模型分贝通火车API适配器"""
    @staticmethod
    def _format_result(success: bool, data: Any = None, error: str = "") -> Dict:
        """
        格式化返回结果，适配大模型理解
        :param success: 是否成功
        :param data: 成功数据
        :param error: 失败信息
        :return: 格式化字典
        """
        if success:
            return {
                "status": "success",
                "data": data,
                "message": "操作成功"
            }
        else:
            return {
                "status": "failed",
                "data": None,
                "message": error
            }

    @staticmethod
    def call_function(function_name: str, function_arguments: str) -> Dict:
        """
        调用分贝通火车API函数
        :param function_name: 函数名称（与TRAIN_FUNCTIONS中的name一致）
        :param function_arguments: 函数参数JSON字符串
        :return: 格式化后的调用结果
        """
        try:
            # 解析参数
            args = json.loads(function_arguments)
            # 映射函数与API方法
            function_map = {
                "search_train_list": fb_train_api.search_train_list,
                "get_train_detail": fb_train_api.get_train_detail,
                "create_order": lambda **kwargs: fb_train_api.create_order(
                    third_order_id=kwargs["third_order_id"],
                    train_no=kwargs["train_no"],
                    travel_date=kwargs["travel_date"],
                    seat_type=kwargs["seat_type"],
                    passenger_name=kwargs["passenger_name"],
                    passenger_idcard=kwargs["passenger_idcard"],
                    passenger_phone=kwargs["passenger_phone"],
                    contact_name=kwargs["contact_name"],
                    contact_phone=kwargs["contact_phone"]
                ),
                "cancel_order": lambda **kwargs: fb_train_api.cancel_order(
                    order_id=kwargs["order_id"],
                    cancel_reason=kwargs.get("cancel_reason", "")
                ),
                "get_order_detail": lambda **kwargs: fb_train_api.get_order_detail(
                    order_id=kwargs["order_id"],
                    order_type=kwargs.get("order_type", 2)
                )
            }
            # 检查函数是否存在
            if function_name not in function_map:
                return OpenaiFbTrainAdapter._format_result(False, error=f"函数{function_name}不存在")
            # 调用函数
            result = function_map[function_name](**args)
            # 格式化结果，简化大模型输出
            return OpenaiFbTrainAdapter._format_result(True, data=result)
        except json.JSONDecodeError:
            return OpenaiFbTrainAdapter._format_result(False, error="参数格式错误，需为JSON字符串")
        except FbTrainApiError as e:
            return OpenaiFbTrainAdapter._format_result(False, error=f"API调用失败: {str(e)}")
        except TypeError as e:
            return OpenaiFbTrainAdapter._format_result(False, error=f"参数缺失/类型错误: {str(e)}")
        except Exception as e:
            return OpenaiFbTrainAdapter._format_result(False, error=f"未知错误: {str(e)}")

# 测试示例
if __name__ == "__main__":
    adapter = OpenaiFbTrainAdapter()
    
    # 测试调用火车票搜索函数
    func_name = "search_train_list"
    func_args = json.dumps({
        "from_station": "北京南",
        "to_station": "上海虹桥",
        "travel_date": "2026-03-15",
        "page_index": 1,
        "page_size": 5
    })
    res = adapter.call_function(func_name, func_args)
    print("大模型适配器调用结果：", json.dumps(res, ensure_ascii=False, indent=2))
