---
title: DINOv3 — species classification
type: method
tags: [dinov3, classification, weak-labels, orthophoto, species]
status: active
updated: 2026-06-03
related_methods:
  - methods/merge-detections
sources:
  - sources/miao-zhang-2024-ptc-uav-species
---

# DINOv3 classification

1. Object detection with DINOv3, crops, feature vectors.
2. Clustering + specialist labels → **weak labels** in Delta Lake.
3. Train classifier on ground truth + weak labels.
4. Classify detected trees.

## In the pipeline

Stage 3 in [[project/pipeline-overview]] — runs on per-tree crops after detection/merge.

## Literature

[[sources/miao-zhang-2024-ptc-uav-species]] — urban UAV study; **not DINOv3** but directly relevant to **per-tree orthophoto patches** and species separability. Shows that **input reformation (PTC)** before a CNN can outperform nadir green-band patches by >10%; best reported setup PyTorch + ResNet50 (~98% on 5 species, 696 patches). Our backbone differs; the lesson is patch geometry/view, not a specific framework.

## Replication notes

| Paper step | Our implementation |
|------------|---------------------|
| Manual / GIS tree patches | Automated crops from detections + orthophoto |
| PTC 3D reprojection of crown | **Not used** — candidate experiment ([[concepts/pseudo-tree-crown]]) |
| ResNet50 64×64, 50 epochs | DINOv3 pipeline (architecture TBD in code repo) |
| Field-validated species labels | Ground truth + weak labels (Delta Lake) |

Full PTC pseudocode: [[sources/miao-zhang-2024-ptc-uav-species#Replication pseudocode]]. **Replication focus for us:** only the *idea* of non-nadir patch views until we run an internal A/B.

## Production parameters

_(model version, crop size, augmentations — link when code repo integrated)_

## Related concepts

- [[concepts/pseudo-tree-crown]] — optional input transform from literature
- Weak labels: Delta Lake / clustering _(wiki page TBD)_

## Open questions from literature

- Would PTC-style views help conifer species confused on nadir orthophoto crops?
- Paper patches are pre-segmented urban crowns; do overlapping crowns in production negate PTC gains?
