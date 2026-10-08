---
title: exp-002 RGB instance-seg backend ceiling (H3 v1.1)
type: Experiment
description: "H3 v1.1 — Compare RGB instance-segmentation backends on the same small-sparse R-class hold-out as exp-001a (kaxen_197_1), with silver clipped mask reference, before locking mask source + prompt policy for exp-003 (merge)."
tags: [ensemble, instance-segmentation, small-sparse-r-class, edgecrafter, stardist, sam2, H3]
status: stable
updated: 2026-10-08
area: "Golden kaxen_197_1 (5 tiles, AREA 197) — same as exp-001a; closed-canopy dense-ITD deferred"
hypothesis: "On small-sparse R-class hold-out with silver clipped mask reference, differences among runnable seg backends and among H1 box-prompt sources (bank C vs svk-only vs FT-only) are large enough to recommend a single mask_backend + prompt_policy for exp-003; if all are similarly weak, do not bet on mask-aware fusion."
metrics:
  mask_iou_matched: TBD
  under_segmentation_rate: TBD
  over_segmentation_rate: TBD
  mask_metrics_small_bin: TBD
  detection_ap_regression: TBD
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
revised:
  by: human+agent
  at: 2026-10-06T12:00:00Z
  reason: "H3 v1.1 — align with exp-001a closure (small-sparse, bank C, silver GT); dense split deferred"
renumbered:
  at: 2026-10-08
  note: "exp-NNN now matches run order 001→002→003; hypothesis id remains H3 (was exp-003 before renumber)"
---

# exp-002 RGB instance-seg backend ceiling (H3 v1.1)

**Queue:** [[experiments/exp-001-per-layer-baselines]] (H1) → **exp-002 / H3 (this page)** → [[experiments/exp-003-merge-fusion-v1]] (H2).  
**Gate:** ADR-002 — sequence approved (see [[project/decisions]]). **Start after exp-001a closure** (bbox bank + golden protocol frozen). exp-001b (LM/CHM) may run in parallel; not required for H3 RGB mask bake-off.  
**Status (2026-10-06):** **H3 v1.1 protocol locked** — hypothesis aligned with exp-001a; **runs not started** (Results TBD). **Next:** mask eval harness + mandatory run **C1** (AI segmentation guided by production merge **bank C** boxes).

## Executive summary (for the board)

exp-001 answered **“where are the trees?”** (bounding boxes) on a fixed young-forest test area: we combine a **large-tree** model and a **small-tree** specialist (**bank C**). exp-002 answers the next product question: **“what is the shape of each crown?”** (instance masks). We compare **how** we generate those masks from the same aerial photos — mainly **AI that follows our detection boxes** (SAM-family), and optionally other published crown-segmentation tools — and score them against a **silver** reference (AI masks clipped to human boxes, not a second human paint job on every pixel). We also test whether mask quality depends on **which boxes we use as hints** (full product merge vs large-only vs small-only). **Outcome for leadership:** either a clear **recommended mask pipeline** before we invest in advanced merge (exp-003), or a **stop signal** if masks are too weak — then we improve labels/data instead of building fusion on shaky crowns. We are **not** claiming closed dense-canopy forest behaviour on this test set (same limitation as exp-001).

## Hypothesis

#### For the board

We test whether **crown outline quality** differs enough between segmentation approaches — and between **which detection boxes we feed in** — to justify a single product choice before we merge detections using masks (exp-003). exp-001 already showed that **finding** small trees matters; H3 asks whether **outlining** them is good enough to bet the next engineering step on.

**H3 v1.1 (active):**

On the **same hold-out as H1 v1.1** — **small-sparse R-class** crowns on `kaxen_197_1` (not closed-canopy dense) — with **silver clipped** masks as the mask reference, differences between **runnable** RGB instance-seg backends and between **box-prompt policies** inherited from exp-001a are **systematic enough** (especially on **small** size bin) that we can recommend one **`mask_backend` + `prompt_policy`** for [[experiments/exp-003-merge-fusion-v1]]. If backends and prompt variants are similarly weak or near-tie, **do not** proceed to mask-aware fusion as the primary bet (data / label program instead).

**H3 v1.0 (superseded):** On **dense** tiles, ECSeg vs Tier A (StarDist / SAM2-prompted) mask ceilings differ enough that backend choice changes merge ROI **more than adding another bbox detector**. *Misaligned with exp-001a:* golden is small-sparse; H1 already fixed the bbox story (multi-scale bank **C** = `svk_full@800` ∪ `FT@400`). Dense-ITD and open/dense structural split remain **deferred** until overlap GT exists.

#### Takeaway

H3 is **mask + prompt policy**, on the **same young-forest test tiles** as H1 — not another round of “which bbox model wins.” Success = one written recommendation for exp-003 (merge); failure = all options similarly bad → invest in labels, not mask-merge.

## Motivation

#### For the board

Production vision moves from **points/boxes** toward **crown shapes** for inventory, overlap, and merge quality. Before we lock engineering on one vendor or model family, we run a **controlled comparison** on the same images and references H1 already uses — so board and product see one story, not three incompatible benchmarks.

- Pick a **mask source** for exp-003 (merge) without assuming [[methods/edgecrafter-ecseg]] is the default ([[project/research-tree-detection-ensemble]])
- H1 showed **FN on small trees** dominates bbox error on this hold-out; mask quality may hinge on **which boxes prompt** SAM-family (bank C vs ablations), not only on seg model family
- Silver reference: clipped SAM pseudo-GT (not raw SAM oracle as a detector ceiling — see exp-001 archive note)
- Literature context for dense ITD remains useful for **future** tiles: [[concepts/literature-map-dense-itd]], [[concepts/dense-stand-detection]] — **out of scope** for this H3 iteration
- Feeds [[experiments/exp-003-merge-fusion-v1]] Variant B (mask-aware merge)

#### Takeaway

Motivation is **de-risk the next merge step** — choose crown outlines with evidence, aligned with the ensemble roadmap — not a parallel science project.

## Pseudocode

#### For the board

In plain terms: (1) use the **same five test images** and **silver** crown references as agreed in H1; (2) draw crowns with several **segmentation methods**, using our **detection boxes** as guides where needed; (3) score **outline accuracy**, especially on **small** trees; (4) pick one method + one **box-hint policy** for the follow-on merge experiment — or stop if nothing is good enough.

**Inputs:** same RGB tiles as exp-001; **mask GT** = silver clipped COCO; **box prompts** from exp-001a preds (primary: bank C; ablations: svk@800-only, FT@400-only)

**Outputs:** per-backend + per-prompt metric tables; `recommended_mask_backend` + `recommended_prompt_policy` for exp-003

**Parameters:** SAM/SAM2 prompt mode (box); ECSeg zero-/few-shot settings (TBD); post-process (TBD); resolution = match ortho GSD

```text
1. Freeze tiles, silver clipped GT, and H1 prompt COCO paths (no LM/CHM fusion).
2. Backend C (mandatory sprint): SAM2- or SAM-prompted crowns from detector boxes.
   - C1 prompts: bank C merged preds (exp-001a product path)
   - C2 prompts: svk_full@800 only
   - C3 prompts: Round1 FT@400 only
3. Backend A (optional if env ready): ECSeg zero-/few-shot ([[methods/edgecrafter-ecseg]]).
4. Backend B (optional): StarDist-style — if runnable; else Gap (skip).
5. Score mask/instance metrics vs silver clipped; stratify small bin (same thresholds as H1).
6. Secondary: regression check vs golden bbox GT where useful (qualitative + optional AP).
7. Recommend mask_backend + prompt_policy for exp-003 (or kill → data program).
```

### Prerequisites

- **exp-001a closed** — golden bbox protocol + bank C reference preds documented
- Shared paths: engineer manifest `research/exp-002/manifest.yaml` in coding module
- At least **two** comparable conditions (e.g. C1 vs C2, or C + A); if only one backend runs, document and **iterate** (do not fake A/B)

### Human gate (before GPU)

#### For the board

Before significant GPU cost, we agree the **minimum credible comparison**: product boxes + SAM-family (**C1**) and scoring vs silver reference. Extra tools (ECSeg, StarDist) and box ablations (C2/C3) are prioritized in the table below — leadership can trim optional tiers if budget is tight.

| Tier | Item |
|------|------|
| **Mandatory** | SAM-family prompted run with **bank C** boxes (C1) |
| **Mandatory** | Eval harness vs **silver clipped** + small-bin stratification |
| **Strongly recommended** | Prompt ablations C2, C3 (link mask errors to H1 bbox path) |
| **Optional** | ECSeg (A), StarDist (B) — skip with Gaps if no weights/recipe |

### Gaps

- StarDist / TreePseCo train recipes and weights outside vault
- Numeric mask metric formulas — provisional until ADR-001; record definitions in Results
- Closed-canopy **dense** eval — requires new GT/tiles; not this sprint

#### Takeaway

We will not run a fake “competition” with only one tool — minimum **two** comparable conditions (e.g. product boxes vs baseline-only boxes). Optional tools (ECSeg, StarDist) are **nice-to-have**, not blockers for a first verdict on SAM + bank C.

## Evaluation protocol

#### For the board

Scores answer: **“How well does the predicted crown match our silver reference?”** — reported **separately for small and large trees** (same size rule as exp-001), so we do not hide poor small-crown outlines inside an average. Human boxes remain a **sanity check**, not the primary mask score. This is the **same test geography** as exp-001; results are **not** proof for closed dense stands.

- **Primary regime:** small-sparse R-class on `kaxen_197_1` (align with H1 v1.1)
- **Primary mask reference:** silver clipped (`instances_tree_sam_clipped.json`)
- **Stratification:** size bins same as exp-001 (small = bbox area &lt; 0.1% of image)
- **Secondary:** golden bbox GT for regression / failure taxonomy overlays
- **Deferred:** dense-ITD split, open structural split — same data gap as H1

### Data / code (engineer repo)

Base: `conifervision-ai-train/`. **Silver** = SAM masks clipped to human boxes; images symlink to golden.

- **Mask reference (primary):** `research/annotations/silver/kaxen_197_1/annotations/instances_tree_sam_clipped.json`
- **Human bbox GT (secondary):** `research/annotations/golden/kaxen_197_1/annotations/instances_tree.json`
- **Images (5 tiles):** `research/annotations/golden/kaxen_197_1/images`
- **Box prompts — product path (C1):** `research/exp-001/results/sahi_bank_002/preds/bank_C.json`
- **Manifest / notes:** `research/exp-002/manifest.yaml`, `research/exp-002/notes.md`

#### Takeaway

When reading future tables, prioritise **small-tree mask quality** and **under/over-segmentation** (merged vs split crowns) — the errors that would break inventory and merge — not a single opaque score.

## Success criteria

#### For the board

**Success** means leadership can approve **one mask pipeline** (tool + which detection hints to use) for the merge experiment, with example failure images on file. **Near-tie** is acceptable if we document trade-offs (speed, cost, licence).

- Clear ranking or documented near-tie among **runnable** backends **and** among prompt policies on silver clipped
- Written **`recommended_mask_backend`** + **`recommended_prompt_policy`** for exp-002
- Failure examples (under-seg on small crowns, spill, duplicate instances)

#### Takeaway

Success is a **decision-ready recommendation**, not “we tried three papers.”

## Kill criteria

#### For the board

**Kill** means: after fair effort, **no** segmentation option is clearly usable on silver reference (especially small crowns) — so we **pause mask-based merge** as the main product bet and fund **better ground truth / labels** first. That is a **responsible stop**, not a failed quarter.

- All backends and prompt variants in budget yield similarly weak / unusable masks on silver clipped (especially small bin) → prioritize gold/pseudo label program; **do not** proceed to exp-003 mask-aware fusion as primary bet

#### Takeaway

Kill criteria **not evaluated yet** (experiment not run). If triggered later, communicate: **boxes may be good enough; crowns are not — fix data before fusion.**

## Setup

#### For the board

**In this experiment:** only **RGB crown segmentation** (no height map or peak fusion). Detection boxes from exp-001 are **inputs** to “draw the crown inside this rectangle,” not a new detection bake-off.

RGB instance-segmentation backends only; detector boxes as **inputs** to prompted paths, not fusion of LM/CHM layers.

#### Takeaway

Setup keeps H3 **narrow** — outline quality only — so results map cleanly to exp-003.

## Runs

#### For the board

| What we call it | Plain English | Priority |
|-----------------|---------------|----------|
| **C1** | Crowns from AI **following boxes from product merge (bank C)** | **Must run first** |
| **C2** | Same AI, but boxes from **large-tree-only** model | Recommended — shows if merge helps outlines |
| **C3** | Same AI, but boxes from **small-tree specialist only** | Recommended |
| **A** | Published **ECSeg**-style tool (zero/few-shot) | Optional if environment ready |
| **B** | **StarDist**-style crown model | Optional; skip if no weights |

| Run | Config / baseline | Notes |
|-----|-------------------|-------|
| C1 | SAM-family + **bank C** box prompts | Product-aligned; **mandatory** |
| C2 | SAM-family + svk@800 only | Prompt ablation |
| C3 | SAM-family + FT@400 only | Small-expert prompt ablation |
| A | ECSeg | Optional; zero-/few-shot |
| B | StarDist-style | Optional; skip if not runnable |

#### Takeaway

The run table is the **audit trail** for which tool and which box hints were used — essential when the board asks “what did we actually ship to the comparison?”

## Results

#### For the board

*No scored runs yet (2026-10-06).* When populated, this section will show **side-by-side mask quality** per run, with emphasis on **small trees** and visual examples of **merged crowns** (under-seg) vs **split crowns** (over-seg). Until then, rely on [[experiments/exp-001-per-layer-baselines]] for detection performance; H3 does not duplicate bbox tables.

| Run | Metric | Value | Split | Notes |
|-----|--------|-------|-------|-------|
| | | | | |

#### Takeaway

Empty Results is expected until GPU work completes — the **protocol and board framing** are what we locked in v1.1.

## Conclusion

<!-- accept | reject | iterate -->

#### For the board

TBD after first scored runs. Expected labels:

| Verdict | Meaning for leadership |
|---------|-------------------------|
| **accept** | One mask pipeline recommended → proceed to exp-003 mask-aware merge with that choice |
| **iterate** | Promising but inconclusive → narrow follow-up (one backend or one prompt fix) before merge |
| **reject** | Masks not usable on reference → **data/label program**, not mask-merge as primary bet |

TBD

#### Takeaway

Conclusion will be one sentence for the board plus technical detail below — same pattern as exp-001 closure.

## Handoff to coding module

#### For the board

Engineering delivers **numbers, recommendation id, and example images** back into this wiki page; no model weights stored in the research vault. **Human gate** before exp-003 spend.

- Wiki: this page (H3 v1.1). Engineer: `conifervision-ai-train/research/exp-002/notes.md` + `manifest.yaml`
- Return: Results table + `recommended_mask_backend` + `recommended_prompt_policy` + failure examples
- No weights committed to this vault
- After conclusion: human gate before exp-003

#### Takeaway

Handoff = **decision package** for product and merge experiment owners, not a code dump.

## Related

- [[experiments/exp-001-per-layer-baselines]]
- [[experiments/exp-003-merge-fusion-v1]]
- [[project/research-tree-detection-ensemble]]
- [[project/hypothesis-validation-loop]]
- [[concepts/literature-map-dense-itd]]
- [[concepts/dense-stand-detection]]
- [[methods/edgecrafter-ecseg]]
- [[methods/merge-detections]]
