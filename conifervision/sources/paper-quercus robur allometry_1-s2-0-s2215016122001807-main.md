---
type: Source
title: "Adapting a Quercus robur allometric equation to quantify carbon sequestration rates on the Middle Elbe floodplain"
description: "Presents a 1-parameter quadratic allometric equation estimating total carbon stock and carbon sequestration rate from DBH alone for Quercus robur."
tags: [allometry, carbon-stock, quercus-robur, dbh, biomass, floodplain-forest]
status: stable
updated: 2026-10-23
source_file: raw/papers/Quercus robur allometry_1-s2.0-S2215016122001807-main.pdf
authors:
  - Heather Alyson Shupe
  - Kai Jensen
  - Kristin Ludewig
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-23T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Quercus robur allometry_1-s2.0-S2215016122001807-main.pdf
    title: "Adapting a Quercus robur allometric equation to quantify carbon sequestration rates on the Middle Elbe floodplain"
related_methods:
  - methods/dinov3-classification
---

# Adapting a Quercus robur allometric equation to quantify carbon sequestration rates on the Middle Elbe floodplain

## Summary

This paper presents an empirical allometric adaptation that derives single-tree total (above- and below-ground) carbon stock (CS) and annual carbon sequestration rate (CSR) for Pedunculate oak (*Quercus robur*) solely from diameter at breast height (DBH). To avoid destructive felling in protected primeval floodplain forests of the Middle Elbe (UNESCO Biosphere Reserve River Landscape Elbe), the authors adapted an existing two-parameter volume equation by Dik (1984) / Zianis et al. (2005) ($H$ and $\text{DBH}$) combined with expansion factors (wood density $0.56$, carbon fraction $0.5$, root:shoot multiplier $1.3$) fitted on 966 trees. By fitting a quadratic function of DBH against the resulting carbon estimates, they eliminated the requirement for tree height ($H$), achieving an $R^2 = 0.972$ against the two-parameter formula and a strong correlation ($R^2 = 0.998$) between predicted carbon sequestration rate and basal area increment (BAI).

## Key claims

- **Height removal via quadratic fit:** Total carbon stock $\text{CS}$ ($\text{Mg tree}^{-1}$) can be parameterized as a quadratic function of $\text{DBH}$ (cm) alone:
  $$\text{CS} = a + b \cdot \text{DBH} + c \cdot \text{DBH}^2$$
  with parameters $a = -0.06$, $b = 0.00223$, and $c = 0.000316$ ($R^2 = 0.972$).
- **Annual CSR estimation:** Carbon sequestration rate ($\text{Mg tree}^{-1}\,\text{year}^{-1}$) between year $t$ and $t-1$ simplifies to the difference between annual DBH-evaluated carbon stocks:
  $$\text{CSR} = (a + b \cdot \text{DBH}_t + c \cdot \text{DBH}_t^2) - (a + b \cdot \text{DBH}_{t-1} + c \cdot \text{DBH}_{t-1}^2)$$
- **Error profile across size classes:** While the overall root mean square error (RMSE) was $1.0\,\text{Mg tree}^{-1}$, variance scales steeply with stem size:
  - $5 \le \text{DBH} < 35\,\text{cm}$: $\text{RMSE} = 0.12\,\text{Mg tree}^{-1}$
  - $35 \le \text{DBH} < 70\,\text{cm}$: $\text{RMSE} = 0.97\,\text{Mg tree}^{-1}$
  - $70 \le \text{DBH} < 140\,\text{cm}$: $\text{RMSE} = 2.6\,\text{Mg tree}^{-1}$
- **Strong proxy validation with BAI:** Annual CSR calculated from reconstructed tree ring widths (TRW) correlates strongly ($R^2 = 0.998$) with basal area increment ($\text{BAI} = \pi(r_t^2 - r_{t-1}^2)$).

## Implications for our pipeline

- **Downstream yield and carbon estimation:** In [[project/pipeline-overview]], after tree detection and species attribution (identifying *Quercus robur* via [[methods/dinov3-classification]]), biomass or carbon stock can be estimated. However, our drone pipeline natively extracts tree height ($H$) from the [[concepts/canopy-height-model]] rather than DBH.
- **Inversion or pairing with DBH models:** To utilize this 1-parameter equation from airborne sensors, DBH must first be derived either from CHM crown dimensions / heights via empirical allometry (see [[concepts/site-index-and-yield]]) or direct point cloud trunk metrics (see [[concepts/direct-stem-dbh-point-cloud]]).
- **Error considerations for mature oak:** Because estimation variance increases markedly for $\text{DBH} \ge 70\,\text{cm}$ ($\text{RMSE} = 2.6$), stands with veteran or dominant canopy oak trees require calibrated crown-to-DBH distributions to avoid large stand-level bias.

## Replication pseudocode

### Prerequisites

- Species identification confirmed as *Quercus robur* (e.g., via crop classification).
- Stem DBH at breast height (1.3 m) in centimeters.
- Optional for CSR: Multi-year DBH measurements or tree-ring increment reconstructions ($\text{DBH}_t, \text{DBH}_{t-1}$).

### Procedure

```text
# Input: dbh_cm (float or array of annual DBH values in cm)
# Parameters for Quercus robur:
a = -0.06
b = 0.00223
c = 0.000316

# 1. Total (above- + below-ground) Carbon Stock in Mg / tree
def estimate_carbon_stock(dbh):
    if dbh < 5.0:
        # Out of calibrated range (study range 5 cm to 140 cm)
        return TBD
    cs = a + (b * dbh) + (c * (dbh ** 2))
    return max(cs, 0.0)

# 2. Annual Carbon Sequestration Rate in Mg / tree / year
def estimate_csr(dbh_current, dbh_previous):
    cs_t = estimate_carbon_stock(dbh_current)
    cs_prev = estimate_carbon_stock(dbh_previous)
    return cs_t - cs_prev
```

### Gaps / not specified in paper

- **Height-to-DBH transfer:** The model replaces $H$ with $\text{DBH}$, which suits field dendrochronology; it does not provide the inverse conversion from CHM top height ($H$) to DBH for remote sensing pipelines.
- **Crown allometry:** No crown diameter or crown area parameters are reported.
- **Geographic transferability:** Parameters are calibrated for Middle Elbe floodplain hydrological conditions; transferability to upland or water-stressed stands was not evaluated.

## Quotes

- **On adapting from volume to carbon:** "To nondestructively estimate CS and CSR, we have adapted a two-parameter allometric equation which uses tree height (H) and diameter at breast height (DBH) (Dik 1984, Zianis et al. 2005) into a 1-parameter equation that requires only DBH to quantify stocks and annual changes in carbon stock... for individual Q. robur trees." (p. 1)
- **On scale-dependent error:** "The greater the DBH, the greater we observed the RMSE to be. Trees with a 5cm ≤ DBH < 35cm had a RMSE of 0.12, trees with a 35cm ≤ DBH < 70cm had a RMSE of 0.97, and trees with a 70cm ≤ DBH < 140 cm had a RMSE of 2.6." (p. 4)
- **On BAI correlation:** "...here we find that the linear relationship between BAI and our estimated CSR is nearly perfect, with a Pearson $R^2$ of 0.998 (Fig. 2)." (p. 4–5)

## Related pages

- [[project/pipeline-overview]] — Operational pipeline from aerial CHM to species classification
- [[methods/dinov3-classification]] — Species classification producing taxonomic classes including oak
- [[concepts/site-index-and-yield]] — Stand volume, growth models, and yield metrics
- [[concepts/direct-stem-dbh-point-cloud]] — Methods deriving stem DBH directly from 3D point cloud slices
- [[concepts/canopy-height-model]] — Photogrammetric canopy height baseline used in Conifervision detection
