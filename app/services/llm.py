import boto3
import json
from typing import List, Dict, Any
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    def generate_market_brief(self, ticker: str, context_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesizes structured market brief JSON from retrieved context chunks."""
        context_text = "\n\n".join([
            f"Title: {chunk.get('article_title', '')} | Source: {chunk.get('source', '')} | URL: {chunk.get('url', '')}\nDate: {chunk.get('published_at', '')}\nText: {chunk.get('chunk_text', '')}"
            for chunk in context_chunks
        ])

        system_prompt = (
            "You are a financial analysis engine. Return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "bias": "bullish" | "bearish" | "neutral" | "no_view",\n'
            '  "confidence": "low" | "medium" | "high",\n'
            '  "drivers": ["short driver citing a source title"],\n'
            '  "risks": ["short risk factor"]\n'
            "}\n"
            "Ground your analysis strictly in the provided articles. Do not give trading advice, order types, or target prices. "
            "Return raw JSON only, no markdown formatting, no backticks."
        )

        user_content = f"Articles for {ticker.upper()}:\n{context_text}\n\nGenerate market brief JSON:"

        try:
            response = self.client.converse(
                modelId=self.model_id,
                system=[{"text": system_prompt}],
                messages=[{"role": "user", "content": [{"text": user_content}]}],
                inferenceConfig={"maxTokens": 1000, "temperature": 0.1}
            )
            raw_text = response["output"]["message"]["content"][0]["text"].strip()

            # Clean possible markdown wrap (```json ... ```)
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]

            return json.loads(raw_text.strip())
        except Exception as e:
            return {
                "bias": "no_view",
                "confidence": "low",
                "drivers": [f"Error during LLM inference: {str(e)}"],
                "risks": []
            }