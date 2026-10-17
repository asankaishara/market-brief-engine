from sqlalchemy.orm import Session
from datetime import datetime
from app.models.article import ArticleModel, ChunkModel
from app.services.fetcher import DataFetcherService
from app.services.embedder import EmbeddingService

class IngestionPipeline:
    """Orchestrates fetching, deduplication, chunking, embedding, and storage."""

    def __init__(self, db: Session):
        self.db = db
        self.fetcher = DataFetcherService()
        self.embedder = EmbeddingService()

    async def ingest_ticker_news(self, ticker: str) -> int:
        """
        Fetches news for a ticker, checks for duplicates, chunks text,
        generates embeddings via Ollama, and stores them in PostgreSQL.
        """
        articles_data = await self.fetcher.fetch_rss_or_api(ticker)
        new_articles_count = 0

        for item in articles_data:
            content = item["content"]
            content_hash = self.fetcher.generate_content_hash(content)
            url = item["url"]

            # Check if article already exists by URL or content hash
            existing = self.db.query(ArticleModel).filter(
                (ArticleModel.url == url) | (ArticleModel.content_hash == content_hash)
            ).first()

            if existing:
                continue  # Skip duplicates

            # Parse published date safely
            try:
                pub_date = datetime.fromisoformat(item["published_at"])
            except ValueError:
                pub_date = datetime.utcnow()

            # Create Article record
            article = ArticleModel(
                url=url,
                title=item["title"],
                source=item["source"],
                published_at=pub_date,
                ticker=item["ticker"],
                content_hash=content_hash
            )
            self.db.add(article)
            self.db.flush()  # Flush to generate article.id

            # Chunk text and generate vector embeddings
            chunks = self.embedder.chunk_text(content)
            for idx, chunk_text in enumerate(chunks):
                embedding = await self.embedder.get_embedding(chunk_text)

                chunk = ChunkModel(
                    article_id=article.id,
                    chunk_index=idx,
                    text=chunk_text,
                    embedding=embedding
                )
                self.db.add(chunk)

            new_articles_count += 1

        self.db.commit()
        return new_articles_count