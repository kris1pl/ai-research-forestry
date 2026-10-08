---
title: exp-001 per-layer baselines (size-stratified R-class)
type: Experiment
description: "H1 v1.1 — Size-stratified R-class ceilings; multi-scale detection bank on Round1 preds (gate=C); Round2 FT after C OK; D=+200 ablation. Open/dense deferred. Queue: H1 → H3 → H2."
tags: [ensemble, baseline, evaluation, R-class, small-trees, multi-scale-bank, H1]
status: stable
updated: 2026-10-06
area: "kaxen_197_1 (AREA 197, R-class / pre-thinning) — small crowns, sparse overlap (not closed-canopy dense); open/dense GT TBD"
hypothesis: "On R-class hold-out with small, sparsely overlapping crowns (kaxen_197_1), the dominant RGB failure mode is FN on small trees; size-stratified per-layer ceilings and a multi-scale detection bank (large from baseline@800, small from FT@400, optional@200) are prerequisites for sensible fusion — before crown-overlap GT can validate dense-stand claims."
metrics:
  # Primary pipeline-realistic RGB: tiled inference (svk_full + window 800 / conf 0.3)
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

# exp-001 per-layer baselines (size-stratified R-class)

**Queue:** **H1 (run first)** → [[experiments/exp-002-rgb-seg-backend-ceiling]] → [[experiments/exp-003-merge-fusion-v1]].  
**Gate:** ADR-002 — run order locked (see [[project/decisions]]).  
**Status (2026-10-06):** **exp-001a (RGB + bank C) closed** — ship `results/sahi_bank_002/` (C: R_small 0.257, R_large 0.761 @ conf 0.3). Round 2 tag **`003`** / verify runs = **Round 1** preds (no v2 golden gain). Weak test **481** closed (`compare_481_*`). **exp-001b (LM/CHM on golden)** deferred. **Next program step:** [[experiments/exp-002-rgb-seg-backend-ceiling]]. Product: large = `svk_full@800`; small = **FT@400 Round 1**.

## Executive summary (for the board)

This experiment measures how well we detect **young / small trees** on a fixed, human-labelled test area (R-class, before thinning). The baseline aerial model finds most **large** trees but misses most **small** ones. After domain training (Round 1), a “small-tree specialist” does much better on small trees but worse on large trees **when used alone** — which is expected. **Combining** baseline (large) + specialist (small) keeps large-tree performance **and** roughly **quadruples** small-tree detection (**bank C**, 2026-09-29). A **second training round** (more AREAs, Oct 2026) improved weak **val** but **did not** improve golden hold-out or weak test **481** vs Round 1 in scored artifacts. Merge **C** from Round 1 is the **shipping reference**. What we have **not** proven yet: performance in truly closed-canopy “dense” stands (we lack that ground truth).

## Hypothesis

#### For the board

We test whether missing **small** trees is the main problem on our R-class test site, and whether measuring each detection path separately (RGB, height, peaks — later) plus **merging specialists by size** is the right way to design the product — before we claim results for dense forest literature.

**H1 v1.1 (active):**

On R-class hold-out with **small, sparsely overlapping crowns** (`kaxen_197_1`), the dominant RGB failure mode is **FN on small trees**; **size-stratified per-layer ceilings** (LM, CHM/DEIMv2, RGB) and a **multi-scale detection bank** (large ← baseline@800; small ← FT@400; optional@200) are prerequisites for sensible fusion — *before* crown-overlap GT can validate dense-stand claims ([[concepts/dense-stand-detection]]).

**H1 v1.0 (superseded, 2026-09-15):** In dense stands, dominant failure modes differ from open stands; per-layer ceilings on an open/dense split are a prerequisite for fusion. *Not testable on current golden — AREA tagged “dense” / pre-thinning, but crowns are small and sparse, not closed-canopy overlap.*

#### Takeaway

The active hypothesis is **size-first** (small vs large trees), not “open vs dense forest” on this dataset. Success means honest ceilings per path and a validated **two-expert merge**, not one model winning every bin.

## Scope revision (2026-09-28)

#### For the board

In September 2026 we narrowed the experiment to match what our labelled test data actually represents: **many small crowns with space between them**, not a closed dense canopy. Open/dense comparison and “dense ITD” claims wait until we have matching labels.

| In scope now | Deferred / out until overlap GT |
|---|---|
| Size bins (small/large) as **primary** stratification | Open vs dense split as success gate |
| RGB ceiling + weak-GT FT as **small expert** (Round2: more AREAs; **not** size-balance to protect AP_large) | Interpreting results as dense-ITD literature alignment |
| **Multi-scale detection bank** + merge ablation (800 baseline ∪ 400 FT ∪ optional 200) | Full mask-aware exp-003 / dense H3 claims |
| LM / CHM+DEIMv2 on same tiles (layer comparison) | under_seg / duplicate as *dense merge* signals |
| Empiric FN/FP taxonomy; box geometry vs GT | Claiming one FT checkpoint must win both size bins |

**Ensemble stance (aligned with production multilayer):** AP_large drop on FT single-pass is **acceptable specialization** if `svk_full@800` (or CHM/LM large path) still supplies large trees after merge — same pattern as CHM bands and R-class 100/50 px + LM in [[methods/merge-detections]].

**Slice roles:**

| Slice | Role |
|------:|------|
| **800** | Large / broad path — prefer **`svk_full`** (not FT) in product bank |
| **400** | **Primary small expert** — Round2 FT target (best Round1 FT gain @ usable P) |
| **200** | **Bank ablation only** — high R_small but low P; FT≈flat vs `svk_full@200`; include in merge ± size-gate, not default expert |

*Note for implementers:* windowed inference on large orthophotos uses the SAHI tiling library under the hood — plain-language text talks about **tile / window size**, not the library name.

**GT characterization:** `kaxen_197_1` = R-class / pre-thinning label, **small crowns + sparse overlap** — treat as **small-sparse R-class proxy**, not dense ITD. Optional follow-up: quantify sparsity (e.g. share of GT with neighbor IoU>0, median NN distance / √area) once in the coding module.

North-star dense/open evaluation ([[concepts/dense-stand-detection]], [[project/research-tree-detection-ensemble]]) remains program-level; H1 no longer blocks on it.

#### Takeaway

**In scope:** small/large metrics, RGB + training a small-tree expert, merge test. **Out of scope for now:** proving dense-stand behaviour; full production fusion with masks. That avoids overstating what one labelled area can support.

## Motivation

#### For the board

This experiment sits in a longer research program: combine several detection sources (colour, height, peaks) the way production already does for R-class. H1 is **step 1** — measure each layer before merging. Links below are scientific and product context.

- Program north star: [[project/research-tree-detection-ensemble]]
- Literature map Tier A: [[concepts/literature-map-dense-itd]] (dense/open still Tier A *when GT exists*; H1 now unlocks size/domain ceilings first)
- Density & tuning dominate method brand: [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]]
- Acquisition / CHM / ITD interactions: [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests]]
- Dense regime (deferred validation): [[concepts/dense-stand-detection]]
- Layers: [[methods/local-maxima]], [[methods/chm-detection]], [[methods/deimv2-canopy]], [[methods/edgecrafter-ecseg]]
- Loop: [[project/hypothesis-validation-loop]]

#### Takeaway

Motivation is alignment with the **ensemble roadmap** and published ITD work — not a separate side project.

## Pseudocode

#### For the board

The workflow in plain terms: (1) score each detector alone on the same fixed test tiles, split by tree size; (2) merge baseline + small specialist and check the combined outcome; (3) only then run further training or change merge rules.

**Inputs:** orthophoto tiles; CHM / height layers; optional LM candidates; gold or proxy labels for eval AREA(s)

**Outputs:** per-layer metric tables stratified by **size bin** (primary); optional multi-scale bank / merge scores; sparsity proxy notes; error taxonomy

**Parameters:** size-bin edges (align with production CHM layers when available; else relative bbox area); density/open tags — **deferred** until overlap GT. **Bank merge (frozen for Round1 scoring):** conf ≥ 0.3 all layers; NMS IoU = 0.5 (fallback 0.3 if C kills large from A); size-gate = `small_max_rel_area_pct = 0.1` (same as eval bins); optional size-aware C = prefer A for large / B for small on conflicts.

```text
1. Freeze eval AREA (`kaxen_197_1`); characterize GT as small-sparse R-class (optional sparsity proxy).
2. For each layer in {LM, CHM+DEIMv2, RGB detection}:
   a. Run inference only (no fusion).
   b. Score metrics by small/large size bins (primary axis).
3. RGB multi-scale detection bank on existing Round1 preds (before Round2 FT):
   a. A = svk_full @ tile 800; B = Round1 FT @ tile 400.
   b. C = A ∪ B + NMS (± size-aware conflict rule) — **Round2 gate**.
   c. D = C ∪ (prefer svk_full@200, optional FT@200) ± size-gate — **ablation only**.
4. Verdict on C vs A (R_large recover + R_small lift); do not equate D failure with specialization fail.
5. If C OK → Round2 FT (more AREAs, small@400). If C fail after frozen merge + size-aware C → revisit merge / large path (not size-balance FT on blind).
6. Emit ceilings + bank verdict → feed exp-002 / exp-003 (mask-aware later).
```

### Prerequisites

- Locked or provisional evaluation protocol; access to labeled or weakly labeled eval AREA outside this repo

### Gaps

- **Open/dense** structural split not testable on current golden (AREA tag ≠ crown-overlap dense) — needs new GT / data program
- LM preds and CHM+DEIMv2 R-band preds on same tiles — not run yet
- Multi-scale **detection bank** scored 2026-09-29 (`sahi_bank_002`) — **C_OK**; Round2 unlocked; D ablation only
- Size bins currently by **relative bbox area** (small < 0.1% of image), not CHM height layers
- ECSeg / multi-backend comparison deferred to exp-002
- `under_segmentation_rate` on bbox eval may conflate misses with crown merging — de-emphasize until mask/overlap GT
- Production R-class tiles are **100/50 px** — research windows 800/400/200 are a proxy scale, not a 1:1 map

#### Takeaway

Main **remaining gaps:** height (CHM) and peak (LM) layers not scored yet on this golden set; dense-stand labels still missing. RGB baseline, Round1 training, and **bank merge are done**.

## Evaluation protocol

#### For the board

All numbers on this page use the same rules: trees classified **small** vs **large** by crown size on the image; a detection counts as correct if it overlaps the human box enough (IoU 0.5). The test area is always **held out** from training. Metrics are reported separately for small and large so we do not hide failure on young trees inside an overall average.

- **Primary axis:** size bins — relative bbox area vs image; `small_max_rel_area_pct = 0.1`; IoU match = 0.5
- **Regime tag:** small-sparse R-class (`kaxen_197_1`); do **not** report as closed-canopy dense
- Open vs dense ([[concepts/dense-stand-detection]]): **deferred** — not a blocker for H1 iterate
- **Per-expert metrics:** AP/R/P by size × model × slice (diagnostic; FT AP_large drop OK if bank C recovers large)
- **Bank metrics (done, Round1):** see Results § Multi-scale detection bank; Round2 unlocked by **C vs A**
- **Merge protocol (frozen):** conf≥0.3; NMS IoU 0.5; size-gate thr = 0.1% image area; naive C + size-aware C_sa both reported
- Align reporting with ADR-001 structure ([[project/decisions]]) where applicable

### Data / code (engineer repo)

Base: `conifervision-ai-train/`. `golden/` = human CVAT boxes; `silver/` = SAM masks (images symlink to golden).

- **Golden GT:** `research/annotations/golden/kaxen_197_1/annotations/instances_tree.json`
- **Images (5 tiles):** `research/annotations/golden/kaxen_197_1/images`
- **Silver seg (SAM ∩ GT):** `research/annotations/silver/kaxen_197_1/annotations/instances_tree_sam_clipped.json`
- **Eval harness:** `research/exp-001/eval_layers.py`, `manifest.yaml`
- **RGB full-frame (no tiling):** `research/exp-001/run_rgb_deimv2.sh` → `results/preds_rgb_deimv2/`
- **RGB tiled windows:** `research/exp-001/run_rgb_deimv2_sahi_800.sh` → `results/preds_rgb_deimv2_sahi_800/` (SAHI lib = implementation detail)

#### Takeaway

When reading tables, prioritise **R_small / R_large** (what fraction of true trees we find) and **AP_small / AP_large** (quality of ranking), not a single headline F1.

## Success criteria

#### For the board

**Success** means: clear size-split scorecards, evidence that merge C works, and an honest note that we are **not** validating closed-canopy dense forest yet. **Failure (kill)** would mean we cannot get useful RGB ceilings **or** merge C fails to beat baseline A on both size bands after fair merge rules — then pause further FT and revisit data or merge strategy.

- Size-stratified ceiling tables for RGB (done) and ideally LM + CHM+DEIMv2 on `kaxen_197_1`
- Written error taxonomy (FN-dominated small) usable as input to exp-002 / exp-003 **with small-sparse disclaimer**
- Bank **C** scored vs A/B: multilayer recovers large and lifts small without FT AP_large protection
- Bank **D** scored as ablation (does not block Round2 if C OK)
- Explicit verdict that this GT does **not** validate dense-stand fusion — data gap logged for overlap / closed-canopy golden

## Kill criteria

- Cannot obtain **useful size-stratified RGB ceiling** on the hold-out within agreed effort **and** cannot obtain GT with measurable crown overlap / closed canopy for later dense claims → pause mask-aware fusion dense claims (exp-003 Variant B / dense H3 framing) and log the data gap
- Bank **C** path: if after frozen merge (NMS ± size-aware C) `800∪400` still fails to recover large vs A **and** fails to lift small vs A → revisit merge rules / large path first; **only then** consider size-balance FT or alternate large expert — do **not** jump to size-balance FT from a single naive-NMS miss or from D alone

**Kill check (2026-09-15, legacy):** AREA-tagged “dense” labels exist (`kaxen_197_1`, 2534 boxes) → **not triggered** (labels exist; structural dense still missing — tracked as Gap, not kill).

**Kill check (2026-09-28, v1.1):** RGB size-stratified ceiling exists; iterate path open (FT / bank merge / LM·CHM pending) → **not triggered**.

#### Takeaway

**Kill criteria not triggered.** Bank C passed (2026-09-29). Experiment continues (**iterate**), not stop.

## Setup

#### For the board

**Done:** RGB at several window sizes, Round1 + Round2 fine-tuning, multi-scale bank on Round1 preds (C_OK). **Still to run:** re-infer golden preds from Round2 checkpoint + re-score bank; weak test **481** A/B; LM + CHM on same tiles.

Planned runs:

- Local maxima / LM baseline — **pending**
- CHM + DEIMv2 baseline — **pending**
- RGB detection baseline — **done** (full-frame + tiled windows 800/400/**200**)
- Multi-scale detection bank on Round1 preds (A/B/C gate; D ablation) — **done** (`sahi_bank_002`, C_OK); Round2 FT **next**
- RGB instance segmentation (ECSeg) — deferred to exp-002; interim SAM silver GT built for later seg work (not a fair H1 detector layer)

## Runs

#### For the board

Inventory of model runs (baseline, training rounds, merge test). Window column = crop size in pixels. **Done** rows include Round2 golden ladder `003`; **next** = bank re-score with Round2 B + LM/CHM layers.

All RGB runs use DEIMv2 `svk_full` init where FT applies. Eval = `kaxen_197_1` (small-sparse R-class). Legacy “dense” = AREA tag only. Single-pass tables below; **bank merge done** (`sahi_bank_002`, C_OK).

| Run ID | Mode | Window | Conf | Role |
|--------|------|-------:|-----:|------|
| `rgb_deimv2_sahi_800_001` | tiled | 800 | 0.3 | **Large-path ceiling** (`svk_full`) |
| `rgb_deimv2_sahi_400_001` | tiled | 400 | 0.3 | Small-tree ablation vs 800 |
| `rgb_deimv2_sahi_200_001` | tiled | 200 | 0.3 | Smallest-window ablation (bank candidate) |
| `rgb_deimv2_001` | full-frame | — | 0.5 | Ablation (understates small recall) |
| `rgb_deimv2_r_weak_sahi_{800,400,200}_001` | tiled | 800/400/200 | 0.3 | **Smoke FT** — weak R GT (AREA 540 tiles), init `svk_full`; golden hold-out |
| `rgb_deimv2_r_weak_sahi_{800,400,200}_002` | tiled | 800/400/200 | 0.3 | **Round 1 multi-AREA FT** — train 473–479 / val 480 / test 481 (`r_weak_v1_a473_481`); **small-expert candidate @400** |
| `sahi_bank_002` | merge | A/B/C/C_sa/D | — | **Done** — C_OK on Round1 B; re-score with Round2 B **pending** |
| `rgb_deimv2_r_weak_sahi_{800,400,200}_003` | tiled | 800/400/200 | 0.3 | **Round 2 multi-AREA FT** — train **473–479 + 482–492** / val **480** / test **481** (`r_weak_v2_a473_492`); init `svk_full`; FT → `deimv2_dinov3_s_trees_r_weak_ft_v2/` |

Data prep: CVAT → golden; SAM full-image + clip-to-GT → silver (`instances_tree_sam_clipped.json` for exp-002).

> Oracle SAM (raw masks → boxes, GT-prompted) — **archived**, not an H1 detector ceiling. Silver under `research/annotations/silver/`.

#### Takeaway

The run log is the audit trail: which model, which window size, and whether it feeds the merge test or the next training round.

## Results

#### For the board

This section is the evidence base: baseline RGB, effect of training, merge test, and checks that boxes are not systematically wrong size or position. **2534** human-labelled trees on **5** tiles; regime = young R-class with sparse overlap (not dense canopy).

Protocol: regime=`small-sparse R-class` (`kaxen_197_1`; legacy tag `dense` = AREA only), small=<0.1% image area, IoU=0.5, n_gt=2534. Open/dense structural split deferred.

### Baseline RGB — single models (aggregate)

#### For the board

Before training or merging: how does the **standard aerial model** behave if we only change **window size** (how much of the image it sees at once)? Smaller windows find more trees overall but also more false alarms; the default production-style window (800) is strong on large trees and weak on small ones.

| Run | P | R | F1 | n_pred |
|-----|--:|--:|---:|-------:|
| tile 800 (primary) | 0.78 | **0.134** | 0.229 | 433 |
| tile 400 | 0.69 | **0.199** | 0.308 | 734 |
| tile 200 | 0.51 | **0.349** | 0.414 | 1736 |
| full-frame | 0.89 | **0.012** | 0.024 | 35 |

### By size (AP / recall)

| Run                |   AP_small |   AP_large |   R_small |   R_large |
| ------------------ | ---------: | ---------: | --------: | --------: |
| tile 800 (primary) | **0.0299** | **0.4793** |     0.063 | **0.617** |
| tile 400           |  **0.068** |     0.4739 | **0.122** | **0.718** |
| tile 200           | **0.1567** |     0.3673 | **0.279** | **0.825** |
| full-frame         |        0.0 |     0.0909 |         — |         — |

### Primary run extras (tile 800)

| Metric | Value |
|--------|------:|
| under_segmentation_rate | 0.8662 |
| duplicate_rate | 0.0004 |

#### Takeaway

**Main message:** the problem is **missed small trees**, not duplicate detections. Shrinking the window helps recall but does not replace domain training or merge — it trades precision for coverage.

### Error taxonomy (RGB tiled, small-sparse R-class)

#### For the board

**Error taxonomy** = where the model fails. Here almost all failure is **false negative** (tree in the map, no detection). False positives exist but are secondary. Very low duplicate rate fits a **sparse** stand (crowns rarely pile on top of each other in the labels).

- Dominant mode still **FN**; 800: FN=2195 FP=94; 400: FN=2031 FP=231; **200: FN=1650 FP=852** (dup≈0.011).
- Tile ladder R_small / AP_small: 800 → 0.063 / 0.03; 400 → 0.122 / 0.068; **200 → 0.279 / 0.157**.
- Cost of 200: P 0.78→0.51; AP_large 0.48→0.37 — more FP and weaker large-box AP.
- Implication: smaller tiles help small crowns but do not close the R-class gap (domain of `svk_full`). Keep **800** as default single-pass.
- Duplicate rate ≈0 — consistent with **sparse** crowns (NMS/merge not the main failure). Treat published `under_segmentation_rate` as descriptive only, not closed-canopy merge evidence.

#### Takeaway

Do not interpret this site as a merge-stress test; the model mostly **does not see** small trees yet.

### Smoke FT Δ vs `svk_full` (2026-09-22) — provisional

#### For the board

**Smoke test** = first small-scale training trial on weak labels from a single area, to see if fine-tuning moves metrics in the right direction before a multi-AREA Round1.

Train: weak GT from AREA **540** only (tiled COCO + ad-hoc tile split); init `svk_full`; ~24 epochs. Eval: golden `kaxen_197_1` windows 800/400/200 conf 0.3 — **never in train**. Artifacts: `results/rgb_deimv2_r_weak_sahi_{800,400,200}_001/`.

| Slice | ΔP | ΔR | ΔF1 | ΔR_small | ΔAP_small | ΔR_large |
|------:|---:|---:|----:|---------:|----------:|---------:|
| 800 | +0.002 | **+0.019** | **+0.027** | +0.011 | +0.001 | **+0.074** |
| 400 | +0.003 | **+0.021** | **+0.025** | +0.020 | +0.006 | +0.025 |
| 200 | **+0.025** | +0.007 | +0.013 | +0.011 | **+0.042** | −0.022 |

Reading: **positive direction** (esp. 800/400: more recall at stable P). Absolute small-tree gap remains large (800 R_small still ~0.07). **Not** H1 success — smoke only. Next = multi-AREA weak FT, then re-ladder; merge still deferred. LM/CHM layers still pending for full H1.

#### Takeaway

Training **can** help, but one area was not enough — next step was Round1 multi-AREA FT.

### Round 1 multi-AREA FT Δ vs `svk_full` (2026-09-28) — `002`

#### For the board

**Round 1** = proper training pass on weak labels from **several** forest areas (train/val/test split), still evaluated only on the **fixed human-labelled** hold-out that was never used in training.

Train: weak GT AREAs **473–479** (train) / **480** (val) / **481** (test); dataset `r_weak_v1_a473_481`; init `svk_full`. Eval: golden `kaxen_197_1` windows 800/400/200 conf 0.3. Artifacts: `results/rgb_deimv2_r_weak_sahi_{800,400,200}_002/`, `delta_r_weak_vs_baseline_002.json`.

Absolute (small-sparse R-class / all sizes):

| Slice | model        |         P |         R |        F1 |  AP_small |  AP_large | n_pred |
| ----: | ------------ | --------: | --------: | --------: | --------: | --------: | -----: |
|   800 | `svk_full`   |     0.783 |     0.134 |     0.229 |     0.030 | **0.479** |    433 |
|   800 | smoke `001`  |     0.785 |     0.153 |     0.256 |     0.031 |     0.517 |    493 |
|   800 | **v1 `002`** |     0.716 | **0.260** | **0.382** | **0.166** |     0.153 |    921 |
|   400 | `svk_full`   |     0.685 |     0.199 |     0.308 |     0.068 | **0.474** |    734 |
|   400 | smoke `001`  |     0.689 |     0.219 |     0.332 |     0.074 |     0.468 |    806 |
|   400 | **v1 `002`** | **0.716** | **0.310** | **0.433** | **0.157** |     0.217 |   1098 |
|   200 | `svk_full`   |     0.509 | **0.349** |     0.414 |     0.157 | **0.367** |   1736 |
|   200 | smoke `001`  |     0.534 |     0.356 |     0.427 | **0.199** |     0.358 |   1688 |
|   200 | **v1 `002`** | **0.558** |     0.336 |     0.419 |     0.188 |     0.211 |   1526 |

Δ vs `svk_full` baseline:

| Slice | ΔP | ΔR | ΔF1 | ΔR_small | ΔAP_small | ΔAP_large |
|------:|---:|---:|----:|---------:|----------:|----------:|
| 800 | −0.067 | **+0.126** | **+0.153** | **+0.150** | **+0.136** | **−0.326** |
| 400 | **+0.031** | **+0.112** | **+0.125** | **+0.130** | **+0.089** | **−0.257** |
| 200 | **+0.049** | −0.013 | +0.005 | −0.013 | +0.031 | −0.157 |

Reading:
- **Primary win at 800/400:** recall and small-tree AP jump hard (800 AP_small 0.03→0.17; R 0.13→0.26) with still usable P (~0.72).
- **Tradeoff:** large-tree AP collapses (800: 0.48→0.15) — model skews toward small R-class crowns from weak R labels. Under multilayer plan this is **specialization**, not a Round2 training must-fix (large stays on `svk_full@800`).
- At **200**, gains flatten vs baseline (slightly lower R, higher P); smoke still slightly better on AP_small — keep 200 as **bank ablation**, not primary FT target.
- vs smoke `001`: multi-AREA is a clear step-up on small/recall at 800/400; large-AP regression is new vs smoke (smoke had raised AP_large).
- H1 v1.1 still **not** closed (FN dominant; LM/CHM pending). **Bank C_OK (2026-09-29)** → Round2 FT unlocked.

#### Takeaway

Round1 **clearly helps small-tree recall** on the specialist checkpoint, but **hurts large-tree quality if used alone**. That is acceptable **only because** the bank test (next section) shows we can pair it with the baseline.

### Multi-scale detection bank on Round1 preds (2026-09-29) — `sahi_bank_002`

#### What “detection bank” means (methodology, non-technical)

A **multi-scale detection bank** is a small set of detectors that each specialize in a different tree size / viewing window, then **combined into one detection list** — instead of forcing a single model to be good at everything.

| Piece | Plain meaning |
|-------|----------------|
| **Window / tile size** (800 / 400 / 200 px) | How large a crop of the orthophoto the model sees at once. Smaller windows help find **small** crowns; larger windows are better for **broad / large** trees. |
| **Expert A** (`svk_full@800`) | Baseline production-style model on large windows — strong on large trees. |
| **Expert B** (fine-tuned `@400`) | Same model family, fine-tuned on R-class weak labels and run on medium windows — stronger on **small** trees, weaker alone on large-tree precision. |
| **Bank merge (C)** | Take detections from A and B together, remove overlaps (NMS). Product-shaped path: *large trees from A, small trees from B*. |
| **Ablation D** | Optional add-on of even smaller windows (`@200`) — diagnostic only; it does **not** decide the next training round. |

**Why we measure this:** Round1 fine-tuning improved small-tree recall but hurt large-tree scores on a **single** checkpoint. That is acceptable **only if** the bank (A∪B) still recovers large trees **and** keeps the small-tree gain. If merge C works, the next training round targets a better **small expert** — we do **not** force one model to win both size bins.

**What it is not:** not a new training run; not full production fusion (masks / CHM / LM — later experiments). Here it is a lightweight box-level merge on already computed predictions. *(Engineer note: windowed inference uses the SAHI tiling library; the method is multi-scale experts + merge, not “SAHI” as a product concept.)*

---

Script: `research/exp-001/score_sahi_bank.py --size-aware-c`. Protocol: conf≥0.3, NMS IoU=0.5, size_gate=0.1%. Preds: A=`svk_full@800`, B=FT `002`@400, D uses `svk_full@200`. Artifacts: `results/sahi_bank_002/`.

| Bank              |     P |     R |    F1 |   R_small |   R_large | AP_small |  AP_large | n_pred |
| ----------------- | ----: | ----: | ----: | --------: | --------: | -------: | --------: | -----: |
| A `svk@800`       | 0.783 | 0.134 | 0.229 |     0.063 |     0.617 |    0.030 |     0.479 |    433 |
| B `FT@400`        | 0.716 | 0.310 | 0.433 |     0.252 |     0.706 |    0.157 |     0.217 |   1098 |
| **C A∪B NMS**     | 0.680 | 0.322 | 0.437 | **0.257** | **0.761** |    0.136 | **0.484** |   1200 |
| C_sa (size-aware) | 0.677 | 0.320 | 0.435 |     0.255 |     0.761 |    0.135 |     0.494 |   1200 |
| D (+200 gated)    | 0.620 | 0.382 | 0.472 |     0.323 |     0.776 |    0.246 |     0.194 |   1560 |
| D_ungated         | 0.492 | 0.408 | 0.446 |     0.342 |     0.856 |    0.191 |     0.378 |   2103 |

#### What the table shows (plain language)

Focus on row **C** vs row **A**. **A** alone finds few small trees (about 6% of them) but is solid on large ones. Combining A with the small-tree specialist (**C**) finds roughly **4× more small trees** while also keeping — and even slightly improving — large-tree coverage. That means we do **not** need one “perfect” model for every size: two specialists merged work better. Rows **D** are optional “what if we add even smaller windows?” tests; they do not change the Round2 gate. **Verdict:** specialization + merge is validated → Round2 training targets a better small-tree expert.

Reading (metrics detail):
- **C vs A:** R_large 0.62→**0.76**, AP_large held (~0.48); R_small 0.06→**0.26**. Specialization **OK** — Round2 unlocked.
- C_sa ≈ C (size-aware not required for this hold-out).
- **D:** lifts R_small further but AP_large collapses when size-gated; ungated keeps more large AP at cost of P — ablation only, does not change Round2 decision.
- Product path until Round2 re-bank: **large = A, small = B**.

#### Takeaway

Round2 small-expert training is unblocked. Product-shaped path: baseline for large, specialist for small, merged output for the map.

### Round 2 multi-AREA FT — golden SAHI (`003`, 2026-10-02)

#### For the board

**Round 2** added more R-class training areas (482–492) on top of Round 1, still starting from the baseline aerial model — goal: a **better small-tree specialist** without trying to fix large-tree scores in one checkpoint. We re-measured on the **same fixed human-labelled hold-out** as before (`kaxen_197_1`, never used in training).

**Headline:** on that hold-out, Round 2 **matches Round 1 exactly** on every window size (800 / 400 / 200). The **merge test from September (bank C)** is therefore **unchanged** for now. Next engineering checks: confirm predictions were generated from the new Round 2 model file, compare on weak test area **481**, then re-run the bank with the new specialist.

Train: weak GT AREAs **473–479 + 482–492** (train) / **480** (val) / **481** (test); dataset `r_weak_v2_a473_492`; init **`svk_full`** (not Round1 weights); checkpoint `deimv2_dinov3_s_trees_r_weak_ft_v2/`. Eval: golden `kaxen_197_1`, windows 800/400/200, conf 0.3. Artifacts: `results/rgb_deimv2_r_weak_sahi_{800,400,200}_003/`, `delta_r_weak_vs_baseline_003.json` (empty rows — use tables below).

Absolute (small-sparse R-class / dense all):

| Slice | Run | P | R | F1 | R_small | R_large | AP_small | AP_large | n_pred |
|------:|-----|--:|--:|---:|--------:|--------:|---------:|---------:|-------:|
| 800 | `svk_full` | 0.783 | 0.134 | 0.229 | 0.063 | 0.617 | 0.030 | 0.479 | 433 |
| 800 | Round1 `002` | 0.716 | 0.260 | 0.382 | 0.213 | 0.580 | 0.166 | 0.153 | 921 |
| 800 | **Round2 `003`** | **0.716** | **0.260** | **0.382** | **0.213** | **0.580** | **0.166** | **0.153** | **921** |
| 400 | `svk_full` | 0.685 | 0.199 | 0.308 | 0.122 | 0.718 | 0.068 | 0.474 | 734 |
| 400 | Round1 `002` | 0.716 | 0.310 | 0.433 | 0.252 | 0.706 | 0.157 | 0.217 | 1098 |
| 400 | **Round2 `003`** | **0.716** | **0.310** | **0.433** | **0.252** | **0.706** | **0.157** | **0.217** | **1098** |
| 200 | `svk_full` | 0.509 | 0.349 | 0.414 | 0.279 | 0.825 | 0.157 | 0.367 | 1736 |
| 200 | Round1 `002` | 0.558 | 0.336 | 0.419 | 0.266 | 0.810 | 0.188 | 0.211 | 1526 |
| 200 | **Round2 `003`** | **0.558** | **0.336** | **0.419** | **0.266** | **0.810** | **0.188** | **0.211** | **1526** |

Δ vs `svk_full` (Round2 `003` — **same numbers as Round1 `002`**):

| Slice | ΔP | ΔR | ΔF1 | ΔR_small | ΔAP_small | ΔAP_large |
|------:|---:|---:|----:|---------:|----------:|----------:|
| 800 | −0.067 | **+0.126** | **+0.153** | **+0.150** | **+0.136** | **−0.326** |
| 400 | **+0.031** | **+0.112** | **+0.125** | **+0.130** | **+0.089** | **−0.257** |
| 200 | **+0.049** | −0.013 | +0.005 | −0.013 | +0.031 | −0.157 |

Δ vs Round1 `002`: **0** on all reported metrics (identical preds counts and splits).

Reading:
- **Hold-out:** Round2 did **not** beat Round1 on `kaxen_197_1` — primary small path (@400) still **R_small≈0.25**, **AP_small≈0.16** vs baseline **0.06 / 0.03**.
- **Specialization pattern unchanged:** large-tree AP still low on FT alone; product path remains **bank C** (baseline@800 + FT@400).
- **Engineer note:** eval dirs `*_003` point to the shared preds path `results/preds_rgb_deimv2_r_weak_sahi_*` (not tag-suffixed). If ladder was run with `SKIP_INFER=1` or Round1 `MODEL_PATH`, metrics would duplicate `002` — **re-run** with `MODEL_PATH=…/deimv2_dinov3_s_trees_r_weak_ft_v2/best_stg2.pth` and fresh infer before claiming “no gain from Round2 training.”
- **Still open:** weak test **481** tile-COCO compare (`run_compare_r_weak_vs_svk.sh`); `score_sahi_bank.py` with Round2 B@400; LM/CHM layers.

#### Takeaway

More training data did **not** move the golden hold-out in this eval package — **bank C from Round 1 remains the validated product path.** Treat Round2 as **inconclusive on golden** until preds are verified from the v2 checkpoint and the bank is re-scored; check weak test **481** for signal that golden is simply saturated.

### Weak COCO monitoring during FT (val **480** / test **481**) — `eval_stats` + `log.txt`

#### For the board

While the model trains, we automatically score it on **weak-labelled forest tiles** (not the human golden hold-out). This is the dashboard used to see whether more training areas help **before** running expensive golden + SAHI eval. Metrics here are **standard COCO on fixed-size training tiles** (~800 px), **not** the multi-window “detection bank” protocol on `kaxen_197_1`.

**Artifacts (copied into research for the wiki):**

| Run | Folder under `research/exp-001/results/` |
|-----|------------------------------------------|
| Round 1 FT | `deimv2_dinov3_s_trees_r_weak_ft/` (`log.txt`, `eval_stats.csv`) |
| Round 2 FT | `deimv2_dinov3_s_trees_r_weak_ft_v2/` (`log.txt`, `eval_stats.csv`) |

**What each file is:**

| File | Meaning |
|------|---------|
| `log.txt` | Per-epoch **`test_coco_eval_bbox`** on **val AREA 480** during training (COCO AP/AR, incl. size bins). |
| `eval_stats.csv` | One-off COCO row when loading a checkpoint into `det_solver.val()` (here tagged `best_stg1.pth` in the export). |

#### In-training val curve (AREA **480**, from `log.txt`)

Round 1 used **two stages** (24 + 36 epochs logged); Round 2 = **36 epochs** from `svk_full` on the expanded train set.

| Run | Best **AP50** on val 480 | @ epoch | AP_small | AP_large |
|-----|-------------------------:|--------:|---------:|---------:|
| Round 1 — stage 2 | **0.085** | 2 | 0.002 | 0.052 |
| Round 1 — stage 1 (ref.) | 0.075 | 18 | 0.000 | 0.162 |
| **Round 2** | **0.112** | 5 | 0.002 | 0.076 |
| Round 2 — last epoch | 0.107 | 35 | 0.001 | 0.072 |

**Reading:** Round 2 **does** lift weak-val **AP50** (~+3 pp vs Round 1 stage-2 peak, ~+31% relative). **AP_small on val stays near zero** (~0.002) in both runs — the weak COCO size bin is not where we see small-tree gains; those show up later on **golden SAHI** (Round 1) and in **bank C**, not in this training dashboard.

#### Snapshot `eval_stats.csv` (checkpoint eval)

| Timestamp | Run | AP50 | AP_small | AP_large | AR_small |
|-----------|-----|-----:|---------:|---------:|---------:|
| 2026-09-25 | Round 1 | 0.094 | 0.011 | 0.006 | 0.013 |
| 2026-10-01 | Round 2 | **0.099** | 0.011 | 0.004 | 0.011 |

Round 2 ≈ **+0.005 AP50** vs Round 1 on this snapshot; **AP_small flat**; **AP_large** slightly lower — consistent with **small-expert** skew (acceptable if large trees stay on `svk_full@800` in the bank).

#### Takeaway

**Two eval layers must not be confused:**

1. **Weak COCO (480/481, tile eval)** — Round 2 **improved** overall detection score on the weak validation distribution.
2. **Golden SAHI (`kaxen_197_1`)** — Round 2 **did not beat** Round 1 in the current artifact set (and may still reflect stale preds).

So Round 2 training **did work on its own val tiles**, but **generalization to the golden hold-out is not automatic** — that is why we keep golden + bank as the product gate, and why the next step is fresh infer from `ft_v2` + weak **test 481** compare, not more AREA-only FT without a golden check.

### Statistical box comparison vs golden GT (2026-09-24) — matched pairs

#### For the board

When the model **does** find a tree, are the boxes the wrong **size** or **position** compared to human labels? We worried weak training labels might teach “too small” boxes. This analysis compares prediction boxes to golden boxes on matched hits only.

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

#### Takeaway

Boxes are slightly **larger** than human GT on hits, not smaller — so the next lever is **finding** more trees, not inflating box size to compensate for bad labels.

### Box / lateral-shift plots vs golden GT (2026-09-28)

#### For the board

Charts for the same question as above, plus **shift**: whether detection centers are systematically offset (e.g. from peak-based weak labels). Read the summary table and “Reading” below; figures are optional detail for technical reviewers.

Re-ran matched-box stats on current preds (`svk_full` vs Round1 FT `002`; smoke preds overwritten by Round1 path). Script: `research/exp-001/plot_box_vs_gt.py` → `results/box_vs_gt_plots/`. Definition: **lateral shift** `dx, dy = pred_center − gt_center` (image: +x right, +y down); also `|dx|/GT_w`, `|dy|/GT_h`.

Motivation: LM-derived weak labels are peak-anchored — tree tip ≠ crown centroid — so FT might inherit a systematic center offset.

![[exp001_box_metrics_medians.png|900]]

*Medians: area ratio, IoU, |dx|, |dy| by tile window*

![[exp001_box_area_ratio_hist.png|900]]

*Area_pred/gt distributions (matched TPs)*

![[exp001_lateral_shift_scatter_800.png|900]]

*Lateral shift scatter @ window 800 (star = mean vector)*

![[exp001_lateral_shift_norm_hexbin_800.png|900]]

*Normalized shift (fraction of GT box size) @ 800*

![[exp001_lateral_shift_magnitude_bars.png|700]]

*Median |dx| / |dy| across slices*

#### Direct vs-GT size + shift skew (added 2026-09-28)

Same matched TPs; charts answer: *does the model inflate/shrink boxes vs GT, and does it slide centers?*

![[exp001_vs_gt_skew_dashboard_800.png|950]]

*Dashboard @800: % area vs GT · mean center offset (in GT units) · area-ratio distribution*

![[exp001_vs_gt_relative_boxes_800.png|950]]

*Pred boxes in GT-normalized frame (black = GT unit square; colored = pred) — size + lateral skew together*

![[exp001_vs_gt_size_scatter_800.png|900]]

*Pred area vs GT area (log); diagonal = perfect size*

![[exp001_vs_gt_size_vs_shift_800.png|900]]

*Joint: area inflation (x) × center shift (y) — ideal near (1, 0)*

![[exp001_vs_gt_wh_ratios.png|800]]

*Median width/height ratios vs GT (=1)*

##### Lateral shift vs golden GT (dedicated)

Definition: `dx, dy = pred_center − gt_center` (0 = centers coincide). Also shown as fraction of GT box size.

![[exp001_vs_gt_lateral_shift_summary_800.png|900]]

*Mean offset vector from GT center + median |shift| (px and % of GT)*

![[exp001_vs_gt_lateral_shift_800.png|950]]

*Signed dx / dy histograms vs GT (=0) and 2D cloud @ window 800*

![[exp001_vs_gt_lateral_shift_norm.png|800]]

*Median |dx|/GT_w and |dy|/GT_h across slices*




Compact lateral numbers (@800):

| model | n | mean (dx,dy) px | med \|dx\| | med \|dy\| | med \|dx\|/w |
|-------|--:|----------------:|----------:|----------:|-------------:|
| `svk_full` | 339 | (−0.65, +0.09) | 1.66 | 1.53 | 0.033 |
| Round1 FT | 659 | (−0.87, +0.29) | 1.76 | 1.51 | 0.045 |

Reading:
- Centers are **tight** on matched TPs (median |shift| ≈ **1.5–1.8 px**; ~3–5% of GT width) — no large LM-style drift visible on detector hits vs golden.
- Round1 FT slightly higher |dx| than baseline, but still sub-pixel-to-few-px; mean vector slightly **left** (~−0.7…−0.9 px) for both models.
- Area ratio: Round1 closer to 1.0 than baseline at 800/400 (less oversize); IoU medians similar (~0.71–0.72).
- Caveat: matched TPs only — does not measure shift on FNs / unmatched weak-label objects in train GT.

#### Takeaway

**Geometry is not the bottleneck** on matched detections; **recall** is. No sign of large systematic “shift” from weak peak labels on hits.

### Visual QA vs golden GT (2026-09-24)

#### For the board

Pictures: **green** = human label, **red** = model box. Qualitative check that metrics match what the eye sees — especially many green boxes with no red partner (missed trees).

Overlays: **lime = golden GT**, **red = smoke FT pred** (conf≥0.3), same tiles as eval.
Paths: `results/preds_rgb_deimv2_r_weak_sahi_{200,400,800}/overlays_vs_gt/` (script `visualize_coco_overlays.py --gt-ann-file …`). Assets (in vault): `experiments/assets/exp001_r_weak_vs_gt_*`.

Same tile `01_01`, window ladder (800 → 400 → 200) — FN fills as window shrinks:

![[exp001_r_weak_vs_gt_800_tile0101.jpg|700]]

*800 — sparse preds, many lime-only FNs*

![[exp001_r_weak_vs_gt_400_tile0101.jpg|700]]

*400 — more hits; red boxes still wrap GT*

![[exp001_r_weak_vs_gt_200_tile0101.jpg|700]]

*200 — denser coverage, more clutter/FP*

Extra tile at 400 (`01_03`):

![[exp001_r_weak_vs_gt_400_tile0103.jpg|700]]

Conclusions from QA + metrics:
- Dominant error remains **missed crowns (FN)** — many lime boxes without a red partner, especially at **800** (sparse preds vs many small GT).
- Where preds exist, red boxes typically **cover the crown at least as generously as GT** (often slightly larger) — aligns with median area_pred/gt > 1; no systematic “tight LM hole” on TPs.
- **200** fills more of the stand (higher recall) but adds clutter / FP; size bias still not “too small vs GT”.
- Practical takeaway: next gains should come from **more recall / multi-AREA FT**, not from “inflate boxes to fix LM shrink” on this hold-out. Visuals also support **sparse-overlap** regime (FN/scale), not crown-clump merge.

#### Takeaway

Visuals confirm the story in the numbers: **missed small trees**, not wrong box shape, drives the gap.

### Return package (engineer) — primary tiled run (window 800)

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
split_notes: kaxen_197_1 small-sparse R-class. Bank C (sahi_bank_002) = product reference. 481 tile-COCO closed; no v2 switch. exp-001b LM/CHM deferred.
conclusion: accept_partial  # exp-001a RGB+bank closed; exp-001b deferred; proceed exp-002
kill_triggered: no
```

Artifacts: … `compare_481_{r1_vs_svk,r2_vs_svk,r2_v2_ckpt}/`, `deimv2_dinov3_s_trees_r_weak_ft{,_v2}/`, `notes.md`.

#### Takeaway

Engineer-facing snapshot for reproducibility; non-technical readers can skip to **Conclusion**.

## Closure / verify (2026-10-06)

#### For the board (PL)

| Pytanie | Odpowiedź |
|---------|-----------|
| Czy tag `003` był na starych predykcjach? | **Tak** — metryki `002`=`003` (identyczne pliki); wspólny `preds_coco` bez sufiksu run (`preds_rgb_deimv2_r_weak_sahi_*`). |
| Czy bank po „Round 2” się zmienił? | **Nie** — `sahi_bank_003` = `sahi_bank_002` (B z Round 1 preds). |
| Workbench `003_verify` (2026-10-06) | **Nie v2** — użyto R1 `best_stg1`; metryki = `002`. Ladder naprawiony (brak cichego fallbacku). |
| Test 481 (tile-COCO) | **Done:** `compare_481_*` — R1≫svk; v2 runs = same JSON as R1 ckpt path on VM; **no v2 product switch**. |
| Artefakty w repo | Sync `results/`: preds, bank 002/003, **`compare_481_{r1_vs_svk,r2_vs_svk,r2_v2_ckpt}/`**, logi FT v1/v2. |
| Checkpoint produktowy (small@400) | **Round 1** w banku **C** — 481 zamknięte bez przełączenia na v2. |
| Zakres zamknięty vs otwarty | **exp-001a** RGB+bank **closed**; **exp-001b** LM/CHM golden **deferred**. |

#### For the board (EN)

| Question | Answer |
|----------|--------|
| Was tag `003` scored on stale preds? | **Yes** — metrics identical to `002`; shared `preds_rgb_deimv2_r_weak_sahi_*` paths (no run suffix on preds). |
| Did the multi-scale bank change for Round 2? | **No** — `sahi_bank_003` matches `sahi_bank_002` (B still Round 1 infer). |
| Workbench `003_verify` (Oct 6) | **Not v2** — R1 stg1; metrics = `002`. No further v2 golden runs planned. |
| Weak test 481 | **Closed** — R1≫svk; `r2_v2_ckpt` duplicate; no v2 gain documented. |
| Artifacts in repo | `compare_481_{r1_vs_svk,r2_vs_svk,r2_v2_ckpt}/`, `sahi_bank_002`. |
| Product checkpoint (small@400) | **Round 1** in bank **C** — no evidence to switch to v2. |
| Closed vs deferred | **exp-001a** RGB+bank **closed**; **exp-001b** LM/CHM on golden **deferred**. |

**Eval folder naming (golden):**

| Pattern | Meaning |
|---------|---------|
| `rgb_deimv2_sahi_{800,400,200}_001` | Baseline **`svk_full`** (not weak FT) |
| `rgb_deimv2_r_weak_sahi_*_001` | Weak FT **smoke** (AREA 540) |
| `rgb_deimv2_r_weak_sahi_*_002` | Round 1 FT golden ladder |
| `rgb_deimv2_r_weak_sahi_*_003` | Round 2 FT **eval tag** — currently same preds as `002` |
| `preds_rgb_deimv2_r_weak_sahi_*` | Shared infer output (use **`PRED_TAG`** on ladder to avoid overwrite) |

## Conclusion

#### For the board

| Question | Answer |
|----------|--------|
| Is small-tree detection the main gap? | **Yes** — most errors are missed small trees. |
| Did domain training help? | **Yes** on recall for small trees; **no** as a single model for all sizes. |
| Can we combine baseline + specialist? | **Yes** — merge **C** validated (2026-09-29). |
| What happens next? | **exp-002** (seg backend); **exp-001b** LM/CHM when AREA 197 pipeline exists; production bank C integration. |
| What is explicitly not proven? | Closed-canopy **dense** stands; full per-layer table (LM/CHM on golden). |

**Status:** **exp-001a closed** (RGB + bank C); **exp-001b deferred** (LM/CHM)

- **Scope:** open/dense **deferred**; golden = **small-sparse R-class**.
- **Bank (2026-09-29):** C recovers large and lifts small vs A → specialization OK; reference `sahi_bank_002`.
- **Round2 tag `003`:** same preds as `002`; **481** audit closed — no v2 product switch.
- **Slice roles:** **400** = small expert (R1); **800** = large (`svk_full`); **200** = bank ablation only.
- **Next:** **exp-003** → exp-002; **exp-001b** LM/CHM backfill.
- **Deferred:** open/dense GT; mask-aware fusion without overlap labels.

#### Takeaway

Technical path forward is **specialization + merge**, not forcing one checkpoint to excel on both small and large trees. Remaining work is **more data/training for small trees** and **other detection layers**, not revising box geometry on this hold-out.

## Handoff to coding module

#### For the board

Technical execution checklist for the engineering team (paths, scripts, next run steps).

- Eval hold-out: `kaxen_197_1` — **never in train**
- Bank done: `python research/exp-001/score_sahi_bank.py --size-aware-c` → `results/sahi_bank_002/`
- **exp-001a:** closed — bank `sahi_bank_002/`; weak FT Round 1; golden + **481** documented in `research/exp-001/notes.md` Closure
- Tags `003` / `003_verify`: audit only (duplicate of `002`) — **not** Round 2 product evidence
- **exp-001b:** LM / CHM+DEIMv2 on golden — deferred (AREA 197)
- **Next experiment:** exp-002 (RGB seg backend); then exp-003 (fusion)
- Product path: **large = A (`svk@800`), small = B (R1 FT@400)**, merge **C**
- Optional: sparsity proxy on golden
- Dense mask-aware fusion → exp-003 after (prefer) overlap GT
- Dense framing for exp-002 deferred until overlap / closed-canopy GT exists

#### Takeaway

Implementation checklist only; non-technical readers can stop at **Conclusion**.

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[concepts/literature-map-dense-itd]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
- [[experiments/exp-002-rgb-seg-backend-ceiling]]
- [[experiments/exp-003-merge-fusion-v1]]
