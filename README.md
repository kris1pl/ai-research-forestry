# Forestry Research LLM Wiki

Team knowledge base for forest area analysis methodology — [LLM Wiki](llm_wiki.md) pattern (Andrej Karpathy): the agent compiles sources into a persistent Markdown wiki instead of rediscovering them on every question.

**Vault language: English.** All pages in `conifervision/` and agent-written updates follow [`AGENTS.md`](AGENTS.md).

**TODO:** Integration with the separate production code repository is not set up yet — see [`conifervision/project/code-repo-integration.md`](conifervision/project/code-repo-integration.md).

## Struktura

| Katalog | Opis |
|---------|------|
| [`raw/`](raw/) | Niezmienne źródła: PDF, clipy web, obrazy (`assets/`) |
| [`conifervision/`](conifervision/) | **Obsidian** vault (English) — published via Quartz |
| [`site/`](site/) | Quartz 4 — build statycznej strony |
| [`tools/`](tools/) | Python: ekstrakcja tekstu z PDF |
| [`AGENTS.md`](AGENTS.md) | Schema dla agenta: ingest / query / lint |

## Szybki start

### 1. Obsidian (lokalnie)

1. Zainstaluj [Obsidian](https://obsidian.md/).
2. **Open folder as vault** → wybierz katalog `conifervision/` w tym repozytorium.
3. Opcjonalnie: [Web Clipper](https://obsidian.md/clipper) → zapisuj artykuły do `raw/web/`.
4. Opcjonalnie: plugin **Dataview** — tabele po polach YAML w frontmatter.

Ustawienia vault (już w repo): linki **shortest**, załączniki w `../raw/assets`. Sync zespołu: **Git** (branch + PR), nie Obsidian Sync.

### 2. Python (narzędzia ingest)

```bash
make install
make extract-pdf FILE=raw/papers/przyklad.pdf   # tworzy przyklad.txt
```

### 3. Podgląd strony wiki (Quartz)

**CI i zalecany lokalny build:** Node.js **≥ 22** (lub Docker poniżej).

```bash
make serve-wiki          # Node 22+ lokalnie
# http://localhost:8080
```

Jeśli lokalny Node jest za stary (np. 20.11), użyj Dockera:

```bash
make build-wiki-docker   # tylko build → site/public/
make serve-wiki-docker   # podgląd na http://localhost:8080
```

Tylko build (lokalnie):

```bash
make build-wiki
```

Treść builda: katalog `conifervision/` (w CI kopiowany do `site/content`). Katalog `raw/` **nie** trafia na stronę publiczną.

Jeśli widzisz **RSS/XML zamiast strony** — deploy zbudował się bez treści (zły folder vault). Po poprawce zrób push i **Re-run** workflow.

### 4. Praca z agentem

In Cursor (or another agent), point at the repo and read [`AGENTS.md`](AGENTS.md) (English wiki only).

Example prompts:

- *“Ingest `raw/papers/foo.pdf` — update the wiki per AGENTS.md (English), including replication pseudocode if the method is clear enough.”*
- *“Query: what does the wiki say about merging local maxima with CHM detections?”*
- *“Lint the wiki against `conifervision/project/pipeline-overview.md`.”*

## Publikacja (GitHub Pages)

### Jednorazowa konfiguracja (obowiązkowa)

Token Actions **nie może** utworzyć strony Pages — musisz włączyć ją raz z komputera (konto admin repo):

```bash
# Zainstaluj: https://cli.github.com/
gh auth login
chmod +x scripts/enable-github-pages.sh
./scripts/enable-github-pages.sh
# lub:
gh api --method POST repos/kris1pl/ai-research-forestry/pages -f build_type=workflow
```

Potem w GitHub:

1. **Settings → Actions → General → Workflow permissions** → **Read and write permissions** → Save.
2. **Settings → Environments → github-pages** — wyłącz *Required reviewers* (jeśli jest).
3. **Actions** → *Deploy Forestry Wiki (Quartz)* → **Re-run all jobs**.

### Kolejne deploye

Push na `main` → workflow buduje `site/public` i wdraża automatycznie.

**URL:** https://kris1pl.github.io/ai-research-forestry/

**Build fail na *Check GitHub Pages is enabled*** — nie wykonano jednorazowego `gh api` powyżej.

**404 w przeglądarce** — `deploy` się nie udał; oba joby muszą być zielone w Actions.

Jeśli forkujesz repo, zmień `baseUrl` w [`site/quartz.config.ts`](site/quartz.config.ts) na `twoj-user.github.io/nazwa-repo`.

### Inne hostingi (ręcznie)

| Platforma | Build | Output |
|-----------|-------|--------|
| Cloudflare Pages | `cd site && npm ci && npx quartz build` | `site/public` |
| VPS | ten sam build + `rsync` do nginx/Caddy | `site/public` |

## Polityka PDF

Pliki `raw/**/*.pdf` są w [`.gitignore`](.gitignore) (rozmiar). Zespół może:

- trzymać PDF na współdzielonym dysku / Git LFS,
- commitować wyłącznie `.txt` z `make extract-pdf`,
- w wiki cytować `source_file: raw/papers/nazwa.pdf` bez publikowania binariów na Pages.

## Współpraca Git

1. Branch z zmianami wiki → PR.
2. Review ingestów literaturowych (correctness claimów).
3. Merge → automatyczny deploy strony read-only.

## Powiązane

- [llm_wiki.md](llm_wiki.md) — opis wzorca
- Pipeline produkcyjny (kod) — osobne repozytorium; wiki opisuje metodologię w [`conifervision/project/pipeline-overview.md`](conifervision/project/pipeline-overview.md)

