---
title: "Tree crown segmentation in three dimensions using density models derived from airborne laser scanning"
type: Source
tags: [itd, point-cloud, 3d-segmentation, template-matching, mean-shift, forestry]
status: stable
updated: 2026-08-21
description: "Introduces a 2D template-matching watershed segmentation followed by a 3D mean-shift clustering using empirical crown density models to detect understory trees."
source_file: raw/papers/Tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114.pdf
authors: [Johan Holmgren, Eva Lindberg, Kenneth Olofsson, Henrik J. Persson]
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114.pdf
    title: "Tree crown segmentation in three dimensions using density models derived from airborne laser scanning"
related_methods:
  - methods/chm-detection
  - methods/local-maxima
---

# Tree crown segmentation in three dimensions using density models derived from airborne laser scanning

## Summary

This paper presents a two-stage individual tree detection (ITD) and delineation framework designed to handle multi-layered forest canopies. Instead of relying purely on a 2D Canopy Height Model (CHM) surface, which often misses suppressed or understory trees, the authors propose using empirical **3D tree crown density models** (templates) trained on manually delineated trees. 

The first stage performs a **2D segmentation** by generating a Model Fit (MF) surface using the Bhattacharyya coefficient to match local point cloud distributions against the templates, followed by a watershed segmentation. The second stage performs a **3D segmentation** within each 2D segment using a modified **mean-shift clustering** algorithm. This 3D search tracks "model fit strings" vertically to identify local maxima of model fits, successfully isolating sub-canopy trees. The method was validated in a Swedish hemiboreal forest using high-altitude ALS (22 pulses/m²) and low-altitude helicopter ALS (2511 pulses/m²).

## Key claims

- **Significant Understory Detection Improvements**: Combining 2D segmentation with 3D clustering increased the tree detection rate from **87% to 92%** for high-altitude ALS, and from **91% to 99%** for low-altitude ALS (page 299).
- **Volume Representation**: Undetected trees accounted for only **0–5% of the total stem volume** across all plots, meaning almost all dominant and co-dominant timber volume was successfully mapped (page 299).
- **Resolution vs. Algorithm**: High-resolution, low-altitude ALS is primarily beneficial for detecting small, suppressed trees in lower vegetation layers, whereas high-altitude ALS is sufficient for capturing dominant canopy layers (page 326).
- **Scale Parameter Solution**: Using empirical templates scaled dynamically by tree height ($h_{max}$) resolves the traditional scale-selection problem associated with CHM smoothing filters (page 307).

## Implications for our pipeline

- **Hybrid 2D/3D Processing**: Our current [[project/pipeline-overview]] relies on 2D local maxima and [[methods/chm-detection]] combined with [[methods/deimv2-canopy]]. Integrating a 3D density-based template matching step could significantly improve detection in multi-layered conifer stands.
- **Template-Based Local Maxima**: Instead of running a simple sliding window on the raw CHM, we could generate a "Model Fit Surface" (MFS) using our target species' structural profiles (e.g., Scots Pine, Norway Spruce) to suppress false maxima from branch structures.
- **Voxelization for Performance**: For ultra-high-density drone orthophotos or photogrammetric point clouds, voxel downsampling (e.g., 0.1m to 0.2m) is critical before running iterative clustering algorithms like mean-shift to maintain operational efficiency (page 313).

## Replication pseudocode

### Prerequisites

- Normalized 3D point cloud $(x, y, z)$ where $z$ is height above ground.
- A Canopy Height Model (CHM) raster (0.25 m resolution).
- Pre-trained 2D crown density templates for target species classes (Pine, Spruce, Deciduous) represented as radially symmetric relative height-radius probability matrices.

### Procedure

```text
1. LOAD normalized point cloud and CHM.
2. For each cell (X_c, Y_c) in the CHM:
    a. Get local height h_max from CHM.
    b. Extract local point cloud within search radius (scaled by h_max).
    c. Project local points to relative radial distance (r_p) and relative height (h_p).
    d. Compute local density distribution q(y_ij).
    e. For each species template p(x_ij):
        i. Calculate Bhattacharyya coefficient B = sum(sqrt(p(x_ij) * q(y_ij))).
    f. Assign the maximum B value across templates to the Model Fit Surface (MFS) at (X_c, Y_c).
3. SMOOTH MFS using a recursive 3x3 Gaussian filter (3 passes).
4. RUN watershed segmentation on smoothed MFS to obtain Initial 2D Segments.
5. For each cell (X_c, Y_c):
    a. Re-calculate B, but restrict the local point cloud extraction to points belonging 
       to the cell's Initial 2D Segment.
    b. Save maximum B to Constrained Model Fit (CMF) surface.
6. RUN watershed segmentation on smoothed CMF to obtain Final 2D Segments.
7. For each Final 2D Segment (to extract sub-canopy trees):
    a. Initialize mean-shift paths from all 3D points in the segment.
    b. Shift points in the 2D plane using the template density as a kernel until convergence 
       to form vertical "Model Fit (MF) strings".
    c. Run 3D mean-shift clustering along the MF strings using a 3D kernel weighted by:
       Weight = B_value * Gaussian(horizontal_dist, sigma_r) * Gaussian(vertical_dist, sigma_z)
       where sigma scales dynamically with height z.
    d. Group converged endpoints within 0.3m to define final 3D tree clusters.
```

### Gaps / not specified in paper

- **Species-Specific Template Selection**: The paper does not detail how to automatically assign a single species classification to the final 3D cluster when multiple templates yield high $B$ values during the mean-shift phase.
- **Computational Complexity**: The exact execution time for the 3D mean-shift clustering on large-area point clouds is not specified, though voxelization is noted as a necessary mitigation (page 313).

## Quotes

> "When applying 3D segmentation as well, the algorithm detected 92% of the trees measured in the field using high-altitude ALS data; the detection rate increased to 99% using low-altitude ALS data." (page 299)

> "These crown density models are more robust compared to algorithms based only on canopy height surface models, since laser returns within a tree crown no longer appear as noise, but contribute to the density model." (page 307)

> "The 3D tree crown segmentation, which was using crown density models, made it possible to detect a large percentage of trees in multi-layered forests, compared with using only a 2D segmentation method." (page 299)

## Related pages

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
- [[methods/local-maxima]]
- [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data]] (Li, 2025) — Another hybrid approach combining CHM region-growing with vertical profile morphology.
