# 场景详细说明

## 预下单

创建支付预订单，返回支付页面 URL 或支付参数，用于后续支付流程。

### 接口说明

| 属性 | 值 |
|-----|-----|
| 接口路径 | `/hfpay/preOrder` |
| 请求方式 | POST |
| Content-Type | application/json |
| 汇付API端点 | `v2/trade/hosting/payment/preorder` |

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| huifuId | String | 是 | 商户号 |
| transAmt | String | 是 | 交易金额（单位：元，如 "1.00"） |
| goodsDesc | String | 是 | 商品描述 |
| preOrderType | String | 否 | 预下单类型，默认 "1"。1=H5/PC；2=支付宝小程序；3=微信小程序 |
| notifyUrl | String | 否 | 支付结果异步通知地址，未传则使用配置文件默认值 |

### 响应参数

| 参数名 | 类型 | 说明 |
|-------|------|------|
| resp_code | String | 响应码，`00000000` 表示成功 |
| resp_desc | String | 响应描述 |
| req_seq_id | String | 请求流水号（后续查询/退款需用到） |
| req_date | String | 请求日期（后续查询/退款需用到） |
| pay_url | String | 支付页面地址，引导用户跳转完成支付 |
| huifu_id | String | 商户号 |
| trans_amt | String | 交易金额 |
| trans_stat | String | 交易状态：P=处理中，S=成功，F=失败 |

### 实现步骤

1. 创建请求 DTO 类 `HostingPayPreOrderReq`，使用 `@NotBlank` 注解标记必填字段
2. 在 Service 层实现 `preOrder` 方法，组装 `V2TradeHostingPaymentPreorderH5Request`
3. 在 Controller 层添加 `POST /preOrder` 端点，使用 `@Validated` 触发参数校验

### 注意事项

1. `pre_order_type` 参数说明：1=H5/PC 预下单；2=支付宝小程序；3=微信小程序
2. 需要正确配置 `notify_url` 以接收支付结果异步通知
3. `hosting_data` 为半支付托管扩展参数，需根据实际项目配置
4. **调用成功后务必保存返回的 `req_seq_id` 和 `req_date`，后续订单查询和退款均需使用**

---

## 订单查询

查询订单支付状态和详细信息，包括交易状态、金额、时间等。

### 接口说明

| 属性 | 值 |
|-----|-----|
| 接口路径 | `/hfpay/queryorderinfo` |
| 请求方式 | POST |
| Content-Type | application/json |
| 汇付API端点 | `v2/trade/hosting/payment/queryorderinfo` |

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| huifuId | String | 是 | 商户号 |
| orgReqDate | String | 是 | 原交易请求日期（格式：yyyyMMdd），来自预下单响应的 `req_date` |
| orgReqSeqId | String | 是 | 原交易请求流水号，来自预下单响应的 `req_seq_id` |

**参数说明**: `orgReqDate` 和 `orgReqSeqId` 均来自预下单接口的响应。`reqDate`（本次查询请求日期）由系统自动生成，无需传入。

### 响应参数

| 参数名 | 类型 | 说明 |
|-------|------|------|
| resp_code | String | 响应码，`00000000` 表示成功 |
| resp_desc | String | 响应描述 |
| trans_stat | String | 交易状态：P=处理中，S=成功，F=失败 |
| trans_amt | String | 交易金额 |
| huifu_id | String | 商户号 |
| org_req_date | String | 原交易请求日期 |
| org_req_seq_id | String | 原交易请求流水号 |

### 实现步骤

1. 创建请求 DTO 类 `HostingPayQueryOrderReq`，使用 `@NotBlank` 注解标记必填字段
2. 在 Service 层实现 `queryOrderInfo` 方法，组装 `V2TradeHostingPaymentQueryorderinfoRequest`
3. 在 Controller 层添加 `POST /queryorderinfo` 端点，使用 `@Validated` 触发参数校验

### 注意事项

1. 需要传入原交易的请求日期和请求流水号，这两个值来自预下单接口的响应
2. 建议在收到异步通知后调用查询接口进行二次确认，确保状态一致
3. 查询结果中可能包含敏感信息，日志中避免打印完整响应体

---

## 退款

对已支付订单发起退款申请，支持全额或部分退款。

### 接口说明

| 属性 | 值 |
|-----|-----|
| 接口路径 | `/hfpay/htRefund` |
| 请求方式 | POST |
| Content-Type | application/json |
| 汇付API端点 | `v2/trade/hosting/payment/htRefund` |

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| huifuId | String | 是 | 商户号 |
| ordAmt | String | 是 | 申请退款金额（单位：元，如 "1.00"），不能超过原交易金额 |
| orgReqDate | String | 是 | 原交易请求日期（格式：yyyyMMdd），来自预下单响应的 `req_date` |
| orgReqSeqId | String | 是 | 原交易请求流水号，来自预下单响应的 `req_seq_id` |

### 响应参数

| 参数名 | 类型 | 说明 |
|-------|------|------|
| resp_code | String | 响应码，`00000000` 表示成功 |
| resp_desc | String | 响应描述 |
| trans_stat | String | 退款状态：P=处理中，S=成功，F=失败 |
| ord_amt | String | 退款金额 |
| huifu_id | String | 商户号 |
| org_req_date | String | 原交易请求日期 |
| org_req_seq_id | String | 原交易请求流水号 |

### 实现步骤

1. 创建请求 DTO 类 `HostingPayHtRefundReq`，使用 `@NotBlank` 注解标记必填字段
2. 在 Service 层实现 `htRefund` 方法，组装 `V2TradeHostingPaymentHtrefundRequest`
3. 在 Controller 层添加 `POST /htRefund` 端点，使用 `@Validated` 触发参数校验

### 注意事项

1. 需要传入原交易的请求日期和请求流水号，这两个值来自预下单接口的响应
2. 退款金额不能超过原交易金额，汇付 API 侧会进行校验并返回错误，建议在业务层也做前置校验
3. `terminal_device_data` 为设备信息，线上交易退款必填。`device_type` 枚举：1=SDK；2=手机浏览器；3=PC浏览器；4=公众号/小程序
4. 需要正确配置 `notify_url` 以接收退款结果异步通知
5. 重复退款请求：如果使用相同的 `orgReqSeqId` 发起重复退款，汇付 API 会返回错误，需在业务层做幂等校验
