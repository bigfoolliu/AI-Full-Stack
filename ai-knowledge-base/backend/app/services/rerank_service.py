import re


class RerankService:
    """
    对检索结果进行重排序，提高最终结果的相关性。

    策略（无需额外 API 调用）：
    1. 提取查询中的关键词
    2. 对每个候选块计算"关键词命中密度"
    3. 将命中密度与向量得分融合产生最终排序分
    """

    @staticmethod
    def rerank(query: str, chunks: list[dict], top_k: int | None = None) -> list[dict]:
        if not chunks:
            return chunks

        keywords = RerankService._extract_keywords(query)
        max_v_score = max((c.get("score", 0) for c in chunks), default=1.0)

        for chunk in chunks:
            content = chunk.get("content", "")
            match_count = sum(1 for kw in keywords if kw.lower() in content.lower())
            density = match_count / max(len(keywords), 1)
            normalized_v = chunk.get("score", 0) / max_v_score if max_v_score > 0 else 0
            chunk["_rerank_score"] = 0.6 * normalized_v + 0.4 * density
            chunk["_rerank_keyword_hits"] = match_count

        reranked = sorted(chunks, key=lambda c: c["_rerank_score"], reverse=True)

        for r in reranked:
            r["score"] = r["_rerank_score"]

        limit = top_k or len(reranked)
        return reranked[:limit]

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        cleaned = re.sub(r"[^\w\u4e00-\u9fff\s]", " ", text)
        tokens = cleaned.split()
        keywords = [t for t in tokens if len(t) > 1]
        return keywords if keywords else tokens[:5]


def compute_retrieval_metrics(chunks: list[dict], time_ms: float) -> dict:
    if not chunks:
        return {
            "total_chunks": 0,
            "used_chunks": 0,
            "score_min": 0.0,
            "score_max": 0.0,
            "score_avg": 0.0,
            "time_ms": round(time_ms, 1),
        }
    scores = [c.get("score", 0) for c in chunks]
    return {
        "total_chunks": len(chunks),
        "used_chunks": len(chunks),
        "score_min": round(min(scores), 4),
        "score_max": round(max(scores), 4),
        "score_avg": round(sum(scores) / len(scores), 4),
        "time_ms": round(time_ms, 1),
    }
