# Wiki log

Chronological record of ingest, query, and lint operations.

## [2026-06-09] ingest | Vo et al. (2024) — SSL data curation (hierarchical k-means)

- Source: `raw/papers/2405.15613v2.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/vo-2024-automatic-data-curation]]
- Updated [[methods/dinov3-classification]], [[concepts/canopy-height-model]], [[index]]

## [2026-06-03] ingest | Miao et al. (2024) — PTC UAV species classification

- Source: `raw/papers/remotesensing-16-01849-v2.pdf`
- Added [[sources/miao-zhang-2024-ptc-uav-species]], [[concepts/pseudo-tree-crown]]
- Updated [[methods/dinov3-classification]], [[project/pipeline-overview]], [[index]], [[methods/index]]

## [2026-06-03] init | repo bootstrap

- Created LLM Wiki repository skeleton (vault `conifervision/`, Quartz, AGENTS.md).
- Seed: [[project/pipeline-overview]], [[methods/index]].

## [2026-06-03] i18n | English as primary language

- Translated vault content to English; `AGENTS.md` requires English for all new wiki pages.

## [2026-06-03] todo | code repo integration deferred

- Added [[project/code-repo-integration]] — planned link to production codebase (separate repo); not implemented yet.

## [2026-06-05] ingest | Popescu & Wynne (2004) — LiDAR CHM local maxima

- Source: `raw/papers/Seeing_the_Trees_in_the_Forest_Using_Lidar_and_Mul.pdf`
- Added [[sources/popescu-wynne-2004-seeing-the-trees]], [[concepts/canopy-height-model]]
- Updated [[methods/local-maxima]], [[methods/chm-detection]], [[index]]
- Added **Replication pseudocode** section; ingest rule in `AGENTS.md`
- **Replication notes** on [[methods/local-maxima]], [[methods/chm-detection]], [[methods/merge-detections]], [[concepts/canopy-height-model]]
