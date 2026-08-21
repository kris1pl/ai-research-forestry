---
title: Dense stand detection (before clearing)
type: Concept
description: "Evaluation concept for tree detection in dense stands where crown overlap breaks bbox-centric NMS and segmentation boundaries drive errors."
tags: [dense-stands, evaluation, detection, instance-segmentation, dense/open]
status: draft
updated: 2026-08-21
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
related_methods:
  - methods/merge-detections
  - methods/deimv2-canopy
  - methods/edgecrafter-ecseg
sources:
  - sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al
  - sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1
  - sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main
  - sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data
  - sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds
  - sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025
  - sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114
  - sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025
  - sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1
  - sources/paper-fsod-vfm
---
# Dense stand detection (before clearing)

This concept defines how we should evaluate (and eventually improve) tree detection in dense stands (for example, before clearing), where crown overlap and connected topology create failure modes that differ from sparse plots.

## Definition (operational, TBD)

We need an operational definition of "dense" vs "open" that we can compute consistently from available geometry and annotations.

- Dense/open split: TBD (example: LiDAR/CHM-derived canopy density proxy, or ground-truth tree count density per AREA tile).
- Size bins: small vs large trees: TBD (must align with your CHM/DEIMv2 height-layer stratification).

## Why dense stands are different

Expected dense-specific error modes:

- Duplicate suppression: bbox-centric NMS may eliminate true neighboring trees.
- Boundary quality: instance segmentation errors (under-segmentation, merged instances, jagged boundaries) can dominate quality.
- Geometry degeneracy: CHM can be locally flat or insufficiently separable, reducing the value of purely geometric layers.

## In our pipeline (research)

Used to structure experiments in `[[project/research-tree-detection-ensemble]]`:

- baseline measurements per layer in open vs dense splits
- error taxonomy specialized for dense plots
- fusion strategy validation where segmentation boundary quality matters

## Design notes (hypotheses)

Working hypothesis:

- segmentation-first fusion (or mask-aware merge rules) yields better separation in dense stands than pure bbox voting.

## Metrics we likely need (without locking numbers yet)

By size bin and open vs dense:

- detection metrics for small and large objects (use your current production definitions)
- boundary-aware instance metrics (for segmentation-first approaches)
- under-segmentation and duplicate rate proxies (to explain dense failure modes)

## Replication notes

TBD:

- when we ingest papers covering dense detection, add links to `[[sources/...#Replication pseudocode]]` here
- until then, this concept is a protocol container for your internal evaluation and ablations

## Related

- `[[project/research-tree-detection-ensemble]]`
- `[[methods/merge-detections]]`
- `[[methods/edgecrafter-ecseg]]`

## Open questions from literature

- Does applying a PageRank-style graph diffusion process over SAM2 mask overlaps help resolve boundary-level under-segmentation and duplicate detections in dense conifer stands?
- Can multi-return ALS intensity or waveform metrics be integrated into our detection merge layer to improve the detection rate of intermediate and suppressed trees in dense stands?
- Can we establish a canopy density threshold above which geometric ITD methods must be supplemented by deep-learning-based multi-layer detectors to resolve suppressed understory trees?
- Does a query-based 3D transformer decoder (like ForestFormer3D) provide better separation of overlapping crowns in dense stands compared to bottom-up clustering or 2D instance segmentation (ECSeg)?
- - Does representing overlapping tree crowns as star-convex polygons resolve the boundary degeneracy and duplicate suppression issues typical of bbox-centric NMS in dense stands?
- What is the optimal polynomial degree ($n$) and surface point extraction interval for fitting vertical profiles across varying conifer species in dense stands?
- What are the optimal spatial distance and energy difference thresholds for merging overlapping tree crowns in dense conifer stands during soft clustering?
- Can deep learning-based multi-layer detection (such as DEIMv2) resolve the crown clumping and undersegmentation issues identified in closed-canopy forests?
- How does the computational complexity of 3D mean-shift clustering scale on high-density drone photogrammetric point clouds in dense stands?
- Can point-prompted SAM mask proposals effectively resolve under-segmentation in extremely dense, multi-layered conifer stands without high-resolution CHM inputs?
- How does the boundary delineation accuracy of box-prompted SAM2 scale in extremely dense conifer stands compared to specialized instance segmentation models like EdgeCrafter ECSeg?