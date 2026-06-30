from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.knowledge_base import CreateKnowledgeBaseRequest, KnowledgeBaseItem

router = APIRouter(prefix="/api", tags=["knowledge-bases"])


MOCK_KNOWLEDGE_BASES = [
    KnowledgeBaseItem(
        id=1,
        name="产品知识库",
        description="产品文档与FAQ",
        document_count=3,
        created_at="2026-06-28 20:00:00",
    ),
    KnowledgeBaseItem(
        id=2,
        name="面试题知识库",
        description="AI 全栈转岗相关面试题与答案",
        document_count=12,
        created_at="2026-06-29 11:30:00",
    ),
    KnowledgeBaseItem(
        id=3,
        name="项目规范知识库",
        description="开发规范、提交流程与项目约定",
        document_count=8,
        created_at="2026-06-30 09:15:00",
    ),
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
def get_knowledge_bases() -> ApiResponse:
    return ApiResponse(
        code=0,
        message="ok",
        data=MOCK_KNOWLEDGE_BASES,
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
