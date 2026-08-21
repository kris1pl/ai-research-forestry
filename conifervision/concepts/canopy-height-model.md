---
title: Canopy height model (CHM)
type: Concept
description: "Normalized height of vegetation above ground: CHM = surface model of canopy top − digital terrain model (DTM)."
tags: [chm, dtm, dsm, lidar, height]
status: stable
updated: 2026-08-21
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
related_methods:
  - methods/chm-detection
  - methods/local-maxima
sources:
  - sources/vo-2024-automatic-data-curation
  - sources/paper-treeflow
  - sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340
  - sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al
  - sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data
  - sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660
  - sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests
  - sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025
  - sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114
  - sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021
  - sources/popescu-wynne-2004-seeing-the-trees
---
# Canopy height model (CHM)

Normalized height of vegetation above ground: **CHM = surface model of canopy top − digital terrain model (DTM)**.

## In our pipeline

Produced from 3D data and laser **ground model**, then used for height-stratified detection (DEIMv2) and merge with [[methods/local-maxima]]. See [[project/pipeline-overview]].

## Literature baseline

[[sources/popescu-wynne-2004-seeing-the-trees]] — small-footprint LiDAR CHM with 0.5 m grid; top-of-canopy DSM from **maximum elevation per sub-cell** before subtracting terrain; discusses underestimation when all first returns are interpolated without max filtering.

[[sources/vo-2024-automatic-data-curation]] — satellite canopy-height SSL experiment (Tolan et al. 2023 setup): hierarchical k-means curation of 18M → 9M patches improved backbone **block R² ~20%** on NEON / aerial NEON height benchmarks — indirect evidence that balanced aerial pre-training helps height-related downstream tasks.

## Design notes for us

- Ground model quality directly bounds height error.
- Grid resolution vs point density (drone GSD / LiDAR density).
- Whether apex detection uses raw CHM peaks ([[methods/local-maxima]]) or learned detectors on CHM layers ([[methods/chm-detection]]).

## Replication notes

Minimal replication chain from [[sources/popescu-wynne-2004-seeing-the-trees#Replication pseudocode]]:

```text
DTM → top_DSM (max per sub-cell) → CHM = top_DSM - DTM
```

Details and gaps (ground classifier, kriging): on the **source** page — not duplicated here. Implementation path: [[methods/chm-detection]].

## Related

- [[methods/chm-detection]]
- [[methods/local-maxima]]

## Open questions from literature

- Does pre-training our backbone on hierarchical-k-means-curated regional orthophotos improve local tree-level height regressions?
- How does the height-dependent resolution degradation in generative models like TreeFlow affect the fidelity of synthetic canopy height models derived from them?
- Can the 2D projection triangle fitting algorithm from BorFIT be reliably automated on noisy, raster-derived canopy height models without full 3D point cloud segmentation?
- Does the unsupervised DEN4 denoising model generalize effectively to highly mixed, multi-layered temperate or tropical forest canopies?
- How does the optimal CHM resolution scale when transitioning from high-density UAV LiDAR (190+ points/m²) to lower-density aerial LiDAR (ALS) in young stands?