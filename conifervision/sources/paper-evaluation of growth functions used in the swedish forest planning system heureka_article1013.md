---
title: "Evaluation of growth models used in the Swedish Forest Planning System Heureka"
type: Source
tags: [forestry, growth-models, heureka, basal-area, volume, sweden, national-forest-inventory]
status: stable
updated: 2026-06-09
description: "Evaluation of stand-level and single-tree empirical basal area and volume growth models in the Swedish Heureka system against NFI and long-term thinning trials."
source_file: raw/papers/Evaluation of growth functions used in the Swedish Forest Planning System Heureka_article1013.pdf
authors:
  - "Nils Fahlvik"
  - "Björn Elfving"
  - "Peder Wikström"
year: 2014
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-06-09T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Evaluation of growth functions used in the Swedish Forest Planning System Heureka_article1013.pdf
    title: "Evaluation of growth models used in the Swedish Forest Planning System Heureka"
---

# Evaluation of growth models used in the Swedish Forest Planning System Heureka

## Summary

Fahlvik, Elfving, and Wikström (2014) evaluate empirical growth models used in Sweden's forestry decision support system, Heureka. The study assesses stand-level models (Ekö 1985 `OLD_S`, Elfving 2010a `NEW_S`) and individual-tree models (Söderberg 1986 `OLD_T`, Elfving 2010a `NEW_T`) using two primary datasets: 1,711 5-year permanent plots from the Swedish National Forest Inventory (NFI) measured between 1999 and 2007, and 57 long-term thinning trial blocks (GG-trials) monitored over 30 years for Scots pine (*Pinus sylvestris*) and Norway spruce (*Picea abies*).

A critical finding is that a single stand-level basal area growth model (`NEW_S`, with only 19 parameters) achieved higher overall precision ($R^2 = 0.75$, residual standard deviation $0.76\text{ m}^2/\text{ha}$) than complex, species-stratified tree-level models (`NEW_T` / `OLD_T` with 400–600 parameters). Heureka’s hybrid design uses the stand-level model to constrain total basal area increment while using tree-level functions to disaggregate growth across diameter distributions. Furthermore, relative prediction error averaged approximately 15% across stands and did not compound or inflate with longer recursive projection periods (up to 30–40 years).

## Key claims

- **Stand-level superior to tree-level for aggregate growth:** A single stand-level model across all Swedish forest types exhibited lower residual variance ($p < 0.001$) than detailed individual-tree models, refuting the hypothesis that tree-level aggregation improves total stand increment precision (p. 10, 14).
- **Stability across historic calibration periods:** Models calibrated on 1970s and 1980s data reliably predicted growth in the 2000s, overestimating basal area increment by only ~2–3% in NFI validation plots despite general national productivity increases (p. 9, 13).
- **No recursive error compounding:** Long-term recursive simulations (5-year steps up to 30–40 years) maintained stable relative standard deviations; error was largest in the initial 7-year step and did not diverge over time (p. 11, 14).
- **Volume growth accuracy:** In the 30-year thinning trials, Heureka predicted Scots pine volume growth within 0.5% and underestimated Norway spruce volume growth by 2% (p. 1, 11).
- **Density-dependent bias:** All models exhibited systematic bias at extremes of stocking: basal area growth was underestimated in high basal area NFI plots and overestimated in unthinned control plots (treatment I), pointing to unresolved handling of site carrying capacity (p. 1, 10, 14).

## Implications for our pipeline

- **Stand-level constraints on individual crown metrics:** While Conifervision operates on drone orthophotos and [[concepts/canopy-height-model|CHMs]] using tree detection ([[methods/local-maxima]], [[methods/deimv2-canopy]]) and crown segmentation, aggregating individual crown predictions to stand-level volume/yield can introduce cumulative variance. Adopting Heureka's hybrid principle—calibrating aggregated individual-tree predictions against stand-level structural baselines—can suppress systematic accumulation errors in long-term inventory projections (see [[sources/paper-appiahmensah_et _al-2022_yield capacity]]).
- **Growth modeling beyond static detection:** In [[project/pipeline-overview]], our operational chain ends at detected hypotheses and [[methods/dinov3-classification|species attribution]]. Linking detected trees to yield forecasts requires empirical diameter and height growth functions. The finding that unthinned or dense stands suffer from overestimation highlights the need for precise local competition metrics (e.g., basal area of larger trees, local crown competition) derivable from 3D point clouds.
- **Biomass and volume disaggregation:** When individual crown areas or heights are estimated from photogrammetry/LiDAR, Brandel (1990) volume equations and Näslund/Pettersson height curves represent standard Swedish forestry references compatible with NFI and Heureka workflows.

## Replication pseudocode

### Prerequisites

- Tree list per stand/plot containing species, initial DBH ($d \ge 4\text{ cm}$), and height $h$ (or diameter-height curve).
- Stand and site covariates: latitude, altitude, site index ($H_{100}$ from Hägglund & Lundmark 1977), stand age, time since thinning.
- Stand-level growth function (`NEW_S`, Elfving 2010a) and tree-level growth functions (`NEW_T`, Elfving 2010a).
- Individual volume functions (Brandel 1990).

### Procedure

```text
# Heureka Hybrid Stand/Tree Simulation Loop (5-year recursive steps)
input: stand_plot_data (trees, site_index, latitude, altitude, age)
output: simulated_stand_trajectory (5-year steps of BA, Volume, DBH distribution)

1. Initialize stand state:
   - For each tree i:
       if height missing: estimate h_i using Näslund (pine) or Pettersson (spruce) height curve
       estimate breast height age using Elfving (2003) age models
   - Compute initial stand basal area (BA_0) and stem density (N_0)

2. For each 5-year projection cycle t = 1 to T_steps:
   a. Compute Stand-Level Basal Area Increment (NEW_S):
        dBA_stand = predict_stand_increment(BA_t, age_t, site_index, latitude, altitude, time_since_thinning)

   b. Compute Individual-Tree Basal Area Increments (NEW_T):
        For each tree i:
            compute competition metric BAL_i (basal area of trees larger than tree i)
            dBA_tree_raw[i] = predict_tree_increment(species_i, DBH_i, BAL_i, site_index, age_t, density)

   c. Harmonize / Scale Tree Increments to Stand Total (Disaggregation):
        scale_factor = dBA_stand / sum(dBA_tree_raw)
        For each tree i:
            dBA_tree_final[i] = dBA_tree_raw[i] * scale_factor
            DBH_new[i] = sqrt(DBH_i^2 + (4 / pi) * dBA_tree_final[i])

   d. Update Heights and Competition:
        For each tree i:
            dH_top = predict_top_height_growth(H_initial, age_initial, age_new)
            dH_tree[i] = adjust_height_increment(dH_top, BAL_i)
            h_new[i] = h_i + dH_tree[i]

   e. Compute Volumes:
        For each tree i:
            v_i = Brandel_volume(species_i, DBH_new[i], h_new[i])
        Total_Volume = sum(v_i)

   f. Handle Planned Interventions / Mortality:
        Apply thinning removals or natural mortality models (Elfving 2010b)
        Update age_t = age_t + 5
        Update stand BA_t and tree list
```

### Gaps / not specified in paper

- Complete mathematical formulas and parameter coefficients for `NEW_S` and `NEW_T` are omitted; readers are directed to the internal SLU report (Elfving 2010a).
- Specific algorithmic scaling/disaggregation formula used to enforce `NEW_S` stand-level sum onto `NEW_T` tree-level predictions is not explicitly detailed in the text (proportional scaling assumed).
- Precise handling of ingrowth (trees crossing the 4 cm DBH threshold during the 30-year simulation) is mentioned in general Heureka terms but specific rules applied in the simulation runs are TBD.

## Quotes

- **On stand vs. single-tree precision:** "An important result of this study is that detailed single tree growth models had lower precision for estimation of total growth than one single stand-based model for all stand types in Sweden. This falsifies our hypothesis 2. It is in line with the so called Occam’s Razor: an efficient model should not be more complicated than necessary to explain the observed variation in a data set." (p. 14)
- **On error propagation over projection length:** "The pure prediction error, due to unexplained variation in growth between blocks (stands) was in average estimated at around 15%. It did not increase with the length of the prediction period. Hypothesis 3 was thus not supported." (p. 14)
- **On dense stand underestimation:** "All of the growth models tended to underestimate the basal area growth for plots with large initial basal areas... It is likely that the underestimation is related to the variation in carrying capacity between sites." (p. 14)
- **On Heureka's combined architecture:** "The Heureka system was designed with this concept, using tree-level growth models to model yield distributions and one single stand-level model for calibrating overall stand growth." (p. 2)

## Related pages

- [[project/pipeline-overview]] — Operational AREA processing flow (detection, fusion, classification)
- [[concepts/canopy-height-model]] — Photogrammetric/LiDAR height models providing top height baselines
- [[sources/paper-appiahmensah_et _al-2022_yield capacity]] — Yield capacity and stand volume models connecting CHM top height and basal area in Sweden
- [[sources/paper-appiahmensah_et_al_2023_site_index_sis_rs]] — Swedish site index estimation using bitemporal height models and terrain predictors
