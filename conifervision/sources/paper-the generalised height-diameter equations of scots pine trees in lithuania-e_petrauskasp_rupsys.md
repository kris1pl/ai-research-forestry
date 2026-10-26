---
title: "The Generalised Height-Diameter Equations of Scots Pine (Pinus sylvestris L.) Trees in Lithuania"
type: Source
tags: [allometry, height-diameter, scots-pine, lithuania, national-forest-inventory, q-exponential]
status: stable
updated: 2026-10-24
description: "Empirical evaluation of four non-linear generalized height-diameter models for Scots pine across 3,456 Lithuanian NFI plots, highlighting q-exponential parameter expansions."
source_file: raw/papers/The Generalised Height-Diameter Equations of Scots Pine Trees in Lithuania-E_PetrauskasP_Rupsys.pdf
authors:
  - Edmundas Petrauskas
  - Petras Rupšys
year: 2013
replication_status: full
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/The Generalised Height-Diameter Equations of Scots Pine Trees in Lithuania-E_PetrauskasP_Rupsys.pdf
    title: "The Generalised Height-Diameter Equations of Scots Pine (Pinus sylvestris L.) Trees in Lithuania"
---

# The Generalised Height-Diameter Equations of Scots Pine (Pinus sylvestris L.) Trees in Lithuania

## Summary

This conference paper evaluates generalized height-diameter ($h$–$d$) models for Scots pine (*Pinus sylvestris* L.) in Lithuania using data from the Lithuanian National Forest Inventory (NFI) collected between 2006 and 2010. The dataset spans 3,456 Scots pine plots split into an estimation set (2,000 plots; 7,352 trees) and an independent validation set (1,456 plots; 5,413 trees). The authors compare four base non-linear growth equations: the 3-parameter Korf model, the 3-parameter Chapman-Richards model, the 3-parameter modified logistic model, and a newly developed 4-parameter $q$-exponential model. 

To create generalized models, the asymptote parameter $\beta_0$ is expressed as a power function of stand-level covariates: stand age ($A$), quadratic mean diameter ($d_0$), mean height weighted by basal area ($h_0$), and the joint combination of $d_0$ and $h_0$. The results show that diameter alone explains roughly 46–47% of height variance, whereas incorporating stand mean height and mean diameter increases the explained variance ($R^2_{\text{adj}}$) to over 90% and reduces mean absolute error to ~1.06 m. Across all comparisons, the $q$-exponential function incorporating both $d_0$ and $h_0$ achieved the best goodness-of-fit and validation metrics.

## Key claims

- **Model fit improvement via stand covariates:** Fitting height strictly as a function of diameter at breast height ($d$) results in $R^2_{\text{adj}} \approx 0.46$–$0.47$ (validation absolute bias $AB \approx 2.48$–$2.50\text{ m}$). Expanding the asymptote parameter with stand mean height $h_0$ and quadratic mean diameter $d_0$ boosts $R^2_{\text{adj}}$ to $0.90$ and lowers validation $AB$ to $1.06\text{ m}$ (Table 3).
- **Superiority of the $q$-exponential formulation:** Among the four tested formulations (Korf, Chapman-Richards, modified logistic, $q$-exponential), the $q$-exponential base model combined with stand variables $d_0$ and $h_0$ achieved the lowest AIC (70,191.1 estimation, 50,119.8 validation) and lowest percentage of absolute bias (PAB: 5.04% estimation, 5.09% validation).
- **Biological boundary constraint ($d=0, h=1.3\text{ m}$):** Direct modification of the candidate functions (Chapman-Richards and $q$-exponential) by adding an explicit $1.3\text{ m}$ constant ensures that estimated heights approach breast height ($1.30\text{ m}$) rather than 0 or negative values as diameter approaches zero.
- **Stand height dominance over stand age:** Incorporating stand mean height ($h_0$) alone yields a dramatic leap in explanatory power ($R^2_{\text{adj}} \approx 0.87$), far outperforming stand age $A$ alone ($R^2_{\text{adj}} \approx 0.50$) or quadratic mean diameter $d_0$ alone ($R^2_{\text{adj}} \approx 0.53$). Adding $d_0$ to $h_0$ provides an incremental further improvement to $R^2_{\text{adj}} \approx 0.90$.

## Implications for our pipeline

- **Inversion for DBH estimation:** In [[project/pipeline-overview]], remote sensing provides directly observed individual tree heights ($h$) from [[concepts/canopy-height-model]] (CHM) and canopy segmentation, but DBH ($d$) is unobserved. These non-linear forward models ($h = f(d, \dots)$) can be inverted or re-parameterized as $d = f^{-1}(h, h_0, d_0)$ to link detected tree heights to merchantable timber volumes in Scots pine stands (see [[concepts/height-diameter-inversion]]).
- **Stand-level remote sensing metrics:** Because the best generalized equations require stand-level mean height ($h_0$) and mean diameter ($d_0$), plot-level canopy metrics extracted across regional blocks (e.g., 90th percentile CHM height or area-level mean crown height) can directly serve as proxies for $h_0$ when predicting stems in [[concepts/normal-forest]].
- **Regional parameter calibration for Scots pine:** Lithuania shares ecological and silvicultural characteristics with broader Baltic and Nordic Scots pine zones. The empirical parameter estimates provided in Table 2 provide calibrated regional priors for pine allometry.

## Replication pseudocode

### Prerequisites

- Paired tree measurements: DBH ($d$, in cm) and total tree height ($h$, in m).
- Stand-level aggregate variables per plot:
  - Quadratic mean diameter: $d_0 = \sqrt{\frac{1}{m} \sum_{j=1}^m d_j^2}$ (cm).
  - Basal area-weighted mean height: $h_0 = \frac{\sum g_j h_j}{\sum g_j}$ (m), where $g_j = \frac{\pi}{4} d_j^2$.
- Non-linear least squares solver (e.g., Levenberg-Marquardt or Gauss-Newton via `scipy.optimize.curve_fit`).

### Procedure

```text
1. Data Preparation:
   a. Filter Scots pine (Pinus sylvestris) records with d > 0.
   b. Compute plot aggregates: quadratic mean diameter (d0) and basal area-weighted mean height (h0).
   c. Split dataset into estimation (approx. 58%) and validation (approx. 42%) subsets.

2. Candidate Model Specification:
   Define base models where h is predicted from d:
   - Eq. 1 (Korf):
       h = beta0 * exp(-beta1 * d^(-beta2))
   - Eq. 2 (Chapman-Richards, constrained h(0)=1.3):
       h = 1.3 + beta0 * (1 - exp(-beta1 * d))^beta2
   - Eq. 3 (Modified Logistic):
       h = beta0 / (1 + beta1 * d^beta2)
   - Eq. 4 (q-exponential, constrained h(0)=1.3):
       h = 1.3 + beta0 * (1 - (1 - (1 - beta3) * beta1 * d^[beta2])^(1 / (1 - beta3)))
       where [a]# = a if a >= 0 else 0

3. Asymptote Parameter Expansion:
   Substitute beta0 with stand-level covariate forms:
   - Base alone:  beta0
   - Form (a):    beta0 = beta0_base * A^alpha1           (Stand age A)
   - Form (b):    beta0 = beta0_base * d0^alpha1          (Mean diameter d0)
   - Form (c):    beta0 = beta0_base * h0^alpha1          (Mean height h0)
   - Form (d):    beta0 = beta0_base * d0^alpha1 * h0^alpha2 (Joint d0 and h0)

4. Model Parameter Estimation:
   a. Fit each model variation on the estimation dataset using non-linear least squares.
   b. Initialize parameters using values from Table 2:
      For Eq. 4 + Form (d):
        beta0 = 3.6201, beta1 = 1.2957, beta2 = 5.2523, beta3 = 2.8365
        alpha1 = -0.2684, alpha2 = 1.0303
   c. Verify convergence and asymptotic parameter standard errors (all p < 0.05).

5. Evaluation on Validation Set:
   a. Compute residual sum of squares (RSS), Mean Bias (B), Mean Absolute Bias (AB),
      Percentage Absolute Bias (PAB), adjusted R^2, and Akaike's Information Criterion (AIC).
   b. Inspect Lowess smoothed residual plots against predicted height to ensure homoscedasticity.
```

### Gaps / not specified in paper

- **Inversion stability:** The study exclusively models forward prediction of $h$ from $d$; mathematical inversion to predict $d$ given $h$ and stand covariates is not evaluated or formulated.
- **Stand density metrics:** Stand density index (SDI), stems per hectare (SPH), or basal area per hectare were not evaluated as candidate expansion variables for $\beta_0$.
- **Small tree behavior ($d < 15\text{ cm}$):** Although the model is described as applicable for $d > 0\text{ cm}$, the empirical dataset minimum diameter was $15.10\text{ cm}$ (Table 1). Performance on juvenile or suppressed trees under $15\text{ cm}$ DBH remains unvalidated.

## Quotes

- **On model constraints at origin:** "A constant, 1.3 was added to the model to avoid prediction of a height less than 1.3 m when diameter at breast height approaches zero." (p. 2)
- **On dataset size:** "3456 plots of Scots pine trees were chosen from the 2006-2010 database. A random sample of 2000 plots (7352 trees) was selected for model estimation, and the remaining data set of 1456 plots (5413 trees) was utilised for model validation." (p. 3)
- **On the performance of stand variables:** "The inclusion of mean diameter and mean height in the height-diameter models provided significantly better fits of height than those using only diameter and alone stand variable" (p. 5)
- **On q-exponential performance:** "In terms of all fitness statistics used, the q-exponential height model defined by Eqs. 4 and 8 appears to best predict height for Scots pine trees." (p. 5)

## Related pages

- [[concepts/height-diameter-inversion]] — Methodological context for reversing forward $h$–$d$ equations to predict DBH from remote sensing heights.
- [[concepts/site-index-and-yield]] — Stand-level dominant height, site index, and yield relationships in forest inventories.
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM surfaces delivering height inputs.
- [[concepts/normal-forest]] — Standard commercial forest stands where Scots pine allometry applies.
- [[project/pipeline-overview]] — Operational AREA processing flow.
