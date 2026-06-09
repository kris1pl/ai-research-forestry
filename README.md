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
| [`tools/`](tools/) | Python: PDF extract, warstwa LLM (Vertex / OpenAI) |
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

Opcjonalnie — test warstwy LLM (Vertex domyślnie, konfiguracja w [`.env.example`](.env.example)):

```bash
cp .env.example .env   # uzupełnij VERTEX_PROJECT itd.
make llm-smoke
```

Szczegóły: [`tools/README.md`](tools/README.md#llm-layer-toolsllm).

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

Treść builda: katalog `conifervision/` (w CI kopiowany do `site/content`). Katalog `raw/` **nie** trafia na stronę.

Jeśli widzisz **RSS/XML zamiast strony** — build/deploy bez treści vault (zły folder `conifervision/`). Po poprawce zrób push i **Re-run** workflow.

### 4. Praca z agentem

In Cursor (or another agent), point at the repo and read [`AGENTS.md`](AGENTS.md) (English wiki only).

Example prompts:

- *“Ingest `raw/papers/foo.pdf` — update the wiki per AGENTS.md (English), including replication pseudocode if the method is clear enough.”*
- *“Query: what does the wiki say about merging local maxima with CHM detections?”*
- *“Lint the wiki against `conifervision/project/pipeline-overview.md`.”*

## Publikacja (GCP + IAP — prywatna)

Wiki jest dostępna **tylko** po zalogowaniu Google:

**https://wiki.conifervision.com**

| Element | Wartość |
|---------|---------|
| Hosting | GCS `conifervision-wiki-prod` → Cloud Run `wiki-frontend` → HTTPS LB + **IAP** (`wiki-backend-v2`) |
| Auth | OAuth **External** (projekt bez GCP Organization) — szczegóły w [`docs/deploy-gcp-iap.md`](docs/deploy-gcp-iap.md) |
| Deploy | Push na `main` → workflow [`.github/workflows/deploy-wiki-gcp.yml`](.github/workflows/deploy-wiki-gcp.yml) |
| `baseUrl` | `wiki.conifervision.com` w [`site/quartz.config.ts`](site/quartz.config.ts) |

**Pełna instrukcja setupu (DNS, OAuth, GitHub Secrets):** [`docs/deploy-gcp-iap.md`](docs/deploy-gcp-iap.md)

**Skrypt infrastruktury (jednorazowo):**

```bash
bash infra/setup-gcp-wiki.sh
```

Czytelnicy **nie** potrzebują dostępu do GCP Console — tylko konta Google z dostępem IAP (poniżej).

### Dodawanie nowych użytkowników

Nowa osoba potrzebuje **dwóch** uprawnień (w trybie OAuth *Testing* oba są wymagane):

#### 1. Test user (OAuth consent screen)

Dopóki aplikacja OAuth jest w trybie **Testing**, Google wpuszcza tylko adresy z listy test users.

1. [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent?project=conifer-vision01)
2. Sekcja **Test users** → **Add users**
3. Wpisz e-mail (np. `nowy.uzytkownik@conifervision.com` lub osobisty Gmail, jeśli tak uzgodniliście)
4. **Save**

#### 2. Dostęp IAP (czytanie wiki)

1. [Identity-Aware Proxy](https://console.cloud.google.com/security/iap?project=conifer-vision01)
2. Zasób **Backend services** → **`wiki-backend-v2`**
3. **Add principal** (lub **Grant access**)
4. **New principals:** adres e-mail użytkownika (np. `nowy.uzytkownik@conifervision.com`)  
   — albo grupa `wiki-readers@conifervision.com`, jeśli użytkownik jest już w grupie w [Google Admin](https://admin.google.com)
5. **Role:** **Cloud IAP** → **IAP-secured Web App User**
6. **Save**

Alternatywnie z terminala (ten sam e-mail co w kroku 1):

```bash
gcloud iap web add-iam-policy-binding \
  --project=conifer-vision01 \
  --resource-type=backend-services \
  --service=wiki-backend-v2 \
  --member='user:nowy.uzytkownik@conifervision.com' \
  --role='roles/iap.httpsResourceAccessor'
```

#### 3. Co wysłać użytkownikowi

- Link: **https://wiki.conifervision.com**
- Logowanie: konto Google podane w krokach 1–2
- **Nie** nadawaj ról w GCP Console (Viewer/Editor) — to nie jest potrzebne do czytania wiki

#### Typowe błędy

| Objaw | Przyczyna |
|-------|-----------|
| *Access blocked* / aplikacja w testowaniu | Brak na liście **Test users** (krok 1) |
| *You don't have access* (403) po logowaniu | Brak roli **IAP-secured Web App User** (krok 2) |
| `Empty Google Account OAuth client ID` | IAP włączone bez OAuth client na `wiki-backend-v2` — patrz [`docs/deploy-gcp-iap.md`](docs/deploy-gcp-iap.md) |

#### Grupa zamiast pojedynczych maili (opcjonalnie)

W [Google Admin](https://admin.google.com): grupa **`wiki-readers@conifervision.com`** → dodaj członków.  
W IAP (krok 2) jeden principal: `wiki-readers@conifervision.com` zamiast wielu `user:…`.  
Każdy nowy członek grupy nadal musi być na liście **Test users**, dopóki OAuth jest w trybie *Testing*.

### GitHub Pages (wyłączone — nie używać)

Publiczny URL `https://kris1pl.github.io/ai-research-forestry/` **musi być wyłączony** — wiki jest tylko na GCP + IAP.

Workflow `.github/workflows/deploy-quartz.yml` został usunięty z repo. Jeśli Pages nadal działają, wyłącz je **raz**:

**Opcja A — skrypt (gh CLI + admin repo):**

```bash
chmod +x scripts/disable-github-pages.sh
./scripts/disable-github-pages.sh
```

**Opcja B — przeglądarka:**

1. [Settings → Pages](https://github.com/kris1pl/ai-research-forestry/settings/pages)
2. **Unpublish site** albo **Source: None** → Save

**Weryfikacja:**

```bash
curl -sI https://kris1pl.github.io/ai-research-forestry/ | head -3
# Oczekiwane: HTTP/2 404 (lub brak 200)
```

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

