# RAG Pipeline 说明

## 架构概览

```text
上传文件 ──→ process ──→ parse ──→ chunk ──→ embed ──→ Qdrant (向量库)
  │                    │         │                    └─→ FTS (全文搜索)
  │                    │         └─ recursive_chunk
  │                    └─ status: processing → completed / failed
  └─ status: pending
```

## 服务职责

| 服务 | 文件 | 职责 |
|------|------|------|
| `document_parser` | `app/services/document_parser.py` | 解析 PDF (PyMuPDF)、Word (python-docx)、TXT (多编码回退) 为纯文本 |
| `chunk_service` | `app/services/chunk_service.py` | `chunk_text()` 固定大小滑动窗口；`recursive_chunk_text()` 按段落→句子→固定回退 |
| `vector_service` | `app/services/vector_service.py` | Embedding 生成 (DashScope)、Qdrant CRUD、语义搜索 |
| `search_service` | `app/services/search_service.py` | FTS5 全文索引创建与关键词搜索（snippet 高亮） |
| `process_service` | `app/services/process_service.py` | 编排 parse → chunk → embed → FTS 全流程 |

## 数据流

### 1. 上传

`POST /api/knowledge-bases/{kb_id}/documents`

- 保存文件到 `uploads/{kb_id}/` 目录
- `documents` 表写入记录，`status = "pending"`

### 2. 触发处理

`POST /api/documents/{id}/process`

```python
# process_service.py 简化流程
doc.status = "processing"
text = parse_document(file_path, ext)       # 解析
chunks = recursive_chunk_text(text, ...)    # 切分
if EMBEDDING_API_KEY:
    vector_svc.upsert_chunks(chunks)        # 向量化 → Qdrant
doc.status = "completed"
create_fts_index(db, doc)                   # FTS 索引
```

### 3. 检索

**关键词搜索** `GET /api/knowledge-bases/{id}/search?q=...`

→ FTS5 MATCH 查询，返回 snippet 高亮片段

**语义搜索** `POST /api/knowledge-bases/{id}/search`

→ 查询文本 Embedding → Qdrant search → 返回向量相似度结果

## Qdrant 配置

| 项目 | 值 |
|------|-----|
| Collection 名称 | `document_chunks` |
| 向量维度 | 1024 |
| 距离度量 | Cosine |
| 访问地址 | `http://localhost:6333` (docker-compose) |
| 持久化路径 | `data/qdrant/` |

### Payload 结构

```json
{
  "doc_id": 1,
  "kb_id": 1,
  "chunk_index": 0,
  "content": "切片文本内容...",
  "page_number": null,
  "chunk_size": 512,
  "filename": "example.pdf"
}
```

## Embedding 配置

| 项目 | 值 |
|------|-----|
| 提供方 | Alibaba DashScope (OpenAI 兼容) |
| API Base | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 模型 | `text-embedding-v3` |
| 维度 | 1024 |
| 环境变量 | `DASHSCOPE_API_KEY` |

如果 `DASHSCOPE_API_KEY` 未设置，Qdrant/Embedding 步骤跳过，仅执行解析 + FTS 索引。

## Chunk 策略

### fixed_size (`chunk_text`)

```
chunk_size=512, overlap=64
滑动窗口，按字符数切分
```

### recursive (`recursive_chunk_text`)

1. 按双换行切段落
2. 段落≤512 → 独立 chunk
3. 段落>512 → 按句号/问号/感叹切句子
4. 单句>512 → 回退到 fixed_size

每个 chunk 默认 `page_number=None`（目前均为纯文本提取，PDF 页码暂未记录到 chunk）。

## 状态流转

```text
uploaded ──→ processing ──→ completed
                           └─→ failed
```

## Docker Compose

```yaml
# ai-knowledge-base/docker-compose.yml
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./data/qdrant:/qdrant/storage
```

启动：`docker compose up -d`
