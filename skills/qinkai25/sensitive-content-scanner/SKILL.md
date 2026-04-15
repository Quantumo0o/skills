---
name: sensitive-content-scanner
description: 专业的敏感内容扫描器，支持 PII 检测（身份证/手机号/银行卡/邮箱/IP）、敏感词检测、置信度评分、多格式报告生成。适用于文档审查、安全审计、内容合规检查、隐私保护等场景。
---

# 敏感内容扫描器 v2.0

## 概述

专业的敏感内容扫描工具，用于检测文件和文档中的敏感内容、个人隐私信息（PII）和违禁词汇。支持精确验证、置信度评分和多格式报告生成。

**核心特性**：
- ✅ PII 检测：身份证、手机号、银行卡、邮箱、IP 地址、护照号
- ✅ 敏感词检测：哈希库匹配 + 自定义词汇
- ✅ 置信度评分：三级评分系统（高/中/低）
- ✅ 智能验证：身份证校验码、银行卡 Luhn、IP 范围验证
- ✅ 多格式报告：Markdown / JSON
- ✅ 低误报率：默认禁用中文姓名检测

## 使用时机

当用户需要以下操作时，调用此技能：
- 📄 发布前文档审查
- 🔒 隐私泄露检查
- ✅ 内容合规审核
- 🛡️ 安全审计
- 📋 敏感信息排查

## 快速开始

### 基础用法

```bash
# 扫描单个文件
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py document.docx

# 扫描目录（递归）
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py ./documents -r

# 输出到文件
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py document.docx -o report.md
```

### 常用场景

**场景一：文档发布前审查**
```bash
# 扫描 Word 文档
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py 白皮书.docx -v
```

**场景二：批量扫描**
```bash
# 递归扫描目录，生成详细报告
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py ./docs -r -o audit_report.md
```

**场景三：集成到 CI/CD**
```bash
# 生成 JSON 报告，检查退出码
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py ./src -f json -o scan.json
# 退出码：0 = 未发现问题，1 = 发现问题
```

## 核心功能

### 1. PII 检测

自动识别个人隐私信息：

| PII 类型 | 检测规则 | 验证机制 |
|---------|---------|---------|
| 身份证号 | `^\d{17}[\dXx]$` | 校验码验证（加权因子算法） |
| 手机号 | `^1[3-9]\d{9}$` | 运营商号段匹配 |
| 银行卡号 | `^\d{16,19}$` | Luhn 算法校验 |
| 邮箱地址 | 标准邮箱格式 | 域名有效性检查 |
| IP 地址 | `^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$` | 范围验证（0-255） |
| 护照号码 | 字母+数字组合 | 格式验证 |
| 中文姓名 | 2-4 个中文字符 | 姓氏白名单（默认禁用） |

**隐私保护**：
- 检测结果自动脱敏
- 仅显示前 3 位和后 2 位
- 示例：`138****800`、`110**********23X`

### 2. 敏感词检测

支持两种检测方式：

**方式一：哈希库匹配**
- 预置敏感词哈希库（SHA256）
- 安全存储敏感词列表
- 位置：`references/sensitive_words_hashed.txt`

**方式二：自定义词汇**
- 加载自定义敏感词文件
- 支持中英文词汇
- 使用：`-c custom_words.txt`

### 3. 置信度评分系统

首次引入三级置信度评分：

| 等级 | 图标 | 含义 | 处理建议 |
|------|------|------|---------|
| 高 | 🔴 | 已通过格式验证 + 校验码验证 | 立即处理 |
| 中 | 🟡 | 格式匹配但验证不确定 | 人工复核 |
| 低 | 🟢 | 仅符合基本模式 | 可选复核 |

**验证算法**：
- 身份证号：加权因子校验码
- 银行卡号：Luhn 算法
- IP 地址：范围验证（0-255）

### 4. 报告生成

支持两种格式：

**Markdown 格式**（默认）：
```markdown
# 敏感内容扫描报告

## 扫描统计
- 高置信度问题: 3 个
- 中置信度问题: 2 个
- 低置信度问题: 5 个

## 详细检测结果
- 🔴 身份证号 (高): 110**********23X
- 🟡 手机号 (中): 138****800
- 🟢 中文姓名 (低): 流转视图
```

**JSON 格式**：
```json
{
  "scan_time": "2026-04-14 16:00:00",
  "statistics": {
    "high_confidence": 3,
    "medium_confidence": 2,
    "low_confidence": 5
  },
  "issues": [...]
}
```

## 工作流程

### 标准扫描流程

**步骤 1：确定扫描目标**
- 单个文件或目录路径
- 是否需要递归扫描

**步骤 2：执行扫描**
```bash
# 基础扫描
python3 scan_sensitive.py /path/to/file

# 详细输出
python3 scan_sensitive.py /path/to/file -v

# 指定输出文件
python3 scan_sensitive.py /path/to/file -o report.md
```

**步骤 3：审查报告**
- 检查高置信度问题（🔴）
- 复核中置信度问题（🟡）
- 可选查看低置信度问题（🟢）

**步骤 4：处理问题**
- 确认真实敏感内容
- 移除或脱敏处理
- 重新扫描验证

### 命令行参数

```
python3 scan_sensitive.py [OPTIONS] PATH

必需参数:
  PATH                  要扫描的文件或目录

可选参数:
  -c, --custom FILE     自定义敏感词文件
  -o, --output FILE     输出报告文件（默认：report.md）
  -f, --format FORMAT   输出格式：json 或 markdown（默认：markdown）
  -r, --recursive       递归扫描目录
  -v, --verbose         显示详细进度
  --enable-chinese-name 启用中文姓名检测（默认禁用）
```

**⚠️ 中文姓名检测说明**：
- 默认禁用，避免大量误报
- 启用时使用 `--enable-chinese-name` 参数
- 会使用姓氏白名单验证
- 在技术文档中仍可能产生误报

## 支持的文件类型

**文本文件**（扫描内容）：
- 文档：`.txt`, `.md`, `.doc`, `.docx`
- 数据：`.json`, `.yaml`, `.yml`, `.xml`, `.csv`
- 代码：`.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`
- 配置：`.conf`, `.cfg`, `.ini`, `.log`

**二进制文件**：
- 自动跳过内容扫描
- 文件名仍会检查敏感词

## 使用示例

### 示例一：文档发布前审查

```bash
# 扫描 Word 文档
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py 白皮书.docx -v
```

**预期结果**：
- ✅ 未发现敏感内容
- 或：发现 X 个问题，按置信度分级显示

### 示例二：批量扫描项目

```bash
# 递归扫描项目文档
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py ./docs -r -o audit.md
```

**报告内容**：
- 扫描文件统计
- 按置信度分级的问题列表
- 每个问题的详细位置和内容

### 示例三：使用自定义敏感词

```bash
# 准备自定义词汇文件
echo -e "内部项目\n客户名称\n机密信息" > custom_words.txt

# 使用自定义词汇扫描
python3 scan_sensitive.py ./documents -c custom_words.txt
```

## 资源文件

### scripts/scan_sensitive.py
主扫描脚本，包含所有核心功能：
- PII 检测与验证
- 敏感词匹配
- 置信度评分
- 报告生成

### references/sensitive_words_hashed.txt
预置敏感词哈希库（SHA256），可通过以下方式扩展：
```python
import hashlib
word = "敏感词"
hash_value = hashlib.sha256(word.encode('utf-8')).hexdigest()
# 添加到文件中
```

### references/pii_patterns.md
PII 模式文档，包含：
- 每种 PII 的正则表达式
- 检测策略说明
- 验证算法详解

### assets/custom_words_example.txt
自定义敏感词模板文件：
```
# 自定义敏感词示例
# 每行一个词汇

内部项目代号
客户名称
机密信息
```

## 最佳实践

### 1. 使用默认模式（推荐）
```bash
# 默认禁用中文姓名检测，误报率最低
python3 scan_sensitive.py document.docx
```

### 2. 重点关注高置信度问题
- 🔴 高置信度：几乎肯定是真实问题
- 🟡 中置信度：需要人工复核
- 🟢 低置信度：可能是误报

### 3. 自定义词汇管理
- 建立组织专属敏感词库
- 定期更新和维护
- 区分公开和私密词汇

### 4. 集成到工作流
```bash
# Git pre-commit hook 示例
#!/bin/bash
python3 ~/.workbuddy/skills/sensitive-content-scanner/scripts/scan_sensitive.py . -r -f json
if [ $? -eq 1 ]; then
  echo "⚠️ 发现敏感内容，请检查后再提交"
  exit 1
fi
```

## 误报处理

### 基于置信度处理

**高置信度问题**（🔴）：
- 通常是真实的 PII 泄露
- 建议立即处理

**中置信度问题**（🟡）：
- 格式匹配但验证不确定
- 需要人工判断

**低置信度问题**（🟢）：
- 可能是误报
- 在技术文档中常见
- 根据实际情况决定是否处理

### 中文姓名误报

**原因**：
- 中文姓名模式过于宽泛
- 技术术语容易被误识别

**解决方案**：
1. 默认禁用中文姓名检测
2. 需要时使用 `--enable-chinese-name`
3. 结合姓氏白名单验证
4. 重点查看置信度评分

## 限制说明

- ✅ 仅扫描文本文件内容
- ✅ PII 检测基于正则表达式
- ✅ 主要支持中英文内容
- ✅ 无法理解上下文语义
- ✅ 不扫描图片中的文字
- ✅ 中文姓名检测默认禁用

## 版本历史

### v2.0 (2026-04-14)

**新增功能**：
- ✅ 置信度评分系统（高/中/低）
- ✅ 智能验证机制（身份证、银行卡、IP）
- ✅ 可视化报告（图标 + 统计）

**优化改进**：
- ✅ 中文姓名检测默认禁用
- ✅ 姓氏白名单验证
- ✅ 误报率大幅降低
- ✅ 报告可读性提升

### v1.0 (初始版本)

**基础功能**：
- PII 检测
- 敏感词检测
- Markdown/JSON 报告

## 更新日志

```markdown
## v2.0.0 (2026-04-14)

### 新增
- 置信度评分系统（高/中/低）
- 身份证号校验码验证
- 银行卡号 Luhn 算法验证
- IP 地址范围验证
- 可视化置信度指示器（🔴🟡🟢）
- 统计摘要（按置信度分组）

### 优化
- 默认禁用中文姓名检测，避免误报
- 姓氏白名单验证机制
- 报告格式优化，增加置信度说明
- 降低技术文档误报率

### 修复
- 中文姓名检测误报问题
- 报告格式不一致问题
```

## 技术支持

**问题反馈**：
- 在 ClawHub 提交 Issue
- 或联系技能维护者

**使用建议**：
- 定期更新敏感词库
- 结合人工审查
- 集成到 CI/CD 流程

---

**技能版本**：v2.0.0  
**最后更新**：2026-04-14  
**维护状态**：✅ 活跃维护
