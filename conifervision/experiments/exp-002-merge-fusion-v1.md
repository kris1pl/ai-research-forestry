---
title: exp-002 merge / fusion v1 (segmentation-aware)
type: Experiment
description: "H2 — First fusion design iteration: bbox-centric NMS vs mask-aware merge under dense stands. Run after H1 (exp-001) and preferably after H3 (exp-003) picks the mask backend."
tags: [ensemble, merge, fusion, dense-stands, H2]
status: stable
updated: 2026-08-24
area: "Same AREA eval set as exp-001; report open vs dense separately"
hypothesis: "In dense stands, mask-aware fusion rules (mask-first / mask-overlap conflict resolution) reduce duplicates and under-segmentation relative to bbox-only NMS with layer priorities, without catastrophic regression on open stands."
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
sources:
  - sources/paper-fsod-vfm
  - sources/paper-edgecrafter
generated:
  by: agent:conifervision-wiki
  at: 2026-08-24T12:00:00Z
---

# exp-002 merge / fusion v1 (segmentation-aware)

**Queue:** [[experiments/exp-001-per-layer-baselines]] (H1) → [[experiments/exp-003-rgb-seg-backend-ceiling]] (H3) → **H2 (this page)**.  
**Gate:** ADR-002 — sequence approved to run (see [[project/decisions]]). Do not treat as first GPU spend.

## Hypothesis

In dense stands, **mask-aware fusion rules** (mask-first / mask-overlap conflict resolution) reduce duplicates and under-segmentation relative to bbox-only NMS with layer priorities, without catastrophic regression on open stands.

## Motivation

- Depends on ceilings from [[experiments/exp-001-per-layer-baselines]]
- Prefer mask backend chosen in [[experiments/exp-003-rgb-seg-backend-ceiling]] (fallback: ECSeg if H3 skipped/killed with documented reason)
- Fusion stub: [[methods/merge-detections]]
- Overlap reweight idea: [[sources/paper-fsod-vfm]]
- Dense errors: [[concepts/dense-stand-detection]]
- Program: [[project/research-tree-detection-ensemble]] · loop: [[project/hypothesis-validation-loop]]

## Pseudocode

**Inputs:** candidate sets from LM, CHM/DEIMv2, RGB bbox (optional); masks from backend selected in exp-003 (or ECSeg); eval labels

**Outputs:** fused instance set; metrics vs Variant A (bbox NMS) and Variant B (mask-aware)

**Parameters:** NMS IoU / distance (TBD); mask-overlap rule (TBD); layer priority order (TBD)

```text
1. Require exp-001 baselines (or provisional ceilings).
2. Lock mask source from exp-003 recommendation (or documented ECSeg fallback).
3. Variant A: bbox-centric NMS + fixed priority across layers.
4. Variant B: resolve conflicts with mask overlap / mask-first rules.
5. Score both on open and dense splits; compare duplicate and under-seg rates.
6. Accept, reject, or iterate fusion rule; update [[methods/merge-detections]].
```

### Prerequisites

- exp-001 Results (at least provisional) on shared tiles
- Working masks from exp-003 winner or explicit fallback
- Shared eval protocol with exp-001

### Gaps

- Exact fusion thresholds and priority table not yet in production docs
- Learned fusion out of scope for v1 (future ADR)
- If exp-003 kill criteria fire, do not force Variant B as primary path

## Evaluation protocol

- Same open vs dense and size bins as exp-001 / [[concepts/dense-stand-detection]]
- Compare Variant A vs B on dense primary; check open for regression
- ADR-001 structure ([[project/decisions]])

## Success criteria

- Dense metrics improve vs Variant A on agreed primary metric family (thresholds TBD in ADR-001)
- Open-stand regression within agreed tolerance (TBD)

## Kill criteria

- Mask-aware fusion does not improve dense metrics after agreed tuning budget
- Masks unavailable or too low quality to define Variant B → fall back to data/seg workstream (exp-003 / Phase 3)

## Setup

Inputs: LM, CHM/DEIMv2, optional RGB boxes, masks from selected backend. Variants A (bbox NMS) vs B (mask-aware).

## Runs

| Run | Config / baseline | Notes |
|-----|-------------------|-------|
| A | bbox NMS + priorities | |
| B | mask-aware merge | mask backend: TBD from exp-003 |

## Results

| Run | Metric | Value | Split | Notes |
|-----|--------|-------|-------|-------|
| | | | | |

## Conclusion

<!-- accept | reject | iterate -->

TBD

## Handoff to coding module

- Fusion variant specs (A/B); mask backend id from exp-003
- Return metrics + qualitative failure examples for wiki
- Do not commit weights or large overlays into this vault

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[concepts/literature-map-dense-itd]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
- [[experiments/exp-001-per-layer-baselines]]
- [[experiments/exp-003-rgb-seg-backend-ceiling]]
