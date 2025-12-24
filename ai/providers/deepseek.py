import requests
import json
from django.conf import settings
from .base import BaseAIProvider

class DeepSeekProvider(BaseAIProvider):
    def generate_answer(self, question: str, context: str) -> str:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": settings.SITE_URL,
                "X-Title": settings.SITE_NAME,
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1-0528:free",
                "messages": [
                    {"role": "system", "content": "You are an AI assistant for a knowledge hub."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
                ],
                "provider": {"sort": "throughput"}
            })
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def generate_embedding(self, text: str) -> list[float]:
        # Placeholder until DeepSeek releases embedding API
        return [0.01] * 768
