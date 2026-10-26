---
title: CHM and height-layer detection
type: Method
description: "CHM from photogrammetric point clouds (CSF ground filter). DEIMv2 detection on height-stratified CHM bands — lower, upper, and R-class."
tags: [chm, photogrammetry, detection]
status: stable
updated: 2026-10-26
generated:
  by: agent:conifervision-wiki
  at: 2026-10-26T12:00:00Z
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
  - sources/paper-appiahmensah_et_al_2023_site_index_sis_rs
  - sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations
  - sources/paper-a_linkage_among_tree_diameter_height_crown_base_he
  - sources/paper-beech allometry_bgc4810s1
  - sources/paper-biomass and stem volume_951-40-1984-9
  - sources/paper-blanchard_tsaf_2016
  - sources/paper-crown_and_root_biomass_equations_fo
  - sources/paper-drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots
  - sources/paper-e_pb_laserdata_nedladdning_skog
  - sources/paper-estimating tree diameter at breast height (dbh) from uav data-1-s2-0-s2666017225001373-main
  - sources/paper-flygburen laserskanning för skogliga skattningar-faktaskog_04_2014
  - sources/paper-löv och lövblandbestånd - ekologi och skötsel-rytter_1998_redogorelse_8_100dpi
  - sources/paper-parameterization of height–diameter and crown radius-diameter relationship across the globe - rtae005
  - sources/paper-pine crown and trunk diameter dependence research-27_short_paper
  - sources/paper-predicting_crown_width_using_nonlinear_mixed-effec
  - sources/paper-prediction of diameter using height and crown attributes - filipescu_etal2012wjafdbh_ht_model
  - sources/paper-quality_description_lidar
  - sources/paper-robust height-diameter allometries for 41 european tree species - stand characteristics and structure matter-2025-09-29-679156v2_full
  - sources/paper-robust height-diameter allometries for 41 european tree species - supplementary data-2025-09-29-679156v2_media-1
  - sources/paper-simplifying uav-based photogrammetry in forestry_how to generate accurate digital terrain model and assess flight mission settings-forests-13-00173
  - sources/paper-skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet
  - sources/paper-skoglig fjärranalys-ljungbergs_sv_20180824
  - sources/paper-skoglig_fjarranalys_v1_0_161211
  - sources/paper-skogsinventering med flygburen laserskanning-appel_lucas
  - sources/paper-uav-enabled evaluation of forestry plantations_a comprehensive assessment of laser scanning and photogrammetric approa-1-s2-0-s2666017225000513-main
  - sources/popescu-wynne-2004-seeing-the-trees
---
# Canopy Height Model (CHM)

CHM from the **photogrammetric point cloud** (LAZ): CSF ground filtering → DTM → terrain-normalised canopy surface → CHM raster. Detection is **2D on CHM rasters** with **DEIMv2** ([[deimv2-canopy]]) — not learned 3D point-cloud detection.

LiDAR-assisted terrain correction is **not** part of the current production repo; external reference data may be used outside this chain.

## In the pipeline

Height-stratified CHM bands feed DEIMv2 + SAHI inference, then [[merge-detections]] together with [[local-maxima]].

## Production height bands

Configured via `LAYER_MODE` (`lower` | `upper` | `both`) and `preprocess_2d_raster_layer.py`:

| Band | Default height range | Role |
|------|---------------------|------|
| Lower | 0.3–4 m | Regeneration / low canopy |
| Upper | 4–30 m | Overstory |
| R-class | ~0–7.77 m (dedicated pipeline) | Small trees — separate DEIMv2 scales (100 px / 50 px) → [[methods/merge-detections]] |

CHM rasterisation may apply Gaussian smoothing (`smooth_sigma` in `chm_rasterizer.py`).

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
| Filter point cloud returns to [1.5 m, 50.0 m] above ground | aligned |
| Extract area-based height percentiles (Hp90, Hp95) on grid | aligned |
| Calculate growing-season normalized height increment (delta_Hp95) | not used |
| Species-specific MLR prediction of site index (SIS) | not used |
| Layered HDBSCAN stem base detection (2–4 m slices) | not used (production pipeline is top-down 2D CHM/ortho) |
| Chi-square radial distribution DBH fitting | not used |
| 3D stem vector extrapolation to CHM apex | TBD (relevant to leaning stem apex-to-base offset) |
| 10th-order polynomial pseudo-waveform height filtering | TBD |
| Extract individual tree height (H) from CHM peak | aligned |
| Condition 4-variate Vasicek SDE covariance on H and CW for DBH estimation | not used |
| Retrieve species parameters for height-DBH curve | TBD |
| Invert Mund power formula to solve DBH from CHM height | TBD |
| Compute expected crown area from double-logistic DBH curve | TBD |
| Compare predicted crown area against CHM/mask segmentation | TBD |
| Fit power allometry log(CA) ~ log(DBH) across canopy strata | TBD |
| Apply Baskerville log back-transformation correction exp(MSE/2) | TBD |
| Compute Iterative Hegyi Index aboveground competition intensity within 10 m radius | TBD |
| Fit component log-transformed power models with crown widths and competition | TBD |
| Apply transformation ratio correction factor k = sum(Y) / sum(exp(ln_Y)) | TBD |
| CHM rasterization from UAV SfM point clouds | aligned |
| Multi-camera GSD comparison (RGB 1.3 cm vs MS 7 cm) | not used |
| Filter ground points (class 2) from open ALS tiles | TBD |
| TIN/rasterize ALS ground points to DTM raster (RH 2000) | TBD |
| Normalize UAV DSM against ALS DTM (DSM - DTM) | TBD |
| Classify ground points and generate DTM/DSM at 2 cm GSD | aligned |
| Compute CHM = DSM - DTM | aligned |
| Marker-controlled watershed tree crown delineation on CHM | TBD |
| Isolate 1.2–1.4 m stem point slices for circle fitting | not used |
| Generate CHM via highest return or 3D geometric crown ellipsoid fitting | Aligned (CSF ground filter + rasterized CHM in production; template fitting not used) |
| Detect local maxima and segment crowns via watershed / region growing | Aligned (LM detection on CHM + height-banded DEIMv2) |
| Extract top height HT from CHM peak and crown area CA from delineated polygon | aligned |
| Compute cumulative crown area of larger trees (CAL = sum(CA_j) / Area for HT_j > HT_i) | TBD |
| Predict DBH via inverted power equation modified with CAL | TBD |
| Validate ALS return completeness (>= 1.0 pts/m2 in forest) | TBD |
| Flag potential ground overestimation zones in dense brushwood (+0.5 to +3.0 m bias) | TBD |
| Flight-line overlap vertical consistency check (< 0.15 m SE) | TBD |
| Fixed-effect height prediction from DBH, Dg, BA, and stand structure | not used |
| Local plot random effect recalibration (4 reference trees) | not used |
| Initial ground filtering (SMRF slope=0.18, window=17, threshold=0.5) | Alternative used (CSF via chm_rasterizer.py) |
| Ground points reclassification via median division & RANSAC plane fitting | Not used |
| Ground extension / surrounded gap closing via planar synthetic point interpolation | Not used |
| Bi-temporal selective logging detection (1/3 max canopy height threshold) | Not used |
| Extract percentile metrics (p70, p90, p95, p100) and vegetation proportion (prop40) per 10 m cell | TBD |
| Incorporate scan angle sine correction for canopy cover fraction | TBD |
| Predict H_gy and dominant height via multi-linear regression | TBD |
| Calculate standing volume and basal area via Jonsson form factors and volume density | TBD |
| Delineate operational thinning units by thresholding and polygon aggregation (gap < 50 m, min area >= 1 ha) | TBD |
| Photogrammetric SfM point matching | ODM / photogrammetry upstream |
| Ground elevation normalization against ALS DTM or ground filter | Aligned (CSF ground filter in chm_rasterizer.py) |
| Multi-scale ITD (<0.5 m pixel resolution) | Aligned (CHM rasterization at fine GSD) |
| Triangulation and bundle block adjustment | Upstream (ODM) |
| Dense 3D point cloud generation (SfM / dense matching) | Upstream (ODM) |
| Ground filtering (DTM derivation) via morphological/CSF filter | CSF ground filter (`chm_rasterizer.py`) |
| Digital surface model (DSM) calculation and CHM subtraction (DSM - DTM) | aligned (`preprocess_2d_raster_layer.py`) |
| Orthorectification onto surface model | Upstream (ODM) |
| Classify ground returns via TIN / progressive densification | aligned (CSF ground filter) |
| Height stratify vegetation (0–0.3 m, 0.3–2.0 m, >2.0 m) | aligned (0.3–4 m, 4–30 m, R-class 0–7.77 m) |
| Generate TIN DEM and DSM at 1.0 m grid resolution | aligned (chm_rasterizer.py) |
| Compute CHM = DSM - DEM | aligned |
| Filter candidate tree peaks at H >= 2.0 m and H > 8.0 m | aligned |
| Point cloud spatial density homogenisation (~400 pts/m²) | TBD |
| Pit-free CHM generation at 0.25 m resolution (Khosravipour et al.) | TBD |
| Marker-controlled watershed restricted to upper 90% of CHM | TBD |
| Initial SMRF/CSF ground filtering | aligned |
| Median-partitioned RANSAC ground reclassification | not used |
| Boundary-surrounded gap RANSAC planar synthesis | not used |
| PDAL DTM/DSM interpolation and CHM derivation | aligned |


Pseudocode: [[sources/paper-uav-enabled evaluation of forestry plantations_a comprehensive assessment of laser scanning and photogrammetric approa-1-s2-0-s2666017225000513-main#Replication pseudocode]].

Pseudocode: [[sources/paper-skogsinventering med flygburen laserskanning-appel_lucas#Replication pseudocode]].

Pseudocode: [[sources/paper-skoglig_fjarranalys_v1_0_161211#Replication pseudocode]].

Pseudocode: [[sources/paper-skoglig fjärranalys-ljungbergs_sv_20180824#Replication pseudocode]].

Pseudocode: [[sources/paper-skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet#Replication pseudocode]].

Pseudocode: [[sources/paper-simplifying uav-based photogrammetry in forestry_how to generate accurate digital terrain model and assess flight mission settings-forests-13-00173#Replication pseudocode]].

Pseudocode: [[sources/paper-robust height-diameter allometries for 41 european tree species - supplementary data-2025-09-29-679156v2_media-1#Replication pseudocode]].

Pseudocode: [[sources/paper-quality_description_lidar#Replication pseudocode]].

Pseudocode: [[sources/paper-prediction of diameter using height and crown attributes - filipescu_etal2012wjafdbh_ht_model#Replication pseudocode]].

Pseudocode: [[sources/paper-flygburen laserskanning för skogliga skattningar-faktaskog_04_2014#Replication pseudocode]].

Pseudocode: [[sources/paper-estimating tree diameter at breast height (dbh) from uav data-1-s2-0-s2666017225001373-main#Replication pseudocode]].

Pseudocode: [[sources/paper-e_pb_laserdata_nedladdning_skog#Replication pseudocode]].

Pseudocode: [[sources/paper-drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots#Replication pseudocode]].

Pseudocode: [[sources/paper-crown_and_root_biomass_equations_fo#Replication pseudocode]].

Pseudocode: [[sources/paper-blanchard_tsaf_2016#Replication pseudocode]].

Pseudocode: [[sources/paper-beech allometry_bgc4810s1#Replication pseudocode]].

Pseudocode: [[sources/paper-a_linkage_among_tree_diameter_height_crown_base_he#Replication pseudocode]].

Pseudocode: [[sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations#Replication pseudocode]].

Pseudocode: [[sources/paper-appiahmensah_et_al_2023_site_index_sis_rs#Replication pseudocode]].

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

| Parameter | Typical value | Notes |
|-----------|---------------|-------|
| `LOWER_MIN_M` / `LOWER_MAX_M` | 0.3 / 4 | Lower band |
| `UPPER_MIN_M` / `UPPER_MAX_M` | 4 / 30 | Upper band |
| R-class band | 0–7.77 m | Small-tree pipeline defaults |
| Ground filter | CSF | Photogrammetric LAZ, not LiDAR DTM in-repo |
| Inference | SAHI tiled | `run_cloud_preds_chm_skip_empty_multiprocess.py` |

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
- Can area-based site index priors (12.5 m SIS rasters) constrain height-growth expectations and improve crown tracking across repeated drone flight epochs?
- Can the 10th-order polynomial pseudo-waveform filter be applied directly to 3D photogrammetric canopy points to prevent stray multipath noise and sparse apex overshoots in height estimation?
- Can the 4-variate SDE conditional covariance between CHM height and crown width be used as a biophysical consistency prior to filter out false-positive tree detections or split oversegmented crowns?
- Can species-specific asymptotic height caps in the inverted Mund allometric equations reliably handle CHM over-estimates without producing runaway DBH predictions?
- Does the observed shift in crown-area vs. height allometric scaling at canopy emergence justify distinct allometric inversion models for lower vs. upper CHM height layers?
- Can horizontal crown dimensions and spatial competition indices derived from 2D crown detections substitute for unreliable sub-canopy photogrammetric heights when estimating understory sapling biomass?
- Can Lantmäteriet 1–2 pts/m² ALS class-2 ground points replace UAV photogrammetric CSF ground filtering for CHM generation across operational Swedish test sites?
- Can 3D ellipsoid template correlation surfaces provide cleaner crown boundaries than raw maximum-return binning for height-stratified CHM rasterization in dense conifer stands?
- Can height-stratified CHM slicing thresholds dynamically adapt to mixed broadleaf-conifer stands where overstory birch crowns exceed 30–40% closure and suppress understory spruce detection?
- Can the piecewise Gaussian trunk-to-crown diameter prior from Pyataev & Vais be inverted to reliably regularize bounding box dimensions during height-stratified detection in dense Scots pine stands?
- Can cumulative crown area of larger trees (CAL) computed directly over sliding spatial neighborhoods from CHM detections substitute for ground-measured basal area of larger trees without exacerbating edge effects?
- When normalising photogrammetric DSMs with Lantmäteriet national DTMs, what automated heuristic can detect and correct 2–3 m ground elevation bias in young regeneration stands (R-class) where historical ALS failed to penetrate dense shrub layers?
- Can the 4-tree local recalibration factor (lambda) be inverted against CHM-derived dominant heights to estimate stand basal area or diameter distributions without ground measurements?
- Can RANSAC-based surrounded gap interpolation be adapted to post-process CSF ground classifications in dense conifer stands to prevent ground-mounding artifacts and height-slicing distortion?
- Can the scan angle correction term (sin|theta|) used for off-nadir ALS penetration bias be adapted to wide-FOV UAV photogrammetry orthophotos or CHM canopy density rasters across swath edges?
- In dense mature conifer stands where photogrammetric point clouds lack under-canopy ground penetration, what vertical error margin is introduced into CHM height-stratified detection bands when relying purely on CSF filtering rather than Lantmäteriet ALS DTM data?
- How do residual terrain interpolation artifacts in photogrammetric DTMs affect height layer stratification boundaries in dense young conifer stands compared to ALS DTM baselines?
- Should high-altitude outlier filtering (e.g. SOR or LAS class 7 exclusion) be formally hardened prior to rasterization to eliminate 20+ m canopy height spikes in low-density or noisy point clouds?
- How severely does photogrammetric DTM drift degrade height-stratified layer slicing in closed-canopy conifer stands when LiDAR ground benchmarks are unavailable?
- Can median-partitioned RANSAC plane reclassification and void gap filling be integrated into `chm_rasterizer.py` to prevent terrain floating and height underestimation in dense pre-thinning stands?