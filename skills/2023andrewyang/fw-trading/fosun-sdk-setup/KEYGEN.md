# 长期密钥生成说明

使用 OpenSSL 生成 PKCS#8 格式的 ECDH 密钥对，用于 OpenAPI 的签名与加解密。

---

## 脚本

将以下内容保存为 `genkey.sh`：

```bash
#!/usr/bin/env bash

set -e

OUT_PRIVATE="${1:-private.pem}"
OUT_PUBLIC="${2:-public.pem}"

# 生成 PKCS#8 私钥
openssl ecparam -name secp384r1 -genkey | openssl pkcs8 -topk8 -nocrypt -out "$OUT_PRIVATE"

# 提取公钥（SubjectPublicKeyInfo 格式）
openssl ec -in "$OUT_PRIVATE" -pubout -out "$OUT_PUBLIC"

echo "已导出私钥: $OUT_PRIVATE (PKCS#8)"
echo "已导出公钥: $OUT_PUBLIC (SubjectPublicKeyInfo)"
```

---

## 使用方法

需已安装 `openssl`。

**默认输出**（`private.pem` + `public.pem`）：

```bash
bash genkey.sh
```

**自定义输出文件名**：

```bash
bash genkey.sh my_private.pem my_public.pem
```

---

## 输出说明

| 文件 | 格式 | 用途 |
|------|------|------|
| `private.pem` | PKCS#8 | 客户端 API 签名 |
| `public.pem` | SubjectPublicKeyInfo | 配置为验证 / 加密用途 |

- CRLF 行结尾会被自动处理，兼容所有平台。
- **备份你的密钥文件！切勿泄露私钥。**

---

## 后续步骤

密钥生成完成后，客户端需要与服务端**互换公钥**，方可用于对 OpenAPI 的请求进行签名与验证。
