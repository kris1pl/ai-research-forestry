---
title: Canopy height model (CHM)
type: Concept
description: "Normalized height of vegetation above ground: CHM = surface model of canopy top − digital terrain model (DTM)."
tags: [chm, dtm, dsm, lidar, height]
status: stable
updated: 2026-08-21
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
related_methods:
  - methods/chm-detection
  - methods/local-maxima
sources:
  - sources/vo-2024-automatic-data-curation
  - sources/paper-treeflow
  - sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340
  - sources/popescu-wynne-2004-seeing-the-trees
---
# Canopy height model (CHM)

Normalized height of vegetation above ground: **CHM = surface model of canopy top − digital terrain model (DTM)**.

## In our pipeline

Produced from 3D data and laser **ground model**, then used for height-stratified detection (DEIMv2) and merge with [[methods/local-maxima]]. See [[project/pipeline-overview]].

## Literature baseline

[[sources/popescu-wynne-2004-seeing-the-trees]] — small-footprint LiDAR CHM with 0.5 m grid; top-of-canopy DSM from **maximum elevation per sub-cell** before subtracting terrain; discusses underestimation when all first returns are interpolated without max filtering.

[[sources/vo-2024-automatic-data-curation]] — satellite canopy-height SSL experiment (Tolan et al. 2023 setup): hierarchical k-means curation of 18M → 9M patches improved backbone **block R² ~20%** on NEON / aerial NEON height benchmarks — indirect evidence that balanced aerial pre-training helps height-related downstream tasks.

## Design notes for us

- Ground model quality directly bounds height error.
- Grid resolution vs point density (drone GSD / LiDAR density).
- Whether apex detection uses raw CHM peaks ([[methods/local-maxima]]) or learned detectors on CHM layers ([[methods/chm-detection]]).

## Replication notes

Minimal replication chain from [[sources/popescu-wynne-2004-seeing-the-trees#Replication pseudocode]]:

```text
DTM → top_DSM (max per sub-cell) → CHM = top_DSM - DTM
```

Details and gaps (ground classifier, kriging): on the **source** page — not duplicated here. Implementation path: [[methods/chm-detection]].

## Related

- [[methods/chm-detection]]
- [[methods/local-maxima]]

## Open questions from literature

- Does pre-training our backbone on hierarchical-k-means-curated regional orthophotos improve local tree-level height regressions?
- How does the height-dependent resolution degradation in generative models like TreeFlow affect the fidelity of synthetic canopy height models derived from them?
- Can the 2D projection triangle fitting algorithm from BorFIT be reliably automated on noisy, raster-derived canopy height models without full 3D point cloud segmentation?