---
title: Local maxima (sliding window)
type: method
tags: [detection, height, 3d, local-maxima]
status: active
updated: 2026-06-05
related_methods:
  - methods/chm-detection
  - methods/merge-detections
sources:
  - sources/popescu-wynne-2004-seeing-the-trees
---

# Local maxima

Detect tree tops from a 3D surface or **CHM** using **local maximum (LM) filtering** with a **sliding / variable-size window** to estimate height and support tree detection.

## In the pipeline

Part of the merge path — see [[merge-detections]], [[project/pipeline-overview]].

## Literature

[[sources/popescu-wynne-2004-seeing-the-trees]] — variable square and **circular** LM windows on LiDAR CHM; window size tied to height–crown relationships from field data; circular windows favored for conifers with a single apex; square vs circular choice affects commission/omission trade-offs.

## Replication notes

Full step-by-step pseudocode: [[sources/popescu-wynne-2004-seeing-the-trees#Replication pseudocode]] (see **§6 — Variable-window local maxima**).

| Paper step | Our implementation (TBD) |
|------------|---------------------------|
| LM on CHM with variable window | Core of this method |
| Window size from height–crown model | Calibrate on our species / plots |
| Square vs circular window | Test both; paper favors circular for conifers |
| Species map scales windows | Optional — paper used multispectral fusion for pines |

**Not in paper:** merge with DEIMv2 detections — see [[methods/merge-detections]]. **Gaps:** exact window coefficients — Popescu (2002); our sliding-window params in production config (when linked).

## Production parameters

_(fill in: window size, resolution, thresholds, circular vs square, variable-window rules)_

## Open questions from literature

- Do we use forest-type or species layers to scale windows (paper used multispectral fusion for pines)?
- Alignment between LM peaks and DEIMv2 boxes before [[merge-detections]].

## Related

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
