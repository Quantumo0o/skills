# Product Research Analyzer | 产品调研分析师

自动化产品调研与竞品分析技能，生成可直接使用的飞书产品分析报告。

## 🎯 功能特点

- ✅ **自动化调研**：输入产品名称，自动执行完整调研流程
- ✅ **交互式引导**（NEW）：通过对话引导输入，确保调研需求准确
- ✅ **多源验证**：整合多个信息来源，交叉验证确保准确性
- ✅ **深度分析**：使用 competitor-analysis 技能进行专业竞品分析
- ✅ **知识库对比**：与目标项目（如蝉小狗）进行对比分析
- ✅ **飞书排版**：自动生成符合飞书最佳实践的精美报告
- ✅ **可追溯性**：完整的信息来源和验证记录
- ✅ **智能推荐**：根据调研目的推荐调研问题

## 📦 安装方法

### 方法 1：本地安装（推荐）

```bash
# 技能已在工作区，无需安装
# 位置：~/.openclaw/workspace/skills/product-research-analyzer/
```

### 方法 2：通过 ClawHub 安装（待发布）

```bash
clawhub install product-research-analyzer
```

## 🚀 快速开始

### 模式 1：交互式（推荐）⭐

**无需参数，通过对话引导输入**

```bash
cd /home/admin/.openclaw/workspace/skills/product-research-analyzer
python3 scripts/research_interactive.py
```

**对话流程**（5 个问题，2-3 分钟）：
1. 产品名称 → 你要调研的产品名称
2. 调研目的 → 竞品分析/设计参考/市场研究等
3. 调研问题 → 希望重点分析的方面
4. 对标项目 → 和哪个项目对比
5. 输出位置 → 飞书知识库空间 ID

**优势**：
- ✅ 无需记忆参数格式
- ✅ 智能推荐调研问题
- ✅ 实时确认调研需求
- ✅ 适合新手用户

### 模式 2：命令行参数

**一次性提供所有参数**

```bash
python3 scripts/research.py '{"product_name": "eilik"}'
```

**优势**：
- ✅ 适合批量调研
- ✅ 可集成到工作流
- ✅ 适合高级用户

### 基础用法

```bash
python3 scripts/research.py '{"product_name": "eilik"}'
```

### 指定调研问题

```bash
python3 scripts/research.py '{"product_name": "芙崽", "research_questions": "生命感设计，触摸反应，表情系统"}'
```

### 竞品对比分析

```bash
python3 scripts/research.py '{"product_name": "eilik", "target_project": "蝉小狗"}'
```

### 指定输出位置

```bash
python3 scripts/research.py '{"product_name": "小爱同学", "feishu_wiki_space": "my_library"}'
```

## 📋 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `product_name` | string | ✅ 是 | - | 要调研的产品名称 |
| `research_questions` | string | ❌ 否 | 自动分析 | 调研问题（逗号分隔） |
| `target_project` | string | ❌ 否 | 蝉小狗 | 对标项目名称 |
| `output_format` | string | ❌ 否 | feishu_doc | 输出格式 |
| `feishu_wiki_space` | string | ❌ 否 | my_library | 飞书知识库空间 ID |

## 📊 输出内容

### 飞书报告结构

```
# 产品名称 产品分析报告

> 📌 报告摘要
> 研究对象 | 品牌 | 核心问题 | 研究目的
> 验证状态 | 验证覆盖率 | 可信度评级 | 报告日期

## 一、核心发现
## 二、产品概述
## 三、硬件配置
## 四、功能与交互设计
## 五、设计原理分析
## 六、与目标项目对比分析
## 七、对目标项目的设计建议
## 八、总结与启示
## 九、参考资料与来源
## 十、附录：待补充信息
```

### 验证报告（JSON）

```json
{
  "success": true,
  "product_name": "eilik",
  "verification_coverage": "93%",
  "credibility_rating": "⭐⭐⭐⭐⭐",
  "sources_count": 6,
  "feishu_doc_url": "https://www.feishu.cn/wiki/..."
}
```

## 🔄 执行流程

```
1. 接收输入 → 产品名称 + 调研问题
   ↓
2. 多源搜索 → baidu-search 技能
   ↓
3. 深度研究 → competitor-analysis 技能
   ↓
4. 知识库对比 → 飞书知识库
   ↓
5. 交叉验证 → 多源信息对比
   ↓
6. 报告生成 → 飞书文档
   ↓
7. 输出结果 → 文档链接 + 验证报告
```

## 📝 使用示例

### 示例 1：调研 eilik 桌面机器人

```bash
python3 scripts/research.py '{
  "product_name": "eilik",
  "research_questions": "生命感设计，交互方式，硬件配置",
  "target_project": "蝉小狗"
}'
```

**输出**：
- 飞书文档链接
- 验证覆盖率：93%
- 可信度评级：⭐⭐⭐⭐⭐

### 示例 2：调研芙崽 AI 玩具

```bash
python3 scripts/research.py '{
  "product_name": "芙崽",
  "research_questions": "情感交互，触摸反应，表情系统，自主行为",
  "target_project": "蝉小狗"
}'
```

### 示例 3：批量调研（脚本）

```bash
#!/bin/bash

products=("eilik" "芙崽" "小爱同学")

for product in "${products[@]}"; do
  python3 scripts/research.py "{\"product_name\": \"$product\", \"target_project\": \"蝉小狗\"}"
done
```

## ⚙️ 依赖技能

| 技能名称 | 用途 | 安装命令 |
|----------|------|----------|
| `baidu-search` | 多源信息搜索 | 已内置 |
| `competitor-analysis` | 竞品分析 | `clawhub install competitor-analysis` |
| `feishu_create_doc` | 飞书文档创建 | 已内置 |
| `feishu_update_doc` | 飞书文档更新 | 已内置 |
| `feishu_search_doc_wiki` | 飞书知识库搜索 | 已内置 |

## ✅ 验证标准

| 验证等级 | 说明 | 来源数量要求 |
|:---------|:-----|:-------------|
| ✅ **已验证** | 多源信息一致，可信度高 | ≥3 个独立来源 |
| ⚠️ **估算** | 单一来源或推算数据 | 1-2 个来源 |
| ❌ **待补充** | 无可靠来源 | 0 个来源 |

## 🛠️ 排障指南

### 问题 1：搜索结果为空

**原因**：产品名称不准确  
**解决**：
```bash
# 使用通用名称
python3 scripts/research.py '{"product_name": "小爱音箱"}'  # 而不是"小爱同学 pro 版"
```

### 问题 2：验证覆盖率低

**原因**：信息来源少  
**解决**：
```bash
# 增加调研问题，扩展搜索范围
python3 scripts/research.py '{"product_name": "产品名", "research_questions": "参数，评测，配置，价格"}'
```

### 问题 3：飞书文档创建失败

**原因**：权限不足  
**解决**：
1. 检查飞书授权状态
2. 重新授权飞书文档创建权限
3. 确认 feishu_wiki_space 参数正确

### 问题 4：competitor-analysis 技能缺失

**原因**：未安装  
**解决**：
```bash
clawhub install competitor-analysis
```

## 📚 相关文档

- [SKILL.md](./SKILL.md) - 技能详细说明
- [scripts/research.py](./scripts/research.py) - 主执行脚本

## 📊 性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **验证覆盖率** | ≥90% | 高质量报告 |
| **信息来源** | ≥5 个 | 独立来源 |
| **报告生成时间** | <10 分钟 | 完整流程 |
| **飞书排版** | 符合最佳实践 | 易读性高 |

## 🎯 最佳实践

1. **产品名称准确性**：使用通用名称，便于搜索
2. **调研问题明确性**：问题越明确，报告越有针对性
3. **目标项目知识库**：确保目标项目知识库已存在且有内容
4. **验证覆盖率检查**：验证覆盖率≥90% 为高质量报告
5. **报告迭代优化**：根据反馈持续优化报告结构和内容

## 📝 更新日志

### v1.0.0 (2026-03-18)

- ✅ 初始版本发布
- ✅ 支持多源搜索
- ✅ 支持深度研究
- ✅ 支持知识库对比
- ✅ 支持交叉验证
- ✅ 支持飞书报告生成
- ✅ 支持验证报告输出

---

*技能版本：1.0.0*  
*创建时间：2026-03-18*  
*作者：产品调研分析系统*  
*许可证：MIT*
