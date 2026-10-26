---
title: "Robust height-diameter allometries for 41 European tree species: stand characteristics and structure matter"
type: Source
tags: [allometry, height-diameter, dbh, chm, stand-structure, basal-area, mixed-effects]
status: stable
updated: 2026-03-03
description: "Generalized nonlinear mixed-effects H-D allometric models for 41 European species incorporating stand structure, basal area, and quadratic mean diameter, with a 1-to-6 tree local recalibration routine."
source_file: raw/papers/Robust height-diameter allometries for 41 European tree species - stand characteristics and structure matter-2025.09.29.679156v2_full.pdf
authors:
  - Natacha Savine
  - Thomas Cordonnier
  - Gauthier Ligot
  - Patrick Vallet
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-03-30T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Robust height-diameter allometries for 41 European tree species - stand characteristics and structure matter-2025.09.29.679156v2_full.pdf
    title: "Robust height-diameter allometries for 41 European tree species: stand characteristics and structure matter"
---

# Robust height-diameter allometries for 41 European tree species: stand characteristics and structure matter

## Summary

Savine et al. present a generalized, species-specific height-diameter ($H$-$D$) allometric modeling framework covering 41 European tree species across four stand structures: even-aged (EA), uneven-aged (UA), coppice-with-standards (CWS), and coppice (C). Calibrated on French National Forest Inventory (NFI) records spanning 2005–2022 (269,460 trees across 49,120 plots) using a modified Hossfeld II nonlinear mixed-effects formulation, the model incorporates individual tree social status ($dbh / D_g$), stand density via basal area ($BA$), and development stage via quadratic mean diameter ($D_g$). Stand structure significantly shifted allometric parameters for 28 to 30 species. To correct for regional or site fertility bias when applying continental models locally, the authors provide a mean-based local recalibration formula: measuring the height of only 1 to 4 trees (predominantly among the largest diameter class) reduced prediction RMSE by 10% to 70% across external validation plots.

## Key claims

- **Model formulation (Hossfeld II):** The Hossfeld II three-parameter sigmoidal curve yielded superior AIC fits over Chapman–Richards and Weibull equations for broad-scale allometric calibration across 41 species.
- **Stand structure effect:** Stand management structure significantly affects the $H$-$D$ relationship. Applying even-aged models to uneven-aged stands produced RMSE errors up to 26.4% higher (e.g. *Pinus sylvestris*). Conifers in uneven-aged stands showed increased asymptotic height relative to even-aged stands, whereas broadleaves exhibited reduced asymptotic height. Coppice structures consistently showed reduced asymptotic heights.
- **Stand density ($BA$) and stage ($D_g$):** As stand basal area ($BA$) increases, asymptotic height increases and diameter at half asymptotic height ($dha$) decreases (trees are taller for a given DBH due to light competition). Higher quadratic mean diameter ($D_g$) monotonically increases stand asymptotic height via a saturating negative exponential function.
- **Local recalibration with minimal sampling:** Using a simple analytic mean-based correction for the plot random site parameter $\lambda_i$, field-measuring 3 to 4 trees per plot (predominantly the largest diameter individuals, plus one small tree) reduced validation RMSE by 10% to 75% on independent historical permanent plots.

## Implications for our pipeline

- **Inverting allometry for DBH estimation from drone CHM:** In [[project/pipeline-overview]] and [[concepts/canopy-height-model]], the pipeline reliably extracts individual tree heights ($H$) and crown bounding boxes, but DBH cannot be measured directly from nadir drone orthophotos. Inverting Equation 4 allows estimating individual tree DBH from CHM-derived height $H$, provided the stand structure, local basal area $BA$, and species identity (derived from [[methods/dinov3-classification]]) are known or approximated.
- **Stand development stage ($D_g$) and competition ($BA$):** Because drone CHM and detection modules provide stand-level canopy height and stem count, approximate $D_g$ and $BA$ can be iteratively estimated across detected crowns in [[project/research-normal-forest]].
- **Crown ownership & height floor thresholds:** In [[concepts/crown-ownership]] and [[concepts/site-index-and-yield]], understanding that suppressed/understory trees have altered height-diameter curves helps calibrate expected height tiers when filtering double-detections or predicting stand merchantable timber volume.
- **Plot-level ground truth calibration:** If ground plots are visited during drone calibration surveys, measuring tree height for just 3–4 large trees allows calculating the site parameter $\lambda_i$, substantially improving DBH/volume modeling accuracy over uncalibrated regional models.

## Replication pseudocode

### Prerequisites

- Species classification per detected stem (from [[methods/dinov3-classification]]).
- Stand structure category: Even-Aged (EA), Uneven-Aged (UA), Coppice-with-Standards (CWS), or Coppice (C).
- Stand basal area $BA$ ($m^2/ha$) and dominant species quadratic mean diameter $D_g$ ($cm$).
- Fitted parameter table per species: $a_{s1}, a_{s,UA}, a_{s,CWS}, a_{s,C}, a_{s2}, a_{s3}, a_{s4}, b_{s1}, b_{s,UA}, b_{s,CWS}, b_{s,C}, b_{s2}, c_s$.

### Procedure

```text
# Input: Tree diameter dbh_i (or drone CHM height htot_i), species s, stand structure S, stand BA, stand Dg
# Optional input: Sample of measured heights for local recalibration { (dbh_k, h_obs_k) } for k in 1..N

1. Evaluate dummy indicators for stand structure S:
     I_UA  = 1 if S == "UA"  else 0
     I_CWS = 1 if S == "CWS" else 0
     I_C   = 1 if S == "C"   else 0

2. Compute base asymptotic height parameter a_s:
     struct_a = 1.0 + (a_s_UA * I_UA) + (a_s_CWS * I_CWS) + (a_s_C * I_C)
     ba_a     = 1.0 + (a_s2 * BA)
     dg_a     = 1.0 - exp(-a_s3 * (Dg ** a_s4))
     a_s = a_s1 * struct_a * ba_a * dg_a

3. Compute diameter at half asymptotic height parameter b_s:
     struct_b = 1.0 + (b_s_UA * I_UA) + (b_s_CWS * I_CWS) + (b_s_C * I_C)
     ba_b     = exp(-b_s2 * BA)
     b_s = b_s1 * struct_b * ba_b

4. Determine random site parameter lambda_i:
     if local_calibration_sample is provided (e.g., 3 largest trees + 1 small tree):
         lambda_accum = 0.0
         for (dbh_k, h_obs_k) in local_calibration_sample:
             x_k = dbh_k / Dg
             h0_k = 1.3 + (a_s / (1.0 + b_s / (x_k ** c_s)))
             lambda_accum += (h_obs_k - 1.3) / (h0_k - 1.3)
         lambda_i = (lambda_accum / N) - 1.0
     else:
         lambda_i = 0.0  # Fixed effects only

5. Predict Total Height htot given dbh:
     x = dbh / Dg
     htot = 1.3 + (1.0 + lambda_i) * (a_s / (1.0 + b_s / (x ** c_s)))

6. Inverse operation (Predict DBH from drone CHM height htot):
     ratio = ((1.0 + lambda_i) * a_s) / (htot - 1.3)
     if ratio <= 1.0:
         return TBD  # Height exceeds theoretical stand asymptote
     x_pred = (b_s / (ratio - 1.0)) ** (1.0 / c_s)
     dbh_est = x_pred * Dg
     return dbh_est
```

### Gaps / not specified in paper

- Parameter convergence failed for 10 out of the 51 initial species; parameters for those 10 species are not available.
- Full parameter tables for all 41 species reside in Supplementary Materials (Table S5), while the main text lists only the top 10 species.
- Inverting the equation to predict DBH from CHM height is mathematically direct, but numerical stability bounds when drone-measured CHM height approaches or exceeds $(1 + \lambda_i) a_s + 1.3$ are not discussed.

## Quotes

- *Model functional form:* "By comparing the Akaike Information Criterion (AIC)(Akaike, 1974), we selected the Hossfeld II function (Eq.1), which gave the best adjustments. $y = 1.3 + a_s * \frac{1}{1 + \frac{b_s}{x^{c_s}}}$" (p. 6, lines 246–250)
- *Full calibrated formula:* "$htot = 1,3 + (1 + \lambda_i) * a_{s1} * (1 + a_{s,UA} + a_{s,CWS} + a_{s,C}) * (1 + a_{s2} * BA) * (1 - exp(-a_{s3} * Dg^{a_{s4}})) * \frac{1}{1 + \frac{b_{s1}*(1+b_{s,UA}+b_{s,CWS}+b_{s,C})*(exp(-b_{s2}*BA))}{(dbh/Dg)^{c_s}}}$" (p. 7, lines 299–301)
- *Local recalibration benefit:* "When the site parameter was estimated from a sub-sample of three to four trees (2 large with 1small and 3large with 1 small), substantial improvements in RMSE generally resulted, compared to using fixed effects only. The RRI ranges from 10 to 70%..." (p. 10, lines 409–412)

## Related pages

- [[project/pipeline-overview]] — Current production pipeline linking CHM height to inventory outputs
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM height layers
- [[concepts/site-index-and-yield]] — Stand development, dominant height, and volume yield modeling
- [[concepts/direct-stem-dbh-point-cloud]] — Direct 3D point cloud stem fitting vs. empirical allometry
- [[project/research-normal-forest]] — Tree delineation and attribute estimation in managed stands
