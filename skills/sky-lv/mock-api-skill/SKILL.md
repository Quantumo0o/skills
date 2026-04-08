# Mock API Skill

快速创建模拟 API 接口，用于开发和测试。

## 功能特性

- 支持 GET/POST/PUT/DELETE 方法
- 自定义响应状态码和延迟
- 模拟 JSON 响应数据
- 路径参数和查询参数支持

## 使用方法

### 1. 快速启动

```bash
# 启动默认端口 3000
python mock_api.py

# 指定端口
python mock_api.py --port 8080

# 指定自定义配置
python mock_api.py --config my_api.json
```

### 2. 配置示例 (api_config.json)

```json
{
  "port": 3000,
  "endpoints": [
    {
      "path": "/api/users",
      "method": "GET",
      "response": {
        "users": [
          {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
          {"id": 2, "name": "李四", "email": "lisi@example.com"}
        ]
      },
      "status": 200,
      "delay": 500
    },
    {
      "path": "/api/users/:id",
      "method": "GET",
      "response": {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
      "status": 200
    },
    {
      "path": "/api/login",
      "method": "POST",
      "response": {"token": "abc123", "expiresIn": 3600},
      "status": 200
    }
  ]
}
```

### 3. 测试接口

```bash
# GET 请求
curl http://localhost:3000/api/users

# POST 请求
curl -X POST http://localhost:3000/api/login -H "Content-Type: application/json" -d '{"username":"test","password":"123456"}'

# 带延迟的响应
curl http://localhost:3000/api/slow
```

## 内置端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/mock/status` | GET | 返回服务状态 |
| `/mock/echo` | POST | 回显请求数据 |
| `/mock/delay/:ms` | GET | 延迟响应(毫秒) |
| `/mock/random` | GET | 返回随机数据 |

## 参数说明

- `--port`: 服务端口 (默认 3000)
- `--config`: 配置文件路径
- `--host`: 绑定地址 (默认 0.0.0.0)
- `--cors`: 启用 CORS (默认 true)