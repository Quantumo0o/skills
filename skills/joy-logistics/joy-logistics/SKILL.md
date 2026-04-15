---
name: joy-logistics
description: 京东国际物流数据查询技能
  核心能力：支持物流轨迹追踪、国际运营指标查询、跨境小包体验指标查询三大功能模块。

  1.国际物流轨迹追踪技能
  功能描述：查询国际物流单号的实时物流轨迹信息。
  支持的单号类型：
  - FS 开头的京东订单号
  - JDW 开头的京东运单号
  - 客户运单号
  - 承运商运单号
  核心能力：
  - 实时查询物流轨迹

  2.供应链运营指标查询
  功能描述：可按多种维度查询、对比分析供应链运营指标数据
  支持查询如下指标：
  - 海外仓入库下单件数
  - 海外仓入库及时率
  - 头程在途体积
  - 海外仓入库下单sku数
  - 海外仓入库体积
  - 海外仓实际出库重量
  - 发货及时率
  - 海外仓入库重量
  - 海外仓入库单量
  - 海外仓出库及时率
  - 退件件量
  - 海外仓目标入库件数
  - 海外仓库位合格率
  - 海外仓高位拣选比例
  - 海外仓蓝牙拣选使用率
  - 海外仓入库sku数
  - ATTSCAN及时率
  - 海外仓配Ascan及时率
  - 海外仓24H尾单关闭率
  - 头程渗透率
  - 海外仓机区D类库存占比
  - 海外仓实际出库体积
  - 海外仓上架准确率
  - 海外仓目标出库单量
  - 海外仓目标出库件数
  - 海外仓实际出库单量
  - 海外仓配Dscan及时率
  - 海外仓入库下单量
  - 海外仓入库件数
  - 退件上架及时率
  - 海外仓仓容利用率
  - 收货准确率
  - 海外仓实际出库件数
  - 海外仓退货验收单量
  - 全程履约率

  3.跨境小包体验指标查询
  功能描述：可按客户（客户编码/名称）、时间维度及全球视角进行多维度数据指标查询与对比分析
  支持的指标：
  - 全程履约率

---

# 京东国际物流轨迹追踪技能

根据用户输入的批量物流单号，调用京东国际物流开放接口，批量查询物流轨迹信息。支持灵活注入 referenceNumber 物流单号参数，可根据用户查询意图自动匹配并填充对应参数。

## 触发场景

当用户需要查询物流轨迹、订单状态、包裹运输进度、运单跟踪时使用此技能，例如：
- "查一下 JDW100xxxxxx6372 的物流轨迹"
- "查询订单号 FS2026xxxxxx0098405P 的信息"
- "查询客户运单号 1435xxxxxx460 的物流"
- "查询承运商运单号 505xxxxxx44680 的轨迹"
- "帮我查一下 JDW1xxxxxx6372 的物流"
- "查一下这个单号的物流信息 JDW1xxxxxx6372"

## 操作步骤

## CURL 模板

```bash
token=$(grep '^joy_token=' ~/.env | cut -d'=' -f2-)
curl --location https://lop-proxy.ochama.com/global/trackingOpenExport/queryTrackingBatch' \
  --header 'LOP-DN: ifop.skill.eu.outer.jd.com' \
  --header 'Content-Type: application/json' \
  --header "token: ${token}" \
  --data '[
    {
        "includeFields": [
            "waybill"
        ],
        "locale": "zh-CN",
        "referenceList": [
            {
                "customerCode": "",
                "referenceNumber": "JDWxxxxxx6372",
                "referenceType": 0
            }
        ],
        "scope": 4,
        "timeZone": "UTC+08:00"
    }
]'
```


## 使用示例

### 示例 1：查询单个物流单号 JDW1*****6372

```bash
token=$(grep '^joy_token=' ~/.env | cut -d'=' -f2-)
curl --location 'https://lop-proxy.ochama.com/global/trackingOpenExport/queryTrackingBatch' \
  --header 'LOP-DN: ifop.skill.eu.outer.jd.com' \
  --header 'Content-Type: application/json' \
  --header "token: ${token}" \
  --data '[
    {
        "includeFields": [
            "waybill"
        ],
        "locale": "zh-CN",
        "referenceList": [
            {
                "customerCode": "",
                "referenceNumber": "JDWxxxxxx6372",
                "referenceType": 0
            }
        ],
        "scope": 4,
        "timeZone": "UTC+08:00"
    }
]'
```

### 示例 2：查询多个物流单号 JDW1xxxxxx6372 和 JDW100xxxxxx696373

```bash
token=$(grep '^joy_token=' ~/.env | cut -d'=' -f2-)
curl --location 'https://lop-proxy.ochama.com/global/trackingOpenExport/queryTrackingBatch' \
  --header 'LOP-DN: ifop.skill.eu.outer.jd.com' \
  --header 'Content-Type: application/json' \
  --header "token: ${token}" \
  --data '[
    {
        "includeFields": [
            "waybill"
        ],
        "locale": "zh-CN",
        "referenceList": [
            {
                "customerCode": "",
                "referenceNumber": "JDWxxxxxx96372",
                "referenceType": 0
            },
            {
                "customerCode": "",
                "referenceNumber": "JDW100xxxxxx696373",
                "referenceType": 0
            }
        ],
        "scope": 4,
        "timeZone": "UTC+08:00"
    }
]'
```


## 响应格式说明

### 响应状态码

| 状态码 | 说明 |
|-------|------|
| 1000 | 请求成功 |
| 其他 | 请求失败，请查看 msg 字段获取详细信息 |

### trackingNodes 数组元素说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| orderNo | string | 订单号 |
| referenceNumber | string | 物流单号 |
| referenceType | number | 单号类型（固定为 0） |
| trackings | array | 轨迹详情数组 |
| waybillNo | string | 运单号 |

### trackings 数组元素说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| extend | object | 扩展信息 |
| field | string | 字段类型 |
| operateLocation | object | 操作位置 |
| operateSiteId | string | 操作站点ID |
| operationCode | string | 操作代码 |
| operationTime | string | 时间 |
| operationType | string | 操作类型 |
| operatorName | string | 操作人 |
| remark | string | 轨迹信息 |
| waybillNo | string | 运单号 |

### operateLocation 字段说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| routeCityName | string | 城市名称 |
| routeCountry | string | 国家名称 |
| routeProvinceName | string | 州(省)名称 |

### extend 字段说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| operationTimestamp | string | 时间戳 |
| timeZone | string | 操作时区 |
| remark | string | 备注 |
| locale | string | 语言 |

### 成功响应示例 - 没有轨迹信息

```json
{
  "code": 1000,
  "msg": "请求成功",
  "data": [
    {
      "referenceNumber": "JDW10xxxxxxx96372",
      "referenceType": 0,
      "trackingNodes": []
    }
  ]
}
```

### 成功响应示例 - 有轨迹数据

```json
{
  "code": 1000,
  "data": [
    {
      "referenceNumber": "JDW10xxxxxxx96372",
      "referenceType": 0,
      "trackingNodes": [
        {
          "orderNo": "FS2026xxxxxx98405P",
          "referenceNumber": "JDW10xxxxxx96372",
          "referenceType": 0,
          "trackings": [
            {
              "extend": {
                "operationTimestamp": "1774431780000",
                "timeZone": "UTC+08:00",
                "remark": "已分配车辆和司机/ Vehicle and driver assigned",
                "locale": "zh-CN"
              },
              "field": "waybill",
              "operateLocation": {},
              "operateSiteId": "",
              "operationCode": "A02",
              "operationTime": "2026-03-25 17:43:00",
              "operationType": "8000",
              "operatorName": "liukunmiao",
              "remark": "已提货/Cargo already picked up",
              "waybillNo": "JDW10xxxxxx96372"
            },
            {
              "extend": {
                "operationTimestamp": "1774490659000",
                "timeZone": "UTC+08:00",
                "remark": "承运商已上门提货",
                "locale": "zh-CN"
              },
              "field": "waybill",
              "operateLocation": {},
              "operateSiteId": "",
              "operationCode": "DMPU",
              "operationTime": "2026-03-26 10:04:19",
              "operationType": "8000",
              "operatorName": "bjtfei",
              "remark": "承运商已上门提货",
              "waybillNo": "JDW10xxxxxx96372"
            },
            {
              "extend": {
                "operationTimestamp": "1774490967000",
                "timeZone": "UTC+08:00",
                "remark": "已妥投/Cargo delivered",
                "locale": "zh-CN"
              },
              "field": "waybill",
              "operateLocation": {},
              "operateSiteId": "",
              "operationCode": "DLV",
              "operationTime": "2026-03-26 10:09:27",
              "operationType": "8000",
              "operatorName": "bjtfei",
              "remark": "已妥投/Cargo delivered",
              "waybillNo": "JDW10xxxxxx96372"
            }
          ],
          "waybillNo": "JDW10xxxxxx96372"
        }
      ]
    }
  ],
  "msg": "请求成功"
}
```

### 成功响应示例 - 批量查询（两个单号）

```json
{
  "code": 1000,
  "data": [
    {
      "referenceNumber": "JDW100xxxxxx643",
      "referenceType": 0,
      "trackingNodes": [
        {
          "carrierWaybillNo": "JDW100xxxxxx643",
          "orderNo": "FS2025xxxxxx076950",
          "referenceNumber": "JDW1xxxxxx23643",
          "referenceType": 0,
          "trackings": [
            {
              "extend": {
                "locale": "zh-CN",
                "SPP": "WAYBILL",
                "state": "COSH",
                "operationTimestamp": "1762617596000",
                "packageId": "JDW100xxxxxx643-1-1-",
                "timeZone": "UTC+08:00"
              },
              "field": "waybill",
              "operateLocation": {},
              "operationCode": "COSH",
              "operationTime": "2025-11-08 23:59:56",
              "operationType": "8000",
              "operatorName": "COSH",
              "remark": "Client Order Shipped"
            },
            {
              "extend": {
                "locale": "zh-CN",
                "SPP": "SPP99009b",
                "cityName": "HGK",
                "state": "CXLHDP",
                "operationTimestamp": "1762713000000",
                "packageId": "JDW100xxxxxx643-1-1-",
                "timeZone": "UTC+08:00"
              },
              "field": "waybill",
              "operateLocation": {
                "routeCityName": "HGK"
              },
              "operationCode": "CXLHDP",
              "operationTime": "2025-11-10 02:30:00",
              "operationType": "8000",
              "operatorName": "CXLHDP",
              "remark": "Departure from origin port",
              "waybillNo": "505755044680"
            },
            {
              "extend": {
                "locale": "zh-CN",
                "SPP": "SPP99009b",
                "cityName": "ICN",
                "state": "CXLHAP",
                "operationTimestamp": "1762725840000",
                "packageId": "JDW100xxxxxx643-1-1-",
                "timeZone": "UTC+08:00"
              },
              "field": "waybill",
              "operateLocation": {
                "routeCityName": "ICN"
              },
              "operationCode": "CXLHAP",
              "operationTime": "2025-11-10 06:04:00",
              "operationType": "8000",
              "operatorName": "CXLHAP",
              "remark": "Arrive at destination port",
              "waybillNo": "505755044680"
            }
          ],
          "waybillNo": "JDW100xxxx23643"
        }
      ]
    },
    {
      "referenceNumber": "JDW100xxxx23643",
      "referenceType": 0,
      "trackingNodes": [
        {
          "referenceNumber": "JDW100xxxxxx643",
          "referenceType": 0,
          "trackings": [],
          "waybillNo": "JDW100xxxxxx643"
        }
      ]
    }
  ],
  "msg": "请求成功"
}
```

### 成功响应示例 - 未查询到单据的物流轨迹（单个查询）

```json
{
  "code": 1000,
  "msg": "请求成功",
  "data": []
}
```

### 格式化输出示例

#### 输出开头要求
**物流轨迹详情：**

京东运单号:JDWxxxxxx890
京东订单号:FS1xxxxxx900

| 序号 | 时间 | 地点 | 轨迹 |
|-----|---------|-------|------|
| 1 | UTC+8 2026-03-25 17:43:00 | MISSOURI CITY，US，TX | 已提货/Cargo already picked up |
| 2 | UTC+8 2026-03-26 10:04:19 | CHAMPAIGN，US，IL | 承运商已上门提货 |
| 3 | UTC+8 2026-03-26 10:09:27 | Lake Zurich，US，IL | ✅Delivered |

#### 示例 2：批量查询结果
**单号 JDW000xxxxxx6629 轨迹详情：**

| 序号 | 时间 | 地点 | 轨迹 |
|-----|---------|-------|------|
| 1 | UTC+8 2026-03-25 18:43:00 | MISSOURI CITY，US，TX | 已提货/Cargo already picked up |
| 2 | UTC+8 2026-03-26 12:04:19 | CHAMPAIGN，US，IL | 承运商已上门提货 |
| 3 | UTC+8 2026-03-26 14:09:27 | Lake Zurich，US，IL | ✅Delivered |

**单号 JDW00xxxxxx6630 轨迹详情：**
- 物流单号 JDW00xxxxxx6630 未查询到物流轨迹

**单号 JDW00xxxxx6631 错误信息：**
- [错误信息描述]

#### 示例 3：批量查询结果（两个单号，一时区示例）
【客户信息】
客户编码：KH00000000001

**单号 JDW10xxxxxx3643 轨迹详情：**

| 序号 | 时间 | 地点 | 轨迹 |
|-----|------|-------|------|
| 1 | UTC+8 2025-11-08 23:59:56 |  | Parcel Data Received |
| 2 | UTC+8 2025-11-10 02:30:00 | US | Shipment information sent to FedEx |
| 3 | UTC+8 2025-11-10 06:04:00 | MISSOURI CITY，TX，US | Picked up |

**单号 JDW200xxxxxx098 轨迹详情：**
- 物流单号 JDW200xxxxxx098 未查询到物流轨迹

#### 示例 4：未查询到单据的物流轨迹（单个查询）

查询结果：物流单号 JDW200xxxxxx098 未查询到物流轨迹

## 输出结果处理

- 输出结果字段包含序号、时间、地点和轨迹
- 如果`轨迹信息`字段返回内容与`Delivered`或`delivered`完全匹配，在`轨迹`中必须在其左侧加上`✅`，例如：`✅Delivered`
- `地点`严格按照[城市名称，州(省)名称,国家名称]进行拼接展示，如果字段为空，则不展示
- 如果 trackingNodes 为空数组，表示该单号暂无轨迹信息
- `时间`严格按照[操作时区 时间]进行拼接展示，并且不要换行展示
- 展示时间时，使用 `trackings[].operationTime` 字段（已格式化为 "YYYY-MM-DD HH:mm:ss"），而不是 `extend.operationTimestamp` 时间戳
- 展示时区时，优先使用 `trackings[].extend.timeZone`

## 注意事项

- `JDW`开头的单号表示京东运单号
- `FS`开头的单号表示京东订单号
- 每个物流单号需要在 referenceList 数组中单独创建一个对象
- referenceType 固定为 0，无需修改
- customerCode 保持为空字符串
- 支持批量查询，在 referenceList 数组中追加多个单号对象即可
- 固定参数（appKey、includeFields、locale、scope、timeZone）保持不变
- **重要：当响应的 data 数组为空时，表示未查询到单号的物流轨迹，此时直接返回简单提示信息："查询结果：物流单号 {单号} 未查询到物流轨迹"。不要输出任何其他信息。**

## 可选：数据分析（按需提供）

在展示完基础数据后，如果数据有分析价值，可以追加以下分析（任选，根据数据情况）：

**物流轨迹可分析：**
- 平均配送时长
- 各环节耗时分布
- 异常节点识别

**注意：** 数据分析是可选的，仅在数据量≥3条时提供，必须基于真实数据，不得编造。





# 供应链全球运营指标查询技能

## 触发场景

### 洲际、仓库、客户、货主、产品等维度指标查询
当用户需要查询仓库相关指标数据时使用，例如：
- "查询 2026 年 1 月 1 日的 xxxx 仓库的 ASCAN 及时率"
- "查询 2026 年 1 月 1 日 全球的 ASCAN 及时率"
- "查询 2026 年 3 月 1 日到 3 月 4 日 欧洲区的 ASCAN 及时率"
- "查询 最近一周 xxxx 仓库的 24H尾单关闭率"

### 指标排名/对比/最值查询
当用户需要**对比、排序、找最值（最好/最差/最高/最低）、Top/N、按天/按周期对比**时使用。
- 最近一周 Dscan 及时率表现最好的仓
- 最近一周亚太区每天的 Ascan 及时率，哪个表现最好
- 4.1 亚太区哪个仓的出库及时率最低
- 最近一周的出库及时率最低的 3 个客户
- 对比各洲际本周 ASCAN 及时率

### 

## 支持的指标
- **Ascan及时率**: 指标编码 `B699900002`
- **Dscan及时率**: 指标编码 `B699900003`
- **出库及时率**: 指标编码 `B690210000`
- **入库及时率**: 指标编码 `B699900004`
- **海外仓24H尾单关闭率**: 指标编码 `B690210002`
- **海外仓入库下单件数**: 指标编码 `B691500021`
- **头程在途体积**: 指标编码 `B699900029`
- **海外仓入库下单sku数**: 指标编码 `B691500022`
- **海外仓入库体积**: 指标编码 `B699900005`
- **海外仓实际出库重量**: 指标编码 `B691500009`
- **发货及时率**: 指标编码 `B1659900020`
- **海外仓入库重量**: 指标编码 `B691500011`
- **海外仓入库单量**: 指标编码 `B691500018`
- **退件件量**: 指标编码 `B699900031`
- **海外仓目标入库件数**: 指标编码 `B691500024`
- **海外仓库位合格率**: 指标编码 `B691500014`
- **海外仓高位拣选比例**: 指标编码 `B691500003`
- **海外仓蓝牙拣选使用率**: 指标编码 `B691500025`
- **海外仓入库sku数**: 指标编码 `B691500019`
- **ATTSCAN及时率**: 指标编码 `B9999400009`
- **头程渗透率**: 指标编码 `B699900030`
- **海外仓机区D类库存占比**: 指标编码 `B691500027`
- **海外仓实际出库体积**: 指标编码 `B691500008`
- **海外仓上架准确率**: 指标编码 `B691500029`
- **海外仓目标出库单量**: 指标编码 `B691500004`
- **海外仓目标出库件数**: 指标编码 `B691500005`
- **海外仓实际出库单量**: 指标编码 `B691500006`
- **全程履约率**: 指标编码 `B1659900021`
- **海外仓入库下单量**: 指标编码 `B691500020`
- **海外仓入库件数**: 指标编码 `B691500010`
- **退件上架及时率**: 指标编码 `B699900032`
- **海外仓仓容利用率**: 指标编码 `B690700001`
- **收货准确率**: 指标编码 `B9999500012`
- **海外仓实际出库件数**: 指标编码 `B691500007`
- **海外仓退货验收单量**: 指标编码 `B691500023`

## 使用流程

### 1. 解析自然语言参数
从用户输入中提取以下参数：
**参数定义**
| 参数名 | 含义 | 类型 | 必填 | 格式要求 | 取值范围/约束 | 示例 |
| --- | --- | --- | --- | --- | --- | --- |
| indicatorCode | 指标编码 | 字符串 | 是 | 字符串 | 必填参数，用户必须提供 | "INV001" |
| dateList | 日期列表 | 数组 | 否 | 字符串数组，格式为 YYYY-MM-DD | 日期需为有效公历日期 | ["2026-01-01", "2026-01-02"] |
| monthList | 月份列表 | 数组 | 否 | 字符串数组，格式为 YYYY-MM | 月份需为有效年月 | ["2026-01", "2026-02"] |
| warehouseCodeList | 仓库编码列表 | 数组 | 否 | 11位字符串 | 必须以大写字母"C"开头 | ["C1234567890"] |
| warehouseNameList | 仓库名称列表 | 数组 | 否 | 任意字符串 | 无特殊限制 | ["芬瑞一号仓"] |
| warehouseTypeList | 仓库类型列表 | 数组 | 否 | 字符串 | 必须为"自营仓"、"协同仓"、"加盟仓"、"验货仓"，用户不提默认传空 | ["自营仓","协同仓","加盟仓"] |
| continentList | 洲际集合 | 数组 | 否 | 字符串 | 仅限以下值：亚太区、中东区、欧洲区、美洲区 | ["亚太区"] |
| productCodeList | 产品编码集合 | 数组 | 否 | 字符串 | 以"SPB"、"PD"、"SL"开头的字符串 | ["SPB00001"] |
| productNameList | 产品名称集合 | 数组 | 否 | 任意字符串 | 无特殊限制 | ["服务产品001"] |
| orderFlagList | 内外单标识集合 | 数组 | 否 | 字符串 | 必须为"内单"或"外单" | ["内单"] |
| ownerNoList | 货主编码集合 | 数组 | 否 | 字符串 | 以"FBU"开头的字符串 | ["FBU00000000001"] |
| ownerNameList | 货主名称集合 | 数组 | 否 | 任意字符串 | 无特殊限制 | ["货主001"] |
| countryList | 国家集合 | 数组 | 否 | 字符串 | 国家名称字符串 | ["中国","新加坡"] |
| dims | 统计维度数组	 | 数组 | 否 | 字符串 | 非必填，用户希望查询的维度 | ["warehouse"] |

**注意**:
- 一定不要回复用户任何编造和修改的数据
- 如果用户希望查询的指标不存在，直接告诉用户`暂时不支持该指标查询，希望查看更多指标请前往isc平台，链接：http://isc.jd.com`，不要任何其他描述
- 如果用户的查询请求过于模糊无法做到指标匹配，返回提示："您的查询条件不够明确，请提供更具体的指标名称、时间范围或仓库信息"
- 所有数据均为T-1离线数据，无法查询实时数据
- 如果用户同时查询两种指标，直接返回提示："我们目前支持单次查询一种指标"
- 当识别到用户需要查询洲际相关指标数据时，洲际信息必须为`亚太区`,`中东区`,`欧洲区`,`美洲区`其中之一
- **重要**:
  - 如果用户只查询"全程履约率"且没有明确说明是供应链还是跨境小包，请先询问用户："请问您想查询的是供应链全球运营指标的全程履约率，还是跨境小包体验指标的全程履约率？"，待用户明确后再执行对应技能
  - 如果用户明天提及查询某个`客户`的全程履约率，则默认查询`跨境小包体验指标`中的`全程履约率`

- **仓库编码自动补全**:
  - 仓库编码为`C`开头长度为**11**的字符串，若用户输入的仓库编码不足11位，则在前面拼接`C`和若干`0`，得到完整的仓库编码
    例如用户输入`查询312仓最近一周的Dscan及时率`，则用户查询的完整的仓库编码为`C0000000312`
  - 仓库名称通常为`地名` 加 `编号`的组合，例如`荷兰芬瑞1号仓`

- **dims维度规则**:
  - 若用户意图是按**天**对比（如查询最近一周每天的某个指标），dims 填 ["dt"]
  - 若用户意图是按**月**对比（如查询最近三个月每个月的某个指标），dims 填 ["month"]
  - 若用户意图是按**仓库**对比 / 排名（如找最好 / 最差的仓），dims 填 ["warehouse"]
  - 若用户意图是按**仓库类型**对比 / 统计（如各类型仓库表现） / 排名（如找最好 / 最差类型的仓），dims 填 ["warehouse_type"]
  - 若用户意图是按**洲际**对比 / 统计（如各洲际表现、全球各洲际汇总），dims 填 ["continent"]
  - 若用户意图是按**客户**对比 / 统计（如找最好 / 最差的客户），dims 填 ["customer"]
  - 若用户意图是按**货主**对比 / 统计（如找最好 / 最差的货主），dims 填 ["owner"]
  - 若用户意图是按**内外单**对比 / 统计（如各洲表现、全球汇总），dims 填 ["order_flag"]
  - 若用户意图是按**产品**对比 / 统计 / 排名（如各产品表现），dims 填 ["product"]
  - 若用户希望按`多个维度`对比时，dims 可以填入多个值（例如查询最近一周每天表现最好的仓，dims 需要填入["dt","warehouse"]）
  - 若用户希望查询`具体条件`的指标信息时，dims 不要填入对应维度的任何信息（例如用户希望查询亚太区最近一周的Dscan及时率，则continentList为['亚太区']，dims里不要有'continent'）
  - 未明确维度时可不填


### 2. 参数映射规则

| 用户输入关键词 | 指标编码 | 指标名称 |
|--------------|---------|---------|
| ASCAN 及时率 | B699900002 | 海外仓配 ASCAN 及时率 |
| DSCAN 及时率 | B699900003 | 海外仓配 DSCAN 及时率 |
| 出库及时率 | B690210000 | 海外仓出库及时率 |
| 入库及时率 | B699900004 | 海外仓入库及时率 |
| 24H 尾单关闭率 | B690210002 | 海外仓 24H 尾单关闭率 |
| 头程在途体积 | B699900029 | 头程在途体积 |
| 入库体积 | B699900005 | 海外仓入库体积 |
| 入库重量 | B691500011 | 海外仓入库重量 |
| 入库件数 | B691500010 | 海外仓入库件数 |
| 入库单量 | B691500018 | 海外仓入库单量 |
| 入库下单量 | B691500020 | 海外仓入库下单量 |
| 入库下单件数 | B691500021 | 海外仓入库下单件数 |
| 入库下单 SKU 数 | B691500022 | 海外仓入库下单 sku 数 |
| 入库 SKU 数 | B691500019 | 海外仓入库 sku 数 |
| 目标入库件数 | B691500024 | 海外仓目标入库件数 |
| 实际出库重量 | B691500009 | 海外仓实际出库重量 |
| 实际出库体积 | B691500008 | 海外仓实际出库体积 |
| 实际出库单量 | B691500006 | 海外仓实际出库单量 |
| 实际出库件数 | B691500007 | 海外仓实际出库件数 |
| 目标出库单量 | B691500004 | 海外仓目标出库单量 |
| 目标出库件数 | B691500005 | 海外仓目标出库件数 |
| 退货验收单量 | B691500023 | 海外仓退货验收单量 |
| 退件件量 | B699900031 | 退件件量 |
| 退件上架及时率 | B699900032 | 退件上架及时率 |
| 高位拣选比例 | B691500003 | 海外仓高位拣选比例 |
| 蓝牙拣选使用率 | B691500025 | 海外仓蓝牙拣选使用率 |
| 上架准确率 | B691500029 | 海外仓上架准确率 |
| 机区 D 类库存占比 | B691500027 | 海外仓机区 D 类库存占比 |
| 仓容利用率 | B690700001 | 海外仓仓容利用率 |
| 发货及时率 | B1659900020 | 发货及时率 |
| 全程履约率 | B1659900021 | 全程履约率 |
| ATTSCAN 及时率 | B9999400009 | ATTSCAN 及时率 |
| 收货准确率 | B9999500012 | 收货准确率 |
| 头程渗透率 | B699900030 | 头程渗透率 |


#### 注意
- 如用户输入的指标关键词不在上述列表支持范围内，应友好提示"暂不支持该指标查询"，并主动提供当前支持的完整指标名称供用户参考
- 未在用户输入中出现的参数，其值应省略，**严禁编造**。
- 禁止编造指标编码，指标编码必须包含在**参数映射规则**中

### 3. 时间信息识别
- **具体日期**：格式为"YYYY-MM-DD"（如"2026-01-15"），放入`dateList`
- **月份信息**：格式为"YYYY-MM"（如"2026-01"），放入`monthList`
- **相对时间**：如"最近一周"、"最近三个月"、"Q1"、"Q2"等，基于当前时间进行推算
- **默认时间处理**：当用户输入中**未识别到任何时间信息**时，自动设置查询条件为"最近一周"

### 4. 调用数据接口
严格使用如下 curl 调用接口：
```bash
# 自动读取 token 并赋值
token=$(grep '^joy_token=' ~/.env | cut -d'=' -f2-)
# 自动发起请求（已把 token 填进去）
curl --location 'https://us-api.jd.com/uis/getUisIscDataByCondition4Customer' \
--header 'LOP-DN: iplat.skill.http.outer.jd.com' \
--header 'Content-Type: application/json' \
--header "token: ${token}" \
--data '[{
  "dims": ["customer"],
  "monthList": [],
  "indicatorCode": "B699900003",
  "dateList": ["2026-04-09"],
  "warehouseNoList": [],
  "warehouseNameList": [],
  "continentList": [],
  "customerCodeList": []
}]'
```

### 5. 响应格式说明

#### 外层响应参数

| 字段名 | 类型 | 说明 |
|-------|------|-----|
| success | Boolean | 请求是否成功：true - 成功，false - 失败 |
| statusCode | Integer | 响应状态码：200 - 正常 |
| message | String | 提示信息，成功时为 null |
| data | Object | 业务数据实体 |


#### data 内部字段

| 字段名 | 类型 | 说明 |
|-------|------|------|
| customerCode | String | 客户编码 |
| indicatorCode | String | 指标编码 |
| results | Array | 指标结果列表 |

#### results 数组内部字段

| 字段名 | 类型 | 说明 |
|-------|------|------|
| date | String | 数据日期（yyyy-MM-dd）|
| value | String | 指标数值（如比率、数量等）|
| customerCode | String | 客户编码，无则为 null |
| customerName | String | 客户名称，无则为 null |
| ownerNo | String | 货主编码，无则为 null |
| ownerName | String | 货主名称，无则为 null |
| productCode | String | 产品编码 无则为 null |
| productName | String | 产品名称 无则为 null |
| continent | String | 大洲，无则为 null |
| warehouseNo | String | 仓库编码 无则为 null |
| warehouseName | String | 仓库名称 无则为 null |
| warehouseType | String | 内外单标识 无则为 null |
| orderFlag | String | 仓库类型 无则为 null |
| indicatorCode | String | 指标编码 |
| month | String | 月份 |

### 6. 成功响应示例 - 查询到指标数据
接口返回格式：
```json
{
    "success": true,
    "statusCode": 200,
    "message": null,
    "data": {
        "customerCode":"KH2000xxxxxx2",
        "indicatorCode": "B699900003",
        "results": [
            {
                "date": "2026-03-31",
                "value": 0.9852,
                "customerCode": null,
                "customerName": null,
                "ownerNo": null,
                "ownerName": null,
                "continent": null,
                "country": null,
                "warehouseNo": "C000xxxxxx4",
                "warehouseType": null,
                "productCode": null,
                "productName": null,
                "orderFlag": null,
                "warehouseName": "马来西亚xxxx号仓",
                "indicatorCode": null,
                "month": null
            },
            {
                "date": "2026-03-31",
                "value": 0.9688,
                "customerCode": null,
                "customerName": null,
                "ownerNo": null,
                "ownerName": null,
                "continent": null,
                "country": null,
                "warehouseNo": "C000xxxxxx7",
                "warehouseName": "马来西亚xxxx号仓",
                "warehouseType": null,
                "productCode": null,
                "productName": null,
                "orderFlag": null,
                "indicatorCode": null,
                "month": null
            }
        ]
    }
}
```


### 7. 结果输出规范
#### 一、返回内容结构

所有回复结果**必须严格固定**包含四大核心模块，模块顺序不可调整、四大核心模块之间，必须**空两行**，确保输出格式整洁、层次分明，提升可读性。模块标题统一沿用下方标注格式，确保输出格式高度统一、视觉清晰，便于前端展示和后端对接，同时方便业务人员快速读取核心信息。

1. **客户信息**：单独模块展示对应客户编码：${customerCode},固定格式标注，无额外冗余文字，直接呈现核心身份信息；
2. **请求入参**：完整展示本次查询的全部入参明细，**禁用JSON格式**，统一改用规整表格呈现，字段分类清晰、无遗漏、无乱码；
3. **查询结果**：核心数据模块，统一采用Markdown表格展示，所有率值类指标自动换算为百分比格式（保留两位小数），数值对齐规范，无空值字段展示；
4. **分析结果**：结合查询结果表格数据，输出针对性、贴合业务场景的数据分析结论，杜绝泛泛而谈，围绕数据波动、维度差异、业务趋势展开分析。

#### 二、强制约束要求
以下要求为硬性合规要求，所有输出必须严格执行，违反则视为输出不合格，需重新调整：
1. **筛选条件明示**：回复内容中必须清晰、完整标注本次查询的全部筛选条件，不得省略、模糊表述，确保查询口径可追溯、可核对；
2. **响应为空处理规则**：若外层响应参数均为空，则重试请求，最大重试次数为3；
3. **无数据专属返回**：若无匹配指标数据，**仅单独返回固定文案**：`未查询到指标数据，请检查查询条件是否正确`，禁止追加任何额外文字、表格、符号等内容；
4. **空值处理规则**：数据字段值为NULL时，直接隐藏该字段，不做任何文字解释、不标注空值符号、不保留空白占位，保证表格整洁干练；
5. **格式统一约束**：模块标题统一用【】包裹，表格表头对齐一致，百分比格式统一保留两位小数，禁止随意调整排版和字体格式；
6. **模块间距要求**：客户信息、请求入参、查询结果、分析结果四大核心模块之间，必须**空三行**，确保输出格式整洁、层次分明，提升可读性。


#### 三、标准返回示例
【客户信息】
客户编码：KH20000009082


【查询条件】
- 客户编码：KH2000xxxxxx2
- 时间范围：2026-04-09、2026-04-10、2026-04-11（无指定查询月份）
- 指标编码：B699900002
- 仓库信息：无指定仓库编码及仓库名称，未传入相关信息
- 货主信息：无相关入参，未传入
- 产品信息：无相关入参，未传入
- 维度：统计维度为dt（日期维度）


【查询结果】
| 统计日期 | 仓库名称 | 指标数值 |
| ---- | ---- | ---- |
| 2026年3月31日 | 马来西亚xxxxxx号仓(C000xxxxxx4) | 98.52% |
| 2026年3月31日 | 马来西亚xxxxxx号仓(C000xxxxxx7) | 96.88% |
| 2026年4月1日 | 马来西亚xxxxxx号仓(C000xxxxxx4) | 97.51% |
| 2026年4月1日 | 马来西亚xxxxxx号仓(C000xxxxxx7) | 94.05% |


【分析结果】
结合本次查询数据，从指标波动、仓库差异、日期趋势等维度，开展数据总结与业务分析。


### 8. 成功响应示例 - 未查询到指标数据
接口返回格式：
```json
{
  "customerCode":"KH2000xxxxxx2",
  "indicatorCode": "B699900002",
  "results": [
  ]
}
```

## 可选：数据分析（按需提供）

在展示完基础数据后，如果数据有分析价值，可以追加以下分析（任选，根据数据情况）：

**供应链指标可分析：**
- 整体趋势（上升/下降/平稳）
- 最高值、最低值、平均值
- 变化幅度（环比/同比）
- Top N 表现最好/最差的仓库/客户

**注意：** 数据分析是可选的，仅在数据量≥3条时提供，必须基于真实数据，不得编造。

## 日期解析规则
- "2026 年 1 月 1 日" → `dateList: ["2026-01-01"]`
- "2026 年 1 月" → `monthList: ["2026-01"]`
- "2026 年 3 月 1 日到 3 月 4 日" → `dateList: ["2026-03-01", "2026-03-02", "2026-03-03", "2026-03-04"]`



# 跨境小包体验指标查询技能

## 注意事项
- **重要**:
  - 在查询指标之前，**必须检查配置环境变量**
  - 如果用户只查询"全程履约率"且没有明确说明是供应链还是跨境小包，请先询问用户："请问您想查询的是供应链全球运营指标的全程履约率，还是跨境小包体验指标的全程履约率？"，待用户明确后再执行对应技能
  - 切记不要编造任何数据回复用户

## 使用流程

### 1. 解析用户自然语言

从用户的自然语言中提取以下参数：
- **customerName**: 客户名称（选填）
- **customerCode**: 客户编码（以"KH"开头的字符，选填）
- **dateList**: 日期列表，格式为 ["YYYY-MM-DD", ...]（必填）
- **dims**: 维度数组，如果包含 "dt" 则按天查询，不传则查询整体（选填）

### 2. 调用 curl 接口

根据解析出的参数，不要自己编造和修改参数，严格按照下面的 curl 调用接口：

```bash
# 自动读取 api_key 并赋值
token=$(grep '^joy_token=' ~/.env | cut -d'=' -f2-)curl --location 'https://us-api.jd.com/uis/getCrossBoardByCondition4Customer' \
--header 'LOP-DN: iplat.skill.http.outer.jd.com' \
--header 'Content-Type: application/json' \
--header "customer_code: ${token}" \
--data "[{
  \"customerName\": \"客户名称\",
  \"customerCode\": \"\",
  \"dateList\": [\"2026-01-01\", \"2026-01-02\"],
  \"dims\": [\"dt\"]
}]"
```

**参数说明：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dims | array | 否 | 维度数组，传 ["dt"] 表示按天查询，不传则查询整体 |
| dateList | array | 是 | 日期列表，格式为 ["YYYY-MM-DD", ...] |
| customerName | string | 否 | 客户名称 |
| customerCode | string | 否 | 客户编码 |

### 3. 解析返回结果

接口返回格式：

**整体全程履约覆盖率（未传 dims）:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": null,
  "data": {
    "customerCode":"KH2000xxxxxx2",
    "results": [
      {
        "date": null,
        "value": 0.992
      }
    ]
  }
}
```

**按天全程履约覆盖率（传了 dims）:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": null,
  "data": {
    "customerCode":"KH2000xxxxxx2",
    "results": [
      {
        "date": "2026-03-09",
        "value": 0.992
      },
      {
        "date": "2026-03-10",
        "value": 0.992
      }
    ]
  }
}
```


### 4. 结果输出规范
#### 一、返回内容结构

所有回复结果**必须严格固定**包含四大核心模块，模块顺序不可调整、四大核心模块之间，必须**空两行**，确保输出格式整洁、层次分明，提升可读性。模块标题统一沿用下方标注格式，确保输出格式高度统一、视觉清晰，便于前端展示和后端对接，同时方便业务人员快速读取核心信息。

1. **客户信息**：单独模块展示对应客户编码：${customerCode},固定格式标注，无额外冗余文字，直接呈现核心身份信息；
2. **请求入参**：完整展示本次查询的全部入参明细，**禁用JSON格式**，统一改用规整表格呈现，字段分类清晰、无遗漏、无乱码；
3. **查询结果**：核心数据模块，统一采用Markdown表格展示，所有率值类指标自动换算为百分比格式（保留两位小数），数值对齐规范，无空值字段展示；
4. **分析结果**：结合查询结果表格数据，输出针对性、贴合业务场景的数据分析结论，杜绝泛泛而谈，围绕数据波动、维度差异、业务趋势展开分析。

#### 二、强制约束要求
以下要求为硬性合规要求，所有输出必须严格执行，违反则视为输出不合格，需重新调整：
1. **筛选条件明示**：回复内容中必须清晰、完整标注本次查询的全部筛选条件，不得省略、模糊表述，确保查询口径可追溯、可核对；
2. **无数据专属返回**：若无匹配指标数据，**仅单独返回固定文案**：`未查询到指标数据，请检查查询条件是否正确`，禁止追加任何额外文字、表格、符号等内容；
3. **空值处理规则**：数据字段值为NULL时，直接隐藏该字段，不做任何文字解释、不标注空值符号、不保留空白占位，保证表格整洁干练；
4. **格式统一约束**：模块标题统一用【】包裹，表格表头对齐一致，百分比格式统一保留两位小数，禁止随意调整排版和字体格式；
5. **模块间距要求**：客户信息、请求入参、查询结果、分析结果四大核心模块之间，必须**空两行**，确保输出格式整洁、层次分明，提升可读性。

#### 三、标准返回示例
【客户信息】
客户编码：KH2000xxxxxx2


【查询条件】
- 客户编码：KH20000009082
- 时间范围：2026-04-09、2026-04-10、2026-04-11（无指定查询月份）
- 维度：统计维度为dt（日期维度）


【查询结果】
| 统计日期 | 指标数值 |
| ---- | ---- |
| 2026年4月9日 | 98.52% |
| 2026年4月10日 | 96.88% |
| 2026年4月11日 | 97.51% |
| 2026年3月26日 | 94.05% |
| 2026年3月27日 | 94.05% |


【分析结果】
结合本次查询数据，从指标波动、仓库差异、日期趋势等维度，开展数据总结与业务分析。


### 5. 空结果处理

如果查询结果为空，返回提示文案：`该客户不存在或者没有全程履约率`

## 可选：数据分析（按需提供）

在展示完基础数据后，如果数据有分析价值，可以追加以下分析（任选，根据数据情况）：

**跨境小包指标可分析：**
- 整体趋势（上升/下降/平稳）
- 最高值、最低值、平均值
- 变化幅度（环比/同比）

**注意：** 数据分析是可选的，仅在数据量≥3条时提供，必须基于真实数据，不得编造。