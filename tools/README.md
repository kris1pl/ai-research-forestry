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

## ingest_paper.py

Próbny ingest paperu do `conifervision/sources/` przez skonfigurowany LLM (domyślnie Vertex `gemini-3.5-flash`). Ekstrahuje tekst PDF, wysyła kontekst wiki + paper, zapisuje stronę `source`.

```bash
make extract-pdf FILE=raw/papers/2405.15613v2.pdf   # opcjonalnie — ingest robi to sam
make ingest-paper FILE=raw/papers/2405.15613v2.pdf WRITE=1
```

Bez `WRITE=1` wypisuje markdown na stdout (podgląd). Z `WRITE=1` skrypt **automatycznie** aktualizuje `log.md`, `index.md` oraz powiązane strony `methods/` / `concepts/` (drugi call LLM → `tools/wiki_update.py`). Idempotentne — ponowny ingest nie duplikuje wpisów.

```bash
# tylko odśwież wiki z istniejącej strony source (bez ponownego LLM na PDF)
make ingest-paper FILE=raw/papers/2405.15613v2.pdf WRITE=1 WIKI_ONLY=conifervision/sources/vo-2024-automatic-data-curation.md
```

## OKF (Open Knowledge Format v0.2)

Vault `conifervision/` jest bundle OKF zgodnym ze [specyfikacją Google](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf). Kontrakt domenowy: `AGENTS.md`, reguła Cursor: `.cursor/rules/100-okf-standards.mdc`.

```bash
make okf-lint          # walidacja frontmatter, indexów, log.md
make okf-lint FIX=1    # auto-fix: status, generated, description, typy Title Case
```

Lint sprawdza m.in. `okf_version` w root `index.md`, brak frontmatter w `log.md` i `*/index.md`, wymagane `type` + zalecane `generated`/`description` na conceptach.
