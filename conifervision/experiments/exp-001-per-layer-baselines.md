---
title: exp-001 per-layer baselines (open vs dense)
type: Experiment
description: "Baseline measurements per ensemble layer before fusion, stratified by open vs dense stands and small vs large trees."
tags: [ensemble, baseline, evaluation, dense-stands, edgecrafter]
status: draft
updated: 2026-08-19
area: "conifervision/project/research-tree-detection-ensemble (detection program)"
hypothesis: "Layer-wise performance ceilings and dense-specific error taxonomy are necessary inputs for robust fusion design."
metrics: {}
sources: []
generated:
  by: agent:conifervision-wiki
  at: 2026-08-19T12:00:00Z
---

# exp-001 per-layer baselines (open vs dense)

## Hypothesis

Dense-stand failures have different dominant error modes than open stands; therefore per-layer baselines stratified by open vs dense will drive a better fusion strategy than global (non-stratified) evaluation.

## Setup

Planned runs (no fusion yet):

- Local maxima / LM baseline
- CHM + DEIMv2 baseline (height-layer stratification: small vs large, as used in production)
- RGB detection baseline (to compare bbox quality)
- RGB instance segmentation baseline (EdgeCrafter ECSeg) (zero-shot / few-shot depending on available checkpoint)

Split protocol:

- open vs dense using the `[[concepts/dense-stand-detection]]` definition (TBD)
- size bins aligned with your CHM/DEIMv2 layers

## Results

| Run | Metric | Value | Notes |
|-----|--------|-------|-------|
| TBD | TBD | TBD | TBD |

## Conclusion

TBD

## Related

- `[[project/research-tree-detection-ensemble]]`
- `[[concepts/dense-stand-detection]]`
- `[[methods/merge-detections]]`
- `[[methods/edgecrafter-ecseg]]`

