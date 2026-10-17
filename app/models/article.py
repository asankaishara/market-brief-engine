import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.session import Base

class ArticleModel(Base):
    """ORM model for ingested market articles."""
    __tablename__ = "articles"

    id = Column(UUID( as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(Text, unique=True, nullable=False)
    title = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=False)
    ticker = Column(String(10), nullable=False, index=True)
    content_hash = Column(String(64), nullable=False)
    fetched_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship to chunk
    chunks = relationship("ChunkModel", back_populates="article", cascade="all, delete-orphan")


class ChunkModel(Base):
    """ORM model to hold chunks and their 768-dim vector embeddings related to article"""
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)

    # Relationship back to article
    article = relationship("ArticleModel", back_populates="chunks")