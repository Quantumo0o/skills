---
name: fb-train-skill
description: 分贝通火车预订助手，实时查询火车票、展示车次列表、预订火车票、查看订单、取消订单。Invoke when user wants to search trains, book train tickets, check train orders, or cancel train bookings.
version: 1.0.0
metadata: {"openclaw": {"emoji": "🚄", "category": "travel", "tags": ["分贝通", "火车", "高铁", "动车", "预订", "退票"], "requires": {"bins": ["python3"]}, "required": true}}
---
# 分贝通火车预订助手 (fb-train-skill)

## 技能描述

分贝通火车预订助手，实时查询火车票、展示车次列表、预订火车票、查看订单、取消订单。

---

⚠️ 【重要约束】
- 必须调用 `scripts/fb_train_api.py` 中的函数获取数据
- 禁止自行编造车次信息、价格或余票
- 接口返回什么数据就展示什么，不要修改

---

## 技能概述

基于分贝通火车OpenAPI开发的自动化对接技能，支持火车票搜索、预订、取消、查询等全流程操作，适配国内火车票预订场景。

## 技能能力

### 核心能力

1. **火车票搜索**：按出发站、到达站、日期查询车次列表
2. **车次详情查询**：获取指定车次座位类型、价格、余票等信息
3. **预订火车票**：创建火车票订单
4. **订单管理**：查询订单详情、取消订单
5. **收银台支付**：获取支付链接，引导用户完成支付

### 触发条件

1. **火车票搜索**：当用户输入「火车票/订火车票/查火车票/高铁/动车」+ 出发地/目的地/日期信息时，必须调用 `scripts/fb_train_api.py` 中的 `search_train_list()` 函数
   - 返回车次列表，使用表格形式展示
   - 默认展示5个车次，用户可选择继续查看更多
   - 展示格式示例：
     ```
     🚄 北京南 → 上海虹桥（3月15日）
     
     | 序号 | 车次 | 出发时间 | 到达时间 | 历时 | 二等座 | 一等座 | 商务座 |
     |:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
     | 1 | G1 | 09:00 | 13:28 | 4时28分 | ¥553 | ¥933 | ¥1748 |
     | 2 | G3 | 14:00 | 18:28 | 4时28分 | ¥553 | ¥933 | ¥1748 |
     
     💡 回复"序号"查看车次详情，如"1"查看第1个车次
     ```

2. **查看车次详情（序号）**：用户回复"序号"查看车次座位详情
   - **必须调用 `scripts/fb_train_api.py` 中的 `get_train_detail()` 函数**
   - 展示各座位类型的价格和余票
   - 展示格式示例：
     ```
     🚄 G1 北京南 → 上海虹桥
     📅 出发：3月15日 09:00 | 到达：3月15日 13:28
     ⏱️ 历时：4时28分
     
     | 座位类型 | 价格 | 余票 |
     |:---:|---:|:---:|
     | 二等座 | ¥553 | 有票 |
     | 一等座 | ¥933 | 5张 |
     | 商务座 | ¥1748 | 无票 |
     
     💡 回复"座位类型"预订，如"二等座"
     ```

3. **订单创建**：用户选择座位类型后创建订单
   - 收集乘车人信息：姓名、身份证号、手机号
   - 调用创建订单接口，返回订单ID
   - 订单创建成功的展示内容：
     ```
     ✅ 订单创建成功！
     
     🚄 G1 北京南 → 上海虹桥
     📅 出发：3月15日 09:00
     🎫 座位：二等座
     💰 价格：¥553
     👤 乘车人：张三
     
     🔗 [立即支付](https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=0)
     🔗 [查看订单详情](https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=1)
     ```

4. **订单操作**：用户发起取消/查询（需提供订单ID）
   - 取消订单：支持填写取消原因
   - 查询订单详情：展示订单完整信息

## 对接信息

### 基础配置

- 环境：线上环境
- 核心域名：https://openapiv2.fenbeitong.com
- X-App-Id：`688c927d2cf90c6f0595571d`（所有接口统一使用此App-Id）
- Content-Type：application/json

### 通用请求规则

1. 所有POST请求，参数为JSON格式
2. 日期格式：yyyy-MM-dd
3. 时间格式：HH:mm

## 核心接口列表

### 一、查询类接口

| 接口名称 | 接口地址 | 核心用途 | 必选参数 |
|---------|---------|---------|---------|
| 火车票搜索 | /openapi/travel/train/search_list/v1 | 按出发站/到达站/日期查车次 | from_station, to_station, travel_date |
| 车次详情 | /openapi/travel/train/detail/v1 | 查车次座位类型/价格/余票 | train_no, travel_date |
| 订单详情查询 | /openapi/travel/train/order/detail/v1 | 查订单状态/信息 | order_id |

### 二、订单类接口

| 接口名称 | 接口地址 | 核心用途 | 必选参数 |
|---------|---------|---------|---------|
| 火车票下单 | /openapi/travel/train/order/create/v1 | 创建火车票订单 | train_no, travel_date, seat_type, passenger_info, contact_info |
| 取消订单 | /openapi/travel/train/order/cancel/v1 | 取消已创建的订单 | order_id |

### 三、收银台支付

| 接口名称 | 接口地址 | 核心用途 |
|---------|---------|---------|
| 收银台支付 | `https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=0` | 引导用户完成支付 |
| 查看订单详情 | `https://app-gate.fenbeitong.com/business/train/open/push/redirect?orderId={order_id}&isSkill=true&type=1` | 查看订单详情 |

## 枚举值说明

### 座位类型 (seat_type)

- 9：商务座
- 1：一等座
- 2：二等座
- 3：软卧
- 4：硬卧
- 5：软座
- 6：硬座
- 7：无座

### 订单状态 (order_status)

- 1：待支付
- 2：已支付
- 3：出票中
- 4：已出票
- 5：已取消
- 6：退票中
- 7：已退票

## 响应规则

### 成功响应

```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

### 失败响应

```json
{
  "code": 500,
  "msg": "错误信息",
  "data": {}
}
```
