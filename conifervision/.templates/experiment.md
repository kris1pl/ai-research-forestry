---
title: "{{title}}"
type: Experiment
description: ""
tags: []
status: draft
updated: {{date}}
area: ""
hypothesis: ""
metrics: {}
related_methods: []
sources: []
generated:
  by: agent:conifervision-wiki
  at: {{date}}T12:00:00Z
---

# {{title}}

## Hypothesis

<!-- One falsifiable sentence (also mirror in frontmatter `hypothesis`). -->

## Motivation

<!-- Cite wiki pages: [[methods/…]], [[sources/…]], [[concepts/…]], [[project/research-tree-detection-ensemble]]. -->

## Pseudocode

**Inputs:**

**Outputs:**

**Parameters:** (named; use `TBD` or “per field calibration” — do not invent numeric thresholds)

```text
1. …
```

### Prerequisites

### Gaps

## Evaluation protocol

- Split: open vs dense — [[concepts/dense-stand-detection]] (definition TBD until locked)
- Size bins: align with CHM / DEIMv2 height layers (TBD if not yet specified)
- Primary metrics: (fill `metrics` in frontmatter)

## Success criteria

-

## Kill criteria

-

## Setup

## Runs

| Run | Config / baseline | Notes |
|-----|-------------------|-------|
| | | |

## Results

| Run | Metric | Value | Split | Notes |
|-----|--------|-------|-------|-------|
| | | | | |

## Conclusion

<!-- accept | reject | iterate — with one-paragraph rationale -->

## Handoff to coding module

What the engineer agent needs (no invented production paths):

- Data assumptions (ortho, CHM, labels) — describe, do not invent Delta Lake paths
- Deliverables expected back (metrics table, run id / MLflow when integrated)
- Out of scope for this wiki repo (weights, training scripts)

## Related
