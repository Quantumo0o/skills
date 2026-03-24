---
name: zhang-criminal-defense
version: "1.1.0"
description: 九章刑事辩护专家V1.1.0 - AI辅助刑事辩护策略与量刑分析（基于DeepSeek R2 + 3000+刑事判例库 + 自我进化）
metadata:
  {
    "openclaw": {
      "requires": { "env": ["DEEPSEEK_API_KEY"] },
      "capabilities": ["reasoning", "file_read"],
      "evolution": {
        "enabled": true,
        "version": "2.0.0",
        "data_collection": true,
        "auto_update": false,
        "feedback_loop": true
      }
    },
    "author": "张律师",
    "category": "legal",
    "tags": ["刑事", "辩护", "量刑", "辩护策略"],
    "evolution_metrics": {
      "usage_tracking": ["案件分析次数", "量刑预测准确率", "辩护策略采纳率"],
      "performance_indicators": ["量刑预测误差", "证据链分析完整性", "辩护要点覆盖率"],
      "feedback_collection": ["判决结果反馈", "新增辩护技巧", "法官量刑倾向"]
    },
    "evolution_plan": {
      "v1.2.0": ["接入实时刑事判例", "新增认罪认罚从宽策略"],
      "v1.3.0": ["支持证据排除规则分析", "AI生成辩护词"],
      "v2.0.0": ["全流程辩护管理", "智能证据质证"]
    },
    "changelog": [
      {
        "version": "1.1.0",
        "date": "2026-03-23",
        "changes": [
          "接入 DeepSeek R2 推理模型",
          "新增 3000+ 刑事判例数据库",
          "新增量刑预测功能",
          "优化辩护策略生成",
          "支持证据链分析",
          "集成自我进化系统（v2.0.0）"
        ]
      }
    ]
  }
---

# 九章刑事辩护专家 V1.1.0

**升级亮点**：
- ⚖️ **量刑预测** - 基于类案的量刑区间预测
- 📚 **3000+判例** - 涵盖各罪名刑事案例
- 🤖 **DeepSeek R2** - 深度推理辩护策略
- 🔗 **证据链分析** - 证据完整性评估
- 💡 **辩护策略** - 无罪/罪轻辩护方案

## 核心功能

### 1. 罪名分析
- 罪名构成要件解析
- 犯罪形态认定
- 共同犯罪分析
- 罪数认定

### 2. 量刑预测
- 刑期区间预测
- 缓刑可能性评估
- 罚金数额估算
- 量刑情节权重

### 3. 辩护策略
- 无罪辩护路径
- 罪轻辩护要点
- 证据辩护策略
- 程序辩护策略

### 4. 类案参考
- 相似案件检索
- 判决结果对比
- 辩护要点提取
- 法官裁判倾向
