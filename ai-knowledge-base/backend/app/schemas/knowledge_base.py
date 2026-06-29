from pydantic import BaseModel


class KnowledgeBaseItem(BaseModel):
    id: int
    name: str
    description: str
    document_count: int
    created_at: str
