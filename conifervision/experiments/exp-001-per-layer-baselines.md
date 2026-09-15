---
title: exp-001 per-layer baselines (open vs dense)
type: Experiment
description: "H1 — Baseline measurements per ensemble layer before fusion, stratified by open vs dense stands and small vs large trees. First in queue: H1 → H3 → H2."
tags: [ensemble, baseline, evaluation, dense-stands, edgecrafter, H1]
status: stable
updated: 2026-09-15
area: "kaxen_197_1 (AREA 197, R-class / pre-thinning) — dense only so far; open GT TBD"
hypothesis: "In dense stands, dominant failure modes differ from open stands; per-layer performance ceilings (LM, CHM/DEIMv2, RGB detection, RGB instance segmentation) on an open/dense split are a prerequisite for sensible fusion — a global AP without stratification hides the errors that matter before thinning."
metrics:
  # Primary pipeline-realistic RGB: rgb_deimv2_sahi (svk_full + SAHI 800 / conf 0.3)
  detection_ap_small: 0.0299
  detection_ap_large: 0.4793
  under_segmentation_rate: 0.8662
  duplicate_rate: 0.0004
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
  at: 2026-09-15T12:00:00Z
---

# exp-001 per-layer baselines (open vs dense)

**Queue:** **H1 (run first)** → [[experiments/exp-003-rgb-seg-backend-ceiling]] → [[experiments/exp-002-merge-fusion-v1]].  
**Gate:** ADR-002 — sequence approved to run (see [[project/decisions]]).  
**Status (2026-09-15):** provisional **dense** baselines started; conclusion **iterate**. Kill criteria not triggered.

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

- **Open-stand** golden still missing (success asks for ≥1 open + ≥1 dense)
- LM preds and CHM+DEIMv2 R-band preds on same tiles — not run yet
- Size bins currently by **relative bbox area** (small < 0.1% of image), not CHM height layers
- ECSeg / multi-backend comparison deferred to exp-003

## Evaluation protocol

- Split: open vs dense — [[concepts/dense-stand-detection]] (current eval set = **dense only**, R-class / pre-thinning)
- Size bins (provisional): relative bbox area vs image; `small_max_rel_area_pct = 0.1`; IoU match = 0.5
- Primary metrics: frontmatter `metrics` (filled from `rgb_deimv2` dense run)
- Align reporting with ADR-001 structure ([[project/decisions]])

### Data / code (engineer repo)

Base: `conifervision-ai-train/`. `golden/` = human CVAT boxes; `silver/` = SAM masks (images symlink to golden).

- **Golden GT:** `research/annotations/golden/kaxen_197_1/annotations/instances_tree.json`
- **Images (5 tiles):** `research/annotations/golden/kaxen_197_1/images`
- **Silver seg (SAM ∩ GT):** `research/annotations/silver/kaxen_197_1/annotations/instances_tree_sam_clipped.json`
- **Eval harness:** `research/exp-001/eval_layers.py`, `manifest.yaml`
- **RGB no-slice:** `research/exp-001/run_rgb_deimv2.sh` → `results/preds_rgb_deimv2/`
- **RGB SAHI:** `research/exp-001/run_rgb_deimv2_sahi_800.sh` → `results/preds_rgb_deimv2_sahi_800/`

## Success criteria

- Complete per-layer tables for at least one open and one dense AREA slice
- Written error taxonomy usable as input to exp-003 / exp-002

## Kill criteria

- Cannot obtain any dense-tagged eval labels within agreed effort → pause fusion/seg A/B and escalate data program (Phase 3)

**Kill check (2026-09-15):** dense golden labels exist (`kaxen_197_1`, 2534 boxes) → **not triggered**.

## Setup

Planned runs (no fusion):

- Local maxima / LM baseline — **pending**
- CHM + DEIMv2 baseline — **pending**
- RGB detection baseline — **done** (no-slice + SAHI 800 primary + SAHI **400** small-tree ablation; no merge)
- RGB instance segmentation (ECSeg) — deferred to exp-003; interim SAM silver GT built for later seg work (not a fair H1 detector layer)

## Runs

All RGB runs use DEIMv2 `svk_full`. Dense only; **no merge**.

| Run ID | Mode | Slice | Conf | Role |
|--------|------|------:|-----:|------|
| `rgb_deimv2_sahi_800_001` | SAHI | 800 | 0.3 | **Primary** ceiling (overlap 0.2) |
| `rgb_deimv2_sahi_400_001` | SAHI | 400 | 0.3 | Small-tree ablation vs 800 |
| `rgb_deimv2_001` | no-slice | — | 0.5 | Ablation (understates small recall) |

Data prep: CVAT → golden; SAM full-image + clip-to-GT → silver (`instances_tree_sam_clipped.json` for exp-003).

> Oracle SAM (raw masks → boxes, GT-prompted) — **archived**, not an H1 detector ceiling. Silver under `research/annotations/silver/`.

## Results

Protocol: density=`dense`, small=<0.1% image area, IoU=0.5, n_gt=2534. No open split yet.

### Aggregate (all sizes)

| Run | P | R | F1 | n_pred |
|-----|--:|--:|---:|-------:|
| SAHI 800 (primary) | 0.78 | **0.134** | 0.229 | 433 |
| SAHI 400 | 0.69 | **0.199** | 0.308 | 734 |
| no-slice | 0.89 | **0.012** | 0.024 | 35 |

### By size (AP / recall)

| Run                |   AP_small |   AP_large |   R_small |   R_large |
| ------------------ | ---------: | ---------: | --------: | --------: |
| SAHI 800 (primary) | **0.0299** | **0.4793** |     0.063 | **0.617** |
| SAHI 400           |  **0.068** |     0.4739 | **0.122** | **0.718** |
| no-slice           |        0.0 |     0.0909 |         — |         — |

### Primary run extras (SAHI 800)

| Metric | Value |
|--------|------:|
| under_segmentation_rate | 0.8662 |
| duplicate_rate | 0.0004 |

### Error taxonomy (RGB SAHI, dense)

- Dominant mode still **FN**; SAHI 800: FN=2195, FP=94; SAHI 400: FN=2031, FP=231.
- Slice **400** ~doubles R_small (0.063 → 0.122) and lifts AP_small (0.03 → 0.068); AP_large ≈ unchanged (~0.47–0.48).
- Cost: lower precision (0.78 → 0.69) from more FP — expected with denser tiling.
- Implication: tile size matters for small crowns but **does not close** the R-class gap; keep 800 as default single-pass ceiling; dual-scale merge (800+400) is exp-002, not H1. Fine-tune / LM/CHM still needed.

### Return package (engineer) — primary SAHI run

```text
exp_id: exp-001
code_repo: conifervision-ai-train
code_git_sha: 7c055dc
entrypoints:
  - research/exp-001/eval_layers.py
  - research/exp-001/run_rgb_deimv2_sahi_800.sh
commands: python eval_layers.py --output-dir research/exp-001/results/rgb_deimv2_sahi_800_001
gcs_results: []
mlflow_run_ids: []
metrics:
  rgb_deimv2_sahi_800:
    detection_ap_small: 0.0299
    detection_ap_large: 0.4793
    under_segmentation_rate: 0.8662
    duplicate_rate: 0.0004
split_notes: kaxen_197_1 dense R. SAHI 800/0.3 vs prior no-slice ablation. No open GT yet.
conclusion: iterate
kill_triggered: no
```

Artifacts: `results/rgb_deimv2_sahi_800_001/`, `results/rgb_deimv2_sahi_400_001/`, `results/rgb_deimv2_001/`, `notes.md`. Oracle SAM archived at `results/_archive/sam_oracle_raw_001/`.

## Conclusion

**iterate**

- Pipeline-realistic RGB (`svk_full` + SAHI **800**) on dense R: usable on **large** (R≈0.62), weak on **small** (AP_small≈0.03, R≈0.06).
- SAHI **400** ablation: R_small ≈2× (→0.12), AP_small→0.068; still far from usable; more FP. Tile size helps but is not enough alone.
- No-slice understated the ceiling (R 0.012) — keep SAHI for H1 RGB reporting; dual-scale merge deferred to exp-002.
- Success criteria **not met** yet (missing open slice + LM/CHM layers).
- Next: LM and/or CHM+DEIMv2; open-stand golden; human gate before exp-003.
- Silver SAM (clipped) ready for exp-003 — not an H1 detector ceiling.

## Handoff to coding module

- Eval AREA: `kaxen_197_1` (dense R); open AREA still needed
- Layer list: RGB DEIMv2 no-slice + SAHI 800 + SAHI 400 done; LM, CHM+DEIMv2 pending; ECSeg → exp-003
- Return: Results + taxonomy above filled from local runs
- Out of scope here: weights, training loops, GPU orchestration details
- After accept/iterate: human gate before starting exp-003 (prefer more H1 layers first)

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[concepts/literature-map-dense-itd]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
- [[experiments/exp-003-rgb-seg-backend-ceiling]]
- [[experiments/exp-002-merge-fusion-v1]]
