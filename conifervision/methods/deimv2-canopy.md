---
title: DEIMv2 — canopy detection
type: Method
description: "Tree detection with DEIMv2 on multiple CHM height layers (small vs large trees)."
tags: [deimv2, detection, ai]
status: stable
updated: 2026-08-19
P26-08-19T12:00:00Z
sources:
  - sources/paper-deimv2
---
# DEIMv2

Tree detection with **DEIMv2** on multiple CHM height layers (small vs large trees).

## In the pipeline

See [[chm-detection]], [[merge-detections]].

## Model versions / checkpoints

_(link to experiment registry / MLflow)_

## Replication notes

No replication pseudocode from [[sources/popescu-wynne-2004-seeing-the-trees]] — paper predates learned detectors on CHM layers. Add a source link here when a relevant paper is ingested.

## Literature / sources

_(after ingest)_

## Open questions from literature

- How does the latency of DEIMv2-S or DEIMv2-M scale on edge hardware (e.g., NVIDIA Jetson) when optimized with TensorRT?
