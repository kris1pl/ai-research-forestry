# AGENTS.md — Forestry Research LLM Wiki

Schema dla agentów (Cursor, Codex, Claude Code) utrzymujących tę bazę wiedzy. Wzorzec: [llm_wiki.md](llm_wiki.md).

## Cel

Research i dokumentacja **metodologii analizy obszarów leśnych (AREA)**:

- Orthophoto z dronów, local maxima (sliding window), CHM, DEIMv2, merge detekcji
- Klasyfikacja: DINOv3, klastrowanie, weak labels, Delta Lake (dane operacyjne poza repo)

Wiki **kompiluje** wiedzę z PDF, artykułów web i wyników eksperymentów — nie zastępuje pipeline’u produkcyjnego ani Delta Lake.

## Struktura repozytorium

| Ścieżka | Rola | Agent |
|---------|------|--------|
| `raw/papers/` | PDF (immutable, często gitignored) | **tylko czyta** |
| `raw/web/` | Markdown z clipów / scrapów | **tylko czyta** |
| `raw/assets/` | Obrazy załączników | **tylko czyta** |
| `wiki/` | Vault Obsidian — strony wiki | **tworzy i edytuje** |
| `site/` | Quartz (build → GitHub Pages) | **nie zmienia** bez prośby |
| `tools/` | Skrypty Python (ekstrakcja PDF) | ostrożnie, zgodnie z README |

## Typy stron (`wiki/`)

| `type` (frontmatter) | Folder | Zawartość |
|----------------------|--------|-----------|
| `project` | `project/` | Pipeline, ADR |
| `method` | `methods/` | Etapy pipeline + literatura |
| `concept` | `concepts/` | Pojęcia (CHM, weak labels, …) |
| `experiment` | `experiments/` | Hipoteza, metryki, wnioski |
| `source` | `sources/` | Streszczenie jednego PDF/artykułu |

Szablony: `wiki/.templates/`.

## Frontmatter (YAML)

Wymagane na każdej stronie wiki:

```yaml
---
title: "Czytelny tytuł"
type: method | concept | experiment | source | project
tags: [tag1, tag2]
status: active | candidate | superseded | draft
updated: YYYY-MM-DD
---
```

Opcjonalne:

- `area` — identyfikator AREA
- `related_methods` — lista slugów metod
- `sources` — lista `sources/slug`
- `metrics` — obiekt (np. `f1`, `dataset`)
- `hypothesis`, `source_file`, `authors`, `year` — wg typu

Strony z `status: draft` są pomijane przez Quartz (`RemoveDrafts`).

## Konwencje linków

- Wikilinki Obsidian: `[[slug]]` lub `[[folder/slug]]` — format **shortest** (zgodny z vault i Quartz).
- Każda teza z literatury: `[[sources/nazwa]]` + cytat lub numer strony w tekście.
- Nie linkuj do plików poza `wiki/` wikilinkami (np. `raw/` podawaj ścieżką w tekście lub w frontmatter `source_file`).

## Operacja: Ingest

**Wejście:** nowy plik w `raw/` (lub ścieżka podana przez użytkownika).

**Kroki:**

1. Przeczytaj źródło (PDF: opcjonalnie `make extract-pdf FILE=...` → `.txt` obok PDF).
2. Omów z użytkownikiem kluczowe wnioski (jeśli sesja interaktywna).
3. Utwórz/ zaktualizuj `wiki/sources/<slug>.md` (streszczenie, tezy, implikacje dla pipeline).
4. Zaktualizuj powiązane strony `methods/`, `concepts/` (typowo 5–15 plików).
5. Zaktualizuj `wiki/index.md` (katalog) i dopisz wpis do `wiki/log.md`:
   `## [YYYY-MM-DD] ingest | Tytuł źródła`
6. Oznacz sprzeczności względem istniejących stron (sekcja „Sprzeczności” lub adnotacja przy tezie).
7. Proponuj commit: `ingest: krótki opis źródła`.

**Nie modyfikuj** plików w `raw/` poza tym, co użytkownik sam doda.

## Operacja: Query

1. Czytaj `wiki/index.md`, potem relevantne strony.
2. Odpowiadaj z cytatami do stron wiki (`[[...]]`).
3. Jeśli odpowiedź jest trwałą wartością (porównanie metod, synteza) — zapisz nową stronę w `wiki/` (np. `concepts/` lub `experiments/`) i zaktualizuj `log.md`.

## Operacja: Lint

Okresowo (lub na prośbę):

- Sprzeczności między stronami i vs `wiki/project/pipeline-overview.md`
- Strony `status: active` z przestarzałymi claimami
- Orphan pages (brak linków przychodzących)
- Koncepty wspomniane bez własnej strony
- Brakujące `sources/` dla metod opartych na literaturze
- Luki do uzupełnienia (web search / nowe PDF)

Wynik lint: lista w czacie + opcjonalnie wpis w `log.md`: `## [date] lint | ...`

## Czego agent NIE robi

- Nie commituje bez prośby użytkownika.
- Nie umieszcza sekretów, kluczy API, ścieżek wewnętrznych z PII.
- Nie zmienia `site/quartz.config.ts` / workflow CI bez prośby.
- Nie zmienia parametrów ryzyka w kodzie produkcyjnym trading/forestry pipeline (inne repo) bez wyraźnej instrukcji.

## Publikacja (Quartz)

- Build: `make build-wiki` (katalog `site/`, treść z `wiki/` przez `site/content` → `../wiki`).
- Ignorowane przy build: `.obsidian`, `.templates`, `private`, pliki draft.
- `baseUrl`: `kris1pl.github.io/ai-research-forestry` — po fork zmień w `site/quartz.config.ts`.

## Język

- Treść wiki: **polski** (chyba że źródło angielskie — wtedy streszczenie PL, cytaty mogą być EN).
- Commity: polski lub angielski, spójnie w ramach PR.
