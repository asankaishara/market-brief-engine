-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Articles table (Metadata and Content Ingestion)
CREATE TABLE IF NOT EXISTS articles (
                                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    content_hash CHAR(64) NOT NULL,
    fetched_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );

-- Chunks table (768-dim embeddings matching nomic-embed-text)
CREATE TABLE IF NOT EXISTS chunks (
                                      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    text TEXT NOT NULL,
    embedding vector(768) NOT NULL
    );

-- Index for rapid ticker + recency filtering
CREATE INDEX IF NOT EXISTS idx_articles_ticker_pub ON articles(ticker, published_at DESC);