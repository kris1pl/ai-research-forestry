---
title: "LiDAR Point Cloud Denoising for Individual Tree Extraction Based on the Noise4Denoise"
type: Source
tags: [lidar, point-cloud, denoising, unsupervised-learning, individual-tree-detection]
status: stable
updated: 2026-08-21
description: "Introduces DEN4, an unsupervised deep learning-based point cloud denoising algorithm that improves individual tree segmentation accuracy by leveraging a multi-level noise separation module."
source_file: raw/papers/LiDAR_point_cloud_denoising_for_individual_tree_extraction_based_on_the_Noise4Denoise-fpls-15-1490660.pdf
authors: [Xiangfei Lu, Zongyu Ye, Liyong Fu, Huaiyi Wang, Kaiyu Wang, Yaquan Dou, Dongbo Xie, Xiaodi Zhao]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/LiDAR_point_cloud_denoising_for_individual_tree_extraction_based_on_the_Noise4Denoise-fpls-15-1490660.pdf
    title: "LiDAR point cloud denoising for individual tree extraction based on the Noise4Denoise"
related_methods:
  - methods/chm-detection
---

# LiDAR Point Cloud Denoising for Individual Tree Extraction Based on the Noise4Denoise

## Summary

This paper introduces **DEN4**, an unsupervised deep learning-based point cloud denoising algorithm designed specifically to improve individual tree segmentation in LiDAR point clouds. Built upon the principles of the *Noise4Denoise* framework, DEN4 uses a multi-level noise separation module to distinguish between signal and noise without requiring pre-labeled training data. 

The model was trained and evaluated on UAV LiDAR data collected from 17 forest plots in Qingyuan City, Guangdong Province (average point density of 110 pts/m²). DEN4 significantly outperforms traditional filtering methods—such as Morphological filtering, Progressive Triangulated Network Denoising (PTD), Statistical Outlier Removal (SOR), and Radius Outlier Removal (ROR)—across key metrics including Mean Squared Error (MSE), Signal-to-Noise Ratio (SNR), Hausdorff Distance, and Structural Similarity Index (SSIM).

## Key claims

* **Unsupervised Denoising without Labels:** DEN4 operates entirely without manual annotations or clean target point clouds, learning directly from noisy inputs by adding independent, identically distributed synthetic noise to construct a "double noise" prior.
* **Superior Metric Performance:** Across a 60-sample dataset, DEN4 achieved a mean MSE of 0.0094 (compared to ~0.0300 for traditional methods), a mean SNR of 149.1570 dB, a mean Hausdorff distance of 0.8503, and a mean SSIM of 0.8399.
* **Geometric and Structural Preservation:** The algorithm preserves critical individual tree metrics, such as canopy width, tree height, and diameter at breast height (DBH), avoiding the over-smoothing and detail loss common in traditional filters.
* **High Stability:** DEN4 demonstrated exceptional robustness across varying forest densities and rugged terrains, showing minimal metric variance (MSE standard deviation of 0.0008 and SNR standard deviation of 0.5628).

## Implications for our pipeline

* **Pre-processing Enhancement:** Integrating DEN4 into our [[project/pipeline-overview]] prior to generating the [[concepts/canopy-height-model]] (CHM) could significantly reduce canopy surface noise, leading to fewer false-positive local maxima detections.
* **Improved Tree Geometry:** By preserving canopy contours and trunk structures more accurately than standard filters, this method can improve downstream segmentation and feature extraction for species classification.
* **Unsupervised Training Feasibility:** Because the model is unsupervised, we can train and fine-tune it directly on our own unlabeled drone orthophoto/LiDAR datasets without manual labeling overhead.

## Replication pseudocode

### Prerequisites

* PyTorch, CUDA 12.5, and PyG (PyTorch Geometric) for graph convolutions.
* Open3D or CloudCompare for point cloud I/O and visualization.
* k-NN search implementation for local neighborhood extraction.

### Procedure

```text
1. Load raw noisy point cloud P_noisy with n points.
2. Normalize coordinates of P_noisy to stabilize training.
3. Generate synthetic noise M (independent and identically distributed to estimated noise N).
4. Construct double-noise point cloud P_double = P_noisy + M.
5. Define Encoder-Decoder Network (Architecture: 3 -> 256 -> 512 -> 1024 -> 2048):
   - Extract local features using k-NN neighborhood grouping and Graph Convolutions (DGCNN style).
   - Aggregate global features using global pooling.
   - Predict displacement vectors d_0 using an MLP with residual connections.
6. Train the network unsupervised for 200 epochs using Cosine Annealing (LR: 0.1 to 0.0001):
   - Predict displacement d_0 for P_double.
   - Calculate L_mse = || d_0 - 2 * (P_noisy - P_double) ||^2
   - Define pseudo-clean point cloud P_pseudo = P_double + 2 * (P_noisy - P_double).
   - Calculate L_rep (repulsion loss) to prevent point clustering:
     L_rep = max_over_neighbors(|| (P_double + d_0) - P_pseudo ||^2)
   - Minimize total loss: L = L_mse + g * L_rep (where g = 0.0005).
7. Apply predicted displacement vectors to the original noisy point cloud to obtain the denoised point cloud.
8. Denormalize coordinates back to original spatial scale.
```

### Gaps / not specified in paper

* **Species Generalization:** The dataset used primarily consists of plots with a single dominant tree species; performance in highly mixed, multi-layered temperate or tropical forests remains TBD (page 14).
* **Computational Overhead:** The exact inference time per hectare or per million points is not specified, which is critical for scaling to large-scale forest surveys.
* **Optimal k-NN Parameter:** The specific value of $k$ used for the k-Nearest Neighbors neighborhood feature extraction is TBD.

## Quotes

* "Specifically, in the S10 dataset, DEN4 attained a 70.2% diminution in MSE and a 37.8% augmentation in SNR in comparison with PTD." (Page 1)
* "The algorithm's superior performance and robustness in diverse forest environments underscores its potential application in single tree segmentation and forest resource management." (Page 1)
* "Compared to other algorithms, our algorithm more accurately captures the contours of individual trees, while maximizing the preservation of critical features such as canopy width, tree height, and diameter at breast height." (Page 9)

## Related pages

* [[concepts/canopy-height-model]]
* [[methods/chm-detection]]
* [[project/pipeline-overview]]
