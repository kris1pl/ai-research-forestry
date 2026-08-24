---
title: Hypothesis validation loop
type: Project
description: "How humans and LLM agents propose, refine, and validate/reject experiments toward dense-stand tree detection — wiki scientist vs GPU engineer handoff."
tags: [research, hypothesis, experiment, workflow, ensemble]
status: stable
updated: 2026-08-24
generated:
  by: agent:conifervision-wiki
  at: 2026-08-24T12:00:00Z
related_methods:
  - methods/merge-detections
  - methods/deimv2-canopy
  - methods/edgecrafter-ecseg
---

# Hypothesis validation loop

This page defines how the Conifervision wiki supports **testable research hypotheses** toward the production objective: individual tree detection/segmentation in forest complexes, especially **dense stands before thinning**, using drone orthophotos and 3D/CHM data.

North star program: [[project/research-tree-detection-ensemble]]. Agent operation: `AGENTS.md` → **Operation: Hypothesis**. Cursor rule: `.cursor/rules/hypothesis-from-wiki.mdc`.

## Roles

| Role | Where | Responsibility |
|------|--------|----------------|
| **Scientist agent** | This wiki repo | Read compiled knowledge; propose 2–3 hypotheses with citations; after human pick, write full `experiments/exp-NNN-*.md` (pseudocode, metrics, success/kill) |
| **Human gate** | Review | Choose hypothesis; approve/reject run (ADR); interpret results; prevent GPU spend on non-falsifiable ideas |
| **Engineer agent** | External code repo + cloud GPU | Implement from Experiment handoff; run jobs; return metrics/run IDs — **not** maintained in this vault |

Language of truth: we **validate** or **reject** (or iterate). We do not “prove” hypotheses in a mathematical sense.

## Artifact handoff

```text
Wiki (index + research program + methods/concepts/sources)
        │
        ▼
Scientist agent → 2–3 candidates (chat) → human picks one
        │
        ▼
experiments/exp-NNN-*.md
  • falsifiable hypothesis
  • high-level pseudocode (inputs/outputs/parameters; Gaps; Prerequisites)
  • evaluation protocol + success/kill criteria
        │
        ▼
Optional ADR: approved to run | rejected
        │
        ▼
Engineer module (code repo / GPU) ← handoff section only
        │
        ▼
Results → update Experiment Conclusion + methods Replication notes
```

## What stays in this repo

- Experiment pages, ADRs, method/concept/source synthesis, log entries
- High-level **pseudocode** (not production training scripts)
- Links to run IDs / MLflow **when** [[project/code-repo-integration]] is done (until then: prose placeholders only)

## What does **not** stay here

- Model weights, large datasets, Delta Lake tables
- Training orchestration, GPU job configs, invented production file paths
- Numeric thresholds not grounded in literature or marked `TBD` / field calibration

## Experiment as the hypothesis unit

Every durable hypothesis is an OKF `type: Experiment` page under `experiments/`. Template: `conifervision/.templates/experiment.md`.

Required substance:

- **Hypothesis** — one falsifiable sentence
- **Motivation** — wiki citations (`[[methods/…]]`, `[[sources/…]]`, `[[concepts/…]]`)
- **Pseudocode** — procedural sketch for the engineer module
- **Evaluation** — open vs dense, size bins (see [[concepts/dense-stand-detection]])
- **Success / kill criteria** — when to stop spending GPU
- **Conclusion** — `accept` | `reject` | `iterate`

## Success and kill criteria (examples)

Define per experiment; align with [[project/decisions]] ADR-001 when accepted.

- **Success (example structure):** improvement on dense split for a named metric family vs a named baseline, without catastrophic regression on open stands — numeric thresholds **TBD** until evaluation protocol is locked.
- **Kill (examples):** no lift vs baseline after agreed label budget; fusion increases duplicates without dense gain; cannot run eval on held-out AREA.

## Related

- [[project/research-tree-detection-ensemble]]
- [[project/decisions]]
- [[project/pipeline-overview]]
- [[concepts/dense-stand-detection]]
- [[experiments/exp-001-per-layer-baselines]]
- [[experiments/exp-002-merge-fusion-v1]]
