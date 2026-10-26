---
title: "Tree allometry of Douglas fir and Norway spruce on a nutrient-poor and a nutrient-rich site"
type: Source
tags: [allometry, crown-area, dbh, height-diameter, picea-abies, pseudotsuga-menziesii]
status: stable
updated: 2026-10-24
description: "Empirical study comparing allometric relationships (height, crown length, crown projected area vs DBH) and stem radial growth of Douglas fir and Norway spruce across nutrient-poor and nutrient-rich sites in the Czech Republic."
source_file: raw/papers/Tree allometry of Douglas fir and Norway spruce on a nutrient-poor and a nutrient-rich site_urban_dg_2012.pdf
authors:
  - Josef Urban
  - Kateřina Holušová
  - Ladislav Menšík
  - Jan Čermák
  - Petr Kantor
year: 2012
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Tree allometry of Douglas fir and Norway spruce on a nutrient-poor and a nutrient-rich site_urban_dg_2012.pdf
    title: "Tree allometry of Douglas fir and Norway spruce on a nutrient-poor and a nutrient-rich site"
---

# Tree allometry of Douglas fir and Norway spruce on a nutrient-poor and a nutrient-rich site

## Summary

Urban et al. (2012) examine the allometric relationships connecting diameter at breast height (DBH) with tree height ($h$), crown length, and projected crown area ($A_{\text{pro}}$) for Douglas fir (*Pseudotsuga menziesii*) and Norway spruce (*Picea abies*). The investigation was carried out across two climatically matched mature forest stands in the Czech Republic differing significantly in soil nutrient status (an oligotrophic Cambisol "poor site" vs. a mesotrophic Cambisol "rich site").

The authors found that site fertility strongly influences the allocation patterns of Norway spruce: spruces on the poor site were significantly shorter, had smaller projected crown areas for a given DBH, and smaller maximum stem diameters compared to the rich site. In contrast, Douglas fir biometry and allometric scaling (both height and crown area vs. DBH) showed no statistically significant sensitivity to the soil fertility differences, demonstrating wider nutrient tolerance and consistent allometric stability. For remote sensing pipelines, the paper provides species-specific parameterizations for Näslund height curves and crown-area scaling functions.

## Key claims

1. **Species-specific nutrient sensitivity:** Site fertility significantly shifted the allometric scaling of Norway spruce ($P < 0.05$ for DBH $> 31\text{ cm}$), whereas Douglas fir exhibited no significant difference in height–DBH or projected crown area–DBH scaling between poor and rich sites.
2. **Crown projected area functional form:** $A_{\text{pro}}$ scales with DBH as a power function for Douglas fir ($A_{\text{pro}} = a \cdot \text{DBH}^b$), whereas for Norway spruce it scales linearly ($A_{\text{pro}} = a \cdot \text{DBH} + y_0$).
3. **Näslund height curves:** Tree height was modeled via Näslund's formulation ($h = 1.3 + \frac{\text{DBH}^2}{(a + b \cdot \text{DBH})^2}$), achieving $R^2 = 0.64\text{--}0.87$ across species and sites (Table 3).
4. **Phenology and cambial dynamics:** Douglas fir initiates radial stem growth approximately 2 weeks earlier than Norway spruce (triggered at soil temperatures $\sim 6^\circ\text{C}$ vs. $\sim 7^\circ\text{C}$ at $30\text{ cm}$ depth).
5. **Drought response threshold:** Mild soil water deficits reduce stem increment, but severe drought ($\le -1.5\text{ MPa}$ soil water potential) causes absolute cessation of radial growth and diurnal stem shrinkage in both species.

## Implications for our pipeline

- **DBH inversion from UAV metrics:** When inverting remote sensing observables (height $h$ from [[concepts/canopy-height-model]] and crown area $A_{\text{pro}}$ from instance segmentation) back to DBH via [[concepts/height-diameter-inversion]], site fertility and species classification from [[methods/dinov3-classification]] are critical. Inverting Norway spruce requires site-index or soil calibration, while Douglas fir can utilize a generalized regional scaling curve.
- **Crown sizing priors in detection:** In [[project/research-normal-forest]] and [[concepts/crown-ownership]], bounding box and crown area priors can exploit the observed linear vs power scaling behaviors. For Norway spruce, minimum observed crown projected areas plateaued around $5\text{--}7\text{ m}^2$, establishing a physical floor for merchantable tree crown filtering.
- **Distinguishing conifer species:** Douglas fir maintained larger projected crown areas for higher DBH tiers compared to Norway spruce on equivalent sites, providing secondary geometric feature verification after spectral classification in [[project/pipeline-overview]].

## Replication pseudocode

### Prerequisites

- Species identification ($S \in \{\text{Douglas fir}, \text{Norway spruce}\}$) per segmented crown.
- Terrain-normalized CHM providing tree top height $h$ (m) and delineated crown polygon area $A_{\text{pro}}$ ($\text{m}^2$).
- Soil trophic classification (poor vs. rich/mesotrophic) for Norway spruce sites.

### Procedure

```text
# Step 1: Invert Näslund height equation to estimate DBH from CHM height h (m)
# Equation: h - 1.3 = DBH^2 / (a + b * DBH)^2
# Let H_eff = sqrt(max(0.1, h - 1.3))
# H_eff * (a + b * DBH) = DBH  =>  DBH * (1 - b * H_eff) = a * H_eff
# DBH_est = (a * H_eff) / (1 - b * H_eff)

if species == "Douglas fir":
    # Parameters stable across sites (Urban et al. 2012 Table 3)
    a = 1.32  # or 1.35
    b = 0.15
    dbh_h = (a * sqrt(h - 1.3)) / (1.0 - b * sqrt(h - 1.3))
elif species == "Norway spruce":
    if site_fertility == "poor":
        a = 1.39; b = 0.16
    else:  # rich / mesotrophic
        a = 1.44; b = 0.14
    dbh_h = (a * sqrt(h - 1.3)) / (1.0 - b * sqrt(h - 1.3))

# Step 2: Invert Crown Projected Area (A_pro) to estimate DBH
if species == "Douglas fir":
    # A_pro = a * DBH^b  =>  DBH_crown = (A_pro / a)^(1 / b)
    if site_fertility == "poor":
        a_c = 0.0005; b_c = 2.83
    else:
        a_c = 0.083; b_c = 1.55
    dbh_crown = (A_pro / a_c) ** (1.0 / b_c)
elif species == "Norway spruce":
    # A_pro = a * DBH + y0  =>  DBH_crown = (A_pro - y0) / a
    if site_fertility == "poor":
        y0 = -6.13; a_c = 0.79  # Table 3 row for Poor SM
    else:
        y0 = 22.01; a_c = 1.09  # Table 3 row for Rich SM
    dbh_crown = max(0.0, (A_pro - y0) / a_c)

# Step 3: Consistency check / fusion
dbh_final = 0.7 * dbh_h + 0.3 * dbh_crown
```

### Gaps / not specified in paper

- **Inversion stability:** The authors fit forward allometric equations ($h = f(\text{DBH})$ and $A_{\text{pro}} = f(\text{DBH})$). Direct inversion can become mathematically ill-conditioned near the horizontal asymptote where $b \cdot \sqrt{h - 1.3} \to 1$.
- **Stand competition index:** Stand density (basal area 45 vs. $54\text{ m}^2\text{ ha}^{-1}$) was not integrated as an explicit continuous covariate in the regression models.
- **Younger stand validation:** Sample trees were in mature stands (89 and 97 years old); parameters cannot be directly applied to young regeneration or R-class pre-thinning stands ($< 10\text{ m}$ height) without recalibration.

## Quotes

- *On site sensitivity differences:* "A significant difference was found in the allometric relationships of Norway spruce trees from the nutrient poor and nutrient rich site. In contrast to the Norway spruce, there was no significant effect of site fertility on allometric relationships for Douglas fir suggesting that its allocation patterns were less sensitive to site nutrient conditions." (Abstract, p. 1)
- *On tree height models:* "Specifically for the calculation of allometric relationships of tree height, we used the Näslund equation... $h = 1.3 + \frac{\text{DBH}^2}{(a + b\text{DBH})^2}$" (Materials and methods, p. 5)
- *On crown area models:* "Best fitting models to DBH were a power function for Douglas fir and a linear function for Norway spruce... The smallest crown projected areas were similar at both sites, about $5\text{ m}^2$." (Discussion, p. 8)
- *On drought response:* "Mild drought suppresses stem growth increment while strong drought (i.e. less than -1.5 MPa soil water potential) entirely stops incremental stem growth." (Conclusions, p. 10)

## Related pages

- [[concepts/height-diameter-inversion]] — Inverting remote sensing height and crown measurements to DBH
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM height layers
- [[concepts/site-index-and-yield]] — Stand productivity, site fertility, and allometric scaling
- [[concepts/normal-forest]] — Merchantable stands with separable crowns
- [[project/pipeline-overview]] — Operational AREA detection and classification flow
