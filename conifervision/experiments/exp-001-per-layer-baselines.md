---
title: exp-001 per-layer baselines (open vs dense)
type: Experiment
description: "H1 — Baseline measurements per ensemble layer before fusion, stratified by open vs dense stands and small vs large trees. First in queue: H1 → H3 → H2."
tags: [ensemble, baseline, evaluation, dense-stands, edgecrafter, H1]
status: stable
updated: 2026-08-24
area: "AREA split TBD — stratify open vs dense; size bins per CHM/DEIMv2 layers"
hypothesis: "In dense stands, dominant failure modes differ from open stands; per-layer performance ceilings (LM, CHM/DEIMv2, RGB detection, RGB instance segmentation) on an open/dense split are a prerequisite for sensible fusion — a global AP without stratification hides the errors that matter before thinning."
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
sources:
  - sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al
  - sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests
  - sources/popescu-wynne-2004-seeing-the-trees
generated:
  by: agent:conifervision-wiki
  at: 2026-08-24T12:00:00Z
---

# exp-001 per-layer baselines (open vs dense)

**Queue:** **H1 (run first)** → [[experiments/exp-003-rgb-seg-backend-ceiling]] → [[experiments/exp-002-merge-fusion-v1]].  
**Gate:** ADR-002 — sequence approved to run (see [[project/decisions]]).

## Hypothesis

In dense stands, dominant failure modes differ from open stands; **per-layer performance ceilings** (LM, CHM/DEIMv2, RGB detection, RGB instance segmentation) on an open/dense split are a prerequisite for sensible fusion — a global AP without stratification hides the errors that matter before thinning.

## Motivation

- Program north star: [[project/research-tree-detection-ensemble]]
- Literature map Tier A: [[concepts/literature-map-dense-itd]]
- Density & tuning dominate method brand: [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]]
- Acquisition / CHM / ITD interactions: [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests]]
- Dense regime: [[concepts/dense-stand-detection]]
- Layers: [[methods/local-maxima]], [[methods/chm-detection]], [[methods/deimv2-canopy]], [[methods/edgecrafter-ecseg]]
- Loop: [[project/hypothesis-validation-loop]]

## Pseudocode

**Inputs:** orthophoto tiles; CHM / height layers; optional LM candidates; gold or proxy labels for eval AREA(s)

**Outputs:** per-layer metric tables stratified by open/dense and size bin; error taxonomy notes

**Parameters:** density tag definition (TBD); size-bin edges (align with production CHM layers, TBD if undocumented); confidence thresholds (TBD / production defaults)

```text
1. Define AREA eval set and open vs dense tags ([[concepts/dense-stand-detection]]).
2. For each layer in {LM, CHM+DEIMv2, RGB detection TBD, ECSeg (single backend for now)}:
   a. Run inference only (no fusion).
   b. Score metrics on open and dense splits, small and large bins.
3. Record failure modes (duplicates, under-segmentation, boundary errors).
4. Emit baseline ceilings → feed exp-003 (seg A/B) and exp-002 (fusion).
```

### Prerequisites

- Locked or provisional evaluation protocol; access to labeled or weakly labeled eval AREA outside this repo

### Gaps

- Exact dense/open threshold and metric formulas TBD until protocol page exists
- ECSeg checkpoint / few-shot recipe TBD ([[methods/edgecrafter-ecseg]]); multi-backend comparison deferred to exp-003

## Evaluation protocol

- Split: open vs dense — [[concepts/dense-stand-detection]]
- Size bins: CHM / DEIMv2 height layers
- Primary metrics: see frontmatter `metrics` (fill after first run)
- Align reporting with ADR-001 structure ([[project/decisions]])

## Success criteria

- Complete per-layer tables for at least one open and one dense AREA slice
- Written error taxonomy usable as input to exp-003 / exp-002

## Kill criteria

- Cannot obtain any dense-tagged eval labels within agreed effort → pause fusion/seg A/B and escalate data program (Phase 3)

## Setup

Planned runs (no fusion):

- Local maxima / LM baseline
- CHM + DEIMv2 baseline
- RGB detection baseline (if available)
- RGB instance segmentation (ECSeg) zero-shot / few-shot — ceiling only; backend bake-off is exp-003

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
- After accept/iterate: human gate before starting exp-003

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[concepts/literature-map-dense-itd]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
- [[experiments/exp-003-rgb-seg-backend-ceiling]]
- [[experiments/exp-002-merge-fusion-v1]]
