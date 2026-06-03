#!/usr/bin/env python3
"""Extract plain text from a PDF into a sibling .txt file."""

from __future__ import annotations

import sys
from pathlib import Path


def extract(pdf_path: Path) -> Path:
    try:
        import fitz  # pymupdf
    except ImportError as e:
        raise SystemExit("Install dependencies: pip install -r requirements.txt") from e

    if not pdf_path.is_file():
        raise SystemExit(f"Not a file: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise SystemExit(f"Expected .pdf: {pdf_path}")

    out_path = pdf_path.with_suffix(".txt")
    doc = fitz.open(pdf_path)
    parts: list[str] = []
    for page in doc:
        parts.append(page.get_text())
    doc.close()

    text = "\n\n".join(parts).strip()
    out_path.write_text(text + "\n", encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> None:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        raise SystemExit(f"Usage: {Path(__file__).name} <path-to.pdf>")
    out = extract(Path(args[0]).resolve())
    print(out)


if __name__ == "__main__":
    main()
