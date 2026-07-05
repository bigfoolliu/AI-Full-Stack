from app.models.user import User
from app.models.knowledge_base import KnowledgeBase
from app.models.document import Document

__all__ = ["Base", "User", "KnowledgeBase", "Document"]

from app.core.database import Base
