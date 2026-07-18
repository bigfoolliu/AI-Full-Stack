from pydantic import BaseModel


class KnowledgeBaseItem(BaseModel):
    """知识库列表项（含文档计数）。"""

    id: int
    name: str
    description: str
    document_count: int
    created_at: str


class CreateKnowledgeBaseRequest(BaseModel):
    """创建知识库请求体。"""

    name: str
    description: str


class SearchFilter(BaseModel):
    """检索过滤条件：按文件名/状态筛选。"""

    filename: str | None = None
    status: str | None = None


class ChatRequest(BaseModel):
    """聊天请求体。"""

    query: str
    history: list[dict] | None = None
    top_k: int = 5
    filter: SearchFilter | None = None


class ChatSessionMessagePayload(BaseModel):
    """对话消息体。"""

    role: str
    content: str


class SaveChatSessionRequest(BaseModel):
    """保存/更新对话请求体。"""

    session_id: int | None = None
    messages: list[ChatSessionMessagePayload]


class SemanticSearchRequest(BaseModel):
    """语义搜索请求体。"""

    query: str
    top_k: int = 5
    filter: SearchFilter | None = None


class KnowledgeBaseSettingItem(BaseModel):
    """知识库配置项（返回数据）。"""

    id: int
    knowledge_base_id: int
    top_k: int
    similarity_threshold: float
    system_prompt: str | None = None
    temperature: float
    max_tokens: int
    model_name: str | None = None
    hybrid_search: bool
    hybrid_alpha: float
    rerank_enabled: bool
    rerank_top_k: int
    updated_at: str


class UpdateKnowledgeBaseSettingRequest(BaseModel):
    """更新知识库配置请求体（所有字段可选）。"""

    top_k: int | None = None
    similarity_threshold: float | None = None
    system_prompt: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    model_name: str | None = None
    hybrid_search: bool | None = None
    hybrid_alpha: float | None = None
    rerank_enabled: bool | None = None
    rerank_top_k: int | None = None


class ChatFeedbackRequest(BaseModel):
    """聊天反馈请求体。"""

    session_id: int
    message_id: int
    feedback: str
    comment: str | None = None


class CompareConfig(BaseModel):
    """效果对比单侧参数配置。"""

    top_k: int = 5
    similarity_threshold: float = 0.0
    hybrid_search: bool = False
    hybrid_alpha: float = 0.3
    rerank_enabled: bool = False
    rerank_top_k: int = 5
    temperature: float = 0.7
    system_prompt: str | None = None


class CompareRequest(BaseModel):
    """效果对比请求体（两组配置并列运行）。"""

    query: str
    config_a: CompareConfig
    config_b: CompareConfig
