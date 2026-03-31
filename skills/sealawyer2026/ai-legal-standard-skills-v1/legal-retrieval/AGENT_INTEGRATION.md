# 法律检索技能 - 智能体集成指南

**版本**: v1.0.0
**创建日期**: 2026-03-07
**适用智能体**: 法律研究员、合同律师、民事律师、商事律师

---

## 集成概述

本指南说明如何将法律检索技能集成到各个智能体的工作流中。

---

## 🎯 集成目标

1. **法律研究员** - 法律检索、案例研究、新法解读
2. **合同律师** - 合同审查、法规依据查找、案例参考
3. **民事律师/商事律师** - 案件研究、法规检索、案例查找
4. **法务助理** - 文书起草支持、法规依据

---

## 📋 智能体集成方案

### 1. 法律研究员 ⭐ 核心集成

**集成位置**: 提示词中的"工具使用"和"工作流程"部分

**添加内容**:

```markdown
## 🔧 工具使用 - 法律检索技能

当需要检索相关法律依据时，使用法律检索技能：

### 使用方法

**Python API调用**:
```python
from skills.legal_retrieval import LegalRetrieval

# 初始化检索器
retriever = LegalRetrieval()

# 执行检索
results = retriever.search(
    query="查询关键词",
    sources=["regulations", "cases", "contracts"],  # 可选数据源
    limit=10  # 返回结果数量
)

# 输出结果
print(f"找到 {results.total} 条相关文档")
for ev in results.evidence:
    print(f"[{ev.score:.2f}] {ev.title}")
    print(f"  {ev.excerpt}\n")
```

**命令行调用**:
```bash
python skills/legal-retrieval/legal-retrieval.py \
  --query "查询关键词" \
  --sources regulations cases \
  --limit 10 \
  --output human
```

### 数据源选项

- `regulations` - 法规库（民法典、司法解释等）
- `cases` - 案例库（真实判例）
- `contracts` - 合同库（合同模板、示例）
- `documents` - 文书库（标准文书）
- `reference` - 参考库（实务经验、常见问题）
- `all` - 全部数据源

### 输出格式

- `json` - JSON格式，适合程序处理
- `human` - 人性化格式，适合阅读

---

## 🔄 工作流程

### 法律检索流程

1. **分析用户需求**
   - 识别法律问题类型
   - 提取关键关键词
   - 确定相关数据源

2. **执行检索**
   - 使用法律检索技能查找相关文档
   - 根据结果相关性筛选
   - 查看原文详情

3. **分析检索结果**
   - 阅读相关法规条文
   - 研究类似案例
   - 整理关键要点

4. **提供研究报告**
   - 综合法规、案例、参考资料
   - 提供法律依据
   - 给出专业建议

---

## 💡 使用示例

### 示例1: 检索法规条文

**用户请求**: "查找民法典中关于违约责任的规定"

**智能体处理**:
```python
from skills.legal_retrieval import LegalRetrieval

retriever = LegalRetrieval()

# 检索违约责任相关法规
results = retriever.search(
    query="民法典 违约责任",
    sources=["regulations"],
    limit=10
)

# 分析结果
for ev in results.evidence:
    if "民法典" in ev.title and "违约" in ev.title:
        # 阅读原文
        original_text = read_document(ev.source_url)
        # 提取法条内容
        # 提供摘要和解读
```

**输出**: 提供民法典违约责任相关条文、适用情形、要点解读

---

### 示例2: 检索类似案例

**用户请求**: "查找关于房屋买卖合同逾期交房的案例"

**智能体处理**:
```python
# 检索相关案例
results = retriever.search(
    query="房屋买卖合同 逾期交房 违约责任",
    sources=["cases", "reference"],
    limit=10
)

# 分析案例要点
for ev in results.evidence:
    # 提取案件基本信息
    # 分析法院观点
    # 总结裁判要点
```

**输出**: 提供类似案例、法院观点、裁判要点、参考价值

---

### 示例3: 综合研究

**用户请求**: "研究民法典第545条债权转让的相关法规和案例"

**智能体处理**:
```python
# 检索相关法规
reg_results = retriever.search(
    query="民法典第545条 债权转让",
    sources=["regulations"],
    limit=10
)

# 检索相关案例
case_results = retriever.search(
    query="债权转让 条件 通知义务",
    sources=["cases"],
    limit=10
)

# 检索实务经验
ref_results = retriever.search(
    query="债权转让 实务 操作",
    sources=["reference"],
    limit=10
)

# 综合分析
# 提供法规依据
# 提供案例参考
# 提供实务建议
```

**输出**: 综合研究报告，包含法规条文、案例参考、实务建议
```

---

### 2. 合同律师 ⭐ 核心集成

**集成位置**: 提示词中的"工具使用"和"合同审查流程"部分

**添加内容**:

```markdown
## 🔧 工具使用 - 法律检索技能

在审查合同时，使用法律检索技能查找相关法规和案例：

### 合同审查场景

#### 场景1: 条款效力审查

**查询示例**:
- "赔偿限额条款的有效性"
- "违约金条款的合理性"
- "不可抗力条款的适用"

**智能体处理**:
```python
from skills.legal_retrieval import LegalRetrieval

# 识别条款关键问题
key_issue = extract_key_issue(clause_text)

# 检索相关法规
results = retriever.search(
    query=key_issue,
    sources=["regulations", "cases"],
    limit=10
)

# 分析结果
# 判断条款效力
# 提供修改建议
```

---

#### 场景2: 条款风险评估

**查询示例**:
- "合同解除的法律后果"
- "赔偿责任的构成要件"
- "担保责任的承担方式"

**智能体处理**:
```python
# 检索风险相关案例
results = retriever.search(
    query=clause_type + " 风险 案例",
    sources=["cases", "reference"],
    limit=10
)

# 分析案例中的风险点
# 评估当前条款的风险
# 提供风险提示
```

---

#### 场景3: 条款完善建议

**查询示例**:
- "合同解除条款的标准写法"
- "赔偿条款的起草要点"
- "争议解决条款的最佳实践"

**智能体处理**:
```python
# 检索标准合同模板
template_results = retriever.search(
    query="合同 " + clause_type + " 模板",
    sources=["contracts"],
    limit=5
)

# 分析标准条款
# 对比当前条款
# 提供完善建议
```

---

## 🔄 合同审查流程

### 标准审查流程

1. **通读合同**
   - 了解合同目的
   - 识别核心条款
   - 记录可疑条款

2. **条款分类**
   - 义务条款
   - 权利条款
   - 违约责任条款
   - 争议解决条款

3. **逐条检索法规依据**
   ```python
   for clause in suspicious_clauses:
       key_issue = extract_key_issue(clause)
       results = retriever.search(key_issue, limit=5)
       # 分析结果，记录风险点
   ```

4. **检索类似案例**
   ```python
   case_results = retriever.search(
       query=contract_type + " 纠纷 案例",
       sources=["cases"],
       limit=10
   )
   # 分析案例中的争议点
   # 评估当前条款风险
   ```

5. **审查意见输出**
   - 风险提示
   - 修改建议
   - 法规依据
   - 案例参考

---

## 💡 审查示例

### 示例: 赔偿限额条款审查

**条款内容**: "在任何情况下，乙方的赔偿责任不得超过合同总金额的10%。"

**审查过程**:
```python
# 1. 识别关键问题
key_issue = "赔偿限额条款"

# 2. 检索相关法规
reg_results = retriever.search(
    query="赔偿限额条款 有效性",
    sources=["regulations"],
    limit=10
)

# 3. 检索相关案例
case_results = retriever.search(
    query="赔偿限额 合同纠纷 案例",
    sources=["cases"],
    limit=10
)

# 4. 分析结果
# 法规: 民法典相关规定
# 案例: 法院对类似条款的判决
# 结论: 可能影响公平性
```

**审查意见**:
1. **风险提示**: 赔偿限额可能影响公平性，存在被认定无效的风险
2. **法规依据**: 民法典相关条款
3. **案例参考**: 类似案例的判决结果
4. **修改建议**: 建议明确限额适用范围，或调整为合理比例
```

---

### 3. 民事律师/商事律师

**集成位置**: 提示词中的"工具使用"和"案件研究流程"部分

**添加内容**:

```markdown
## 🔧 工具使用 - 法律检索技能

在处理案件时，使用法律检索技能查找相关法规和案例：

### 案件研究场景

#### 场景1: 法规依据查找

**查询示例**:
- "房屋买卖合同的违约责任"
- "侵权责任的构成要件"
- "劳动争议的处理程序"

**智能体处理**:
```python
from skills.legal_retrieval import LegalRetrieval

# 分析案件法律问题
legal_issues = analyze_case_facts(case_info)

# 检索相关法规
for issue in legal_issues:
    results = retriever.search(
        query=issue,
        sources=["regulations"],
        limit=10
    )
    # 整理法规依据
```

---

#### 场景2: 类似案例检索

**查询示例**:
- "房屋买卖合同纠纷 逾期交房"
- "人身损害赔偿 误工费"
- "公司股权转让纠纷"

**智能体处理**:
```python
# 检索类似案例
results = retriever.search(
    query=case_type + " " + key_facts,
    sources=["cases"],
    limit=15
)

# 分析案例要点
# 总结裁判规则
# 提供策略建议
```

---

#### 场景3: 实务经验参考

**查询示例**:
- "合同纠纷 诉讼技巧"
- "侵权纠纷 证据收集"
- "劳动争议 和解技巧"

**智能体处理**:
```python
# 检索实务经验
results = retriever.search(
    query=case_type + " 实务 技巧",
    sources=["reference"],
    limit=10
)

# 提供实务建议
# 总结经验教训
```

---

## 🔄 案件处理流程

### 标准案件处理流程

1. **案件分析**
   - 理解案件事实
   - 识别法律关系
   - 提取法律问题

2. **检索法规依据**
   ```python
   for legal_issue in legal_issues:
       reg_results = retriever.search(
           query=legal_issue,
           sources=["regulations"],
           limit=10
       )
       # 整理法规依据
   ```

3. **检索类似案例**
   ```python
   case_results = retriever.search(
       query=case_type + " " + key_facts,
       sources=["cases"],
       limit=15
   )
   # 分析案例要点
   # 总结裁判规则
   ```

4. **检索实务经验**
   ```python
   ref_results = retriever.search(
       query=case_type + " 实务 经验",
       sources=["reference"],
       limit=10
   )
   # 提供实务建议
   ```

5. **制定策略**
   - 法规依据
   - 案例参考
   - 实务建议
   - 策略建议
```

---

### 4. 法务助理

**集成位置**: 提示词中的"工具使用"和"文书起草"部分

**添加内容**:

```markdown
## 🔧 工具使用 - 法律检索技能

在起草文书时，使用法律检索技能查找相关法规、案例和模板：

### 文书起草场景

#### 场景1: 起诉状起草

**查询示例**:
- "买卖合同纠纷 起诉状"
- "离婚纠纷 起诉状"
- "劳动争议 起诉状"

**智能体处理**:
```python
from skills.legal_retrieval import LegalRetrieval

# 检索类似起诉状
template_results = retriever.search(
    query="起诉状 " + dispute_type,
    sources=["documents"],
    limit=5
)

# 分析模板结构
# 提取关键要素
# 起草起诉状
```

---

#### 场景2: 合同起草

**查询示例**:
- "设备买卖合同"
- "服务合同"
- "保密协议"

**智能体处理**:
```python
# 检索合同模板
template_results = retriever.search(
    query="合同 " + contract_type,
    sources=["contracts"],
    limit=5
)

# 分析模板条款
# 根据需求修改
# 起草合同
```

---

#### 场景3: 答辩状起草

**查询示例**:
- "合同纠纷 答辩状"
- "侵权纠纷 答辩状"

**智能体处理**:
```python
# 检索类似答辩状
template_results = retriever.search(
    query="答辩状 " + dispute_type,
    sources=["documents", "reference"],
    limit=5
)

# 分析答辩要点
# 起草答辩状
```
```

---

## 🔧 实际集成步骤

### 步骤1: 找到智能体提示词文件

智能体提示词存储在：
- `/workspace/projects/agents/legal-ai-team/legal-ceo/agents/<agent-id>/agent.json`
- `/workspace/projects/agents/legal-ai-team/legal-ceo/agents/<agent-id>/SYSTEM_PROMPT.md`

### 步骤2: 编辑提示词

在适当的位置添加上述内容。

### 步骤3: 测试集成

使用测试用例验证集成效果。

### 步骤4: 优化迭代

根据实际使用反馈优化集成方案。

---

## 📊 集成检查清单

### 法律研究员

- [x] 添加法律检索技能使用说明
- [x] 更新工作流程
- [x] 添加使用示例
- [ ] 实际测试验证
- [ ] 优化提示词

### 合同律师

- [x] 添加法律检索技能使用说明
- [x] 更新合同审查流程
- [x] 添加审查示例
- [ ] 实际测试验证
- [ ] 优化提示词

### 民事律师/商事律师

- [x] 添加法律检索技能使用说明
- [x] 更新案件处理流程
- [x] 添加使用示例
- [ ] 实际测试验证
- [ ] 优化提示词

### 法务助理

- [x] 添加法律检索技能使用说明
- [x] 更新文书起草流程
- [x] 添加使用示例
- [ ] 实际测试验证
- [ ] 优化提示词

---

## 📞 支持

如有问题或建议，请联系：
- 飞书: ou_5701bdf1ba73fc12133c04858da7af5c
- 智能体: 知识库管理

---

**文档创建**: 2026-03-07
**创建者**: 阿拉丁（法律AI团队 - 知识库管理）
**版本**: v1.0.0
