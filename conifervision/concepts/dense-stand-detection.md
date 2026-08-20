---
title: Dense stand detection (before clearing)
type: Concept
description: "Evaluation concept for tree detection in dense stands where crown overlap breaks bbox-centric NMS and segmentation boundaries drive errors."
tags: [dense-stands, evaluation, detection, instance-segmentation, dense/open]
status: draft
updated: 2026-08-20
P26-08-20T12:00:00Z
related_methods:
  - methods/merge-detections
  - methods/deimv2-canopy
  - methods/edgecrafter-ecseg
sources: []
sources:
  - sources/paper-fsod-vfm
---
# Dense stand detection (before clearing)

This concept defines how we should evaluate (and eventually improve) tree detection in dense stands (for example, before clearing), where crown overlap and connected topology create failure modes that differ from sparse plots.

## Definition (operational, TBD)

We need an operational definition of "dense" vs "open" that we can compute consistently from available geometry and annotations.

- Dense/open split: TBD (example: LiDAR/CHM-derived canopy density proxy, or ground-truth tree count density per AREA tile).
- Size bins: small vs large trees: TBD (must align with your CHM/DEIMv2 height-layer stratification).

## Why dense stands are different

Expected dense-specific error modes:

- Duplicate suppression: bbox-centric NMS may eliminate true neighboring trees.
- Boundary quality: instance segmentation errors (under-segmentation, merged instances, jagged boundaries) can dominate quality.
- Geometry degeneracy: CHM can be locally flat or insufficiently separable, reducing the value of purely geometric layers.

## In our pipeline (research)

Used to structure experiments in `[[project/research-tree-detection-ensemble]]`:

- baseline measurements per layer in open vs dense splits
- error taxonomy specialized for dense plots
- fusion strategy validation where segmentation boundary quality matters

## Design notes (hypotheses)

Working hypothesis:

- segmentation-first fusion (or mask-aware merge rules) yields better separation in dense stands than pure bbox voting.

## Metrics we likely need (without locking numbers yet)

By size bin and open vs dense:

- detection metrics for small and large objects (use your current production definitions)
- boundary-aware instance metrics (for segmentation-first approaches)
- under-segmentation and duplicate rate proxies (to explain dense failure modes)

## Replication notes

TBD:

- when we ingest papers covering dense detection, add links to `[[sources/...#Replication pseudocode]]` here
- until then, this concept is a protocol container for your internal evaluation and ablations

## Related

- `[[project/research-tree-detection-ensemble]]`
- `[[methods/merge-detections]]`
- `[[methods/edgecrafter-ecseg]]`

## Open questions from literature

- Does applying a PageRank-style graph diffusion process over SAM2 mask overlaps help resolve boundary-level under-segmentation and duplicate detections in dense conifer stands?
