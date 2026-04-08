# 学习天数评估 · 科学依据

## 理论基础

学习天数评估基于以下经过同行评审的教育心理学研究：

### 1. 认知负荷理论（Cognitive Load Theory）
- **来源**: Sweller, J. (1988). Cognitive load during problem solving. Cognitive Science, 12(2), 257-285.
- **核心发现**: 工作记忆容量有限，每次只能处理 4±1 个信息块（chunks）
- **对本评估的启示**: 
  - 每天学习的新概念不超过 4-5 个
  - 复杂概念必须拆解到多天
  - 每天学习时间上限 30-60 分钟（避免认知超载）

### 2. 间隔重复效应（Spacing Effect）
- **来源**: Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks. Psychological Science, 17(10), 830-837.
- **核心发现**: 将学习分散到多天，比集中学习效果好 2-3 倍
- **对本评估的启示**:
  - 一个主题最少 3 天（低于此效果急剧下降）
  - 最佳间隔：每两天之间间隔 24-48 小时
  - 超过 7 天的大主题效果优于压缩到 3-4 天

### 3. 费曼技巧（Feynman Technique）
- **来源**: Feynman, R. (1965). The Feynman Lectures on Physics; Dunlosky, J., et al. (2013). Improving Students' Learning With Effective Learning Techniques. Psychological Science in the Public Interest, 14(1), 4-58.
- **核心发现**: 用自己的话解释概念（elaborative interrogation + practice testing）是最有效的学习方法之一
- **对本评估的启示**:
  - 每天必须包含"输出"环节（复述/自测）
  - 自测环节至少占总学习时间的 30%

### 4. 精通学习理论（Mastery Learning）
- **来源**: Bloom, B. S. (1968). Learning for Mastery. UCLA Evaluation Comment, 1(2), 1-12.
- **核心发现**: 给每个学生足够的时间，95% 的学生能达到精通水平
- **对本评估的启示**:
  - 不固定天数上限，根据掌握情况动态调整
  - 每日完成后需要检测是否真正掌握（费曼复述 + 查漏）

### 5. 学习金字塔（Learning Pyramid / Cone of Experience）
- **来源**: Dale, E. (1969). Audiovisual Methods in Teaching（存在争议，但输出学习的有效性有多项 meta 分析支持）
- **核心发现**: 主动输出（教授他人/实践）的留存率 75-90%，被动阅读仅 10%
- **对本评估的启示**: 费曼四步中的"讲给我听"环节是学习效果的倍增器

## 天数评估公式

基于以上理论，学习天数评估公式为：

```
基础天数 = max(3, ceil(新概念数量 / 3))

其中：
- 新概念数量 = 通过 Step 1 搜索确认的、用户不熟悉的核心概念总数
- 每天学习 ≤ 3 个新概念（基于认知负荷理论 4±1 chunks）
- 最低 3 天（基于间隔重复效应）
```

### 修正因子

| 修正条件 | 修正公式 | 科学依据 |
|---|---|---|
| 零基础 | 基础天数 × 1.3 | 需要更多时间建立先验知识（Ausubel, 1968） |
| 有相关经验 | 基础天数 × 0.7 | 可利用已有图式（schema theory） |
| 需动手实践 | + 2 天 | 实践需要额外时间（experiential learning） |
| 用户要求速成 | max(3, 基础天数 - 2) | 速成牺牲深度，但保持最低间隔 |
| 用户要求系统学 | 基础天数 × 1.5 | 增加深度和广度 |

### 实际计算示例

**学习 React 前端框架（零基础）：**
- 新概念：组件、JSX、Props、State、Hooks、生命周期、虚拟DOM、路由、状态管理 = 9 个
- 基础天数 = max(3, ceil(9 / 3)) = 3 天
- 零基础修正：3 × 1.3 ≈ 4 天
- 需动手实践：4 + 2 = 6 天
- 取整到 7 天（含 1 天总结自测）

**学习 Python 基础语法：**
- 新概念：变量、数据类型、控制流、函数、模块、文件操作、异常处理 = 7 个
- 基础天数 = max(3, ceil(7 / 3)) = 3 天
- 需动手实践：3 + 2 = 5 天
- 取整到 5 天（含 1 天总结自测）

**学习 LLM 原理（有编程基础）：**
- 新概念：Transformer、注意力机制、Token 化、训练数据、微调、Prompt Engineering、评估 = 7 个
- 基础天数 = max(3, ceil(7 / 3)) = 3 天
- 有相关经验：3 × 0.7 ≈ 2.1 → 取 3（不低于最低值）
- 需动手实践：3 + 2 = 5 天
- 取整到 7 天（概念较抽象，增加理解时间）

## 学习路径结构 · 科学依据

### 为什么每天学 3 个概念？
- **Miller 定律**（Miller, 1956）: 工作记忆容量约 7±2 chunks
- **Cowan 更新研究**（Cowan, 2001）: 实际有效容量约 4 chunks
- 每天 3 个新概念 + 1 个复习 = 4 chunks，接近上限

### 为什么最低 3 天？
- **间隔重复研究**（Cepeda et al., 2006）: 间隔 < 1 天的集中学习，长期留存率比间隔学习低 50%+
- 3 天是保证最少 2 次间隔的最小值

### 为什么最后 1-2 天自测？
- **测试效应**（Roediger & Karpicke, 2006）: 主动提取比重复复习效果好 2-3 倍
- **合意困难**（Bjork, 1994）: 自测制造"合意困难"，反而促进长期记忆

## 参考文献

1. Sweller, J. (1988). Cognitive load during problem solving. Cognitive Science.
2. Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks. Psychological Science.
3. Dunlosky, J., et al. (2013). Improving Students' Learning With Effective Learning Techniques. Psychological Science in the Public Interest.
4. Bloom, B. S. (1968). Learning for Mastery. UCLA Evaluation Comment.
5. Cowan, N. (2001). The magical number 4 in short-term memory. Behavioral and Brain Sciences.
6. Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning. Psychological Science.
7. Miller, G. A. (1956). The magical number seven, plus or minus two. Psychological Review.
8. Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings.
