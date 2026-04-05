# 高级用法

## 目录

- [批量上传](#批量上传)
- [从 URL 上传](#从-url-上传)
- [并发上传](#并发上传)

---

## 批量上传

### 上传当前目录所有图片

```bash
for file in *.jpg *.png; do
  [ -f "$file" ] && \
  wrangler r2 object put "$R2_BUCKET/agent/$(date +%Y%m%d)/$file" --file "$file" --remote && \
  echo "✓ $file"
done
```

### 上传指定目录所有文件

```bash
for file in /path/to/dir/*; do
  [ -f "$file" ] && \
  wrangler r2 object put "$R2_BUCKET/agent/$(date +%Y%m%d)/$(basename "$file")" --file "$file" --remote
done
```

---

## 从 URL 上传

下载并直接上传（无需本地存储）：

```bash
# 从 URL 下载并直接上传到 R2
curl -sL "<url>" | wrangler r2 object put "$R2_BUCKET/$R2_PATH" --file - --remote
```

示例：
```bash
curl -sL "https://example.com/image.png" | \
  wrangler r2 object put "hugo-blog/agent/20260401/image.png" --file - --remote
```

---

## 并发上传

使用 `xargs` 并发上传（4 个进程）：

```bash
find . -name "*.jpg" -print0 | xargs -0 -P 4 -I {} \
  wrangler r2 object put "$R2_BUCKET/agent/$(date +%Y%m%d)/{}" --file "{}" --remote
```

参数说明：
- `-P 4`: 同时运行 4 个进程
- `-print0` / `-0`: 处理含空格的文件名