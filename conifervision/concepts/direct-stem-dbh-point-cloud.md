---
title: "Direct Stem and DBH Measurement from 3D Point Clouds"
type: Concept
description: "Existing concept tree-allometry covers empirical/allometric models predicting DBH from height or crown metrics rather than direct geometric stem reconstruction, trunk detection, and diameter extraction directly from 3D point cloud slices."
tags: [direct, stem, dbh, point, cloud]
status: draft
updated: 2026-10-26
generated:
  by: agent:concept-gate
  at: 2026-10-26T10:45:34Z
sources:
  - sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations
  - sources/paper-comparison_of_individual_tree-twec21_public
  - sources/paper-estimating tree diameter at breast height (dbh) from uav data-1-s2-0-s2666017225001373-main
---

# Direct Stem and DBH Measurement from 3D Point Clouds

Existing concept tree-allometry covers empirical/allometric models predicting DBH from height or crown metrics rather than direct geometric stem reconstruction, trunk detection, and diameter extraction directly from 3D point cloud slices.

This page names the shared idea. It does not open an experiment folder. [[project/domains]] does not gain a new program from this page.

```mermaid
flowchart LR
  sources["Source pages"] --> concept["This concept"]
```

## What the sources describe

- [[sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations]] — Bottom-up individual tree extraction using HDBSCAN trunk clustering, chi-square distribution stem DBH measurement, and pseudo-waveform tree height estimation from ultra-high-density low-cost UAV-LiDAR.
- [[sources/paper-comparison_of_individual_tree-twec21_public]] — A comparative study of local maxima, trunk detection, and point density methods for individual tree detection using high-density UAV laser scanning.
- [[sources/paper-estimating tree diameter at breast height (dbh) from uav data-1-s2-0-s2666017225001373-main]] — Compares direct geometric DBH estimation via multi-angle UAV-DAP (nadir + 30°/60° oblique) circle fitting against Random Forest allometric modeling from vertical CHM/crown metrics.

Stand dominant height, site index, and stand volume stay on [[concepts/site-index-and-yield]].

## Replication notes

Coefficients stay on the source pages. Nothing here is implemented in the detection pipeline.

| Paper | Our status |
|---|---|
| [[sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations]] — Extraction of Individual Tree Attributes Using Ultra-High-Density Point Clouds Acquired by Low-Cost UAV-LiDAR in Eucalyptus Plantations | TBD |
| [[sources/paper-comparison_of_individual_tree-twec21_public]] — Comparison of individual tree detection methods | TBD |
| [[sources/paper-estimating tree diameter at breast height (dbh) from uav data-1-s2-0-s2666017225001373-main]] — Estimating tree diameter at breast height (DBH) from UAV data: A comparison of oblique–Vertical imagery fusion and allometric modeling | TBD |

## Related

- [[concepts/site-index-and-yield]] — stand site index and stand volume
- [[concepts/crown-ownership]] — a crown box is not yet a measured crown width
- [[concepts/canopy-height-model]] — tree height read from the canopy surface
- [[project/domains]] — allometry program not started
