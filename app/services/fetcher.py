import hashlib
import httpx
from datetime import datetime
from typing import List, Dict, Any

class DataFetcherService:
    """Service to fetch and parse market news/articles for ingestion."""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    async def fetch_rss_or_api(self, ticker: str) -> List[Dict[str, Any]]:
        """
        Simulates fetching articles for a given stock ticker.
        In production, this would connect to an external financial news API or RSS feed.
        """
        # For development and demonstration, we provide a structured mock payload
        mock_articles = [
            {
                "url": f"https://example.com/news/{ticker.lower()}-q4-earnings",
                "title": f"{ticker} Reports Strong Q4 Earnings Growth",
                "source": "Financial Wire",
                "published_at": datetime.utcnow().isoformat(),
                "ticker": ticker.upper(),
                "content": f"{ticker} announced robust financial performance for the fourth quarter, driven by strong cloud adoption and expanding operating margins. Analysts expressed optimism regarding upcoming product launches."
            },
            {
                "url": f"https://example.com/news/{ticker.lower()}-market-expansion",
                "title": f"{ticker} Expands Global Footprint with New Strategic Partnership",
                "source": "Global Markets Today",
                "published_at": datetime.utcnow().isoformat(),
                "ticker": ticker.upper(),
                "content": f"In a strategic move to capture emerging markets, {ticker} has partnered with key regional distributors. Leadership highlights long-term growth potential and supply chain resilience."
            }
        ]
        return mock_articles

    @staticmethod
    def generate_content_hash(content: str) -> str:
        """Generates a SHA-256 hash of the content to prevent duplicate storage."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    async def close(self):
        await self.client.aclose()