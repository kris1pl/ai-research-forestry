---
title: CHM and height-layer detection
type: method
tags: [chm, lidar, detection]
status: active
updated: 2026-06-05
related_methods:
  - methods/deimv2-canopy
  - methods/local-maxima
  - methods/merge-detections
sources:
  - sources/popescu-wynne-2004-seeing-the-trees
---

# Canopy Height Model (CHM)

CHM from the 3D model and **ground model** (laser / DTM). Object detection on height layers (small / large trees) — in production with **DEIMv2** ([[deimv2-canopy]]).

## In the pipeline

Feeds [[merge-detections]] together with [[local-maxima]].

## Literature

[[sources/popescu-wynne-2004-seeing-the-trees]] — CHM construction workflow: ground classification, first-return DSM at fine grid, **max height per cell** for canopy surface, subtract terrain. Notes that CHM accuracy tracks DTM error and that interpolating all returns can underestimate apex height vs max-filtered DSM.

## Production parameters

_(height thresholds, CHM resolution, ground model version)_

## Related

- [[concepts/canopy-height-model]]
- [[methods/local-maxima]]
