"""
CLI: python scripts/extract_resume.py

- Reads backend/data/resume.pdf
- Extracts text with PyMuPDF (fitz)
- Normalizes whitespace / hyphenation
- Writes:
  - backend/data/resume.raw.txt   (verbatim-ish)
  - backend/data/resume.clean.txt (normalized)
"""

import re
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "data" / "resume.pdf"
RAW_OUT = ROOT / "data" / "resume.raw.txt"
CLEAN_OUT = ROOT / "data" / "resume.clean.txt"


def extract_pdf_text(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    chunks = []
    for page in doc:
        # 'get_text("text")' gives a readable linear text
        chunks.append(page.get_text("text"))
    doc.close()
    return "\n".join(chunks)


def normalize_text(s: str) -> str:
    # Collapse excessive whitespace
    s = re.sub(r"[ \t]+\n", "\n", s)  # strip trailing spaces
    s = re.sub(r"\n{3,}", "\n\n", s)  # max 2 newlines in a row
    s = re.sub(r"[ \t]{2,}", " ", s)  # collapse runs of spaces

    # Undo common PDF hyphenation: line-break splits like "experi-\nence"
    s = re.sub(r"(\w)-\n(\w)", r"\1\2", s)  # join hyphen-broken words

    # Merge soft line wraps where a line ends mid-sentence (heuristic)
    s = re.sub(r"(?<![.\!\?:])\n(?!\n)", " ", s)

    # Trim
    return s.strip()


def main():
    if not PDF_PATH.exists():
        raise SystemExit(f"Missing PDF at {PDF_PATH}. Put your file there.")

    raw = extract_pdf_text(PDF_PATH)
    RAW_OUT.write_text(raw, encoding="utf-8")

    clean = normalize_text(raw)
    CLEAN_OUT.write_text(clean, encoding="utf-8")

    print(f"✅ Wrote {RAW_OUT.relative_to(ROOT)} ({len(raw):,} chars)")
    print(f"✅ Wrote {CLEAN_OUT.relative_to(ROOT)} ({len(clean):,} chars)")
    print("Next: we’ll chunk & embed resume.clean.txt for RAG.")


if __name__ == "__main__":
    main()
