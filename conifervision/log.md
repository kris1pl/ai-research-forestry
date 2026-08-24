# Wiki log

Chronological record of ingest, query, hypothesis, and lint operations.

## [2026-08-24] hypothesis | Queue H1 → H3 → H2 approved (ADR-002)

- Human selected sequence: baselines → RGB seg backend ceiling → mask-aware fusion
- Updated [[experiments/exp-001-per-layer-baselines]] (H1), [[experiments/exp-002-merge-fusion-v1]] (H2)
- Added [[experiments/exp-003-rgb-seg-backend-ceiling]] (H3)
- ADR-002 accepted in [[project/decisions]]; Current focus + [[experiments/index]] updated

## [2026-08-24] lint | Visibility lift — north star on index + literature map

- Primary objective made explicit in `AGENTS.md` Purpose (dense ITD/segmentation, ensemble)
- Root [[index]]: Current focus + links to research program, hypothesis loop, experiments; OKF frontmatter only `okf_version`
- Added [[concepts/literature-map-dense-itd]] (Tier A/B/C synthesis)
- Promoted to `stable`: research program, hypothesis loop, dense-stand, edgecrafter-ecseg, exp-001, exp-002
- `wiki_update.append_index_source` no longer bumps root index frontmatter (OKF)

## [2026-08-21] ingest | Chen (2025) — Zero-shot tree detection and segmentation with SAM2

- Source: `raw/papers/ZERO-SHOT_TREE_DETECTION_AND_SEGMENTATION_FROM_AERIAL_FOREST_IMAGERY-2506.03114v1.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/merge-detections]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Rodríguez-Puerta (2022) — UAV LiDAR for young forest ITD and height

- Source: `raw/papers/UAV-Based_LiDAR_Scanning_for_Individual_Tree_Detection_and_Height_Measurement_in_Young_Forest-5_2021.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021]]
- Updated [[index]], [[concepts/canopy-height-model]], [[methods/chm-detection]], [[methods/local-maxima]], [[methods/merge-detections]]

## [2026-08-21] ingest | Vaschetti (2025) — TreePseCo for individual tree crown segmentation

- Source: `raw/papers/TreePseCo_Scaling_Individual_Tree_Crown_Segmentation_using_Large_Vision_Models-isprs-archives-XLVIII-M-7-2025-275-2025.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Holmgren (2022) — 3D density models and mean-shift for understory ITD

- Source: `raw/papers/Tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Pucino (2025) — CHM and ITS algorithm benchmark across vegetation types

- Source: `raw/papers/The_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-XLVIII-G-2025-1223-2025.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Shaheen (2025) — Self-supervised 3D LiDAR tree segmentation

- Source: `raw/papers/Self-Supervised_Learning_for_Precise_Individual_Tree_Segmentation_in_Airborne_LiDAR_Point_Clouds.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Young et al. (2022) — Drone parameters and ITD optimization in complex conifer forests

- Source: `raw/papers/Optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]]

## [2026-08-21] ingest | Lu (2025) — DEN4 unsupervised point cloud denoising

- Source: `raw/papers/LiDAR_point_cloud_denoising_for_individual_tree_extraction_based_on_the_Noise4Denoise-fpls-15-1490660.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/canopy-height-model]]

## [2026-08-21] ingest | Li (2025) — RDT hybrid tree segmentation using UAV LiDAR

- Source: `raw/papers/Individual_Tree_Segmentation_Based_on_Region-Growing_and_Density-Guided_Canopy_3-D_Morphology_Detection_Using_UAV_LiDAR_Data.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Tong (2025) — StarDist-based tree crown delineation

- Source: `raw/papers/Individual_tree_crown_delineation_in_high_resolution_aerial_RGB_imagery_using_StarDist-based_model-1-s2.0-S0034425725000227-main.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main]]
- Updated [[index]], [[methods/edgecrafter-ecseg]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Xiang (2025) — ForestFormer3D end-to-end 3D forest segmentation

- Source: `raw/papers/ForestFormer3D_A_Unified_Framework_for_End-to-End_Segmentation_of_Forest_LiDAR_3DPoint_Clouds-2506.16991v1.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1]]
- Updated [[index]], [[methods/chm-detection]], [[methods/merge-detections]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Sparks (2022) — ITD benchmark on low/high pulse density ALS

- Source: `raw/papers/Cross-comparision-of-ITD-methods-using-low-and-hight-pulse-density-ALS-2022-Sparks-et-al.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]]
- Updated [[index]], [[methods/local-maxima]], [[methods/chm-detection]], [[concepts/dense-stand-detection]]

## [2026-08-21] hypothesis | Hypothesis validation loop + Experiment template

- Added [[project/hypothesis-validation-loop]] (scientist ↔ engineer handoff)
- Strengthened `.templates/experiment.md`; refreshed [[experiments/exp-001-per-layer-baselines]], [[experiments/exp-002-merge-fusion-v1]]
- ADR-001 proposed in [[project/decisions]] (ensemble v1 success structure)
- AGENTS.md Operation: Hypothesis; Cursor rule `.cursor/rules/hypothesis-from-wiki.mdc`
- Linked from [[project/index]], [[project/research-tree-detection-ensemble]], README quick reference

## [2026-08-21] ingest | Weckman (2021) — UAV-LiDAR individual tree detection comparison

- Source: `raw/papers/Comparison_of_individual_tree-twec21_public.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-comparison_of_individual_tree-twec21_public]]
- Updated [[index]], [[methods/local-maxima]], [[methods/chm-detection]], [[methods/merge-detections]]

## [2026-08-21] ingest | Mu (2020) — K-means watershed segmentation for canopy LiDAR

- Source: `raw/papers/CANOPY_LIDAR_POINT_CLOUD_DATA_K-MEANS_CLUSTERING_WATERSHED_SEGMENTATION_METHOD-isprs-annals-VI-3-W1-2020-67-2020.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[methods/merge-detections]]

## [2026-08-21] ingest | Schladebach (2025) — BorFIT LiDAR dataset & species classification

- Source: `raw/papers/BorFIT_A_Novel_LiDAR-Based_Training_Dataset_for_Individual_Tree-essd-2025-340.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340]]
- Updated [[index]], [[methods/dinov3-classification]], [[concepts/canopy-height-model]]

## [2026-08-21] ingest | Ding (2025) — bottom-up oriented search and clustering for ALS

- Source: `raw/papers/A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds-1-s2.0-S157495412400520X-main.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/pseudo-tree-crown]]

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
