---
title: "Contrasted allometries between stem diameter, crown area, and tree height in five tropical biogeographic areas"
type: Source
tags: [allometry, crown-area, dbh, tree-height, remote-sensing, biomass]
status: stable
updated: 2026-10-21
description: "Empirical study across five tropical wet regions demonstrating that DBH-crown area allometric scaling exponents remain stable across sites, whereas DBH-height scaling varies widely."
source_file: raw/papers/Blanchard_TSAF_2016.pdf
authors:
  - Elodie Blanchard
  - Philippe Birnbaum
  - Thomas Ibanez
  - Thomas Boutreux
  - Cécile Antin
  - Pierre Ploton
  - Grégoire Vincent
  - Robin Pouteau
  - Hervé Vandrot
  - Vanessa Hequet
  - Nicolas Barbier
  - Vincent Droissart
  - Bonaventure Sonké
  - Nicolas Texier
  - Narcisse Guy Kamdem
  - Donatien Zebaze
  - Moses Libalah
  - Pierre Couteron
year: 2016
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Blanchard_TSAF_2016.pdf
    title: "Contrasted allometries between stem diameter, crown area, and tree height in five tropical biogeographic areas"
---

# Contrasted allometries between stem diameter, crown area, and tree height in five tropical biogeographic areas

## Summary

Blanchard et al. (2016) compile and analyze field measurements of diameter at breast height ($\text{DBH} \ge 10\text{ cm}$), total height ($H$), and projected crown area ($\text{CA}$) for 4,148 trees across 538 species in five wet tropical regions: New Caledonia (NC), Indonesia (ID), India (IN), French Guiana (FG), and Cameroon–Gabon (CM–GA). Using ordinary least-squares regressions on log-transformed power functions ($\log y = \log b + a \log x$), the authors test for inter-site and intra-site scaling exponent stability.

Their primary finding is that the scaling exponent for $\text{DBH}\text{–}\text{CA}$ ($a \approx 1.21\text{–}1.35$, mean pooled estimate 1.237) exhibits no statistically significant variation across geographic sites ($P = 0.091$), whereas $\text{DBH}\text{–}H$ and $H\text{–}\text{CA}$ exponents vary significantly across sites ($P < 0.001$). Furthermore, partitioning by canopy position reveals a "liberation effect": shifting from sub-canopy to sun-exposed canopy trees increases the $\text{DBH}\text{–}\text{CA}$ scaling exponent (crown expansion accelerates relative to diameter) and decreases the $\text{DBH}\text{–}H$ scaling exponent (height growth levels off).

## Key claims

1. **Inter-site stability of $\text{DBH}\text{–}\text{CA}$ scaling:** Across all five biogeographic areas, the scaling exponent of $\text{DBH}\text{–}\text{CA}$ fell within a narrow range (1.212 to 1.354), showing no statistically significant variation ($F$-test, $P = 0.091$, p. 123). The pooled exponent was 1.237 (95% CI: 1.198–1.275).
2. **Inter-site variability of $\text{DBH}\text{–}H$ and $H\text{–}\text{CA}$:** In contrast, scaling exponents varied sharply across sites for $\text{DBH}\text{–}H$ (0.374 to 0.631, $P < 0.001$) and $H\text{–}\text{CA}$ (0.828 to 1.795, $P < 0.001$, p. 123, 125).
3. **Canopy emergence ("liberation") allocation shift:** Within sites, transitioning from sub-canopy to canopy trees systematically increased the $\text{DBH}\text{–}\text{CA}$ exponent (by 17% to 30%) and decreased the $\text{DBH}\text{–}H$ exponent (by 5% to 75%, p. 125, 126).
4. **Deviation from Metabolic Theory of Ecology (MTE):** The pooled $\text{DBH}\text{–}\text{CA}$ scaling exponent (1.237) was significantly lower than the MTE prediction of $4/3 \approx 1.333$ ($P < 0.050$), although two individual sites (NC and ID) did not reject $4/3$ (p. 123, 125).
5. **High residual crown plasticity:** For a given $\text{DBH}$, the coefficient of variation ($\text{CV}$) of crown area was 3 to 5 times larger than that of height ($\text{CV}_{\text{CA}} = 94\%\text{–}126\%$ vs. $\text{CV}_H = 29\%\text{–}47\%$, p. 123, 126).

## Implications for our pipeline

- **Inversion of stem diameter from drone crown segmentations:** While our primary pipeline focuses on orthophoto and [[concepts/canopy-height-model|CHM]] detection via [[methods/deimv2-canopy]] and local maxima ([[project/pipeline-overview]]), converting 2D crown polygons or bounding boxes to diameter and stem volume requires allometric linkage ([[concepts/tree-allometry]]). The observed inter-site stability of the $\text{DBH}\text{–}\text{CA}$ power exponent suggests that crown area derived from instance segmentation models can serve as a robust regional predictor of quadratic mean diameter without recalibrating exponents across stands.
- **Canopy vs. sub-canopy stratification:** The strong shift in allocation at canopy emergence corroborates our multi-layer height stratification (e.g., lower vs. upper CHM layer inference in [[project/pipeline-overview]]). Crowns segmented in the upper dominant canopy cannot use the same height-to-crown or diameter-to-crown equations as suppressed stems ([[concepts/understory-tree-detection]]).
- **Error expectations for individual tree metrics:** Due to crown plasticity ($\text{CV}_{\text{CA}} \approx 100\%$), individual-tree $\text{DBH}$ predictions derived purely from crown area will retain substantial per-tree variance; aggregating crown distributions over forest management units or stand parcels will provide much more stable estimates than single-crown predictions.

## Replication pseudocode

### Prerequisites

- Tree inventory table containing per-stem measurements: $\text{DBH} \ge 10\text{ cm}$, total height $H \ge 4\text{ m}$, and crown projected radii or diameters in orthogonal axes.
- Stratification field: Crown light exposure index or site-specific height threshold dividing sub-canopy vs. canopy exposure.

### Procedure

```text
# 1. Crown Area (CA) computation
# If 4 orthogonal radii (r1, r2, r3, r4) available:
CA = (pi / 4) * (r1*r2 + r2*r3 + r3*r4 + r4*r1)
# If 2 orthogonal diameters (d1, d2) available:
r_mean = (d1 + d2) / 4.0
CA = pi * (r_mean ** 2)

# 2. Stratification
# Split dataset by canopy exposure index (Dawkins 4/5 vs 1/2/3) or height threshold H_canopy
canopy_subset = data[data.H >= H_canopy]
sub_canopy_subset = data[data.H < H_canopy]

# 3. Log-Log OLS Allometric Fitting
# Fit power model: log(y) = log(b) + a * log(x)
fit_model(log(CA), log(DBH)) -> returns scaling_exponent_a, intercept_b, MSE
fit_model(log(H), log(DBH))  -> returns scaling_exponent_a, intercept_b, MSE
fit_model(log(CA), log(H))   -> returns scaling_exponent_a, intercept_b, MSE

# 4. Back-transformation with Baskerville correction
# Predicted y_hat = b * (x ** a) * exp(MSE / 2.0)

# 5. Breakpoint Analysis
# Run Davies' test across 1000 candidate DBH values to test for non-constant slopes
# Fit segmented regression using the detected breakpoint as initialization
```

### Gaps / not specified in paper

- **Crown projection overlap:** In closed stands, edge boundary delineation protocols between overlapping neighboring crowns are not fully formalized; crown shyness gaps and overlapping branches are simplified into orthogonal radii approximations.
- **Drone canopy view bias:** Field-measured crown area accounts for ground-projected radii, which includes foliage hidden beneath adjacent overtopping crowns. Airborne drone orthophoto segmentation only perceives zenithal sunlight-exposed crown surface area.
- **Conifer stand applicability:** The paper samples wet broadleaf tropical rainforests ($\text{DBH} \ge 10\text{ cm}$). Applicability of the $a \approx 1.24$ exponent to temperate or boreal conifer stands (e.g., *Pinus*, *Picea*) requires separate empirical validation.

## Quotes

- "Across five biogeographic areas, DBH-CA allometry was characterized by inter-site homogeneity and intra-site heterogeneity, whereas the reverse was observed for DBH-H allometry." (Abstract, p. 117)
- "Our results indicated that, in contrast to both DBH-H and H-CA allometries, DBH-CA allometry shows no significant inter-site variation. This fairly invariant scaling calls for increased effort in documenting crown sizes as part of tree morphology." (Abstract, p. 117)
- "In addition, our results point to inverse changes in the scaling exponent of the DBH-CA vs. DBH-H allometries when shifting from sub-canopy to canopy trees, suggesting a change in carbon allocation when a tree reaches direct light." (Abstract, p. 117)
- "The scaling exponent of the DBH-CA allometry revealed no significant variations (F test, P = 0.091) across the five study sites. The scaling exponent of the mean DBH-CA allometry (across all sites) was 1.237 (with a confidence interval ranging from 1.198 to 1.275)..." (Results, p. 123)

## Related pages

- [[concepts/tree-allometry]]
- [[concepts/canopy-height-model]]
- [[concepts/site-index-and-yield]]
- [[concepts/understory-tree-detection]]
- [[project/pipeline-overview]]
- [[project/research-normal-forest]]
