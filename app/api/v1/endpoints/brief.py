from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.search_service import SearchService
from app.services.llm import LLMService
from app.models.brief import MarketBrief, SourceMetadata
import logging

router = APIRouter(prefix="/market-brief", tags=["Market Brief"])
logger = logging.getLogger(__name__)

@router.get("/{ticker}", response_model=MarketBrief)
async def get_market_brief(ticker: str, db: Session = Depends(get_db)):

    logger.info("Getting market brief for ticker [%s]", ticker)

    """
    RAG Endpoint: Retrieves news for a ticker from pgvector and synthesizes
    a structured market brief via AWS Bedrock.
    """
    search_service = SearchService(db)
    llm_service = LLMService()

    # 1. Retrieve top relevant chunks for this ticker
    chunks = await search_service.semantic_search(
        query=f"latest financial performance, outlook, and risk factors for {ticker}",
        ticker=ticker,
        top_k=4
    )

    logger.info("Found existing chunks from DB %d", len(chunks))

    # If no news found
    if not chunks:
        logger.info("No news found for %s", ticker)
        return MarketBrief(
            ticker=ticker.upper(),
            bias="no_view",
            confidence="low",
            drivers=["No ingested news found for this ticker."],
            risks=[],
            sources=[],
            rules_applied=["No news available -> return no_view"]
        )

    # 2. Extract unique sources for attribution
    seen_urls = set()
    sources = []
    for c in chunks:
        url = c.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            sources.append(SourceMetadata(
                title=c.get("article_title", "Unknown"),
                url=url,
                published_at=c.get("published_at", "")
            ))

    # 3. Call LLM for structured brief
    llm_output = llm_service.generate_market_brief(ticker=ticker, context_chunks=chunks)

    return MarketBrief(
        ticker=ticker.upper(),
        bias=llm_output.get("bias", "neutral"),
        confidence=llm_output.get("confidence", "low"),
        drivers=llm_output.get("drivers", []),
        risks=llm_output.get("risks", []),
        sources=sources,
        rules_applied=[]
    )