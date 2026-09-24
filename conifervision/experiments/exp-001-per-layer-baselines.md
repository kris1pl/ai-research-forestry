---
title: exp-001 per-layer baselines (open vs dense)
type: Experiment
description: "H1 — Baseline measurements per ensemble layer before fusion, stratified by open vs dense stands and small vs large trees. First in queue: H1 → H3 → H2."
tags: [ensemble, baseline, evaluation, dense-stands, edgecrafter, H1]
status: stable
updated: 2026-09-21
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
**Status (2026-09-22):** weak-GT FT **smoke** done (1 AREA, hold-out golden); conclusion **iterate** — positive Δ, scale to multi-AREA. Kill criteria not triggered.

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
- RGB detection baseline — **done** (no-slice + SAHI 800/400/**200** tile ladder; no merge)
- RGB instance segmentation (ECSeg) — deferred to exp-003; interim SAM silver GT built for later seg work (not a fair H1 detector layer)

## Runs

All RGB runs use DEIMv2 `svk_full`. Dense only; **no merge**.

| Run ID | Mode | Slice | Conf | Role |
|--------|------|------:|-----:|------|
| `rgb_deimv2_sahi_800_001` | SAHI | 800 | 0.3 | **Primary** ceiling (overlap 0.2) |
| `rgb_deimv2_sahi_400_001` | SAHI | 400 | 0.3 | Small-tree ablation vs 800 |
| `rgb_deimv2_sahi_200_001` | SAHI | 200 | 0.3 | Smallest-tile ablation vs 400/800 |
| `rgb_deimv2_001` | no-slice | — | 0.5 | Ablation (understates small recall) |
| `rgb_deimv2_r_weak_sahi_{800,400,200}_001` | SAHI | 800/400/200 | 0.3 | **Smoke FT** — weak R GT (AREA 540 tiles), init `svk_full`; golden hold-out |
| `rgb_deimv2_r_weak_*` | SAHI | 800/400/200 | 0.3 | **Next** — multi-AREA weak FT (same protocol) |

Data prep: CVAT → golden; SAM full-image + clip-to-GT → silver (`instances_tree_sam_clipped.json` for exp-003).

> Oracle SAM (raw masks → boxes, GT-prompted) — **archived**, not an H1 detector ceiling. Silver under `research/annotations/silver/`.

## Results

Protocol: density=`dense`, small=<0.1% image area, IoU=0.5, n_gt=2534. No open split yet.

### Aggregate (all sizes)

| Run | P | R | F1 | n_pred |
|-----|--:|--:|---:|-------:|
| SAHI 800 (primary) | 0.78 | **0.134** | 0.229 | 433 |
| SAHI 400 | 0.69 | **0.199** | 0.308 | 734 |
| SAHI 200 | 0.51 | **0.349** | 0.414 | 1736 |
| no-slice | 0.89 | **0.012** | 0.024 | 35 |

### By size (AP / recall)

| Run                |   AP_small |   AP_large |   R_small |   R_large |
| ------------------ | ---------: | ---------: | --------: | --------: |
| SAHI 800 (primary) | **0.0299** | **0.4793** |     0.063 | **0.617** |
| SAHI 400           |  **0.068** |     0.4739 | **0.122** | **0.718** |
| SAHI 200           | **0.1567** |     0.3673 | **0.279** | **0.825** |
| no-slice           |        0.0 |     0.0909 |         — |         — |

### Primary run extras (SAHI 800)

| Metric | Value |
|--------|------:|
| under_segmentation_rate | 0.8662 |
| duplicate_rate | 0.0004 |

### Error taxonomy (RGB SAHI, dense)

- Dominant mode still **FN**; 800: FN=2195 FP=94; 400: FN=2031 FP=231; **200: FN=1650 FP=852** (dup≈0.011).
- Tile ladder R_small / AP_small: 800 → 0.063 / 0.03; 400 → 0.122 / 0.068; **200 → 0.279 / 0.157**.
- Cost of 200: P 0.78→0.51; AP_large 0.48→0.37 — more FP and weaker large-box AP.
- Implication: smaller tiles help small crowns but do not close the R-class gap (domain of `svk_full`). Keep **800** as default single-pass.

### Smoke FT Δ vs `svk_full` (2026-09-22) — provisional

Train: weak GT from AREA **540** only (tiled COCO + ad-hoc tile split); init `svk_full`; ~24 epochs. Eval: golden `kaxen_197_1` SAHI 800/400/200 conf 0.3 — **never in train**. Artifacts: `results/rgb_deimv2_r_weak_sahi_{800,400,200}_001/`.

| Slice | ΔP | ΔR | ΔF1 | ΔR_small | ΔAP_small | ΔR_large |
|------:|---:|---:|----:|---------:|----------:|---------:|
| 800 | +0.002 | **+0.019** | **+0.027** | +0.011 | +0.001 | **+0.074** |
| 400 | +0.003 | **+0.021** | **+0.025** | +0.020 | +0.006 | +0.025 |
| 200 | **+0.025** | +0.007 | +0.013 | +0.011 | **+0.042** | −0.022 |

Reading: **positive direction** (esp. 800/400: more recall at stable P). Absolute small-tree gap remains large (800 R_small still ~0.07). **Not** H1 success — smoke only. Next = multi-AREA weak FT, then re-ladder; merge still deferred. LM/CHM layers still pending for full H1.

### Statistical box comparison vs golden GT (2026-09-24) — matched pairs

Hypothesis: production weak labels (esp. local-maxima) often **under-cover** crowns → FT might learn systematically **too-small** boxes.

Protocol: IoU≥0.5 greedy match pred↔GT on golden `kaxen_197_1`; conf≥0.3. Script: `research/exp-001/analyze_box_size_vs_gt.py` → `results/box_size_vs_gt_r_weak.json`.

Definitions:
- `area` = area_pred / area_gt
- `covGT` = inter / area_gt (1 ⇒ GT fully inside pred)
- `covPr` = inter / area_pred
- `ctr` = center distance in px

#### Smoke FT (`r_weak`) vs baseline — medians (all matched)

| Slice | model | n | IoU | area | covGT | covPr | ctr_px |
|------:|-------|--:|----:|-----:|------:|------:|-------:|
| 800 | `svk_full` | 339 | 0.717 | **1.373** | 1.000 | 0.725 | 2.93 |
| 800 | `r_weak` | 387 | 0.727 | **1.351** | 1.000 | 0.736 | 3.05 |
| 400 | `svk_full` | 503 | 0.722 | **1.339** | 1.000 | 0.734 | 2.88 |
| 400 | `r_weak` | 555 | 0.731 | **1.315** | 1.000 | 0.750 | 2.81 |
| 200 | `svk_full` | 884 | 0.711 | **1.321** | 1.000 | 0.738 | 2.91 |
| 200 | `r_weak` | 901 | 0.717 | **1.293** | 0.997 | 0.751 | 2.97 |

#### `r_weak` area_pred/gt by GT size bin

| Slice | all | small | large |
|------:|----:|------:|------:|
| 800 | 1.351 | **1.454** | 1.298 |
| 400 | 1.315 | **1.370** | 1.242 |
| 200 | 1.293 | **1.329** | 1.221 |

Reading:
- **No shrink vs golden on TP matches** — median area ≈ **1.29–1.35**; `covGT` median ≈ **1.0** ⇒ matched GT almost always fully contained in pred (pred wraps GT).
- `covPr` ≈ 0.73–0.75 ⇒ ~25% of pred area is outside GT — consistent with mild oversize, not under-size.
- Centers well aligned (median ~3 px). IoU median ~0.71–0.73.
- Oversize is **stronger on small GT** (area med 1.33–1.45) than large (1.22–1.30).
- Smoke FT slightly **closer** to GT size than `svk_full` (area Δ ≈ −0.02); IoU slightly higher.
- At 200, `frac(area<1)` ≈12% (vs ≈9% baseline) — small under-size tail only.
- Caveat: matched TPs only; FNs still dominate (match-rate of GT: 15% @800 → 36% @200).

### Visual QA vs golden GT (2026-09-24)

Overlays: **lime = golden GT**, **red = smoke FT pred** (conf≥0.3), same tiles as eval.
Paths: `results/preds_rgb_deimv2_r_weak_sahi_{200,400,800}/overlays_vs_gt/` (script `visualize_coco_overlays.py --gt-ann-file …`). Assets (in vault): `experiments/assets/exp001_r_weak_vs_gt_*`.

Same tile `01_01`, SAHI ladder (800 → 400 → 200) — FN fills as slice shrinks:

![[exp001_r_weak_vs_gt_800_tile0101.jpg|700]]

*800 — sparse preds, many lime-only FNs*

![[exp001_r_weak_vs_gt_400_tile0101.jpg|700]]

*400 — more hits; red boxes still wrap GT*

![[exp001_r_weak_vs_gt_200_tile0101.jpg|700]]

*200 — denser coverage, more clutter/FP*

Extra tile at 400 (`01_03`):

![[exp001_r_weak_vs_gt_400_tile0103.jpg|700]]

Conclusions from QA + metrics:
- Dominant error remains **missed crowns (FN)** — many lime boxes without a red partner, especially at **800** (sparse preds vs dense GT).
- Where preds exist, red boxes typically **cover the crown at least as generously as GT** (often slightly larger) — aligns with median area_pred/gt > 1; no systematic “tight LM hole” on TPs.
- **200** fills more of the stand (higher recall) but adds clutter / FP; size bias still not “too small vs GT”.
- Practical takeaway: next gains should come from **more recall / multi-AREA FT**, not from “inflate boxes to fix LM shrink” on this hold-out.

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
conclusion: iterate  # smoke FT positive Δ; next: multi-AREA weak FT; merge deferred
kill_triggered: no
```

Artifacts: `results/rgb_deimv2_sahi_800_001/`, `results/rgb_deimv2_sahi_400_001/`, `results/rgb_deimv2_sahi_200_001/`, `results/rgb_deimv2_r_weak_sahi_{800,400,200}_001/`, `results/preds_rgb_deimv2_r_weak_sahi_{200,400,800}/overlays_vs_gt/`, `results/box_size_vs_gt_r_weak.json`, `results/rgb_deimv2_001/`, `notes.md`. Oracle SAM archived at `results/_archive/sam_oracle_raw_001/`.

## Conclusion

**iterate**

- Pipeline-realistic RGB (`svk_full` + SAHI **800**) on dense R: usable on **large** (R≈0.62), weak on **small** (AP_small≈0.03, R≈0.06).
- SAHI tile ladder 800→400→**200**: R_small 0.06→0.12→**0.28**, AP_small 0.03→0.07→**0.16**; P falls to ~0.51 at 200.
- **Smoke weak-GT FT (2026-09-22):** 1 AREA (540) → golden hold-out ladder. Positive Δ vs `svk_full` especially at **800/400** (ΔR ≈ +0.02, P stable; 800 ΔR_large ≈ +0.07). Absolute small gap remains (800 R_small ~0.07). Direction validated; **not** H1 closed.
- **Box stats + visual QA vs golden (2026-09-24):** matched TPs — median area_pred/gt ≈1.3, covGT≈1.0 (GT inside pred), centers ~3 px; small GT oversized more than large. Overlays confirm dominant **FN**. Do **not** prioritize anti-shrink inflation; prioritize multi-AREA FT / recall.
- No-slice understated the ceiling (R 0.012) — keep SAHI for H1 RGB reporting.
- **Next RGB step:** scale weak-GT FT to **multiple R AREAs** (same init/`svk_full`, golden hold-out); re-run SAHI 800/400/200 and report Δ vs this smoke + baseline. Run family: `rgb_deimv2_r_weak_*`.
- **Deferred:** multi-scale RGB merge (800+400+200) until after multi-AREA Δ; full fusion remains [[experiments/exp-002-merge-fusion-v1]].
- Success criteria **not met** yet (missing open slice + LM/CHM as separate layers; smoke FT only).
- Silver SAM (clipped) ready for exp-003 — not an H1 detector ceiling.

## Handoff to coding module

- Eval AREA (hold-out): `kaxen_197_1` (dense R) — do **not** use in train
- Smoke done: AREA 540 weak tiles + `rgb_deimv2_r_weak_sahi_*_001` on golden
- Next train: more R-class AREAs via `prepare_r_weak_coco_from_areas.py` (split by AREA, not tiles); exclude golden
- Init checkpoint: `gs://conifer-vision/big-trees/summer/models/detection/deimv2_dinov3_s_trees_svk_full/best_stg2.pth` (or continue from smoke FT weights)
- After multi-AREA FT: same SAHI 800/400/200 conf 0.3 → Δ vs baseline + vs smoke; ladder script `research/exp-001/run_rgb_deimv2_r_weak_sahi_ladder.sh`
- Layer list so far: RGB no-slice + SAHI 800/400/200 + smoke FT; LM / CHM+DEIMv2 as separate H1 layers still pending; ECSeg → exp-003
- Out of scope until multi-AREA Δ: multi-scale RGB merge, exp-002 fusion design
- After accept/iterate on scaled FT: human gate before exp-003

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[concepts/literature-map-dense-itd]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
- [[experiments/exp-003-rgb-seg-backend-ceiling]]
- [[experiments/exp-002-merge-fusion-v1]]
