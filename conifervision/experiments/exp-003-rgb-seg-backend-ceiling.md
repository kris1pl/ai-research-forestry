---
title: exp-003 RGB instance-seg backend ceiling (dense)
type: Experiment
description: "H3 — Compare RGB instance-segmentation backends (ECSeg vs StarDist-style vs SAM2-prompted) on the same dense tiles before locking a mask source for fusion."
tags: [ensemble, instance-segmentation, dense-stands, edgecrafter, stardist, sam2, H3]
status: stable
updated: 2026-08-24
area: "Same AREA eval tiles as exp-001 once available; prioritize dense split; report open for regression check"
hypothesis: "On the same dense tiles, the mask-quality ceiling of ECSeg (zero-/few-shot) vs a Tier A competitor (e.g. StarDist / SAM2-prompted) differs enough that choosing one backend before fusion changes later merge ROI more than adding another bbox detector."
metrics:
  mask_boundary_quality_dense: TBD
  under_segmentation_rate_dense: TBD
  over_segmentation_rate_dense: TBD
  detection_ap_dense: TBD
related_methods:
  - methods/edgecrafter-ecseg
  - methods/merge-detections
  - methods/deimv2-canopy
sources:
  - sources/paper-edgecrafter
  - sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main
  - sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025
  - sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1
generated:
  by: agent:conifervision-wiki
  at: 2026-08-24T12:00:00Z
---

# exp-003 RGB instance-seg backend ceiling (dense)

**Queue:** [[experiments/exp-001-per-layer-baselines]] (H1) → **H3 (this page)** → [[experiments/exp-002-merge-fusion-v1]] (H2).  
**Gate:** ADR-002 — sequence approved to run (see [[project/decisions]]). Prefer starting after exp-001 has at least provisional dense ceilings; may run narrowly in parallel on the same tiles if H1 data is ready.

## Hypothesis

On the same dense tiles, the **mask-quality ceiling** of ECSeg (zero-/few-shot) vs a Tier A competitor (e.g. StarDist / SAM2-prompted: Tong, TreePseCo, Chen) differs enough that **choosing one backend before fusion** changes later merge ROI more than adding another bbox detector.

## Motivation

- Avoid locking [[methods/edgecrafter-ecseg]] without a ceiling comparison ([[project/research-tree-detection-ensemble]])
- Literature map Tier A RGB crowns: [[concepts/literature-map-dense-itd]]
- [[sources/paper-edgecrafter]], [[sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main]], [[sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025]], [[sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1]]
- Dense errors: [[concepts/dense-stand-detection]]
- Feeds mask source for [[experiments/exp-002-merge-fusion-v1]]

## Pseudocode

**Inputs:** same RGB tiles (+ optional detector boxes as prompts for SAM-family); dense/open tags from exp-001 protocol; eval labels

**Outputs:** per-backend metric tables on dense (and open check); chosen backend recommendation for exp-002

**Parameters:** prompt strategy for SAM-family (TBD); confidence / post-process (TBD); input resolution (TBD / match ortho GSD)

```text
1. Freeze eval tiles and labels from exp-001 protocol (no fusion).
2. Backend A: ECSeg zero-shot / few-shot ([[methods/edgecrafter-ecseg]]).
3. Backend B: StarDist-style or equivalent sparse-label crown model (Tong lineage) — if runnable; else skip with Gaps note.
4. Backend C: SAM2-prompted crowns (DeepForest / detector boxes as prompts — Chen / TreePseCo lineage) — if runnable.
5. Score mask/instance metrics on dense; check open for gross failure.
6. Recommend single mask backend for exp-002 Variant B (or kill → data program).
```

### Prerequisites

- Shared tiles/labels with exp-001
- At least two backends runnable in the coding module; if only ECSeg runs, document and **iterate** (do not fake A/B)

### Gaps

- Exact trainable StarDist/TreePseCo recipes and weights live outside this wiki
- Numeric metric formulas TBD (ADR-001)
- Which competitor pair is mandatory vs optional — decide at human gate before GPU spend

## Evaluation protocol

- Primary: **dense** split ([[concepts/dense-stand-detection]])
- Secondary: open (regression / sanity)
- Size bins: same as exp-001 if available
- Prefer boundary-aware / under-seg / over-seg proxies in addition to detection AP (TBD)

## Success criteria

- Clear ranking or documented near-tie among runnable backends on dense
- Written recommendation of mask source for exp-002

## Kill criteria

- All backends in budget yield similarly weak / unusable masks on dense → prioritize gold/pseudo labels (Phase 3), do **not** proceed to exp-002 mask-aware fusion as primary bet

## Setup

Compare only instance-segmentation backends on RGB (optional box prompts). No LM/CHM fusion in this experiment.

## Runs

| Run | Config / baseline | Notes |
|-----|-------------------|-------|
| A | ECSeg | |
| B | StarDist-style (if available) | |
| C | SAM2-prompted (if available) | |

## Results

| Run | Metric | Value | Split | Notes |
|-----|--------|-------|-------|-------|
| | | | | |

## Conclusion

<!-- accept | reject | iterate -->

TBD

## Handoff to coding module

- Same AREA tiles as exp-001; list which backends are in scope for this sprint
- Return: Results table + recommended backend id for exp-002 + failure examples
- No weights committed to this vault
- After conclusion: human gate before exp-002

## Related

- [[experiments/exp-001-per-layer-baselines]]
- [[experiments/exp-002-merge-fusion-v1]]
- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/literature-map-dense-itd]]
- [[concepts/dense-stand-detection]]
- [[methods/edgecrafter-ecseg]]
- [[methods/merge-detections]]
