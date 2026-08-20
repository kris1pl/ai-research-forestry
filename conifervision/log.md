# Wiki log

Chronological record of ingest, query, and lint operations.

## [2026-08-20] ingest | Yun (2026) — LGINet text-guided diffusion for tree species generation

- Source: `raw/papers/Linguistic_guided_image_diffusion_model_for_tree_species_generation.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-linguistic_guided_image_diffusion_model_for_tree_species_generation]]
- Updated [[index]], [[methods/dinov3-classification]]

## [2026-08-20] ingest | Marcozzi (2026) — TreeFlow conditional 3D tree generation

- Source: `raw/papers/TreeFlow.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-treeflow]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/canopy-height-model]], [[concepts/pseudo-tree-crown]]

## [2026-08-20] ingest | Feng (2026) — FSOD-VFM few-shot detection & graph diffusion

- Source: `raw/papers/FSOD-VFM.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-fsod-vfm]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/deimv2-canopy]], [[concepts/dense-stand-detection]]

## [2026-08-20] ingest | Yu et al. (2026) — Hybrid Ensemble Decoder and progressive fine-tuning for cross-domain FSOD

- Source: `raw/papers/Fine-Tuning_Matters_and_Parallel_Decoder_Helps.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-fine-tuning_matters_and_parallel_decoder_helps]]
- Updated [[index]], [[methods/deimv2-canopy]], [[methods/dinov3-classification]]

## [2026-08-20] ingest | Liu et al. (2026) — EdgeCrafter compact ViTs for edge dense prediction

- Source: `raw/papers/EdgeCrafter.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-edgecrafter]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/deimv2-canopy]], [[methods/edgecrafter-ecseg]]

## [2026-08-19] ingest | Huang et al. (2026) — DEIMv2 real-time object detection with DINOv3

- Source: `raw/papers/deimv2.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-deimv2]]
- Updated [[index]], [[methods/deimv2-canopy]], [[methods/dinov3-classification]]

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
