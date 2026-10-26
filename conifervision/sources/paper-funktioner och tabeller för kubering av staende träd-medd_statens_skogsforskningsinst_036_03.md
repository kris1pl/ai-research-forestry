---
title: "Functions and Tables for Computing the Cubic Volume of Standing Trees: Pine, Spruce and Birch in Southern Sweden, and in the Whole of Sweden"
type: Source
tags: [allometry, volume, stem-volume, taper, national-forest-inventory, scandinavia]
status: stable
updated: 2026-10-24
description: "Foundational Swedish empirical equations and volume tables for Pinus sylvestris, Picea abies, and Betula spp. using DBH, height, crown ratio, and bark thickness."
source_file: raw/papers/FUNKTIONER OCH TABELLER FÖR KUBERING AV STAENDE TRÄD-medd_statens_skogsforskningsinst_036_03.pdf
authors:
  - Manfred Näslund
year: 1947
replication_status: completed
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/FUNKTIONER OCH TABELLER FÖR KUBERING AV STAENDE TRÄD-medd_statens_skogsforskningsinst_036_03.pdf
    title: "Funktioner och tabeller för kubering av stående träd: Tall, gran och björk i södra Sverige samt i hela landet"
---

# Functions and Tables for Computing the Cubic Volume of Standing Trees: Pine, Spruce and Birch in Southern Sweden, and in the Whole of Sweden

## Summary

This work provides empirical allometric formulas and lookup tables for calculating the standing stem volume of Scots pine (*Pinus sylvestris*), Norway spruce (*Picea abies*), and birch (*Betula pendula* / *Betula pubescens*) across Southern Sweden as well as nationally. Extending earlier work focused on Northern Sweden, the analysis relies on destructive section-wise measurements of thousands of sample trees. 

The study models the breast-height form factor ($f$) and converts it to cubic volume ($v$ in $\text{dm}^3$) above stump (defined as 1% of tree height) both with bark and inside bark. Two levels of equations are established:
1. **Shortened functions:** Requiring only diameter breast height ($d$) and tree height ($h$).
2. **Complete functions:** Incorporating crown ratio ($K$) and/or bark percentage ($B$) / double bark thickness ($b$) for greater precision.

The derived equations replaced older, subjective form-point estimation methods in Swedish National Forest Inventories and remain the national benchmark for Scandinavian single-tree volume estimation.

## Key claims

- Replaces subjective visual form-point assessments with an objective mathematical framework using readily measurable tree characteristics.
- Includes butt-swell in the stem volume calculations by using sectional measurements starting directly above a standardized stump height (1% of tree height).
- Provides distinct regression models for Southern Sweden and transition zones covering all of Sweden, compensating for regional differences in stem taper and bark thickness.
- Demonstrates that shortened functions relying purely on DBH and height provide acceptable accuracy for standard forestry tasks, while complete models (incorporating crown ratio and bark metrics) yield lower residuals where high accuracy is demanded.
- Age was found not to explain significant additional form-factor variance once diameter, height, crown ratio, and bark percentage were taken into account.

## Implications for our pipeline

- **Volume and Biomass Attribution:** In the Conifervision pipeline, once individual trees are detected via [[concepts/canopy-height-model]]/CHM processing and species is assigned via [[methods/dinov3-classification]], height ($h$) is obtained from photogrammetric or LiDAR surfaces. If DBH ($d$) is estimated via allometric height-to-DBH models or [[concepts/direct-stem-dbh-point-cloud]], Näslund's shortened functions serve as the primary Scandinavian standard for merchantable stem volume inside and outside bark.
- **Crown Ratio Integration:** For refined estimations in the complete functions, crown ratio ($K$) can be extracted directly from point clouds or segmented crown masks using relative height metrics (distance from peak to crown base).
- **Merchantable Crown Evaluation:** Directly supports stand-level inventory calculations within [[concepts/site-index-and-yield]] and merchantability thresholds discussed in [[concepts/normal-forest]].

## Replication pseudocode

### Prerequisites

- Tree species classification: Pine (*Pinus sylvestris*), Spruce (*Picea abies*), or Birch (*Betula* spp.).
- Total tree height $h$ (meters), measured from ground level.
- Diameter breast height $d$ (centimeters) at 1.3 m above ground.
- Optional for complete models: crown ratio $K$ (% of total height), crown base height $k$ (m), double bark thickness $b$ (mm), or bark percentage $B$ (%).

### Procedure

```text
# Compute individual tree stem volume above stump using Näslund (1947)
# Inputs: species, region ('southern' or 'national'), d (cm), h (m), bark_mode ('outside' or 'inside')

1. Select model coefficients based on species, geographic region, and bark mode:
   - For standard UAV pipelines without direct bark measurements, select shortened function v = f(d, h).
   - If crown base height k is extracted from 3D point cloud slices, use the complete function v = f(d, h, k, ...).

2. Evaluate Shortened Cubic Volume (Southern Sweden, volume outside bark in dm3):
   if species == "pine":
       v = 0.1072 * (d**2) + 0.02427 * (d**2 * h) + 0.007315 * (d * h**2)
   elif species == "spruce":
       v = 0.1104 * (d**2) + 0.01925 * (d**2 * h) + 0.01815 * (d * h**2) - 0.04936 * (h**2)
   elif species == "birch":
       v = 0.1432 * (d**2) + 0.008561 * (d**2 * h) + 0.02180 * (d * h**2) - 0.06630 * (h**2)

3. Evaluate Shortened Cubic Volume (Southern Sweden, volume inside bark in dm3):
   if species == "pine":
       v = 0.06271 * (d**2) + 0.03208 * (d**2 * h) + 0.005725 * (d * h**2)
   elif species == "spruce":
       v = 0.1076 * (d**2) + 0.01929 * (d**2 * h) + 0.01723 * (d * h**2) - 0.04615 * (h**2)
   elif species == "birch":
       v = 0.09944 * (d**2) + 0.01862 * (d**2 * h) + 0.01278 * (d * h**2) - 0.03544 * (h**2)

4. Convert volume:
   volume_m3 = v / 1000.0

5. Return volume_m3
```

### Gaps / not specified in paper

- DBH range is parameterized primarily for merchantable trees with $d \ge 5\text{ cm}$; separate equations were designated for saplings and young regenerating stands ($d < 5\text{ cm}$).
- For aerial remote sensing, DBH ($d$) is not observed directly and must be estimated via empirical crown diameter/height allometry or point-cloud stem fitting.
- Double-stemmed and forked trees were excluded from the sampling calibration; applying the formula to multi-stemmed broadleaves introduces bias.

## Quotes

- The objective was to replace subjective ocular assessments of form points with measurable parameters: *Summary / Ch. II* (p. 43–44).
- The definition of stump height is standardized to one percent of tree height from the ground: *Ch. II* (p. 43).
- Evaluation of tree age indicated no significant residual explanation in form factor when diameter, height, crown ratio, and bark metrics were included: *Ch. II* (p. 44).

## Related pages

- [[project/pipeline-overview]]
- [[concepts/site-index-and-yield]]
- [[concepts/canopy-height-model]]
- [[concepts/normal-forest]]
- [[concepts/direct-stem-dbh-point-cloud]]
