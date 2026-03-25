---
name: china-doc-ocr
description: 智能文档OCR识别与结构化提取。Use when the user has a complex document, PDF, scanned image, photo, invoice, receipt, ID card, table, or chart that needs to be recognized and converted to text or Markdown. Handles complex layouts, multi-column text, tables, and mixed image-text that OpenClaw cannot process natively. Uses SiliconFlow DeepSeek-OCR and PaddleOCR-VL models — domestic access, no VPN, same API key as china-image-gen and china-tts.
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["curl", "python3"], "env": ["SILICONFLOW_API_KEY"]}, "primaryEnv": "SILICONFLOW_API_KEY"}}
---

# 智能文档 OCR China Doc OCR

识别并提取复杂文档内容：PDF、图片、扫描件、发票、表格、证件等。
使用硅基流动 DeepSeek-OCR / PaddleOCR-VL，国内直连，无需翻墙。
与 china-image-gen、china-tts 共用同一个 SILICONFLOW_API_KEY。

模型选择与参数说明 → `references/models.md`
各场景提示词模板 → `references/prompts.md`

## 触发时机

- "帮我识别这个PDF/图片里的内容"
- "把这张发票/收据的信息提取出来"
- "将这份扫描合同转成可编辑文字"
- "这个表格里的数据帮我提取一下"
- "帮我把这张截图的文字识别出来"
- "这份报告转成 Markdown 格式"
- "识别这张身份证/营业执照的信息"

---

## Step 0：环境检查

```bash
# 检查 API Key
if [ -z "$SILICONFLOW_API_KEY" ]; then
  echo "❌ 缺少 SILICONFLOW_API_KEY"
  echo "配置方法："
  echo "  1. 访问 cloud.siliconflow.cn 注册（国内直连）"
  echo "  2. 进入「API密钥」页面创建 Key"
  echo "  3. export SILICONFLOW_API_KEY='sk-xxxxxxxx'"
  echo "  或写入 ~/.openclaw/.env"
  exit 1
fi

# 检查 python3（用于 base64 编码）
if ! command -v python3 &> /dev/null; then
  echo "❌ 需要 python3（用于文件 base64 编码）"
  echo "  macOS:  brew install python3"
  echo "  Ubuntu: sudo apt install python3"
  exit 1
fi

echo "✅ 环境检查通过"
```

---

## Step 1：识别内容类型，选择处理模式

```
用户提供文件路径或 URL → 判断类型：

文件扩展名/用户描述 → 处理模式：

.pdf                    → PDF 模式（见 Step 3）
.jpg/.jpeg/.png/.webp   → 图片模式（见 Step 2）
.bmp/.tiff/.gif         → 图片模式（先转换格式）
URL（http/https开头）   → URL 直接模式（见 Step 2B）
用户粘贴了 base64       → 直接使用

用户意图 → 选择 Prompt 模式（见 references/prompts.md）：

"转成文字/提取文字"     → 通用OCR
"转成Markdown/保留格式" → 文档转Markdown
"提取表格/表格数据"     → 图表解析
"发票/收据/单据"        → 发票识别
"身份证/证件/执照"      → 证件识别
"图表/图形/柱状图"      → 图表解析
未指定                  → 默认文档转Markdown
```

---

## Step 2：图片 OCR（本地文件）

### Step 2A：本地图片文件

```bash
IMAGE_PATH="/path/to/image.jpg"  # 用户提供的图片路径
PROMPT="<image>\n<|grounding|>Convert the document to markdown."  # 见 references/prompts.md

# 将图片编码为 base64
BASE64_DATA=$(python3 -c "
import base64, sys
with open('$IMAGE_PATH', 'rb') as f:
    data = base64.b64encode(f.read()).decode('utf-8')
print(data)
")

# 判断图片格式（用于 data URL）
EXT="${IMAGE_PATH##*.}"
case "$EXT" in
  jpg|jpeg) MIME="image/jpeg" ;;
  png)      MIME="image/png" ;;
  webp)     MIME="image/webp" ;;
  bmp)      MIME="image/bmp" ;;
  *)        MIME="image/jpeg" ;;
esac

# 调用 DeepSeek-OCR
curl -s -X POST "https://api.siliconflow.cn/v1/chat/completions" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"Pro/deepseek-ai/DeepSeek-V3\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": [
          {
            \"type\": \"image_url\",
            \"image_url\": {
              \"url\": \"data:${MIME};base64,${BASE64_DATA}\",
              \"detail\": \"high\"
            }
          },
          {
            \"type\": \"text\",
            \"text\": \"$PROMPT\"
          }
        ]
      }
    ],
    \"max_tokens\": 4096,
    \"stream\": false
  }" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'choices' in data:
    print(data['choices'][0]['message']['content'])
else:
    print('错误：', json.dumps(data, ensure_ascii=False))
"
```

### Step 2B：图片 URL（无需下载，直接传 URL）

```bash
IMAGE_URL="https://example.com/document.jpg"

curl -s -X POST "https://api.siliconflow.cn/v1/chat/completions" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"Pro/deepseek-ai/DeepSeek-V3\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": [
          {
            \"type\": \"image_url\",
            \"image_url\": {
              \"url\": \"$IMAGE_URL\",
              \"detail\": \"high\"
            }
          },
          {
            \"type\": \"text\",
            \"text\": \"<image>\\n<|grounding|>Convert the document to markdown.\"
          }
        ]
      }
    ],
    \"max_tokens\": 4096
  }" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data['choices'][0]['message']['content'])
"
```

---

## Step 3：PDF OCR

### 单页或少页 PDF（直接整体处理）

```bash
PDF_PATH="/path/to/document.pdf"

# PDF 转 base64
BASE64_PDF=$(python3 -c "
import base64
with open('$PDF_PATH', 'rb') as f:
    print(base64.b64encode(f.read()).decode('utf-8'))
")

curl -s -X POST "https://api.siliconflow.cn/v1/chat/completions" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"Pro/deepseek-ai/DeepSeek-V3\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": [
          {
            \"type\": \"image_url\",
            \"image_url\": {
              \"url\": \"data:application/pdf;base64,${BASE64_PDF}\",
              \"detail\": \"high\"
            }
          },
          {
            \"type\": \"text\",
            \"text\": \"<image>\\n<|grounding|>Convert the document to markdown.\"
          }
        ]
      }
    ],
    \"max_tokens\": 8192
  }" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data['choices'][0]['message']['content'])
"
```

### 多页 PDF 分页处理

```bash
PDF_PATH="/path/to/multipage.pdf"
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/ocr_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# 用 python3 分页提取并分别识别
python3 << PYEOF
import base64, json, urllib.request, os, sys

pdf_path = "$PDF_PATH"
output_dir = "$OUTPUT_DIR"
api_key = "$SILICONFLOW_API_KEY"

# 尝试用 pypdf 分页
try:
    import pypdf
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"PDF 共 {total_pages} 页，开始逐页识别...")

    all_results = []
    for i, page in enumerate(reader.pages):
        # 单页写成临时 PDF
        writer = pypdf.PdfWriter()
        writer.add_page(page)
        tmp_path = f"{output_dir}/page_{i+1:03d}.pdf"
        with open(tmp_path, "wb") as f:
            writer.write(f)

        # base64 编码
        with open(tmp_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        # 调用 API
        payload = json.dumps({
            "model": "Pro/deepseek-ai/DeepSeek-V3",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {
                        "url": f"data:application/pdf;base64,{b64}",
                        "detail": "high"
                    }},
                    {"type": "text", "text": "<image>\n<|grounding|>Convert the document to markdown."}
                ]
            }],
            "max_tokens": 4096
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.siliconflow.cn/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            content = result["choices"][0]["message"]["content"]
            all_results.append(f"## 第 {i+1} 页\n\n{content}")
            print(f"✅ 第 {i+1}/{total_pages} 页识别完成")

    # 合并输出
    merged = "\n\n---\n\n".join(all_results)
    output_path = f"{output_dir}/result.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(merged)
    print(f"\n✅ 全部完成，结果已保存：{output_path}")

except ImportError:
    print("需要安装 pypdf：pip install pypdf")
    print("安装后重新运行")
    sys.exit(1)
PYEOF
```

---

## Step 4：格式化输出

识别完成后根据用户需求输出：

### 文档转 Markdown（保留结构）

```
直接输出 Markdown 内容，保留：
  - 标题层级（# ## ###）
  - 列表（- * 1.）
  - 表格（| 列1 | 列2 |）
  - 代码块（```）
  - 加粗、斜体等格式
```

### 发票/证件识别（结构化输出）

```
📄 发票识别结果
━━━━━━━━━━━━━━━━━━━━
发票类型：增值税专用发票
发票号码：XXXXXXXXXXXXXXXX
开票日期：2026年03月21日
购买方：[公司名称]
销售方：[公司名称]
商品/服务：[明细]
不含税金额：¥X,XXX.XX
税率：13%
税额：¥XXX.XX
价税合计：¥X,XXX.XX
```

### 表格数据（CSV 友好格式）

```
识别结果同时输出：
1. Markdown 表格（可读）
2. 询问用户是否需要 CSV 格式（方便导入 Excel）
```

---

## 输出文件保存

```bash
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/ocr_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# 保存 Markdown 结果
cat > "$OUTPUT_DIR/result.md" << 'RESULT'
{OCR识别内容}
RESULT

echo "✅ OCR 识别完成"
echo "结果已保存：$OUTPUT_DIR/result.md"
```

---

## 错误处理

```
文件不存在           → 提示用户确认路径
文件过大（>10MB）    → 建议压缩或分页处理
图片分辨率过低       → 提示识别效果可能较差，建议重新拍摄
PDF 加密            → 提示需要先解密：qpdf --decrypt input.pdf output.pdf
识别结果为空         → 可能是纯图片型PDF，尝试截图后重新识别
401 错误            → API Key 失效，重新获取
429 错误            → 请求频率超限，等待后重试
```

---

## 注意事项

- 图片最小 56×56，最大 3584×3584 像素，超出会自动压缩
- PDF 支持 base64 编码输入，DeepSeek-OCR 同时支持 PDF URL
- 多页 PDF 需要安装 pypdf：`pip install pypdf`
- 识别结果保存到工作区，长期保留
- detail=high 时按实际像素计费，detail=low 统一约256 token，复杂文档建议用 high
- 发票/证件等隐私文件处理后请及时删除工作区临时文件
