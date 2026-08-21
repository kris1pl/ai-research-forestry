---
title: Local maxima (sliding window)
type: Method
description: "Detect tree tops from a 3D surface or CHM using local maximum (LM) filtering with a sliding / variable-size window to estimate height and support tree detection."
tags: [detection, height, 3d, local-maxima]
status: stable
updated: 2026-08-21
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
related_methods:
  - methods/chm-detection
  - methods/merge-detections
sources:
  - sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main
  - sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020
  - sources/paper-comparison_of_individual_tree-twec21_public
  - sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al
  - sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data
  - sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests
  - sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds
  - sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025
  - sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114
  - sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021
  - sources/popescu-wynne-2004-seeing-the-trees
---
# Local maxima

Detect tree tops from a 3D surface or **CHM** using **local maximum (LM) filtering** with a **sliding / variable-size window** to estimate height and support tree detection.

## In the pipeline

Part of the merge path — see [[merge-detections]], [[project/pipeline-overview]].

## Literature

[[sources/popescu-wynne-2004-seeing-the-trees]] — variable square and **circular** LM windows on LiDAR CHM; window size tied to height–crown relationships from field data; circular windows favored for conifers with a single apex; square vs circular choice affects commission/omission trade-offs.

## Replication notes

Full step-by-step pseudocode: [[sources/popescu-wynne-2004-seeing-the-trees#Replication pseudocode]] (see **§6 — Variable-window local maxima**).

| Paper step | Our implementation (TBD) |
|------------|---------------------------|
| LM on CHM with variable window | Core of this method |
| Window size from height–crown model | Calibrate on our species / plots |
| Square vs circular window | Test both; paper favors circular for conifers |
| Species map scales windows | Optional — paper used multispectral fusion for pines |
| Adaptive height filtering (shrub removal) | TBD |
| Oriented search and clustering | TBD |
| Validity checking and point updating | TBD |
| Variable window size calculation based on height/crown | TBD |
| Local maxima detection on CMM | TBD |
| Rasterize normalized point cloud to CHM | aligned |
| Apply Gaussian smoothing filter to CHM | aligned |
| Calculate minimum curvature for each cell | TBD |
| Contrast-stretch CHM based on curvature | TBD |
| Perform local maxima search on scaled image | aligned |
| Define circular search window shape | aligned |
| Set search window diameter to average crown diameter (~2.5 m) | TBD |
| Run LMF over CHM to extract coordinates and heights | aligned |
| Fixed Local Maxima Filter (LMF) | aligned |
| Variable Window Filter (VWF) | aligned |
| Window size tuned to average crown diameter (<2.5 m) | TBD |
| Local height maxima detection on CHM | aligned |
| Local density maxima detection on PDM | TBD |
| Apply moving-window mean smooth to CHM | TBD |
| Calculate dynamic search radius based on height | aligned |
| Flag pixel as treetop if local maximum within radius | aligned |
| Compute Height Energy (Sigmoid normalized) | TBD |
| Compute Density Energy (Gaussian kernel over k-neighbors) | TBD |
| Compute Slope Energy (local slope based on neighbor height differences) | TBD |
| Combine energies into unified treetop indicator | TBD |
| Run DalPonte ITS Segmentation (local maxima + decision tree) | TBD |
| Evaluate accuracy using adjusted IoU (adj_IoU) | TBD |
| Scale search radius dynamically by local height h_max | aligned |
| Extract local point cloud distributions for template matching | not used |
| Identify local maxima on 10 cm CHM | aligned |


Pseudocode: [[sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021#Replication pseudocode]].

Pseudocode: [[sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114#Replication pseudocode]].

Pseudocode: [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025#Replication pseudocode]].

Pseudocode: [[sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds#Replication pseudocode]].

Pseudocode: [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests#Replication pseudocode]].

Pseudocode: [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data#Replication pseudocode]].

Pseudocode: [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al#Replication pseudocode]].

Pseudocode: [[sources/paper-comparison_of_individual_tree-twec21_public#Replication pseudocode]].

Pseudocode: [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020#Replication pseudocode]].

Pseudocode: [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main#Replication pseudocode]].
**Not in paper:** merge with DEIMv2 detections — see [[methods/merge-detections]]. **Gaps:** exact window coefficients — Popescu (2002); our sliding-window params in production config (when linked).

## Production parameters

_(fill in: window size, resolution, thresholds, circular vs square, variable-window rules)_

## Open questions from literature

- Do we use forest-type or species layers to scale windows (paper used multispectral fusion for pines)?
- Alignment between LM peaks and DEIMv2 boxes before [[merge-detections]].
- How does the 3D spherical neighborhood search radius selection compare to 2D variable-window local maxima in terms of over-segmentation in broadleaf crowns?
- How can we dynamically estimate local crown diameter (TC) and tree height (TH) per pixel to parameterize variable-window local maxima detection without prior manual measurements?
- What is the optimal standard deviation ($\sigma$) and window size for the Gaussian filter when applying the minimum curvature local maxima method to high-density UAV-LiDAR?
- How can we dynamically adjust the local maxima search window size based on local stand density proxies rather than a fixed average crown diameter?
- How can we dynamically scale the local maxima sliding window size based on local canopy density metrics rather than a single stand-level average?
- Can the spatial discrepancy between local height maxima and local density maxima be systematically used to detect asymmetric or leaning tree crowns?
- How does the multi-attribute energy function for treetop detection compare in commission/omission rates against variable-window local maxima on CHMs in dense conifer stands?
- What are the optimal sliding window sizes and maximum crown radius parameters for the DalPonte algorithm across different canopy density classes?
## Related

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
