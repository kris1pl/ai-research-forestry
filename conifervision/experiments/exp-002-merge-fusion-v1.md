---
title: exp-002 merge / fusion v1 (segmentation-aware)
type: Experiment
description: "First fusion design iteration: compare bbox-centric NMS vs mask-aware merge under dense-stand conditions."
tags: [ensemble, merge, fusion, dense-stands]
status: draft
updated: 2026-08-21
area: "Same AREA eval set as exp-001 once available; report open vs dense separately"
hypothesis: "Mask-aware fusion rules reduce dense-stand duplicates and under-segmentation artifacts compared to bbox-only priority NMS, without catastrophic regression on open stands."
metrics:
  detection_ap_dense: TBD
  detection_ap_open: TBD
  duplicate_rate_dense: TBD
  under_segmentation_rate_dense: TBD
related_methods:
  - methods/merge-detections
  - methods/edgecrafter-ecseg
  - methods/deimv2-canopy
  - methods/local-maxima
sources: []
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
---

# exp-002 merge / fusion v1 (segmentation-aware)

## Hypothesis

Using instance masks in fusion (or using segmentation quality to resolve bbox conflicts) improves dense-stand separation relative to bbox-only NMS.

## Motivation

- Depends on ceilings from [[experiments/exp-001-per-layer-baselines]]
- Fusion stub: [[methods/merge-detections]]
- Masks: [[methods/edgecrafter-ecseg]]
- Dense errors: [[concepts/dense-stand-detection]]
- Program: [[project/research-tree-detection-ensemble]] · loop: [[project/hypothesis-validation-loop]]

## Pseudocode

**Inputs:** candidate sets from LM, CHM/DEIMv2, ECSeg masks; eval labels

**Outputs:** fused instance set; metrics vs Variant A (bbox NMS) and Variant B (mask-aware)

**Parameters:** NMS IoU / distance (TBD); mask-overlap rule (TBD); layer priority order (TBD)

```text
1. Require exp-001 baselines (or provisional ceilings) for context.
2. Variant A: bbox-centric NMS + fixed priority across layers.
3. Variant B: resolve conflicts with mask overlap / mask-first rules.
4. Score both on open and dense splits; compare duplicate and under-seg rates.
5. Accept, reject, or iterate fusion rule; update [[methods/merge-detections]].
```

### Prerequisites

- Working ECSeg (or proxy masks) and bbox layers on the same tiles
- Shared eval protocol with exp-001

### Gaps

- Exact fusion thresholds and priority table not yet in production docs
- Learned fusion out of scope for v1 (ADR-002 later)

## Evaluation protocol

- Same open vs dense and size bins as exp-001 / [[concepts/dense-stand-detection]]
- Compare Variant A vs B on dense primary; check open for regression

## Success criteria

- Dense metrics improve vs Variant A on agreed primary metric family (thresholds TBD in ADR-001)
- Open-stand regression within agreed tolerance (TBD)

## Kill criteria

- Mask-aware fusion does not improve dense metrics after agreed tuning budget
- Masks unavailable or too low quality to define Variant B → fall back to data/seg workstream

## Setup

Inputs: LM, CHM/DEIMv2, ECSeg masks. Variants A (bbox NMS) vs B (mask-aware).

## Runs

| Run | Config / baseline | Notes |
|-----|-------------------|-------|
| | | |

## Results

| Run | Metric | Value | Split | Notes |
|-----|--------|-------|-------|-------|
| | | | | |

## Conclusion

<!-- accept | reject | iterate -->

TBD

## Handoff to coding module

- Fusion variant specs (A/B) as above; implement in code repo only
- Return metrics + qualitative failure examples for wiki
- Do not commit weights or large overlays into this vault

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
- [[experiments/exp-001-per-layer-baselines]]
