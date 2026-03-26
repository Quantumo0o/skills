# Leap Customs API Reference

## Base URL

```
${LEAP_API_BASE_URL:-https://platform.daofeiai.com}
```

## Authentication

All requests require the `Authorization` header:

```
Authorization: Bearer $LEAP_API_KEY
```

---

## Endpoints

### 1. File Upload

**POST** `/api/v1/files/upload`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | binary (multipart) | ✅ | 支持 PDF, Excel (.xlsx/.xls), 图片 (.jpg/.png/.tiff) |

**Response:**
```json
{
  "file_id": "string (UUID)",
  "original_name": "string",
  "file_size": "integer (bytes)",
  "mime_type": "string",
  "content_hash": "string",
  "is_duplicate": "boolean",
  "created_at": "string (ISO 8601)",
  "download_url": "string"
}
```

---

### 2. Submit Process Task

**POST** `/api/v1/process`

#### 2a. Fast Classification

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | string | ✅ (or file_ids) | 单个文件ID |
| `file_ids` | string[] | ✅ (or file_id) | 多个文件ID |
| `output` | string | ✅ | 固定值 `"classify_fast"` |

#### 2b. Customs Declaration

| Parameter | Type | Required | Description |
|---|---|---|---|
| `output` | string | ✅ | 固定值 `"customs"` |
| `params.files` | array | ✅ | 文件列表，包含 file_id 和 segments |
| `params.files[].file_id` | string | ✅ | 文件ID |
| `params.files[].file_name` | string | ❌ | 原始文件名 |
| `params.files[].segments` | array | ✅ | 分类结果中的 segments |

**Response:**
```json
{
  "result_id": "string (UUID)",
  "file_id": "string",
  "status": "pending | processing | completed | failed",
  "message": "string",
  "task_id": "string",
  "created_at": "string (ISO 8601)"
}
```

---

### 3. Query Task Status

**GET** `/api/v1/process/tasks/{result_id}`

**Response (completed):**
```json
{
  "result_id": "string",
  "status": "completed",
  "progress": 100,
  "processing_time": "integer (ms)",
  "result_data": { ... }
}
```

---

### 4. List Tasks

**GET** `/api/v1/process/tasks`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `status` | string | ❌ | 过滤状态: pending/processing/completed/failed |
| `limit` | integer | ❌ | 返回数量 (默认 20) |
| `offset` | integer | ❌ | 偏移量 (默认 0) |

---

### 5. Download Result File

**GET** `/api/v1/results/{result_id}/files/{filename}`

Returns the binary file content (e.g., Excel).

---

### 6. Cancel Task

**DELETE** `/api/v1/process/tasks/{result_id}`

Only works for `pending` or `processing` tasks.

---

### 7. Retry Failed Task

**POST** `/api/v1/process/tasks/{result_id}/retry`

Only works for `failed` tasks.

---

## File Type Enum

| Value | Chinese | English |
|---|---|---|
| `invoice` | 发票/商业发票 | Commercial Invoice |
| `packing_list` | 装箱单 | Packing List |
| `bill_of_lading` | 提单 | Bill of Lading |
| `contract` | 合同 | Sales Contract |
| `draft` | 汇票 | Draft |
| `certificate_of_origin` | 原产地证 | Certificate of Origin |
| `insurance` | 保险单 | Insurance Policy |
| `unknown` | 未知 | Unrecognized |

## Segment Type Enum

| Value | Use Case |
|---|---|
| `page` | PDF documents (by page number) |
| `image` | Image files (whole image = one segment) |
| `sheet` | Excel files (by sheet) |
| `text` | Plain text content |
