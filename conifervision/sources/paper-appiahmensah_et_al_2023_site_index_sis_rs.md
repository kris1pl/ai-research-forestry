---
title: "Mapping site index in coniferous forests using bi-temporal airborne laser scanning data and field data from the Swedish national forest inventory"
type: Source
tags: [site-index, als, bi-temporal, height-increment, sweden, conifer, norway-spruce, scots-pine]
status: stable
updated: 2026-10-21
description: "Predicts site index according to site properties (SIS) for Scots pine and Norway spruce across Sweden using bi-temporal ALS height percentiles, annual height increment, and terrain auxiliaries via multiple linear regression."
source_file: raw/papers/AppiahMensah_et_al_2023_Site_Index_SIS_RS.pdf
authors:
  - Alex Appiah Mensah
  - Jonas Jonzén
  - Kenneth Nyström
  - Jörgen Wallerman
  - Mats Nilsson
year: 2023
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T18:00:00Z
sources:
  - id: primary
    resource: raw/papers/AppiahMensah_et_al_2023_Site_Index_SIS_RS.pdf
    title: "Mapping site index in coniferous forests using bi-temporal airborne laser scanning data and field data from the Swedish national forest inventory"
related_methods:
  - methods/chm-detection
---

# Mapping site index in coniferous forests using bi-temporal airborne laser scanning data and field data from the Swedish national forest inventory

## Summary

This study by Appiah Mensah et al. (2023) develops an area-based methodology to map forest site productivity across Sweden at a 12.5 m grid resolution. Focusing on even-aged stands of Norway spruce (*Picea abies*) and Scots pine (*Pinus sylvestris*), the authors predict site index based on site properties (SIS, representing expected dominant height at age 100) by combining bi-temporal airborne laser scanning (ALS) data with auxiliary geographic and environmental rasters.

Using over 11,500 field plots from the Swedish National Forest Inventory (NFI) — calibrated on permanent plots and validated against both temporary NFI plots and an independent 311-stand operational dataset from Sveaskog — the study compared ordinary least squares Multiple Linear Regression (MLR) against Random Forests (RF). MLR exhibited superior stability and generalization (relative efficiency close to 1.0, vs. >2.2 for RF which severely overfitted). The final MLR models achieved RMSEs of 1.96 m (relative RMSE 9.2%) for Scots pine and 2.07 m (relative RMSE 7.7%) for Norway spruce, leveraging canopy height percentiles ($H_{p90}$), annual top-height increment ($\Delta H_{p95}$), latitude, altitude, distance to coast, and soil moisture.

## Key claims

- **Parametric MLR generalizes better than Random Forests across regional scales**: RF models suffered severe overfitting, with relative efficiency ($RE = \mathrm{RMSE}_{\text{val}} / \mathrm{RMSE}_{\text{cal}}$) of 2.58 for pine and 2.29 for spruce, compared to 1.03 and 1.02 for MLR (p. 6–8, Table 2).
- **Annual height increment ($\Delta H_{p95}$) captures site-level volume productivity**: Normalizing the change in the 95th percentile height by the exact number of intervening growing seasons accounted for latitudinal growth variations and eliminated residual bias across stem volume gradients (p. 4, 8).
- **Average canopy height ($H_{p90}$) handles stand density dependence**: The inclusion of $H_{p90}$ at time 2 eliminated residual bias across stand basal area ranges (p. 8, Fig. A5).
- **Non-linear response to soil wetness**: Forest site productivity responds to mobile water flow according to a quadratic function of soil moisture ($\text{Soilwet} + \text{Soilwet}^2$) (p. 5, 8).
- **High operational accuracy at 12.5 m pixel scale**: Independent stand-level validation on Sveaskog commercial forest stands produced an RMSE of 1.80 m (9.98% relative) for pine and 1.56 m (6.20% relative) for spruce (p. 9, Table 5).

## Implications for our pipeline

- **Stand-level growth priors for detection priors**: Site index (SIS) mapped at 12.5 m resolution offers a direct prior for expected annual height increment and crown crown expansion rates in [[concepts/normal-forest]] stands, supporting crown growth tracking between multi-temporal drone flights.
- **CHM calibration and normalization**: The demonstrated stability of height metrics ($H_{p90}$, $H_{p95}$) on terrain-normalized [[concepts/canopy-height-model|CHM]] rasters validates using high-percentile height filters when setting minimum height thresholds (e.g., separating understory vegetation from R-class conifer crowns in [[project/pipeline-overview]]).
- **Growth rate tracking across repeated drone surveys**: Incorporating growing-season-normalized top-height differences ($\Delta H_{p95}$) can be integrated into temporal repeat surveys to verify thinning interventions or stand vigor alongside [[sources/paper-appiahmensah_et _al-2022_yield capacity]].

## Replication pseudocode

### Prerequisites

- Bi-temporal ALS or photogrammetric point clouds normalized to ground DEM (e.g., via CSF ground filter).
- Geospatial site layers resampled to 12.5 m grid: DEM altitude, latitude coordinates, distance to sea vector layer, and rasterized soil wetness index (0–100%).
- Regional meteorological data defining start and end dates of growing seasons (air temperature threshold > +5 °C) to compute exact fractional growing seasons between scans.
- Pre-stratified species dominance masks (e.g., from [[methods/dinov3-classification]] or regional forest registers).

### Procedure

```text
# Area-based site index (SIS) prediction workflow

1. Derive area-based canopy height percentiles (12.5 m cell):
   - Filter point cloud returns to [1.5 m, 50.0 m] above ground.
   - For scan t1 and scan t2, compute height distribution percentiles:
       Hp90_t2 = 90th percentile height at time 2
       Hp95_t1 = 95th percentile height at time 1
       Hp95_t2 = 95th percentile height at time 2

2. Compute annual height increment:
   - Determine fractional growing seasons (num_growing_seasons) between t1 and t2 using local degree-day records (> 5 °C).
   - delta_Hp95 = (Hp95_t2 - Hp95_t1) / num_growing_seasons

3. Extract ancillary site variables per pixel:
   - Lat: coordinate latitude (in projective CRS units / m)
   - Alt: elevation from DEM (m a.s.l.)
   - Distcoast: Euclidean distance to nearest coastline (km or m per model unit)
   - Soilwet: mapped soil wetness probability index (0 - 100 %)

4. Evaluate species-specific MLR equation:
   For Scots pine:
       SIS = 45.87
             - 3.877e-6 * Lat
             - 0.0042 * Alt
             - 0.0012 * Distcoast
             + 0.0079 * (Hp90_t2)^2     # Note: Eq. 9 uses squared terms for height metrics
             + 11.66 * (delta_Hp95)^2
             + 0.0649 * Soilwet
             - 0.0010 * (Soilwet)^2

   For Norway spruce:
       SIS = 115.4
             - 1.326e-5 * Lat
             - 0.0105 * Alt
             + 9.319e-4 * Distcoast    # non-significant in paper (p = 0.119), but in full model
             + 0.0036 * (Hp90_t2)^2
             + 4.9340 * (delta_Hp95)^2
             + 0.0096 * Soilwet
             - 3.678e-4 * (Soilwet)^2

5. Compute pixel prediction standard error (Saarela et al., 2020):
   - Var_pred = X_i * Cov_beta * X_i^T + Var_residual
   - RMSE_SIS = sqrt(Var_pred)
   - Rel_RMSE = (RMSE_SIS / SIS) * 100
```

### Gaps / not specified in paper

- **Exact coordinate scale for Lat**: Table 3 lists parameter $\hat{\beta}_1$ with tiny coefficients (e.g. $-3.877 \times 10^{-6}$), indicating metric coordinates (e.g. SWEREF99 TM Northing in meters) rather than decimal degrees, though the text states "latitude".
- **Height term exponent discrepancy**: Eq. (1.4) defines $\omega_1 \cdot (Hp90.t2) + \omega_2 \cdot (\Delta Hp95)$, but Eq. (9) and text on p. 8 write $\omega_1 \cdot (Hp90.t2)^2 + \omega_2 \cdot (\Delta Hp95)^2$ without documenting the transformation decision in the methods text.
- **Handling clear-cuts and heavy thinning**: Outliers with $\pm 5$ m deviation between $Hp95$ and field height were discarded (p. 5), but wall-to-wall application across recently thinned or harvested patches without a mask would yield invalid negative growth increments ($\Delta Hp95$).

## Quotes

- *"For both species, the MLR model gave precise and accurate estimates of SIS. The RMSE for SIS predictions was in the range of 1.96 – 2.11 m, and the relative RMSE was less than 10 % (7.68 – 9.49 %) of the reference mean value."* (p. 1, Abstract)
- *"Owing to the biological limitations of the site index (Antón-Fernández et al., 2016), a logical parametric model would probably do better than a non-parametric machine learning model when applied outside the range of the training data..."* (p. 2)
- *"Lower values (RE less than and close to 1) of the ratio of the residual variability around model validation (i.e., on temporary plots) to residual variability around model calibration (i.e., on permanent plots) reflect better and a more stable predictive model and otherwise for an over-fitted model (i.e. RE values greater than 1)."* (p. 6)
- *"Diagnostics of the MLR models showed that the variance of residuals was fairly constant over the predicted site index, but slight trends in the residuals were observed when validated against soil moisture and textural class from the Swedish NFI..."* (p. 8–9)

## Related pages

- [[sources/paper-appiahmensah_et _al-2022_yield capacity]] — Companion paper on yield capacity and stand volume models driven by top height and site index.
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM normalization and height metrics.
- [[project/pipeline-overview]] — Current AREA production flow utilizing multi-layer CHM processing.
- [[concepts/normal-forest]] — Stand-level structure context for mature conifer canopies.
