---
title: CHM and height-layer detection
type: Method
description: "CHM from the 3D model and ground model (laser / DTM). Object detection on height layers (small / large trees) — in production with DEIMv2 (deimv2-canopy)."
tags: [chm, lidar, detection]
status: stable
updated: 2026-08-21
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
related_methods:
  - methods/deimv2-canopy
  - methods/local-maxima
  - methods/merge-detections
sources:
  - sources/paper-treeflow
  - sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main
  - sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020
  - sources/paper-comparison_of_individual_tree-twec21_public
  - sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al
  - sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1
  - sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data
  - sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660
  - sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests
  - sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds
  - sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025
  - sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114
  - sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025
  - sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021
  - sources/popescu-wynne-2004-seeing-the-trees
---
# Canopy Height Model (CHM)

CHM from the 3D model and **ground model** (laser / DTM). Object detection on height layers (small / large trees) — in production with **DEIMv2** ([[deimv2-canopy]]).

## In the pipeline

Feeds [[merge-detections]] together with [[local-maxima]].

## Literature

[[sources/popescu-wynne-2004-seeing-the-trees]] — CHM construction workflow: ground classification, first-return DSM at fine grid, **max height per cell** for canopy surface, subtract terrain. Notes that CHM accuracy tracks DTM error and that interpolating all returns can underestimate apex height vs max-filtered DSM.

## Replication notes

CHM build pseudocode: [[sources/popescu-wynne-2004-seeing-the-trees#Replication pseudocode]] (steps **1–3**).

| Paper step | Our implementation (TBD) |
|------------|---------------------------|
| Ground / DTM from laser | Ground model in pipeline |
| Top canopy surface (max per sub-cell → grid) | Compare with our DSM/CHM rasterization |
| `CHM = top_DSM − DTM` | [[concepts/canopy-height-model]] |
| Height layers + DEIMv2 | **Beyond paper** — learned detectors on CHM strata |
| Load trained TreeFlow U-ViT model checkpoint | not used |
| Define conditioning parameters (species, platform, height) | not used |
| Sample source noise and integrate velocity field via ODE solver | not used |
| Denormalize and scale generated point cloud by target height | not used |
| Adaptive height filtering (shrub removal) | TBD |
| Oriented search and clustering | TBD |
| Validity checking and point updating | TBD |
| Morphological opening (erosion + dilation) on CHM | TBD |
| CMM calculation (3x3 neighborhood max) | TBD |
| Rasterize normalized point cloud to CHM | aligned |
| Apply Gaussian smoothing filter to CHM | aligned |
| Calculate minimum curvature for each cell | TBD |
| Contrast-stretch CHM based on curvature | TBD |
| Perform local maxima search on scaled image | aligned |
| Generate pit-free CHM at 50 cm resolution for high-density data | TBD |
| Evaluate detections against stem-mapped field data using 2.5 m horizontal search radius | TBD |
| CHM Generation (Pit-free method) | aligned |
| CHM Resolution Selection (25 cm vs 50 cm based on density) | TBD |
| Voxelize input point cloud (0.2m resolution) | TBD |
| Extract voxel-wise features using SpConvUNet | TBD |
| ISA-guided query point selection (dual-head MLP) | TBD |
| Transformer decoder forward pass | TBD |
| CHM Region-Growing coarse segmentation | aligned |
| Error classification using PDM local maxima | TBD |
| 3-D morphological vertical profile correction | TBD |
| Load raw noisy point cloud | TBD |
| Generate synthetic noise and construct double-noise point cloud | TBD |
| Train Encoder-Decoder Network unsupervised with MSE and repulsion loss | TBD |
| Apply predicted displacement vectors to denoise point cloud | TBD |
| Load normalized CHM raster | aligned |
| Apply moving-window mean smooth filter | TBD |
| Define VWF search radius function | aligned |
| Run VWF local maxima search | aligned |
| Extract height value at treetop location | aligned |
| Filter out treetops below minimum height | aligned |
| Statistical Outlier Removal (SOR) filtering | TBD |
| Coordinate normalization & spatial chunking | TBD |
| Pretext task training (predicting theta, T, s) | TBD |
| Energy function computation (height, density, slope) | TBD |
| Adaptive soft clustering (centroid initialization & merging) | TBD |
| Classify point cloud density | TBD |
| Generate Pit-Free CHM | TBD |
| Generate Model Fit Surface (MFS) via Bhattacharyya coefficient | not used |
| Smooth MFS with recursive Gaussian filter | not used |
| Watershed segmentation on smoothed MFS | not used |
| Target Generation (CHM peaks to Gaussian heatmap) | aligned |
| Heatmap Decoder Training (SSIM loss) | TBD |
| SAM Point & Box Prompting | TBD |
| Faster R-CNN Refinement & NMS | TBD |
| Generate 10 cm CHM | aligned |
| Detect treetops using Dalponte and Coomes (2016) | aligned |
| Segment individual tree crowns | aligned |


Pseudocode: [[sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021#Replication pseudocode]].

Pseudocode: [[sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025#Replication pseudocode]].

Pseudocode: [[sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114#Replication pseudocode]].

Pseudocode: [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025#Replication pseudocode]].

Pseudocode: [[sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds#Replication pseudocode]].

Pseudocode: [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests#Replication pseudocode]].

Pseudocode: [[sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660#Replication pseudocode]].

Pseudocode: [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data#Replication pseudocode]].

Pseudocode: [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1#Replication pseudocode]].

Pseudocode: [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al#Replication pseudocode]].

Pseudocode: [[sources/paper-comparison_of_individual_tree-twec21_public#Replication pseudocode]].

Pseudocode: [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020#Replication pseudocode]].

Pseudocode: [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main#Replication pseudocode]].

Pseudocode: [[sources/paper-treeflow#Replication pseudocode]].
**Replication focus for us:** validate ground model and CHM grid against paper’s max-cell rule before tuning DEIMv2 thresholds. Paper grid **0.5 m** — map to our resolution.

## Production parameters

_(height thresholds, CHM resolution, ground model version)_

## Related

- [[concepts/canopy-height-model]]
- [[methods/local-maxima]]

## Open questions from literature

- Can synthetic 3D tree point clouds generated by TreeFlow be used to train more robust 3D-to-2D projection layers for CHM-based detectors?
- Can the bottom-up oriented search and clustering method be integrated with CHM-based height-layer detection to resolve understory occlusions?
- Can morphological opening to generate a Canopy Maximum Model (CMM) replace Gaussian smoothing as our primary pre-processing step for reducing false positive treetops?
- How does the minimum curvature-based CHM contrast stretching scale across varying forest densities and species compositions?
- Does adaptive smoothing of the CHM based on local point density outperform a fixed-resolution CHM selection strategy across heterogeneous forest stands?
- Does ultra-fine CHM resolution (e.g., 10 cm) from drone photogrammetry introduce high-frequency surface noise that degrades local maxima detection compared to smoothed 25 cm or 50 cm resolutions?
- Can the ISA-guided query point selection mechanism be adapted to improve 2D/2.5D local maxima or DEIMv2-based canopy detection stages by incorporating 3D spatial and semantic embeddings?
- How does the RDT region-growing and density-guided correction perform on lower-density ALS or photogrammetric point clouds (SfM) compared to the high-density UAV LiDAR (18–125 pts/m²) used in the study?
- How does the computational overhead of DEN4 scale when processing large-scale forest surveys (e.g., inference time per hectare)?
- What are the optimal linear intercept and slope coefficients for the Variable Window Filter (VWF) across different conifer species densities, and how do wind speed thresholds affect the initial photogrammetric CHM reconstruction quality?
- Can the 3D energy-based soft clustering approach be optimized to run within acceptable operational latency bounds for large-scale regional datasets?
- How do the optimal height thresholds and grid resolutions for Pit-Free CHM generation scale across highly contrasting forest structures (e.g., tropical rainforests vs. open woodlands)?
- Can empirical 3D crown density templates be dynamically scaled using predicted heights from our 2D CHM-detection models to improve understory detection?
- How does the latency of the heavy SAM ViT-H encoder in TreePseCo scale when deployed in production pipelines compared to lighter CNN/ViT backbones?
- Can specialized sub-models or deep learning approaches reduce the high omission rates (RE ~15%) observed for young conifer trees under 1.0 m in height?