# 敏感内容扫描器 v2.0

> 专业的敏感内容扫描工具，支持 PII 检测、敏感词检测、置信度评分

[![版本](https://img.shields.io/badge/版本-v2.0.0-blue.svg)](https://clawhub.ai/)
[![许可证](https://img.shields.io/badge/许可证-MIT--0-green.svg)](LICENSE)

## ✨ 核心特性

- 🔍 **PII 检测**：身份证、手机号、银行卡、邮箱、IP 地址、护照号
- 🛡️ **敏感词检测**：哈希库匹配 + 自定义词汇
- 📊 **置信度评分**：三级评分系统（高/中/低）
- ✅ **智能验证**：身份证校验码、银行卡 Luhn、IP 范围验证
- 📝 **多格式报告**：Markdown / JSON
- 🎯 **低误报率**：默认禁用中文姓名检测

## 🚀 快速开始

### 安装

```bash
# 方式一：从 ClawHub 安装（推荐）
# 访问 https://clawhub.ai/ 搜索 "sensitive-content-scanner"

# 方式二：手动安装
git clone https://github.com/your-username/sensitive-content-scanner.git
cd sensitive-content-scanner
pip install -r requirements.txt
```

### 基础用法

```bash
# 扫描单个文件
python3 scripts/scan_sensitive.py document.docx

# 扫描目录（递归）
python3 scripts/scan_sensitive.py ./documents -r

# 输出到文件
python3 scripts/scan_sensitive.py document.docx -o report.md

# 详细输出
python3 scripts/scan_sensitive.py document.docx -v
```

## 📖 使用示例

### 示例一：文档发布前审查

```bash
python3 scripts/scan_sensitive.py 白皮书.docx -v
```

**输出示例**：
```
✅ 扫描完成，未发现敏感内容
```

或

```markdown
# 敏感内容扫描报告

## 扫描统计
- 🔴 高置信度: 2 个
- 🟡 中置信度: 1 个
- 🟢 低置信度: 3 个
```

### 示例二：批量扫描

```bash
python3 scripts/scan_sensitive.py ./docs -r -o audit_report.md
```

### 示例三：使用自定义敏感词

```bash
# 准备自定义词汇文件
echo -e "内部项目\n客户名称\n机密信息" > custom_words.txt

# 使用自定义词汇扫描
python3 scripts/scan_sensitive.py ./documents -c custom_words.txt
```

### 示例四：集成到 CI/CD

```bash
# 生成 JSON 报告
python3 scripts/scan_sensitive.py ./src -f json -o scan.json

# 检查退出码
if [ $? -eq 1 ]; then
  echo "⚠️ 发现敏感内容！"
  exit 1
fi
```

## 🎯 置信度评分系统

首次引入三级置信度评分，帮助您快速识别真实威胁：

| 等级 | 图标 | 含义 | 处理建议 |
|------|------|------|---------|
| 高 | 🔴 | 已通过格式验证 + 校验码验证 | 立即处理 |
| 中 | 🟡 | 格式匹配但验证不确定 | 人工复核 |
| 低 | 🟢 | 仅符合基本模式 | 可选复核 |

## 🔍 支持的 PII 类型

| PII 类型 | 检测规则 | 验证机制 |
|---------|---------|---------|
| 身份证号 | `^\d{17}[\dXx]$` | 校验码验证 |
| 手机号 | `^1[3-9]\d{9}$` | 号段匹配 |
| 银行卡号 | `^\d{16,19}$` | Luhn 算法 |
| 邮箱地址 | 标准格式 | 域名检查 |
| IP 地址 | IPv4 格式 | 范围验证 |
| 护照号码 | 字母+数字 | 格式验证 |

## 📁 项目结构

```
sensitive-content-scanner/
├── SKILL.md                       # 技能定义文件
├── README.md                      # 本文件
├── scripts/
│   └── scan_sensitive.py          # 主扫描脚本
├── references/
│   ├── sensitive_words_hashed.txt # 敏感词哈希库
│   └── pii_patterns.md            # PII 模式文档
└── assets/
    └── custom_words_example.txt   # 自定义词汇模板
```

## ⚙️ 命令行参数

```
python3 scripts/scan_sensitive.py [OPTIONS] PATH

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

## 📋 最佳实践

1. ✅ **使用默认模式** - 中文姓名检测默认禁用，误报率最低
2. ✅ **关注高置信度** - 🔴 高置信度问题几乎肯定是真实问题
3. ✅ **自定义词汇** - 建立组织专属敏感词库
4. ✅ **定期更新** - 保持敏感词库和自定义词汇最新
5. ✅ **集成工作流** - 添加到 Git pre-commit 或 CI/CD

## 🐛 误报处理

### 中文姓名误报

**问题**：技术文档中的术语容易被误识别为中文姓名

**解决方案**：
- ✅ 默认禁用中文姓名检测
- ✅ 需要时使用 `--enable-chinese-name`
- ✅ 结合置信度评分判断

### 其他误报

- 🔴 高置信度：极少误报，建议立即处理
- 🟡 中置信度：可能误报，建议人工复核
- 🟢 低置信度：可能是误报，可选处理

## 📦 支持的文件类型

**文本文件**（扫描内容）：
- 文档：`.txt`, `.md`, `.doc`, `.docx`
- 数据：`.json`, `.yaml`, `.xml`, `.csv`
- 代码：`.py`, `.js`, `.java`, `.c`, `.cpp`
- 配置：`.conf`, `.cfg`, `.ini`, `.log`

**二进制文件**：
- 自动跳过内容扫描
- 文件名仍会检查敏感词

## 🔧 高级用法

### 更新敏感词哈希库

```python
import hashlib

word = "新的敏感词"
hash_value = hashlib.sha256(word.encode('utf-8')).hexdigest()
# 添加到 references/sensitive_words_hashed.txt
```

### 扩展 PII 检测

修改 `scripts/scan_sensitive.py` 中的 `_get_pii_patterns()` 方法：

```python
'custom_pii': re.compile(r'your_pattern_here'),
```

## 📝 更新日志

### v2.0.0 (2026-04-14)

**新增**：
- ✅ 置信度评分系统（高/中/低）
- ✅ 身份证号校验码验证
- ✅ 银行卡号 Luhn 算法验证
- ✅ IP 地址范围验证
- ✅ 可视化置信度指示器

**优化**：
- ✅ 默认禁用中文姓名检测
- ✅ 姓氏白名单验证
- ✅ 报告格式优化
- ✅ 误报率大幅降低

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT-0 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢腾讯云 CodeBuddy 团队提供的技能平台
- 感谢所有贡献者和用户的支持

## 📮 联系方式

- **ClawHub**: https://clawhub.ai/
- **问题反馈**: 在 ClawHub 提交 Issue

---

**⭐ 如果这个项目对您有帮助，请给一个 Star！**

**技能版本**：v2.0.0  
**最后更新**：2026-04-14
