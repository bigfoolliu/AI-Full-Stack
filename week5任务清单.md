## 1. 本周目标

第 5 周的目标是跑通 RAG 最小闭环。

到本周结束时，你应该具备以下成果：

- 文档上传后可被后端解析（PDF/Word/TXT）
- 解析后的内容完成 Chunk 切分
- 切片内容完成向量化并写入 Qdrant
- 支持按知识库进行语义检索
- 前端知识库列表页可看到文档解析状态
- 检索结果可在接口层面验证

这一周的唯一目标可以概括为：

**文档能入库、内容能检索、RAG 最小链路跑通。**

---

## 2. 本周完成标准

如果这一周结束时，你能做到以下几点，就算顺利完成：

- [ ] 上传 PDF/Word/TXT 文档后，后端能成功解析为纯文本
- [ ] 文档内容按策略切片，切片结果可查看
- [ ] Embedding 接口调用成功，向量写入 Qdrant
- [ ] 按关键字或语义可检索到对应文档片段
- [ ] 检索结果包含文档来源和片段内容
- [ ] 文档上传页面可跟踪解析/索引状态
- [ ] Qdrant 容器可正常运行，数据可持久化

---

## 3. 本周项目范围

这一周只做 RAG 最小闭环，不要扩展到问答对话。

### 3.1 页面范围

以下页面可能涉及改动：

1. 文档上传页（增加上传后状态跟踪）
2. 知识库详情页（展示文档列表与解析状态）

### 3.2 接口范围

本周新增以下接口：

1. `POST /api/documents/{id}/process` — 触发文档解析与入库
2. `GET /api/knowledge-bases/{id}/documents` — 知识库下文档列表（含解析状态）
3. `POST /api/knowledge-bases/{id}/search` — 按知识库检索（返回切片片段）

### 3.3 学习范围

只围绕这些知识点学：

- 文档解析（PyMuPDF / python-docx / txt）
- Chunk 切分策略（固定长度 / 递归切分）
- Embedding 模型调用（text-embedding-ada-002 或 text2vec）
- Qdrant 向量库（Collection / Point / Payload / Search）
- Docker Compose 集成 Qdrant 服务

---

## 4. 每日执行清单

## Day 1：文档解析基础 ✅

### 目标

让后端能解析上传的 PDF、Word、TXT 文件，提取纯文本内容。

### 任务清单

- [x] 安装文档解析依赖（PyMuPDF / python-docx）
- [x] 创建 `app/services/document_parser.py`
- [x] 实现 PDF 解析函数（提取全部文本）
- [x] 实现 Word 解析函数（`.docx` 提取文本）
- [x] 实现 TXT 解析函数（直接读取）
- [x] 编写解析器统一入口，根据文件类型分发
- [x] 简单测试：通过 `scripts/test_parser.py` 验证 PDF/docx/txt 解析

### 今日重点

今天主要掌握：

- PyMuPDF（`fitz`）的基本用法
- python-docx 的基本用法
- 异常处理：解析失败时给出明确错误

### 验收标准

- 能解析 PDF 并输出纯文本
- 能解析 `.docx` 并输出纯文本
- 能解析 `.txt` 并输出纯文本
- 解析错误时有明确的异常信息

---

## Day 2：Chunk 切分 ✅

### 目标

将文档的原始文本按策略切分成适合检索的片段。

### 任务清单

- [x] 创建 `app/services/chunk_service.py`
- [x] 实现固定长度切分（`chunk_size=512`, `overlap=64`）
- [x] 实现递归切分（按段落 → 按句子 → 按固定长度回退）
- [x] 每个 Chunk 记录以下元数据：
  - `doc_id`
  - `kb_id`
  - `chunk_index`
  - `page_number`（如果是 PDF）
- [x] 编写单元测试验证切分结果（`scripts/test_chunk.py`，10 个测试全部通过）

### Chunk 格式示例

```python
{
    "doc_id": 1,
    "kb_id": 1,
    "chunk_index": 0,
    "content": "切片文本内容...",
    "page_number": 3,
    "chunk_size": 512
}
```

### 验收标准

- 长文本能被正确切分成多个 Chunk
- Chunk 之间保留 overlap 部分
- 每个 Chunk 携带完整的元数据
- 切分后不丢失文本内容

---

## Day 3：向量化与 Qdrant 写入 ✅

### 目标

将 Chunk 内容向量化，并写入 Qdrant 向量库。

### 任务清单

- [x] 在 `docker-compose.yml` 中增加 Qdrant 服务
- [x] 创建 `app/services/vector_service.py`
- [x] 集成 Embedding API（OpenAI `text-embedding-3-small`，1536 维）
- [x] 实现 Qdrant 客户端初始化
- [x] 创建 Collection（1536 维，Cosine 距离，自动创建）
- [x] 实现批量写入 Points（向量 + Payload）
- [x] 验证 Qdrant 中数据已写入（`scripts/test_vector.py` 测试通过）

### docker-compose 新增

```yaml
qdrant:
  image: qdrant/qdrant
  ports:
    - "6333:6333"
  volumes:
    - ./data/qdrant:/qdrant/storage
```

### 验收标准

- Qdrant 容器可正常启动
- Collection 创建成功
- Chunk 向量成功写入 Qdrant
- 可通过 Qdrant UI 或 API 查看写入的数据

---

## Day 4：文档处理全流程串联

### 目标

将「上传 → 解析 → 切分 → 向量化 → 入库」串联成一个完整的处理流程。

### 任务清单

- [x] 创建 `app/services/process_service.py`
- [x] 实现 `process_document(document_id)` 统一入口
- [x] 处理开始：更新文档状态为 `processing`
- [x] 执行解析
- [x] 执行 Chunk 切分
- [x] 执行向量化与入库
- [x] 处理成功：更新文档状态为 `completed`
- [x] 处理失败：更新文档状态为 `failed`，记录错误信息
- [x] 编写 `POST /api/documents/{id}/process` 接口

### 处理状态流转

```text
uploaded → processing → completed
                       → failed
```

### 验收标准

- 上传文档后可手动触发处理
- 处理成功后文档状态变为 `completed`
- 处理失败时状态变为 `failed` 且有错误信息
- 数据库 `documents` 表中 `status` 字段正确更新

---

## Day 5：按知识库检索（后端）

### 目标

实现基于 Qdrant 的语义检索，能按知识库返回匹配的文档片段。

### 任务清单

- [ ] 在 `vector_service.py` 中实现 `search` 方法
- [ ] 接收查询文本 → 向量化 → Qdrant search
- [ ] 支持按 `kb_id` 过滤（Payload Filter）
- [ ] 支持返回 Top-k（默认 5）
- [ ] 检索结果包含：文档片段、文件名、得分、来源
- [ ] 编写 `POST /api/knowledge-bases/{id}/search` 接口

### 接口示例

`POST /api/knowledge-bases/1/search`

请求：

```json
{
  "query": "什么是 RAG",
  "top_k": 5
}
```

响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": [
    {
      "doc_id": 1,
      "filename": "RAG介绍.pdf",
      "content": "RAG 是一种检索增强生成技术...",
      "score": 0.92,
      "chunk_index": 3,
      "page_number": 2
    }
  ]
}
```

### 验收标准

- 输入查询文本能返回相关性最高的 Chunk
- 不同知识库之间的检索结果互不干扰（kb_id 过滤生效）
- Top-k 参数生效
- 检索结果包含文档来源信息

---

## Day 6：前端状态展示

### 目标

让前端页面能反映文档的处理状态，给用户可见的进度反馈。

### 任务清单

- [ ] 增加 `GET /api/knowledge-bases/{id}/documents` 接口
- [ ] 前端知识库详情页展示文档列表
- [ ] 列表显示字段：文件名、上传时间、解析状态、操作
- [ ] 状态以标签形式展示（待处理 / 处理中 / 已完成 / 失败）
- [ ] 增加"触发解析"按钮（调用 `POST /documents/{id}/process`）
- [ ] 增加简单的检索测试页面或输入框（可选）

### 状态标签配色建议

| 状态 | 标签类型 |
|------|----------|
| `uploaded` | 灰色 |
| `processing` | 蓝色（可加旋转动画） |
| `completed` | 绿色 |
| `failed` | 红色 |

### 验收标准

- 知识库详情页可看到文档列表
- 可看到每个文档的解析状态
- 可手动触发解析处理
- 处理完成后状态自动更新

---

## Day 7：整理、复盘、封版

### 目标

不要继续加新功能，把第 5 周成果整理成一个干净的里程碑版本。

### 任务清单

- [ ] 检查所有接口命名和返回格式是否统一
- [ ] 补充 `docs/` 目录下的 RAG 链路说明文档
- [ ] 记录 Qdrant Collection 配置信息
- [ ] 记录 Embedding 模型和向量维度
- [ ] 验证全链路：上传 → 解析 → 切片 → 向量化 → 检索
- [ ] 更新 README，补充本周新增功能
- [ ] 记录下周任务清单

### 验证全链路脚本（手动）

```bash
# 1. 上传文档
curl -X POST http://localhost:8000/api/documents -F "file=@test.pdf"

# 2. 触发处理
curl -X POST http://localhost:8000/api/documents/{id}/process

# 3. 检索测试
curl -X POST http://localhost:8000/api/knowledge-bases/1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "测试内容", "top_k": 3}'
```

### 验收标准

- RAG 全链路可完整跑通
- Qdrant 数据可持久化
- 项目可被别人快速理解和运行
- 第 5 周有一个可展示、可继续开发的稳定基础版本

---

## 5. 本周接口清单汇总

第 5 周新增以下接口：

1. `POST /api/documents/{id}/process` — 触发文档解析与入库
2. `GET /api/knowledge-bases/{id}/documents` — 知识库下文档列表
3. `POST /api/knowledge-bases/{id}/search` — 按知识库语义检索

---

## 6. 本周页面清单汇总

第 5 周涉及以下页面改动：

1. 文档上传页（增加状态跟踪）
2. 知识库详情页（文档列表与解析状态展示）

---

## 7. 本周知识点清单汇总

本周围绕 RAG 最小闭环学习以下技术：

- 文档解析（PDF / Word / TXT）
- Chunk 切分策略（固定长度 / 递归切分 / Overlap）
- Embedding 模型调用
- Qdrant 向量库（Collection / Point / Payload / Search）
- Filter 检索过滤
- Docker Compose 集成 Qdrant
- 异步任务与状态管理

---

## 8. 本周完成后的状态

如果你能完成这份清单，第 5 周结束时你将拥有：

- 一个可运行的 RAG 检索链路
- 文档从上传到入库的完整处理流程
- Qdrant 向量库的正常运行与数据持久化
- 按知识库过滤的语义检索能力
- 前端可查看文档处理状态
- 一套可继续扩展的 RAG 基础代码结构

这一步很重要，因为它标志着你已经从「前后端联调阶段」正式进入 **「AI 应用工程阶段」**。
