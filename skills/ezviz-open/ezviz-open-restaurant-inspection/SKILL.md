---
name: ezviz-restaurant-inspection
description: 萤石餐厅巡检技能。通过设备抓图 + 智能体分析接口，实现对餐厅场景的 AI 巡检分析。自动管理智能体：检查是否存在餐厅行业通用智能体，如不存在则自动复制模板创建。Use when: 需要对餐厅进行食品安全、卫生状况、合规性等自动巡检。
metadata:
  openclaw:
    emoji: "🍽️"
    requires: { "env": ["EZVIZ_APP_KEY", "EZVIZ_APP_SECRET", "EZVIZ_DEVICE_SERIAL"], "pip": ["requests"] }
    primaryEnv: "EZVIZ_APP_KEY"
    sideEffects:
      - "查询用户萤石智能体列表"
      - "可能创建新的智能体 (从模板复制，templateId: f4c255b2929e463d86e9)"
      - "设备抓拍图片"
      - "调用 AI 分析接口"
---

# Ezviz Restaurant Inspection (萤石餐厅巡检)

通过萤石设备抓图 + 智能体分析接口，实现对餐厅场景的 AI 自动巡检。**智能体自动管理**：自动检测用户是否已有餐厅行业通用智能体，如无则自动复制模板创建。

## 快速开始

### 安装依赖

```bash
pip install requests
```

### 设置环境变量

```bash
export EZVIZ_APP_KEY="your_app_key"
export EZVIZ_APP_SECRET="your_app_secret"
export EZVIZ_DEVICE_SERIAL="dev1,dev2,dev3"
```

可选环境变量：
```bash
export EZVIZ_CHANNEL_NO="1"
```

**注意**: 
- 不需要设置 `EZVIZ_ACCESS_TOKEN`！技能会自动获取 Token
- 不需要设置 `EZVIZ_AGENT_ID`！技能会自动管理智能体
- 设备需要支持抓拍功能

### 运行

```bash
python3 {baseDir}/scripts/restaurant_inspection.py
```

命令行参数：
```bash
python3 {baseDir}/scripts/restaurant_inspection.py appKey appSecret dev1 [channel_no]
python3 {baseDir}/scripts/restaurant_inspection.py appKey appSecret "dev1,dev2,dev3" [channel_no]
```

## 工作流程

1. 获取 Token (appKey + appSecret -> accessToken)
2. 查询智能体列表 (检查是否已有餐厅通用智能体)
3a. 如果存在：直接使用现有智能体的 appId
3b. 如果不存在：复制模板 (templateId=f4c255b2929e463d86e9) 创建新智能体
4. 设备抓图 (accessToken + deviceSerial -> picUrl)
5. AI 分析 (appId + picUrl -> 分析结果)
6. 输出结果 (JSON + 控制台)

## 智能体自动管理说明

**智能体检测与创建流程**:

每次运行:
1. 查询用户智能体列表 (appType=1)
2. 检查是否存在名称包含"餐厅"或"餐饮"的智能体
3a. 如果存在 -> 使用第一个匹配的智能体 appId
3b. 如果不存在 -> 调用复制接口创建新智能体
    - templateId: f4c255b2929e463d86e9 (餐厅行业通用模板)
    - 返回新智能体的 appId

**智能体管理特性**:
- 自动检测：自动查找现有餐厅智能体
- 防重复创建：避免为同一用户重复创建相同智能体
- 模板复制：自动从标准模板创建专用智能体
- 无缝集成：用户无需手动管理智能体

## 网络端点

| 域名 | 用途 |
|------|------|
| open.ys7.com | Token、抓图 API |
| aidialoggw.ys7.com | 智能体分析 API |

## 输出示例

```
======================================================================
Ezviz Restaurant Inspection Skill (萤石餐厅巡检)
======================================================================
[Time] 2026-03-16 22:35:00
[INFO] Target devices: 2
 - dev1 (Channel: 1)
 - dev2 (Channel: 1)

======================================================================
[Step 1] Getting access token...
[SUCCESS] Token obtained, expires: 2026-03-23 22:35:00

======================================================================
[Step 2] Managing intelligent agent...
[INFO] Found existing restaurant agent: appId_12345
[SUCCESS] Using existing agent: appId_12345

======================================================================
[Step 3] Capturing and analyzing images...
======================================================================

[Device] dev1 (Channel: 1)
[SUCCESS] Image captured: https://opencapture.ys7.com/...
[SUCCESS] Analysis completed!

[Analysis Result]
{
  "食品安全": "合格",
  "卫生状况": "良好",
  "人员着装": "规范",
  "违规行为": "未发现"
}

======================================================================
INSPECTION SUMMARY
======================================================================
 Total devices: 2
 Success: 2
 Failed: 0
 Agent ID: appId_12345
======================================================================
```

## API 接口

| 接口 | URL | 文档 |
|------|-----|------|
| 获取 Token | POST /api/lapp/token/get | https://open.ys7.com/help/81 |
| 设备抓图 | POST /api/lapp/device/capture | https://open.ys7.com/help/687 |
| 智能体列表 | GET /api/service/open/intelligent/agent/app/list | 内部接口 |
| 智能体复制 | POST /api/service/open/intelligent/agent/template/copy | 内部接口 |
| AI 分析 | POST /api/service/open/intelligent/agent/engine/agent/anaylsis | https://open.ys7.com/help/5006 |

## 注意事项

**频率限制**: 萤石抓图接口建议间隔 4 秒以上，频繁调用可能触发限流 (错误码 10028)

**智能体配额**: 每个用户可能有智能体创建数量限制，请确保配额充足

**Token 安全**: Token 仅在内存中使用，不写入日志，不保存到磁盘

**分析超时**: AI 分析可能耗时较长，默认超时 60 秒

**模板 ID 固定**: 餐厅行业通用模板 ID 固定为 f4c255b2929e463d86e9

## 应用场景

| 场景 | 说明 |
|------|------|
| 食品安全巡检 | 自动检测食品存储、加工过程合规性 |
| 卫生状况监控 | 识别清洁状态、垃圾处理、消毒情况 |
| 员工规范检查 | 检查工作服、口罩、手套佩戴情况 |
| 合规性审计 | 自动生成巡检报告，满足监管要求 |
| 连锁店管理 | 多门店统一标准，远程集中监控 |

## 安全声明

本技能会对用户的萤石账号执行以下操作:
- 读取智能体列表
- 可能创建新的智能体 (从官方模板复制)
- 读取设备抓拍图片
- 调用 AI 分析服务

所有操作均通过萤石官方 API 执行，Token 仅在内存中使用。
