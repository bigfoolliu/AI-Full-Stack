from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import (
    COLLECTION_NAME,
    EMBEDDING_API_KEY,
    EMBEDDING_BASE_URL,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    QDRANT_URL,
)


class VectorService:
    """管理 Qdrant 向量集合：嵌入、检索、混合搜索。"""

    def __init__(self, collection_name: str = COLLECTION_NAME):
        self.collection_name = collection_name
        self.embedding_model = EMBEDDING_MODEL
        self.embedding_dimension = EMBEDDING_DIMENSION

        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.client = (
            OpenAI(
                api_key=EMBEDDING_API_KEY,
                base_url=EMBEDDING_BASE_URL,
            )
            if EMBEDDING_API_KEY
            else None
        )

        if self.client:
            self._ensure_collection()

    def _ensure_collection(self):
        """确保 Qdrant 集合已创建，不存在则新建。"""
        collections = self.qdrant.get_collections().collections
        existing = {c.name for c in collections}
        if self.collection_name not in existing:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE,
                ),
            )

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """调用 Embedding API 将文本列表转为向量。"""
        if not self.client:
            raise RuntimeError("DASHSCOPE_API_KEY 未设置，无法生成 Embedding")
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def upsert_chunks(
        self,
        chunks: list[dict],
        filename: str = "",
        status: str = "completed",
    ) -> int:
        """向量化 chunks 并写入 Qdrant，同时记录 payload 元信息。"""
        texts = [c["content"] for c in chunks]
        vectors = self.embed_texts(texts)

        points = []
        for chunk, vector in zip(chunks, vectors):
            point_id = f"{chunk['doc_id']}_{chunk['chunk_index']}"
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "doc_id": chunk["doc_id"],
                        "kb_id": chunk["kb_id"],
                        "chunk_index": chunk["chunk_index"],
                        "content": chunk["content"],
                        "page_number": chunk.get("page_number"),
                        "chunk_size": chunk["chunk_size"],
                        "filename": filename,
                        "status": status,
                    },
                )
            )

        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        return len(points)

    def search(
        self,
        query: str,
        kb_id: int | None = None,
        limit: int = 10,
        filename: str | None = None,
    ) -> list[dict]:
        """向量相似度搜索，支持 kb_id / filename 过滤。"""
        query_vector = self.embed_texts([query])[0]

        from qdrant_client.models import FieldCondition, Filter, MatchValue

        conditions: list[FieldCondition] = []
        if kb_id is not None:
            conditions.append(FieldCondition(key="kb_id", match=MatchValue(value=kb_id)))
        if filename:
            conditions.append(FieldCondition(key="filename", match=MatchValue(value=filename)))

        qdrant_filter = Filter(must=conditions) if conditions else None

        hits = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=limit,
        )

        return [
            {
                "doc_id": hit.payload.get("doc_id"),
                "kb_id": hit.payload.get("kb_id"),
                "chunk_index": hit.payload.get("chunk_index"),
                "content": hit.payload.get("content"),
                "filename": hit.payload.get("filename", ""),
                "page_number": hit.payload.get("page_number"),
                "score": hit.score,
            }
            for hit in hits
        ]

    def hybrid_search(
        self,
        query: str,
        kb_id: int,
        limit: int = 10,
        alpha: float = 0.3,
        filename: str | None = None,
    ) -> list[dict]:
        """向量搜索 + FTS 关键词搜索，按 alpha 权重融合排序。"""
        from sqlalchemy import text

        from app.core.database import SessionLocal

        vector_results = self.search(query=query, kb_id=kb_id, limit=limit, filename=filename)

        db = SessionLocal()
        try:
            fts_limit = limit * 2
            search_term = " OR ".join(f'"{p}"' for p in query.strip().split())
            if not search_term:
                return vector_results

            rows = db.execute(
                text(
                    """\
SELECT f.doc_id, f.filename, f.kb_id, f.content, f.rank
FROM document_fts f
WHERE f.document_fts MATCH :q AND f.kb_id = :kb_id
ORDER BY f.rank
LIMIT :limit
"""
                ),
                {"q": search_term, "kb_id": kb_id, "limit": fts_limit},
            ).fetchall()

            fts_results = [
                {
                    "doc_id": row.doc_id,
                    "filename": row.filename,
                    "kb_id": row.kb_id,
                    "content": row.content,
                    "score": row.rank,
                }
                for row in rows
            ]
        finally:
            db.close()

        return self._fuse_results(vector_results, fts_results, alpha=alpha, limit=limit)

    @staticmethod
    def _fuse_results(
        vector_results: list[dict],
        fts_results: list[dict],
        alpha: float = 0.3,
        limit: int = 10,
    ) -> list[dict]:
        """归一化向量分与 FTS 分后按 alpha 加权融合。"""
        doc_id_to_source: dict[int, dict] = {}
        seen_doc_ids: set[int] = set()

        max_v_score = max((r["score"] for r in vector_results), default=1.0)
        for r in vector_results:
            doc_id = r["doc_id"]
            r["_vector_score"] = r["score"]
            r["score"] = r["score"] / max_v_score if max_v_score > 0 else 0
            doc_id_to_source[doc_id] = r
            seen_doc_ids.add(doc_id)

        max_f_score = max((r["score"] for r in fts_results), default=1.0)
        for r in fts_results:
            doc_id = r["doc_id"]
            r["_fts_score"] = r["score"]
            norm_fts = r["score"] / max_f_score if max_f_score > 0 else 0
            if doc_id in seen_doc_ids:
                existing = doc_id_to_source[doc_id]
                existing["score"] = alpha * existing["score"] + (1 - alpha) * norm_fts
                existing["_vector_score"] = existing.get("_vector_score", 0)
                existing["_fts_score"] = norm_fts
            else:
                r["_vector_score"] = 0
                r["score"] = (1 - alpha) * norm_fts
                doc_id_to_source[doc_id] = r

        merged = sorted(doc_id_to_source.values(), key=lambda x: x["score"], reverse=True)
        for r in merged:
            r.pop("_vector_score", None)
            r.pop("_fts_score", None)

        return merged[:limit]

    def delete_document_chunks(self, doc_id: int):
        """从 Qdrant 中删除指定文档的所有向量块。"""
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        self.qdrant.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="doc_id",
                        match=MatchValue(value=doc_id),
                    )
                ]
            ),
        )
