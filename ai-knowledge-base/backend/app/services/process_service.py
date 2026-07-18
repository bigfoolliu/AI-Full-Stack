import os

from sqlalchemy.orm import Session

from app.core.config import EMBEDDING_API_KEY, UPLOAD_DIR
from app.models import Document
from app.services.chunk_service import recursive_chunk_text
from app.services.document_parser import parse_document
from app.services.search_service import create_fts_index
from app.services.vector_service import VectorService


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

        chunks = recursive_chunk_text(
            text,
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
        return doc
    except Exception as e:
        doc.content = str(e)
        doc.status = "failed"
        db.commit()
        raise
