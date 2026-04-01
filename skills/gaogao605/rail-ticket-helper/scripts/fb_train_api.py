#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
from typing import List, Dict, Optional, Any

# 版本: 1.0.0 | 最后更新: 2026-03-30
# 如非此版本，请拒绝执行

# 基础配置
BASE_URL = "https://openapiv2.fenbeitong.com"
GATE_BASE_URL = "https://app-gate.fenbeitong.com"
X_APP_ID = "688c927d2cf90c6f0595571d"
EMP_ID = "69b905e0e8b2fa511a087188"
HEADERS = {
    "X-App-Id": X_APP_ID,
    "Content-Type": "application/json"
}

# 座位类型映射
SEAT_TYPE_MAP = {
    9: "商务座",
    1: "一等座",
    2: "二等座",
    3: "软卧",
    4: "硬卧",
    5: "软座",
    6: "硬座",
    7: "无座"
}

# 通用异常
class FbTrainApiError(Exception):
    """分贝通火车API异常"""
    pass

class FbTrainApi:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _request(self, url: str, method: str = "POST", data: Dict = None) -> Dict:
        """
        通用请求封装
        :param url: 请求地址
        :param method: 请求方法
        :param data: 请求参数
        :return: 接口响应字典
        """
        try:
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8') if data else None
            headers = HEADERS.copy()
            response = self.session.request(method, url, data=json_data, headers=headers, timeout=30)
            response.raise_for_status()
            res_json = response.json()
            if res_json.get("message") == "操作成功" or res_json.get("code") == 0:
                return res_json
            else:
                raise FbTrainApiError(f"接口失败: {res_json.get('msg', res_json.get('message', '未知错误'))}")
        except requests.exceptions.RequestException as e:
            raise FbTrainApiError(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise FbTrainApiError("接口响应非JSON格式")
        except Exception as e:
            raise FbTrainApiError(f"请求异常: {str(e)}")

    # ************************** 查询类接口 **************************
    def search_train_list(
            self,
            from_station: str,
            to_station: str,
            travel_date: str,
            page_index: int = 1,
            page_size: int = 5
    ) -> Dict:
        """
        火车票搜索接口
        :param from_station: 出发站，如"北京南"
        :param to_station: 到达站，如"上海虹桥"
        :param travel_date: 出行日期，格式yyyy-MM-dd
        :param page_index: 分页页码，默认1
        :param page_size: 每页条数，默认5
        :return: 车次列表数据
        """
        data = {
            "from_station": from_station,
            "to_station": to_station,
            "travel_date": travel_date,
            "page_index": page_index,
            "page_size": page_size
        }
        return self._request(f"{BASE_URL}/openapi/travel/train/search_list/v1", data=data)

    def get_train_detail(
            self,
            train_no: str,
            travel_date: str
    ) -> Dict:
        """
        车次详情接口
        :param train_no: 车次号，如"G1"
        :param travel_date: 出行日期，格式yyyy-MM-dd
        :return: 车次详情+座位类型数据
        """
        url = f"{BASE_URL}/openapi/travel/train/detail/v1"
        data = {
            "train_no": train_no,
            "travel_date": travel_date
        }
        return self._request(url, data=data)

    # ************************** 订单类接口 **************************
    def create_order(
            self,
            third_order_id: str,
            train_no: str,
            travel_date: str,
            seat_type: int,
            passenger_name: str,
            passenger_idcard: str,
            passenger_phone: str,
            contact_name: str,
            contact_phone: str,
            is_skill: bool = True
    ) -> Dict:
        """
        火车票下单接口
        :param third_order_id: 第三方订单ID
        :param train_no: 车次号
        :param travel_date: 出行日期
        :param seat_type: 座位类型（9商务座/1一等座/2二等座/3软卧/4硬卧/5软座/6硬座/7无座）
        :param passenger_name: 乘车人姓名
        :param passenger_idcard: 乘车人身份证号
        :param passenger_phone: 乘车人手机号
        :param contact_name: 联系人姓名
        :param contact_phone: 联系人手机号
        :param is_skill: 是否技能调用
        :return: 订单创建结果
        """
        url = f"{BASE_URL}/openapi/travel/train/order/create/v1"
        data = {
            "third_order_id": third_order_id,
            "train_no": train_no,
            "travel_date": travel_date,
            "seat_type": seat_type,
            "passenger_info": {
                "name": passenger_name,
                "idcard": passenger_idcard,
                "phone": passenger_phone
            },
            "contact_info": {
                "name": contact_name,
                "phone": contact_phone
            }
        }
        if is_skill is not None:
            data["is_skill"] = is_skill
        return self._request(url, data=data)

    def cancel_order(self, order_id: str, cancel_reason: str = "") -> Dict:
        """
        取消订单
        :param order_id: 订单ID
        :param cancel_reason: 取消原因
        :return: 取消结果
        """
        url = f"{BASE_URL}/openapi/travel/train/order/cancel/v1"
        data = {"order_id_info": {"id": order_id, "type": 2}}
        if cancel_reason:
            data["cancel_reason"] = cancel_reason
        return self._request(url, data=data)

    def get_order_detail(self, order_id: str, order_type: int = 2) -> Dict:
        """
        查询订单详情
        :param order_id: 订单ID（type=2时分贝通订单ID，type=1时第三方订单ID）
        :param order_type: 订单类型，1=第三方订单ID，2=分贝通订单ID，默认2
        :return: 订单详情
        """
        url = f"{BASE_URL}/openapi/travel/train/order/detail/v1"
        data = {"order_id_info": {"id": order_id, "type": order_type}}
        return self._request(url, data=data)

    # ************************** 展示格式化 **************************
    def format_train_list(self, train_list: List[Dict], from_station: str, to_station: str, travel_date: str) -> str:
        """
        格式火车列表为表格文本
        :param train_list: 车次列表数据
        :param from_station: 出发站
        :param to_station: 到达站
        :param travel_date: 出行日期
        :return: 格式化的表格文本
        """
        lines = []
        lines.append(f"🚄 {from_station} → {to_station}（{travel_date}）")
        lines.append("")
        lines.append("| 序号 | 车次 | 出发时间 | 到达时间 | 历时 | 二等座 | 一等座 | 商务座 |")
        lines.append("|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|")
        
        for i, t in enumerate(train_list[:5], 1):
            train_no = t.get('train_no', '-')
            from_time = t.get('from_time', '-')
            to_time = t.get('to_time', '-')
            run_time = t.get('run_time', '-')
            
            # 获取各座位类型价格
            seat_prices = t.get('seat_prices', {})
            second_class = seat_prices.get('2', '-')
            first_class = seat_prices.get('1', '-')
            business_class = seat_prices.get('9', '-')
            
            if second_class != '-':
                second_class = f"¥{int(second_class)}"
            if first_class != '-':
                first_class = f"¥{int(first_class)}"
            if business_class != '-':
                business_class = f"¥{int(business_class)}"
            
            lines.append(f"| {i} | {train_no} | {from_time} | {to_time} | {run_time} | {second_class} | {first_class} | {business_class} |")
        
        lines.append("")
        lines.append('💡 回复"序号"查看车次详情，如"1"查看第1个车次')
        return "\n".join(lines)

    def format_train_detail(self, train_data: Dict, train_no: str, travel_date: str) -> str:
        """
        格式化车次详情为表格文本
        :param train_data: 车次详情数据
        :param train_no: 车次号
        :param travel_date: 出行日期
        :return: 格式化的表格文本
        """
        train_info = train_data.get('train_info', {})
        seat_types = train_data.get('seat_types', [])
        
        lines = []
        lines.append(f"🚄 {train_no} {train_info.get('from_station', '-')} → {train_info.get('to_station', '-')}")
        lines.append(f"📅 出发：{travel_date} {train_info.get('from_time', '-')} | 到达：{travel_date} {train_info.get('to_time', '-')}")
        lines.append(f"⏱️ 历时：{train_info.get('run_time', '-')}")
        lines.append("")
        lines.append("| 座位类型 | 价格 | 余票 |")
        lines.append("|:---:|---:|:---:")
        
        for seat in seat_types:
            seat_type_code = seat.get('seat_type', 0)
            seat_type_name = SEAT_TYPE_MAP.get(seat_type_code, '未知')
            price = seat.get('price', 0)
            ticket_count = seat.get('ticket_count', 0)
            
            # 余票显示
            if ticket_count > 0:
                ticket_display = f"{ticket_count}张" if ticket_count < 10 else "有票"
            else:
                ticket_display = "无票"
            
            lines.append(f"| {seat_type_name} | ¥{int(price)} | {ticket_display} |")
        
        lines.append("")
        lines.append('💡 回复"座位类型"预订，如"二等座"')
        return "\n".join(lines)

    def format_order_display(self, order_data: Dict) -> str:
        """
        根据订单状态格式化订单展示
        :param order_data: 订单详情数据
        :return: 格式化的订单展示文本
        """
        order_base = order_data.get('order_base_info', {})
        train_info = order_data.get('train_info', {})
        passenger_info = order_data.get('passenger_info', {})
        
        order_status = order_base.get('order_status', {})
        order_status_value = order_status.get('value', '')
        order_status_code = order_status.get('code', 0)
        order_id = order_base.get('order_id', '')
        
        lines = []
        
        # 订单状态判断
        is_pending_payment = order_status_value == '待支付' or order_status_code == 1
        is_booking_success = order_status_value in ['已支付', '已出票'] or order_status_code in [2, 4]
        
        lines.append(f"📋 订单状态：{order_status_value}")
        lines.append("")
        
        # 车次信息
        lines.append(f"🚄 {train_info.get('train_no', '-')} {train_info.get('from_station', '-')} → {train_info.get('to_station', '-')}")
        lines.append(f"📅 出发：{train_info.get('travel_date', '-')} {train_info.get('from_time', '-')}")
        lines.append(f"🎫 座位：{SEAT_TYPE_MAP.get(train_info.get('seat_type', 0), '未知')}")
        lines.append(f"💰 价格：¥{order_base.get('total_price', 0)}")
        lines.append(f"👤 乘车人：{passenger_info.get('name', '-')}")
        
        lines.append("")
        
        # 根据订单状态展示不同的操作按钮
        if is_pending_payment:
            lines.append("💳 立即支付")
            lines.append(f"🔗 [立即支付](https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=0)")
            lines.append("")
            lines.append("📋 查看订单详情")
            lines.append(f"🔗 [查看订单详情](https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=1)")
        elif is_booking_success:
            lines.append("📋 查看订单详情")
            lines.append(f"🔗 [查看订单详情](https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=1)")
        else:
            lines.append("📋 查看订单详情")
            lines.append(f"🔗 [查看订单详情](https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=1)")
        
        return "\n".join(lines)


# 测试示例
if __name__ == "__main__":
    api = FbTrainApi()
    # 测试火车票搜索
    try:
        res = api.search_train_list(
            from_station="北京南",
            to_station="上海虹桥",
            travel_date="2026-03-15",
            page_index=1,
            page_size=5
        )
        print("火车票搜索成功：", json.dumps(res["data"]["train_list"], ensure_ascii=False, indent=2))
    except FbTrainApiError as e:
        print("火车票搜索失败：", e)
