from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Document


@dataclass
class SearchResultItem:
    id: int
    filename: str
    kb_id: int
    status: str
    snippet: str
    score: float
    created_at: str


@dataclass
class SearchResults:
    items: list[SearchResultItem]
    total: int
    page: int
    page_size: int


def create_fts_index(db: Session, document: Document) -> None:
    """
    文件内容表
    """

    if document.status != "completed" or not document.content:
        return

    doc_id = document.id
    kb_id = document.knowledge_base_id
    filename = document.filename
    content = document.content

    db.execute(
        text("DELETE FROM document_fts WHERE doc_id = :doc_id"),
        {"doc_id": doc_id},
    )
    db.execute(
        text(
            "INSERT INTO document_fts (doc_id, kb_id, filename, content) VALUES (:doc_id, :kb_id, :filename, :content)"
        ),
        {"doc_id": doc_id, "kb_id": kb_id, "filename": filename, "content": content},
    )
    db.commit()


def search_documents(
    db: Session,
    kb_id: int,
    keyword: str,
    status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> SearchResults:
    """
    根据关键字搜索文档
    """

    search_term = _fts_query(keyword)

    status_filter = ""
    if status:
        status_filter = " AND d.status = :status"

    count_sql = text(
        """\
SELECT COUNT(*)
FROM document_fts f
JOIN documents d ON d.id = f.doc_id
WHERE f.document_fts MATCH :q AND f.kb_id = :kb_id"""
        + status_filter
    )
    params = {"q": search_term, "kb_id": kb_id}
    if status:
        params["status"] = status
    total = db.execute(count_sql, params).scalar() or 0

    data_sql = text(
        """\
SELECT f.doc_id, f.filename, f.kb_id, d.status, d.created_at,
       snippet(f.document_fts, 3, '<mark>', '</mark>', '...', 32) AS snippet,
       f.rank
FROM document_fts f
JOIN documents d ON d.id = f.doc_id
WHERE f.document_fts MATCH :q AND f.kb_id = :kb_id"""
        + status_filter
        + """
ORDER BY f.rank
LIMIT :limit OFFSET :offset
"""
    )
    data_params = {
        "q": search_term,
        "kb_id": kb_id,
        "limit": page_size,
        "offset": (page - 1) * page_size,
    }
    if status:
        data_params["status"] = status
    rows = db.execute(data_sql, data_params).fetchall()

    items = [
        SearchResultItem(
            id=row.doc_id,
            filename=row.filename,
            kb_id=row.kb_id,
            status=row.status,
            snippet=row.snippet,
            score=row.rank,
            created_at=row.created_at,
        )
        for row in rows
    ]

    return SearchResults(items=items, total=total, page=page, page_size=page_size)


def _fts_query(keyword: str) -> str:
    parts = keyword.strip().split()
    if not parts:
        return ""
    return " OR ".join(f'"{p}"' for p in parts)
