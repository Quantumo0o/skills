---
name: pugoing-smart
description: 提供 common API calls to Pugoing centralized control platform，用于查询区域、主机、设备，以及通过自然语言控制设备。
---


# Pugoing Smart

这个目录给龙虾或其他 Agent 用，目标是用最少的上下文完成对蒲公英集控平台的常见调用。

## 鉴权方式

推荐使用环境变量传 API Key，这也是很多同类技能最常见的做法。

需要的环境变量：

```bash
export PUGOING_BASE_URL="http://127.0.0.1:8080"
export PUGOING_API_KEY="xq_agent_xxx"
```

可选环境变量：

```bash
export PUGOING_BEARER_TOKEN="..."
export PUGOING_TIMEOUT="30"
```

默认鉴权：

- `auth=agent` 时，脚本自动带 `X-API-Key: $PUGOING_API_KEY`
- `auth=bearer` 时，脚本自动带 `Authorization: Bearer $PUGOING_BEARER_TOKEN`
- `auth=none` 时，不带鉴权头

## 通用调用对象

推荐传一个 JSON 对象给 `client.py`：

```json
{
  "path": "/api/xq_host/list",
  "method": "GET",
  "params": {},
  "data": {},
  "auth": "agent"
}
```

字段说明：

- `path`: 相对路径，推荐写法
- `url`: 也支持完整 URL；若同时给了 `url`，优先使用 `url`
- `method`: `GET` 或 `POST`
- `params`: 查询参数
- `data`: JSON body
- `auth`: `agent` / `bearer` / `none`
- `headers`: 额外请求头
- `timeout`: 单次请求超时秒数

## 常见能力

### 1. 查区域和主机

调用：

- `/api/host_area/list`

返回重点：

- `data.tree`: 区域树，区域下带 `hosts`
- `data.unpartitioned`: 未分区主机

示例：

```bash
python pugoing_smart/client.py pugoing_smart/examples/list_areas_and_hosts.json
```

### 2. 查主机

调用：

- `/api/xq_host/list`

返回重点：

- 主机列表
- 每个主机的 `ip`、`name`、`area_name`、`is_online`

示例：

```bash
python pugoing_smart/client.py pugoing_smart/examples/list_hosts.json
```

### 3. 查某个主机下的设备

调用：

- `/api/device/sync?host_ip=...`

说明：

- 优先从主机同步设备
- 主机不可达时会回退本地缓存

示例：

```bash
python pugoing_smart/client.py pugoing_smart/examples/list_host_devices.json
```

### 4. 用自然语言控制设备

调用：

- `/api/device/control/voice`

推荐只用：

- `host_ip`
- `dvcm`

示例：

```bash
python pugoing_smart/client.py pugoing_smart/examples/control_device_by_dvcm.json
```

请求体示例：

```json
{
  "host_ip": "192.168.1.88",
  "dvcm": "打开客厅灯"
}
```

### 5. 万能兜底：调用内置 AI

调用：

- `/api/ai/chat`

建议：

- 平台级查询或跨主机场景时，`host_ip` 传 `"global"`
- 单主机设备控制或上下文理解时，`host_ip` 传实际主机 IP
- `need_tts` 对接龙虾时通常设为 `false`

`client.py` 会自动把这个 SSE 接口收集为普通 JSON 输出，所以可以当普通接口用。

示例：

```bash
python pugoing_smart/client.py pugoing_smart/examples/ai_fallback.json
```

## 建议的调用顺序

当需求明确时，优先直调平台 API：

1. 先查区域和主机
2. 再查主机设备
3. 能直接用 `dvcm` 控制就直接控制

当需求模糊或要兜底时，再走内置 AI：

1. `/api/ai/chat`
2. `host_ip=global` 适合问“平台里有什么”
3. `host_ip=<实际主机IP>` 适合问“帮我控制这个主机下的设备”

## 目录内容

- `client.py`: 通用调用脚本
- `examples/list_areas_and_hosts.json`: 查区域和主机
- `examples/list_hosts.json`: 查主机列表
- `examples/list_host_devices.json`: 查某台主机设备
- `examples/control_device_by_dvcm.json`: 用 `dvcm` 控制设备
- `examples/ai_fallback.json`: 调内置 AI 兜底
