---
title: "Modelling potential yield capacity in conifers using Swedish long-term experiments"
type: Source
tags: [forestry, allometry, site-index, yield-capacity, conifers, sweden, basal-area]
status: stable
updated: 2026-10-24
description: "Establishes non-linear mixed-effects models relating Site Index (SI) and basal area development to total stem volume yield and potential yield capacity (MAI_max) across Swedish conifer long-term experiments."
source_file: raw/papers/AppiahMensah_et _al.2022_yield capacity.pdf
authors: ["Alex Appiah Mensah", "Emma Holmström", "Kenneth Nyström", "Urban Nilsson"]
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: "raw/papers/AppiahMensah_et _al.2022_yield capacity.pdf"
    title: "Modelling potential yield capacity in conifers using Swedish long-term experiments"
---

# Modelling potential yield capacity in conifers using Swedish long-term experiments

## Summary

This paper presents empirical growth and yield equations for four major conifer groups across Sweden: Norway spruce (*Picea abies*), Scots pine (*Pinus sylvestris*), Lodgepole pine (*Pinus contorta*), and Larch (*Larix decidua* and *Larix sibirica*). Using multi-decadal remeasurements from 330 long-term experimental (LTE) trials across latitudinal and altitudinal gradients, the authors formulate a five-step modeling framework to predict site-level maximum mean annual volume increment ($\text{MAI}_{\max}$, termed yield capacity) directly from Site Index (SI).

A central methodological finding is that relying strictly on Eichhorn’s law (predicting stand volume exclusively from dominant top height) yields systematic site-dependent errors. Incorporating stand basal area ($G$, $\text{m}^2/\text{ha}$) as an allometric covariate with top height ($H$, $\text{m}$) reduces volume estimation RMSE by a factor of 1.5 across all species. Furthermore, exponential regressions relating SI to yield capacity reveal that earlier standard Swedish yield tables (Hägglund & Lundmark, 1982) substantially underestimate yield capacity at high SI classes under modern growing conditions.

## Key claims

1. **Volume prediction requires basal area, not just top height:** Modeling stand volume strictly via Eichhorn's law ($V = f(H)$) ignores density and site carrying capacity variations. Augmenting allometric equations to $V = \alpha_0 H^{\alpha_1} G^{\alpha_2}$ reduced relative RMSE by a factor of 1.5 across all studied species (relative RMSE of 10.96% to 17.72%).
2. **Basal area development follows dynamic difference forms:** Total basal area production ($G_2$, including standing, thinned, and mortality volume) is accurately modeled using algebraic difference formulations parameterized by age, SI, and initial stem density ($N_1 = \sqrt{10000 / N}$). The Pienaar et al. (1990) formulation (F01) was optimal for Scots pine and Norway spruce (relative RMSE: 3.39% and 2.14%), whereas Bertalanffy-Richards (F04) performed best for Lodgepole pine and Larch (relative RMSE: 3.29% and 5.78%).
3. **Yield capacity is an exponential function of Site Index:** The relationship between SI ($H_{100}$ or $H_{50}$) and maximum mean annual increment ($\text{MAI}_{\max}$, $\text{m}^3\,\text{ha}^{-1}\,\text{yr}^{-1}$) was best modeled by $\text{MAI}_{\max} = \alpha_0 \exp(\alpha_1 \cdot \text{SI})$ ($R^2$ of 0.81 to 0.96).
4. **Historical yield curves diverge from modern forest productivity:** Comparison with 1982 Swedish yield tables indicates that modern stands achieve significantly higher yield capacity at upper SI values (and lower at poor site indices), reflecting climate warming, elevated atmospheric $\text{CO}_2$, nitrogen deposition, and updated dynamic difference height curves.

## Implications for our pipeline

While the Conifervision operational pipeline ([[project/pipeline-overview]]) directly computes stem counts, individual tree locations, and crown bounding boxes via photogrammetric CHM rasters ([[concepts/canopy-height-model]]) and deep learning detectors (DEIMv2, Local Maxima), downstream forest metric aggregation requires turning detection counts and top heights into stand-level timber volume and commercial yield:

- **Volume and Yield Attribute Estimation:** In merchantable normal forest stands ([[concepts/normal-forest]]), top height ($H_{100}$) can be directly sampled from the 95th–99th percentile of CHM heights per hectare. When paired with stem density ($N$) derived from ITD detections, stand basal area and standing/cumulative volume yield can be estimated via the paper's species-specific allometric models (Table 4 and Table 5).
- **Species-Specific Parameterization:** After tree crowns are classified using DINOv3 ([[methods/dinov3-classification]] / `methods/dinov3-classification`), plot-level basal area and yield projections must branch into Mensah et al.'s species coefficients ($\alpha_0, \alpha_1, \alpha_2$) for *Picea abies* vs. *Pinus sylvestris*.
- **Validation of Stand Density:** The initial density transformation $N_1 = \sqrt{10000 / N}$ directly connects drone-derived stocking estimates (trees per hectare) to stand carrying capacity trajectories.

## Replication pseudocode

### Prerequisites

- Species classification per detected stem from [[methods/dinov3-classification]]
- Top height $H$ ($\text{m}$) computed as the mean height of the 100 thickest trees/ha (or upper percentile from [[concepts/canopy-height-model]])
- Stand age $A$ (years) and reference Site Index $\text{SI}$ ($H_{100}$ for spruce/pine/larch; $H_{50}$ for lodgepole pine)
- Stand density $N$ ($\text{trees/ha}$) and current stand basal area $G$ ($\text{m}^2/\text{ha}$)

### Procedure

```text
# 1. Compute transformed initial density covariate
N1 = sqrt(10000.0 / N)

# 2. Project Basal Area Development (G2 from G1 over growth interval A1 -> A2)
# Select formulation by species:
if species in ["Scots_pine", "Norway_spruce"]:
    # Formulation F01 (Pienaar et al., 1990)
    # Fixed parameters: alpha0, alpha1, alpha2 from Table 4
    delta_inv_age = (1.0 / A2) - (1.0 / A1)
    ln_G2 = ln(G1) + alpha0 * delta_inv_age + alpha1 * N1 + alpha2 * SI
    G2 = exp(ln_G2)
elif species in ["Lodgepole_pine", "Larch"]:
    # Formulation F04 (Bertalanffy-Richards)
    # Fixed parameters: alpha0, alpha1, alpha2, c0 from Table 4
    num = 1.0 - exp(-alpha0 * A2)
    den = 1.0 - exp(-alpha0 * A1)
    power_term = c0 + alpha1 * N1 + alpha2 * SI
    G2 = G1 * (num / den) ** power_term

# 3. Predict Total Volume Yield (V, m3/ha) using Top Height (H) and Basal Area (G)
# Fixed parameters: alpha0, alpha1, alpha2 from Table 5
V = alpha0 * (H ** alpha1) * (G ** alpha2)

# 4. Predict Stand Yield Capacity (MAI_max, m3/ha/yr) from Site Index (SI)
# Fixed parameters: alpha0, alpha1 from Table 6
MAI_max = alpha0 * exp(alpha1 * SI)
```

### Gaps / not specified in paper

- **Direct Individual Tree Volume Conversion:** The equations operate at the stand aggregate level ($\text{m}^2/\text{ha}$ and $\text{m}^3/\text{ha}$). Converting individual tree crown polygons or bounding boxes to individual stem volumes requires single-tree diameter-height equations (e.g., Brandel, 1990) not modeled directly here.
- **Stand Age Extraction from UAV:** The model relies on known total stand age ($A$), which cannot be determined solely from single-epoch drone orthophotos or CHM rasters without external management records or regional growth inversion.
- **Deciduous Species:** The models only cover coniferous species (*Picea abies*, *Pinus sylvestris*, *Pinus contorta*, *Larix spp.*); broadleaf species (e.g., *Betula pendula*) common in Swedish boreal mixtures are omitted.

## Quotes

- **On Eichhorn’s law limitation (p. 2):**  
  > "The law stipulates that stands have the same total volume yield when they reach the same dominant height, independent of age and SI (Eichhorn, 1902)... Therefore, for a given species and management regime, significant site-dependent variations may occur in the yield levels (total volume production at a given height)..."
- **On incorporating basal area in volume-height models (p. 13–14):**  
  > "Errors in the volume-height relations were significantly reduced by a factor of 1.5 units when including basal area (Fig. 6) and the yield level trajectory was higher for high site index (Fig. 8)... augmenting the volume-top height relationship with basal area guarantees high accuracy in yield level estimation..."
- **On the exponential SI-Yield Capacity relationship (p. 13):**  
  > "The relationship between yield capacity and SI was best fitted by the exponential regression function (Eq. (6.1)) for the studied tree species... The explained variation (adjusted $R^2$) ranged from 80 to 96% and the relative model errors ranged from 6 to 17%..."

## Related pages

- [[project/pipeline-overview]] — Operational pipeline producing stem counts, heights, and species classifications
- [[concepts/canopy-height-model]] — Direct input source for dominant top height ($H$)
- [[concepts/normal-forest]] — Merchantable stands where stand-level yield and volume equations apply
- [[methods/dinov3-classification]] — Species classification required to choose allometric parameter sets
