---
title: exp-001 per-layer baselines (open vs dense)
type: Experiment
description: "Baseline measurements per ensemble layer before fusion, stratified by open vs dense stands and small vs large trees."
tags: [ensemble, baseline, evaluation, dense-stands, edgecrafter]
status: stable
updated: 2026-08-24
area: "AREA split TBD — stratify open vs dense; size bins per CHM/DEIMv2 layers"
hypothesis: "Layer-wise performance ceilings and dense-specific error taxonomy are necessary inputs for robust fusion design; global (non-stratified) eval hides the failure modes that matter before thinning."
metrics:
  detection_ap_small: TBD
  detection_ap_large: TBD
  under_segmentation_rate: TBD
  duplicate_rate: TBD
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/edgecrafter-ecseg
  - methods/merge-detections
sources: []
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
---

# exp-001 per-layer baselines (open vs dense)

## Hypothesis

Dense-stand failures have different dominant error modes than open stands; therefore per-layer baselines stratified by open vs dense will drive a better fusion strategy than global (non-stratified) evaluation.

## Motivation

- Program north star: [[project/research-tree-detection-ensemble]]
- Dense regime: [[concepts/dense-stand-detection]]
- Layers: [[methods/local-maxima]], [[methods/chm-detection]], [[methods/deimv2-canopy]], [[methods/edgecrafter-ecseg]]
- Loop: [[project/hypothesis-validation-loop]]

## Pseudocode

**Inputs:** orthophoto tiles; CHM / height layers; optional LM candidates; gold or proxy labels for eval AREA(s)

**Outputs:** per-layer metric tables stratified by open/dense and size bin; error taxonomy notes

**Parameters:** density tag definition (TBD); size-bin edges (align with production CHM layers, TBD if undocumented); confidence thresholds (TBD / production defaults)

```text
1. Define AREA eval set and open vs dense tags ([[concepts/dense-stand-detection]]).
2. For each layer in {LM, CHM+DEIMv2, RGB detection TBD, ECSeg}:
   a. Run inference only (no fusion).
   b. Score metrics on open and dense splits, small and large bins.
3. Record failure modes (duplicates, under-segmentation, boundary errors).
4. Emit baseline ceilings for fusion design (exp-002).
```

### Prerequisites

- Locked or provisional evaluation protocol; access to labeled or weakly labeled eval AREA outside this repo

### Gaps

- Exact dense/open threshold and metric formulas TBD until protocol page exists
- ECSeg checkpoint / few-shot recipe TBD ([[methods/edgecrafter-ecseg]])

## Evaluation protocol

- Split: open vs dense — [[concepts/dense-stand-detection]]
- Size bins: CHM / DEIMv2 height layers
- Primary metrics: see frontmatter `metrics` (fill after first run)

## Success criteria

- Complete per-layer tables for at least one open and one dense AREA slice
- Written error taxonomy usable as input to fusion design

## Kill criteria

- Cannot obtain any dense-tagged eval labels within agreed effort → pause and escalate data program (Phase 3)

## Setup

Planned runs (no fusion):

- Local maxima / LM baseline
- CHM + DEIMv2 baseline
- RGB detection baseline (if available)
- RGB instance segmentation (ECSeg) zero-shot / few-shot

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

- Eval AREA IDs and label sources (describe; no invented Delta Lake paths)
- Layer list and any existing production defaults for DEIMv2/LM
- Return: filled Results table + short error taxonomy markdown for wiki update
- Out of scope here: weights, training loops, GPU orchestration

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
