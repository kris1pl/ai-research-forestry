---
title: Pipeline overview
type: project
tags: [pipeline, production]
status: active
updated: 2026-06-03
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/merge-detections
  - methods/dinov3-classification
---

# Forest area analysis pipeline (AREA)

**Status:** reference description — update whenever production methodology changes. Lint compares this page against code and `methods/` pages.

## 1. Data acquisition

- Drone imagery for selected **AREA** units.
- Build an **orthophoto** for each AREA.

## 2. Tree detection (geometry + CHM + AI)

1. **Local maxima** with a sliding window on the 3D model — tree tops and heights.
2. **Canopy Height Model (CHM)** from the 3D model and laser data (ground model).
3. **Object detection** with **DEIMv2** on multiple height layers (small / large trees).
4. **Merge** local maxima + CHM detections → final tree detections.

## 3. Species classification

1. **DINOv3** — object detection, crops, feature vectors.
2. **Clustering** — specialist groups clusters by dominant species.
3. **Object registry** (Delta Lake) — `weak_label` from clustering.
4. Train DINOv3 classifier on ground truth + weak labels.
5. Classify detected trees with the trained model.

**Literature (not in production):** [[concepts/pseudo-tree-crown]] from [[sources/miao-zhang-2024-ptc-uav-species]] — optional 3D-style crown reprojection before CNN input; tested with ResNet50 on UAV orthophoto patches, not DINOv3.

## External integrations

- Operational data and labels: **Delta Lake** (outside this repo) — the wiki links metrics and versions; it does not duplicate tables.

## Methods (wiki)

| Stage | Wiki page |
|-------|-----------|
| Local maxima | [[methods/local-maxima]] |
| CHM + detection | [[methods/chm-detection]] |
| DEIMv2 | [[methods/deimv2-canopy]] |
| Merge | [[methods/merge-detections]] |
| DINOv3 | [[methods/dinov3-classification]] |
