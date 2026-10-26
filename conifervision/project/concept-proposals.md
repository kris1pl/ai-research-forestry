---
type: Project
title: "Concept proposals"
description: "Review sheet for proposed concept pages. Accept, reject, or correct them here."
tags: [concepts, review]
status: draft
updated: 2026-10-26
generated:
  by: agent:concept-gate
  at: 2026-10-26T11:10:34Z
---

# Concept proposals

This sheet is the decision. The terminal list is only a copy.

Set `decision` to `accept` or `reject`. To correct a proposal, edit `name`, `slug`, and `why`, then set `decision` to `accept`. Leave `pending` while you are still reading.

Then run `make concept-gate APPLY=1`. That writes a concept page for each `accept`. It does not open an experiment folder.

```mermaid
flowchart LR
  run["make concept-gate"] --> sheet["This sheet"]
  sheet --> accept["decision: accept"]
  sheet --> reject["decision: reject"]
  accept --> page["Concept page"]
```

## area-based-approach

decision: accepted
name: Area-Based Approach
slug: area-based-approach
why: Existing concept literature-map-dense-itd covers individual tree detection workflows, leaving the standard plot- and grid-level statistical modeling of forest structural attributes (ABA) unrepresented.
sources:
- sources/paper-flygburen laserskanning för skogliga skattningar-faktaskog_04_2014
- sources/paper-skoglig fjärranalys-ljungbergs_sv_20180824
- sources/paper-skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet

## stem-taper-curve

decision: accepted
name: Stem Taper Curve
slug: stem-taper-curve
why: Existing concept tree-allometry covers total stem volume and whole-tree scaling relations, leaving continuous longitudinal diameter profile functions along tree height unrepresented.
sources:
- sources/paper-taper curve and volume functions for pine, spruce and birch-951-40-0589-9
- sources/paper-a rapid method for estimating the median diameter of the stem profile of norway spruce trees-iforest_ifor1945-009_vasilescu
- sources/paper-diameter, height and volume increment single tree models for improved sitka spruce in great britain-cpab049

## height-diameter-inversion

decision: accepted
name: Height-Diameter and Crown-Diameter Inversion
slug: height-diameter-inversion
why: Existing concept tree-allometry covers forward scaling of DBH to volume/crown metrics, whereas remote sensing inventory relies on inverted allometric formulations predicting DBH from height, crown width, and stand density.
sources:
- sources/paper-dbh vs height 1-s2-0-s0378112725008801-main
- sources/paper-prediction of diameter using height and crown attributes - filipescu_etal2012wjafdbh_ht_model
- sources/paper-robust height-diameter allometries for 41 european tree species - stand characteristics and structure matter-2025-09-29-679156v2_full

## direct-stem-dbh-point-cloud

decision: accepted
name: Direct Stem and DBH Measurement from 3D Point Clouds
slug: direct-stem-dbh-point-cloud
why: Existing concept tree-allometry covers empirical/allometric models predicting DBH from height or crown metrics rather than direct geometric stem reconstruction, trunk detection, and diameter extraction directly from 3D point cloud slices.
sources:
- sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations
- sources/paper-comparison_of_individual_tree-twec21_public
- sources/paper-estimating tree diameter at breast height (dbh) from uav data-1-s2-0-s2666017225001373-main

## foundation-model-tree-delineation

decision: accepted
name: Foundation Model Prompting for Tree Delineation
slug: foundation-model-tree-delineation
why: Existing concepts literature-map-dense-itd and dense-stand-detection focus on conventional CNN/watershed/NMS detection pipelines rather than zero-shot/few-shot prompting workflows leveraging vision foundation models (SAM/SAM2/DINOv2/v3) for crown delineation.
sources:
- sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025
- sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1
- sources/paper-fsod-vfm

## point-cloud-individual-tree-segmentation

decision: accepted
name: Point Cloud Individual Tree Segmentation
slug: point-cloud-individual-tree-segmentation
why: Existing concept canopy-height-model and literature-map-dense-itd focus on raster CHMs or dense 2D imagery, leaving direct 3D point cloud clustering and bottom-up tree instance segmentation unrepresented.
sources:
- sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main
- sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1
- sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds

## tree-allometry

decision: accepted
name: Tree-Level Allometric Scaling
slug: tree-allometry
why: Existing concept site-index-and-yield explicitly restricts coverage to stand-level site index, dominant height, basal area, and yield capacity, leaving individual tree DBH, crown width, crown base height, and stem volume relationships unrepresented.
sources:
- sources/paper-a crown width-diameter model for natural even-aged black pine forest management-forests-09-00610-v2
- sources/paper-a rapid method for estimating the median diameter of the stem profile of norway spruce trees-iforest_ifor1945-009_vasilescu
- sources/paper-a_linkage_among_tree_diameter_height_crown_base_he
- sources/paper-alder_allometry_cpi023
- sources/paper-allometric relationships of selected european tree-gp_eudor_pdfa1b_euna20855enc_001

## understory-tree-detection

decision: accepted
name: Understory tree detection
slug: understory-tree-detection
why: A canopy-height surface shows the top tree. A stem under that crown has no peak of its own. Dense-stand detection is side-by-side overlap, not this vertical case.
sources:
- sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114
- sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main
