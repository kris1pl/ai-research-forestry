---
title: DINOv3 — species classification
type: Method
description: "1. Object detection with DINOv3, crops, feature vectors."
tags: [dinov3, classification, weak-labels, orthophoto, species]
status: stable
updated: 2026-06-09
generated:
  by: agent:conifervision-wiki
  at: 2026-06-09T12:00:00Z
related_methods:
  - methods/merge-detections
sources:
  - sources/miao-zhang-2024-ptc-uav-species
  - sources/vo-2024-automatic-data-curation
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

[[sources/vo-2024-automatic-data-curation]] — Meta FAIR (DINOv2 authors). **Hierarchical k-means + resampling** to build balanced SSL pre-training sets from long-tailed pools; explains why **vanilla k-means fails** to balance dominant vs rare visual concepts. Directly relevant to our **clustering → weak labels** step (same embedding-space pathology, different goal). Satellite experiment: curated 9M / 18M patch pool improved **canopy height R² ~20%** vs raw pre-training — indirect support for balanced aerial/satellite representation learning before tree-level tasks.

## Replication notes

| Paper step | Our implementation |
|------------|---------------------|
| Manual / GIS tree patches | Automated crops from detections + orthophoto |
| PTC 3D reprojection of crown | **Not used** — candidate experiment ([[concepts/pseudo-tree-crown]]) |
| ResNet50 64×64, 50 epochs | DINOv3 pipeline (architecture TBD in code repo) |
| Field-validated species labels | Ground truth + weak labels (Delta Lake) |
| Hierarchical k-means curation (Vo 2024) | **Not used** — we use plain clustering for weak labels; candidate improvement |

Full PTC pseudocode: [[sources/miao-zhang-2024-ptc-uav-species#Replication pseudocode]]. **Replication focus for us:** only the *idea* of non-nadir patch views until we run an internal A/B.

## Production parameters

_(model version, crop size, augmentations — link when code repo integrated)_

## Related concepts

- [[concepts/pseudo-tree-crown]] — optional input transform from literature
- Weak labels: Delta Lake / clustering — see [[sources/vo-2024-automatic-data-curation#Implications for our pipeline]] for balancing theory

## Open questions from literature

- Would PTC-style views help conifer species confused on nadir orthophoto crops?
- Paper patches are pre-segmented urban crowns; do overlapping crowns in production negate PTC gains?
- Can we adapt hierarchical k-means with resampling to balance highly skewed species distributions in our weak-label generation pipeline?
- Can we adapt the hierarchical k-means + resampling pipeline to balance our weak-label species pools in Delta Lake?
- Can we use hierarchical k-means with resampling to resolve the dominant-species cluster splitting issue in our weak-label generation pipeline?