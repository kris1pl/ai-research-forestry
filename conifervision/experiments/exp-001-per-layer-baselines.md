---
title: exp-001 per-layer baselines (size-stratified R-class)
type: Experiment
description: "H1 v1.1 — Size-stratified R-class ceilings; multi-scale detection bank on Round1 preds (gate=C); Round2 FT after C OK; D=+200 ablation. Open/dense deferred. Queue: H1 → H3 → H2."
tags: [ensemble, baseline, evaluation, R-class, small-trees, multi-scale-bank, H1]
status: stable
updated: 2026-09-29
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

**Queue:** **H1 (run first)** → [[experiments/exp-003-rgb-seg-backend-ceiling]] → [[experiments/exp-002-merge-fusion-v1]].  
**Gate:** ADR-002 — sequence approved to run (see [[project/decisions]]).  
**Status (2026-09-29):** Round 1 multi-AREA weak FT done (`002`). **Multi-scale detection bank scored** on Round1 preds → **C_OK** (specialization holds) → **Round2 FT unlocked**. Scope v1.1 — open/dense deferred. D = ablation only. Round2 = FT **small expert** (no AP_large protect); large = `svk_full@800`; small = **FT@400**.

## Executive summary (for the board)

This experiment measures how well we detect **young / small trees** on a fixed, human-labelled test area (R-class, before thinning). The baseline aerial model finds most **large** trees but misses most **small** ones. After a first round of domain training, a “small-tree specialist” does much better on small trees but worse on large trees **when used alone** — which is expected. We then **combined** the baseline (large) with the specialist (small): the combined result keeps large-tree performance **and** roughly **quadruples** small-tree detection. **Decision:** that combination works → we proceed to a second training round focused only on improving the small-tree specialist, without forcing one model to do everything. What we have **not** proven yet: performance in truly closed-canopy “dense” stands (we lack that ground truth).

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
| **Multi-scale detection bank** + merge ablation (800 baseline ∪ 400 FT ∪ optional 200) | Full mask-aware exp-002 / dense H3 claims |
| LM / CHM+DEIMv2 on same tiles (layer comparison) | under_seg / duplicate as *dense merge* signals |
| Empiric FN/FP taxonomy; box geometry vs GT | Claiming one FT checkpoint must win both size bins |

**Ensemble stance (aligned with production multilayer):** AP_large drop on FT single-pass is **acceptable specialization** if `svk_full@800` (or CHM/LM large path) still supplies large trees after merge — same pattern as CHM bands and R-class 100/50 px + LM in [[methods/merge-detections]].

**Slice roles:**

| Slice | Role |
|------:|------|
| **800** | Large / broad path — prefer **`svk_full`** (not FT) in product bank |
| **400** | **Primary small expert** — Round2 FT target (best Round1 FT gain @ usable P) |
| **200** | **Bank ablation only** — high R_small but low P; FT≈flat vs `svk_full@200`; include in merge ± size-gate, not default expert |

*Note for implementers:* windowed inference on large orthophotos uses the SAHI tiling library under the hood — board-facing text talks about **tile / window size**, not the library name.

**GT characterization:** `kaxen_197_1` = R-class / pre-thinning label, **small crowns + sparse overlap** — treat as **small-sparse R-class proxy**, not dense ITD. Optional follow-up: quantify sparsity (e.g. share of GT with neighbor IoU>0, median NN distance / √area) once in the coding module.

North-star dense/open evaluation ([[concepts/dense-stand-detection]], [[project/research-tree-detection-ensemble]]) remains program-level; H1 no longer blocks on it.

#### Takeaway

**In scope:** small/large metrics, RGB + training a small-tree expert, merge test. **Out of scope for now:** proving dense-stand behaviour; full production fusion with masks. That avoids overstating what one labelled area can support.

## Motivation

#### For the board

This experiment sits in a longer research program: combine several detection sources (colour, height, peaks) the way production already does for R-class. The links below are the scientific and product context for engineers; the board need only know H1 is **step 1** — measure each layer before merging.

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

The workflow in plain terms: (1) score each detector alone on the same fixed test tiles, split by tree size; (2) merge baseline + small specialist and check the combined outcome; (3) only then invest in more training or change merge rules.

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
6. Emit ceilings + bank verdict → feed exp-003 / exp-002 (mask-aware later).
```

### Prerequisites

- Locked or provisional evaluation protocol; access to labeled or weakly labeled eval AREA outside this repo

### Gaps

- **Open/dense** structural split not testable on current golden (AREA tag ≠ crown-overlap dense) — needs new GT / data program
- LM preds and CHM+DEIMv2 R-band preds on same tiles — not run yet
- Multi-scale **detection bank** scored 2026-09-29 (`sahi_bank_002`) — **C_OK**; Round2 unlocked; D ablation only
- Size bins currently by **relative bbox area** (small < 0.1% of image), not CHM height layers
- ECSeg / multi-backend comparison deferred to exp-003
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

**Success** means: clear size-split scorecards, evidence that merge C works, and an honest note that we are **not** validating closed-canopy dense forest yet. **Failure (kill)** would mean we cannot get useful RGB ceilings **or** merge C fails to beat baseline A on both size bands after fair merge rules — then we stop and fix data or merge strategy before more spend.

- Size-stratified ceiling tables for RGB (done) and ideally LM + CHM+DEIMv2 on `kaxen_197_1`
- Written error taxonomy (FN-dominated small) usable as input to exp-003 / exp-002 **with small-sparse disclaimer**
- Bank **C** scored vs A/B: multilayer recovers large and lifts small without FT AP_large protection
- Bank **D** scored as ablation (does not block Round2 if C OK)
- Explicit verdict that this GT does **not** validate dense-stand fusion — data gap logged for overlap / closed-canopy golden

## Kill criteria

- Cannot obtain **useful size-stratified RGB ceiling** on the hold-out within agreed effort **and** cannot obtain GT with measurable crown overlap / closed canopy for later dense claims → pause mask-aware fusion dense claims (exp-002 Variant B / dense H3 framing) and escalate data program
- Bank **C** path: if after frozen merge (NMS ± size-aware C) `800∪400` still fails to recover large vs A **and** fails to lift small vs A → revisit merge rules / large path first; **only then** consider size-balance FT or alternate large expert — do **not** jump to size-balance FT from a single naive-NMS miss or from D alone

**Kill check (2026-09-15, legacy):** AREA-tagged “dense” labels exist (`kaxen_197_1`, 2534 boxes) → **not triggered** (labels exist; structural dense still missing — tracked as Gap, not kill).

**Kill check (2026-09-28, v1.1):** RGB size-stratified ceiling exists; iterate path open (FT / bank merge / LM·CHM pending) → **not triggered**.

#### Takeaway

**Kill criteria not triggered.** Bank C passed (2026-09-29). Experiment continues (**iterate**), not stop.

## Setup

#### For the board

**Done:** RGB detection at several window sizes, Round1 fine-tuning, multi-scale bank evaluation. **Still to run:** local-maxima and CHM-based detectors on the same tiles for apples-to-apples comparison. **Next spend:** Round2 fine-tuning for the small-tree expert.

Planned runs:

- Local maxima / LM baseline — **pending**
- CHM + DEIMv2 baseline — **pending**
- RGB detection baseline — **done** (full-frame + tiled windows 800/400/**200**)
- Multi-scale detection bank on Round1 preds (A/B/C gate; D ablation) — **done** (`sahi_bank_002`, C_OK); Round2 FT **next**
- RGB instance segmentation (ECSeg) — deferred to exp-003; interim SAM silver GT built for later seg work (not a fair H1 detector layer)

## Runs

#### For the board

Inventory of model runs (baseline, training rounds, merge test). Window column = crop size in pixels. **Done** rows support the bank decision; **next** = Round2 training.

All RGB runs use DEIMv2 `svk_full` init where FT applies. Eval = `kaxen_197_1` (small-sparse R-class). Legacy “dense” = AREA tag only. Single-pass tables below; **bank merge done** (`sahi_bank_002`, C_OK).

| Run ID | Mode | Window | Conf | Role |
|--------|------|-------:|-----:|------|
| `rgb_deimv2_sahi_800_001` | tiled | 800 | 0.3 | **Large-path ceiling** (`svk_full`) |
| `rgb_deimv2_sahi_400_001` | tiled | 400 | 0.3 | Small-tree ablation vs 800 |
| `rgb_deimv2_sahi_200_001` | tiled | 200 | 0.3 | Smallest-window ablation (bank candidate) |
| `rgb_deimv2_001` | full-frame | — | 0.5 | Ablation (understates small recall) |
| `rgb_deimv2_r_weak_sahi_{800,400,200}_001` | tiled | 800/400/200 | 0.3 | **Smoke FT** — weak R GT (AREA 540 tiles), init `svk_full`; golden hold-out |
| `rgb_deimv2_r_weak_sahi_{800,400,200}_002` | tiled | 800/400/200 | 0.3 | **Round 1 multi-AREA FT** — train 473–479 / val 480 / test 481 (`r_weak_v1_a473_481`); **small-expert candidate @400** |
| `sahi_bank_002` | merge | A/B/C/C_sa/D | — | **Done** — C_OK → Round2 unlocked; D ablation |
| `rgb_deimv2_r_weak_*` | tiled | 800/400/200 | 0.3 | **Round 2 (next)** — more AREAs; small expert (**no** AP_large protect); re-score bank after |

Data prep: CVAT → golden; SAM full-image + clip-to-GT → silver (`instances_tree_sam_clipped.json` for exp-003).

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

**Smoke test** = first cheap training trial on weak labels from a single area, to see if fine-tuning moves metrics in the right direction before scaling data and compute.

Train: weak GT from AREA **540** only (tiled COCO + ad-hoc tile split); init `svk_full`; ~24 epochs. Eval: golden `kaxen_197_1` windows 800/400/200 conf 0.3 — **never in train**. Artifacts: `results/rgb_deimv2_r_weak_sahi_{800,400,200}_001/`.

| Slice | ΔP | ΔR | ΔF1 | ΔR_small | ΔAP_small | ΔR_large |
|------:|---:|---:|----:|---------:|----------:|---------:|
| 800 | +0.002 | **+0.019** | **+0.027** | +0.011 | +0.001 | **+0.074** |
| 400 | +0.003 | **+0.021** | **+0.025** | +0.020 | +0.006 | +0.025 |
| 200 | **+0.025** | +0.007 | +0.013 | +0.011 | **+0.042** | −0.022 |

Reading: **positive direction** (esp. 800/400: more recall at stable P). Absolute small-tree gap remains large (800 R_small still ~0.07). **Not** H1 success — smoke only. Next = multi-AREA weak FT, then re-ladder; merge still deferred. LM/CHM layers still pending for full H1.

#### Takeaway

Training **can** help, but one area was not enough — justified scaling to Round1.

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

**Why we measure this:** Round1 fine-tuning improved small-tree recall but hurt large-tree scores on a **single** checkpoint. That is acceptable **only if** the bank (A∪B) still recovers large trees **and** keeps the small-tree gain. If merge C works, we invest the next training round in a better **small expert** — we do **not** force one model to win both size bins.

**What it is not:** not a new training run; not full production fusion (masks / CHM / LM — later experiments). Here it is a lightweight box-level merge on already computed predictions. *(Engineer note: windowed inference uses the SAHI tiling library; the method is multi-scale experts + merge, not “SAHI” as a product concept.)*

---

Script: `research/exp-001/score_sahi_bank.py --size-aware-c`. Protocol: conf≥0.3, NMS IoU=0.5, size_gate=0.1%. Preds: A=`svk_full@800`, B=FT `002`@400, D uses `svk_full@200`. Artifacts: `results/sahi_bank_002/`.

| Bank | P | R | F1 | R_small | R_large | AP_small | AP_large | n_pred |
|------|--:|--:|---:|--------:|--------:|---------:|---------:|-------:|
| A `svk@800` | 0.783 | 0.134 | 0.229 | 0.063 | 0.617 | 0.030 | 0.479 | 433 |
| B `FT@400` | 0.716 | 0.310 | 0.433 | 0.252 | 0.706 | 0.157 | 0.217 | 1098 |
| **C A∪B NMS** | 0.680 | 0.322 | 0.437 | **0.257** | **0.761** | 0.136 | **0.484** | 1200 |
| C_sa (size-aware) | 0.677 | 0.320 | 0.435 | 0.255 | 0.761 | 0.135 | 0.494 | 1200 |
| D (+200 gated) | 0.620 | 0.382 | 0.472 | 0.323 | 0.776 | 0.246 | 0.194 | 1560 |
| D_ungated | 0.492 | 0.408 | 0.446 | 0.342 | 0.856 | 0.191 | 0.378 | 2103 |

#### What the table shows (plain language)

Focus on row **C** vs row **A**. **A** alone finds few small trees (about 6% of them) but is solid on large ones. Combining A with the small-tree specialist (**C**) finds roughly **4× more small trees** while also keeping — and even slightly improving — large-tree coverage. That means we do **not** need one “perfect” model for every size: two specialists merged work better. Rows **D** are optional “what if we add even smaller windows?” tests; they are not the decision for the next training round. Bottom line for the program: **specialization + merge is validated → proceed to Round2 training of a better small-tree expert.**

Reading (metrics detail):
- **C vs A:** R_large 0.62→**0.76**, AP_large held (~0.48); R_small 0.06→**0.26**. Specialization **OK** — Round2 unlocked.
- C_sa ≈ C (size-aware not required for this hold-out).
- **D:** lifts R_small further but AP_large collapses when size-gated; ungated keeps more large AP at cost of P — ablation only, does not change Round2 decision.
- Product path until Round2 re-bank: **large = A, small = B**.

#### Takeaway (program decision)

**Go** on Round2 small-expert training. Product-shaped path: baseline for large, specialist for small, merged output for the map.

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
split_notes: kaxen_197_1 small-sparse R-class. Multi-scale detection bank on Round1 (gate=C; D ablation). Open/dense deferred (H1 v1.1).
conclusion: iterate  # bank C before Round2; no AP_large protect in FT; LM/CHM after bank
kill_triggered: no
```

Artifacts: `results/rgb_deimv2_sahi_{800,400,200}_001/`, `results/rgb_deimv2_r_weak_sahi_{800,400,200}_{001,002}/`, `results/delta_r_weak_vs_baseline_002.json`, `results/box_size_vs_gt_r_weak.json`, `results/rgb_deimv2_001/`, `notes.md`. Oracle SAM archived at `results/_archive/sam_oracle_raw_001/`. Bank: `results/sahi_bank_002/`.

#### Takeaway

Engineer-facing snapshot for reproducibility; board readers can skip to **Conclusion**.

## Conclusion

#### For the board (decision status)

| Question | Answer |
|----------|--------|
| Is small-tree detection the main gap? | **Yes** — most errors are missed small trees. |
| Did domain training help? | **Yes** on recall for small trees; **no** as a single model for all sizes. |
| Can we combine baseline + specialist? | **Yes** — merge **C** validated (2026-09-29). |
| What happens next? | **Round2** training to improve the small-tree expert; then re-test merge. |
| What is explicitly not proven? | Closed-canopy **dense** stands; full fusion with height/peaks (pending LM/CHM runs). |

**Status:** **iterate** (continue experiment — not stop, not “done”)

**iterate** (H1 v1.1 — bank C_OK → Round2 next)

- **Scope:** open/dense **deferred**; golden = **small-sparse R-class**.
- **Bank (2026-09-29):** C recovers large and lifts small vs A → specialization OK; **do not** size-balance FT. D ablation only.
- **Slice roles:** **400** = primary small path; **200** = optional bank ablation; **800** = large from `svk_full`.
- Pipeline-realistic single-pass `svk@800` still weak on small; FT@400 + bank is the product-shaped path.
- **Next:** (1) Round2 FT — more R AREAs, small@400, no AP_large protect; re-score bank with new B; (2) LM + CHM+DEIMv2 on same tiles.
- **Deferred:** crown-overlap GT; full mask-aware exp-002.
- Success **partial** (bank C done; LM/CHM + Round2 pending; FN still dominant).

#### Takeaway

Invest in **specialization + merge**, not in forcing one checkpoint to excel on both small and large trees. Remaining work is **more data/training for small trees** and **other detection layers**, not revising box geometry on this hold-out.

## Handoff to coding module

#### For the board

Technical execution checklist for the engineering team (paths, scripts, next GPU steps). No separate board action unless Round2 scope or budget is approved.

- Eval hold-out: `kaxen_197_1` — **never in train**
- Bank done: `python research/exp-001/score_sahi_bank.py --size-aware-c` → `results/sahi_bank_002/`
- **Round2 train (next):** more R AREAs; goal = better **small expert @400** — **no** size-balance / AP_large protect
- Ladder after Round2: `MODEL_PATH=… RUN_TAG=003 bash research/exp-001/run_rgb_deimv2_r_weak_sahi_ladder.sh`
- Re-run bank with new B after Round2; product path: **large = A, small = B**
- LM / CHM+DEIMv2 pending; ECSeg → exp-003
- Optional: sparsity proxy on golden
- Dense mask-aware fusion → exp-002 after (prefer) overlap GT
- Human gate before exp-003 dense framing

#### Takeaway

Implementation-only; board can stop at **Conclusion** unless approving Round2 compute or labelling budget.

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/dense-stand-detection]]
- [[concepts/literature-map-dense-itd]]
- [[methods/merge-detections]]
- [[methods/edgecrafter-ecseg]]
- [[experiments/exp-003-rgb-seg-backend-ceiling]]
- [[experiments/exp-002-merge-fusion-v1]]
