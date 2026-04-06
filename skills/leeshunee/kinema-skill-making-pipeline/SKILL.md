---
name: kinema-skill-making-pipeline
displayName: "Kinema's Skill Making Pipeline"
version: 1.4.0
description: |
  KinemaClaw Skill development and publishing specification. Defines the standard process for skill development, version management, and publishing. All skills built in KinemaClaw must follow this specification.
  Trigger: Creating new skills, publishing skills, modifying existing skills.
---

# Kinema's Skill Making Pipeline | Kinema Skill 开发与发布规范

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/kinema-skill-making-pipeline

本规范定义了 KinemaClaw ecosystem 中 skill 的开发、版本管理、发布的标准化流程。

## Core Principles | 核心原则

1. **Git First** - All modifications must be managed in Git repository | 所有修改必须在 Git 仓库中管理
2. **Atomic Commits** - Each commit must be a meaningful independent change | 每次 commit 必须是有意义的独立变更
3. **Versioned Releases** - Must create Git tag before publishing | 发布前必须打 Git tag
4. **No In-Place Publishing** - Never publish raw skills from /app/skills/ | 禁止发布 /app/skills/ 中的原位 skill
5. **Onboarding Required** - Every skill must have installation/configuration guide | 每个 skill 必须有安装/配置引导
6. **Four-Way Sync** - After release, sync versions across: projects repo, local skills, GitHub Release, ClawHub | 发版后同步四地版本：projects 仓库、本地 skills、GitHub Release、ClawHub

## Development Workflow | 开发流程

### 1. Create Skill Repository | 创建 Skill 仓库

```
projects/<skill-name>/
├── SKILL.md              # Required: skill definition
├── scripts/              # Optional: automation scripts
├── references/           # Optional: reference materials
└── other project files
```

### 2. Development Guidelines | 开发规范

- **Atomic commits**: One thing per commit | 每个 commit 只做一件事
- **Commit frequently**: Commit after completing each feature/fix | 完成一个功能/修复一个问题后立即 commit
- **Descriptive messages**: Use meaningful commit messages | 使用描述性的 commit message

```bash
# Good | 好
git commit -m "Add install command to searxng-search CLI"

# Bad | 不好
git commit -m "update" 
git commit -m "fix stuff"
```

### 3. Release Process | 发布流程

```bash
cd projects/<skill-name>

# 1. Ensure all changes are committed | 确保所有修改已 commit
git status

# 2. Create version tag (Semantic Versioning) | 打版本 tag (语义化版本)
git tag -a v1.2.0 -m "Release v1.2.0: Add onboarding"

# 3. Push tag to GitHub | 推送 tag 到 GitHub
git push origin v1.2.0

# 4. Create release on GitHub | 在 GitHub 仓库发布
# Settings → Releases → Create new release

# 5. Publish to ClawHub | 推送到 ClawHub
clawhub publish . --slug <skill-name> --name "<displayName>" --version 1.2.0 --changelog "description of changes"
```

> **Fallback**: 如果 `clawhub publish` 返回 502 错误，可通过 Node.js 直接调用 ClawHub API 发布。详见附录。


```bash
node -e "
const fs = require('fs');
const path = require('path');
const TOKEN = JSON.parse(fs.readFileSync(process.env.HOME + '/.config/clawhub/config.json','utf8')).token;

const folder = '/path/to/<skill-name>';
const files = [];
function walk(dir, prefix='') {
  for (const f of fs.readdirSync(dir, {withFileTypes: true})) {
    const full = path.join(dir, f.name);
    const rel = prefix ? prefix + '/' + f.name : f.name;
    if (f.name === '.git' || f.name === 'node_modules') continue;
    if (f.isDirectory()) walk(full, rel);
    else if (rel.split('.').pop().match(/^(md|json|yaml|yml|js|ts|py|sh|txt|toml|css|html|svg|xml|csv|env|ini|cfg)$/)) {
      files.push({ relPath: rel, bytes: fs.readFileSync(full) });
    }
  }
}
walk(folder);

const form = new FormData();
form.set('payload', JSON.stringify({
  slug: '<skill-name>',
  displayName: '<displayName>',
  version: '1.2.0',
  changelog: 'description of changes',
  acceptLicenseTerms: true,
  tags: ['latest']
}));
for (const f of files) form.append('files', new Blob([f.bytes], {type: 'text/plain'}), f.relPath);

fetch('https://clawhub.ai/api/v1/skills', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/json' },
  body: form
}).then(async r => {
  const data = await r.json();
  console.log(r.ok ? 'OK ' + data.versionId : JSON.stringify(data));
});
"
```

**ClawHub 发版要求**:
- `--name` 必须使用 SKILL.md 中的 `displayName` 值
- `--version` 必须与 Git tag 版本号一致
- `--changelog` 必须包含本次变更说明
- 发布前确保 GitHub Release 已创建

### 4. Four-Way Version Sync | 四地版本同步

完成发版后，必须确保以下四个位置的版本一致：

| Location | Path/URL | Action |
|----------|----------|--------|
| **projects 仓库** | `~/.openclaw/workspace/projects/<skill-name>/` | Git tag + SKILL.md version |
| **本地 skills** | `~/.openclaw/workspace/skills/<skill-name>/` | `clawhub update` 或手动同步 |
| **GitHub Release** | `https://github.com/<org>/<repo>/releases` | `gh release create` |
| **ClawHub** | `https://clawhub.ai` | `clawhub publish` |

**发版后自动同步本地 skills**:

```bash
# 发版完成后，更新本地安装的 skill
clawhub update <skill-name>

# 或手动同步
cp projects/<skill-name>/SKILL.md skills/<skill-name>/SKILL.md
cp -r projects/<skill-name>/scripts skills/<skill-name>/scripts/
```

**完整发版检查清单**:

- [ ] 1. projects 仓库 SKILL.md 版本号已更新
- [ ] 2. Git commit 并打 tag (vX.Y.Z)
- [ ] 3. Push 到 GitHub (`git push origin master --tags`)
- [ ] 4. 创建 GitHub Release (`gh release create vX.Y.Z`)
- [ ] 5. 发布到 ClawHub (`clawhub publish` 或 API fallback)
- [ ] 6. 更新本地 skills (`clawhub update <skill-name>` 或手动同步)
- [ ] 7. 验证四地版本一致

### Version Numbering | 版本号规则

Follow Semantic Versioning: | 遵循语义化版本 (Semantic Versioning):
- **MAJOR**: Incompatible API changes | 不兼容的 API 变更
- **MINOR**: Backward-compatible new features | 向后兼容的新功能
- **PATCH**: Backward-compatible bug fixes | 向后兼容的 bug 修复

```
v1.0.0 → First release | 首次发布
v1.1.0 → New features | 新功能
v1.1.1 → Bug fixes | bug 修复
v2.0.0 → Breaking changes | 重大变更
```

## Required Elements | 必须要素

Each skill must include: | 每个 skill 必须包含：

### 1. SKILL.md

Must include: | 包含：
- name: skill name | skill 名称
- displayName: human-readable name with feature description | 人类可读名称（含功能描述）
- version: semantic version number | 语义化版本号
- description: functionality description and trigger condition | 功能描述和触发条件
- Complete usage instructions | 完整使用说明

**作者声明规范**:

SKILL.md 正文开头（标题之后）必须声明作者信息：

```markdown
# Skill Name

- **Author**: [AuthorName](https://github.com/authorname)
- **Organization**: [OrgName](https://github.com/orgname)
- **GitHub**: https://github.com/orgname/skill-name
```

| 字段 | 说明 |
|------|------|
| Author | 作者 GitHub 个人主页链接 |
| Organization | 所属组织 GitHub 主页链接 |
| GitHub | Skill 源码仓库链接 |

**displayName 格式规范**:
- 统一格式: \`Name (Feature Description)\`

### 2. Onboarding | Onboarding

**ONBOARDING.md 是必选文件。** SKILL.md 不包含安装/配置细节，仅引用 ONBOARDING.md。

#### 2.1 SKILL.md 中的 Onboarding 引导

SKILL.md 文件开头（`#` 标题之后、Environment Variables 之前）必须包含以下引导块：

```markdown
## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [ONBOARDING.md](ONBOARDING.md) 完成环境配置。**

- **首次配置** → 读取 ONBOARDING.md 完成全部步骤
- **环境不可用**（命令不存在、依赖缺失、连接失败）→ 读取 ONBOARDING.md Troubleshooting 排查修复
- **配置完成后** → 直接使用下方 Run Commands
```

Agent 读取 SKILL.md 时会看到此块，根据场景决定是否继续读取 ONBOARDING.md。

#### 2.2 ONBOARDING.md 结构规范

ONBOARDING.md 是给 AI Agent 执行的引导文档，必须按以下结构编写：

```markdown
# <Skill Name> Onboarding

> 本文档指导 AI Agent 完成首次环境配置。按顺序执行，遇到问题时参考 Troubleshooting。

## Prerequisites | 前置条件
（列出运行此 skill 所需的系统和软件条件）

## Step 1: <步骤名称>
### 检测
（检测命令 + 期望输出，agent 据此判断是否需要执行本步骤）
### 安装
（多种降级方案，按优先级排列，agent 逐条尝试）
### 验证
（验证命令 + 期望输出，确认本步骤完成）

## Step 2: <步骤名称>
...

## Step N: <验证连接或最终检查>

## Troubleshooting | 故障排除
（按错误信息分类的排查表，每行包含：错误 → 原因 → 解决方案）
```

**编写规则：**

| 规则 | 说明 |
|------|------|
| 按顺序执行 | Steps 之间有依赖关系，不可跳步 |
| 每步可独立验证 | 每个 Step 必须有验证命令 + 期望输出 |
| 降级策略 | 每步提供多种方案（至少 2 种），适配不同环境 |
| 不硬编码路径 | 用 `<skill_dir>` 等占位符，agent 运行时替换 |
| 需要用户输入时明确标注 | 如"必须询问用户" "用户提供"，不猜测 |
| Troubleshooting 覆盖常见错误 | 列出所有已知失败场景和解决方案 |

#### 2.3 setup.reference.sh（可选）

对于安装配置较复杂的 skill，可提供 `scripts/setup.reference.sh` 作为**参考范式**。

**注意**：
- 文件名必须包含 `reference`，明确标识为参考文件而非可执行脚本
- **Agent 不应直接执行此文件**，而是读取其内容，根据当前环境适配执行
- 内容是安装流程的模板代码，展示检测→安装→验证的逻辑模式

```bash
# scripts/setup.reference.sh - SETUP REFERENCE (DO NOT EXECUTE DIRECTLY)
# Agent should read this file and adapt commands to current environment.

# Step 1: Check Python
python3 --version

# Step 2: Install dependencies (try in order)
uv pip install --system requests 2>/dev/null || \
pip3 install requests 2>/dev/null || \
sudo pip3 install --break-system-packages requests

# Step 3: Create symlink
sudo ln -sf <skill_dir>/scripts/tool.py /usr/local/bin/tool

# Step 4: Verify
tool --help
```

#### 2.4 Onboarding 触发场景

| 场景 | Agent 行为 |
|------|-----------|
| **首次使用** | 读取 ONBOARDING.md，按 Step 1-N 顺序执行 |
| **环境不可用** | 读取 ONBOARDING.md Troubleshooting，按错误信息匹配解决方案 |
| **依赖缺失** | 跳转到对应 Step 重新执行安装 |
| **版本升级后** | 重新执行 ONBOARDING 全流程（新版本可能引入新依赖） |

### 3. Prohibited Content | 禁止内容

Skills must NOT contain: | skill 中**禁止**包含：
- Personal websites, domains | 个人网站、域名
- Passwords, accounts, tokens | 密码、账号、Token
- Personal email, phone | 个人邮箱、电话
- Real names, identity information | 真实姓名、身份信息

## GitHub Repository Guidelines | GitHub 仓库规范

- Default to **Private** repositories | 默认创建 **Private** 仓库
- Use meaningful repository names | 使用有意义的仓库名称
- Keep README.md in sync with SKILL.md | 保持 README.md 与 SKILL.md 一致

## Directory Structure | 目录结构

```
<skill-name>/                     # Git repository | Git 仓库
├── SKILL.md                      # Required: skill definition | 必需
├── ONBOARDING.md                 # Required: onboarding guide | 必需（见 Onboarding 章节）
├── README.md                     # Recommended: project readme | 推荐
├── LICENSE                       # Recommended: license | 推荐
├── scripts/                      # Optional: scripts | 可选
│   └── setup.reference.sh        # Optional: setup reference | 可选（见 Onboarding 章节）
└── references/                   # Optional: reference materials | 可选
```

## Automation Script Example | 自动化脚本示例

```bash
#!/bin/bash
# skill-publish.sh - Publish skill to GitHub + ClawHub

SKILL_NAME=$1
VERSION=$2

if [ -z "$SKILL_NAME" ] || [ -z "$VERSION" ]; then
    echo "Usage: $0 <skill-name> <version>"
    exit 1
fi

cd projects/$SKILL_NAME

# Check for uncommitted changes | 检查是否有未提交的修改
if ! git diff --quiet; then
    echo "Error: Commit all changes first | 先提交所有修改"
    exit 1
fi

# Create tag | 打 tag
git tag -a v$VERSION -m "Release v$VERSION"

# Push | 推送
git push origin master
git push origin v$VERSION

# Publish to ClawHub | 发布到 ClawHub
clawhub publish . --slug $SKILL_NAME --version $VERSION
```

## Related Documentation | 相关文档

- [ClawHub Documentation](https://docs.openclaw.ai) | [ClawHub 文档](https://docs.openclaw.ai)
- [Skill Creator Specification](/app/skills/skill-creator/SKILL.md) | [Skill 创建规范](/app/skills/skill-creator/SKILL.md)

## Appendix: ClawHub API Fallback | 附录: ClawHub API 备用发布

> 当 `clawhub publish` 返回 502 错误时，可通过 Node.js 直接调用 ClawHub API 发布。

```bash
node -e "
const fs = require('fs');
const path = require('path');
const TOKEN = JSON.parse(fs.readFileSync(process.env.HOME + '/.config/clawhub/config.json','utf8')).token;

const folder = '/path/to/<skill-name>';
const files = [];
function walk(dir, prefix='') {
  for (const f of fs.readdirSync(dir, {withFileTypes: true})) {
    const full = path.join(dir, f.name);
    const rel = prefix ? prefix + '/' + f.name : f.name;
    if (f.name === '.git' || f.name === 'node_modules') continue;
    if (f.isDirectory()) walk(full, rel);
    else if (rel.split('.').pop().match(/^(md|json|yaml|yml|js|ts|py|sh|txt|toml|css|html|svg|xml|csv|env|ini|cfg)$/)) {
      files.push({ relPath: rel, bytes: fs.readFileSync(full) });
    }
  }
}
walk(folder);

const form = new FormData();
form.set('payload', JSON.stringify({
  slug: '<skill-name>',
  displayName: '<displayName>',
  version: '1.2.0',
  changelog: 'description of changes',
  acceptLicenseTerms: true,
  tags: ['latest']
}));
for (const f of files) form.append('files', new Blob([f.bytes], {type: 'text/plain'}), f.relPath);

fetch('https://clawhub.ai/api/v1/skills', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/json' },
  body: form
}).then(async r => {
  const data = await r.json();
  console.log(r.ok ? 'OK ' + data.versionId : JSON.stringify(data));
});
"
```
