---
title: "Predicting crown width using nonlinear mixed-effects models accounting for competition in multi-species secondary forests"
type: Source
tags: [allometry, crown-width, competition-index, mixed-effects, chm, individual-tree-detection]
status: stable
updated: 2026-10-24
description: "Nonlinear mixed-effects crown width models incorporating tree size and competition indices across multi-species secondary forests."
source_file: raw/papers/Predicting_crown_width_using_nonlinear_mixed-effec.pdf
authors:
  - Rui Hou
  - Zongzheng Chai
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
related_methods:
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/local-maxima
sources:
  - id: primary
    resource: raw/papers/Predicting_crown_width_using_nonlinear_mixed-effec.pdf
    title: "Predicting crown width using nonlinear mixed-effects models accounting for competition in multi-species secondary forests"
---

# Predicting crown width using nonlinear mixed-effects models accounting for competition in multi-species secondary forests

## Summary

The authors formulate and evaluate crown width (CW) models for diverse secondary forests in southwest China using nonlinear mixed-effects (NLME) approaches. Using field measurements across 39 subplots containing over 2,800 trees of multiple species groups, the study tests twelve base function forms correlating stem diameter to crown extent. A power function provides the most robust empirical base. The authors then integrate additional tree-level covariates (total tree height, height to crown base) along with stand competition indices. Both distance-dependent metrics (such as the Hegyi index calculated over fixed neighbor sets) and distance-independent metrics (relative diameter sums) are compared. Including species identity as a random grouping factor alongside competition terms significantly increases explained variance ($R_a^2 > 0.55$) and reduces heteroscedasticity compared to basic single-variable equations.

## Key claims

- Single-predictor allometric models based solely on stem diameter systematically misestimate crown width across varying stand densities, overestimating dimensions in crowded conditions and underestimating them in open stands.
- A two-parameter power equation yields the most stable baseline performance among twelve mathematical forms, achieving better convergence and validation stability than higher-parameter logistic or sigmoidal equations.
- Incorporating height to crown base (HCB) and total tree height (TH) alongside competition indices substantially improves goodness-of-fit metrics across multi-species stands.
- Distance-dependent competition indices (specifically the Hegyi index over fixed neighbor counts) yield slightly superior model fits compared to distance-independent metrics; however, a strong linear correlation ($R^2 = 0.943$) exists between the distance-dependent and distance-independent measures, making non-spatial forms a practical surrogate when neighbor coordinate data are missing.
- Accounting for species-level variations via random-effect parameters on the power exponent and crown base coefficient significantly boosts predictive performance over fixed-effects formulations.

## Implications for our pipeline

- **Crown extent bounding and NMS windows**: When using local maxima or raster peak finders in [[methods/local-maxima]] and [[methods/chm-detection]], variable search window sizing can be bounded using allometric crown width estimates derived from height and local tree density instead of static pixel radii.
- **Support for crown ownership logic**: The findings align with the principles explored in [[concepts/crown-ownership]] and [[concepts/normal-forest]], highlighting that crown dimensions contract under local crowding and crown recession. Photogrammetric metrics derived from [[concepts/canopy-height-model]] (such as dominant height and nearest-neighbor density) can parameterize realistic crown bounding boxes before polygon delineation.
- **Species-stratified priors**: Because species groups showed distinct random-effect deviations in crown expansion behavior, downstream predictions from [[methods/dinov3-classification]] can be fed back into allometric models to validate whether detected crown footprints match expected biological dimensions.

## Replication pseudocode

### Prerequisites

- Tree inventories with geographic positions $(x, y)$, diameter at breast height (DBH), total height (TH), height to crown base (HCB), and species classification.
- Nonlinear mixed-effects optimization packages (e.g., `nlme` or `scipy.optimize`).

### Procedure

```text
1. Compute plot-level and neighborhood competition metrics:
   a. Distance-independent metric: Sum of relative DBH (SRD) per plot normalized by mean dominant diameter.
   b. Distance-dependent metric: Sum of Hegyi index (SHGN) using fixed-count nearest neighbors with edge reflection buffering.
2. Fit baseline power function: CW = a * (DBH ^ b).
3. Expand parameters with covariates:
   CW = (phi_1 - phi_3 * CI + phi_4 * TH + (phi_5 + u_5) * HCB) * (DBH ^ (phi_2 + u_2)) + error
   where CI is either SRD or SHGN, and u_2, u_5 are species-level random effects.
4. Model heteroscedastic residual variance as a power function of DBH.
5. Predict crown width across validation trees given detected heights, neighbor competition, and assigned species classes.
```

### Gaps / not specified in paper

- Direct extraction of HCB from aerial remote sensing: in UAV photogrammetric point clouds, crown base height is notoriously difficult to measure reliably without full waveform LiDAR or direct field measurements.
- Operational behavior on small saplings ($< 5\text{ cm}$ DBH) was grouped but showed higher relative measurement variability in dense regeneration pockets.

## Quotes

- Model performance on primary secondary forest data indicated that the power formulation served as the most effective baseline: "The Power (F2), Logistic (F10) and Quadratic (F8) functions were found to be superior... and the F2 functions performed better... during the validation stage" (p. 8).
- Addressing spatial vs. non-spatial competition: "spatially explicit models are computationally complex and difficult and can be replaced by corresponding spatially non-explicit models due to the small differences in the fit statistics" (p. 1).
- Competition effects on crown architecture: "crowding in a stand results in trees growing taller with smaller crowns and narrower crown widths" (p. 12).

## Related pages

- [[concepts/canopy-height-model]] — Photogrammetric elevation surface used to derive heights and spacing
- [[concepts/crown-ownership]] — Rules for assigning crown extent and bounding boxes around detected tree tops
- [[concepts/normal-forest]] — Structural crown models for established, non-overlapping stands
- [[methods/local-maxima]] — Variable window tree detection informed by crown width allometry
- [[project/pipeline-overview]] — Operational structure for detection, fusion, and species attribution
