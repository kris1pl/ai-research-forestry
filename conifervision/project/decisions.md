---
title: Methodological decisions (ADR)
type: Project
description: "ADR format: Context → Decision → Consequences. The agent adds an entry after team agreement."
tags: [adr]
status: stable
updated: 2026-08-21
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
4. **Kill / do not ship v1** if dense primary metric does not improve after the agreed label and tuning budget, or if fusion only shifts error modes without net dense gain.
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
   - **H1** — [[experiments/exp-001-per-layer-baselines]] first
   - **H3** — [[experiments/exp-003-rgb-seg-backend-ceiling]] next (optional narrow parallel only if H1 tiles/labels already ready)
   - **H2** — [[experiments/exp-002-merge-fusion-v1]] last, using mask backend from H3 when available
2. Human gate after each experiment Conclusion before starting the next GPU tranche.
3. If H1 kill criteria fire (no dense labels) → pause H3/H2 and escalate data program (Phase 3).
4. If H3 kill criteria fire (all masks unusable) → do not treat H2 Variant B as the primary path.
5. Numeric success thresholds remain TBD under ADR-001 until the evaluation protocol is locked.

**Consequences:**

- Coding/GPU module should prioritize handoff from exp-001.
- Index / Current focus should list this queue.
- Future reordering requires a superseding ADR.
