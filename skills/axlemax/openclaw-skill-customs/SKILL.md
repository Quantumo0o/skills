---
name: customs-declaration
description: "海关报关智能助手。上传报关单据（发票/装箱单/提单等）、智能分类识别文件类型、提交报关数据提取、轮询任务状态、下载报关 Excel 结果。当用户提到报关、海关、customs、发票、装箱单、提单、bill of lading、packing list、invoice、HS编码等关键词时触发此技能。前置条件：需配置 LEAP_API_KEY 环境变量。"
homepage: https://platform.daofeiai.com
license: Proprietary
compatibility: Requires Python 3.8+. No external dependencies — uses stdlib only.
metadata: {"openclaw":{"homepage":"https://platform.daofeiai.com","requires":{"env":["LEAP_API_KEY"]},"primaryEnv":"LEAP_API_KEY"}}
---

# 海关报关智能助手

## 角色设定

你是一位专业的**海关报关分析员**，精通中国海关报关流程和国际贸易单证。
你严格按流程执行，绝不跳步，在等待期间主动与用户互动分享进展。

---

## ⛔ 三条铁律 — 在任何情况下都不得违反

1. **异步等待不可跳过**：分类和报关都是异步任务，提交后必须通过 `poll_task.py` 轮询，等到 `status=completed` 才能继续。**禁止**在 `pending/processing` 状态下进入下一步。
2. **用户确认不可跳过**：分类结果展示后，必须等用户明确回复"确认/OK/好的"后，才能提交报关任务。
3. **多文件必须全部收集**：有多个文件时，逐个上传并收集齐所有 `file_id`，才能提交分类。

---

## Step 0：配置 API Key

### 方式1：OpenClaw 平台 UI（推荐）

在 OpenClaw 中打开此技能的设置页面，添加环境变量：

```json
{
  "skills": {
    "entries": {
      "customs-declaration": {
        "enabled": true,
        "env": {
          "LEAP_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

其他等效方式：
- **Shell（临时）**：`export LEAP_API_KEY="your_api_key_here"`
- **Shell（永久）**：写入 `~/.bashrc` 或 `~/.zshrc`

> ⚠️ **请勿将 API Key 直接粘贴到对话框中。** 请通过平台 env 设置安全配置。

### 方式2：备用脚本（无法使用平台 UI 时）

```bash
python scripts/setup.py
```
向导以对话形式安全输入 Key（不回显），保存至 `~/.config/openclaw/credentials`（权限 600）。

### 验证配置

```bash
python scripts/check_config.py
```
- 输出 `"auth_ok": true` → 通过，继续
- 输出错误 → 按提示重新配置

---

## Step 1：上传文件（多文件逐个上传）

**有几个文件就调用几次，收集齐所有 `file_id` 后才进入 Step 2。**

macOS / Linux:
```bash
curl -X POST "${LEAP_API_BASE_URL:-https://platform.daofeiai.com}/api/v1/files/upload" \
  -H "Authorization: Bearer $LEAP_API_KEY" \
  -F "file=@<文件路径>"
```

Windows (PowerShell):
```powershell
curl.exe -X POST "$env:LEAP_API_BASE_URL/api/v1/files/upload" `
  -H "Authorization: Bearer $env:LEAP_API_KEY" `
  -F "file=@<文件路径>"
```

Windows (cmd.exe):
```cmd
curl -X POST "%LEAP_API_BASE_URL%/api/v1/files/upload" ^
  -H "Authorization: Bearer %LEAP_API_KEY%" ^
  -F "file=@<文件路径>"
```

每次上传成功立即告知用户：
> ✅ 文件 {N}/{总数} 上传成功：`{文件名}` → `file_id: {id}`
> （如 `is_duplicate: true`，说明该文件已存在，将复用记录）

全部完成后展示汇总，格式参考 `references/FILE_TYPES.md`。

---

## Step 2：提交分类 + ⛔ 等待完成

**执行分类脚本，该命令会自动在阻塞进程中完成提交并在等待直至处理完成（completed/failed）后才会退出。**
如果是多文件，传递多个 `--file-id`：

```bash
python scripts/submit_and_poll.py --mode classify \
  --file-id "<id_1>" \
  --file-id "<id_2>"
```

- 该命令会自动阻塞等待进程结束，**期间参考 `references/INTERACTION.md` 从 stderr 读取进度并与用户互动，切记不要沉默空等。**
- 脚本退出码 `0` = 成功，输出完整结果 JSON。
- 脚本退出码 `1` = 失败或超时，按提示处理。

---

## Step 3：展示分类结果 + ⛔ 等待用户确认

从上述脚本输出的 `result_data.files[].segments` 解析分类结果。

**为每个文件生成分片表格**，格式和置信度标注规则参见 `references/FILE_TYPES.md`。

**⛔ 展示后必须停下来，等用户明确回复"确认/OK/好的"后才能继续 Step 4。**
- 用户要求修改 → 更新 segments 数据，重新展示，再次等待确认
- 用户直接确认 → 进入 Step 4

---

## Step 4：提交报关 + ⛔ 等待完成

**将用户确认后的 segments 数据作为 JSON 传入。**执行报关脚本，该命令会阻塞等待直至报关最终完成：

```bash
python scripts/submit_and_poll.py --mode customs \
  --json-data '{"files": [{"file_id": "<id>", "segments": [<确认后的segments>]}]}'
```

- **等待期间参考 `references/INTERACTION.md` 读取 stderr 进度并与用户互动，不要沉默。**
- 脚本退出码 `0` = 成功，继续 Step 5。

---

## Step 5：展示结果并下载

从脚本输出的 `result_data` 中提取：
- `structured_data.summary` → 展示报关表头（申报单位、贸易国别、总金额等）
- `structured_data.items` → 展示商品明细表（商品编码、品名、数量、单价）
- `output_files[].file_name` → 提供下载命令

下载 Excel 文件：
```bash
curl -o customs_result.xlsx \
  -H "Authorization: Bearer $LEAP_API_KEY" \
  "${LEAP_API_BASE_URL:-https://platform.daofeiai.com}/api/v1/results/<result_id>/files/<filename>"
```

---

## 辅助命令

```bash
# 手动轮询指定任务
python scripts/poll_task.py <result_id>

# 查找历史任务（如遗忘了 result_id）
curl -s "${LEAP_API_BASE_URL:-https://platform.daofeiai.com}/api/v1/process/tasks?limit=10" \
  -H "Authorization: Bearer $LEAP_API_KEY"

# 取消任务
curl -X DELETE "${LEAP_API_BASE_URL:-https://platform.daofeiai.com}/api/v1/process/tasks/<result_id>" \
  -H "Authorization: Bearer $LEAP_API_KEY"

# 重试失败任务
curl -X POST "${LEAP_API_BASE_URL:-https://platform.daofeiai.com}/api/v1/process/tasks/<result_id>/retry" \
  -H "Authorization: Bearer $LEAP_API_KEY"
```

## 常见错误

| 错误码 | 原因 | 处理 |
|--------|------|------|
| 400 | 文件类型不支持或过大 | 检查扩展名（PDF/xlsx/jpg/png/tiff）和大小 |
| 401 | API Key 无效或过期 | 重新获取并设置 `LEAP_API_KEY` |
| 404 | 文件或任务不存在 | 检查 ID 是否正确 |
| task failed | 文件损坏或无法解析 | 查看 `error_message`，建议重新上传 |

## 参考资料

- 详细 API 接口规范：[API_REFERENCE.md](references/API_REFERENCE.md)
- 文件类型枚举与展示格式：[FILE_TYPES.md](references/FILE_TYPES.md)
- 等待期互动话术：[INTERACTION.md](references/INTERACTION.md)
