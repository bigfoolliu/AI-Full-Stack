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

        self._ensure_collection()

    def _ensure_collection(self):
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
    ) -> int:
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
    ) -> list[dict]:
        query_vector = self.embed_texts([query])[0]

        qdrant_filter = None
        if kb_id is not None:
            from qdrant_client.models import FieldCondition, Filter, MatchValue

            qdrant_filter = Filter(
                must=[
                    FieldCondition(
                        key="kb_id",
                        match=MatchValue(value=kb_id),
                    )
                ]
            )

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

    def delete_document_chunks(self, doc_id: int):
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
