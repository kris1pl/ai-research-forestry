---
title: EdgeCrafter ECSeg — instance segmentation
type: Method
description: "Instance segmentation layer based on EdgeCrafter (ECSeg) for tree crown instances, designed to improve dense-stand separation and fusion."
tags: [edgecrafter, ecseg, instance-segmentation, detection, rgb]
status: draft
updated: 2026-08-19
generated:
  by: agent:conifervision-wiki
  at: 2026-08-19T12:00:00Z
related_methods:
  - methods/merge-detections
  - methods/deimv2-canopy
sources: []
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

## Production parameters

TBD:

- mask resolution / upsampling method
- confidence thresholding and post-processing

## Related

- `[[concepts/dense-stand-detection]]`
- `[[methods/merge-detections]]`

