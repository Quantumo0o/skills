# 国内天气预报 - 和风天气(QWeather)驱动

基于中国气象局数据的完整天气服务技能，专为OpenClaw优化。

## 🎯 功能特点

### 🌤️ 完整天气服务
- **实时天气**: 温度、湿度、风力、降水等
- **天气预报**: 3天/7天详细预报
- **生活指数**: 穿衣、洗车、运动、紫外线等
- **空气质量**: 实时AQI、污染物数据
- **天气预警**: 官方预警信息

### 🇨🇳 中国本地化
- **数据源**: 中国气象局官方数据
- **准确性**: 针对中国气候特点优化
- **中文支持**: 完整中文天气描述
- **城市覆盖**: 全国主要城市

### 🚀 高性能
- **智能缓存**: 减少API调用
- **错误恢复**: 自动降级和重试
- **快速响应**: 优化请求处理

## 📦 安装

### 通过ClawHub安装
```bash
clawhub install qweather-china
```

### 手动安装
1. 复制本目录到OpenClaw技能目录
2. 安装Python依赖：
   ```bash
   pip install pyjwt cryptography requests
   ```
3. **配置和风天气API**（必需步骤）：
   - 前往 https://dev.qweather.com/ 注册账号
   - 创建项目，获取API认证信息
   - 编辑 `config.json` 文件，填入您的：
     - `api_host` (如: YOUR_API_HOST_HERE.re.qweatherapi.com)
     - `jwt.kid` (凭据ID: YOUR_CREDENTIALS_ID_HERE)
     - `jwt.sub` (项目ID: YOUR_PROJECT_ID_HERE)
     - `private_key_path` (私钥文件路径: PATH_TO_YOUR_PRIVATE_KEY.pem)
4. 测试安装：
   ```bash
   python qweather.py now --city beijing
   ```

## 🔧 配置

### 配置文件 (config.json)
```json
{
  "qweather": {
    "enabled": true,
    "api_host": "YOUR_API_HOST_HERE.re.qweatherapi.com",
    "jwt": {
      "kid": "YOUR_CREDENTIALS_ID_HERE",
      "sub": "YOUR_PROJECT_ID_HERE",
      "private_key_path": "PATH_TO_YOUR_PRIVATE_KEY.pem"
    },
    "cache": {
      "enabled": true,
      "ttl": {
        "now": 600,
        "forecast": 3600,
        "indices": 10800,
        "air": 1800
      },
      "directory": "~/.cache/qweather"
    },
    "default_city": "beijing",
    "cities": {
      "beijing": "101010100",
      "shanghai": "101020100",
      "guangzhou": "101280101",
      "shenzhen": "101280601",
      "hangzhou": "101210101",
      "chengdu": "101270101",
      "wuhan": "101200101",
      "nanjing": "101190101",
      "xian": "101110101",
      "chongqing": "101040100"
    }
  }
}
```

### 环境变量（可选）
```bash
export QWEATHER_API_HOST="YOUR_API_HOST_HERE.re.qweatherapi.com"
export QWEATHER_KID="YOUR_CREDENTIALS_ID_HERE"
export QWEATHER_SUB="YOUR_PROJECT_ID_HERE"
export QWEATHER_PRIVATE_KEY_PATH="PATH_TO_YOUR_PRIVATE_KEY.pem"
```

## 🚀 使用

### 命令行使用
```bash
# 查询北京实时天气
python qweather.py now --city beijing

# 查询3天预报
python qweather.py forecast --city shanghai --days 3

# 查询生活指数
python qweather.py indices --city guangzhou

# 查询空气质量
python qweather.py air --city shenzhen
```

### OpenClaw集成
在OpenClaw中直接使用自然语言查询：
- "北京天气怎么样？"
- "上海未来3天预报"
- "广州需要带伞吗？"
- "深圳穿什么？"
- "杭州空气质量"

## 🏙️ 支持的城市
- 北京 (beijing)
- 上海 (shanghai)
- 广州 (guangzhou)
- 深圳 (shenzhen)
- 杭州 (hangzhou)
- 成都 (chengdu)
- 武汉 (wuhan)
- 南京 (nanjing)
- 西安 (xian)
- 重庆 (chongqing)

或直接使用城市代码：`101010100` (北京)

## 🛠️ 开发

### 项目结构
```
qweather-china/
├── qweather.py          # 核心天气服务
├── openclaw_integration.py # OpenClaw集成
├── encoding_utils.py    # 编码处理工具
├── location_handler.py  # 智能地点处理器
├── simple_question_fix.py # 简单问题处理器
├── SKILL.md            # 技能文档
├── README.md           # 本文件
├── config.json         # 配置文件
├── skill.yaml          # ClawHub技能配置
└── ...其他支持文件
```

### 扩展功能
1. **添加新城市**: 在`config.json`的`cities`部分添加
2. **自定义模板**: 修改`config.json`的`response_templates`部分
3. **添加新命令**: 在`openclaw_integration.py`中添加处理函数

## 📞 支持与反馈

- 和风天气文档: https://dev.qweather.com/docs/
- 问题反馈: 通过GitHub Issues
- 紧急支持: 联系和风天气客服

## 📄 许可证

MIT License

---

**版本**: 1.2.0  
**作者**: uni-huang  
**更新日期**: 2026-03-16