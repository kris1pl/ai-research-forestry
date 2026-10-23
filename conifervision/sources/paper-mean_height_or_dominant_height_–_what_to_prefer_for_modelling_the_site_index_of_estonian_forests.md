---
title: "Mean height or dominant height – what to prefer for modelling the site index of Estonian forests?"
type: Source
tags: [forest-inventory, dominant-height, mean-height, site-index, estonia, thinning, height-curve]
status: stable
updated: 2026-10-22
description: "Comparison of mean vs dominant stand height under thinning in Estonia, showing dominant height insensitivity to low thinning and providing a conversion model (residual SD 0.466 m)."
source_file: raw/papers/Mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_Estonian_forests.pdf
authors: [Toomas Tarmu, Diana Laarmann, Andres Kiviste]
year: 2020
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-22T10:15:00Z
sources:
  - id: primary
    resource: raw/papers/Mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_Estonian_forests.pdf
    title: "Mean height or dominant height – what to prefer for modelling the site index of Estonian forests?"
---

# Mean height or dominant height – what to prefer for modelling the site index of Estonian forests?

## Summary

This study evaluates the differences between stand mean height ($h_g$, regression height at quadratic mean diameter $d_g$) and dominant height ($h_{g\text{dom}}$, defined per IUFRO as the mean height of the 100 thickest DBH trees per hectare) for forest growth and site index modeling across Estonian forests. Using repeated 5-year measurements from 753 permanent plots (3,132 total plot visits, 412,604 tree measurements) from the Estonian Network of Forest Research Plots (ENFRP), the authors evaluate height curve approximations and compare 5-year increment behavior across unthinned versus thinned stands.

The authors show that conventional mean height increases artificially following commercial thinning from below (which removes smaller subordinate stems and inflates the arithmetic/quadratic mean), introducing bias into stand growth and site index projections. In contrast, dominant height is robust to thinning interventions. The paper selects a single-parameter height-curve formulation based on Nilson (2002) to derive non-decreasing height curves and fits a practical multi-variable regression model predicting dominant height from standard stand metrics ($h_g$, $d_g$, and stand density $N$) with a residual standard deviation of 0.466 m ($R^2 = 0.995$).

## Key claims

- **Thinning artifact on mean height:** Commercial thinning from below significantly increases the observed 5-year change in stand mean height ($h_g$) for commercial species (*Pinus sylvestris*, *Picea abies*, *Betula pendula*), whereas its impact on dominant height ($h_{g\text{dom}}$) change is statistically non-significant (p. 133, Fig. 8).
- **Growth model error under thinning:** In thinned stands, standard mean height growth difference models (Kiviste 1997) exhibit higher projection errors than dominant height models (Elfving & Kiviste 1997). In undisturbed/unthinned stands, both models show comparable accuracy (p. 133, 135, Fig. 10).
- **Optimal height curve parameterization:** Among five evaluated height curves (Näslund and Nilson formulations), Nilson's single-parameter model (Equation 6) prevents descending curves on dominant trees across all cohorts while achieving an empirical prediction error standard deviation of $s_{de} = 1.45\text{ m}$ (p. 127, Table 2).
- **Dominant height regression equation:** Dominant height can be accurately derived from stand-level inventory variables ($h_g$, $d_g$, $N$) across four species groups using the equation:
  $$h_{g\text{dom}} = a_0 + 1.1165 \cdot h_g + a_1 \cdot d_g + \frac{a_2}{\sqrt{N}}$$
  yielding an overall residual standard deviation of 0.466 m and $R^2 = 0.995$ ($p < 0.0001$; p. 132–133).
- **Main species vs. dominant cohort:** In semi-natural stands—especially those dominated by Norway spruce or deciduous species—the 100 thickest trees per hectare often contain mixtures of other species; Scots pine stands remain the most uniform (p. 123, Fig. 2).

## Implications for our pipeline

- **Calibration of remote sensing height metrics:** Drone photogrammetry and [[concepts/canopy-height-model|CHM]] rasters naturally detect the uppermost canopy top envelope rather than suppressed understorey stems. Consequently, direct max/percentile heights derived from CHM or local maxima ([[methods/local-maxima]]) correlate much more closely with dominant height ($h_{g\text{dom}}$, top height of 100 trees/ha) than mean stand height ($h_g$).
- **Thinning-invariant stand monitoring:** In production pipelines ([[project/pipeline-overview]]), computing top canopy height distributions allows site index and growth estimation that remains invariant to intermediate thinning operations, whereas trying to regress stand mean height from UAV without full understorey tree detection will introduce artificial spikes post-thinning.
- **Conversion to traditional Estonian inventory attributes:** Stand registries in Estonia historically rely on mean height ($h_g$) at $d_g$. Equation 9 and the coefficients in Table 4 provide an analytical bridge to convert detected top/dominant heights back to conventional inventory variables when density ($N$) is known from individual tree detection (ITD) in [[project/research-normal-forest]].

## Replication pseudocode

### Prerequisites

- Stand inventory or remote sensing data containing:
  - Quadratic mean diameter ($d_g$ in cm)
  - Stand mean height ($h_g$ in m)
  - Stand upper-layer tree stocking density ($N$ stems per hectare)
  - Main species category: Scots pine, Norway spruce, Silver birch, or Other deciduous

### Procedure

```text
# Conversion from stand variables to dominant height (Tarmu et al. 2020, Eq. 9)

INPUT: species, h_g, d_g, N

COEFFICIENTS = {
    "Scots pine":      {"a0": 2.0494, "a1": -0.0964, "a2": -15.686},
    "Norway spruce":   {"a0": 3.3661, "a1": -0.1231, "a2": -14.070},
    "Silver birch":    {"a0": 3.0474, "a1": -0.0824, "a2": -34.854},
    "Other deciduous": {"a0": 1.7910, "a1": -0.1108, "a2": -15.215}
}

1. Look up species coefficients {a0, a1, a2} from COEFFICIENTS table.
2. Assert N > 0 and d_g > 0 and h_g > 0.
3. Compute dominant height h_gdom:
     h_gdom = a0 + (1.1165 * h_g) + (a1 * d_g) + (a2 / sqrt(N))
4. Return h_gdom (in meters)
```

### Gaps / not specified in paper

- **Inversion of Equation 9:** The paper specifies forward regression from ($h_g$, $d_g$, $N$) to $h_{g\text{dom}}$, but does not evaluate inverted parameter stability if solving directly for $h_g$ given remote-sensing derived $h_{g\text{dom}}$.
- **Extreme density bounds:** The paper does not explicitly benchmark the behavior of $a_2 / \sqrt{N}$ at very low densities ($N < 100\text{ trees/ha}$) or hyper-dense juvenile pre-thinning conditions ($N > 4000\text{ trees/ha}$).
- **Species classification threshold:** The boundary rules for grouping mixed deciduous species under the "Other deciduous" parameters are not parameterized beyond broad taxonomic groups.

## Quotes

- **On thinning distortion of mean height:** *"Figure 8 shows that for commercially important tree species (Scots pine, Norway spruce, silver birch), the change in the average mean height is significantly greater in the case of thinning when compared to undisturbed stand development. Whereas the change in the average dominant height in the case of thinning compared to undisturbed development was not significant. This is evidence of the Estonian forest management practice of applying thinning from below."* (p. 133)
- **On dominant height definition:** *"The current study uses dominant height, which is defined by the IUFRO (International Union of Forest Research Organizations) as the average height of the 100 largest trees per hectare (dominant trees)... the following research defines dominant height as the average height of the 100 trees with the largest diameters at breast height per hectare..."* (p. 122)
- **On the regression bridge:** *"The outcome is significant as the prediction precision was more than twice as accurate when compared to the empirical dominant height prediction of model (6), which had a residual standard deviation of 1.45 m. This means that the dominant height could be calculated easily from stand attributes as a new stand variable without additional measurement work."* (p. 133)

## Related pages

- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM normalization representing top canopy height
- [[concepts/normal-forest]] — Standard commercial forest stands where top height metrics apply
- [[project/pipeline-overview]] — Operational pipeline producing height layers and tree detections
- [[methods/local-maxima]] — Canopy top height extraction via local peak filtering
