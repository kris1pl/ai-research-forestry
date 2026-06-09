---
title: Pseudo tree crown (PTC)
type: concept
tags: [ptc, uav, orthophoto, species-classification, deep-learning]
status: active
updated: 2026-06-03
related_methods:
  - methods/dinov3-classification
sources:
  - sources/miao-zhang-2024-ptc-uav-species
---

# Pseudo tree crown (PTC)

A **synthetic side/3D view** of an individual tree crown generated from a **nadir** UAV (or aerial) patch, used as classifier input instead of a conventional top-down crop. Introduced by Miao et al. (2024) to increase feature contrast for CNN-based **individual tree species** classification.

## Definition (from literature)

- Input: typically the **green band** of a nadir crown patch (greyscale grid).
- Transform: 3D subplot projection with configurable **azimuth** and **elevation** (paper default: **−120°**, **75°**).
- Output: a 2D image (PTC) fed to standard image classifiers (ResNet50, YOLOv5, RF, etc.) at fixed size (paper: **64×64** px).

Lineage noted in paper: longitudinal crown profile work (Fourier et al.; Zhang & Hu; Balkenhol & Zhang); prototype in Miao et al. (2023).

## In our pipeline

**Not implemented** in production. Our species path uses [[methods/dinov3-classification]] on crops from orthophoto detections. PTC is a **candidate preprocessing** step if nadir crops underperform for similar species pairs.

See [[project/pipeline-overview]] stage 3.

## Design notes for us

| Topic | Paper finding | Our action |
|-------|----------------|------------|
| vs nadir RGB/green | +12–14% accuracy (DL), +9% (RF) | A/B on held-out AREA species if confusion is high |
| View angles | Stable >95% for ±120° azimuth at 75° elevation | Default angles if we trial PTC |
| GSD / resolution | PTC tolerates ~10× coarser source | May help mixed-resolution orthophotos |
| Detection | Manual GIS patches | Requires reliable tree boxes from [[methods/merge-detections]] first |
| Forest vs urban | Campus, isolated urban trees | Revalidate on dense conifer stands |

## Replication notes

Procedure summary: [[sources/miao-zhang-2024-ptc-uav-species#Replication pseudocode]]. Full rendering code not in the PDF.

## Related

- [[methods/dinov3-classification]]
- [[sources/miao-zhang-2024-ptc-uav-species]]
