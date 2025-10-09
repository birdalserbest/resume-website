# Groq implementation; very fast hosted OSS models.
from typing import List, Dict
from groq import Groq
from .base import ChatProvider
from settings import GROQ_API_KEY, GROQ_MODEL


class GroqProvider(ChatProvider):
    def __init__(self):
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY missing. Set it in backend/.env")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def generate(self, messages: List[Dict[str, str]], context: str = "") -> str:
        sys = {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers ONLY about the candidate's "
                "resume and projects. Be concise and specific."
                + (f"\nContext:\n{context}" if context else "")
            ),
        }

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[sys] + messages,
            temperature=0.3,
        )
        return (resp.choices[0].message.content or "").strip()
