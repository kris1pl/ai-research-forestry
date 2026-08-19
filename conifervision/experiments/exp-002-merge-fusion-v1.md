---
title: exp-002 merge / fusion v1 (segmentation-aware)
type: Experiment
description: "First fusion design iteration: compare bbox-centric NMS vs mask-aware merge under dense-stand conditions."
tags: [ensemble, merge, fusion, dense-stands]
status: draft
updated: 2026-08-19
area: "conifervision/project/research-tree-detection-ensemble (fusion program)"
hypothesis: "Mask-aware fusion rules reduce dense-stand duplicates and under-segmentation artifacts compared to bbox-only priority."
metrics: {}
sources: []
generated:
  by: agent:conifervision-wiki
  at: 2026-08-19T12:00:00Z
---

# exp-002 merge / fusion v1 (segmentation-aware)

## Hypothesis

Using instance masks in fusion (or using segmentation quality to resolve bbox conflicts) improves dense-stand separation relative to bbox-only NMS.

## Setup

Inputs:

- LM candidates
- CHM/DEIMv2 candidates
- ECSeg masks (RGB instance segmentation)

Fusion variants to compare:

- Variant A: bbox-centric NMS + priority rules (baseline)
- Variant B: segmentation-aware conflict resolution (mask-first or mask-guided)

Dense evaluation:

- same open vs dense split definition from `[[concepts/dense-stand-detection]]`
- size bins aligned with CHM/DEIMv2 height layers

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

