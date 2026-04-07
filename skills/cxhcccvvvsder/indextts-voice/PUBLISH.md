# IndexTTS Voice Skill - 发布说明

## 📦 发布信息

- **技能名称**: indextts-voice
- **版本**: 1.2.1
- **发布日期**: 2026-04-02
- **作者**: OpenClaw Community
- **许可证**: MIT

---

## ⚠️ 重要提示

### 企业会员要求

**本技能需要 IndexTTS 企业会员才能使用**

- API 签名仅对企业会员开放
- 个人用户请使用 [IndexTTS 网页版](https://indextts.cn)
- 购买前请确认您的需求

### 获取 API 签名

1. 访问 [https://indextts.cn](https://indextts.cn)
2. 注册/登录账户
3. **购买企业会员服务**
4. 进入「开发者中心」获取 API 签名
5. 配置环境变量：
   ```powershell
   $env:INDEX_API_SIGN='你的 API 签名'
   ```

---

## 🎯 功能特性

### 声音模型管理
- ✅ 创建声音克隆模型（2-60 秒音频）
- ✅ 查看模型列表
- ✅ 查看模型详情
- ✅ 删除模型

### 语音合成（TTS）
- ✅ 文本转语音（最大 5000 字符）
- ✅ 支持 3 种模型版本（基础/专业/多语言）
- ✅ 语速调节（0.5-1.5）
- ✅ 一键下载合成音频

### 情感合成
- ✅ **genre=1**: 语气参考模式（8 种情感参数）
  - 开心、愤怒、悲伤、恐惧、厌恶、忧郁、惊讶、平静
- ✅ **genre=2**: 参考音频模式（使用上传的音频作为语调模板）

### 参考音频管理
- ✅ 上传参考音频（24 小时有效）
- ✅ 查看参考音频列表
- ✅ 删除参考音频
- ✅ 最多支持 30 个参考音频

### 其他功能
- ✅ 配额查询
- ✅ 任务状态查询
- ✅ Windows 控制台兼容

---

## 📋 命令列表

| 命令 | 功能 | 需要 API |
|------|------|----------|
| `create-model` | 创建声音模型 | ✅ |
| `list-models` | 查看模型列表 | ✅ |
| `get-model` | 查看模型详情 | ⚠️ 部分账户 |
| `delete-model` | 删除模型 | ✅ |
| `upload-tts-reference` | 上传参考音频 | ✅ |
| `list-tts-references` | 查看参考音频 | ✅ |
| `delete-tts-reference` | 删除参考音频 | ✅ |
| `tts-create` | 语音合成 | ✅ |
| `tts-list` | 查看任务列表 | ✅ |
| `tts-result` | 查询任务结果 | ✅ |
| `tts-download` | 下载音频 | ✅ |
| `quota` | 查询配额 | ⚠️ 部分账户 |

---

## 🚀 安装方法

### 从 ClawHub 安装

```bash
npx clawhub@latest install indextts-voice
```

### 手动安装

1. 克隆或下载技能目录
2. 安装依赖：
   ```bash
   pip install requests
   ```
3. 配置环境变量
4. 测试：
   ```bash
   python scripts/indextts_api.py --help
   ```

---

## 📖 使用示例

### 1. 创建声音模型

```bash
python scripts/indextts_api.py create-model "我的旁白声" "C:/Users/yanyu/Desktop/voice.wav"
```

### 2. 查看模型列表

```bash
python scripts/indextts_api.py list-models
```

### 3. 上传参考音频（用于情感合成）

```bash
python scripts/indextts_api.py upload-tts-reference "C:/Users/yanyu/Desktop/emotion.wav"
```

### 4. 语音合成（使用情感参数）

```bash
python scripts/indextts_api.py tts-create "今天天气真好！" <audioId> \
  --style 2 --genre 1 --happy 0.8 --speed 1.1
```

### 5. 下载合成音频

```bash
python scripts/indextts_api.py tts-download <taskId> "C:/Users/yanyu/Desktop/output.wav"
```

---

## 🔧 技术规格

### 系统要求
- Python 3.6+
- requests 库

### API 端点
- 基础 URL: `https://openapi.indextts.cn/api/third/`
- 鉴权方式：Header `sign` 或 URL params

### 文件格式支持
- **音频格式**: MP3, WAV, M4A
- **文件大小**: < 50MB
- **时长要求**: 2-60 秒（声音模型）

---

## ⚡ 限制说明

| 项目 | 限制 |
|------|------|
| 参考音频数量 | 最多 30 个 |
| 参考音频有效期 | 24 小时（自动清理） |
| 合成音频有效期 | 24 小时（自动清理） |
| 文本长度 | 最大 5000 字符 |
| 并发任务 | 最多 30 个排队 |

---

## 📝 更新日志

### v1.2.1 (2026-04-02)
- 🎯 品牌调整为 IndexTTS（indextts.cn）
- ✅ 更新所有文档和配置

### v1.2.0 (2026-04-01)
- ✅ 新增参考音频管理功能
- ✅ 支持情感合成（genre=1/2）
- ✅ 修复 API 端点路径
- ✅ 优化 Windows 兼容性
- ✅ 添加企业会员提示

### v1.1.0
- 新增模型详情查询
- 新增一键下载功能
- 新增配额查询

### v1.0.0
- 初始版本

---

## 📞 支持与反馈

- **官方文档**: [https://indextts.cn/main/developer](https://indextts.cn/main/developer)
- **ClawHub**: [https://clawhub.ai/skills/indextts-voice](https://clawhub.ai/skills/indextts-voice)
- **问题反馈**: ClawHub 技能页面评论区

---

## ⚠️ 免责声明

- 本技能为第三方开发，与 IndexTTS 官方无关联
- API 使用需遵守 [IndexTTS 服务条款](https://indextts.cn/terms)
- 企业会员价格和服务请咨询 IndexTTS 官方
- 本技能按"原样"提供，不提供任何明示或暗示的保证

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)
