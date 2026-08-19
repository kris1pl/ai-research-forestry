# AGENTS.md — Conifervision Research LLM Wiki

Schema for agents (Cursor, Codex, Claude Code) maintaining this knowledge base. Pattern: [llm_wiki.md](llm_wiki.md).

## Language (required)

**All wiki work is in English.**

- New and updated pages in `conifervision/`: **English only** (body, titles, frontmatter `title` / `description`, ADRs, log entries).
- Agent replies to the user may be in the user’s language; **files committed to the vault are always English**.
- Source papers may be any language; summaries and integration into the wiki are **English**. Original quotes may stay in the source language with an English gloss if needed.
- Commit messages: **English**, imperative mood (e.g. `ingest: Smith 2024 CHM detection review`).

## Purpose

Research and documentation of **forest area (AREA) analysis methodology**:

- Drone orthophotos, local maxima (sliding window), CHM, DEIMv2, detection merge
- Classification: DINOv3, clustering, weak labels, Delta Lake (operational data outside this repo)

The wiki **compiles** knowledge from PDFs, web articles, and experiment results — it does not replace the production pipeline or Delta Lake.

**Production code repo:** lives in a separate repository (not linked yet). See `conifervision/project/code-repo-integration.md` — integration is **TODO**; do not add code paths or cross-repo automation until that page is marked done.

## Repository layout

| Path | Role | Agent |
|------|------|--------|
| `raw/papers/` | PDFs (immutable, often gitignored) | **read only** |
| `raw/web/` | Markdown from clips / scrapes | **read only** |
| `raw/assets/` | Attachment images | **read only** |
| `conifervision/` | Obsidian vault — wiki pages | **create and edit** |
| `site/` | Quartz (build → private GCP/IAP) | **do not change** unless asked |
| `tools/` | Python scripts (PDF extract) | careful, per README |

## Page types (`conifervision/`)

| `type` (frontmatter) | Folder | Content |
|----------------------|--------|-----------|
| `project` | `project/` | Pipeline, ADRs |
| `method` | `methods/` | Pipeline stages + literature |
| `concept` | `concepts/` | Concepts (CHM, weak labels, …) |
| `experiment` | `experiments/` | Hypothesis, metrics, conclusions |
| `source` | `sources/` | Single PDF/article summary |

Templates: `conifervision/.templates/`.

## Frontmatter (YAML) — OKF v0.2

`conifervision/` is an [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) bundle. Every **concept** `.md` (all files except reserved `index.md` / `log.md`) MUST have parseable YAML frontmatter with at least:

```yaml
---
type: Method | Concept | Source | Project | Experiment
title: "Human-readable title (English)"
description: "One-line summary"
tags: [tag1, tag2]
status: draft | stable | deprecated
generated:
  by: agent:ingest/gemini-3.5-flash   # or human:<name>
  at: 2026-06-09T12:00:00Z
---
```

**Reserved files (OKF):**

| File | Frontmatter |
|------|-------------|
| `conifervision/index.md` | **Only** `okf_version: "0.2"` |
| `conifervision/log.md` | None |
| `conifervision/*/index.md` | None — directory listing for progressive disclosure |

**Domain extensions** (optional, keep for forestry wiki):

- `updated: YYYY-MM-DD` — last touch date (legacy; prefer `generated.at`)
- `area`, `related_methods`, `sources` (OKF provenance list), `metrics`, `hypothesis`, `source_file`, `authors`, `year`, `replication_status`

**Status:** use OKF lifecycle — `stable` (was `active`), `draft`, `deprecated` (was `superseded`). Pages with `status: draft` or `draft: true` are skipped by Quartz.

**Links:** prefer OKF bundle-relative `[text](/methods/slug.md)` in new content; existing `[[wikilinks]]` remain valid for Obsidian/Quartz.

**Lint:** `make okf-lint` (see `.cursor/rules/100-okf-standards.mdc`).

Concept ID = path relative to `conifervision/` without `.md`.

## Link conventions

- Obsidian wikilinks: `[[slug]]` or `[[folder/slug]]` — **shortest** format (matches vault and Quartz).
- Every literature claim: `[[sources/name]]` + quote or page number in the text.
- Do not wikilink outside `conifervision/` (use plain paths for `raw/`, or `source_file` in frontmatter).

## Operation: Ingest

**Input:** new file in `raw/` (or path provided by the user).

**Steps:**

1. Read the source (PDF: optional `make extract-pdf FILE=...` → `.txt` beside the PDF). Batch: `make ingest-paper FILE=raw/papers/....pdf WRITE=1` — uses `get_llm_client()` (default Vertex) and `tools/wiki_update.py` to write the source page **and** update `log.md`, `index.md`, related `methods/` / `concepts/` pages. Wiki page output remains **English**.
2. Discuss key takeaways with the user when the session is interactive.
3. Create/update `conifervision/sources/<slug>.md` (summary, claims, pipeline implications, **replication pseudocode when feasible**) **in English**.
4. Update related `methods/`, `concepts/` pages (typically 1–5 files; automated by `ingest_paper` when using `WRITE=1`).
5. Update `conifervision/index.md` and prepend to `conifervision/log.md`:
   `## [YYYY-MM-DD] ingest | Source title` (automated by `ingest_paper`).
6. Flag contradictions with existing pages (“Contradictions” section or inline note).
7. Suggest commit: `ingest: short English description`.

**Do not modify** files in `raw/` except what the user adds.

### Replication pseudocode (on source pages)

When the paper describes a **procedural method** with enough detail, add a section **## Replication pseudocode** on the source page:

- Use **high-level pseudocode** (not production code) — numbered steps or a single fenced `text` block.
- State **inputs**, **outputs**, and **parameters** named in the paper (with units).
- Add **Prerequisites** (data, resolution, field plots, software assumptions).
- Add **Gaps** — what the paper does not specify (thresholds, full ground-classification rules, etc.).
- If replication is **not feasible** from the paper alone, write that explicitly and list what is missing (supplementary material, prior paper, proprietary workflow).

Do not invent numeric thresholds absent from the source; use `TBD` or “per field calibration” where appropriate.

Link replication steps to [[methods/...]] pages when updating them.

On each touched **method** or **concept** page, add or refresh **## Replication notes**:

- Link to `sources/<slug>#Replication pseudocode` (do not copy the full pseudocode block).
- Short table: paper step → our implementation status (`TBD`, aligned, not applicable).
- State when replication does not apply to that method.

## Operation: Query

1. Read `conifervision/index.md`, then relevant pages.
2. Answer with citations to wiki pages (`[[...]]`).
3. If the answer is durable (method comparison, synthesis) — save a new page under `conifervision/` (e.g. `concepts/` or `experiments/`) **in English** and update `log.md`.

## Operation: Lint

Periodically (or on request):

- Contradictions between pages and vs `conifervision/project/pipeline-overview.md`
- `status: active` pages with stale claims
- Orphan pages (no inbound links)
- Concepts mentioned without a dedicated page
- Missing `sources/` for literature-backed methods
- Non-English prose in the vault (flag for translation)

Lint output: list in chat + optional `log.md` entry: `## [date] lint | ...`

## What the agent must not do

- Commit without user request.
- Store secrets, API keys, or internal paths with PII.
- Change `site/quartz.config.ts` / CI workflows without request.
- Change production risk parameters in the forestry/trading pipeline repo without explicit instruction.
- Add or leave **Polish (or other non-English) body text** in `conifervision/` except inside quoted source excerpts.

## Publishing (Quartz)

- Build: `make build-wiki` (content from `conifervision/`; CI copies to `site/content`).
- Ignored at build: `.obsidian`, `.templates`, `private`, draft pages.
- Published URL: `https://wiki.conifervision.com` (IAP; `baseUrl`: `wiki.conifervision.com` in `site/quartz.config.ts`).
- UI locale: `en-US` in `site/quartz.config.ts`.

## Deferred: production code repository

Cross-linking to the main pipeline codebase (sibling repo, implementation paths, experiment ↔ `git sha` / MLflow) is **out of scope until completed** on `conifervision/project/code-repo-integration.md`. Until then, document methodology only; mention the external code repo in prose if needed, without inventing file paths.
