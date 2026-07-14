"""
知识库 api
"""

import os
import time

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import EMBEDDING_API_KEY, UPLOAD_DIR
from app.core.security import get_current_user, get_db
from app.models import ChatMessage, ChatSession, Document, KnowledgeBase, KnowledgeBaseSetting, User
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.knowledge_base import (
    ChatRequest,
    ChatSessionMessagePayload,
    CreateKnowledgeBaseRequest,
    KnowledgeBaseItem,
    KnowledgeBaseSettingItem,
    SaveChatSessionRequest,
    SemanticSearchRequest,
    UpdateKnowledgeBaseSettingRequest,
)
from app.services.llm_service import LlmService
from app.services.process_service import process_document
from app.services.search_service import search_documents
from app.services.vector_service import VectorService

router = APIRouter(prefix="/api", tags=["knowledge-bases"])


def _filter_by_threshold(chunks: list[dict], threshold: float) -> list[dict]:
    if threshold <= 0 or not chunks:
        return chunks
    return [c for c in chunks if c.get("score", 1.0) >= threshold]


def _format_datetime(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _build_session_title(messages: list[ChatSessionMessagePayload]) -> str:
    first_user = next((msg.content.strip() for msg in messages if msg.role == "user" and msg.content.strip()), "")
    if not first_user:
        return "新对话"
    return first_user[:40]


def _serialize_chat_session(session: ChatSession, messages: list[ChatMessage]) -> dict:
    return {
        "id": session.id,
        "knowledge_base_id": session.knowledge_base_id,
        "title": session.title,
        "created_at": _format_datetime(session.created_at),
        "updated_at": _format_datetime(session.updated_at or session.created_at),
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": _format_datetime(message.created_at),
            }
            for message in messages
        ],
    }


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
        query = query.filter(KnowledgeBase.name.ilike(kw) | KnowledgeBase.description.ilike(kw))

    total = query.count()
    items = query.order_by(KnowledgeBase.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    counts = db.query(Document.knowledge_base_id, func.count(Document.id)).group_by(Document.knowledge_base_id).all()
    doc_counts = {kb_id: count for kb_id, count in counts}

    result = [
        KnowledgeBaseItem(
            id=kb.id,
            name=kb.name,
            description=kb.description,
            document_count=doc_counts.get(kb.id, 0),
            created_at=_format_datetime(kb.created_at),
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
            created_at=_format_datetime(kb.created_at),
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

    doc_count = db.query(Document).filter(Document.knowledge_base_id == knowledge_base_id).count()

    return ApiResponse(
        code=0,
        message="ok",
        data=KnowledgeBaseItem(
            id=kb.id,
            name=kb.name,
            description=kb.description,
            document_count=doc_count,
            created_at=_format_datetime(kb.created_at),
        ),
    )


@router.get("/knowledge-bases/{knowledge_base_id}/documents", response_model=ApiResponse)
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
        data={
            "items": [
                {
                    "id": doc.id,
                    "name": doc.filename,
                    "status": _status_label(doc.status),
                    "updated_at": _format_datetime(doc.created_at),
                }
                for doc in docs
            ],
            "total": len(docs),
        },
    )


@router.post("/knowledge-bases/{knowledge_base_id}/documents", response_model=ApiResponse)
async def upload_knowledge_base_document(
    knowledge_base_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """
    上传文件，保存后 status = pending，后续通过 process 接口触发处理
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
        status="pending",
        file_path=f"/uploads/{knowledge_base_id}/{safe_name}",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return ApiResponse(
        code=0,
        message="ok",
        data={
            "id": doc.id,
            "name": file.filename,
            "status": _status_label(doc.status),
            "updated_at": _format_datetime(doc.created_at),
            "file_size": len(content),
            "file_path": doc.file_path,
        },
    )


@router.post("/documents/{document_id}/process", response_model=ApiResponse)
def process_knowledge_base_document(
    document_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    """
    触发文档处理：解析 → 切分 → 向量化 → 入库
    """
    try:
        doc = process_document(document_id, db)
        return ApiResponse(
            code=0,
            message="ok",
            data={
                "id": doc.id,
                "name": doc.filename,
                "status": _status_label(doc.status),
                "updated_at": _format_datetime(doc.created_at),
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        doc = db.query(Document).filter(Document.id == document_id).first()
        return ApiResponse(
            code=1,
            message="处理失败",
            data={
                "id": document_id,
                "status": _status_label(doc.status if doc else "failed"),
                "error": str(e),
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
            "created_at": _format_datetime(doc.created_at),
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
                    "knowledge_base_id": item.knowledge_base_id,
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


@router.post("/knowledge-bases/{knowledge_base_id}/search", response_model=ApiResponse)
def search_knowledge_base_semantic(
    knowledge_base_id: int,
    req: SemanticSearchRequest,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    if not EMBEDDING_API_KEY:
        return ApiResponse(
            code=1,
            message="语义搜索需要配置 DASHSCOPE_API_KEY",
            data=[],
        )

    settings = _get_or_create_settings(knowledge_base_id, db)
    svc = VectorService()
    results = svc.search(query=req.query, kb_id=knowledge_base_id, limit=req.top_k or settings.top_k)

    return ApiResponse(code=0, message="ok", data=results)


@router.post("/knowledge-bases/{knowledge_base_id}/chat", response_model=ApiResponse)
def chat_with_knowledge_base(
    knowledge_base_id: int,
    req: ChatRequest,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    settings = _get_or_create_settings(knowledge_base_id, db)

    context_chunks = []
    if EMBEDDING_API_KEY:
        svc = VectorService()
        try:
            context_chunks = svc.search(query=req.query, kb_id=knowledge_base_id, limit=settings.top_k)
            context_chunks = _filter_by_threshold(context_chunks, settings.similarity_threshold)
        except RuntimeError:
            pass

    llm = LlmService()
    result = llm.chat(query=req.query, context_chunks=context_chunks, history=req.history)

    return ApiResponse(
        code=0,
        message="ok",
        data={
            "answer": result["answer"],
            "sources": result["sources"],
        },
    )


@router.post("/knowledge-bases/{knowledge_base_id}/chat/stream")
def chat_stream_with_knowledge_base(
    knowledge_base_id: int,
    req: ChatRequest,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    settings = _get_or_create_settings(knowledge_base_id, db)

    context_chunks = []
    if EMBEDDING_API_KEY:
        svc = VectorService()
        try:
            context_chunks = svc.search(query=req.query, kb_id=knowledge_base_id, limit=settings.top_k)
            context_chunks = _filter_by_threshold(context_chunks, settings.similarity_threshold)
        except RuntimeError:
            pass

    llm = LlmService()
    return StreamingResponse(
        llm.chat_stream(query=req.query, context_chunks=context_chunks, history=req.history),
        media_type="text/event-stream",
    )


@router.get("/knowledge-bases/{knowledge_base_id}/chat/sessions", response_model=ApiResponse)
def get_chat_sessions(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    sessions = (
        db.query(ChatSession)
        .filter(ChatSession.knowledge_base_id == knowledge_base_id)
        .order_by(ChatSession.updated_at.desc(), ChatSession.id.desc())
        .all()
    )
    session_ids = [session.id for session in sessions]
    message_map: dict[int, list[ChatMessage]] = {session_id: [] for session_id in session_ids}
    if session_ids:
        all_messages = (
            db.query(ChatMessage).filter(ChatMessage.session_id.in_(session_ids)).order_by(ChatMessage.id.asc()).all()
        )
        for message in all_messages:
            message_map.setdefault(message.session_id, []).append(message)

    active_session = None
    if sessions:
        latest = sessions[0]
        active_session = _serialize_chat_session(latest, message_map.get(latest.id, []))

    return ApiResponse(
        code=0,
        message="ok",
        data={
            "items": [
                {
                    "id": session.id,
                    "knowledge_base_id": session.knowledge_base_id,
                    "title": session.title,
                    "created_at": _format_datetime(session.created_at),
                    "updated_at": _format_datetime(session.updated_at or session.created_at),
                    "messages": [
                        {
                            "id": message.id,
                            "role": message.role,
                            "content": message.content,
                            "created_at": _format_datetime(message.created_at),
                        }
                        for message in message_map.get(session.id, [])
                    ],
                }
                for session in sessions
            ],
            "active_session": active_session,
        },
    )


@router.post("/knowledge-bases/{knowledge_base_id}/chat/sessions", response_model=ApiResponse)
def save_chat_session(
    knowledge_base_id: int,
    payload: SaveChatSessionRequest,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    if not payload.messages:
        raise HTTPException(status_code=400, detail="消息不能为空")

    if payload.session_id is None:
        session = ChatSession(
            knowledge_base_id=knowledge_base_id,
            title=_build_session_title(payload.messages),
        )
        db.add(session)
        db.flush()
    else:
        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == payload.session_id,
                ChatSession.knowledge_base_id == knowledge_base_id,
            )
            .first()
        )
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        db.query(ChatMessage).filter(ChatMessage.session_id == session.id).delete()
        session.title = _build_session_title(payload.messages)
        session.updated_at = func.now()

    for item in payload.messages:
        db.add(
            ChatMessage(
                session_id=session.id,
                role=item.role,
                content=item.content,
            )
        )

    db.commit()
    db.refresh(session)

    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).order_by(ChatMessage.id.asc()).all()

    return ApiResponse(
        code=0,
        message="ok",
        data=_serialize_chat_session(session, messages),
    )


def _serialize_settings(s: KnowledgeBaseSetting) -> KnowledgeBaseSettingItem:
    return KnowledgeBaseSettingItem(
        id=s.id,
        knowledge_base_id=s.knowledge_base_id,
        top_k=s.top_k,
        similarity_threshold=s.similarity_threshold,
        system_prompt=s.system_prompt,
        temperature=s.temperature,
        max_tokens=s.max_tokens,
        model_name=s.model_name,
        hybrid_search=s.hybrid_search,
        hybrid_alpha=s.hybrid_alpha,
        updated_at=_format_datetime(s.updated_at) if s.updated_at else "",
    )


def _get_or_create_settings(knowledge_base_id: int, db: Session) -> KnowledgeBaseSetting:
    settings = (
        db.query(KnowledgeBaseSetting).filter(KnowledgeBaseSetting.knowledge_base_id == knowledge_base_id).first()
    )
    if settings:
        return settings
    settings = KnowledgeBaseSetting(knowledge_base_id=knowledge_base_id)
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


@router.get("/knowledge-bases/{knowledge_base_id}/settings", response_model=ApiResponse)
def get_knowledge_base_settings(
    knowledge_base_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    settings = _get_or_create_settings(knowledge_base_id, db)
    return ApiResponse(code=0, message="ok", data=_serialize_settings(settings).model_dump())


@router.put("/knowledge-bases/{knowledge_base_id}/settings", response_model=ApiResponse)
def update_knowledge_base_settings(
    knowledge_base_id: int,
    payload: UpdateKnowledgeBaseSettingRequest,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse:
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    settings = _get_or_create_settings(knowledge_base_id, db)
    if payload.top_k is not None:
        settings.top_k = payload.top_k
    if payload.similarity_threshold is not None:
        settings.similarity_threshold = payload.similarity_threshold
    db.commit()
    db.refresh(settings)
    return ApiResponse(code=0, message="ok", data=_serialize_settings(settings).model_dump())


def _status_label(status: str) -> str:
    labels = {
        "pending": "待处理",
        "processing": "处理中",
        "completed": "已完成",
        "failed": "处理失败",
    }
    return labels.get(status, status)
