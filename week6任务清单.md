## 1. 本周目标

第 6 周的目标是在 Week 5 的 RAG 检索链路之上，接入 LLM 实现问答对话，让项目 1 具备用户可见的核心能力。

到本周结束时，你应该具备以下成果：

- LLM 接入配置（DashScope / Qwen API）
- Chat 接口：query → 检索 → 上下文组装 → LLM 生成回答
- 流式输出（SSE）前端逐字渲染
- 前端 Chat 对话框 + 引用来源展示
- 多轮对话上下文管理
- （可选）会话历史记录

这一周的唯一目标可以概括为：

**能提问、能流式回答、能看引用、能继续聊。**

---

## 2. 本周完成标准

如果这一周结束时，你能做到以下几点，就算顺利完成：

- [ ] 配置 DashScope LLM API（区别于 Embedding 的对话模型）
- [ ] 可通过 API 向知识库提问并收到基于内容的回答
- [ ] 流式输出：后端逐字推送，前端逐字渲染
- [ ] 前端 Chat 对话框可发送消息、展示 AI 回复
- [ ] 回答中展示引用来源（文档名 + 片段 + 得分）
- [ ] 多轮对话中上下文正常传递
- [ ] 路由 `/knowledge-bases/:id/chat` 可访问

---

## 3. 本周项目范围

这一周主要做 RAG 问答对话，不要扩展到用户管理、权限等非核心功能。

### 3.1 页面范围

1. Chat 对话页 `/knowledge-bases/:id/chat`（新增）
2. 知识库详情页 `/knowledge-bases/:id/documents`（新增"问答"入口）

### 3.2 接口范围

1. `POST /api/knowledge-bases/{id}/chat` — 知识库问答（返回完整回答 + 引用）
2. `GET /api/knowledge-bases/{id}/chat/stream` — 知识库问答（SSE 流式）
3. `GET /api/knowledge-bases/{id}/chat/sessions` — 会话列表（Day 6）
4. `POST /api/knowledge-bases/{id}/chat/sessions` — 创建/保存会话（Day 6）

### 3.3 学习范围

只围绕这些知识点学：

- Prompt 拼接与上下文组装
- Chat Completion API（OpenAI 兼容格式）
- Server-Sent Events（SSE）
- FastAPI StreamingResponse
- 前端 EventSource / ReadableStream
- Markdown 渲染（markdown-it）
- 引用溯源设计
- 对话上下文管理

---

## 4. 每日执行清单

## Day 1：LLM 接入与 Chat 基础接口

### 目标

配置 LLM API，实现基础的 Chat 接口，用 Week 5 的向量检索结果作为上下文。

### 任务清单

- [x] 在 `config.py` 中增加 `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` 配置
- [x] 创建 `app/services/llm_service.py`
  - [x] 实现 `chat(query, context_chunks, history)` 函数
  - [x] 调用 DashScope Chat API（`qwen-plus` 或 `qwen-turbo`）
  - [x] 构造 prompt：系统指令 + 检索上下文 + 对话历史 + 用户问题
- [x] 创建 `POST /api/knowledge-bases/{id}/chat` 接口
  - [x] 请求：`{ query, history?, top_k? }`
  - [x] 内部调用 `VectorService.search()` 获取相关片段
  - [x] 组装 prompt → 调用 LLM
  - [x] 返回：`{ answer, sources: [{filename, content, score, page_number}] }`
- [x] 编写测试脚本验证 Chat 接口

### Prompt 模板建议

```text
你是一个知识库问答助手。
请基于以下检索到的文档内容回答用户的问题。
如果文档内容不足以回答，请如实告知，不要编造。

检索到的相关内容：
{context}

对话历史：
{history}

用户问题：{query}
```

### 验收标准

- LLM 能正常调用并返回回答
- 回答内容基于检索结果，可验证
- 无检索结果时能如实告知

---

## Day 2：流式输出（SSE）

### 目标

将 Chat 接口改为流式输出（SSE），前端逐字接收 AI 回复。

### 任务清单

- [ ] 创建 `POST /api/knowledge-bases/{id}/chat/stream` 接口
  - [ ] 使用 FastAPI `StreamingResponse` + `EventSourceResponse`
  - [ ] 先检索 + 组装 prompt（同步完成）
  - [ ] 流式调用 LLM API，逐 token yield
  - [ ] 格式：`data: {"type": "token", "content": "你"}\n\n`
  - [ ] 引用来源：`data: {"type": "sources", "data": [...]}\n\n`
  - [ ] 结束标记：`data: {"type": "done"}\n\n`
- [ ] 前端使用 `fetch` + `ReadableStream` 接收 SSE
- [ ] 处理连接中断和错误

### 验收标准

- 后端 SSE 端点可正常调用
- 前端可逐字接收到响应
- 连接中断可感知并提示用户

---

## Day 3：前端 Chat 对话框

### 目标

实现前端 Chat 对话页面，支持消息收发与流式展示。

### 任务清单

- [ ] 创建 `ChatView.vue`（`/knowledge-bases/:id/chat`）
- [ ] 消息列表组件（用户消息 / AI 消息 / 气泡样式）
- [ ] 底部输入框 + 发送按钮
- [ ] `Enter` 发送，`Shift+Enter` 换行
- [ ] 流式接收 → 逐字渲染（打字机效果）
- [ ] 安装并接入 markdown-it，AI 回复支持 Markdown 渲染
- [ ] AI 回答中的引用来源以卡片形式展示在回答下方
- [ ] 加载中状态（三点闪烁动画）
- [ ] 错误处理与重试机制
- [ ] 注册路由 `/knowledge-bases/:id/chat`
- [ ] 知识库详情页增加"问答"按钮入口

### 验收标准

- 可发送消息并看到 AI 回复（流式逐字展示）
- 回答中的 Markdown 正确渲染
- 引用来源可识别
- 页面风格与现有系统一致

---

## Day 4：多轮对话与上下文管理

### 目标

实现对话上下文传递，确保多轮对话中的连贯性。

### 任务清单

- [ ] 前端维护当前会话的消息列表（`ref<Message[]>`）
- [ ] 每次 Chat 请求携带 `history: [{role, content}]`
- [ ] 后端正确定义 history 在 prompt 中的位置
- [ ] 控制上下文长度（超出 token 限制时截断早期消息）
- [ ] 实现"新对话"按钮，清空当前上下文
- [ ] 实现"重新提问"按钮，重新发送同一条消息

### 上下文结构

```python
history = [
    {"role": "user", "content": "什么是 RAG？"},
    {"role": "assistant", "content": "RAG 是..."},
]
```

### 验收标准

- 多轮对话中上下文正确传递，AI 能引用前文
- "上下文"指什么、为什么重要，能讲清楚
- 历史过长时能自动截断

---

## Day 5：引用溯源与体验优化

### 目标

让用户能清晰看到 AI 回答的依据，打完基础交互体验。

### 任务清单

- [ ] 前端引用来源卡片：文档名 + 片段预览 + 相似度得分
- [ ] 引用与回答对应展示（回答段落下方附来源）
- [ ] 引用可点击展开查看完整片段
- [ ] 空知识库 / 无检索结果时的提示文案
- [ ] 消息时间戳展示
- [ ] 新消息自动滚屏到页面底部

### 验收标准

- 每个回答都能看到引用了哪些文档片段
- 引用信息对用户有实际参考价值
- 交互体验流畅

---

## Day 6：会话历史与管理

### 目标

将对话记录持久化到数据库，支持历史会话查看与恢复。

### 任务清单

- [ ] 创建 `chat_sessions` 表（id, kb_id, title, created_at, updated_at）
- [ ] 创建 `chat_messages` 表（id, session_id, role, content, created_at）
- [ ] Chat 流式接口结束时保存消息到数据库
- [ ] `GET /api/knowledge-bases/{id}/chat/sessions` — 会话列表
- [ ] `POST /api/knowledge-bases/{id}/chat/sessions` — 创建/更新会话
- [ ] 前端左侧会话列表（新建 / 切换 / 标题展示）
- [ ] 刷新页面后恢复当前会话

### 验收标准

- 刷新页面后对话记录不丢失
- 可查看和切换历史会话
- 可创建新会话

---

## Day 7：整理、复盘、封版

### 目标

不要继续加新功能，把第 6 周成果整理成一个干净的里程碑版本。

### 任务清单

- [ ] 检查所有接口命名和返回格式是否统一
- [ ] 检查 Chat 页面在不同知识库之间的数据隔离
- [ ] 补充 `docs/` 下的 LLM 接入与流式输出说明
- [ ] 更新 README，补充第 6 周新增功能
- [ ] 验证全链路：上传 → 解析 → 检索 → 问答 → 流式
- [ ] 记录下周任务清单（Week 7）

### 验收标准

- RAG 问答全链路可完整跑通
- 项目可被别人快速理解和运行
- 第 6 周有一个可展示、可继续开发的基础版本

---

## 5. 本周接口清单汇总

第 6 周新增以下接口：

1. `POST /api/knowledge-bases/{id}/chat` — 知识库问答（完整回答 + 引用来源）
2. `GET /api/knowledge-bases/{id}/chat/stream` — 知识库问答（SSE 流式）
3. `GET /api/knowledge-bases/{id}/chat/sessions` — 会话列表（Day 6）
4. `POST /api/knowledge-bases/{id}/chat/sessions` — 创建/更新会话（Day 6）

---

## 6. 本周页面清单汇总

第 6 周涉及以下页面改动：

| 页面 | 路径 | 类型 |
|------|------|------|
| Chat 对话页 | `/knowledge-bases/:id/chat` | 新增 |
| 知识库详情页 | `/knowledge-bases/:id/documents` | 修改（新增"问答"入口按钮） |

---

## 7. 本周知识点清单汇总

本周只围绕这些技术学习，不扩展到部署和工具调用：

- LLM API 调用（OpenAI 兼容格式）
- Chat Completion 与 Prompt 工程
- 检索上下文组装
- Server-Sent Events（SSE）
- FastAPI StreamingResponse
- 前端 EventSource / ReadableStream
- Markdown 渲染（markdown-it）
- 引用溯源设计
- 对话上下文管理
- SQLAlchemy 消息持久化

---

## 8. 本周完成后的状态

如果你能完成这份清单，第 6 周结束时你将拥有：

- 一个可运行的 RAG 问答对话系统
- 基于知识库内容的智能回答
- 流式输出的良好用户体验
- 前端 Chat 对话框组件（Markdown + 引用溯源）
- 多轮对话支持
- （可选）会话历史记录
- 一套可继续扩展的 RAG + LLM 代码结构

这一步很重要，因为它标志着你已经正式进入 **「AI 应用工程：对话与推理阶段」**。
