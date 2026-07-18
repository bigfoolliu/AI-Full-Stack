from pydantic import BaseModel


class KnowledgeBaseItem(BaseModel):
    id: int
    name: str
    description: str
    document_count: int
    created_at: str


class CreateKnowledgeBaseRequest(BaseModel):
    name: str
    description: str


class SearchFilter(BaseModel):
    filename: str | None = None
    status: str | None = None


class ChatRequest(BaseModel):
    query: str
    history: list[dict] | None = None
    top_k: int = 5
    filter: SearchFilter | None = None


class ChatSessionMessagePayload(BaseModel):
    role: str
    content: str


class SaveChatSessionRequest(BaseModel):
    session_id: int | None = None
    messages: list[ChatSessionMessagePayload]


class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filter: SearchFilter | None = None


class KnowledgeBaseSettingItem(BaseModel):
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
    session_id: int
    message_id: int
    feedback: str
    comment: str | None = None


class CompareConfig(BaseModel):
    top_k: int = 5
    similarity_threshold: float = 0.0
    hybrid_search: bool = False
    hybrid_alpha: float = 0.3
    rerank_enabled: bool = False
    rerank_top_k: int = 5
    temperature: float = 0.7
    system_prompt: str | None = None


class CompareRequest(BaseModel):
    query: str
    config_a: CompareConfig
    config_b: CompareConfig
