---
type: Source
title: "TreePseCo: Scaling Individual Tree Crown Segmentation using Large Vision Models"
description: "Adapts the PseCo framework using Segment Anything Model (SAM) and Faster R-CNN for robust individual tree crown segmentation in aerial imagery."
tags: [tree-detection, instance-segmentation, foundation-models, sam, deepforest]
status: stable
updated: 2026-08-21
source_file: raw/papers/TreePseCo_Scaling_Individual_Tree_Crown_Segmentation_using_Large_Vision_Models-isprs-archives-XLVIII-M-7-2025-275-2025.pdf
authors: [Jacopo Lungo Vaschetti, Edoardo Arnaudo, Claudio Rossi]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/TreePseCo_Scaling_Individual_Tree_Crown_Segmentation_using_Large_Vision_Models-isprs-archives-XLVIII-M-7-2025-275-2025.pdf
    title: "TreePseCo: Scaling Individual Tree Crown Segmentation using Large Vision Models"
related_methods:
  - methods/chm-detection
  - methods/deimv2-canopy
---

# TreePseCo: Scaling Individual Tree Crown Segmentation using Large Vision Models

## Summary

TreePseCo adapts the Point Segment and Count (PseCo) framework to perform automated individual tree crown detection and instance segmentation in high-resolution aerial RGB imagery. The method leverages a frozen Segment Anything Model (SAM) ViT-H encoder combined with a trainable task-specific heatmap decoder to estimate tree centers. These centers serve as point prompts for SAM's mask decoder to generate multiple crown proposals, which are subsequently classified and refined using a modified Faster R-CNN head with a ResNet50-FPN backbone. Tested on the NEON dataset and an independent alpine dataset (Valle d'Aosta - VdA), TreePseCo demonstrates superior geographical generalization and higher recall in dense, overlapping canopy environments compared to the standard DeepForest baseline.

## Key claims

- **Improved Generalization**: While DeepForest outperforms TreePseCo on its native NEON dataset (18.04 vs 15.43 mAP), TreePseCo generalizes significantly better to unseen geographical contexts, achieving 14.76 mAP on the alpine VdA dataset compared to DeepForest's 6.54 mAP (and 9.10 mAP when fine-tuned) (p. 279).
- **Dense and Small Tree Detection**: TreePseCo excels at identifying smaller tree instances and resolving individual trees in densely clustered formations where traditional bounding-box detectors merge crowns (p. 275, 279).
- **Large Tree Delineation**: On the VdA dataset, TreePseCo achieves 23.35 mAP for large trees, whereas both baseline and fine-tuned DeepForest models fail entirely (0.00 mAP) (p. 279).
- **Optimal Loss and Upsampling**: Structural Similarity Index Measure (SSIM) loss combined with transposed convolutions in the heatmap decoder yields sharper, more defined probability peaks than Mean Squared Error (MSE) and bilinear interpolation (p. 280).

## Implications for our pipeline

- **Foundation Model Integration**: The use of a frozen SAM ViT-H backbone to generate high-quality zero-shot mask proposals could complement or replace our current [[methods/deimv2-canopy]] or [[methods/chm-detection]] stages for complex, multi-layered forest structures.
- **Hybrid Point-to-Mask Pipeline**: The three-stage pipeline (Heatmap -> SAM Prompting -> R-CNN Refinement) provides a blueprint for converting local maxima or CHM peaks directly into precise instance masks without relying purely on watershed algorithms.
- **Computational Overhead Warning**: The authors note that TreePseCo introduces higher computational overhead due to the heavy SAM ViT-H encoder (p. 280). This must be weighed against processing speed requirements in our production [[project/pipeline-overview]].

## Replication pseudocode

### Prerequisites

- PyTorch, Torchvision
- Segment Anything Model (SAM) pretrained weights (ViT-H)
- PyCrown library (for training target generation from CHMs)
- ResNet50-FPN backbone

### Procedure

```text
# 1. Target Generation (Pretraining Phase)
For each training image patch (600x600 pixels):
    a. Extract tree centers from Canopy Height Model (CHM) using PyCrown:
       - Apply raster smoothing
       - Detect peaks using 2x2 max pooling
       - Filter out peaks below 5 meters
    b. Generate ground truth heatmap by placing a 2D Gaussian (sigma = 5) at each peak.

# 2. Heatmap Decoder Training
Initialize SAM ViT-H encoder (frozen) and a trainable Heatmap Decoder.
For each epoch:
    a. Extract image features using frozen SAM encoder.
    b. Pass features through Heatmap Decoder.
    c. Upsample using Transposed Convolutions.
    d. Compute loss using SSIM (for fine-tuning) or MSE (for noisy pretraining).
    e. Backpropagate and update Heatmap Decoder weights.

# 3. Mask and Box Proposal Generation
For a given test image:
    a. Generate probability heatmap using the trained decoder.
    b. Extract peak coordinates (local maxima) using:
       - Window size detection = 2
       - Window size smoothing = 0
       - Minimum height threshold = 0.3
    c. For each peak, prompt the standard SAM mask decoder with:
       - The peak point coordinate
       - A small surrounding box
       - A larger surrounding box
    d. Extract 6 circumscribing bounding boxes (proposals) per peak.

# 4. Classification and Refinement (Faster R-CNN Head)
Pass proposals and image features through a ResNet50-FPN backbone:
    a. Perform Multi-scale RoI Align on the FPN levels for each proposal.
    b. Pass through fully connected heads to output:
       - Classification score (tree confidence)
       - Bounding box regression offsets
    c. Apply Non-Maximum Suppression (NMS) to generate final refined boxes and masks.
```

### Gaps / not specified in paper

- The exact architecture of the "trainable heatmap decoder" attached to the SAM encoder is not fully detailed.
- The precise dimensions of the "small" and "larger" surrounding boxes used alongside the peak point to prompt SAM are not specified (TBD).
- The exact threshold used for Non-Maximum Suppression (NMS) during the final refinement stage is not explicitly stated (TBD).

## Quotes

> "Our approach implements a three-stage pipeline: (1) tree center detection using a modified Segment Anything Model (SAM) decoder that generates probability heatmaps, (2) instance mask generation through prompt-guided segmentation utilizing SAM's visual features, and (3) boundary refinement via specialized classification to eliminate false positives." (p. 275)

> "Notably, TreePseCo excels in detecting trees across all size categories in the VdA dataset, particularly for large trees (23.35 mAP) where both DeepForest variants failed to detect any instances (0.00 mAP)." (p. 279)

> "First, TreePseCo introduces a higher computational overhead compared to frameworks like DeepForest, potentially limiting its deployment in resource-constrained scenarios where processing speed is crucial." (p. 280)

## Related pages

- [[project/pipeline-overview]]
- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
- [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025]]
