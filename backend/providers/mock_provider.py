# Simple mock provider so backend won't crash if no API keys are set.
# Returns a placeholder response for development.

from typing import Iterable, List, Dict
import time
from .base import ChatProvider


class MockProvider(ChatProvider):
    def generate(self, messages: List[Dict[str, str]], context: str = "") -> str:
        # Extract the latest user message for context
        last = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), "..."
        )
        # You can customize this to simulate different responses
        return f"I am the Mock provider. You said: '{last}'. Real model replies will appear here later."

    def stream(self, messages: list[dict], context: str = "") -> Iterable[str]:
        last = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), "…"
        )
        txt = f"I am the Mock provider. You said: '{last}'. Real streaming later."
        for ch in txt:
            time.sleep(0.01)  # slow drip to simulate stream
            yield ch
