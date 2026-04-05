# 错误处理指南

## 目录

- [诊断流程](#诊断流程)
- [错误码对照表](#错误码对照表)
- [重试机制](#重试机制)
- [特殊路径处理](#特殊路径处理)

---

## 诊断流程

当上传失败时，按以下步骤排查：

### 步骤 1：验证登录状态
```bash
wrangler whoami
# 输出应显示账户信息，否则运行 wrangler login
```

### 步骤 2：验证 bucket
```bash
wrangler r2 bucket list | grep "<bucket>"
# 未找到则创建：wrangler r2 bucket create <bucket>
```

### 步骤 3：验证文件
```bash
ls -la "<file-path>"
# 不存在则重新定位文件
```

### 步骤 4：尝试临时路径上传
```bash
# 适用于路径问题导致的失败
cp "<file>" "/tmp/upload-tmp" && \
wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "/tmp/upload-tmp" --remote && \
rm "/tmp/upload-tmp"
```

---

## 错误码对照表

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `The file does not exist` | 路径错误/空格处理问题 | 使用 `find` 查找正确路径 → 临时文件上传 |
| `Authentication required` | 未登录 | `wrangler login` |
| `Bucket not found` | bucket 不存在 | `wrangler r2 bucket create <name>` |
| `Network error` | 网络问题 | 检查网络 → 重试（最多 3 次） |
| `Permission denied` | 文件权限不足 | `chmod +r "<file>"` |
| `Timeout` | 大文件/网络慢 | 增加超时时间或检查网络 |

---

## 重试机制

网络不稳定时，使用自动重试：

```bash
# 最多重试 3 次，每次间隔 2 秒
for i in 1 2 3; do
  if wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "<file>" --remote; then
    echo "✓ 上传成功"
    break
  fi
  echo "⚠ 第 $i 次失败，2秒后重试..."
  sleep 2
done
```

---

## 特殊路径处理

含空格/中文路径可能失败，使用临时文件：

```bash
# 复制到临时路径（无空格）
TMP_FILE="/tmp/r2-upload-$(date +%s)"
cp "<source-path>" "$TMP_FILE"

# 上传临时文件
wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file "$TMP_FILE" --remote

# 清理
rm "$TMP_FILE"
```