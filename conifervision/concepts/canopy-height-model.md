---
title: Canopy height model (CHM)
type: concept
tags: [chm, dtm, dsm, lidar, height]
status: active
updated: 2026-06-05
related_methods:
  - methods/chm-detection
  - methods/local-maxima
sources:
  - sources/popescu-wynne-2004-seeing-the-trees
---

# Canopy height model (CHM)

Normalized height of vegetation above ground: **CHM = surface model of canopy top − digital terrain model (DTM)**.

## In our pipeline

Produced from 3D data and laser **ground model**, then used for height-stratified detection (DEIMv2) and merge with [[methods/local-maxima]]. See [[project/pipeline-overview]].

## Literature baseline

[[sources/popescu-wynne-2004-seeing-the-trees]] — small-footprint LiDAR CHM with 0.5 m grid; top-of-canopy DSM from **maximum elevation per sub-cell** before subtracting terrain; discusses underestimation when all first returns are interpolated without max filtering.

## Design notes for us

- Ground model quality directly bounds height error.
- Grid resolution vs point density (drone GSD / LiDAR density).
- Whether apex detection uses raw CHM peaks ([[methods/local-maxima]]) or learned detectors on CHM layers ([[methods/chm-detection]]).

## Related

- [[methods/chm-detection]]
- [[methods/local-maxima]]
