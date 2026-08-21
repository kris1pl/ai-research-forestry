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
## Related

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
