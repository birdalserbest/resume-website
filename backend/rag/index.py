# Minimal, in-memory RAG for the resume site.
# - Load cleaned resume text (data/resume.clean.txt)
# - Chunk into digestible pieces (~600 chars)
# - Embed chunks with Sentence-Transformers (MiniLM)
# - Cosine search (via dot on L2-normalized vectors)
#
# Notes:
# - First run downloads the ST model (~90MB).
# - Everything is in-memory; fast for a single-user site.
# - Keep chunk size small enough to fit in prompts later.
# --------------------------------------------

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class Chunk:
    """Holds text and its vector embedding."""

    text: str
    emb: np.ndarray


def _simple_chunks(text: str, max_chars: int = 600) -> List[str]:
    """Split resume text into short, logical chunks."""
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    chunks: List[str] = []
    for b in blocks:
        if len(b) <= max_chars:
            chunks.append(b)
        else:
            i = 0
            while i < len(b):
                j = min(i + max_chars, len(b))
                pivot = b.rfind(" ", i, j)  # break near space
                cut = pivot if pivot != -1 and pivot > i + 200 else j
                chunks.append(b[i:cut].strip())
                i = cut
    return chunks


class ResumeRAG:
    """Handles embedding + retrieval over resume text."""

    def __init__(self, path: Path, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.path = path
        self.model = SentenceTransformer(model_name)
        self.chunks: List[Chunk] = []

    def build(self) -> int:
        """Load resume text, chunk it, embed each piece."""
        text = self.path.read_text(encoding="utf-8")
        parts = _simple_chunks(text)
        embs = self.model.encode(parts, normalize_embeddings=True)
        self.chunks = [
            Chunk(p, np.asarray(e, dtype=np.float32)) for p, e in zip(parts, embs)
        ]
        return len(self.chunks)

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """Return top-k similar chunks for a query."""
        query = (query or "").strip()
        if not query or not self.chunks:
            return []
        q = self.model.encode([query], normalize_embeddings=True)[0].astype(np.float32)
        scores = np.dot(np.stack([c.emb for c in self.chunks]), q)
        idx = np.argsort(-scores)[:k]
        return [(self.chunks[i].text, float(scores[i])) for i in idx]
