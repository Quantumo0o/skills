# 不同领域的学习模式

> 以下路径结构基于认知负荷理论（Sweller, 1988）和间隔重复效应（Cepeda et al., 2006）。
> 完整科学依据见 [scientific-basis.md](scientific-basis.md)。

## 编程/技术

```
Day 1: 概念速览 + Hello World
Day 2-3: 核心语法/API
Day 4-5: 动手项目
Day 6: 最佳实践 + 踩坑
Day 7: 总结 + 自测
```

- 每节必须含实践环节
- 材料配比：文档 40% + 教程 40% + 视频 20%

## 理论/概念

```
Day 1: 全景概述（是什么、为什么）
Day 2-3: 核心概念拆解
Day 4-5: 案例/应用场景
Day 6: 进阶/争议
Day 7: 总结 + 自测
```

- 材料配比：综述/书籍 50% + 文章 30% + 视频 20%
- 适合用 TTS 朗读

## 产品/业务

```
Day 1: 行业全景
Day 2-3: 竞品/模式拆解
Day 4-5: 运营/增长策略
Day 6: 数据/指标
Day 7: 总结 + 自测
```

- 优先行业报告、头部公司公开分享
- 材料配比：报告 40% + 文章 40% + 播客 20%

## 通用规则

- **默认 7 天**，用户可自定义 3-30 天
- 每天学习时长默认 30 min，可调整
- 最后 1-2 天固定为总结+自测
- 用户说「速成」→ 压缩到 3 天，只留核心
- 用户说「系统学」→ 扩展到 14+ 天，增加深度

## 进阶主题映射

学习完成后自动推荐的进阶路径：

```json
{
  "react-intro": {
    "tier1": [
      { "topic": "React Hooks 深入", "days": 7, "reason": "已掌握组件基础，Hook 是核心进阶" },
      { "topic": "React 状态管理", "days": 5, "reason": "理解 State 后自然需要全局状态方案" }
    ],
    "tier2": [
      { "topic": "Next.js 全栈开发", "days": 10, "reason": "React 进阶到生产级框架" }
    ]
  },
  "python-basic": {
    "tier1": [
      { "topic": "Python 数据分析", "days": 7, "reason": "Python 最热门应用方向" },
      { "topic": "Python Web 开发", "days": 7, "reason": "Flask/FastAPI 实战" }
    ]
  },
  "llm-principles": {
    "tier1": [
      { "topic": "Prompt Engineering", "days": 5, "reason": "理解原理后最佳实践" },
      { "topic": "LLM 微调实践", "days": 7, "reason": "理论到动手" }
    ]
  },
  "docker-intro": {
    "tier1": [
      { "topic": "Docker Compose 编排", "days": 5, "reason": "单容器到多服务" },
      { "topic": "Kubernetes 入门", "days": 10, "reason": "容器编排进阶" }
    ]
  },
  "javascript-basic": {
    "tier1": [
      { "topic": "TypeScript", "days": 7, "reason": "JS 基础上加类型安全" },
      { "topic": "Node.js", "days": 7, "reason": "JS 扩展到后端" }
    ]
  }
}
```
