---
type: Source
title: "Robust height-diameter allometries for 41 European tree species: stand characteristics and structure matter (Supplementary Data)"
description: "Supplementary tables, parameter estimates, and local recalibration formulations for height-diameter allometries across 41 European tree species."
tags: [allometry, dbh, height-diameter, nfi, forestry, calibration]
status: stable
updated: 2026-06-09
source_file: raw/papers/Robust height-diameter allometries for 41 European tree species - supplementary data-2025.09.29.679156v2_media-1.pdf
authors:
  - Patrick Vallet
  - et al.
year: 2025
replication_status: partial
related_methods:
  - methods/chm-detection
  - methods/dinov3-classification
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-06-09T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Robust height-diameter allometries for 41 European tree species - supplementary data-2025.09.29.679156v2_media-1.pdf
    title: "Robust height-diameter allometries for 41 European tree species: stand characteristics and structure matter (Supplementary Data)"
---

# Robust height-diameter allometries for 41 European tree species: stand characteristics and structure matter (Supplementary Data)

## Summary

This supplementary document provides calibration dataset descriptions, parameter fits, and a local recalibration routine for generalised height-diameter ($H\text{--}DBH$) models covering 41 European temperate and Mediterranean tree species derived from French National Forest Inventory (NFI) data.

The underlying model formulation predicts tree height as a function of diameter at breast height ($DBH$), plot quadratic mean diameter ($D_g$), stand basal area ($BA$), and silvicultural stand structure (even-aged, uneven-aged, coppice-with-standards, coppice). Crucially, the authors detail a four-tree local recalibration procedure using site random effects that halves residual prediction error ($RMSE$ dropped from $3.70\,\text{m}$ to $1.76\,\text{m}$ on a test *Fagus sylvatica* stand).

## Key claims

- **Species-specific calibration:** Parameter tables ($a_{s1}\dots a_{s4}, b_{s1}\dots b_{s2}, c_s$) are fitted for 41 major European tree species across broad conifer and broadleaved taxa (Table S5).
- **Structure covariates:** Incorporating stand structure (regular even-aged, irregular uneven-aged, coppice, coppice-with-standards) alongside competition metrics ($BA, D_g$) captures morphological shifts in height-to-diameter ratio.
- **Local recalibration power:** Selecting just four measured trees per plot (the three largest diameter trees and one smallest diameter tree) allows estimating the local plot random effect $\lambda_{m,j}$, cutting plot $RMSE$ substantially (e.g., $3.70\,\text{m} \to 1.76\,\text{m}$ on remaining trees; Section C).

## Implications for our pipeline

- **Inverting $H \to DBH$ from Drone CHM:** Our production AREA pipeline ([[project/pipeline-overview]]) directly extracts individual tree height tops from photogrammetric CHMs ([[concepts/canopy-height-model]]). Combined with species classifications from [[methods/dinov3-classification]], these equations can be inverted or solved numerically to infer $DBH$ and timber volume from drone heights when local stand metrics ($BA, D_g$) or regional inventory baselines are known.
- **Support for merchantable volume estimation:** Connects individual tree detection in [[concepts/normal-forest]] and [[concepts/site-index-and-yield]] to standard European forestry metrication without requiring direct point-cloud stem segmentation ([[concepts/direct-stem-dbh-point-cloud]]).
- **Calibration via sparse field samples:** If drone-based surveys are paired with quick sub-sample field plots (sampling 4 reference trees: 3 dominant, 1 suppressed), the local adjustment factor $\lambda_{m,j}$ can directly remove regional height-bias across the drone tract.

## Replication pseudocode

### Prerequisites

- Species identification from classifier (e.g., DINOv3).
- Tree height $H$ (from CHM summit / local maxima) or $DBH$ from field/point-cloud extraction.
- Stand-level basal area $BA$ ($\text{m}^2/\text{ha}$) and quadratic mean diameter $D_g$ ($\text{cm}$).
- Silvicultural structure type: Even-aged (`EA`), Uneven-aged (`UA`), Coppice-with-standards (`CWS`), or Coppice (`C`).
- Parameter estimates from Table S5 ($a_{s1}, a_{s,\text{struct}}, a_{s2}, a_{s3}, a_{s4}, b_{s1}, b_{s,\text{struct}}, b_{s2}, c_s$).

### Procedure

```text
# 1. Height Prediction from DBH (Fixed effects)
Function predict_height_fixed(dbh, Dg, BA, structure, params):
    # Select structure indicator offsets
    as_struct = select_structure_offset(structure, params.as_UA, params.as_CWS, params.as_C)
    bs_struct = select_structure_offset(structure, params.bs_UA, params.bs_CWS, params.bs_C)
    
    # Asymptote term (Equation 4')
    asymptote = 1.3 + params.as1 * (1.0 + as_struct) * (1.0 + params.as2 * BA) * (1.0 - exp(-params.as3 * (Dg ** params.as4)))
    
    # Sigmoid shape denominator
    ratio = dbh / Dg
    denom = 1.0 + (params.bs1 * (1.0 + bs_struct) * exp(-params.bs2 * BA)) / (ratio ** params.cs)
    
    h_pred = asymptote * (1.0 / denom)
    return h_pred

# 2. Local Recalibration using 4 field-measured trees
Function compute_local_lambda(field_trees, Dg, BA, structure, params):
    # field_trees: list of 4 trees (3 largest DBH, 1 smallest DBH) with measured h_tot and dbh
    sum_ratio = 0.0
    For tree in field_trees:
        h0 = predict_height_fixed(tree.dbh, Dg, BA, structure, params)
        sum_ratio += (tree.h_tot - 1.3) / (h0 - 1.3)
    
    lambda_mj = (sum_ratio / len(field_trees)) - 1.0
    return lambda_mj

# 3. Predict Recalibrated Height
Function predict_height_local(dbh, Dg, BA, structure, params, lambda_mj):
    h0 = predict_height_fixed(dbh, Dg, BA, structure, params)
    h_calibrated = 1.3 + (h0 - 1.3) * (1.0 + lambda_mj)
    return h_calibrated
```

### Gaps / not specified in paper

- **Direct inversion formulation ($H \to DBH$):** The equations are formulated exclusively for $DBH \to H$. Because $H$ is the observable metric from remote sensing (UAV photogrammetry / CHM), numerical root-finding (e.g., Newton-Raphson or Brent's method) is required to solve for $DBH$.
- **Stand-level parameter availability:** Calculating $D_g$ and $BA$ prior to stem diameter prediction requires an initial stand-level estimate or iterative approximation from crown area / height distributions.

## Quotes

- **Local recalibration sampling strategy (Section C, p. 5):**
  > "To perform a local recalibration of our height-diameter model, we selected four trees: three with the largest diameters (trees IDs 1 to 3) and one with the smallest diameter (tree ID 4)."
- **Recalibration impact (Section C, p. 5):**
  > "As a result, the root-mean square error, for the remaining 38 trees, decreases from 3.70m (fixed effects only) to 1.76m with local recalibration based on 4 trees."
- **Recalibration formulation (Section C, p. 5, Eq. 6):**
  > $\lambda_{m,j} = \frac{1}{N_j} \sum \left( \frac{h_{\text{tot},ij} - 1.3}{\hat{h}_{0,ij} - 1.3} \right) - 1$

## Related pages

- [[project/pipeline-overview]] — Operational AREA detection and DINOv3 species classification pipeline.
- [[concepts/canopy-height-model]] — Height extraction substrate from photogrammetric point clouds.
- [[concepts/site-index-and-yield]] — Stand dominant height, allometry, and yield estimation concepts.
- [[concepts/normal-forest]] — Application scope for dominant crown and stem dimension estimation.
- [[concepts/direct-stem-dbh-point-cloud]] — Direct 3D geometric stem extraction vs. allometric estimation.
