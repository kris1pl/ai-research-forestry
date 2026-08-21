---
title: "Self-Supervised Learning for Precise Individual Tree Segmentation in Airborne LiDAR Point Clouds"
type: Source
tags: [lidar, self-supervised-learning, individual-tree-detection, point-cloud, clustering]
status: stable
updated: 2026-08-21
description: "A self-supervised learning framework for label-free individual tree segmentation in LiDAR point clouds using transformation-invariant pretext tasks and energy-based soft clustering."
source_file: raw/papers/Self-Supervised_Learning_for_Precise_Individual_Tree_Segmentation_in_Airborne_LiDAR_Point_Clouds.pdf
authors: [Lama Shaheen, Bader Rasheed, Manuel Mazzara]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Self-Supervised_Learning_for_Precise_Individual_Tree_Segmentation_in_Airborne_LiDAR_Point_Clouds.pdf
    title: "Self-Supervised Learning for Precise Individual Tree Segmentation in Airborne LiDAR Point Clouds"
---

# Self-Supervised Learning for Precise Individual Tree Segmentation in Airborne LiDAR Point Clouds

## Summary

This paper introduces a novel self-supervised learning (SSL) framework designed to segment individual trees directly from 3D airborne LiDAR point clouds without requiring manual annotations. The framework operates in two distinct stages:
1. **Pretext Task:** A PointNet-inspired shape-aware neural network is trained to predict geometric transformations (rotation, translation, and scaling) applied to unlabeled point cloud chunks. This forces the network to learn robust, transformation-invariant local and global features.
2. **Main Segmentation Task:** An unsupervised segmentation step leverages a custom energy function combining height, density, and slope attributes to guide an adaptive soft clustering mechanism. Centroids are initialized at high-energy points (treetops) and dynamically merged, pruned, or refined in the learned feature space.

The method was validated on high-density Estonian Land Board LiDAR data (LAS 1.4, 2.5 cm point spacing) across dense, mixed, and scattered forest environments, demonstrating high geometric fidelity (up to 83% convexity and 78% solidity in dense canopies) and a significant reduction in over-segmentation compared to traditional hard-clustering baselines.

## Key claims

* **Label-Free Feature Learning:** The pretext task successfully forces the model to learn robust, scale-invariant, and rotation-invariant representations of tree structures without manual labels, achieving a Mean Squared Error (MSE) of 0.037 for rotations, 0.0011 for translations, and 0.0131 for scaling (p. 70903).
* **Energy-Based Structural Representation:** Combining height, density, and slope into a unified energy function effectively models tree geometry, mapping treetops to high-energy zones and boundaries to low-energy zones (p. 70899-70900).
* **Soft Clustering Superiority:** Probabilistic soft clustering handles overlapping canopies and boundary ambiguities far better than hard-boundary algorithms like DBSCAN or K-means, significantly reducing over-segmentation (p. 70901, 70905).
* **High Geometric Fidelity:** The segmented tree crowns closely match natural geometries, achieving up to 83% convexity, 78% solidity, and an elliptical fit error as low as 0.30 in dense forest environments (p. 70904).

## Implications for our pipeline

* **Potential 3D Upgrade Path:** Our current [[project/pipeline-overview]] relies on 2D Canopy Height Models (CHMs) and 2D object detection via [[methods/deimv2-canopy]]. This paper provides a viable, unsupervised methodology to process raw 3D LiDAR point clouds directly, preserving vertical structural details that are lost during rasterization.
* **Unsupervised Pretraining:** The pretext task of predicting rotation, translation, and scaling could be used to pretrain 3D feature extractors on our unlabeled regional LiDAR datasets before fine-tuning them for downstream tasks.
* **Treetop Detection Refinement:** The energy function (combining height, density, and slope) could serve as an alternative or refinement to our current [[methods/local-maxima]] sliding window approach on CHMs, especially in dense or structurally complex conifer stands.
* **High Computational Overhead:** The reported processing times (e.g., 116.68 minutes for dense forest and 142.60 minutes for mixed forest on a laptop GPU) indicate that this method is currently too slow for real-time or large-scale operational deployment in our production pipeline without heavy optimization (p. 70904).

## Replication pseudocode

### Prerequisites

* Python 3.11, PyTorch, Laspy, and Open3D (or similar point cloud processing library).
* Unlabeled airborne LiDAR point cloud data in `.las` format.
* Statistical Outlier Removal (SOR) and PCA normal estimation tools.

### Procedure

```text
1. PREPROCESSING
   a. Apply Statistical Outlier Removal (SOR) filter:
      - For each point, compute mean distance to k-nearest neighbors.
      - Remove points with mean distance > (global_mean + 2 * std_dev).
   b. Apply Morphological Filtering:
      - Estimate local surface normals using PCA.
      - Remove points with abnormal normal deviations (e.g., power lines, isolated noise).
   c. Normalize coordinates to a unit cube [0, 1] using bounding box min/max.
   d. Divide the point cloud into non-overlapping spatial chunks along the X-Y plane.

2. PRETEXT TASK (Self-Supervised Feature Learning)
   a. For each point cloud chunk:
      - Apply random rotation Rz(theta) where theta is in [-45°, +45°].
      - Apply random translation T in [-1, 1] units along each axis.
      - Apply random scaling factor s in [0.5, 2.0].
   b. Pass the transformed chunk through a PointNet-inspired architecture:
      - Extract local features via shared MLPs.
      - Aggregate global features via symmetric max-pooling.
      - Concatenate local, global, and raw geometric features (height, density) into an augmented feature vector.
   c. Train the network to predict the applied transformation parameters (theta, T, s) using MSE Loss.
   d. Freeze the trained feature extractor weights.

3. ENERGY FUNCTION COMPUTATION
   For each point pi:
   a. Compute Height Energy: E_height(pi) = Sigmoid((zi - mean_z) / std_z)
   b. Compute Density Energy:
      - Calculate local density rho_i using a Gaussian kernel over k-neighbors.
      - Normalize density: E_density(pi) = exp(rho_i) / sum(exp(rho_k))
   c. Compute Slope Energy:
      - Calculate local slope s_i based on height differences to neighbors.
      - E_slope(pi) = exp(-s_i / sigma_s)
   d. Compute Combined Energy: E(pi) = (wh*E_height + wd*E_density + ws*E_slope) / (wh + wd + ws)

4. UNSUPERVISED SEGMENTATION LOSS TRAINING
   Train the segmentation network using the frozen feature extractor and the combined loss:
   L_total = lambda1 * L_intra + lambda2 * L_inter + lambda3 * L_slope
   - L_intra: Pulls points with similar energy values closer in feature space.
   - L_inter: Pushes points with dissimilar energy values apart.
   - L_slope: Guides points with steep slopes toward identified treetop points.

5. ADAPTIVE SOFT CLUSTERING
   a. Initialize Centroids:
      - Select high-energy points as initial centroids, enforcing a minimum spatial distance (d_min) between them.
   b. Soft Assignment:
      - Compute probabilistic membership of each point to each centroid using a softmax over feature-space distances.
   c. Adaptive Management:
      - Merge Centroids: If spatial distance < epsilon and energy difference < delta.
      - Prune Centroids: If total membership sum < T_min (spurious clusters).
      - Refine Centroids: Recalculate centroid positions as the weighted average of assigned points.
   d. Iterate until centroid positions stabilize.
```

### Gaps / not specified in paper

* **Hyperparameter Values:** The exact weights for the combined energy function ($w_h, w_d, w_s$) and the loss function coefficients ($\lambda_1, \lambda_2, \lambda_3$) are described as requiring fine-tuning but their optimal values are not explicitly specified (p. 70900, 70906).
* **Thresholds for Clustering:** The specific values for the spatial distance threshold ($\epsilon$), energy difference threshold ($\delta$), and minimum cluster size ($T_{min}$) used in the adaptive cluster management phase are left as TBD (p. 70902).
* **Neighborhood Size ($k$):** The exact number of nearest neighbors ($k$) used for the SOR filter, PCA normal estimation, and density calculations is not explicitly defined.

## Quotes

* "The framework operates in two stages: a pretext task applies geometric transformations—rotation (from –45° to +45°), translation (between –1 and 1 units), and scaling (between 0.5 and 2.0)—to learn robust features, while an unsupervised segmentation step leverages an energy function that combines height, density, and slope attributes to cluster points corresponding to individual trees." (p. 70895)
* "Unlike hard clustering techniques, which assign each point to a single cluster, soft clustering enables points to have varying degrees of membership across different clusters. This flexibility is crucial for handling the natural variability in tree shapes and sizes, as well as managing points that lie near the boundaries between trees." (p. 70901)
* "While the reported processing times are high, they are reasonable given the complex nature of the segmentation task, the variability in point cloud density, and the current hardware configuration." (p. 70905)

## Related pages

* [[concepts/canopy-height-model]] — The 2D raster equivalent of the 3D structural data processed here.
* [[methods/local-maxima]] — Traditional local maxima detection, which is conceptually similar to the high-energy treetop initialization.
* [[methods/chm-detection]] — Our current production approach for tree detection.
* [[sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660]] — Another unsupervised deep learning approach for LiDAR point cloud preprocessing.
