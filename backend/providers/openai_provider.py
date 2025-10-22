from typing import List, Dict, Iterable
from openai import OpenAI
from .base import ChatProvider
from settings import OPENAI_API_KEY, OPENAI_MODEL


# simple flag: treat GPT-5 models as Responses-only
def _uses_responses(model: str) -> bool:
    return model.startswith("gpt-5")


class OpenAIProvider(ChatProvider):
    def __init__(self):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY missing. Set it in backend/.env")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def _system_msg(self, context: str) -> Dict[str, str]:
        # single place to keep the system prompt
        return {
            "role": "system",
            "content": (
                """ Have a natural conversation about Birdal using only information from the provided resume snippets.
                    Speak conversationally and just answer what the user is asking. Birdal is a male."""
                + (f"\nContext:\n{context}" if context else "")
            ),
        }

    def generate(self, messages: List[Dict[str, str]], context: str = "") -> str:
        sys = self._system_msg(context)

        if _uses_responses(self.model):
            # Responses API path (required for GPT-5)
            # input accepts a messages-style array
            resp = self.client.responses.create(
                model=self.model,
                input=[sys] + messages,
            )
            # prefer friendly accessor if present
            text = getattr(resp, "output_text", None)
            if not text:
                # fallback parse (SDK structures can vary slightly)
                try:
                    parts = []
                    for item in getattr(resp, "output", []) or []:
                        for c in getattr(item, "content", []) or []:
                            # text may be at c.text.value or c.output_text
                            v = getattr(getattr(c, "text", None), "value", None)
                            if v:
                                parts.append(v)
                    text = "".join(parts)
                except Exception:
                    text = ""
            return (text or "").strip()

        # Classic chat.completions path (gpt-4.1 / gpt-4o, etc.)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[sys] + messages,
            temperature=0.3,
        )
        return (resp.choices[0].message.content or "").strip()

    # keep stream() as-is if you want; GPT-5 streaming would need Responses streaming
    def stream(
        self, messages: List[Dict[str, str]], context: str = ""
    ) -> Iterable[str]:
        sys = self._system_msg(context)

        if _uses_responses(self.model):
            # simple non-streaming fallback for GPT-5 to keep interface stable
            yield self.generate(messages, context)
            return

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[sys] + messages,
            temperature=0.3,
            stream=True,
        )
        for ev in resp:
            piece = ev.choices[0].delta.content or ""
            if piece:
                yield piece
