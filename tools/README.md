# Tools

Skrypty pomocnicze do warstwy `raw/` (nie modyfikują wiki bez ingest przez agenta).

## extract_pdf_text.py

Ekstrakcja tekstu z PDF do pliku `.txt` obok źródła (ułatwia ingest dużych paperów).

```bash
make install
make extract-pdf FILE=raw/papers/example.pdf
# lub
.venv/bin/python tools/extract_pdf_text.py raw/papers/example.pdf
```

Wymaga: `make install` (pymupdf).

## LLM layer (`tools/llm/`)

Cienka abstrakcja nad providerami — logika woła `get_llm_client().complete(...)`, nie SDK OpenAI/Vertex bezpośrednio.

| Provider | Env |
|----------|-----|
| **Vertex (domyślny)** | `LLM_PROVIDER=vertex` |
| **OpenAI** | `LLM_PROVIDER=openai` |

Skopiuj [`.env.example`](../.env.example) → `.env` i uzupełnij (`.env` jest w `.gitignore`).

### Zmienne środowiskowe

| Zmienna | Wymagane | Domyślnie | Opis |
|---------|----------|-----------|------|
| `LLM_PROVIDER` | nie | `vertex` | `vertex` lub `openai` |
| `VERTEX_PROJECT` | przy vertex | — | np. `conifer-vision01` |
| `VERTEX_LOCATION` | nie | `global` | region Model Garden (`gemini-3.5-flash` wymaga `global`) |
| `LLM_MODEL` | nie | `gemini-3.5-flash` / `gpt-4o-mini` | model zależny od providera |
| `OPENAI_API_KEY` | przy openai | — | klucz API OpenAI |

### Apple Silicon (M1/M2/M3) — błąd `incompatible architecture`

Jeśli `make llm-smoke` kończy się na `pydantic_core` / `have 'arm64', need 'x86_64'` (lub odwrotnie):

1. Terminal **nie** może działać pod Rosetta (Finder → Applications → Terminal → Get Info → odznacz „Open using Rosetta”).
2. Conda `(base)` czasem miesza architekturę — przed `make` spróbuj `conda deactivate`.
3. Odtwórz venv natywnie:

```bash
make venv-recreate
```

Sprawdzenie:

```bash
.venv/bin/python -c "import platform; print(platform.machine())"
# Oczekiwane: arm64
```

### Vertex (GCP)

1. Włącz API: `aiplatform.googleapis.com` w projekcie.
2. Lokalnie: `gcloud auth application-default login`
3. Rola konta: `roles/aiplatform.user` na projekcie Vertex.
4. Dla `gemini-3.5-flash` ustaw `VERTEX_LOCATION=global` (regionalne endpointy EU/US zwracają 404).

```bash
export LLM_PROVIDER=vertex
export VERTEX_PROJECT=conifer-vision01
export VERTEX_LOCATION=global
export LLM_MODEL=gemini-3.5-flash
make llm-smoke
```

### OpenAI (fallback)

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
export LLM_MODEL=gpt-4o-mini
make llm-smoke
```

### Użycie w kodzie

```python
from tools.llm import ChatMessage, get_llm_client

client = get_llm_client()
response = client.complete([
    ChatMessage("system", "You are a forestry research assistant. English only."),
    ChatMessage("user", "Summarize this paper in three bullets."),
])
print(response.text)
```
