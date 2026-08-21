---
type: Source
title: "Individual Tree Segmentation Based on Region-Growing and Density-Guided Canopy 3-D Morphology Detection Using UAV LiDAR Data"
description: "A hybrid individual tree segmentation method combining CHM region-growing with point cloud density-guided vertical profile morphology analysis."
tags: [lidar, tree-detection, chm, point-cloud, region-growing]
status: stable
updated: 2026-08-21
source_file: raw/papers/Individual_Tree_Segmentation_Based_on_Region-Growing_and_Density-Guided_Canopy_3-D_Morphology_Detection_Using_UAV_LiDAR_Data.pdf
authors: [Shihua Li, Shunda Zhao, Zhilin Tian, Hao Tang, Zhonghua Su]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Individual_Tree_Segmentation_Based_on_Region-Growing_and_Density-Guided_Canopy_3-D_Morphology_Detection_Using_UAV_LiDAR_Data.pdf
    title: "Individual Tree Segmentation Based on Region-Growing and Density-Guided Canopy 3-D Morphology Detection Using UAV LiDAR Data"
related_methods:
  - methods/chm-detection
  - methods/local-maxima
---

# Individual Tree Segmentation Based on Region-Growing and Density-Guided Canopy 3-D Morphology Detection Using UAV LiDAR Data

## Summary

This paper introduces a hybrid individual tree detection (ITD) and segmentation framework (referred to as **RDT**) that bridges the gap between computationally efficient raster-based methods and highly accurate point-based methods. 

The workflow begins with a coarse segmentation of a Canopy Height Model ([[concepts/canopy-height-model|CHM]]) using a modified region-growing algorithm. It then projects the normalized point cloud to construct a Point Density Model (PDM). By analyzing the number of local density maxima within each coarse segment, the algorithm classifies segments as correct, oversegmented, or undersegmented. Erroneous segments are corrected using 3-D morphological analysis along vertical profiles guided by the density maxima, followed by a final region-growing step using the refined tree tops as seeds.

The method was validated on six temperate forest plots in Germany (from the Weiser et al. 2025 dataset), achieving an average F1-score of 0.95, outperforming traditional watershed and point-clustering baselines.

## Key claims

- **Density-Guided Error Classification**: Point cloud density features (PDM) can reliably identify undersegmentation and oversegmentation within coarse CHM-derived segments without complex manual heuristics (p. 8898).
- **Vertical Profile 3-D Morphology**: Undersegmented clusters can be resolved by extracting a narrow vertical slice (0.2 m buffer) between the reference top and potential tops, fitting a polynomial curve to the canopy surface, and finding the local height minimum (boundary point) (p. 8902).
- **Parameter Insensitivity**: The final F1-score of the RDT method is highly stable across different CHM local height maximum filter window sizes, though it is moderately sensitive to the PDM local density maximum filter window size (p. 8907).
- **Computational Efficiency**: By performing point-cloud operations only on identified erroneous segments (and avoiding global point-cloud clustering), the algorithm runs in a few seconds when point cloud storage overhead is excluded (p. 8905).

## Implications for our pipeline

- **Refining [[methods/chm-detection|CHM-detection]]**: Our current pipeline merges local maxima and DEIMv2 detections. Incorporating a Point Density Model (PDM) alongside the CHM could help us flag and split undersegmented canopy clusters (e.g., closely spaced codominant conifers) before species classification.
- **Splitting Overlapping Crowns**: The 3-D vertical profile polynomial fitting technique offers a geometric alternative to deep-learning-based instance segmentation for separating overlapping tree crowns.
- **Preprocessing Constraints**: The method relies on high-density UAV LiDAR (ranging from 18 to 125 pts/m² in the study). Its performance on lower-density ALS or photogrammetric point clouds (SFM) remains TBD.

## Replication pseudocode

### Prerequisites

- Normalized point cloud (Z coordinates represent height above ground, e.g., via CSF filtering).
- Smoothed Canopy Height Model (CHM) at 0.5 m resolution.
- Smoothed Point Density Model (PDM) at 0.5 m resolution (grid cell values = count of projected points).

### Procedure

```text
1. COARSE SEGMENTATION (CHM Region-Growing):
   a. Detect initial seeds using a local maximum filter on CHM (window size = 5 pixels).
   b. Grow regions using a circular-like kernel. A neighbor pixel belongs to the crown if:
      - Neighbor height > seed height * 0.6 AND neighbor height < seed height * 1.05
      - Neighbor height > mean height of current crown * 0.6
      - Maximum crown radius <= 10 m
   c. Output: Coarse crown polygons and a list of initial tree tops.

2. ERROR CLASSIFICATION (PDM Local Maxima):
   a. Detect local density maximum points on the PDM using a sliding window (size = 4 to 10 pixels).
   b. For each coarse crown segment:
      - Count the number of local density maxima falling within its boundary.
      - If count == 1: Classify as CORRECT.
      - If count == 0: Classify as OVERSEGMENTED.
      - If count >= 2: Classify as UNDERSEGMENTED.

3. OVERSEGMENTATION CORRECTION:
   a. For each oversegmented cluster:
      - Project points onto the 2D plane and compute the covariance matrix.
      - Perform Singular Value Decomposition (SVD) to find major and minor axes.
      - If major_axis / minor_axis > 3.0:
        - Reassign all points in this cluster to the nearest valid tree crown.
        - Remove the redundant seed from the tree top list.

4. UNDERSEGMENTATION CORRECTION (3-D Morphology):
   a. For each undersegmented cluster with multiple density maxima:
      - Identify the highest point within a 0.5 m radius of each density maximum.
      - Define a vertical profile plane passing through the primary tree top and the secondary density maximum.
      - Project points within 0.2 m of this plane onto the profile.
      - Fit an n-degree polynomial curve (e.g., n=4) to the upper surface points of the profile.
      - Find the boundary point (local minimum of the fitted curve where p'(x) = 0 and p''(x) > 0).
      - Apply geometric rules to filter out branches:
        - If height difference between tops < 1 m AND (planar distance < 2 m OR distance ratio to boundary > 1.5):
          - Reject secondary top (classify as branch).
        - Else if boundary height < height of the shorter top:
          - Accept secondary top as a valid tree top and add to the seed list.

5. FINE SEGMENTATION:
   a. Re-run the region-growing algorithm using the updated, refined seed list to generate final individual tree crowns.
```

### Gaps / not specified in paper

- **Polynomial Degree ($n$)**: The paper defines the polynomial fitting function $p(x)$ but does not explicitly specify the optimal degree $n$ used in their experiments (p. 8902).
- **Surface Point Extraction Interval**: The exact interval used to extract "surface points" from the vertical profile before curve fitting is not specified (p. 8902).
- **Adaptive Window Selection**: The paper notes that automatically determining the optimal PDM window size for different forest structures is a task left for future work (p. 8908).

## Quotes

> "First, based on CHM-based segmentation, the point cloud density feature is introduced to identify the wrong segmented trees. Next, the height and density information are combined to guide the selection of vertical profiles." (p. 8897)

> "From Fig. 4, it can be found that for trees with regular shapes, the positions of their local maximum density and local maximum height in the horizontal direction nearly coincide." (p. 8901)

> "The results indicated that the average F1-scores of six study plots were 0.95, which improved by 5% after the introduction of density information." (p. 8897)

## Related pages

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
- [[methods/local-maxima]]
- [[sources/paper-comparison_of_individual_tree-twec21_public]] (Weckman 2021)
- [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]] (Sparks 2022)
