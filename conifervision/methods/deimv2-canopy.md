---
title: DEIMv2 — canopy detection
type: Method
description: "Tree detection with DEIMv2 on multiple CHM height layers (small vs large trees)."
tags: [deimv2, detection, ai]
status: stable
updated: 2026-08-20
P26-08-19T12:00:00Z
sources:
  - sources/paper-edgecrafter
  - sources/paper-deimv2
  - sources/paper-fine-tuning_matters_and_parallel_decoder_helps
  - sources/paper-fsod-vfm
P26-08-20T12:00:00Z
generated:
  by: agent:conifervision-wiki
  at: 2026-08-20T12:00:00Z
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
- Can the simple bilinear interpolation and linear projection multi-scale feature generation from EdgeCrafter replace the feature pyramid network in DEIMv2-canopy to reduce edge latency on drone hardware?
- How does the optimal ratio of stacked-to-parallel decoder layers (K vs L-K) scale when adapting DEIMv2-canopy for multi-height tree crown detection?
- Can the graph diffusion-based confidence reweighting mechanism from FSOD-VFM be adapted to resolve overfragmentation (e.g., multiple sub-crown detections) in DEIMv2 canopy predictions?