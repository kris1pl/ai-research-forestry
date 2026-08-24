---
title: EdgeCrafter ECSeg — instance segmentation
type: Method
description: "Instance segmentation layer based on EdgeCrafter (ECSeg) for tree crown instances, designed to improve dense-stand separation and fusion."
tags: [edgecrafter, ecseg, instance-segmentation, detection, rgb]
status: stable
updated: 2026-08-24
generated:
  by: agent:conifervision-wiki
  at: 2026-08-24T12:00:00Z
related_methods:
  - methods/merge-detections
  - methods/deimv2-canopy
sources:
  - sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main
  - sources/paper-edgecrafter
---
# EdgeCrafter ECSeg

Instance segmentation layer (ECSeg) intended as the main ROI provider for an ensemble tree detector, especially in dense stands where bbox-centric NMS can suppress true neighboring trees.

## In the pipeline

Research ensemble layer in `[[project/research-tree-detection-ensemble]]`:

- RGB instance segmentation (masks) feeding into `[[methods/merge-detections]]`
- masks improving conflict resolution where geometric (LM) and CHM/DEIMv2 detections overlap

## Model versions / checkpoints

_(link to experiment registry / MLflow once connected to the code repo)_

## Replication notes

TBD:

- after ingesting EdgeCrafter sources: link replication pseudocode here as
  `[[sources/edgecrafter-...#Replication pseudocode]]`
- map the paper's steps to our implementation status

| Paper step | Our implementation |
|------------|---------------------|
| Teacher distillation setup | TBD |
| ECSeg training recipe | TBD |
| Inference output format (mask) | TBD |
| Tile orthophoto into 256 x 256 patches | TBD |
| Generate instance masks with unique integer IDs | TBD |
| Compute normalized Euclidean distance transform and radial distances (32 angles) | TBD |
| Apply modified sparse-annotation loss (BCE only on p > 0) | TBD |
| Train U-Net backbone with probability and radial distance heads | TBD |
| Apply Polygon Non-Maximum Suppression (IoU threshold = 0.3) | TBD |


Pseudocode: [[sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main#Replication pseudocode]].
## Production parameters

TBD:

- mask resolution / upsampling method
- confidence thresholding and post-processing

## Related

- `[[concepts/dense-stand-detection]]`
- `[[methods/merge-detections]]`

## Open questions from literature

- Does the detection-distilled representation from ECDet transfer to tree crown instance segmentation (ECSeg) in dense stands without requiring separate backbone pretraining?
- - Can the sparse-annotation loss constraint ($p > 0$) from StarDist be integrated into EdgeCrafter ECSeg to allow training on partially annotated drone imagery?