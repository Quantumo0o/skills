
# README.zh-CN.md

# arxiv-to-zotero

[English version / 英文版](README.md)

这是一个 OpenClaw skill，用于在 arXiv 上查找近期论文，并将 **Zotero 中尚不存在的新条目** 导入进去。

## 这个 skill 做什么

这个 skill 会帮助 agent：

1. 收集用户给出的研究主题关键词或短语，以及时间范围
2. 在内部构造一条合法的 arXiv `search_query`
3. 在 arXiv 上检索近期论文
4. 与现有 Zotero 条目做去重
5. 只导入 Zotero 中还没有的论文
6. 在可能的情况下附加 PDF
7. 最后返回一段面向用户的总结

一句话概括：**搜索近期 arXiv 论文，跳过 Zotero 中已有的论文，只保存新的。**

## 为什么适合这个场景

这个 skill 适合用来做一个边界清晰、行为稳定的文献收集流程：

- 只使用 arXiv 作为发现来源
- 以 Zotero 去重为核心
- 不修改已有 Zotero 条目
- 自动处理常见的 PDF 附件问题
- 运行依赖简单，不需要第三方 Python 包

## 典型请求示例

下面是 agent 可以处理的自然语言请求示例：

- 帮我找近三年来用 Mamba 做股票预测的论文，并把新的导入 Zotero。
- 搜索近几年关于多模态用于股票预测的论文，和 Zotero 去重后，只导入新的。
- 帮我查近期关于 test-time adaptation 和 active search 的 arXiv 论文，只保存我 Zotero 里还没有的条目。

## 快速开始

### 运行要求

- Python 3.10+
- `curl`
- 通过 `ZOTERO_API_KEY` 访问 Zotero Web API
- OpenClaw skill 运行环境

### 首次运行

第一次使用时，如果 setup-state 文件不存在，这个 skill 会：

1. 读取 [`setup.md`](setup.md)
2. 收集所需的 Zotero 配置
3. 将非敏感配置写回 `config.json`
4. 创建 setup-state 文件
5. 精确恢复并继续原始请求一次

## agent 应该如何使用这个 skill

推荐的交互方式是：

1. 收集主题关键词或短语
2. 收集时间范围
3. 如用户给出中文关键词，先翻译为简洁、准确的英文技术短语
4. 在内部构造一条合法的英文 arXiv `search_query`
5. 只调用脚本一次

示例：

```bash
python3 scripts/main.py --config ./config.json --query '(all:"Mamba" OR all:"state space model") AND (all:"stock prediction" OR all:"financial prediction" OR all:"market prediction" OR all:"price forecasting") AND submittedDate:[202304010000 TO 202604092359]'
```



## 关键行为说明

### 论文发现来源

这个 skill **只使用 arXiv** 作为论文发现来源。

### 查询语言

最终发送给 arXiv 的查询应当是英文。
如果用户提供的是中文关键词，agent 应先翻译，再构造查询语句。

### 去重方式

这个 skill 会把最终 arXiv 查询拆成若干单词，对每个单词分别搜索一次 Zotero，建立一个临时缓存。
随后基于以下规则进行去重：

- 标准化标题的精确匹配
- 标准化标题前缀的严格匹配
- 在可用时使用 arXiv ID 匹配

Zotero 中已有的条目会被跳过，且不会被修改。

### PDF 附件处理

对每个新导入的 Zotero 父条目，skill 会根据保存的论文 URL 推导 PDF URL。

它会优先尝试把 PDF 作为真正的 Zotero 文件附件上传。
如果 Zotero 返回 `413 Request Entity Too Large`，则会删除未完成的上传附件，将该论文改为 `linked_url` 方式附加，并在本轮后续论文中继续使用 `linked_url` 模式。

### 导入数量上限

当新建 Zotero 父条目数量达到 `import_policy.max_new_items` 后，skill 会停止继续创建。
默认上限是每轮 50 篇。

## 固定运行路径

- 默认非敏感配置：skill 根目录下的 `./config.json`
- setup 状态文件：`~/.openclaw/config/skills/arxiv-to-zotero.setup.json`
- 密钥 / 环境变量：`~/.openclaw/.env`

## 仓库结构

- [`SKILL.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/SKILL.md)：skill 定义与运行说明
- [`setup.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/setup.md)：首次运行配置说明
- [`SECURITY.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/SECURITY.md)：安全边界与风险说明
- [`scripts/main.py`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/scripts/main.py)：主脚本实现
- [`config.json`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/config.json)：默认非敏感配置

## 安全与隐私

这个 skill 会访问：

- arXiv Atom API
- arXiv PDF 链接
- Zotero Web API

这个 skill 会：

- 创建新的 Zotero 条目和附件
- 不修改已有的 Zotero 条目
- 使用 `ZOTERO_API_KEY` 访问 Zotero API

更多细节请见 [`SECURITY.md`](https://chatgpt.com/g/g-p-69d25911ad748191adf4dc1095ea14bb-openclawyang-zhi-ji-lu/c/SECURITY.md)。

## 备注

- 这个脚本只适用于一次直接程序调用。
- 不要使用 `&&`、`;`、管道或串联 `cd` 等 shell 组合方式。
- 查询参数的 URL 编码由脚本自身处理，不要手动预编码空格、引号或括号。

## 关于

一个用于搜索近期 arXiv 论文并将新条目导入 Zotero 的 OpenClaw skill。
