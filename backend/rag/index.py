# Lightweight RAG loader: in prod we just load JSON with precomputed vectors.
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional
import json
import numpy as np


@dataclass
class Chunk:
    text: str
    emb: np.ndarray  # l2-normalized


class ResumeRAG:
    def __init__(self, json_path: Path):
        self.json_path = json_path
        self.chunks: List[Chunk] = []

    def build(self) -> int:
        data = json.loads(Path(self.json_path).read_text(encoding="utf-8"))
        self.chunks = [
            Chunk(c["text"], np.asarray(c["emb"], dtype=np.float32))
            for c in data["chunks"]
        ]
        return len(self.chunks)

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        if not self.chunks or not query.strip():
            return []
        # NOTE: We need a query embedding. In prod (no model), use a fallback:
        # simple bag-of-words cosine using chunk texts. It’s weaker but zero-deps.
        # If you want full quality, call OpenAI embeddings instead (see below).
        q_vec = _bow_vec(query, [c.text for c in self.chunks])
        if q_vec is None:
            return []
        # build matrix over same vocab space
        M = np.stack([_bow_vec(c.text, None, vocab=_GLOBAL_VOCAB) for c in self.chunks])
        qn = q_vec / (np.linalg.norm(q_vec) + 1e-8)
        Mn = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-8)
        scores = (Mn @ qn).astype(np.float32)
        idx = np.argsort(-scores)[:k]
        return [(self.chunks[i].text, float(scores[i])) for i in idx]


# --- very small BoW helper so we don’t ship heavy ML to prod ---
_GLOBAL_VOCAB = {}  # filled lazily


def _make_vocab(texts: List[str]):
    vocab = {}
    for t in texts:
        for w in t.lower().split():
            if w not in vocab:
                vocab[w] = len(vocab)
    return vocab


def _bow_vec(text: str, corpus: Optional[List[str]], vocab=None):
    global _GLOBAL_VOCAB
    if vocab is None:
        if not _GLOBAL_VOCAB:
            if not corpus:
                return None
            _GLOBAL_VOCAB = _make_vocab(corpus)
        vocab = _GLOBAL_VOCAB
    v = np.zeros(len(vocab), dtype=np.float32)
    for w in text.lower().split():
        idx = vocab.get(w)
        if idx is not None:
            v[idx] += 1.0
    return v
