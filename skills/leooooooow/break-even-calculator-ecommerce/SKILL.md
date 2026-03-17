---
name: break-even-calculator-ecommerce
description: Calculate ecommerce break-even thresholds using price, cost, shipping, ad spend, and overhead assumptions. Use when operators need a simple no-loss baseline before scaling.
---

# Break-even Calculator Ecommerce

先把“不亏钱”的线算出来，再谈放量。

## 解决的问题

很多电商投放或促销决策的问题，不是不会增长，而是不知道：
- 当前价格下，最低要卖多少单才不亏；
- CPA 到多少还能接受；
- 打折、包邮、广告加码后，盈亏平衡点被推高了多少。

这个 skill 的目标是：
**给出一套清楚的 break-even 计算，让团队知道什么情况下只是“看起来有营收”，什么情况下才是真正不亏。**

## 何时使用

- 新品投放前要设底线；
- 调整价格、折扣、包邮政策前；
- 老品利润变薄，想找出关键压力项。

## 输入要求

- 售价
- 单件成本
- 运费 / 包装 / 手续费
- 广告成本或目标获客成本
- 固定成本（如团队 / 工具 / 月度分摊）
- 折扣、退款损耗等额外变量

## 工作流

1. 计算单笔贡献利润。
2. 计算固定成本覆盖所需销量。
3. 反推 break-even CPA / ROAS / conversion 阈值。
4. 提示最敏感的成本项。

## 输出格式

1. 核心假设表
2. Break-even 结果
3. 关键阈值
4. 风险提醒与建议动作

## 质量标准

- 公式清楚，可复核。
- 区分可变成本和固定成本。
- 不是只给一个数字，要给可执行阈值。
- 对不确定假设做明确标注。

## 资源

参考 `references/output-template.md`。
