import boto3
import json
from typing import List, Dict, Any
from app.core.config import settings

class LLMService:
    """Service to interact with foundational models via AWS Bedrock."""

    def __init__(self):
        # Initialize the Bedrock Runtime client using settings from config.py
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    def generate_market_brief(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Synthesizes a market brief by passing the user query and retrieved context chunks
        to the AWS Bedrock LLM.
        """
        # 1. Format context chunks into a clean reference string
        context_text = "\n\n".join([
            f"Source: {chunk['source']} | Ticker: {chunk['ticker']} | Date: {chunk['published_at']}\nContent: {chunk['chunk_text']}"
            for chunk in context_chunks
        ])

        # 2. Construct prompt engineering instructions for RAG
        prompt = f"""You are an expert Financial Analyst AI assistant. Use the provided context extracts from recent financial news to answer the user's query accurately and concisely. 
If the answer cannot be found in the context, state clearly that there is insufficient data in the ingested news.

Context Articles:
{context_text}

User Query: {query}

Financial Market Briefing:"""

        # 3. Format payload for Anthropic Claude models on Bedrock
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        }

        try:
            # 4. Invoke AWS Bedrock
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(native_request)
            )

            # 5. Parse response body
            response_body = json.loads(response.get("body").read())
            return response_body.get("content", [{}])[0].get("text", "No response generated.")

        except Exception as e:
            return f"Error communicating with AWS Bedrock: {str(e)}"