---
title: CHM and height-layer detection
type: Method
description: "CHM from the 3D model and ground model (laser / DTM). Object detection on height layers (small / large trees) — in production with DEIMv2 (deimv2-canopy)."
tags: [chm, lidar, detection]
status: stable
updated: 2026-06-05
generated:
  by: agent:conifervision-wiki
  at: 2026-06-05T12:00:00Z
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

## Replication notes

CHM build pseudocode: [[sources/popescu-wynne-2004-seeing-the-trees#Replication pseudocode]] (steps **1–3**).

| Paper step | Our implementation (TBD) |
|------------|---------------------------|
| Ground / DTM from laser | Ground model in pipeline |
| Top canopy surface (max per sub-cell → grid) | Compare with our DSM/CHM rasterization |
| `CHM = top_DSM − DTM` | [[concepts/canopy-height-model]] |
| Height layers + DEIMv2 | **Beyond paper** — learned detectors on CHM strata |

**Replication focus for us:** validate ground model and CHM grid against paper’s max-cell rule before tuning DEIMv2 thresholds. Paper grid **0.5 m** — map to our resolution.

## Production parameters

_(height thresholds, CHM resolution, ground model version)_

## Related

- [[concepts/canopy-height-model]]
- [[methods/local-maxima]]
