# Tools

Skrypty pomocnicze do warstwy `raw/` (nie modyfikują wiki bez ingest przez agenta).

## extract_pdf_text.py

Ekstrakcja tekstu z PDF do pliku `.txt` obok źródła (ułatwia ingest dużych paperów).

```bash
make extract-pdf FILE=raw/papers/example.pdf
# lub
.venv/bin/python tools/extract_pdf_text.py raw/papers/example.pdf
```

Wymaga: `make install` (pymupdf).
