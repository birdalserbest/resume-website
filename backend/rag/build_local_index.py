# Run locally to build a lightweight search index JSON.
# Writes: backend/data/rag_index.json (chunks + l2-normalized vectors)

from pathlib import Path
import json
from sentence_transformers import SentenceTransformer

SRC = Path(__file__).resolve().parent.parent / "data" / "resume.clean.txt"
OUT = Path(__file__).resolve().parent.parent / "data" / "rag_index.json"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def simple_chunks(text: str, max_chars: int = 600):
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    out = []
    for b in blocks:
        if len(b) <= max_chars:
            out.append(b)
        else:
            i = 0
            while i < len(b):
                j = min(i + max_chars, len(b))
                pivot = b.rfind(" ", i, j)
                cut = pivot if pivot != -1 and pivot > i + 200 else j
                out.append(b[i:cut].strip())
                i = cut
    return out


def main():
    txt = SRC.read_text(encoding="utf-8")
    parts = simple_chunks(txt)
    model = SentenceTransformer(MODEL)
    embs = model.encode(parts, normalize_embeddings=True)
    # save as plain lists so JSON is portable
    data = {
        "model": MODEL,
        "dim": int(embs.shape[1]),
        "chunks": [{"text": t, "emb": e.tolist()} for t, e in zip(parts, embs)],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data), encoding="utf-8")
    print(f"wrote {len(parts)} chunks → {OUT}")


if __name__ == "__main__":
    main()
