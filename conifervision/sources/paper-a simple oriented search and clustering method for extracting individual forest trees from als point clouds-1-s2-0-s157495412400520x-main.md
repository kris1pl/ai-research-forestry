---
type: Source
title: "A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds"
description: "A bottom-up oriented search and clustering method that groups ALS point clouds upward to local tops, optimizing sub-canopy tree detection."
tags: [lidar, point-cloud, clustering, individual-tree-detection, understory]
status: stable
updated: 2026-06-09
source_file: raw/papers/A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds-1-s2.0-S157495412400520X-main.pdf
authors: [Wenhui Ding, Rong Huang, Wei Yao, Wuming Zhang, Marco Heurich, Xiaohua Tong]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-06-09T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds-1-s2.0-S157495412400520X-main.pdf
    title: "A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds"
related_methods:
  - methods/local-maxima
  - methods/chm-detection
---

# A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds

## Summary

This paper introduces a bottom-up point cloud clustering algorithm designed to extract individual trees from Airborne Laser Scanning (ALS) data, with a specific focus on multi-layered and deciduous forest structures. Inspired by the "bottom-to-top" growth characteristics of trees, the method bypasses traditional Canopy Height Model (CHM) limitations by operating directly on 3D coordinates. It iteratively searches for the highest point within a spherical neighborhood, moving upward until a local peak is found or an existing path is intersected. The algorithm incorporates a vertical point distribution analysis for adaptive understory shrub filtering, alongside a post-clustering validity check and point-updating mechanism to resolve branch over-segmentation.

## Key claims

- **Superior Sub-Canopy Detection**: On the NEWFOR benchmark, the method achieved matching rates ($RMS_{match}$) of 30% in the 2–5 m range, 31% in the 5–10 m range, and 55% in the 10–15 m range, outperforming traditional CHM-based and deep-learning-based detectors in the understory (p. 1, p. 13).
- **Reduced Computational Complexity**: Unlike Mean-Shift, the algorithm does not generate synthetic "process center points" or require a preset $k$-value like $K$-means, reducing computational overhead by shifting points directly to existing coordinates (p. 4).
- **Effective Post-Processing**: The validity checking and point-updating step reduced False Positives (FPs) to 0 on the CULS and SCION subsets of the FOR-instance dataset, boosting precision from 51% to 100% (p. 12).

## Implications for our pipeline

- **Enhancing [[methods/chm-detection]]**: Our current pipeline relies on 2D local maxima and CHM layers. Integrating this bottom-up 3D point clustering could significantly improve sub-canopy tree detection in multi-layered AREA units where high overstory canopies occlude lower layers.
- **Synergy with [[methods/deimv2-canopy]]**: While DEIMv2 handles horizontal layers, this oriented search can act as a geometric verification step to merge and validate multi-layer detections.
- **Pre-processing for [[concepts/pseudo-tree-crown]]**: The point-updating and cluster-cleaning steps provide highly clean 3D point clusters per tree, which can directly feed into pseudo-tree-crown generation pipelines for species classification.

## Replication pseudocode

### Prerequisites

- Normalized ALS point cloud (ground points removed via CSF, elevations normalized to DTM).
- KD-Tree structure for fast spherical neighborhood queries.

### Procedure

```text
1. ADAPTIVE HEIGHT FILTERING (SHRUB REMOVAL)
   a. Compute vertical point distribution histogram along the Z-axis.
   b. Smooth the distribution curve using a Gaussian function.
   c. Calculate the first derivative of the smoothed curve to find the first trough.
   d. Set the height threshold (H_thresh) to the Z-value of the first trough (capped at 3.0m).
   e. Filter out all points where Z < H_thresh.

2. ORIENTED SEARCH AND CLUSTERING
   Initialize all points as unclassified.
   For each unclassified point P_start:
       Initialize P_path = [P_start]
       P_center = P_start
       
       Loop:
           Find all points P_k within Neighbor_radius of P_center.
           Identify P_high = highest Z-coordinate point in P_k.
           
           If P_high == P_center (Treetop found):
               Create new class C_new.
               Assign all points in P_path to C_new.
               Break loop.
               
           Else if P_high is already classified into class C_existing:
               Assign all points in P_path to C_existing.
               Break loop.
               
           Else:
               Append P_center to P_path.
               Set P_center = P_high.

3. VALIDITY CHECKING AND POINT UPDATING
   For each raw cluster:
       Fit a 2D projection ellipse using least squares to get Area_cluster.
       Calculate Height = H_high - H_low.
       Check validity using dataset-specific thresholds (e.g., NEWFOR: Area > 5m² OR Height > 3m).
       If invalid:
           Mark cluster as invalid.
           
   For each point P in the dataset:
       If P belongs to an invalid class:
           Reassign P to the nearest valid class C_near(P) based on edge distance E_p_c.
       Else if P belongs to a valid class C_orig:
           Find nearest valid class C_near(P).
           If (E_p_c_orig - E_p_c_near > 1.0m) AND (H_p < H_cnear):
               Reassign P to C_near(P).
```

### Gaps / not specified in paper

- **Neighborhood Radius Selection**: The search radius parameter ($Neighbor\_radius$) is highly sensitive to forest density and must be manually tuned per plot (ranging from 1.0m to 3.0m, see Appendix Table 13). No automated method is provided for setting this radius dynamically.
- **Broadleaf Limitations**: The paper notes that the algorithm relies on local elevation maxima, making it less effective for broadleaf trees with wide, multi-peak crowns, which can lead to over-segmentation (p. 14).

## Quotes

> "Although the CHM-based method improves the processing efficiency, it is reliant on the accuracy of the CHM. Moreover, considering that the points in the middle and lower layers are barely utilized, the accuracy of detecting individual trees, especially for the sub-canopy and understory, is limited." (p. 2)

> "In the non-dominant layers of multi-layered forests, our method achieved $RMS_{match}$ values of 30% in the 2–5 m range, 31% in the 5–10 m range, and 55% in the 10–15 m range, demonstrating the best extraction performance." (p. 1)

## Related pages

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
- [[methods/local-maxima]]
- [[sources/popescu-wynne-2004-seeing-the-trees]]
