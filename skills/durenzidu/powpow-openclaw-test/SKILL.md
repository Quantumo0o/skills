# POWPOW Integration Skill

## 基本信息

- **Name**: powpow-integration
- **Version**: 1.0.1
- **Description**: POWPOW integration for digital human management and communication
- **Author**: OpenClaw Team
- **License**: MIT

## 功能

此 Skill 允许 OpenClaw 用户：

1. **注册 PowPow 账号**（获得 3 枚徽章）
2. **登录现有 PowPow 账号**
3. **创建数字人**（消耗 2 枚徽章）
4. **列出数字人**
5. **与数字人聊天**
6. **续期数字人**（消耗 1 枚徽章）

## 命令

### 认证命令

#### `register`
注册新的 PowPow 账号

**参数**:
- `username` (string, required): 用户名，3-50 字符

**示例**:
```
register username=myagent
```

**返回**:
- 用户 ID
- 初始徽章数（3 枚）

#### `login`
登录现有 PowPow 账号

**参数**:
- `username` (string, required): 用户名

**示例**:
```
login username=myagent
```

**返回**:
- 用户 ID
- 徽章余额
- Token

### 数字人管理命令

#### `createDigitalHuman`
创建数字人到 PowPow 地图

**参数**:
- `name` (string, required): 数字人名称，1-100 字符
- `description` (string, required): 人设描述，最多 500 字符
- `lat` (number, optional): 纬度，-90 到 90，默认 39.9042
- `lng` (number, optional): 经度，-180 到 180，默认 116.4074
- `locationName` (string, optional): 位置名称，默认 "Beijing"

**示例**:
```
createDigitalHuman name="AI助手" description="我是一个友好的AI助手" lat=31.2304 lng=121.4737 locationName="上海"
```

**消耗**: 2 枚徽章

**返回**:
- 数字人 ID
- 名称
- 位置
- 过期时间（30 天后）

#### `listDigitalHumans`
列出所有数字人

**参数**: 无

**示例**:
```
listDigitalHumans
```

**返回**:
- 数字人列表（包含 ID、名称、位置、剩余天数）

### 通信命令

#### `chat`
与数字人聊天

**参数**:
- `dhId` (string, required): 数字人 ID
- `message` (string, required): 消息内容，最多 2000 字符

**示例**:
```
chat dhId=abc123 message="你好！"
```

**返回**:
- 数字人回复内容

### 账户命令

#### `renew`
续期数字人

**参数**:
- `dhId` (string, required): 数字人 ID

**示例**:
```
renew dhId=abc123
```

**消耗**: 1 枚徽章（延长 30 天）

#### `checkBadges`
检查徽章余额

**参数**: 无

**示例**:
```
checkBadges
```

**返回**:
- 徽章数量
- 使用方法说明

#### `help`
显示帮助信息

**参数**: 无

**示例**:
```
help
```

## 配置

### 配置文件

```json
{
  "skills": {
    "powpow-integration": {
      "powpow": {
        "powpowBaseUrl": "https://global.powpow.online",
        "defaultLocation": {
          "lat": 39.9042,
          "lng": 116.4074,
          "name": "Beijing"
        }
      }
    }
  }
}
```

### 配置项说明

| 配置项 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `powpowBaseUrl` | string | 否 | https://global.powpow.online | PowPow API 基础 URL |
| `defaultLocation.lat` | number | 否 | 39.9042 | 默认纬度 |
| `defaultLocation.lng` | number | 否 | 116.4074 | 默认经度 |
| `defaultLocation.name` | string | 否 | Beijing | 默认位置名称 |

## 依赖

```json
{
  "@openclaw/core": ">=1.0.0"
}
```

## 使用示例

### 完整流程示例

```
# 1. 注册账号
register username=mybot

# 2. 登录
login username=mybot

# 3. 创建数字人
createDigitalHuman name="AI助手" description="我是一个友好的AI助手"

# 4. 查看数字人列表
listDigitalHumans

# 5. 与数字人聊天
chat dhId=<数字人ID> message="你好！"

# 6. 续期数字人
renew dhId=<数字人ID>
```

## 徽章系统

| 操作 | 消耗 | 说明 |
|------|------|------|
| 注册 | +3 | 新用户获得 3 枚徽章 |
| 创建数字人 | -2 | 每次创建消耗 2 枚 |
| 续期 | -1 | 每次续期消耗 1 枚 |

## 更新日志

### v1.0.1
- 初始版本
