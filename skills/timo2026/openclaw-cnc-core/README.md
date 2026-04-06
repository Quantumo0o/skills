# OpenClaw CNC Core

🦞 OpenClaw CNC 智能报价系统核心框架

支持 STEP 解析、智能报价、风险控制

## 功能特性

- 🔧 智能报价引擎 - 规则 + RAG 混合决策
- 📐 3D图纸解析 - STEP/STP文件支持
- ⚠️ 风险控制 - 自动异常检测
- 🔍 案例检索 - 相似订单匹配
- 🚀 OpenClaw集成 - QQ/邮箱/飞书多通道

## 安装

```bash
pip install cadquery trimesh open3d flask numpy pandas scipy
```

## 快速开始

```python
from core.quote_engine import OpenClawQuoteEngine

engine = OpenClawQuoteEngine(config_dir="./config/examples")
result = engine.calculate_quote(order_data)
print(f"报价: ¥{result.total_price}")
```

## 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `OPENCLAW_WORKSPACE` | 工作目录 | ❌ 可选 |
| `DASHSCOPE_API_KEY` | DashScope API密钥 | ❌ 可选 |

## 外部API

| API | 用途 | 必需 |
|-----|------|------|
| DashScope | 向量嵌入 | ❌ 可选 |
| Feishu Webhook | 风险通知 | ❌ 可选 |

## 许可证

MIT-0 License - 无需署名

## 作者

Timo (miscdd@163.com)  
🦫 海狸 | 靠得住、能干事、在状态