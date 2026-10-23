---
title: "A Linkage among Tree Diameter, Height, Crown Base Height, and Crown Width 4-Variate Distribution and Their Growth Models: A 4-Variate Diffusion Process Approach"
type: Source
tags: [allometry, sde, tree-dimensions, stem-volume, crown-width, scots-pine]
status: stable
updated: 2026-10-21
description: "Vasicek-type 4-variate stochastic differential equation framework modeling Scots pine DBH, height, crown base height, and crown width dynamics over stand age."
source_file: raw/papers/A_Linkage_among_Tree_Diameter_Height_Crown_Base_He.pdf
authors:
  - Petras Rupšys
  - Edmundas Petrauskas
year: 2017
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T21:40:00Z
sources:
  - id: primary
    resource: raw/papers/A_Linkage_among_Tree_Diameter_Height_Crown_Base_He.pdf
    title: "A Linkage among Tree Diameter, Height, Crown Base Height, and Crown Width 4-Variate Distribution and Their Growth Models: A 4-Variate Diffusion Process Approach"
related_methods:
  - methods/chm-detection
  - methods/deimv2-canopy
---

# A Linkage among Tree Diameter, Height, Crown Base Height, and Crown Width 4-Variate Distribution and Their Growth Models: A 4-Variate Diffusion Process Approach

## Summary

This paper introduces a continuous-time, 4-variate stochastic differential equation (SDE) model of the Vasicek type (mean-reverting Ornstein-Uhlenbeck diffusion process) to describe the joint dynamic distribution of four essential individual tree dimensions over stand age: diameter at breast height ($D$ or $X_1$), tree height ($H$ or $X_2$), crown base height ($CH$ or $X_3$), and crown width ($CW$ or $X_4$). Calibrated and validated on *Pinus sylvestris* L. (Scots pine) stands in Lithuania across 17 plots (1630 trees for calibration, 699 for validation), the resulting 4-variate normal distribution enables deriving marginal and conditional distributions of any subset of variables conditioned on others. The study demonstrates that predicting missing structural parameters (such as $D$ or stem volume) significantly improves when conditioning on both canopy height and crown dimensions ($H$, $CW$) simultaneously rather than relying on age or univariate allometry alone.

## Key claims

- Tree dimensions in even-aged stands can be modeled dynamically across stand age $t$ using a 4-variate Vasicek-type SDE drift-diffusion system:
  $$dX(t) = A(X(t))dt + B^{\frac{1}{2}} dW(t)$$
  which yields an exact 4-variate normal transition distribution $N_4(\mu(t), \Sigma(t))$ with closed-form time-dependent mean vector and covariance matrix (p. 3–4).
- The dynamic covariance structure captures mutual dependence between stem diameter, height, crown base height, and crown width over time (p. 4).
- Height ($H$) and crown base height ($CH$) exhibited the highest empirical correlation coefficient among Scots pine dimensions, whereas crown base height ($CH$) and crown width ($CW$) had the lowest (p. 9, Figure 3).
- In conditional univariate predictions of diameter ($D$):
  - Conditioning on age alone ($A$) achieved $R^2 = 0.432$ ($AE = 6.554\text{ m}$) on validation data.
  - Conditioning on age and height ($A, H$) yielded $R^2 = 0.773$ ($AE = 4.111\text{ m}$).
  - Conditioning on age, height, and crown width ($A, H, CW$) achieved $R^2 = 0.889$ ($AE = 2.873\text{ m}$), approaching the full model ($A, H, CH, CW$) with $R^2 = 0.892$ ($AE = 2.804\text{ m}$) (p. 9–10, Table 2).
- In predicting crown width ($CW$) from drone-observable variables, height alone ($A, H$) yielded an $R^2$ of only 0.447, while adding diameter or crown base height raised $R^2$ above 0.72 (p. 10–11, Table 2).
- Mean stem volume $V(t)$ and its standard deviation $SD(t)$ can be integrated directly over the marginal bivariate distribution $f(x_1, x_2, t \mid \hat{\theta})$ combining an allometric volume equation $V(d, h) = \beta_1 d^{\beta_2} h^{\beta_3}$ with the joint density (p. 12).

## Implications for our pipeline

- **Allometry and Volume Derivation from Drone Products:** In [[project/pipeline-overview]] and [[concepts/site-index-and-yield]], UAV surveys directly provide individual tree height ($H$) from the [[concepts/canopy-height-model]] and crown width/extent ($CW$) from segmentation polygons or bounding boxes. Rupšys & Petrauskas demonstrate that knowing both $H$ and $CW$ provides almost identical predictive power for stem diameter ($D$) as knowing $H$ and crown base height ($CH$) ($R^2 \approx 0.89$ vs $0.89$), allowing robust tree-level DBH and stem volume estimation without measuring beneath the canopy.
- **Biophysical Consistency Constraints:** For crown segmentation and ownership algorithms ([[concepts/crown-ownership]], [[concepts/normal-forest]]), the derived joint confidence ellipsoids $\chi^2_2(\alpha)$ provide parametric bounds to flag or reject impossible crown-to-height combinations (e.g., extreme crown width with juvenile height).
- **Stand Level Aggregation:** Marginal bivariate integration over $f(D, H, t)$ provides an analytical approach to integrate individual tree detections into stand-level volume distributions while accounting for natural variance-covariance without empirical fitting ad-hoc regression lines per flight.

## Replication pseudocode

### Prerequisites

- Stand age $t$ (years) and reference initial age $t_0$ (e.g., $t_0 \ge 0$, typically at germination/planting).
- Calibrated 4-variate fixed-effect parameters $\hat{\theta}$:
  - Drift asymptotic parameters $\alpha = [\alpha_1, \alpha_2, \alpha_3, \alpha_4]^T$ (for $D, H, CH, CW$).
  - Mean reversion speeds $\beta = [\beta_1, \beta_2, \beta_3, \beta_4]^T$.
  - Diffusion covariance matrix $B$ ($4 \times 4$ symmetric positive-semidefinite matrix with entries $\sigma_{ij}$).
- Observed tree metrics from UAV remote sensing: tree height $H$ ($x_2$) from CHM peak and crown diameter/width $CW$ ($x_4$) from instance segmentation mask/box.

### Procedure

```text
# Estimating Tree Diameter (D) and Stem Volume from UAV Height (H) and Crown Width (CW)

1. Compute time-dependent mean vector mu(t):
   For i in {1, 2, 3, 4}:
       mu_i(t) = alpha_i + (x0_i - alpha_i) * exp(-beta_i * (t - t0))
   (For Scots pine in Lithuania: alpha = [37.33, 27.63, 24.06, 4.98], beta = [0.0174, 0.0277, 0.0177, 0.0137])

2. Compute time-dependent variance-covariance matrix Sigma(t):
   For i, j in {1, 2, 3, 4}:
       Sigma_ij(t) = (sigma_ij / (beta_i + beta_j)) * (1 - exp(-(beta_i + beta_j) * (t - t0)))

3. Condition DBH (X1) on observed Height (X2 = h_obs) and Crown Width (X4 = cw_obs):
   Extract sub-vector for predictors: x_pred = [h_obs, cw_obs]^T
   Extract predictor mean: mu_pred = [mu_2(t), mu_4(t)]^T
   Extract cross-covariance Sigma_1_pred = [Sigma_12(t), Sigma_14(t)]
   Extract sub-covariance Sigma_pred_pred = [[Sigma_22(t), Sigma_24(t)],
                                            [Sigma_42(t), Sigma_44(t)]]

4. Calculate conditional mean and variance of diameter D (Equation 22-23):
   D_hat = mu_1(t) + Sigma_1_pred * inverse(Sigma_pred_pred) * (x_pred - mu_pred)
   Var_D = Sigma_11(t) - Sigma_1_pred * inverse(Sigma_pred_pred) * transpose(Sigma_1_pred)

5. Estimate individual stem volume V:
   V = beta_1 * (D_hat ^ beta_2) * (h_obs ^ beta_3)
   (For Scots pine: beta_1 = 5.8e-5, beta_2 = 1.8801, beta_3 = 0.9723)
```

### Gaps / not specified in paper

- **Initial state specifications ($x_0, t_0$):** The equations incorporate initial condition vector $x_0$ at $t_0$, but specific numerical start coordinates (e.g., seed/seedling baseline at $t_0=0$) are omitted in the main parameter table; parameter fits assume asymptotic convergence from planting/sprouting origin.
- **Stand density/competition index input:** Stand stocking density (trees per hectare) is omitted as a direct covariate; density effects are implicitly absorbed into crown size and age distributions.
- **Mixed-effects implementation:** The presented model uses fixed effects across all stands; the authors acknowledge that extending to mixed effects is necessary to address plot-level site index variation.

## Quotes

- *"The Vasicek type 4-variate fixed effect stochastic differential equation (SDE) to quantify the dynamic of tree size components distribution against the age... incorporated covariance structure driving changes in tree size components and improved predictions in one tree size component given the other tree size components in the system."* (p. 1, Abstract)
- *"In the modeling of the tree diameter, the largest contribution arises from the tree height (the second scenario) and from the tree height and crown width (the third scenario)."* (p. 11, Section 3.4)
- *"It is obvious that without knowing the underlying covariance structure driving changes in tree size components via age, we cannot appropriately identify predictor variables."* (p. 13, Section 4)

## Related pages

- [[concepts/site-index-and-yield]] — context on dominant height, stand age, and allometric yield estimation
- [[concepts/canopy-height-model]] — extraction of dominant canopy heights ($H$) matching parameter $X_2$
- [[concepts/crown-ownership]] — segmenting individual crown bounding regions ($CW$) matching parameter $X_4$
- [[project/pipeline-overview]] — production pipeline where tree detection outputs can feed allometric volume routines
