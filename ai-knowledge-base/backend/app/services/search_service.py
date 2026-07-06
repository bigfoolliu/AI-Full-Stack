from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Document


@dataclass
class SearchResultItem:
    id: int
    filename: str
    kb_id: int
    snippet: str
    score: float


@dataclass
class SearchResults:
    items: list[SearchResultItem]
    total: int
    page: int
    page_size: int


def create_fts_index(db: Session, document: Document) -> None:
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
            "INSERT INTO document_fts (doc_id, kb_id, filename, content) "
            "VALUES (:doc_id, :kb_id, :filename, :content)"
        ),
        {"doc_id": doc_id, "kb_id": kb_id, "filename": filename, "content": content},
    )
    db.commit()


def search_documents(
    db: Session,
    kb_id: int,
    keyword: str,
    page: int = 1,
    page_size: int = 10,
) -> SearchResults:
    search_term = _fts_query(keyword)

    count_sql = text(
        "SELECT COUNT(*) FROM document_fts WHERE document_fts MATCH :q AND kb_id = :kb_id"
    )
    total = db.execute(count_sql, {"q": search_term, "kb_id": kb_id}).scalar() or 0

    data_sql = text(
        """\
SELECT doc_id, filename, kb_id,
       snippet(document_fts, 3, '<mark>', '</mark>', '...', 32) AS snippet,
       rank
FROM document_fts
WHERE document_fts MATCH :q AND kb_id = :kb_id
ORDER BY rank
LIMIT :limit OFFSET :offset
"""
    )
    rows = db.execute(
        data_sql,
        {
            "q": search_term,
            "kb_id": kb_id,
            "limit": page_size,
            "offset": (page - 1) * page_size,
        },
    ).fetchall()

    items = [
        SearchResultItem(
            id=row.doc_id,
            filename=row.filename,
            kb_id=row.kb_id,
            snippet=row.snippet,
            score=row.rank,
        )
        for row in rows
    ]

    return SearchResults(items=items, total=total, page=page, page_size=page_size)


def _fts_query(keyword: str) -> str:
    parts = keyword.strip().split()
    if not parts:
        return ""
    return " OR ".join(f'"{p}"' for p in parts)
