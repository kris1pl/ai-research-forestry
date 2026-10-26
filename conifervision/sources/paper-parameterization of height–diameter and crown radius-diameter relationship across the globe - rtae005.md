---
title: "Parameterization of height–diameter and crown radius–diameter relationships across the globe"
type: Source
tags: [allometry, dbh, tree-height, crown-radius, pft]
status: stable
updated: 2026-10-22
description: "Global evaluation of 29 mathematical functions parameterizing tree height-DBH and crown radius-DBH across six plant functional types using the Tallo database."
source_file: raw/papers/Parameterization of height–diameter and crown radius-diameter relationship across the globe - rtae005.pdf
authors:
  - Xiang Song
  - Jinxu Li
  - Xiaodong Zeng
year: 2024
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-22T00:00:00Z
sources:
  - id: primary
    resource: raw/papers/Parameterization of height–diameter and crown radius-diameter relationship across the globe - rtae005.pdf
    title: "Parameterization of height–diameter and crown radius–diameter relationships across the globe"
related_methods:
  - methods/chm-detection
  - methods/deimv2-canopy
---

# Parameterization of height–diameter and crown radius–diameter relationships across the globe

## Summary

Song et al. (2024) evaluate 29 mathematical equations for modeling individual tree height (H) and crown radius (CR) as functions of diameter at breast height (DBH). Using over 418,000 individual tree records from the global Tallo dataset across six plant functional types (PFTs; boreal, temperate, and tropical needleleaf and broadleaf), the study analyzes predictive accuracy ($R^2$, RMSE) and functional properties. The findings show that S-shaped functions (such as Logistic curves) excel for boreal trees, Chapman–Richards functions perform best for temperate height, and exponential or fractional functions best characterize tropical and temperate crown dimensions.

## Key claims

- Standard allometric formulations used in dynamic vegetation models (typically simple power functions $H = a \cdot \text{DBH}^b$) fail to capture regional and functional variations across PFTs.
- S-shaped asymptotic curves (e.g., Logistic functions) best reproduce boreal tree height and crown dynamics, reflecting bounded growth and slow-fast-slow structural accumulation.
- Temperate tree height is best modeled by the Chapman–Richards curve, while tropical needleleaf height follows fractional functions of DBH.
- For crown radius against DBH, model performance is generally comparable across several formulations ($R^2 \approx 0.60\text{--}0.68$), with Logistic and exponential formulations achieving the highest accuracy across temperate and boreal categories.
- Predictive relative bias ($\text{RMSE} / H_{\text{obs}}$) is disproportionately elevated for small to intermediate tree classes (often exceeding 20% to 100% relative error in shorter stature bins).

## Implications for our pipeline

- **DBH Estimation from Remote Sensing:** While our pipeline directly observes height from [[concepts/canopy-height-model]] rasters and crown area from 2D crown segmentation ([[methods/deimv2-canopy]], [[project/pipeline-overview]]), operational inventory requires estimating DBH. Inverting these evaluated allometric curves enables converting remote sensing metrics ($H$, $\text{CR}$) into stem diameter and volume estimates.
- **Biomass and Volume Calculation:** Rather than using universal power laws across all surveyed regions, adopting PFT-specific curves (e.g., Chapman–Richards for temperate conifers, Logistic for boreal zones) reduces systematic biases in biomass estimation.
- **Crown Size Bounds for Prior Filters:** In automated delineation workflows such as [[concepts/crown-ownership]] and [[concepts/normal-forest]], empirical CR-to-DBH and CR-to-H curves provide dynamic boundary constraints on maximum and minimum plausible crown bounding box sizes.

## Replication pseudocode

### Prerequisites

- Global tree inventory dataset containing individual tree measurements ($H$ in m, DBH in cm, CR in m, taxonomic classification, and geographic coordinates).
- PFT mapping scheme based on latitudinal bands (boreal: $|lat| > 66.5^\circ$, temperate: $23.5^\circ \le |lat| \le 66.5^\circ$, tropical: $|lat| < 23.5^\circ$) and leaf type (needleleaf vs. broadleaf).

### Procedure

```text
# Evaluation of allometric functions across PFTs

1. Load dataset (e.g., Tallo records) and filter records where DBH > 0 and H >= 1.3 m.
2. Group records into six PFT strata:
   - Boreal Needleleaf (BN), Boreal Broadleaf (BB)
   - Temperate Needleleaf (MN), Temperate Broadleaf (MB)
   - Tropical Needleleaf (TN), Tropical Broadleaf (TB)
3. For each PFT:
   a. Fit 29 candidate regression functions for H = f(DBH) with offset C0 = 1.3 m.
   b. Fit 27 candidate regression functions for CR = f(DBH) with offset C0 = 0.0 m.
   c. Optimize parameters (a, b, c, d) using nonlinear least squares regression.
   d. Compute goodness-of-fit metrics: R-squared and RMSE.
   e. Calculate relative predictive bias across size intervals: RMSE / mean(observed).
4. Rank functions per PFT using highest R-squared, lowest RMSE, and model parsimony.
```

### Gaps / not specified in paper

- Leaf phenology (evergreen vs. deciduous distinctions) was omitted due to missing attribute flags in the base dataset.
- Stand-level competitive density, local basal area, soil parameters, and microclimate predictors were not incorporated into the bivariate fitting equations.
- Fitting convergence configurations (initial optimization seeds, bounds, optimizer algorithms) are designated as TBD.

## Quotes

- On functional form performance for boreal stands:
  > "For boreal PFTs, the S-shaped Logistic function fitted the H–DBH relationship best, while for temperate PFTs the Chapman–Richards function performed well." (p. 1)
- On relative bias trends across size classes:
  > "...relative biases in predicted H and CR were high for small or medium-sized individuals." (p. 11)

## Related pages

- [[project/pipeline-overview]] — Operational pipeline converting aerial imagery to detection crops and classifications
- [[concepts/canopy-height-model]] — Height raster extraction used as the primary remote sensing input for vertical allometry
- [[concepts/crown-ownership]] — Crown boundary and peak ownership constraints in forest stands
- [[concepts/normal-forest]] — Structural crown representation and delineation in managed forest compartments
- [[concepts/site-index-and-yield]] — Stand-level site index, dominant height, and volume growth concepts
