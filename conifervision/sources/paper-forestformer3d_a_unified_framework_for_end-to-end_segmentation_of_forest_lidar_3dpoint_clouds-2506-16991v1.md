---
type: Source
title: "ForestFormer3D: A Unified Framework for End-to-End Segmentation of Forest LiDAR 3D Point Clouds"
description: "An end-to-end transformer-based 3D instance and semantic segmentation framework for forest LiDAR point clouds using ISA-guided query selection, score-based block merging, and one-to-many association."
tags: [lidar, point-cloud, instance-segmentation, semantic-segmentation, transformer, deep-learning]
status: stable
updated: 2026-08-21
source_file: raw/papers/ForestFormer3D_A_Unified_Framework_for_End-to-End_Segmentation_of_Forest_LiDAR_3DPoint_Clouds-2506.16991v1.pdf
authors: [Binbin Xiang, Maciej Wielgosz, Stefano Puliti, Kamil Král, Martin Krůček, Azim Missarov, Rasmus Astrup]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/ForestFormer3D_A_Unified_Framework_for_End-to-End_Segmentation_of_Forest_LiDAR_3DPoint_Clouds-2506.16991v1.pdf
    title: "ForestFormer3D: A Unified Framework for End-to-End Segmentation of Forest LiDAR 3D Point Clouds"
related_methods:
  - methods/chm-detection
  - methods/dinov3-classification
---

# ForestFormer3D: A Unified Framework for End-to-End Segmentation of Forest LiDAR 3D Point Clouds

## Summary

ForestFormer3D is a unified, end-to-end transformer-based framework designed for joint individual tree (instance) and semantic segmentation of forest 3D LiDAR point clouds. Unlike traditional bottom-up methods that rely on non-differentiable clustering steps (e.g., watershed or K-means), ForestFormer3D utilizes a sparse 3D U-Net backbone combined with a transformer decoder. It introduces three key innovations: Instance- and Semantic-Aware (ISA) guided query point selection, a score-based global ranking block-merging strategy for large-scale inference, and a one-to-many association mechanism for training that bypasses Hungarian matching. Evaluated on the newly expanded FOR-instanceV2 dataset, it achieves state-of-the-art individual tree segmentation performance and demonstrates strong generalization across diverse forest types and sensor modalities (including UAV, MLS, and TLS).

## Key claims

- **State-of-the-Art Performance:** Outperforms existing methods (such as ForAINet, TreeLearn, and OneFormer3D) on individual tree segmentation, achieving an F1-score of 82.8% (+9.7 percentage points over the second-best baseline) and a coverage (Cov) of 81.2% on the FOR-instanceV2 test split (p. 6, Tab. 1).
- **ISA-Guided Query Point Selection:** Replaces random or farthest point sampling (FPS) with a dual-head MLP strategy (5D discriminative embedding + binary tree/non-tree classification). This achieves a 92.7% tree instance coverage rate and a 98.5% tree voxel ratio, minimizing background ground-point queries (p. 4-5).
- **One-to-Many Association:** Bypasses the computationally expensive Hungarian matching algorithm during training by directly associating pre-aligned query points with ground truth instances, improving F1-score by 0.8 pp (p. 5, Tab. 3).
- **Score-Based Block Merging:** Implements a global score-ranking and Non-Maximum Suppression (NMS) strategy to merge overlapping cylindrical inference blocks, resolving boundary splitting issues by discarding predicted masks within 0.5 m of the crop boundary (p. 5-6).
- **Robust Generalization:** Successfully generalizes to unseen datasets (Wytham woods and LAUTx) without retraining, demonstrating adaptability to different sensor types (TLS, MLS) and complex broadleaved structures (p. 6, Tab. 2).

## Implications for our pipeline

- **Transition to 3D Point Clouds:** While our current production pipeline ([[project/pipeline-overview]]) relies heavily on 2D orthophotos and 2.5D Canopy Height Models ([[concepts/canopy-height-model]]), ForestFormer3D offers a blueprint for direct 3D point cloud segmentation. This could bypass the need for intermediate 2D projections when high-density LiDAR data is available.
- **Query-Based Tree Detection:** The ISA-guided query point selection mechanism could be adapted to improve our local maxima sliding window or DEIMv2-based canopy detection stages by incorporating 3D spatial and semantic embeddings.
- **Cylindrical Block Merging:** The score-based block merging strategy with boundary mask discarding (0.5 m threshold) is highly relevant for our large-area tiling and merging steps, helping to mitigate edge-effect double-detections.

## Replication pseudocode

### Prerequisites

- PyTorch, SpConv (Spatially Sparse Convolution Library)
- MinkowskiEngine or similar sparse tensor framework
- Training data with individual tree IDs and semantic labels (ground, wood, leaf)

### Procedure

```text
# High-level steps for ForestFormer3D forward pass and inference

1. Voxelize the input point cloud P (resolution = 0.2m) to obtain sparse tensor V.
2. Extract voxel-wise features F (M x 32) using SpConvUNet.
3. Pass F through two parallel MLP heads:
   a. Head 1: Learn 5D discriminative embeddings (F1) to group voxels of the same tree.
   b. Head 2: Perform binary classification (F2) to separate tree vs. non-tree voxels.
4. Exclude non-tree voxels and apply Farthest Point Sampling (FPS) in the 5D embedding space to select Kins query points.
5. Feed selected instance query points and Ksem learnable semantic queries into the 6-layer Transformer Decoder.
6. Output Kins tree instance masks, confidence scores, and Ksem semantic masks.
7. During Inference:
   a. Crop large scenes into overlapping cylindrical blocks (radius = 16m, stride = 4m).
   b. Discard predicted masks within 0.5m of the cylinder boundaries.
   c. Merge overlapping blocks using global score-ranking and Non-Maximum Suppression (NMS).
```

### Gaps / not specified in paper

- **Voxelization details:** The exact handling of point attributes (intensity, return number) when multiple points fall into a single 0.2m voxel is not fully detailed, though the authors state they only use 3D coordinates (p. 3).
- **NMS Thresholds:** The exact IoU threshold used during the final score-based block merging NMS step is not explicitly specified in the main text (TBD).

## Quotes

> "Unlike previous bottom-up methods that rely on non-differentiable clustering steps for individual tree segmentation, our transformer-based decoder enables fully differentiable, end-to-end training." (p. 3)

> "Specifically, for a cylinder radius of 16 m, we remove masks within 0.5 m of the boundary to remove incomplete tree masks." (p. 6)

## Related pages

- [[project/pipeline-overview]]
- [[concepts/canopy-height-model]]
- [[sources/paper-comparison_of_individual_tree-twec21_public]]
- [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]]
