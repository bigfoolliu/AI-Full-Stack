# 配置参数说明

Week 7 将知识库的检索、Prompt、模型参数从硬编码改为页面可配置，所有参数持久化到 `knowledge_base_settings` 表，实时生效。

---

## 1. 检索参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `top_k` | int | 5 | 向量/混合检索返回的最大 chunk 数 |
| `similarity_threshold` | float | 0.0 | 相似度过滤阈值（0~1），低于此值的 chunk 被丢弃 |
| `hybrid_search` | bool | false | 是否启用 Hybrid Search（FTS + 向量融合） |
| `hybrid_alpha` | float | 0.3 | 融合权重：alpha * 向量分 + (1-alpha) * FTS 分 |
| `rerank_enabled` | bool | false | 是否启用 Rerank 重排序 |
| `rerank_top_k` | int | 5 | Rerank 后保留的最多 chunk 数 |

### 调优建议

**场景 1：知识库文档量大**
- 调高 `top_k` (10~15)，调低 `similarity_threshold` (0.2~0.3)
- 开启 `hybrid_search` 以捕获关键词命中

**场景 2：追求回答准确度**
- 调低 `top_k` (3~5)，调高 `similarity_threshold` (0.4~0.6)
- 开启 `rerank_enabled`，利用关键词密度二次排序

**场景 3：需要覆盖全面**
- 调高 `top_k` (10~15)，关闭 `similarity_threshold`
- 开启 `hybrid_search` + `rerank_enabled`

---

## 2. 模型参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model_name` | str | qwen-plus | LLM 模型 ID（从 `/api/models` 获取可选列表） |
| `temperature` | float | 0.7 | 生成随机性（0~2，越高越随机） |
| `max_tokens` | int | 2048 | 单次回答最大 token 数（256~8192） |

### 调优建议

- **创意型回答**：temperature 0.8~1.2
- **事实型回答**：temperature 0.1~0.4
- **长文档总结**：max_tokens 调高到 4096~8192

---

## 3. Prompt 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `system_prompt` | text | 见代码 | 系统指令模板，检索到的上下文自动追加到末尾 |

### 默认 Prompt

```
你是一个知识库问答助手。
请基于以下检索到的文档内容回答用户的问题。
如果文档内容不足以回答，请如实告知，不要编造。
```

### 变量说明

系统不支持模板变量。上下文始终自动附加到 prompt 末尾，格式为：

```
{system_prompt}

检索到的相关内容：
[1] 来源：{filename}
{content}
...
```

---

## 4. Rerank 策略

Rerank 使用**关键词密度 + 向量分数融合**策略，无需额外 API 调用：

1. 从查询中提取关键词（长度 > 1 的中/英文词）
2. 对每个 chunk 计算「关键词命中密度」= 命中数 / 关键词总数
3. 最终得分 = 0.6 × 归一化向量分 + 0.4 × 关键词密度
4. 按最终得分降序取 `rerank_top_k` 条

---

## 5. Hybrid Search 策略

向量搜索 + FTS 关键词搜索的结果按 RRF 风格融合：

1. 向量搜索结果归一化到 [0, 1]
2. FTS 搜索结果归一化到 [0, 1]
3. 最终得分 = alpha × 向量分 + (1 - alpha) × FTS 分
4. 按 doc_id 去重后取 top_k 条

---

## 6. 全链路时序

```text
用户提问
  ↓
读取知识库配置（settings）
  ↓
[向量搜索] / [Hybrid Search]   ← top_k * 3（若启用了 rerank）
  ↓
[相似度阈值过滤]               ← similarity_threshold
  ↓
[Rerank 重排序]                 ← rerank_enabled
  ↓
[指标统计]                      ← metrics（命中数、得分分布、耗时）
  ↓
[组装 system_prompt + 上下文]
  ↓
[LLM 生成回答]                  ← temperature / max_tokens / model_name
  ↓
返回 answer + sources + metrics
```

---

## 7. A/B 效果对比

`POST /api/knowledge-bases/{id}/chat/compare` 接受两组 `CompareConfig`，并行执行上述全链路后返回两路结果，便于对比不同参数配置的效果。
