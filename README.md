# Forestry Research LLM Wiki

Baza wiedzy zespołu o metodologii analizy obszarów leśnych — wzorzec [LLM Wiki](llm_wiki.md) (Andrej Karpathy): agent kompiluje źródła do trwałego wiki w Markdown, zamiast odkrywać je od zera przy każdym pytaniu.

## Struktura

| Katalog | Opis |
|---------|------|
| [`raw/`](raw/) | Niezmienne źródła: PDF, clipy web, obrazy (`assets/`) |
| [`wiki/`](wiki/) | Vault **Obsidian** — strony wiki (publikowane przez Quartz) |
| [`site/`](site/) | Quartz 4 — build statycznej strony |
| [`tools/`](tools/) | Python: ekstrakcja tekstu z PDF |
| [`AGENTS.md`](AGENTS.md) | Schema dla agenta: ingest / query / lint |

## Szybki start

### 1. Obsidian (lokalnie)

1. Zainstaluj [Obsidian](https://obsidian.md/).
2. **Open folder as vault** → wybierz katalog `wiki/` w tym repozytorium.
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

Treść builda: symlink `site/content` → `wiki/`. Katalog `raw/` **nie** trafia na stronę publiczną.

### 4. Praca z agentem

W Cursor (lub innym agencie) wskaż repozytorium i przeczytaj [`AGENTS.md`](AGENTS.md).

Przykładowe polecenia:

- *„Ingest PDF z `raw/papers/foo.pdf` — zaktualizuj wiki według AGENTS.md.”*
- *„Query: jakie metody merge local maxima z CHM opisuje literatura w wiki?”*
- *„Lint wiki — sprzeczności względem `wiki/project/pipeline-overview.md`.”*

## Publikacja (GitHub Pages)

Po pushu na `main`:

1. **Settings → Actions → General → Workflow permissions** → *Read and write permissions* → Save (wymagane m.in. dla `pages: write`).
2. **Actions** → *Deploy Forestry Wiki (Quartz)* → **Re-run all jobs** (workflow sam włącza Pages przy pierwszym runie, krok *Enable GitHub Pages*).

   Jeśli `deploy` nadal pada: ręcznie (jednorazowo):
   ```bash
   gh auth login
   gh api --method POST repos/kris1pl/ai-research-forestry/pages -f build_type=workflow
   ```
   oraz **Settings → Environments → github-pages** — wyłącz wymóg ręcznej akceptacji deployów (jeśli włączone).

Workflow [`.github/workflows/deploy-quartz.yml`](.github/workflows/deploy-quartz.yml) buduje `site/public` i wdraża.

**404 „There isn't a GitHub Pages site here”** — deploy się nie udał (sprawdź czerwony job `deploy`; `build` musi być zielony).

**Build fail na `configure-pages`** — Pages nie były włączone; ten krok nie jest w workflow — najpierw krok 2 powyżej.

**URL (domyślny):** https://kris1pl.github.io/ai-research-forestry/

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
- Pipeline produkcyjny (kod) — osobne repozytorium; wiki opisuje metodologię w [`wiki/project/pipeline-overview.md`](wiki/project/pipeline-overview.md)

