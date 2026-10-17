from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.services.ingestion import IngestionPipeline

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

class IngestRequest(BaseModel):
    ticker: str

@router.post("/")
async def ingest_market_news(payload: IngestRequest, db: Session = Depends(get_db)):
    """Triggers news fetching, chunking, embedding, and storage for a given stock ticker."""
    try:
        pipeline = IngestionPipeline(db)
        count = await pipeline.ingest_ticker_news(payload.ticker)
        return {
            "status": "success",
            "ticker": payload.ticker.upper(),
            "new_articles_ingested": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))