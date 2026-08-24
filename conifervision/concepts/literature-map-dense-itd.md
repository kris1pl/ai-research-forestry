---
title: Literature map — dense individual tree detection (ITD)
type: Concept
description: "Prioritized synthesis of ingested papers for dense-stand tree detection/segmentation from drone RGB and LiDAR/CHM — what to test first vs background."
tags: [literature-map, dense-stands, itd, segmentation, ensemble, synthesis]
status: stable
updated: 2026-08-24
generated:
  by: agent:conifervision-wiki
  at: 2026-08-24T12:00:00Z
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/edgecrafter-ecseg
  - methods/merge-detections
sources:
  - sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al
  - sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests
  - sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main
  - sources/paper-edgecrafter
  - sources/paper-deimv2
  - sources/paper-fsod-vfm
---

# Literature map — dense ITD

Living synthesis for agents and humans: among ~25 ingested sources, **what matters first** for the Conifervision objective (drone ortho + CHM/3D, **dense stands before thinning**, ensemble path). North star: [[project/research-tree-detection-ensemble]]. Dense eval concept: [[concepts/dense-stand-detection]].

This page does **not** replace individual [[sources/index]] summaries. Refresh after major ingests or when experiment conclusions contradict claims below.

## Tier A — test / design first (align with exp-001 / exp-002)

| Theme | Why it matters for us | Key sources |
|-------|----------------------|-------------|
| Density & tuning beat method brand | Sparks: stand density and parameters drive ITD accuracy more than which classic algorithm you pick → baselines + dense split before fancy fusion | [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]] |
| Acquisition + CHM + ITD interactions | Young: huge combinatorial space (flight / photogrammetry / ITD) in complex conifer → protocol and GSD/CHM choices are first-class | [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests]] |
| RGB instance / crown delineation in dense imagery | Tong StarDist + sparse labels; TreePseCo / SAM-family for crowns — candidates for RGB seg layer next to ECSeg | [[sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main]], [[sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025]], [[sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1]] |
| Production detector stack | DEIMv2 (DINOv3 adapters); EdgeCrafter ECDet/ECSeg — our planned RGB/CHM learned layers | [[sources/paper-deimv2]], [[sources/paper-edgecrafter]] |
| Overfragmentation / proposal merge | FSOD-VFM graph diffusion on overlaps — idea for fusion / NMS in dense crowns | [[sources/paper-fsod-vfm]] |
| Classic LM + CHM baselines | Popescu variable window; Weckman / Mu / Pucino comparisons — ceilings for geometric path | [[sources/popescu-wynne-2004-seeing-the-trees]], [[sources/paper-comparison_of_individual_tree-twec21_public]], [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020]], [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025]] |

## Tier B — strong for 3D / understory / hybrid CHM+cloud (after RGB/CHM ensemble baselines)

| Theme | Sources (examples) |
|-------|-------------------|
| Hybrid CHM + point morphology | [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data]] (RDT) |
| 3D density / understory | [[sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114]] |
| End-to-end 3D instance (LiDAR) | [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1]] |
| Bottom-up ALS clustering | [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]] |
| Denoise before ITD | [[sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660]] |
| Young stand / CHM resolution | [[sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021]] |

## Tier C — data / SSL / species (support, not first ITD experiment)

| Theme | Sources |
|-------|---------|
| Gold / benchmark LiDAR crowns | [[sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340]] |
| SSL point segmentation | [[sources/paper-self_supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds]] |
| Weak-label / SSL curation | [[sources/vo-2024-automatic-data-curation]] |
| Species / PTC / synthetic canopies | [[sources/miao-zhang-2024-ptc-uav-species]], [[sources/paper-linguistic_guided_image_diffusion_model_for_tree_species_generation]], [[sources/paper-treeflow]] |
| Few-shot detector training tricks | [[sources/paper-fine-tuning_matters_and_parallel_decoder_helps]] |

## Implications for the hypothesis loop

1. Run [[experiments/exp-001-per-layer-baselines]] with **open vs dense** before comparing new algorithms (Sparks / Young lesson).
2. Optionally compare RGB instance backends on dense tiles ([[experiments/exp-003-rgb-seg-backend-ceiling]]) before locking ECSeg for fusion.
3. Prefer **mask-aware fusion** ([[experiments/exp-002-merge-fusion-v1]]) once RGB seg has a chosen ceiling.
4. Treat pure 3D end-to-end models as **parallel track** unless AREA workflow already commits to dense UAV LiDAR as primary input.
5. Species and synthetic data stay **downstream** of instance detection quality.

Approved queue: **ADR-002** (H1 → H3 → H2) in [[project/decisions]].

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[methods/merge-detections]]
