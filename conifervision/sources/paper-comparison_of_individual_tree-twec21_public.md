---
type: Source
title: "Comparison of individual tree detection methods"
description: "A comparative study of local maxima, trunk detection, and point density methods for individual tree detection using high-density UAV laser scanning."
tags: [itd, local-maxima, trunk-detection, point-density, uav-lidar]
status: stable
updated: 2026-08-21
source_file: raw/papers/Comparison_of_individual_tree-twec21_public.pdf
authors: [Aino Weckman]
year: 2021
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Comparison_of_individual_tree-twec21_public.pdf
    title: "Comparison of individual tree detection methods"
---

# Comparison of individual tree detection methods

## Summary

This thesis compares three individual tree detection (ITD) methods applied to high-density airborne laser scanning (ALS) point cloud data ($140\text{ pts/m}^2$) collected via a helicopter-borne UAV system in Evo, Finland. The three evaluated methods are:
1. **Local Maxima Method**: A raster-based Canopy Height Model (CHM) approach utilizing minimum curvature-based region detection and Gaussian smoothing.
2. **Trunk Detection Method**: A point-cloud-based approach that identifies vertical elongated structures using local linearity and verticality thresholds.
3. **Point Density Method**: A grid-based approach assuming higher laser return density on tree trunks, smoothed with a Gaussian filter to locate local maxima.

The local maxima method achieved the best overall performance, particularly for larger trees (diameter at breast height $\text{DBH} > 20\text{ cm}$), while the trunk detection method demonstrated the highest correctness (least commission errors/false positives) but suffered from low completeness.

## Key claims

* **Local Maxima Performance**: Achieved the highest overall F-score ($0.5861$) and completeness ($0.5740$). It successfully detected over $90\%$ of trees with $\text{DBH} > 20\text{ cm}$ ($91.94\%$ for $20\text{-}40\text{ cm}$ and $95.97\%$ for $> 40\text{ cm}$) (p. 11-12).
* **Trunk Detection Precision**: Achieved a correctness of $0.9658$, indicating almost no false positives ("made-up trees"), but had a very low completeness of $0.1700$ (p. 12).
* **Point Density DBH-Invariance**: Unlike the other two methods, the point density method's performance was relatively uniform across different tree sizes, detecting small trees ($5\text{-}20\text{ cm}$ DBH) at $31.18\%$ and large trees ($> 40\text{ cm}$ DBH) at $34.88\%$ (p. 12).
* **Methodology over Point Density**: In ITD, the accuracy of the inventory depends more on the chosen detection algorithm than on increasing the point density of the laser scanning data (p. 6).

## Implications for our pipeline

* **Hybrid Detection Potential**: The paper suggests that combining local maxima (which excels at dominant canopy trees) with point density or trunk detection (which can identify suppressed or intermediate trees via trunk returns) could improve overall detection rates (p. 12). This supports our multi-layered detection strategy in [[project/pipeline-overview]].
* **Validation of Local Maxima**: Confirms that local maxima on smoothed CHMs remains the most robust baseline for dominant canopy layers, matching our implementation in [[methods/local-maxima]].
* **Trunk Detection Constraints**: While highly precise, direct trunk detection from point clouds is highly dependent on trunk visibility (e.g., Scots pines with fewer low branches) and requires extremely high point densities to achieve viable completeness (p. 10, 12).

## Replication pseudocode

### Prerequisites

* Normalized ALS point cloud (ground points removed/normalized to DTM).
* MATLAB environment with spatial processing toolboxes.
* `edgesKNNgraph.m` dependency for the Trunk Detection method.

### Procedure

```text
================================================================================
METHOD 1: LOCAL MAXIMA (Yu et al. 2011)
================================================================================
1. Rasterize normalized point cloud to construct Canopy Height Model (CHM).
2. Apply Gaussian smoothing filter to CHM to reduce micro-variations.
3. For each raster cell, calculate the minimum curvature (principal curvature measuring surface bending).
4. Contrast-stretch the CHM based on the calculated minimum curvature values.
5. Perform a local maxima search on the scaled image to identify treetops.

================================================================================
METHOD 2: TRUNK DETECTION (Lehtomäki)
================================================================================
1. For each point in the normalized point cloud:
    a. Calculate local linearity and verticality metrics using its k-nearest neighbors (KNN).
2. Filter points where:
    linearity > threshold_linearity AND verticality > threshold_verticality
3. Cluster the remaining "trunk points" using a spatial distance threshold (small horizontal distance).
4. Compute the centroid of each cluster to define individual tree coordinates.

================================================================================
METHOD 3: POINT DENSITY (Soininen)
================================================================================
1. Project normalized point cloud onto a 2D horizontal grid.
2. For each grid cell, count the number of laser returns (point density).
3. Smooth the 2D density grid using a Gaussian filter.
4. Detect local maxima within the smoothed density grid.
5. Map each local maximum to the coordinates of the highest raw point within that grid cell.
```

### Gaps / not specified in paper

* **Threshold Values**: The exact threshold values for linearity and verticality in the trunk detection method are not specified (TBD).
* **Filter Parameters**: The standard deviation ($\sigma$) and window size for the Gaussian filters used in both the local maxima and point density methods are not detailed (TBD).
* **Grid Resolutions**: The spatial resolution (pixel size) of the grids for the local maxima and point density methods is not explicitly defined for the Evo dataset, though a historical $0.5\text{ m}$ grid is referenced (p. 7, 10).

## Quotes

* "When ITD is done by using laser scanning data, the accuracy depends more on the ITD method than the point density of the data." (p. 6)
* "The trunk detection method was the most accurate. It got correctness value of over 0.95, so it gave almost no made-up trees as output." (p. 12)
* "Therefore, combination of local maxima method and density method might lead to better results." (p. 12)

## Related pages

* [[methods/local-maxima]] — Production implementation of local maxima windowing.
* [[concepts/canopy-height-model]] — Canopy Height Model generation and smoothing.
* [[sources/popescu-wynne-2004-seeing-the-trees]] — Historical context on variable-window local maxima.
* [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020]] — Alternative point cloud segmentation using watershed and K-means.
