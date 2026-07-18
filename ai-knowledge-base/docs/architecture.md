# Architecture — AI Knowledge Base

## System Architecture

```mermaid
graph TB
    subgraph 用户端
        Browser["浏览器"]
    end

    subgraph 前端["Frontend (Docker)"]
        Nginx["Nginx (alpine)
                端口 8080
                SPA 路由 + API 反向代理"]
        VueApp["Vue 3 + TypeScript
                Element Plus UI
                Pinia 状态管理
                Axios HTTP 客户端"]
    end

    subgraph 后端["Backend (Docker)"]
        FastAPI["FastAPI (Uvicorn)
                 端口 8000
                 SSE 流式输出
                 JWT 认证"]
        Process["process_service
                 文档解析(PDF/DOCX/TXT)
                 Chunk 切分
                 Embedding → Qdrant"]
        RAG["RAG Pipeline
             检索 → 上下文组装 → LLM"]
    end

    subgraph 数据层["Data Layer (Docker)"]
        SQLite[("SQLite (默认)
                 知识库/文档/会话/反馈")]
        PG[("PostgreSQL 16 (可选)
             通过 DATABASE_URL 切换")]
        Qdrant[("Qdrant
                 向量数据库
                 语义搜索")]
        Redis[("Redis 7
                搜索缓存 5min
                会话缓存 30s")]
    end

    subgraph AI服务["AI Services (外部)"]
        LLM["DashScope Qwen API
              LLM 对话"]
        Embedding["DashScope
                    text-embedding-v3
                    1024 维"]
    end

    Browser -->|"http://localhost:8080"| Nginx
    Nginx -->|"/api/* 代理"| FastAPI
    Nginx -->|"静态资源"| VueApp
    FastAPI --> SQLite
    FastAPI --> PG
    FastAPI --> Qdrant
    FastAPI --> Redis
    FastAPI --> Process
    FastAPI --> RAG
    Process -->|"向量化"| Embedding
    Process -->|"存储"| Qdrant
    RAG -->|"检索"| Qdrant
    RAG -->|"生成回答"| LLM
```

## Data Flow

### Document Processing Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Backend
    participant Qdrant
    participant Embedding as Embedding API
    participant DB as SQLite/Postgres

    User->>Frontend: Upload document
    Frontend->>Backend: POST /documents (UploadFile)
    Backend->>DB: Save document (status=pending)
    Backend-->>Frontend: Return document info
    User->>Frontend: Click "Process"
    Frontend->>Backend: POST /documents/{id}/process

    Note over Backend: Read chunk params from settings
    Backend->>DB: Update status=processing
    Backend->>Backend: Parse file (PDF/DOCX/TXT)
    Backend->>Backend: Chunk text (fixed/recursive)
    Backend->>Embedding: Batch embed chunks
    Embedding-->>Backend: Return vectors
    Backend->>Qdrant: upsert vectors + metadata
    Backend->>DB: Save FTS5 index
    Backend->>DB: Update status=completed
    Backend->>Redis: Invalidate search cache
    Backend-->>Frontend: Return success
```

### Chat Q&A Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Backend
    participant Qdrant
    participant LLM as LLM API
    participant Redis
    participant DB as SQLite/Postgres

    User->>Frontend: Type question
    Frontend->>Backend: POST /chat (query + kb_id)
    Backend->>Backend: Build context from history

    Note over Backend: Read settings (top_k, threshold, hybrid, rerank)
    Backend->>DB: Check session list cache
    alt Cache hit
        Redis-->>Backend: Return cached sessions
    else Cache miss
        Backend->>DB: Query sessions
        Backend->>Redis: Cache sessions (30s TTL)
    end

    Note over Backend: Retrieve relevant chunks
    alt FTS Search with cache
        Backend->>Redis: Check search cache
        alt Cache hit
            Redis-->>Backend: Return cached results
        else Cache miss
            Backend->>DB: FTS5 search
            Backend->>Redis: Cache results (5min TTL)
        end
    end

    alt Semantic Search with cache
        Backend->>Redis: Check semantic cache
        alt Cache hit
            Redis-->>Backend: Return cached chunks
        else Cache miss
            Backend->>Qdrant: Vector search
            Backend->>Redis: Cache results (5min TTL)
        end
    end

    Note over Backend: Hybrid Search & Rerank
    Backend->>LLM: Send prompt + context
    LLM-->>Backend: Stream response (SSE)
    Backend-->>Frontend: SSE stream (tokens + sources + metrics)
    Frontend-->>User: Render with typing animation
```

## Service Dependencies

```mermaid
graph LR
    Frontend -->|depends_on| Backend
    Backend -->|depends_on| Qdrant
    Backend -->|depends_on| Redis
    Backend -->|optional| PG[(PostgreSQL)]
    PG -.->|profile: postgres| Backend

    style PG fill:#f9f,stroke:#333,stroke-width:1px
```

## Docker Services

| Service | Image | Port | Storage | Profile |
|---------|-------|------|---------|---------|
| frontend | node:22 → nginx:alpine | 8080:80 | — | default |
| backend | uv:python3.13-slim | 8000:8000 | uploads (volume) | default |
| qdrant | qdrant/qdrant:latest | 6333, 6334 | qdrant-data (volume) | default |
| redis | redis:7-alpine | 6379 | redis-data (volume) | default |
| db | postgres:16-alpine | 5432 | postgres-data (volume) | `--profile postgres` |
