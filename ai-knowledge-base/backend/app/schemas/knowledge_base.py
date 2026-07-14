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


class ChatRequest(BaseModel):
    query: str
    history: list[dict] | None = None
    top_k: int = 5


class ChatSessionMessagePayload(BaseModel):
    role: str
    content: str


class SaveChatSessionRequest(BaseModel):
    session_id: int | None = None
    messages: list[ChatSessionMessagePayload]


class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int = 5
