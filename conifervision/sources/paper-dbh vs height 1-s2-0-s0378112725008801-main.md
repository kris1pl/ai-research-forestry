---
title: "Species-specific modeling of tree diameter at breast height using tree height and relative density with implications for remote sensing-based forest inventory"
type: Source
tags: [allometry, dbh-estimation, relative-density, remote-sensing, permanent-sample-plots, competition-index]
status: stable
updated: 2026-06-09
description: "Inverted allometric model predicting tree DBH from height and Reineke-based stand relative density across six temperate tree species."
source_file: raw/papers/DBH vs Height 1-s2.0-S0378112725008801-main.pdf
authors:
  - Soheil Soheili Esfahani
  - Fan-Rui Meng
  - Christopher YS Wong
year: 2026
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-06-09T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/DBH vs Height 1-s2.0-S0378112725008801-main.pdf
    title: "Species-specific modeling of tree diameter at breast height using tree height and relative density with implications for remote sensing-based forest inventory"
---

# Species-specific modeling of tree diameter at breast height using tree height and relative density with implications for remote sensing-based forest inventory

## Summary

This paper develops a species-specific nonlinear modeling framework to invert the classical forestry allometric relationship by predicting individual tree diameter at breast height (DBH, cm) directly from total tree height ($H$, m) and stand-level relative density ($RD$). Using permanent sample plot (PSP) data from New Brunswick, Canada (1,807 trees across 653 plots of 400 m² between 1985 and 2014), the authors model six dominant boreal and temperate species: *Abies balsamea* (balsam fir), *Acer rubrum* (red maple), *Acer saccharum* (sugar maple), *Picea mariana* (black spruce), *Picea rubens* (red spruce), and *Picea glauca* (white spruce).

While height-only models yield low-to-moderate explanatory power for broadleaves ($R^2 = 0.15$ to $0.35$) and moderate power for conifers ($R^2 = 0.41$ to $0.74$), adding $RD$ as a competitive suppression index raises $R^2$ to $0.85\text{--}0.89$ for broadleaves and $0.72\text{--}0.88$ for conifers while slashing RMSE and MAE by more than half. The study provides an allometric bridge for remote sensing pipelines (e.g., LiDAR or drone [[concepts/canopy-height-model|CHM]]), where vertical height is directly measurable but stem diameter must be inferred.

## Key claims

- **Height-only inversion is inadequate for broadleaves:** Predicting DBH from height alone yields weak fits in shade-tolerant and competitive broadleaves (*Acer saccharum* $R^2 = 0.15$, RMSE = 6.27 cm; *Acer rubrum* $R^2 = 0.35$, RMSE = 5.44 cm). Conifers perform moderately better (*Abies balsamea* $R^2 = 0.74$, *Picea mariana* $R^2 = 0.54$, *Picea rubens* $R^2 = 0.41$, *Picea glauca* $R^2 = 0.58$).
- **Multiplicative power-law formulation stabilizes fit:** The selected model formulation $\text{DBH} = (1 + K_0) \times \text{HEIGHT}^{K_h} \times \text{RD}^{K_r}$ avoids parameter collinearity and non-identifiability problems observed in varying-parameter forms $a(RD), b(RD)$.
- **Stand competition suppresses radial growth:** Across all species, the competition parameter $K_r$ is negative. Sugar maple ($K_r = -0.45$) and balsam fir ($K_r = -0.34$) exhibit strong radial growth suppression under high stand density, whereas black spruce ($K_r = -0.07$) and red spruce ($K_r = -0.06$) are less sensitive to density variations.
- **RD improves conifer fits as well:** Incorporating $RD$ raises fits to $R^2 = 0.86$ for *A. balsamea*, $R^2 = 0.82$ for *P. mariana*, and $R^2 = 0.88$ for *P. rubens*. *Picea glauca* shows the lowest fit ($R^2 = 0.72$, RMSE = 4.42 cm), attributed to wider ecological plasticity and microsite variability.
- **Self-thinning slope deviates from Reineke's universal constant:** Log-linear OLS fits of the self-thinning boundary $\ln(N_{\text{ha}}) = \ln(\alpha) - \beta \cdot \ln(\text{DBH}_{\text{plot}} / \text{DBH}_r)$ yield $\beta$ slopes from $-0.05$ (black spruce) to $-1.075$ (sugar maple), consistently shallower than Reineke's classical $-1.605$ due to multi-cohort, mixed-species structural dynamics.

## Implications for our pipeline

- **Downstream allometry attribution:** In [[project/pipeline-overview]], our operational AREA pipeline outputs 2D crown detections with heights derived from the [[concepts/canopy-height-model|CHM]] and taxonomic identity from [[methods/dinov3-classification|DINOv3 species classification]]. Integrating this paper's power law enables tree-level DBH and subsequent stem volume calculations without direct ground stem measurements ([[concepts/tree-allometry]]).
- **Local density computation:** Operational drone data lacks direct ground plot DBH tallies to calculate Reineke's $RD$. To apply this model to drone orthophotos, $N_{\text{plot}}$ can be estimated via detected crown density (stems/ha) within a moving window or stand polygon, but mean plot DBH ($\text{DBH}_{\text{plot}}$) must either be solved iteratively or approximated using regional yield tables / diameter priors ([[concepts/site-index-and-yield]]).
- **Impact of classification error:** The paper explicitly notes that species misclassification between conifers (e.g., *A. balsamea* vs. *P. glauca*) will inject equation selection errors. If [[methods/dinov3-classification|DINOv3]] confidence is below threshold, fallback grouping (conifer vs. broadleaf general equations) is recommended.

## Replication pseudocode

### Prerequisites

- Tree-level vertical height (e.g., peak elevation above ground from [[concepts/canopy-height-model|CHM]]).
- Stand-level or local neighborhood relative density ($RD$), derived from stem density and mean DBH reference.
- Species attribution (e.g., from [[methods/dinov3-classification|DINOv3 classification]]).
- Calibrated regression parameters ($K_0, K_h, K_r$) per species (or genus fallback).

### Procedure

```text
# Estimating DBH from remote sensing height and stand density

1. Obtain tree crown position and maximum canopy height (HEIGHT in meters) from CHM.
2. Predict species label using crown crop and DINOv3 classifier.
3. Compute stand-level or localized neighborhood density:
   a. Compute stem count N_plot within local evaluation radius/polygon (converted to stems/ha).
   b. Estimate DBH_plot (mean DBH in cm) via stand inventory prior or iterative allometry convergence.
   c. Retrieve species-specific self-thinning parameters alpha and beta (reference DBH_r = 20 cm):
        N_max = alpha * (DBH_plot / 20.0) ^ (-beta)
   d. Calculate Relative Density:
        RD = N_plot / N_max
4. Select species-specific coefficients (K0, Kh, Kr) from calibration table:
   - Abies balsamea:      Kh ~ 0.60 to 0.67, Kr = -0.34
   - Acer rubrum:         Kh = 0.66,         Kr = -0.23
   - Acer saccharum:      Kh = 0.39,         Kr = -0.45
   - Picea mariana:       Kh ~ 0.60 to 0.67, Kr = -0.07
   - Picea rubens:        Kh ~ 0.60 to 0.67, Kr = -0.06
   - Picea glauca:        Kh = 0.10,         Kr = -0.35
   - Fallback (group):    Use broadleaf or conifer group parameters if species confidence < TBD
5. Calculate predicted DBH:
   DBH_pred = (1.0 + K0) * (HEIGHT ^ Kh) * (RD ^ Kr)
6. Attach DBH_pred attribute to tree GeoJSON hypothesis.
```

### Gaps / not specified in paper

- **Remote-sensing-only $RD$ calculation:** The paper calculates $RD$ using ground-measured plot mean diameter ($\text{DBH}_{\text{plot}}$). In a pure remote sensing workflow, $\text{DBH}_{\text{plot}}$ is unobserved *a priori*; the paper does not specify how to estimate $RD$ purely from remote sensing metrics without circular dependency.
- **Exact coefficient tables:** Numerical values for $K_0$, standard errors, and complete regression diagnostics are listed in online supplementary material Appendix A (Tables A8–A11), which are summarized in the main text narrative but lack explicit table prints for all intercepts in the primary body.
- **Spatial smoothing / edge effects:** The paper uses bounded 400 m² plots; moving-window edge buffer corrections for calculating local stem density from orthomosaics are not evaluated.

## Quotes

- **On remote sensing height availability vs. DBH:** "With the rise of remote sensing technologies, height has become a readily available and spatially continuous variable, offering a valuable opportunity to estimate DBH in areas where field access is limited... direct DBH measurements remain unattainable from above-canopy remote sensing, especially in closed-canopy and multi-layered forests." (p. 1–2)
- **On relative density formulation:** "The relative density index RD is defined as: $\text{RD} = \frac{N_{\text{plot}}}{N_{\text{max}}} = \frac{N_{\text{plot}}}{\alpha \left( \frac{\text{DBH}_{\text{plot}}}{\text{DBH}_r} \right)^\beta}$" (p. 3)
- **On the nonlinear DBH model:** "$\text{DBH} = (1+K_0) \times \text{HEIGHT}^{K_h} \times \text{RD}^{K_r}$ ... maintaining parameter stability while allowing HEIGHT to represent vertical growth allocation and RD to represent competition-driven suppression of diameter growth." (p. 4)
- **On classification error propagation:** "classification errors would not affect the height input, but may result in model-selection error (assigning a tree to the wrong species-specific equation). This may introduce bias in predicted DBH, especially for species pairs with differing competitive responses. To address this, we recommend (1) using species-group (e.g., conifer vs. broadleaf) model forms when species-level confidence is low..." (p. 9)

## Related pages

- [[concepts/tree-allometry]] — Individual tree allometric relations (height, DBH, crown width).
- [[concepts/canopy-height-model]] — Input source for tree height measurements.
- [[concepts/site-index-and-yield]] — Stand-level metrics, dominant height, and stocking relationships.
- [[methods/dinov3-classification]] — Species classification supplying taxonomic labels for equation selection.
- [[project/pipeline-overview]] — Operational pipeline context where DBH can be derived post-detection.
