import httpx
from typing import List
from app.core.config import settings

class EmbeddingService:
    """Service to chunk article text and generate vector embeddings via local Ollama."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model_name = settings.EMBEDDING_MODEL

    def chunk_text(self, text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
        """Splits raw article text into overlapping character chunks."""
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunks.append(text[start:end])
            if end == text_length:
                break
            start += chunk_size - overlap

        return chunks

    async def get_embedding(self, text: str) -> List[float]:
        """Calls local Ollama API to generate a 768-dimensional vector embedding."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model_name,
                    "prompt": text
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", [])