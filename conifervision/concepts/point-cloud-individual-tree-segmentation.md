---
title: "Point Cloud Individual Tree Segmentation"
type: Concept
description: "Existing concept canopy-height-model and literature-map-dense-itd focus on raster CHMs or dense 2D imagery, leaving direct 3D point cloud clustering and bottom-up tree instance segmentation unrepresented."
tags: [point, cloud, individual, tree, segmentation]
status: draft
updated: 2026-10-23
generated:
  by: agent:concept-gate
  at: 2026-10-23T11:37:49Z
sources:
  - sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main
  - sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1
  - sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds
---

# Point Cloud Individual Tree Segmentation

Existing concept canopy-height-model and literature-map-dense-itd focus on raster CHMs or dense 2D imagery, leaving direct 3D point cloud clustering and bottom-up tree instance segmentation unrepresented.

This page names the shared idea. It does not open an experiment folder. [[project/domains]] does not gain a new program from this page.

```mermaid
flowchart LR
  sources["Source pages"] --> concept["This concept"]
```

## What the sources describe

- [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]] — A bottom-up oriented search and clustering method that groups ALS point clouds upward to local tops, optimizing sub-canopy tree detection.
- [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1]] — An end-to-end transformer-based 3D instance and semantic segmentation framework for forest LiDAR point clouds using ISA-guided query selection, score-based block merging, and one-to-many association.
- [[sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds]] — A self-supervised learning framework for label-free individual tree segmentation in LiDAR point clouds using transformation-invariant pretext tasks and energy-based soft clustering.

Stand dominant height, site index, and stand volume stay on [[concepts/site-index-and-yield]].

## Replication notes

Coefficients stay on the source pages. Nothing here is implemented in the detection pipeline.

| Paper | Our status |
|---|---|
| [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]] — A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds | TBD |
| [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1]] — ForestFormer3D: A Unified Framework for End-to-End Segmentation of Forest LiDAR 3D Point Clouds | TBD |
| [[sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds]] — Self-Supervised Learning for Precise Individual Tree Segmentation in Airborne LiDAR Point Clouds | TBD |

## Related

- [[concepts/site-index-and-yield]] — stand site index and stand volume
- [[concepts/crown-ownership]] — a crown box is not yet a measured crown width
- [[concepts/canopy-height-model]] — tree height read from the canopy surface
- [[project/domains]] — allometry program not started
