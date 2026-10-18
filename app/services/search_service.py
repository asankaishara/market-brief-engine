from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict, Any
from app.models.article import ChunkModel, ArticleModel
from app.services.embedder import EmbeddingService
import logging

class SearchService:
    """Service to execute semantic vector similarity search against stored article chunks."""

    def __init__(self, db: Session):
        self.db = db
        self.embedder = EmbeddingService()

    async def semantic_search(self, query: str, ticker: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Generates an embedding for the query and searches the database
        for the most relevant article chunks using cosine distance.
        """
        # 1. Generate query embedding via Ollama
        query_embedding = await self.embedder.get_embedding(query)
        logging.warning("Embeddings generated for query: %s", query_embedding)
        if not query_embedding:
            return []

        # 2. Build base query with vector cosine distance operator (<=>)
        stmt = (
            select(ChunkModel, ArticleModel)
            .join(ArticleModel, ChunkModel.article_id == ArticleModel.id)
        )

        # Optional ticker filtering
        if ticker:
            stmt = stmt.where(ArticleModel.ticker == ticker.upper())

        # Order by vector similarity (cosine distance ascending) and limit results
        stmt = stmt.order_by(ChunkModel.embedding.cosine_distance(query_embedding)).limit(top_k)

        results = self.db.execute(stmt).all()

        # 3. Format output
        search_results = []
        for chunk, article in results:
            search_results.append({
                "chunk_id": str(chunk.id),
                "article_title": article.title,
                "ticker": article.ticker,
                "source": article.source,
                "published_at": article.published_at.isoformat(),
                "url": article.url,
                "chunk_text": chunk.text
            })

        return search_results