---
title: Canopy height model (CHM)
type: concept
tags: [chm, dtm, dsm, lidar, height]
status: active
updated: 2026-06-09
related_methods:
  - methods/chm-detection
  - methods/local-maxima
sources:
  - sources/vo-2024-automatic-data-curation
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
