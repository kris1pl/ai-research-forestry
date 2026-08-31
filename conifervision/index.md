---
okf_version: "0.2"
---
# Conifervision Research Wiki

Compiled team knowledge for **individual tree detection and segmentation** from drone imagery (orthophoto + CHM/3D), especially in **dense stands before thinning**. Also covers the current AREA production pipeline and species classification. Maintained by an LLM agent per `AGENTS.md` at the repository root.

## Current focus

1. **Research north star:** [[project/research-tree-detection-ensemble]] — multi-layer ensemble (LM, CHM/DEIMv2, RGB det/seg, fusion).
2. **Hypothesis loop:** [[project/hypothesis-validation-loop]] — propose → Experiment page → human gate → GPU module → validate/reject.
3. **Approved experiment queue (ADR-002):** [[experiments/exp-001-per-layer-baselines]] (**H1**, run first) → [[experiments/exp-003-rgb-seg-backend-ceiling]] (**H3**) → [[experiments/exp-002-merge-fusion-v1]] (**H2**).
4. **Literature map (dense ITD):** [[concepts/literature-map-dense-itd]] — what to test first vs background reading.

Production baseline (what ships today): [[project/pipeline-overview]]. Success structure: ADR-001 in [[project/decisions]] (proposed until eval numbers are locked).

## Project

- [[project/research-tree-detection-ensemble]] — **research north star** (ensemble, dense stands, data strategy)
- [[project/hypothesis-validation-loop]] — scientist ↔ engineer handoff for experiments
- [[project/pipeline-overview]] — current production AREA pipeline
- [[project/decisions]] — methodological ADRs (incl. ADR-001 ensemble v1)
- [[project/code-repo-integration]] — **TODO:** link to production code repository

## Pipeline methods

- [[methods/index]] — methods index (OKF progressive disclosure)

## Concepts

- [[concepts/literature-map-dense-itd]] — synthesis: priorities among ingested ITD/segmentation papers
- [[concepts/dense-stand-detection]] — evaluation concept for dense plots (before clearing)
- [[concepts/canopy-height-model]] — CHM (DSM − DTM); LiDAR and satellite SSL links
- [[concepts/pseudo-tree-crown]] — PTC input reformation for species CNNs (UAV)

## Experiments

- [[experiments/index]] — hypothesis units (queue H1 → H3 → H2)
- [[experiments/exp-001-per-layer-baselines]] — **H1** per-layer ceilings, open vs dense
- [[experiments/exp-003-rgb-seg-backend-ceiling]] — **H3** RGB seg backend A/B on dense
- [[experiments/exp-002-merge-fusion-v1]] — **H2** bbox NMS vs mask-aware fusion

## Literature sources

- [[sources/paper-insid3_in_context_segmentation_dinov3]] — INSID3 — training-free in-context segmentation using SVD-debiased DINOv3 features
- [[sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1]] — Chen (2025) — Evaluates SAM2 zero-shot tree crown segmentation prompted by DeepForest bounding boxes.
- [[sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021]] — Rodríguez-Puerta (2022) — Evaluates ITD and height extraction on young pine plantations, finding 10 cm CHM optimal and point cloud height extraction unbiased.
- [[sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025]] — TreePseCo — adapts PseCo framework using SAM and Faster R-CNN for robust individual tree crown segmentation in aerial imagery
- [[sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114]] — Holmgren et al. (2022) — Introduces 3D tree crown density models and mean-shift clustering to detect understory trees in multi-layered forest canopies.
- [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025]] — Pucino (2025) — Evaluates combinations of 3 CHM and 4 ITS algorithms across 15 Australian vegetation classes, finding Pit-Free CHM and DalPonte segmentation yield the highest accuracy.
- [[sources/paper-self_supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds]] — Shaheen (2025) — Self-supervised 3D LiDAR point cloud segmentation using transformation-invariant pretext tasks and energy-based soft clustering.
- [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests]] — Young et al. (2022) — Comprehensive evaluation of 7,568 combinations of drone flight parameters, photogrammetry settings, and ITD algorithms in a complex mixed-conifer stand.
- [[sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660]] — Lu (2025) — Introduces DEN4, an unsupervised deep learning-based point cloud denoising algorithm that improves individual tree segmentation accuracy.
- [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data]] — Li (2025) — introduces RDT, a hybrid tree segmentation framework combining CHM region-growing with point cloud density-guided vertical profile morphology analysis
- [[sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main]] — Tong (2025) — Adapts StarDist with a sparse-annotation loss function for individual tree crown delineation in dense RGB imagery.
- [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1]] — ForestFormer3D — End-to-end transformer-based 3D instance and semantic segmentation framework for forest LiDAR point clouds using ISA-guided query selection and score-based block merging.
- [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]] — Sparks (2022) — Comparative study of seven ITD methods across mixed-conifer stands using 8 and 22 ppm² ALS data, showing that stand density and parameter tuning drive accuracy more than method choice.
- [[sources/paper-comparison_of_individual_tree-twec21_public]] — Weckman (2021) — Comparative study of local maxima, trunk detection, and point density methods for individual tree detection using high-density UAV laser scanning.
- [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020]] — Mu (2020) — Canopy Maximum Model (CMM) and seeded K-means watershed segmentation to mitigate over-segmentation.
- [[sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340]] — BorFIT — A manually segmented and species-classified boreal forest LiDAR dataset with structural and spectral metrics
- [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]] — Ding (2025) — bottom-up oriented search and clustering method for extracting individual trees from ALS point clouds
- [[sources/paper-linguistic_guided_image_diffusion_model_for_tree_species_generation]] — Yun (2026) — LGINet text-guided diffusion model for synthetic tree canopy generation and enhanced YOLOv11 species identification
- [[sources/paper-treeflow]] — TreeFlow — Conditional Flow Matching for 3D tree point cloud generation from inventory attributes
- [[sources/paper-fsod-vfm]] — FSOD-VFM — A training-free few-shot object detection framework using UPN, SAM2, and DINOv2/v3 with graph diffusion to mitigate proposal overfragmentation.
- [[sources/paper-fine-tuning_matters_and_parallel_decoder_helps]] — Yu et al. (2026) — Introduces Hybrid Ensemble Decoder (HED) and progressive fine-tuning to stabilize few-shot object detection and reduce OOD overconfidence.
- [[sources/paper-edgecrafter]] — EdgeCrafter — compact ViT framework utilizing task-specialized DINOv3 distillation for edge dense prediction
- [[sources/paper-deimv2]] — DEIMv2 — Real-time DETR-based detector integrating DINOv3 backbones via Spatial Tuning Adapters
- [[sources/popescu-wynne-2004-seeing-the-trees]] — LiDAR CHM, variable-window local maxima, multispectral fusion (2004)
- [[sources/miao-zhang-2024-ptc-uav-species]] — pseudo tree crown (PTC), UAV species classification, ResNet50/PyTorch (2024)
- [[sources/vo-2024-automatic-data-curation]] — hierarchical k-means SSL data curation, satellite canopy height (Meta FAIR, 2024)

## Navigation

- [[log]] — wiki change timeline
- Full index: see sections above; the agent updates lists on this page after each ingest.
