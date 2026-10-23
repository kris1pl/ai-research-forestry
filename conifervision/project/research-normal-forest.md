---
title: Normal-forest crown detection and segmentation
type: Project
description: "Proposed program: one box per crown on trees larger than R-class where a peak maps to one crown, then outlines after those boxes are trusted. ADR-003 is proposed."
tags: [research, normal-forest, detection, segmentation, crown-ownership]
status: draft
updated: 2026-10-22
generated:
  by: agent:conifervision-wiki
  at: 2026-10-21T10:51:00Z
related_methods:
  - methods/deimv2-canopy
  - methods/local-maxima
  - methods/chm-detection
---

# Normal-forest crown detection and segmentation

**Status:** draft. **ADR-003** in [[project/decisions]] is **proposed**, not accepted. Accepting it still requires the team to lock the precision bar and the height floor before any CVAT import. A condensed discussion sheet is [[project/normal-forest-flow]]. It does not add a phase.

## Executive summary (for the board)

The product bet is one box per crown on trees larger than R-class, in forest where a local-maxima peak can be assigned to one crown. A small test AREA, id TBD, holds the layers already produced: RGB DEIMv2 at SAHI 800 and 400, local maxima, and CHM. People spot-check the ownership rule. They do not draw the stand. Segmentation waits until those boxes are trusted.

`kaxen_197_1` and AREA 540 do not score this program. The previous north star, [[project/research-tree-detection-ensemble]], stays in the wiki as history.

#### Takeaway

One trusted box per separable crown comes first. Outlines, and any later student, wait on that check.

## Cohort

#### For the board

This task is larger trees with tops we can tell apart. A stand where the tops clump together is outside the task, including when someone calls that stand normal forest. The height cutoff is still to be written down. It has to be written before people open the review task.

In operational terms:

- Larger than R-class. Height floor TBD, written before the audit.
- A peak maps to one crown. A stand where peaks merge into clumps is outside this task even if sales calls it normal forest.
- Not `kaxen_197_1`. Not AREA 540. Not the pre-thinning thicket in [[concepts/dense-stand-detection]].

See [[concepts/normal-forest]] and [[concepts/crown-ownership]].

#### Takeaway

The cohort is separable crowns above R-class. The test AREA is not chosen yet, and it is not a site we already used for small trees.

## Phases

#### For the board

Each phase has a gate. Naming the site does not train a model. The first human check is a sample of crown candidates. Only a passing sample turns those candidates into labels for the crowns they mark. A tighter-window box outside those crowns is a separate question. A student is not part of the first experiment. Outlines start only after the boxes are trusted.

```mermaid
flowchart LR
  p0["Name a small AREA\nfour layers on disk"] --> p1["Smoke sample\nexp-005"]
  p1 -->|pass on a small set\nor a tight interval| p2["Owned boxes\nfor those crowns"]
  p1 -->|still wide| again["Same rule\nanother sample"]
  again -->|still under the bar\nafter the read cap| tighten["Tighten the rule\nnew sample"]
  p2 --> p3["400 proposals\nseparate yes or no"]
  p2 --> p4["Score the owned set\nstudent only after that"]
  p4 --> p5["Outlines on owned boxes"]
```

0. Name the small AREA. Confirm the four layers exist: RGB DEIMv2 at SAHI 800, RGB DEIMv2 at SAHI 400, local maxima, and CHM. Do not train.
1. Smoke: build ownership candidates (SAHI 800, one peak in the core, height above the floor). Sample them. This is [[experiments/normal-forest/exp-005-normal-forest-ownership-smoke]].
2. If the sample passes, those labels are ground truth for the crowns they mark. Unread candidates are promoted only by the small-set path or the Wilson lower-bound path, both still to lock before CVAT. Pixels with no owned box stay ignore until one fully reviewed tile measures how many visible crowns have no owned box.
3. Proposals are SAHI 400 boxes whose center lies outside every owned box. Separate yes/no sample. They are not ground truth.
4. Only after phase 2, score the owned set. Only after that score, consider a student. The student is not part of exp-005.
5. Masks on owned boxes only. Start a new delineation model only if a mask joins two crowns that touch. SAM vit_h from [[experiments/r-class-itd/exp-002-rgb-seg-backend-ceiling]] is the existing mask path. ECSeg and StarDist stay deferred.
6. Weak labels for another region reuse the frozen rule plus a new small human check. They are not written into this AREA’s golden set. Round 2 showed that more area with an unchanged teacher does not transfer.

#### Takeaway

exp-005 is the sample in phase 1. It does not train, and it does not draw outlines.

## Motivation

#### For the board

R-class small-tree finding stopped being the commercial priority. [[experiments/r-class-itd/exp-004-rgb-small-student-pseudo-v2]] closed without training. The useful piece of that pilot is the procedure: a wide-window box is usually one crown, and a tighter box is a proposal only when its center sits outside that crown. [[experiments/r-class-itd/exp-003-merge-fusion-v1]] stays parked because the cohort changed. This page does not fuse layers. An 800 box becomes a candidate when one peak sits in its core and the height is above the floor ([[concepts/crown-ownership]]).

### Illustration, not a milestone, not a gate

One 800×800 tile, file `01_y0_x0.jpg`, cut from `research/exp-004/image (1).png`. Not AREA 540. Not golden. `svk_full` SAHI 800 found 100 crowns. A Gemini 4 hole-fill pass listed 230. SAHI 400 found 317, of which 194 have their center outside every 800 box. Of the Gemini boxes whose centers fall outside the 800 map, 120 contain a 400-proposal center and 12 do not. Forty of the 194 proposals lie in no Gemini box. Forty-five of the 317 slice-400 boxes have their center outside every Gemini box.

Read this as: the 800 map is the crown layer, 400 is the proposal layer, and the VLM is a review aid. These counts are not success thresholds. A VLM box is not a label. A missing VLM box does not delete a detector box.

#### Takeaway

The tile shows how to read the three layers. It does not pass a gate and it does not name the test AREA.

## Related

- [[project/normal-forest-flow]] — condensed path for discussion; does not add a phase
- [[project/decisions]] — ADR-003 (proposed)
- [[project/research-tree-detection-ensemble]] — previous north star; background as of 2026-10-21
- [[concepts/normal-forest]]
- [[concepts/crown-ownership]]
- [[concepts/dense-stand-detection]]
- [[concepts/pseudo-label-audit-cvat]]
- [[concepts/canopy-height-model]]
- [[experiments/normal-forest/exp-005-normal-forest-ownership-smoke]]
- [[experiments/r-class-itd/exp-004-rgb-small-student-pseudo-v2]]
- [[experiments/r-class-itd/exp-003-merge-fusion-v1]]
- [[experiments/r-class-itd/exp-002-rgb-seg-backend-ceiling]]
- [[methods/deimv2-canopy]]
- [[methods/local-maxima]]
- [[methods/chm-detection]]
