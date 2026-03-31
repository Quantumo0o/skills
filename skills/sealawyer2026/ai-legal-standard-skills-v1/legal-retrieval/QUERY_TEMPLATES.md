# 法律检索技能 - 常用查询模板

**版本**: v1.0.0
**创建日期**: 2026-03-07

---

## 📋 概述

本文档收录了法律检索技能的常用查询模板，按业务场景分类，方便快速使用。

---

## 🏷️ 模板分类

1. **合同相关** (12条)
2. **债权债务** (8条)
3. **侵权责任** (8条)
4. **民法典** (10条)
5. **诉讼程序** (6条)
6. **劳动争议** (6条)
7. **公司商事** (6条)
8. **婚姻家庭** (6条)
9. **房地产** (6条)

---

## 📄 合同相关（12条）

### 1. 违约责任

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同违约责任" \
  --sources regulations cases \
  --limit 10 \
  --output human
```

**说明**: 检索合同违约责任的相关法规和案例

---

### 2. 合同解除

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同解除条件 法律后果" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索合同解除的法定条件和法律后果

---

### 3. 合同无效

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同无效 法律情形" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索导致合同无效的法定情形

---

### 4. 赔偿限额

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "赔偿限额条款 有效性" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索赔偿限额条款的有效性判断

---

### 5. 违约金

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约金 调整 标准" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索违约金调整的相关规定

---

### 6. 不可抗力

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "不可抗力 适用 情形" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索不可抗力条款的适用情形

---

### 7. 情势变更

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "情势变更 适用条件" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索情势变更制度的适用条件

---

### 8. 合同变更

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同变更 条件 程序" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索合同变更的条件和程序

---

### 9. 合同转让

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同转让 同意 义务" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索合同转让的相关规定

---

### 10. 定金罚则

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "定金 罚则 适用" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索定金罚则的适用规则

---

### 11. 迟延履行

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "迟延履行 责任" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索迟延履行的法律责任

---

### 12. 合同解释

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "合同解释 原则 方法" \
  --sources regulations reference \
  --limit 10
```

**说明**: 检索合同解释的原则和方法

---

## 💰 债权债务（8条）

### 1. 债权转让

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "债权转让 条件 通知" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索债权转让的条件和通知义务

---

### 2. 债务承担

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "债务承担 同意 效力" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索债务承担的相关规定

---

### 3. 债权人撤销权

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "债权人撤销权 行使条件" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索债权人撤销权的行使条件

---

### 4. 债权人代位权

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "债权人代位权 行使条件" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索债权人代位权的行使条件

---

### 5. 保证责任

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "保证责任 承担方式" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索保证责任的承担方式

---

### 6. 抵押权

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "抵押权 设立 实现" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索抵押权的设立和实现

---

### 7. 质权

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "质权 设立 实现" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索质权的设立和实现

---

### 8. 留置权

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "留置权 行使条件" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索留置权的行使条件

---

## ⚖️ 侵权责任（8条）

### 1. 侵权责任构成

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "侵权责任 构成要件" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索侵权责任的构成要件

---

### 2. 过错责任

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "过错责任 归责原则" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索过错责任的归责原则

---

### 3. 无过错责任

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "无过错责任 适用情形" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索无过错责任的适用情形

---

### 4. 共同侵权

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "共同侵权 连带责任" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索共同侵权和连带责任

---

### 5. 精神损害赔偿

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "精神损害赔偿 标准" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索精神损害赔偿的认定标准

---

### 6. 人身损害赔偿

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "人身损害赔偿 计算 标准" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索人身损害赔偿的计算标准

---

### 7. 财产损害赔偿

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "财产损害赔偿 计算 标准" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索财产损害赔偿的计算标准

---

### 8. 侵权责任减免

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "侵权责任 减免 事由" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索侵权责任的减免事由

---

## 📚 民法典（10条）

### 1. 民法典总则

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 总则 基本原则" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典总则的基本原则

---

### 2. 民法典物权编

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 物权编 所有权" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典物权编的主要内容

---

### 3. 民法典合同编

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 合同编 通则" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典合同编的通则部分

---

### 4. 民法典人格权编

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 人格权编 人格权" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典人格权编的主要内容

---

### 5. 民法典婚姻家庭编

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 婚姻家庭编 结婚 离婚" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典婚姻家庭编的主要内容

---

### 6. 民法典继承编

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 继承编 继承 遗嘱" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典继承编的主要内容

---

### 7. 民法典侵权责任编

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 侵权责任编 归责原则" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典侵权责任编的主要内容

---

### 8. 民法典诉讼时效

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 诉讼时效 期间" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典关于诉讼时效的规定

---

### 9. 民法典代理

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 代理 无权代理" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典关于代理的规定

---

### 10. 民法典民事法律行为

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "民法典 民事法律行为 效力" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民法典关于民事法律行为的规定

---

## ⚖️ 诉讼程序（6条）

### 1. 起诉条件

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "起诉 条件 程序" \
  --sources regulations reference \
  --limit 10
```

**说明**: 检索民事诉讼的起诉条件

---

### 2. 证据规则

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "证据 举证责任 规则" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索民事诉讼的证据规则

---

### 3. 审理期限

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "审理 期限 程序" \
  --sources regulations \
  --limit 10
```

**说明**: 检索民事诉讼的审理期限规定

---

### 4. 财产保全

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "财产保全 条件 程序" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索财产保全的条件和程序

---

### 5. 强制执行

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "强制执行 程序 措施" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索强制执行的程序和措施

---

### 6. 上诉程序

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "上诉 条件 期限" \
  --sources regulations reference \
  --limit 10
```

**说明**: 检索上诉的条件和期限

---

## 👨‍👩‍👧 劳动争议（6条）

### 1. 劳动合同解除

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "劳动合同解除 补偿" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索劳动合同解除的补偿规定

---

### 2. 工资拖欠

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "工资拖欠 赔偿 责任" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索工资拖欠的赔偿责任

---

### 3. 工伤认定

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "工伤认定 标准 程序" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索工伤认定的标准和程序

---

### 4. 加班工资

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "加班工资 计算 标准" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索加班工资的计算标准

---

### 5. 社会保险

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "社会保险 缴纳 义务" \
  --sources regulations \
  --limit 10
```

**说明**: 检索社会保险的缴纳义务

---

### 6. 劳动仲裁

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "劳动仲裁 程序 期限" \
  --sources regulations reference \
  --limit 10
```

**说明**: 检索劳动仲裁的程序和期限

---

## 🏢 公司商事（6条）

### 1. 股权转让

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "股权转让 限制 程序" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索股权转让的限制和程序

---

### 2. 公司治理

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "公司治理 股东权利" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索公司治理和股东权利

---

### 3. 破产清算

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "破产清算 程序 顺序" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索破产清算的程序和清偿顺序

---

### 4. 并购重组

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "并购重组 监管 要求" \
  --sources regulations \
  --limit 10
```

**说明**: 检索并购重组的监管要求

---

### 5. 公司法纠纷

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "公司 股东 纠纷 解决" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索公司股东纠纷的解决方式

---

### 6. 董事责任

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "董事 忠实义务 勤勉义务" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索董事的忠实义务和勤勉义务

---

## 💑 婚姻家庭（6条）

### 1. 结婚登记

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "结婚登记 条件 程序" \
  --sources regulations reference \
  --limit 10
```

**说明**: 检索结婚登记的条件和程序

---

### 2. 离婚登记

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "离婚登记 条件 程序" \
  --sources regulations reference \
  --limit 10
```

**说明**: 检索离婚登记的条件和程序

---

### 3. 财产分割

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "离婚 财产分割 原则" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索离婚财产分割的原则

---

### 4. 子女抚养

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "子女抚养 费用 标准" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索子女抚养费用的确定标准

---

### 5. 抚养权

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "抚养权 确定 原则" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索抚养权确定的原则

---

### 6. 抚养费

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "抚养费 调整 标准" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索抚养费的调整标准

---

## 🏠 房地产（6条）

### 1. 房屋买卖

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "房屋买卖合同 风险" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索房屋买卖合同的风险点

---

### 2. 逾期交房

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "房屋买卖 逾期交房 违约" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索逾期交房的违约责任

---

### 3. 房屋租赁

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "房屋租赁合同 权利义务" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索房屋租赁合同的权利义务

---

### 4. 房屋过户

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "房屋过户 程序 费用" \
  --sources regulations reference \
  --limit 10
```

**说明**: 检索房屋过户的程序和费用

---

### 5. 物业纠纷

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "物业 纠纷 解决" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索物业纠纷的解决方式

---

### 6. 违建拆除

```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "违章建筑 拆除 程序" \
  --sources regulations cases \
  --limit 10
```

**说明**: 检索违章建筑拆除的程序

---

## 🎯 高级技巧

### 1. 组合查询

```bash
# 检索多个相关主题
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任 赔偿限额 合同" \
  --sources regulations cases \
  --limit 15
```

### 2. 指定数据源

```bash
# 只检索法规
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --sources regulations \
  --limit 10

# 只检索案例
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --sources cases \
  --limit 10

# 检索多个数据源
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --sources regulations cases reference \
  --limit 20
```

### 3. 调整结果数量

```bash
# 少量结果（3-5条）
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --limit 5

# 中量结果（10-15条）
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --limit 15

# 大量结果（20+条）
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --limit 30
```

### 4. 选择输出格式

```bash
# JSON格式（程序处理）
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --output json

# 人性化格式（阅读）
python skills/legal-retrieval/legal-retrieval.py \
  --query "违约责任" \
  --output human
```

---

## 📞 反馈与建议

如果需要添加新的查询模板或有改进建议，请联系：
- 飞书: ou_5701bdf1ba73fc12133c04858da7af5c
- 智能体: 知识库管理

---

**文档创建**: 2026-03-07
**创建者**: 阿拉丁（法律AI团队 - 知识库管理）
**版本**: v1.0.0
**模板总数**: 68条
