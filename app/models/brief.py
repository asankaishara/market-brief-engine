from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any
from datetime import datetime

class SourceMetadata(BaseModel):
    title: str
    url: str
    published_at: str

class MarketBrief(BaseModel):
    ticker: str
    as_of: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    bias: Literal["bullish", "bearish", "neutral", "no_view"]
    confidence: Literal["low", "medium", "high"]
    drivers: List[str] = Field(description="Key drivers, each citing a retrieved source")
    risks: List[str] = Field(description="Key identified risks")
    sources: List[SourceMetadata]
    rules_applied: List[str] = Field(default_factory=list)
    prompt_version: str = "v1.0"
    disclaimer: str = (
        "This is a research aid, not financial advice. It never trades. "
        "It never gives orders, entry prices, or position sizes."
    )