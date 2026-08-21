---
type: Source
title: "Canopy LiDAR Point Cloud Data K-Means Clustering Watershed Segmentation Method"
description: "An improved watershed segmentation method utilizing K-means clustering initialized by variable-window local maxima on a Canopy Maximum Model (CMM) to mitigate over-segmentation."
tags: [chm, watershed, k-means, local-maxima, lidar, segmentation]
status: stable
updated: 2026-08-21
source_file: raw/papers/CANOPY_LIDAR_POINT_CLOUD_DATA_K-MEANS_CLUSTERING_WATERSHED_SEGMENTATION_METHOD-isprs-annals-VI-3-W1-2020-67-2020.pdf
authors: [Y. Mu, G. Zhou, H. Wang]
year: 2020
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/CANOPY_LIDAR_POINT_CLOUD_DATA_K-MEANS_CLUSTERING_WATERSHED_SEGMENTATION_METHOD-isprs-annals-VI-3-W1-2020-67-2020.pdf
    title: "Canopy LiDAR Point Cloud Data K-Means Clustering Watershed Segmentation Method"
---

# Canopy LiDAR Point Cloud Data K-Means Clustering Watershed Segmentation Method

## Summary

This paper introduces an improved watershed segmentation algorithm designed to address the over-segmentation issues common in traditional watershed-based individual tree crown delineation. The method integrates a Canopy Height Model (CHM) optimized into a Canopy Maximum Model (CMM), variable-window local maxima detection for treetop seeding, $K$-means clustering for initial coarse segmentation, and a neighborhood-similarity-based region merging step to refine the final tree crown boundaries. Tested on a 760 m² plot in the Saihanba forest area (Hebei Province, China) containing 175 pine trees, the method achieved an F-score of 0.90, outperforming traditional watershed segmentation.

## Key claims

*   **Over-Segmentation Mitigation**: Traditional watershed algorithms are highly sensitive to noise and local height variations, leading to over-segmentation. Combining $K$-means clustering with a neighborhood similarity-based merging step significantly mitigates this issue (p. 68).
*   **CMM vs. CHM**: Generating a Canopy Maximum Model (CMM) via morphological "opening" (erosion followed by dilation) on the CHM eliminates false treetops and reduces missing treetops (p. 70).
*   **Accuracy Improvements**: The proposed algorithm improved the Recall ($R$) by 11% (from 0.85 to 0.91), Precision ($P$) by 9.8% (from 0.80 to 0.89), and the overall F-score by 7.1% (from 0.82 to 0.90) compared to traditional watershed segmentation (p. 71).

## Implications for our pipeline

*   **CMM Smoothing**: Our [[methods/chm-detection]] pipeline could benefit from implementing the morphological "opening" operation to convert standard CHMs into Canopy Maximum Models (CMMs) before running local maxima detection.
*   **Seeded K-Means for Crown Delineation**: Instead of relying solely on watershed or region growing directly on the CHM, we can evaluate using the detected [[methods/local-maxima]] as initial cluster centers ($K$ seeds) for a $K$-means spatial-spectral clustering step.
*   **Adjacency-Based Merging**: The 4-neighborhood similarity metric ($C_{ij}$) based on standard deviation and variance between adjacent segments offers a mathematical framework to merge over-segmented canopy fragments in [[methods/merge-detections]].

## Replication pseudocode

### Prerequisites

*   Airborne LiDAR point cloud or high-resolution Canopy Height Model (CHM).
*   Morphological processing library (e.g., OpenCV or SciPy Multidimensional Image Processing).
*   $K$-means clustering implementation.

### Procedure

```text
1. POINT CLOUD FILTERING
   - Apply a radius filter to the raw point cloud.
   - Draw a circle of radius R = 15m around each point.
   - If the number of points within the radius is less than a threshold, delete the point as noise.

2. CANOPY HEIGHT MODEL (CHM) TO CANOPY MAXIMUM MODEL (CMM)
   - Interpolate filtered point cloud to generate a raw CHM.
   - Apply morphological "opening" (erosion followed by dilation) to smooth boundaries and remove small noise.
   - Compute CMM for each pixel (x, y) using a 3x3 neighborhood:
     CMM(x, y) = max( CHM(i, j) ) for (i, j) in 3x3 window around (x, y)

3. VARIABLE WINDOW TREETOP DETECTION
   - For each pixel, calculate the variable window size based on estimated tree height (TH) and crown diameter (TC):
     Window_Size = 29.77 - 1.46 * TC + 0.03 * TH^2
   - Detect local maxima within the variable window on the CMM to obtain K treetop coordinates.
   - Apply Gaussian filtering to smooth the CMM (generating GCMM) to suppress insignificant local maxima:
     GCMM = Gaussian_Filter(CMM, sigma)

4. K-MEANS COARSE SEGMENTATION
   - Initialize K cluster centers (m_1, m_2, ..., m_k) using the coordinates of the K detected treetops.
   - Run K-means clustering on the GCMM gray-scale values to partition the image into K regions.
   - Extract the maximum connected component for each cluster using 4-neighborhood connectivity.

5. IMPROVED WATERSHED & REGION MERGING
   - For each segmented block S_i, calculate its gray value variance (M_i^2).
   - For adjacent blocks S_i and S_j:
     a. Calculate variance difference: M_ij^2 = (M_i - M_j)^2
     b. Identify N_ij edge pixels satisfying 4-neighborhood relationships between S_i and S_j.
     c. Calculate the mean standard deviation of edge pixels:
        P_ij = (1 / N_ij) * Sum( sqrt( (I(x_i, y_i) - I(x_j, y_j))^2 ) )
     d. Define similarity: C_ij = M_ij^2 - P_ij
   - Determine optimal threshold T using Otsu's method (maximizing between-class variance).
   - Merge adjacent blocks S_i and S_j if C_ij < T; otherwise, keep them separated.
```

### Gaps / not specified in paper

*   **TC and TH Estimation**: Equation 10 requires Crown Diameter ($TC$) and Tree Height ($TH$) to calculate the variable window size, but the paper does not explicitly detail how these are dynamically estimated per pixel prior to window calculation (it mentions manual measurement for validation, but implies a predictive formula is used for detection).
*   **Gaussian Sigma**: The standard deviation ($\sigma$) for the Gaussian filter applied to the CMM (Equation 12) is not specified.
*   **Radius Filter Threshold**: The exact point count threshold used in the 15m radius filter is omitted.

## Quotes

*   "Due to the over-segmentation phenomenon occurring in the traditional watershed single-wood segmentation, this paper presents a method, called $K-means$ clustering watershed for single tree segmentation." (p. 67)
*   "The experimental results demonstrate that the false treetops can be significantly eliminated, and the phenomenon of the missing treetops is largely reduced." (p. 70)
*   "Compared with the traditional watershed segmentation method, the improved watershed segmentation method combined with $K-means$ clustering has higher tree recognition rate and segmentation accuracy rate." (p. 71)

## Related pages

*   [[concepts/canopy-height-model]]
*   [[methods/local-maxima]]
*   [[methods/chm-detection]]
*   [[sources/popescu-wynne-2004-seeing-the-trees]] — Basis for the variable-window local maxima approach.
