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

### 5. Codzienna praca z wiki (quick reference)

```bash
# Ingest nowego paperu (podgląd → zapis)
make ingest-paper FILE=raw/papers/foo.pdf
make ingest-paper FILE=raw/papers/foo.pdf WRITE=1

# OKF lint — sprawdź / napraw frontmatter
make okf-lint
make okf-lint FIX=1

# Podgląd strony
make serve-wiki

# Build (CI / lokalnie)
make build-wiki-docker

# Deploy na GCP (ręcznie, normalnie robi CI)
make deploy-wiki-gcp
```

**Hipotezy (agent w Cursor):** *„Propose hypotheses for dense-stand segmentation”* (lub po polsku równoważnie). Agent czyta wiki, proponuje 2–3 kandydatów, a po Twoim wyborze zapisuje `conifervision/experiments/exp-NNN-*.md` (pseudokod, success/kill, handoff), aktualizuje `experiments/index.md` + `log.md`, opcjonalnie ADR w `project/decisions.md`. Opis pętli: [`conifervision/project/hypothesis-validation-loop.md`](conifervision/project/hypothesis-validation-loop.md) · reguła [`.cursor/rules/hypothesis-from-wiki.mdc`](.cursor/rules/hypothesis-from-wiki.mdc) · operacja w [`AGENTS.md`](AGENTS.md).

Szczegóły OKF: [`.cursor/rules/100-okf-standards.mdc`](.cursor/rules/100-okf-standards.mdc) · [`tools/README.md`](tools/README.md#okf-open-knowledge-format-v02) · [`AGENTS.md`](AGENTS.md#frontmatter-yaml--okf-v02)

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

### Deploy flow (end-to-end)

Architektura (kolejność ruchu):

```text
git push main
  → GitHub Actions (.github/workflows/deploy-wiki-gcp.yml)
    → cp conifervision/ → site/content/
    → npx quartz build → site/public/
    → gcloud storage rsync → gs://conifervision-wiki-prod
    → gcloud run services update wiki-frontend (SYNC_TRIGGER=$GITHUB_SHA)
      → kontener nginx przy starcie: gcloud storage rsync z GCS → /usr/share/nginx/html
wiki.conifervision.com
  → HTTPS Load Balancer + IAP (wiki-backend-v2)
  → Serverless NEG → Cloud Run wiki-frontend
```

#### Normalna ścieżka (zalecana)

```bash
# 1. Sprawdź vault przed push
make okf-lint

# 2. Commit + push na main → CI robi build + GCS + Cloud Run refresh
git push origin main

# 3. Status workflow
# GitHub → Actions → "Deploy Wiki (GCP + IAP)"
```

Ręczny deploy (gdy CI nie uruchomiłeś / lokalny build):

```bash
make deploy-wiki-gcp   # wymaga gcloud auth + uprawnień jak wiki-deployer
```

#### Weryfikacja po deploy

```bash
# Czy GCS ma świeży build?
gcloud storage ls -l "gs://conifervision-wiki-prod/index.html" --project=conifer-vision01

# Czy Cloud Run zsynchronizował pliki przy starcie?
gcloud run services logs read wiki-frontend \
  --region=europe-central2 \
  --project=conifer-vision01 \
  --limit=30
```

#### Gdy strona wygląda na starą (CI zielony)

CI wgrywa pliki do GCS i wymusza nową rewizję Cloud Run. Jeśli Safari/Chrome nadal pokazuje starą treść:

```bash
# 1. Wymuś restart kontenera (ponowny sync z GCS)
gcloud run services update wiki-frontend \
  --region=europe-central2 \
  --project=conifer-vision01 \
  --update-env-vars="SYNC_TRIGGER=$(date +%s)" \
  --quiet

# 2. Opcjonalnie: wyczyść cache CDN na Load Balancerze
gcloud compute url-maps invalidate-cdn-cache wiki-url-map \
  --path="/*" \
  --global \
  --project=conifer-vision01
```

Potem **hard refresh** (Cmd+Shift+R) albo tryb incognito.  
Uwaga: strony ze `status: draft` **nie trafiają** na wiki (filtr Quartz `RemoveDrafts`) — w Explorerze widać je dopiero po zmianie na `stable`.

#### Znane problemy i fixy

| Objaw | Przyczyna | Fix |
|-------|-----------|-----|
| CI: `PERMISSION_DENIED` … `artifactregistry.repositories.downloadArtifacts` | SA `wiki-deployer` nie może czytać obrazu Cloud Run z Artifact Registry | `gcloud artifacts repositories add-iam-policy-binding wiki --project=conifer-vision01 --location=europe-central2 --member="serviceAccount:wiki-deployer@conifer-vision01.iam.gserviceaccount.com" --role="roles/artifactregistry.reader"` |
| CI: Quartz `can not read a block mapping entry` + linia `P26-08-…T12:00:00Z` | Bug w `tools/wiki_update.py`: `re.sub` z `\1` + datą `2026-…` → oktal `\120` (= `P`) psuje frontmatter | Naprawione (`\g<1>`); lokalnie: `make okf-lint`, popraw `generated:` i push |
| CI: brak `index.html` / RSS zamiast strony | Vault nie skopiowany do `site/content` | Sprawdź krok „Prepare Quartz content”; treść musi być w `conifervision/` |
| Wiki bez nowych stron research | `status: draft` | Zmień na `stable` w frontmatter i zrób push |
| Lokalnie: `util.styleText` / Node engine | Quartz wymaga **Node ≥ 22** | `make build-wiki-docker` albo `nvm use 22` |
| Cloud Run URL `.run.app` → 404 bez IAP | Serwis jest `--no-allow-unauthenticated` | Czytaj tylko przez `https://wiki.conifervision.com` (IAP) |

GitHub Secrets (WIF): `bash infra/print-github-wiki-secrets.sh` → Settings → Secrets → Actions (`GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`).

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

