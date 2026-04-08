---
name: dougong-aggregation-aggregate-refund
display_name: 汇付聚合支付退款
description: "汇付聚合支付（dg-lightning-sdk）退款 Skill：聚合交易退款和退款结果查询。当开发者需要对聚合支付订单发起退款或查询退款状态时使用。触发词：聚合退款、聚合退款申请、聚合退款查询、聚合退款状态。"
version: 1.0.0
author: "jiaxiang.li | 内容版权：上海汇付支付有限公司"
homepage: https://paas.huifu.com/open/home/index.html
license: MIT
compatibility:
  - openclaw
dependencies:
  - dougong-aggregation-pay-base
metadata:
  openclaw:
    requires:
      bins:
        - java
        - mvn
      config:
        - HUIFU_PRODUCT_ID
        - HUIFU_SYS_ID
        - HUIFU_RSA_PRIVATE_KEY
        - HUIFU_RSA_PUBLIC_KEY
        - HUIFU_REFUND_NOTIFY_URL
---

> **版权声明**：本 Skill 内容来源于上海汇付支付有限公司官方开放平台文档，版权归属上海汇付支付有限公司。如有疑问可咨询汇付支付客服：400-820-2819 / cs@huifu.com
>
> **Source**: Official Open Platform documentation of Shanghai Huifu Payment Co., Ltd.
>
> **Copyright**: Shanghai Huifu Payment Co., Ltd.

---

# 聚合支付 - 退款

交易退款 + 退款结果查询。

## 运行依赖与凭据边界

本 Skill 依赖 [dougong-aggregation-pay-base](../dougong-aggregation-pay-base/SKILL.md) 提供公共运行时与商户配置约束。metadata 中列出的 `HUIFU_PRODUCT_ID`、`HUIFU_SYS_ID`、`HUIFU_RSA_PRIVATE_KEY`、`HUIFU_RSA_PUBLIC_KEY` 用于让接入方应用在运行时完成 `dg-lightning-sdk` 初始化，并由 SDK 在应用侧完成请求签名和响应验签；本 Skill 本身只提供接入说明，不会在 Skill 包内保存、打印、上传或持久化这些凭据。

> **前置依赖**：首次接入请先阅读 [dougong-aggregation-pay-base](../dougong-aggregation-pay-base/SKILL.md) 完成 SDK 初始化。

> **进入本 Skill 前先确认**：原交易定位键已经在订单侧沉淀，退款请求也按 [payload-construction.md](../dougong-aggregation-pay-base/references/payload-construction.md) 做过必填 / 条件必填校验，避免把缺少原交易标识的请求直接打到汇付。

## 触发词

- "聚合退款"、"聚合退款申请"、"聚合交易退款"
- "聚合退款查询"、"聚合退款状态"、"查询聚合退款结果"

## 场景路由

| 用户意图 | 场景 | 详细说明 |
|---------|------|---------|
| 对已支付订单发起退款 | 交易退款 | 见 [refund.md](references/refund.md) |
| 查询退款结果 | 退款结果查询 | 见 [refund-query.md](references/refund-query.md) |

## 退款流程

```text
1. 确认原交易已支付成功（trans_stat=S）
2. 调用退款接口 v4/trade/payment/scanpay/refund
3. 退款 resp_code=00000100（处理中）是正常的
4. 等待异步通知或轮询退款查询接口
5. 退款成功（trans_stat=S）后执行业务退款逻辑
```

## 退款期限

| 渠道 | 最大退款期限 |
|------|-----------|
| 微信 | 360天 |
| 支付宝 | 360天 |
| 银联二维码 | 360天 |

## 注意事项

1. **退款金额不能超过原交易金额**（延时交易退款金额须≤待确认金额）
2. `resp_code=00000000` 或 `00000100` 仅表示退款请求**已受理**
3. 退款最终结果以**异步通知**或**退款查询接口**为准
4. 退款成功后资金**原路返回**给用户
5. 退款为异步处理，请做好**幂等校验**
6. 原交易定位键为 `org_hf_seq_id`、`org_party_order_id`、`org_req_seq_id` 三选一
7. `remark`、`notify_url`、`tx_metadata` 通常通过 `client.optional()` 或 `request.optional()` 传入
8. 退款查询使用的是退款标识：`org_hf_seq_id`、退款 `org_req_seq_id`、`mer_ord_id` 三选一；传退款全局流水号时 `org_req_date` 可不传
9. 退款涉及资金变动，日志中记录关键参数但**避免打印完整密钥**

## 流水号关系

退款涉及三层流水号，需清楚关联关系：

```text
1. 原交易下单: req_seq_id = "A001"（原支付流水号）
2. 退款请求: req_seq_id = "B001"（退款流水号），org_req_seq_id = "A001"
3. 退款查询: org_req_seq_id = "B001"（查的是退款的流水号）
   org_hf_seq_id = 退款返回的 hf_seq_id（也可以用这个查）
```

> 快速接入代码示例见 [quickstart.md](references/quickstart.md)。

---

## 版权声明

本 Skill 的内容来源于 **上海汇付支付有限公司** 官方开放平台文档。

- **版权归属**：上海汇付支付有限公司
- **客服热线**：400-820-2819
- **客服邮箱**：cs@huifu.com
- **官方网站**：[https://www.huifu.com/](https://www.huifu.com/)
- **开放平台**：[https://paas.huifu.com/open/home/index.html](https://paas.huifu.com/open/home/index.html)

本 Skill 仅作技术学习交流使用，原始内容由汇付支付官方维护和更新。如有任何疑问或需要商业支持，请直接联系汇付支付官方客服。
