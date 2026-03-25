# 安全声明

## 数据隐私
- API Token (`KJJ_API_TOKEN`) 仅用于与 api.jiujing.com 通信
- Token 可选择存储于：a) 环境变量 b) 本地配置文件 `~/.kjiujing/config.yaml`
- 不会收集系统信息、文件内容或其他敏感数据

## 网络范围
- 出站连接限制：仅 `https://api.jiujing.com`
- 无数据上报、无遥测、无第三方分析

## 依赖审计与验证
本 Skill 依赖 `equal-data==0.0.2`，用户可通过以下方式验证包完整性：

### 验证方式 A：PyPI 官方源
```bash
pip install equal-data==0.0.2
