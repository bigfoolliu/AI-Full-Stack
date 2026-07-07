"""
知识库 api
"""

import os
import time

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from sqlalchemy import func

from app.core.config import UPLOAD_DIR
from app.core.security import get_current_user, get_db
from app.models import Document, KnowledgeBase, User
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.knowledge_base import CreateKnowledgeBaseRequest, KnowledgeBaseItem
from app.services.document_parser import parse_document
from app.services.search_service import create_fts_index, search_documents

router = APIRouter(prefix="/api", tags=["knowledge-bases"])


@router.get("/knowledge-bases", response_model=ApiResponse)
def get_knowledge_bases(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    keyword: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """
    知识库列表
    """

    query = db.query(KnowledgeBase)

    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            KnowledgeBase.name.ilike(kw) | KnowledgeBase.description.ilike(kw)
        )

    total = query.count()
    items = (
        query.order_by(KnowledgeBase.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    counts = (
        db.query(Document.knowledge_base_id, func.count(Document.id))
        .group_by(Document.knowledge_base_id)
        .all()
    )
    doc_counts = {kb_id: count for kb_id, count in counts}

    result = [
        KnowledgeBaseItem(
            id=kb.id,
            name=kb.name,
            description=kb.description,
            document_count=doc_counts.get(kb.id, 0),
            created_at=kb.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )
        for kb in items
    ]

    return ApiResponse(
        code=0,
        message="ok",
        data=PaginatedData(
            items=[item.model_dump() for item in result],
            total=total,
            page=page,
            page_size=page_size,
        ),
    )


@router.post("/knowledge-bases", response_model=ApiResponse)
def create_knowledge_base(
    payload: CreateKnowledgeBaseRequest,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """
    创建知识库
    """

    kb = KnowledgeBase(name=payload.name, description=payload.description)
    db.add(kb)
    db.commit()
    db.refresh(kb)

    return ApiResponse(
        code=0,
        message="ok",
        data=KnowledgeBaseItem(
            id=kb.id,
            name=kb.name,
            description=kb.description,
            document_count=0,
            created_at=kb.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )


@router.get("/knowledge-bases/{knowledge_base_id}", response_model=ApiResponse)
def get_knowledge_base_detail(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """
    查看单个知识库的详细信息
    """

    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    doc_count = (
        db.query(Document)
        .filter(Document.knowledge_base_id == knowledge_base_id)
        .count()
    )

    return ApiResponse(
        code=0,
        message="ok",
        data=KnowledgeBaseItem(
            id=kb.id,
            name=kb.name,
            description=kb.description,
            document_count=doc_count,
            created_at=kb.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )


@router.get(
    "/knowledge-bases/{knowledge_base_id}/documents", response_model=ApiResponse
)
def get_knowledge_base_documents(
    knowledge_base_id: int,
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """
    查看单个知识库下的所有文档
    """

    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    query = db.query(Document).filter(Document.knowledge_base_id == knowledge_base_id)
    if status:
        query = query.filter(Document.status == status)

    docs = query.order_by(Document.id.desc()).all()

    return ApiResponse(
        code=0,
        message="ok",
        data=[
            {
                "id": doc.id,
                "name": doc.filename,
                "status": _status_label(doc.status),
                "updated_at": doc.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for doc in docs
        ],
    )


@router.post(
    "/knowledge-bases/{knowledge_base_id}/documents", response_model=ApiResponse
)
async def upload_knowledge_base_document(
    knowledge_base_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """
    上传文档的时候开始解析文档
    """

    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    upload_dir = os.path.join(UPLOAD_DIR, str(knowledge_base_id))
    os.makedirs(upload_dir, exist_ok=True)

    ts = int(time.time() * 1000)
    safe_name = f"{ts}_{file.filename}"
    file_path = os.path.join(upload_dir, safe_name)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    doc = Document(
        knowledge_base_id=knowledge_base_id,
        filename=file.filename,
        status="parsing",
        file_path=f"/uploads/{knowledge_base_id}/{safe_name}",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    ext = (
        (file.filename or "").rsplit(".", 1)[-1] if "." in (file.filename or "") else ""
    )
    try:
        text = parse_document(file_path, ext)
        doc.content = text
        doc.status = "completed"
        db.commit()
        create_fts_index(db, doc)
    except Exception as e:
        doc.content = str(e)
        doc.status = "failed"
        db.commit()

    return ApiResponse(
        code=0,
        message="ok",
        data={
            "id": doc.id,
            "name": file.filename,
            "status": _status_label(doc.status),
            "updated_at": doc.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "file_size": len(content),
            "file_path": doc.file_path,
        },
    )


@router.get(
    "/knowledge-bases/{knowledge_base_id}/documents/{document_id}/content",
    response_model=ApiResponse,
)
def get_document_content(
    knowledge_base_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    doc = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.knowledge_base_id == knowledge_base_id,
        )
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")

    content_preview = (doc.content or "")[:5000]

    return ApiResponse(
        code=0,
        message="ok",
        data={
            "id": doc.id,
            "name": doc.filename,
            "status": _status_label(doc.status),
            "content": content_preview,
            "created_at": doc.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )


@router.get("/knowledge-bases/{knowledge_base_id}/search", response_model=ApiResponse)
def search_knowledge_base_documents(
    knowledge_base_id: int,
    q: str = Query(default="", min_length=1),
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    if not q.strip():
        return ApiResponse(
            code=0,
            message="ok",
            data={"items": [], "total": 0, "page": page, "page_size": page_size},
        )

    results = search_documents(
        db,
        kb_id=knowledge_base_id,
        keyword=q,
        status=status,
        page=page,
        page_size=page_size,
    )

    return ApiResponse(
        code=0,
        message="ok",
        data={
            "items": [
                {
                    "id": item.id,
                    "filename": item.filename,
                    "kb_id": item.kb_id,
                    "status": _status_label(item.status),
                    "snippet": item.snippet,
                    "updated_at": item.created_at,
                }
                for item in results.items
            ],
            "total": results.total,
            "page": results.page,
            "page_size": results.page_size,
        },
    )


def _status_label(status: str) -> str:
    labels = {
        "pending": "待处理",
        "parsing": "解析中",
        "completed": "已完成",
        "failed": "解析失败",
    }
    return labels.get(status, status)
