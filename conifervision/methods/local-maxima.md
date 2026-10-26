---
title: Local maxima (sliding window)
type: Method
description: "Detect tree tops from a 3D surface or CHM using local maximum (LM) filtering with a sliding / variable-size window to estimate height and support tree detection."
tags: [detection, height, 3d, local-maxima]
status: stable
updated: 2026-10-26
generated:
  by: agent:conifervision-wiki
  at: 2026-10-26T12:00:00Z
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
  - sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations
  - sources/paper-mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_estonian_forests
  - sources/paper-site index models for main forest-forming tree species in poland_forests-11-00301
  - sources/paper-drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots
  - sources/paper-flygburen laserskanning för skogliga skattningar-faktaskog_04_2014
  - sources/paper-löv och lövblandbestånd - ekologi och skötsel-rytter_1998_redogorelse_8_100dpi
  - sources/paper-predicting_crown_width_using_nonlinear_mixed-effec
  - sources/paper-quality_description_lidar
  - sources/paper-skoglig fjärranalys-ljungbergs_sv_20180824
  - sources/paper-skogsinventering med flygburen laserskanning-appel_lucas
  - sources/paper-uav-enabled evaluation of forestry plantations_a comprehensive assessment of laser scanning and photogrammetric approa-1-s2-0-s2666017225000513-main
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
| Extrapolate 3D stem vector from base slices (1.3 m and 7.0 m) to CHM | TBD |
| 0.75 m cylinder pseudo-waveform height refinement | not used |
| Sample dominant/codominant trees (100 thickest/tallest per ha) | Aligned (LM picks local maxima in upper canopy layer) |
| Evaluate dynamic GADA height curve at base age 100 | TBD (not yet implemented in pipeline post-processing) |
| CanopyMaxima sliding window CHM detection | aligned |
| Ground classification via FUSION groundfilter and LAStools lasnoise | not used (CSF ground filter in production) |
| Watershed segmentation benchmark parity test | TBD |
| Detect peaks on rasterized surface model / template correlation surface | Aligned (variable sliding-window LM precomputed GeoJSON) |
| Extract segment morphology (width, height, width-to-height ratio) to model stem multiplicity | Not used (candidate for crown ownership and dense clumping logic) |
| Fit baseline power function CW = a * DBH^b | not used |
| Incorporate competition index (Hegyi or sum of relative DBH) and tree height into CW equation | TBD |
| Parameterize species-level random effects on exponent and crown base | not used |
| CHM rasterization (<0.5 m GSD) | Aligned |
| Local maxima crown apex identification | Aligned |
| Identify local canopy maxima on CHM | aligned |
| Watershed / morphological crown boundary delineation around peaks | not used (replaced by DEIMv2 bboxes and geometric merge) |
| CHM 3x3 moving-window mean smoothing | aligned |
| Local maxima detection parameterized by stand planting spacing | aligned |
| Filtering codominant leaders / forked stems prior to allometric extraction | not used |


Pseudocode: [[sources/paper-uav-enabled evaluation of forestry plantations_a comprehensive assessment of laser scanning and photogrammetric approa-1-s2-0-s2666017225000513-main#Replication pseudocode]].

Pseudocode: [[sources/paper-skogsinventering med flygburen laserskanning-appel_lucas#Replication pseudocode]].

Pseudocode: [[sources/paper-skoglig fjärranalys-ljungbergs_sv_20180824#Replication pseudocode]].

Pseudocode: [[sources/paper-predicting_crown_width_using_nonlinear_mixed-effec#Replication pseudocode]].

Pseudocode: [[sources/paper-flygburen laserskanning för skogliga skattningar-faktaskog_04_2014#Replication pseudocode]].

Pseudocode: [[sources/paper-drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots#Replication pseudocode]].

Pseudocode: [[sources/paper-site index models for main forest-forming tree species in poland_forests-11-00301#Replication pseudocode]].

Pseudocode: [[sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations#Replication pseudocode]].

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
- In dense stands on steep terrain, does horizontal displacement between local maxima apex candidates and bottom-up stem locations introduce systematic crown misattribution?
- Does variable-window local maxima on high-density RGB CHMs produce significantly different omission patterns compared to marker-controlled watershed segmentation when evaluating dominant normal-forest cohorts?
- Can segment width-to-height ratios be applied to local maxima clusters to flag multi-stem fused crowns before merge and CVAT ownership audits?
- Can competition indices estimated directly from initial CHM peak density serve as non-spatial surrogates to dynamically bound variable search windows in local maxima detection?
- Can automated geometric eccentricity or multi-peak clustering reliably identify and merge codominant leaders before crown metric extraction?
## Related

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
