import os

from sqlalchemy.orm import Session

from app.core.config import EMBEDDING_API_KEY, UPLOAD_DIR
from app.core.redis_client import cache_delete_pattern
from app.models import Document, KnowledgeBaseSetting
from app.services.chunk_service import chunk_text, recursive_chunk_text
from app.services.document_parser import parse_document
from app.services.search_service import create_fts_index
from app.services.vector_service import VectorService


def _get_chunk_params(knowledge_base_id: int, db: Session) -> dict:
    """从知识库配置中读取 chunk 参数，不存在时返回默认值。"""
    setting = db.query(KnowledgeBaseSetting).filter(KnowledgeBaseSetting.knowledge_base_id == knowledge_base_id).first()
    if setting:
        return {
            "chunk_size": setting.chunk_size,
            "overlap": setting.overlap,
            "chunk_strategy": setting.chunk_strategy,
        }
    return {"chunk_size": 512, "overlap": 64, "chunk_strategy": "recursive"}


def process_document(document_id: int, db: Session) -> Document:
    """解析文档 → 切分 → 向量化 → 建立 FTS 索引的完整处理流程。"""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise ValueError(f"文档不存在: {document_id}")

    doc.status = "processing"
    db.commit()

    try:
        rel_path = doc.file_path.lstrip("/").removeprefix("uploads/")
        abs_path = os.path.join(UPLOAD_DIR, rel_path)
        ext = doc.filename.rsplit(".", 1)[-1] if "." in doc.filename else ""
        text = parse_document(abs_path, ext)
        doc.content = text

        params = _get_chunk_params(doc.knowledge_base_id, db)
        chunk_fn = chunk_text if params["chunk_strategy"] == "fixed" else recursive_chunk_text
        chunks = chunk_fn(
            text,
            chunk_size=params["chunk_size"],
            overlap=params["overlap"],
            doc_id=doc.id,
            kb_id=doc.knowledge_base_id,
        )

        if EMBEDDING_API_KEY and chunks:
            vector_svc = VectorService()
            vector_svc.delete_document_chunks(doc.id)
            vector_svc.upsert_chunks(chunks, filename=doc.filename, status=doc.status)

        doc.status = "completed"
        db.commit()
        create_fts_index(db, doc)

        kb_id = doc.knowledge_base_id
        cache_delete_pattern(f"kb:search:{kb_id}:*")
        cache_delete_pattern(f"kb:semantic:{kb_id}:*")

        return doc
    except Exception as e:
        doc.content = str(e)
        doc.status = "failed"
        db.commit()
        raise
