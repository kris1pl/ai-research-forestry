---
type: Source
title: "A Crown Width-Diameter Model for Natural Even-Aged Black Pine Forest Management"
description: "Nonlinear fixed and mixed-effects crown width models for Pinus nigra using DBH, competition metrics, and variance modeling."
tags: [allometry, crown-width, dbh, mixed-effects, pinus-nigra, forestry]
status: stable
updated: 2026-10-22
source_file: raw/papers/A Crown Width-Diameter Model for Natural Even-Aged Black Pine Forest Management-forests-09-00610-v2.pdf
authors:
  - Dimitrios Raptis
  - Vassiliki Kazana
  - Angelos Kazaklis
  - Christos Stamatiou
year: 2018
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-22T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/A Crown Width-Diameter Model for Natural Even-Aged Black Pine Forest Management-forests-09-00610-v2.pdf
    title: "A Crown Width-Diameter Model for Natural Even-Aged Black Pine Forest Management"
---

# A Crown Width-Diameter Model for Natural Even-Aged Black Pine Forest Management

## Summary

This paper develops empirical nonlinear models for predicting horizontal crown width ($CW$) in natural, even-aged Black pine (*Pinus nigra* Arn.) stands on Mount Olympus, Greece, using a dataset of 3,442 trees across 66 sample plots. The authors evaluate simple power models relating $CW$ directly to diameter at breast height ($DBH$), as well as generalized formulations incorporating stand and tree covariates: stand basal area ($BA$), canopy base height ($CBH$), relative spacing index ($RSI$), total tree height ($H$), and diameter-to-quadratic-mean-diameter ratio ($DQMD$).

To address plot-level autocorrelation and heteroscedasticity, the authors implement nonlinear mixed-effects modeling (`nlme`) paired with power and constant-power variance functions. Validation against an independent holdout sample demonstrated that calibrating the random plot effects using a small subsample (4 randomly chosen trees per plot) significantly reduced prediction error (RMSE $\approx 0.93$–$0.97\text{ m}$ vs. $>1.00\text{ m}$ for uncalibrated fixed effects), with the simple mixed-effects model performing almost on par with the multi-variable generalized model.

## Key claims

- **Power law dominates simple allometry:** Among base single-predictor forms, the power model $CW = \beta_0 DBH^{\beta_1}$ achieved the highest efficiency index ($EI = 0.6477$, $\text{RMSE} = 1.1151\text{ m}$) compared to linear, monomolecular, exponential, and logistic formulations (Table 3, p. 9).
- **Heteroscedasticity correction is essential:** Residual variance increases with tree diameter. Implementing a constant-power variance function $\operatorname{Var}(\varepsilon_{ij}) = \sigma^2 (\delta_1 + DBH_{ij}^{\delta_2})^2$ substantially reduced AIC from 8534.2 to 8169.9 for the simple mixed model (Table 4, p. 9).
- **Covariate interactions reverse marginal height effects:** While bivariate correlation shows $CW$ increasing with height $H$ ($r > 0$), in the generalized model containing $BA$ and $CBH$, the coefficient for $H$ becomes negative ($\beta_5 = -0.0019$). For a fixed diameter, taller trees possess narrower crowns due to lateral competition (p. 15–16).
- **Dominant height becomes redundant:** In forward stepwise addition, dominant height ($HDOM$) initially entered significantly, but became non-significant ($p > 0.05$) once stand basal area ($BA$) and canopy base height ($CBH$) were included (p. 16).
- **Mixed model calibration parity:** A simple mixed model using only $DBH$ with plot-level random intercept and slope, calibrated using 4 measured trees, attained an evaluation RMSE of $0.966\text{ m}$ (mean bias $0.0021\text{ m}$), nearly matching the generalized mixed model incorporating 5 covariates (RMSE $0.933\text{ m}$, bias $0.2557\text{ m}$) (p. 14).

## Implications for our pipeline

- **Inverting crown bounding boxes to stem diameter:** In [[project/research-normal-forest]] and [[concepts/crown-ownership]], detection modules output 2D bounding boxes and segmented crown widths from UAV orthophotos and [[concepts/canopy-height-model]]. While this paper predicts $CW$ from ground $DBH$, such power equations can be inverted ($DBH \approx (CW / \beta_0)^{1/\beta_1}$) to infer stem diameter distributions and stand volume from remote sensing detections.
- **Stand density adjustments:** Single-tree crown delineation often over-segments or merges crowns in dense conifer stands. The paper's negative allometric relationship between crown width and basal area ($BA$) or relative spacing ($RSI$) confirms that expected crown diameter priors in [[methods/deimv2-canopy]] must adapt downwards as stand density increases.
- **Subsample plot calibration:** When deploying UAV forest assessment over regional scales, a minimal ground sample (4 trees per stand) can calibrate random-effect intercepts, eliminating local bias in crown width/stem size estimations without requiring dense inventory re-cruising.

## Replication pseudocode

### Prerequisites

- Tree inventory dataset containing: plot ID, $CW$ (mean horizontal spread in meters across $\ge 2$ perpendicular axes), $DBH$ (cm), total height $H$ (m), $CBH$ (m).
- Plot-level stand metrics: $BA$ ($\text{m}^2/\text{ha}$), dominant height $HDOM$ (m), number of stems per hectare $N$, and Relative Spacing Index $RSI = \sqrt{10000 / N} / HDOM$.
- Nonlinear mixed-effects optimization library (e.g., R `nlme::nlme` or Python `statsmodels` / custom PyTorch/SciPy optimization).

### Procedure

```text
# Step 1: Fit base power model via Ordinary Least Squares (OLS)
fit_base:
    model: CW = beta0 * (DBH ^ beta1)
    record parameter estimates (beta0 ~ 0.35, beta1 ~ 0.79)

# Step 2: Fit Simple Nonlinear Mixed-Effects Model (MM2)
fit_simple_mixed:
    model: CW_ij = (beta0 + b0_i) * (DBH_ij ^ (beta1 + b1_i)) + eps_ij
    random effects: [b0_i, b1_i] ~ N(0, D)
    variance structure: Var(eps_ij) = sigma^2 * (delta1 + DBH_ij ^ delta2)^2
    optimize via maximum likelihood (nlme)

# Step 3: Fit Generalized Mixed-Effects Model (GMM2)
fit_generalized_mixed:
    model: CW_ij = (beta0 + b0_i) * (DBH_ij ^ beta1) * (
               BA_i ^ beta2 + 
               beta3 * CBH_ij + 
               beta4 * RSI_i + 
               beta5 * H_ij
           ) + eps_ij
    random effect: b0_i ~ N(0, sigma_b0^2)   # single random intercept
    variance structure: Var(eps_ij) = sigma^2 * (delta1 + DBH_ij ^ delta2)^2
    optimize via maximum likelihood

# Step 4: Localize / Calibrate for a new plot using k=4 trees
calibrate_plot(new_plot_data, k=4):
    sample_trees = randomly select 4 trees from new_plot_data
    compute residuals: e_hat = CW_sample - f(fixed_params, sample_trees)
    compute derivative matrix Z_hat w.r.t random parameters
    estimate random vector b_hat using empirical Bayes:
        b_hat = D_hat * Z_hat.T * inv(R_hat + Z_hat * D_hat * Z_hat.T) * e_hat
    predict CW for remaining trees in plot using fixed_params + b_hat
```

### Gaps / not specified in paper

- **Inversion stability:** The paper does not evaluate error propagation when mathematically inverting $CW = f(DBH)$ to predict $DBH = f^{-1}(CW)$ for airborne canopy measurements.
- **Tree crown eccentricity:** Crown width was averaged over two perpendicular axes using a hypsometer; horizontal crown asymmetry or polygon irregularity from UAV orthophotos is not modeled.
- **Dense young stands:** The dataset mean $DBH$ is $23.85\text{ cm}$ with minimum $1.1\text{ cm}$, but average stand height is $14.75\text{ m}$. Performance specifically on pre-thinning thickets ($H < 4\text{ m}$, R-class regeneration) is not isolated.

## Quotes

- *"Popescu et al. [13] demonstrated that the crown width is a tree dimension that is possible to measure directly with a lidar photogrammetric technique, while Gering and May [14] inversed a simple linear model for crown width prediction in order to predict diameter at breast height from aerial photos or photogrammetric data."* (p. 2)
- *"From Figure 2, it is quite clear that as height increases, crown width increases too, which is biologically valid. However, in conjunction with other variables (Equation (13) and Table 6), crown width decreases as height increases. This, however, was reported much earlier by Briegleb [60], who concluded that 'for trees of given diameter, the shorter trees have larger crowns than the taller'."* (p. 15–16)
- *"The results of the current study confirm this hypothesis, since the prediction improvement of the GMM2 model is relatively low compared to the MM2 model as far as crown width modeling is concerned. The random part of the simple MM2 model explained a large part of crown width variation, which the generalized GMM2 model managed to explain with the additional prediction variables."* (p. 16)

## Related pages

- [[project/pipeline-overview]] — Operational AREA processing flow from CHM/orthophoto detection to tree-level extraction
- [[project/research-normal-forest]] — Normal forest crown detection and dimensional assessment
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM surface generation
- [[concepts/crown-ownership]] — Spatial bounding box and top attribution logic
- [[concepts/site-index-and-yield]] — Stand-level dominant height, site curves, and timber stock modeling
