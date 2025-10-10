# Defines the minimal interface our chat providers implement.
from typing import List, Dict


class ChatProvider:
    def generate(self, messages: List[Dict[str, str]], context: str = "") -> str:
        """Return a single assistant reply string given prior messages.
        'messages' is an array like: [{"role":"user","content":"..."}, ...]
        'context' can include retrieved resume/project info (we'll add later)."""
        raise NotImplementedError
