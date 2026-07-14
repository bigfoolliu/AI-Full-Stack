# LLM 接入与流式问答说明

## 架构概览

```text
用户提问 ──→ 向量检索 (Qdrant) ──→ 上下文组装 ──→ LLM 生成 ──→ SSE 流式返回
                                                      │
                                                      └─→ 会话持久化 (前端触发)
```

## 新增服务

| 服务 | 文件 | 职责 |
|------|------|------|
| `LlmService` | `app/services/llm_service.py` | Prompt 组装、Chat API 调用（完整 + 流式） |

## 流式问答接口

### `POST /api/knowledge-bases/{id}/chat/stream`

**请求：**

```json
{
  "query": "什么是 RAG？",
  "history": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的？"}
  ],
  "top_k": 5
}
```

**响应（SSE）：**

```
data: {"type": "token", "content": "RAG"}

data: {"type": "token", "content": " 是"}

data: {"type": "token", "content": "检索增强生成（Retrieval-Augmented Generation）..."}

data: {"type": "sources", "data": [{"doc_id": 1, "content": "...", "filename": "doc.pdf", "score": 0.89}]}

data: {"type": "done"}
```

### SSE 事件类型

| 类型 | 触发时机 | 内容 |
|------|----------|------|
| `token` | LLM 每生成一个 token | `content`: 文本片段 |
| `sources` | 所有 token 推送完成后 | `data`: 检索到的引用来源列表 |
| `done` | SSE 结束 | 无额外数据 |

### `POST /api/knowledge-bases/{id}/chat`（非流式）

返回完整 answer + sources，适用于无需流式渲染的场景。

## LLM 配置

| 项目 | 值 |
|------|-----|
| 提供方 | Alibaba DashScope (OpenAI 兼容) |
| API Base | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 默认模型 | `qwen-plus` |
| 环境变量 | `LLM_API_KEY`（回退到 `DASHSCOPE_API_KEY`） |
| 自定义 | `LLM_BASE_URL` / `LLM_MODEL` 可覆盖 |

## Prompt 模板

```
你是一个知识库问答助手。
请基于以下检索到的文档内容回答用户的问题。
如果文档内容不足以回答，请如实告知，不要编造。

检索到的相关内容：
[1] 来源：文档名
文档内容片段...

对话历史：
user: 之前的问题
assistant: 之前的回答

用户问题：当前问题
```

## 上下文管理

- `LlmService._build_messages()` 组装 system + history + user query
- 历史按 `MAX_HISTORY_TOKENS`（默认 2000）限制截断
- 优先保留最近的对话，从后往前裁剪
- 截断按字符估算（1 token ≈ 4 char），超出时丢弃最早消息

## 会话持久化

流式回答完成后，**由前端触发保存**：

1. 流式接收完成（`done` 事件）
2. 前端将用户消息 + AI 回答合并为完整消息列表
3. 调用 `POST /api/knowledge-bases/{id}/chat/sessions` 写入数据库

### 会话管理接口

| 方法 | 路径 | 用途 |
|------|------|------|
| `GET` | `/api/knowledge-bases/{id}/chat/sessions` | 列出会话（含 active_session） |
| `POST` | `/api/knowledge-bases/{id}/chat/sessions` | 创建新会话 / 更新已有会话 |

### 数据库表

**chat_sessions**: `id, knowledge_base_id, title, created_at, updated_at`
**chat_messages**: `id, session_id, role, content, created_at`

## 前端流式接收

使用 `fetch` + `ReadableStream` 手动解析 SSE：

```typescript
// frontend/src/api/knowledge-bases.ts — chatStream()
const response = await fetch(url, { method: "POST", body: JSON.stringify(payload) });
const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = "";

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  buffer += decoder.decode(value, { stream: true });
  // 按行解析 data: {...}
}
```

## 前端 Chat 页面

`/knowledge-bases/:id/chat` → `ChatView.vue`

- 左侧会话历史侧边栏（新建 / 切换）
- 消息列表（用户气泡 + AI Markdown 渲染）
- 引用来源卡片（文档名 + 片段预览 + 相似度得分）
- 流式逐字渲染（打字机效果）
- Enter 发送 / Shift+Enter 换行
- 重新提问 / 重试 / 新对话

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| LLM API Key 未配置 | 返回提示消息，不调用 LLM |
| Qdrant 不可用 | 跳过向量检索，LLM 基于空上下文回答 |
| 网络中断 | 前端 AbortController 中止，显示重试按钮 |
| 空知识库 | 显示提示文案引导用户上传文档 |
