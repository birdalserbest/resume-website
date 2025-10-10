# OpenAI implementation using the official SDK.
from typing import List, Dict
from openai import OpenAI
from .base import ChatProvider
from settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIProvider(ChatProvider):
    def __init__(self):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY missing. Set it in backend/.env")
        # The new SDK uses an explicit client object
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def generate(self, messages: List[Dict[str, str]], context: str = "") -> str:
        # We prepend a system message to constrain behavior to your resume domain.
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
