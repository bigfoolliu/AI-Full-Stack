from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, func

from app.core.database import Base


class KnowledgeBaseSetting(Base):
    """知识库可配置参数：检索、Prompt、模型、Hybrid Search、Rerank。"""

    __tablename__ = "knowledge_base_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    knowledge_base_id = Column(Integer, nullable=False, unique=True, index=True)
    top_k = Column(Integer, nullable=False, default=5)
    similarity_threshold = Column(Float, nullable=False, default=0.0)
    system_prompt = Column(Text, nullable=True)
    temperature = Column(Float, nullable=False, default=0.7)
    max_tokens = Column(Integer, nullable=False, default=2048)
    model_name = Column(String(64), nullable=True)
    hybrid_search = Column(Boolean, nullable=False, default=False)
    hybrid_alpha = Column(Float, nullable=False, default=0.3)
    rerank_enabled = Column(Boolean, nullable=False, default=False)
    rerank_top_k = Column(Integer, nullable=False, default=5)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
