---
title: DEIMv2 — canopy detection
type: Method
description: "Tree detection with DEIMv2 on multiple CHM height layers (small vs large trees)."
tags: [deimv2, detection, ai]
status: stable
updated: 2026-10-26
generated:
  by: agent:conifervision-wiki
  at: 2026-10-26T12:00:00Z
sources:
  - sources/paper-edgecrafter
  - sources/paper-deimv2
  - sources/paper-fine-tuning_matters_and_parallel_decoder_helps
  - sources/paper-refdrone_llms
  - sources/paper-a crown width-diameter model for natural even-aged black pine forest management-forests-09-00610-v2
  - sources/paper-a_linkage_among_tree_diameter_height_crown_base_he
  - sources/paper-allometric relationships of selected european tree-gp_eudor_pdfa1b_euna20855enc_001
  - sources/paper-interregional crown width models for individual trees growing in pure and mixed stands in austria-forests-11-00114-v3
  - sources/paper-parameterization of height–diameter and crown radius-diameter relationship across the globe - rtae005
  - sources/paper-fsod-vfm
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
- Can the auxiliary number prediction head and learnable number-queries from NGDINO be integrated into DEIMv2-canopy to reduce false positives in empty canopy gaps and improve multi-tree counting?
- Can stand density proxies (e.g. basal area or relative spacing from preliminary CHM local maxima density) be used to dynamically parameterize expected crown bounding box sizes in DEIMv2 inference?
- Can the age-dependent joint confidence ellipsoids of height and crown width from Rupšys & Petrauskas (2017) guide height-stratified anchor or box-size priors in DEIMv2 canopy detection?
- Can the empirical height-to-crown-radius ($H \leftrightarrow C_r$) curves from Widlowski et al. (2003) serve as dynamic bounding box aspect/size priors during height-stratified DEIMv2 inference to suppress over-split crowns in spruce and pine stands?
- Can the species-specific crown width allometries and admixture adjustment factors from Buchacher & Ledermann (2020) serve as bounding box priors or over-segmentation filters in DEIMv2 canopy detection?
- Can PFT-specific crown radius-to-height allometric bounds (e.g. Chapman–Richards or Logistic curves from Song et al., 2024) be used as dynamic box-size sanity filters to prune false positive DEIMv2 canopy proposals?