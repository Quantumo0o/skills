# IndexTTS Voice Skill 🎙️

> [!WARNING]
> ## ⚠️ 重要提示：需要企业会员
> 
> **本技能是 IndexTTS 的第三方客户端工具，不是官方产品**
> 
> - 💼 **企业会员要求**: 需要 IndexTTS 企业会员才能使用 API
> - 🆓 **免费替代**: 使用 [网页版](https://indextts.cn) 无需企业会员
> - 📌 **代码开源**: 本技能代码采用 MIT 许可证开源
> - 🔑 **API 费用**: API 调用费用支付给 IndexTTS 官方，与本技能无关

---

## 技能描述

IndexTTS 语音克隆与合成技能，提供完整的命令行接口，支持：

- 🎯 声音模型创建与管理
- 🎙️ 文本转语音（TTS）
- 🎭 语调参考音频管理（情感合成）
- 📊 配额查询

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 获取 API 签名（企业会员）

**访问官方网站：** [https://indextts.cn](https://indextts.cn)

**获取步骤：**
1. 注册/登录账户
2. **购买企业会员服务**
3. 进入「开发者中心」获取 API 签名

> 💡 **提示**: API 调用会产生费用，具体价格请咨询 IndexTTS 官方

### 3. 配置环境变量

**PowerShell:**
```powershell
$env:INDEX_API_SIGN='你的 API 签名'
$env:INDEX_BASE_URL='https://openapi.indextts.cn'
```

**CMD:**
```cmd
set INDEX_API_SIGN=你的 API 签名
set INDEX_BASE_URL=https://openapi.indextts.cn
```

### 4. 使用示例

```bash
# 查看声音模型列表
python indextts_api.py list-models

# 创建声音模型
python indextts_api.py create-model "我的声音" "voice.wav"

# 语音合成
python indextts_api.py tts-create "你好，这是测试文本" <audioId>

# 下载合成音频
python indextts_api.py tts-download <taskId> "output.wav"
```

## 完整命令

| 命令 | 功能 |
|------|------|
| `create-model` | 创建声音模型 |
| `list-models` | 查看模型列表 |
| `get-model` | 查看模型详情 |
| `delete-model` | 删除模型 |
| `upload-tts-reference` | 上传参考音频（24h 有效） |
| `list-tts-references` | 查看参考音频列表 |
| `delete-tts-reference` | 删除参考音频 |
| `tts-create` | 语音合成 |
| `tts-list` | 查看合成任务 |
| `tts-result` | 查询合成结果 |
| `tts-download` | 下载合成音频 |
| `quota` | 查询配额 |

## 文档

完整文档请查看 [SKILL.md](./SKILL.md)

## 支持

- 📖 官方文档：[https://indextts.cn/main/developer](https://indextts.cn/main/developer)
- 💬 问题反馈：GitHub Issues

## 版本

**v1.2.1** - 2026-04-02

- 🎯 品牌调整为 IndexTTS
- ✅ 完整的参考音频管理
- ✅ 情感合成支持（genre=1/2）
- ✅ 一键下载合成音频
- ✅ Windows 控制台兼容

---

## ⚠️ 免责声明

1. **第三方工具**: 本技能是独立的第三方开源工具，与 IndexTTS 官方无关联
2. **商标声明**: IndexTTS 及相关商标归其所有者所有
3. **API 服务**: API 服务由 IndexTTS 官方提供，本技能仅提供调用接口
4. **费用说明**: API 调用产生的费用由用户直接向 IndexTTS 支付
5. **使用条款**: 使用本技能需遵守 IndexTTS 服务条款
6. **无担保**: 本技能按"原样"提供，不提供任何明示或暗示的担保

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)
