# Karpathy Autoresearch 核心理念

## 原始项目

GitHub: https://github.com/karpathy/autoresearch

作者：Andrej Karpathy（OpenAI 联合创始人、前 Tesla AI 总监）

---

## 核心思想

> **让 AI Agent 自主运行实验，一夜完成 100 次训练迭代**

### 关键创新

1. **自主循环**
   - Agent 自己修改代码
   - 自己运行实验
   - 自己评估结果
   - 自己筛选最优

2. **三文件架构**
   - prepare.py（只读）- 数据准备
   - train.py（可修改）- 训练代码
   - program.md（人类维护）- 基线指令

3. **简单评估**
   - val_bpb（validation bits per byte）
   - 越低越好
   - 自动记录和筛选

---

## 迁移到 CPU 场景

### 核心保留

- 自主循环理念
- 增量改进策略
- 自动评估和筛选
- 结果记录

### 调整适配

- GPU 训练 → CPU 任务
- val_bpb → 根据场景定义指标
- H100 → 普通服务器

---

## 适用场景

### 技能优化
- 自动测试 prompt
- 自动评估成功率
- 找到最优配置

### 策略回测
- 自动测试参数
- 自动评估收益
- 找到最优策略

### 内容创作
- 自动测试风格
- 自动评估质量
- 找到最优内容

---

## 参考资源

- Karpathy autoresearch: https://github.com/karpathy/autoresearch
- Unwind AI 分析: https://www.theunwindai.com/p/karpathy-s-autoresearch-for-agent-engineering
- Medium 实践: https://medium.com/@k.balu124/i-turned-andrej-karpathys-autoresearch-into-a-universal-skill-1cb3d44fc669

---

*整理时间：2026-04-14*