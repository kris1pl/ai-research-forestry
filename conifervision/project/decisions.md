---
title: Methodological decisions (ADR)
type: Project
description: "ADR format: Context → Decision → Consequences. The agent adds an entry after team agreement."
tags: [adr]
status: stable
updated: 2026-10-21
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
---
# Methodological decisions

ADR format: **Context → Decision → Consequences**. The agent adds an entry after team agreement.

## Template

```markdown
## ADR-NNN: Title (YYYY-MM-DD)

**Status:** proposed | accepted | superseded

**Context:** …

**Decision:** …

**Consequences:** …
```

## Entries

## ADR-001: Ensemble v1 success definition (2026-08-21)

**Status:** proposed

**Context:** The research program ([[project/research-tree-detection-ensemble]]) targets multi-layer tree detection/segmentation with emphasis on dense stands before thinning. Without a shared success definition, experiments cannot be accepted or killed consistently. Evaluation protocol details (exact metric formulas, dense/open threshold, size-bin edges) remain TBD — see [[concepts/dense-stand-detection]] and Phase 0 on the research program page. Hypothesis workflow: [[project/hypothesis-validation-loop]].

**Decision (proposed structure — numeric thresholds TBD until protocol locked):**

1. **Primary split:** report metrics separately for **open** and **dense** stands.
2. **Size:** report at least **small** vs **large** bins aligned with CHM/DEIMv2 height layers used in production.
3. **Ensemble v1 “accept”** requires (all must hold once numbers are filled in):
   - Improvement on **dense** primary detection/segmentation metric family vs the agreed baseline (e.g. current LM+CHM/DEIMv2 merge) — threshold TBD.
   - No catastrophic regression on **open** stands — tolerance TBD.
   - Documented fusion/merge rule in [[methods/merge-detections]] matching the winning experiment.
4. **Kill / do not ship v1** if dense primary metric does not improve after the agreed label and tuning effort, or if fusion only shifts error modes without net dense gain.
5. Language: experiments **validate** or **reject** (or iterate); they do not “prove” success.

**Consequences:**

- New experiments should reference this ADR in Success/Kill criteria.
- Until thresholds are filled, status stays **proposed**; accepting ADR-001 requires a follow-up edit with concrete numbers from the evaluation protocol.
- Does not change the production pipeline in [[project/pipeline-overview]] until an experiment is accepted and an implementation ADR follows.

## ADR-002: Experiment sequence H1 → H3 → H2 (2026-08-24)

**Status:** accepted

**Context:** With literature mapped ([[concepts/literature-map-dense-itd]]) and the research north star set ([[project/research-tree-detection-ensemble]]), the team chose an initial hypothesis queue: per-layer open/dense baselines, then a narrow RGB instance-seg backend ceiling, then mask-aware fusion. Running fusion or multi-backend seg without stratified baselines risks wasted GPU and lock-in. Workflow: [[project/hypothesis-validation-loop]].

**Decision:**

1. **Order (approved to run):**
   - **H1** — [[experiments/r-class-itd/exp-001-per-layer-baselines]] first
   - **H3** — [[experiments/r-class-itd/exp-002-rgb-seg-backend-ceiling]] next (optional narrow parallel only if H1 tiles/labels already ready)
   - **H2** — [[experiments/r-class-itd/exp-003-merge-fusion-v1]] last, using mask backend from H3 when available
2. Human gate after each experiment Conclusion before starting the next GPU tranche.
3. If H1 kill criteria fire (no dense labels) → pause H3/H2 and escalate data program (Phase 3).
4. If H3 kill criteria fire (all masks unusable) → do not treat H2 Variant B as the primary path.
5. Numeric success thresholds remain TBD under ADR-001 until the evaluation protocol is locked.

**Consequences:**

- Coding/GPU module should prioritize handoff from exp-001.
- Index / Current focus should list this queue.
- Future reordering requires a superseding ADR.

**Renumbering note (2026-10-08):** **`exp-NNN` now matches execution order** `001 → 002 → 003`. Hypothesis ids **H1 / H2 / H3** are unchanged (H3 = seg = **exp-002**; H2 = merge = **exp-003**). Do not confuse with exp-001 run tags such as `sahi_bank_003` or ladder tag `003` — those are inference labels, not experiment ids.

**Sequencing note (2026-10-13):** H1 (exp-001a) and H3 (exp-002, closed preliminary) are done. The remaining bottleneck is **small-tree detection**, not mask choice. **[[experiments/r-class-itd/exp-004-rgb-small-student-pseudo-v2]]** is the next GPU tranche. **H2 ([[experiments/r-class-itd/exp-003-merge-fusion-v1]]) and any H3 follow-up** (deferred ECSeg / StarDist) **wait** until exp-004 meets its single-checkpoint SAHI-400 usefulness gate versus Round 1 FT. This note inserts exp-004; it does not reopen H3 or replace ADR-002. A later ADR is required only if the team drops H2 entirely.

Proposed superseded by ADR-003 (2026-10-21).

## ADR-003: Normal-forest priority; close exp-004 without training (2026-10-21)

**Status:** proposed

**Context:** ADR-001 and the north star in [[project/research-tree-detection-ensemble]] target dense stands before thinning. ADR-002 plus the 2026-10-13 note put [[experiments/r-class-itd/exp-004-rgb-small-student-pseudo-v2]] next and held H2 ([[experiments/r-class-itd/exp-003-merge-fusion-v1]]) until a small-tree usefulness gate. Commercially, R-class is no longer the first bet. exp-004 has a finished procedure pilot on AREA 540 and an open human review. Training has not started. Gates stay TBD.

**Decision:**

1. Stop exp-004 before Phase B. Do not train the small-tree student. Do not fill `audit_precision_min`, `b1_r_small_margin`, `b1_ap_small_margin`, or `b1_precision_floor`. Keep the AREA 540 counts and the proposal rule as the procedure record.
2. Park [[experiments/r-class-itd/exp-003-merge-fusion-v1]] (H2). It is parked because the cohort changed, not because it is the next step after a small-tree gate.
3. The current program is [[project/research-normal-forest]]: detect one crown per tree in normal forest, then outline those crowns. The old north star stays in the wiki as history. It is not the current priority.
4. `kaxen_197_1` and AREA 540 do not score this program.
5. A DEIMv2 box at SAHI 800 becomes an ownership candidate only when one local-maxima peak lies in its core and CHM height is above the R-class floor. The height number is TBD and must be written before the CVAT task opens. CHM detections at slice 100 px are not a witness. A VLM may confirm a box the detector already drew. A VLM box is not a label, and a missing VLM box does not delete a detector box.
6. Candidates become ground truth for the crowns they mark only after a fixed human sample of that frozen rule passes a bar written before CVAT. Proposed bar, not yet signed: precision ≥ 0.95 and two-reader agreement ≥ 0.80. Precision = accept / (accept + reject + accept_resize), same as [[concepts/pseudo-label-audit-cvat]]. `accept_resize` counts against. Rejected and resize boxes in the sample are removed. Unreviewed candidates from the same rule are promoted with the rule only by the small-set path or the Wilson lower-bound path, both still to lock before CVAT. Empty pixels are not “no tree”.
7. Segmentation is out of the first experiment. Instance masks start only on owned boxes, after the ownership bar. SAM vit_h from [[experiments/r-class-itd/exp-002-rgb-seg-backend-ceiling]] is the existing mask path. ECSeg and StarDist stay deferred.
8. The same rule may later mint weak labels for a new region. That is a later use. A new geography still needs its own small human check. Round 2 showed that more area with an unchanged teacher does not transfer.

**Consequences:**

- The experiments index queue changes. exp-004’s conclusion changes. exp-003 stays unstarted. A new north star, [[concepts/normal-forest]], [[concepts/crown-ownership]], and [[experiments/normal-forest/exp-005-normal-forest-ownership-smoke]] are added.
- ADR-002 is not rewritten. The 2026-10-13 sequencing note is proposed superseded by this ADR.
- Accepting ADR-003 still requires the team to lock the precision bar and the height floor before any CVAT import.
