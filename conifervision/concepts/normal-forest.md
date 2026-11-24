---
title: Normal forest
type: Concept
description: "Merchantable crowns larger than R-class, with separable tops. Not any stand that is not R, and not closed canopy before thinning."
tags: [normal-forest, cohort, detection]
status: stable
updated: 2026-10-29
generated:
  by: agent:conifervision-wiki
  at: 2026-10-21T10:51:00Z
related_methods:
  - methods/local-maxima
  - methods/deimv2-canopy
  - methods/chm-detection
---

# Normal forest

## Executive summary (for the board)

Normal forest here means merchantable crowns larger than R-class, with separable tops. It is not “any stand that is not R” and it is not closed canopy before thinning.

The program that uses this cohort is [[project/research-normal-forest]]. How a box becomes the crown it marks is [[concepts/crown-ownership]]. The closed canopy this page leaves out is [[concepts/dense-stand-detection]].

#### Takeaway

Separable tops, larger than R-class. A sales name does not put a clumped stand into this cohort.

## Operational cohort

#### For the board

A tree is in this cohort when its tree height is at least 7 m and one peak can be given to one crown. Tree height is the local-maxima peak's Z. Young stands with space between small crowns, and thickets before thinning, are other tasks.

- Larger than R-class. Tree height at least 7 m.
- A peak maps to one crown. A stand where peaks clump is outside this task even if sales calls it normal forest.
- Not `kaxen_197_1`. Not AREA 540. Not the pre-thinning thicket in [[concepts/dense-stand-detection]].

`kaxen_197_1` and AREA 540 do not score [[project/research-normal-forest]]. The exp-005 test AREA id is 663-17568.

#### Takeaway

The exp-005 site is AREA 663-17568. Do not reuse the small-tree sites as the score for this cohort.

## Related

- [[project/research-normal-forest]]
- [[concepts/crown-ownership]]
- [[concepts/dense-stand-detection]]
- [[project/research-tree-detection-ensemble]]
- [[methods/local-maxima]]
- [[concepts/canopy-height-model]]
