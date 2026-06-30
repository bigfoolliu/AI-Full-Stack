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
