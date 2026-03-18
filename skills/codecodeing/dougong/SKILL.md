---
name: huifu-hosting-payment
description: "Integrates Huifu hosting payment SDK for Java backend projects, covering pre-order creation, order status query, and refund operations. Triggers on keywords: pre-order, payment, order query, refund, hosting payment, or /hfpay endpoints."
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - HUIFU_PRODUCT_ID
        - HUIFU_SYS_ID
        - HUIFU_RSA_PRIVATE_KEY
        - HUIFU_RSA_PUBLIC_KEY
        - HUIFU_NOTIFY_URL
        - HUIFU_REFUND_NOTIFY_URL
        - HUIFU_PROJECT_ID
        - HUIFU_PROJECT_TITLE
        - HUIFU_CALLBACK_URL
      bins:
        - java
        - mvn
---

# 汇付托管支付接口

集成汇付 SDK 实现托管支付的完整链路：预下单 → 订单查询 → 退款。

## 引导词

当开发者提到以下关键词时，本技能被触发：

- 预下单、支付预下单、托管支付、创建支付订单
- 订单查询、支付查询、查询订单、支付状态
- 退款、支付退款、订单退款、refund
- /hfpay/preOrder、/hfpay/queryorderinfo、/hfpay/htRefund

## 前置检查

在编写代码之前，必须完成以下检查：

### 步骤1：检查 SDK 依赖

检查项目 `pom.xml` 中是否包含 `dg-java-sdk` 依赖：

```xml
<dependency>
    <groupId>com.huifu.bspay.sdk</groupId>
    <artifactId>dg-java-sdk</artifactId>
    <version>3.0.34</version>
</dependency>
```

### 步骤2：安装依赖（如未安装）

在 `pom.xml` 中添加上述依赖后执行：

```bash
mvn clean install
```

### 步骤3：验证导入

确认以下核心类可正常导入：

- `com.huifu.bspay.sdk.opps.core.BasePay`
- `com.huifu.bspay.sdk.opps.core.config.MerConfig`
- `com.huifu.bspay.sdk.opps.client.BasePayClient`
- `com.huifu.bspay.sdk.opps.core.utils.DateTools`
- `com.huifu.bspay.sdk.opps.core.utils.SequenceTools`

各场景所需的 Request 类：

| 场景 | Request 类 |
|-----|-----------|
| 预下单 | `V2TradeHostingPaymentPreorderH5Request` |
| 订单查询 | `V2TradeHostingPaymentQueryorderinfoRequest` |
| 退款 | `V2TradeHostingPaymentHtrefundRequest` |

**只有完成以上前置检查后，才能继续按照 reference 目录中的示例代码进行开发。**

### javax / jakarta 命名空间说明

示例代码使用 `javax.annotation` 和 `javax.validation` 命名空间（适用于 Spring Boot 2.x）。如果项目使用 **Spring Boot 3.x + JDK 17/21**，需将 `javax` 替换为 `jakarta`：

| Spring Boot 2.x (javax) | Spring Boot 3.x (jakarta) |
|--------------------------|---------------------------|
| `javax.annotation.PostConstruct` | `jakarta.annotation.PostConstruct` |
| `javax.validation.constraints.NotBlank` | `jakarta.validation.constraints.NotBlank` |

## 场景路由

根据用户意图选择对应场景：

| 用户意图 | 场景 | 接口路径 | 详细说明 |
|---------|------|---------|---------|
| 创建支付订单 | **预下单** | `POST /hfpay/preOrder` | 见 [SCENARIOS.md #预下单](SCENARIOS.md#预下单) |
| 查询订单状态 | **订单查询** | `POST /hfpay/queryorderinfo` | 见 [SCENARIOS.md #订单查询](SCENARIOS.md#订单查询) |
| 对已支付订单退款 | **退款** | `POST /hfpay/htRefund` | 见 [SCENARIOS.md #退款](SCENARIOS.md#退款) |

**根据用户描述的场景，读取 [SCENARIOS.md](SCENARIOS.md) 中对应章节获取请求参数、响应参数和实现细节。**

## 通用架构设计

三个场景共享同一套分层架构和商户配置：

```
HuifuConfig (@Configuration)
    └── @PostConstruct initSdk() — 初始化 SDK（仅应用启动时执行一次）

HFPayController (@RestController, /hfpay)
    ├── POST /preOrder      → hostingPayService.preOrder(req)
    ├── POST /queryorderinfo → hostingPayService.queryOrderInfo(req)
    └── POST /htRefund      → hostingPayService.htRefund(req)

HostingPayService (@Service, 构造器注入 ObjectMapper)
    ├── preOrder()       → 组装请求 → BasePayClient.request() → 返回响应
    ├── queryOrderInfo() → 组装请求 → BasePayClient.request() → 返回响应
    └── htRefund()       → 组装请求 → BasePayClient.request() → 返回响应

DTO层（含 @NotBlank 校验）
    ├── HostingPayPreOrderReq
    ├── HostingPayQueryOrderReq
    └── HostingPayHtRefundReq
```

### 交易状态枚举（通用）

| 状态码 | 含义 | 建议处理方式 |
|-------|------|------------|
| P | 处理中 | 等待异步通知或轮询查询 |
| S | 交易成功 | 执行业务成功逻辑 |
| F | 交易失败 | 提示用户重新发起或联系客服 |

## 代码示例

详见 [reference](reference/) 目录下的示例代码文件：

| 文件 | 说明 |
|-----|------|
| [HuifuConfig.java](reference/HuifuConfig.java) | SDK 配置初始化类（@Configuration + @PostConstruct） |
| [HFPayController.java](reference/HFPayController.java) | Controller 层（三个接口端点） |
| [HostingPayService.java](reference/HostingPayService.java) | Service 层（三个场景的业务方法） |
| [HostingPayPreOrderReq.java](reference/HostingPayPreOrderReq.java) | 预下单请求 DTO |
| [HostingPayQueryOrderReq.java](reference/HostingPayQueryOrderReq.java) | 订单查询请求 DTO |
| [HostingPayHtRefundReq.java](reference/HostingPayHtRefundReq.java) | 退款请求 DTO |
| [Result.java](reference/Result.java) | 统一响应封装 |

## 安全规则

1. **严禁在源代码中硬编码商户密钥**，必须通过 `application.yml` 配置并使用环境变量注入
2. **notify_url 和 callback_url 必须替换为实际业务地址**，禁止使用任何测试域名
3. 退款操作涉及资金变动，日志中应记录关键参数但避免打印完整密钥信息
4. hosting_data 中的 `project_id` 需替换为实际项目 ID

## 环境变量配置

`application.yml` 配置示例：

```yaml
huifu:
  product-id: ${HUIFU_PRODUCT_ID}
  sys-id: ${HUIFU_SYS_ID}
  rsa-private-key: ${HUIFU_RSA_PRIVATE_KEY}
  rsa-public-key: ${HUIFU_RSA_PUBLIC_KEY}
  notify-url: ${HUIFU_NOTIFY_URL}
  refund-notify-url: ${HUIFU_REFUND_NOTIFY_URL}
  hosting:
    project-id: ${HUIFU_PROJECT_ID}
    project-title: ${HUIFU_PROJECT_TITLE}
    callback-url: ${HUIFU_CALLBACK_URL}
```
