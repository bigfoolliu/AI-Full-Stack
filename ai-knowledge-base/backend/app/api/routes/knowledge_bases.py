from fastapi import APIRouter, Query

from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.knowledge_base import CreateKnowledgeBaseRequest, KnowledgeBaseItem

router = APIRouter(prefix="/api", tags=["knowledge-bases"])


MOCK_KNOWLEDGE_BASES = [
    KnowledgeBaseItem(id=1, name="产品知识库", description="产品文档与FAQ", document_count=3, created_at="2026-06-28 20:00:00"),
    KnowledgeBaseItem(id=2, name="面试题知识库", description="AI 全栈转岗相关面试题与答案", document_count=12, created_at="2026-06-29 11:30:00"),
    KnowledgeBaseItem(id=3, name="项目规范知识库", description="开发规范、提交流程与项目约定", document_count=8, created_at="2026-06-30 09:15:00"),
    KnowledgeBaseItem(id=4, name="前端技术文档", description="Vue3 / React / TypeScript 技术总结", document_count=5, created_at="2026-07-01 08:00:00"),
    KnowledgeBaseItem(id=5, name="后端技术文档", description="FastAPI / Django / Spring Boot 笔记", document_count=7, created_at="2026-07-01 09:00:00"),
    KnowledgeBaseItem(id=6, name="算法与数据结构", description="面试高频算法题与解析", document_count=15, created_at="2026-07-01 10:00:00"),
    KnowledgeBaseItem(id=7, name="数据库知识库", description="MySQL / PostgreSQL / Redis 总结", document_count=6, created_at="2026-07-01 11:00:00"),
    KnowledgeBaseItem(id=8, name="DevOps 知识库", description="Docker / CI/CD / 部署方案", document_count=4, created_at="2026-07-01 12:00:00"),
    KnowledgeBaseItem(id=9, name="设计模式", description="常见设计模式与最佳实践", document_count=9, created_at="2026-07-02 08:00:00"),
    KnowledgeBaseItem(id=10, name="网络协议", description="HTTP / TCP / WebSocket 知识点", document_count=5, created_at="2026-07-02 09:00:00"),
    KnowledgeBaseItem(id=11, name="安全知识库", description="认证授权 / 加密 / OWASP", document_count=6, created_at="2026-07-02 10:00:00"),
]

MOCK_DOCUMENTS = {
    1: [
        {
            "id": 1,
            "name": "产品介绍.pdf",
            "status": "已完成",
            "updated_at": "2026-07-01 09:30:00",
        },
        {
            "id": 2,
            "name": "FAQ_v2.docx",
            "status": "解析中",
            "updated_at": "2026-07-01 10:05:00",
        },
    ],
    2: [
        {
            "id": 1,
            "name": "AI面试题合集.txt",
            "status": "待处理",
            "updated_at": "2026-07-01 11:15:00",
        }
    ],
    3: [],
}


@router.get("/knowledge-bases", response_model=ApiResponse)
def get_knowledge_bases(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> ApiResponse:
    total = len(MOCK_KNOWLEDGE_BASES)
    start = (page - 1) * page_size
    end = start + page_size
    items = MOCK_KNOWLEDGE_BASES[start:end]

    return ApiResponse(
        code=0,
        message="ok",
        data=PaginatedData(
            items=[item.model_dump() for item in items],
            total=total,
            page=page,
            page_size=page_size,
        ),
    )


@router.post("/knowledge-bases", response_model=ApiResponse)
def create_knowledge_base(payload: CreateKnowledgeBaseRequest) -> ApiResponse:
    next_id = max((item.id for item in MOCK_KNOWLEDGE_BASES), default=0) + 1
    created_item = KnowledgeBaseItem(
        id=next_id,
        name=payload.name,
        description=payload.description,
        document_count=0,
        created_at="2026-07-01 14:00:00",
    )
    MOCK_KNOWLEDGE_BASES.append(created_item)

    return ApiResponse(
        code=0,
        message="ok",
        data=created_item,
    )


@router.get("/knowledge-bases/{knowledge_base_id}", response_model=ApiResponse)
def get_knowledge_base_detail(knowledge_base_id: int) -> ApiResponse:
    for item in MOCK_KNOWLEDGE_BASES:
        if item.id == knowledge_base_id:
            return ApiResponse(code=0, message="ok", data=item)

    return ApiResponse(code=1, message="知识库不存在", data=None)


@router.get("/knowledge-bases/{knowledge_base_id}/documents", response_model=ApiResponse)
def get_knowledge_base_documents(knowledge_base_id: int) -> ApiResponse:
    for item in MOCK_KNOWLEDGE_BASES:
        if item.id == knowledge_base_id:
            return ApiResponse(
                code=0,
                message="ok",
                data=MOCK_DOCUMENTS.get(knowledge_base_id, []),
            )

    return ApiResponse(code=1, message="知识库不存在", data=None)


@router.post("/knowledge-bases/{knowledge_base_id}/documents", response_model=ApiResponse)
def upload_knowledge_base_document(
    knowledge_base_id: int,
    payload: dict,
) -> ApiResponse:
    for item in MOCK_KNOWLEDGE_BASES:
        if item.id == knowledge_base_id:
            current_documents = MOCK_DOCUMENTS.setdefault(knowledge_base_id, [])
            next_id = max((doc["id"] for doc in current_documents), default=0) + 1
            created_document = {
                "id": next_id,
                "name": payload.get("name", f"document-{next_id}.txt"),
                "status": "待处理",
                "updated_at": "2026-07-01 15:00:00",
            }
            current_documents.append(created_document)
            return ApiResponse(code=0, message="ok", data=created_document)

    return ApiResponse(code=1, message="知识库不存在", data=None)
