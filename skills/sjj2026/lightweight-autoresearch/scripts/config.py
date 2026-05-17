{
  "evaluation_metrics": {
    "skill": {
      "success_rate": {
        "description": "成功率",
        "weight": 0.5,
        "target": ">= 80"
      },
      "avg_response_time": {
        "description": "平均响应时间",
        "weight": 0.3,
        "target": "<= 2s"
      },
      "quality_score": {
        "description": "质量评分",
        "weight": 0.2,
        "target": ">= 7"
      }
    },
    "strategy": {
      "total_return": {
        "description": "总收益率",
        "weight": 0.4,
        "target": ">= 10%"
      },
      "sharpe_ratio": {
        "description": "夏普比率",
        "weight": 0.3,
        "target": ">= 1.5"
      },
      "max_drawdown": {
        "description": "最大回撤",
        "weight": 0.3,
        "target": "<= 20%"
      }
    },
    "content": {
      "quality_score": {
        "description": "质量评分",
        "weight": 0.4,
        "target": ">= 8"
      },
      "engagement_rate": {
        "description": "互动率",
        "weight": 0.3,
        "target": ">= 5%"
      },
      "readability": {
        "description": "可读性",
        "weight": 0.3,
        "target": ">= 70"
      }
    }
  },
  "constraints": {
    "can_modify": [
      "experiment.py",
      "parameters",
      "prompt_templates"
    ],
    "cannot_modify": [
      "config.py",
      "evaluation_logic",
      "safety_rules"
    ]
  },
  "stopping_conditions": {
    "max_iterations": 100,
    "no_improve_limit": 10,
    "min_score": 90
  }
}