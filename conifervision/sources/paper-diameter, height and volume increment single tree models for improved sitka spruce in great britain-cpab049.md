---
title: "Diameter, height and volume increment single tree models for improved Sitka spruce in Great Britain"
type: Source
tags: [allometry, growth-models, sitka-spruce, taper-models, volume-estimation, forestry-yield]
status: stable
updated: 2026-10-24
description: "Climate-sensitive single-tree diameter and height difference equations coupled with stem taper integration for volume forecasting in improved Sitka spruce."
source_file: raw/papers/Diameter, height and volume increment single tree models for improved Sitka spruce in Great Britain-cpab049.pdf
authors:
  - Rubén Manso
  - Rachael Davidson
  - J. Paul McLean
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T00:00:00Z
sources:
  - id: primary
    resource: raw/papers/Diameter, height and volume increment single tree models for improved Sitka spruce in Great Britain-cpab049.pdf
    title: "Diameter, height and volume increment single tree models for improved Sitka spruce in Great Britain"
---

# Diameter, height and volume increment single tree models for improved Sitka spruce in Great Britain

## Summary

This paper presents a single-tree dynamic growth framework tailored to genetically improved Sitka spruce (*Picea sitchensis*) plantations in Great Britain. Using retrospective dendrochronological data (annual ring widths from CT scans and inter-whorl height measurements) from over 1,400 felled trees across two genetic trial sites (Kintyre, Scotland and Brecon, Wales), the authors fit nonlinear difference growth equations for annual diameter at breast height increment ($\Delta\text{DBH}$) and annual height increment ($\Delta H$).

The models parameterize growth as an expansion component (a power function of tree size) tempered by a decline component driven by tree age, stand competition (proxied by quadratic mean diameter $d_g$), and climate covariates (minimum 1-month SPEI drought index, minimum spring temperature, and annual mean temperature). Continuous-time autoregressive correlation (CAR) and family-level random effects account for longitudinal and genetic autocorrelation. Tree-level DBH and height projections are then propagated through Monte Carlo simulations and fed into a static stem taper equation (Fonweban et al., 2011), numerically integrated to predict merchantable stem volume at harvest.

## Key claims

1. **Failure of legacy yield models:** Standard Forestry Commission static yield tables underestimate the growth rate and volume yield of modern genetically improved Sitka spruce stands.
2. **Functional difference forms:** Tree increment is well characterized by Zeide (1993) difference equations:
   - $\Delta\text{DBH}$ follows a power function of age: $\Delta y = \alpha y^\beta t^\gamma$.
   - $\Delta H$ follows an exponential function of age: $\Delta y = \alpha y^\beta e^{\gamma t}$.
3. **Competition via quadratic mean diameter:** Competition effects in randomly sampled stems can be captured by stand quadratic mean diameter ($d_g$), which reflects canopy closure and onset of self-thinning when $d_g \approx 12\text{--}13\text{ cm}$ (around age 12–13).
4. **Climatic sensitivity:** Higher minimum SPEI (lower drought) and warmer minimum spring temperatures (reduced late frost damage) significantly mitigate growth decline across sites. Mean annual temperature exhibits site-dependent effects (negative at Kintyre, positive at high-elevation Brecon).
5. **Genetic family variance absorption:** Family-level random effects accounted for only a modest share of residual variance; tree initial size (DBH or height) captured the majority of genetic superiority, simplifying application across half-sibling and full-sibling stock.
6. **Unbiased stochastic volume projection:** Iterative multi-year simulation coupled with Fonweban's taper model produced merchantable volume estimates at age 22 with low absolute bias ($+0.0111\text{ m}^3$ in Kintyre, $+0.0088\text{ m}^3$ in Brecon) and valid confidence interval coverage.

## Implications for our pipeline

- **Linking UAV metrics to allometry:** [[project/pipeline-overview]] detects individual tree crowns and extracts top heights from [[concepts/canopy-height-model]]. Coupling individual tree heights from photogrammetry/LiDAR with site-level height-diameter models (e.g., Arcangeli et al., 2014) enables initializing single-tree dynamic simulators for conifer stands without intensive ground DBH inventories.
- **Yield & volume projection:** Connects directly with [[concepts/site-index-and-yield]] and [[concepts/tree-allometry]]. Instead of static lookup tables, stem volume can be calculated directly by integrating taper profiles driven by detected height and predicted DBH.
- **Stand competition context:** Stand density and quadratic mean diameter ($d_g$) estimated across segmented crowns in [[concepts/normal-forest]] provide the necessary competition metrics to evaluate growth stagnation or thinning schedules.

## Replication pseudocode

### Prerequisites

- Initial tree state at starting age $t_0$: stem height $H_0$ (e.g., extracted from UAV CHM) and diameter $\text{DBH}_0$ (measured or derived via height-diameter allometry).
- Stand quadratic mean diameter $d_{g,0}$.
- Annual climate metrics: annual minimum 1-month SPEI ($\text{min.spei.1}$), spring minimum temperature ($\text{min.temp.sp}$), and mean annual temperature ($\text{mean.temp.yr}$).
- Calibrated model parameters from Table 3 ($\Delta\text{DBH}$) and Table 4 ($\Delta H$), plus Fonweban et al. (2011) taper parameters.

### Procedure

```text
# High-level annual stepping and taper integration
1. Set initial stand and tree metrics at t = t_start:
   For each tree i in stand:
       DBH[i, t_start] = DBH_0[i]
       H[i, t_start]   = H_0[i]
   Calculate stand dg[t_start] = sqrt(mean(DBH[:, t_start]^2))

2. For year t in t_start to t_end - 1:
   a. Retrieve annual climate covariates: min_spei, min_temp_sp, mean_temp_yr
   b. For each tree i:
        # Sample error terms from covariance matrices (residual + random effects)
        eps_d = sample_normal(0, sigma_eps_d)
        eps_h = sample_normal(0, sigma_eps_h)
        
        # Calculate increments via Equations 3/4 and 5/6
        delta_DBH = calc_dbh_increment(DBH[i, t], t, dg[t], min_spei, min_temp_sp, mean_temp_yr) + eps_d
        delta_H   = calc_height_increment(H[i, t], t, min_spei, min_temp_sp) + eps_h
        
        # Update size for next period
        DBH[i, t + 1] = DBH[i, t] + max(0.0, delta_DBH)
        H[i, t + 1]   = H[i, t] + max(0.0, delta_H)
        
   c. Recalculate stand competition proxy:
        dg[t + 1] = sqrt(mean(DBH[:, t + 1]^2))

3. At target rotation age t_end:
   For each tree i:
        # Generate diameter taper profile d(h) at 1 m height intervals along stem
        taper_profile = evaluate_fonweban_taper(DBH[i, t_end], H[i, t_end])
        
        # Numerically integrate stem profile (sum of truncated cone segments)
        Volume[i] = integrate_stem_profile(taper_profile, stump_height=0.15, top_diameter=0.07)
```

### Gaps / not specified in paper

- **Mortality module:** The study lacked mortality data (all sampled stems were harvested survivors), meaning self-thinning mortality must be supplied by an external function when simulating unthinned stands past canopy closure.
- **Early-age height increments:** Ring-width and height-whorl scars before trees reached breast height ($1.3\text{ m}$) were indistinct and excluded; simulations require initialization at $t \ge 10$ years ($H > 1.3\text{ m}$).
- **Taper validity at early ages:** Fonweban's taper equations were verified at age 22; their mathematical behavior on juvenile trees ($t < 15$) was not validated.
- **Geographic recalibration:** Site models required site-specific parameters between Kintyre and Brecon; general application across the UK requires regional recalibration ($TBD$).

## Quotes

- **On legacy yield models:** *"These gains have been so substantial that there is concern that the old yield models developed by the Forestry Commission (Edwards and Christie, 1981, Matthews et al., 2016) might not accurately model improved stands."* (p. 391)
- **On competition and canopy closure:** *"The specific functional form for the competition term is such that the growth decline component of the model becomes less than one... when some dg is reached given a set of climatic conditions. If we take the example of Kintyre and use the mean value of each of the climatic variables involved, it is possible to see that growth decrease would roughly take place when dg ~12-13 cm. This corresponds to an age of 12 or 13 years. Our data clearly shows that canopy closure must have occurred at age 11–12 at that site..."* (p. 402)
- **On drone/remote sensing height initialization:** *"Airborne LiDAR is a precise and more affordable alternative, at least when scanning relatively large areas. Although the identification of individual trees in point clouds is still imperfect... reliable methods to estimate stand mean height without individual delineation have been available for some time... This stand mean height estimate could be used to calibrate height-diameter models... to obtain an estimate of the individual initial heights from measured DBHs."* (pp. 402–403)

## Related pages

- [[concepts/site-index-and-yield]] — Stand-level dominant height, site index tables, and dynamic yield simulation.
- [[concepts/tree-allometry]] — Individual-tree allometric relationships linking height, crown diameter, DBH, and stem volume.
- [[concepts/canopy-height-model]] — Photogrammetric/LiDAR elevation models providing individual tree top heights.
- [[concepts/normal-forest]] — Structural definitions of commercial stands where individual crown delineation and allometric volume estimation apply.
- [[project/pipeline-overview]] — Operational tree detection, canopy extraction, and downstream attribution.
