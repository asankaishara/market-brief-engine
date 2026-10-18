from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.db.session import get_db
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Semantic Search"])

class SearchRequest(BaseModel):
    query: str
    ticker: Optional[str] = None
    top_k: Optional[int] = 3

@router.post("/")
async def search_market_news(payload: SearchRequest, db: Session = Depends(get_db)):
    """Executes a semantic vector search across ingested financial news chunks."""
    try:
        search_service = SearchService(db)
        results = await search_service.semantic_search(
            query=payload.query,
            ticker=payload.ticker,
            top_k=payload.top_k
        )
        return {
            "query": payload.query,
            "filter_ticker": payload.ticker.upper() if payload.ticker else None,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))