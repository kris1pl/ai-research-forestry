---
type: Source
title: "Wang et al. (2013) — Crown and root biomass equations for the small trees of Pinus koraiensis under canopy"
description: "Branch- and whole-tree level allometric equations for understory Pinus koraiensis, demonstrating DBH and crown width utility over tree height."
tags: [allometry, biomass, understory, competition, pinus-koraiensis, crown-dimensions]
status: stable
updated: 2026-10-23
source_file: raw/papers/Crown_and_root_biomass_equations_fo.pdf
authors:
  - Jinsong Wang
  - Juan Fan
  - Xiuhua Fan
  - Chunyu Zhang
  - L. Wu
  - Klaus v. Gadow
year: 2013
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-23T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Crown_and_root_biomass_equations_fo.pdf
    title: "Crown and root biomass equations for the small trees of Pinus koraiensis under canopy"
related_methods:
  - methods/chm-detection
---

# Wang et al. (2013) — Crown and root biomass equations for the small trees of Pinus koraiensis under canopy

## Summary

Wang et al. (2013) analyze branch-level and tree-level allometry for small, understory *Pinus koraiensis* (DBH < 10 cm, height < 10 m) growing under a mature canopy (competing trees 30–35 m tall) in Changbaishan Nature Reserve, northeastern China. Based on destructive harvesting of 10 understory sample trees and 79 branch sub-samples, the authors fitted log-transformed power allometric equations for stem, live branch, needle, and coarse/fine root dry biomass components.

At the whole-tree level, stem DBH alone served as a strong predictor across components ($R^2_{\text{adj}} = 0.842\text{--}0.989$). Adding tree height ($H$) provided minimal improvement (except for needle biomass, adding ~8% explained variance), largely due to severe collinearity ($r = 0.96$ between DBH and $H$). Conversely, directional crown widths (specifically south–north width $\text{CSN}$ and east–west width $\text{CEW}$) significantly refined branch and needle biomass estimates. Additionally, aboveground competition intensity (Iterative Hegyi Index) was a significant negative predictor for all tree biomass components except crown foliage/branches. The authors show that generic or mature-tree allometric equations significantly overestimate understory sapling biomass.

## Key claims

- **Understory allometry diverges from mature trees**: Understory Korean pine saplings had lower aboveground and belowground biomass for a given DBH compared to published allometric models derived from larger trees in Heilongjiang ($b = 2.144$) and South Korea ($b = 2.386$), showing a lower allometric scaling slope ($b = 1.867$).
- **Tree height adds negligible predictive value**: Adding height to DBH models did not improve biomass component fits (except foliage), because DBH and height were highly collinear ($r = 0.96$), and height measurements introduce cumulative field error variance.
- **Crown dimensions improve canopy biomass estimates**: Crown widths ($\text{CSN}$ and $\text{CEW}$) significantly improved model fits ($R^2_{\text{adj}}$ increased from 0.910 to 0.991 for live branches, and from 0.842 to 0.972 for needles). $\text{CSN}$ correlated positively while $\text{CEW}$ correlated negatively with canopy biomass, reflecting asymmetric light interception in high-latitude stands.
- **Competition index impacts non-crown biomass**: Aboveground competition intensity ($\text{CI}$, measured via the Iterative Hegyi Index) was a statistically significant negative determinant for stem, fine root, and belowground biomass components.
- **Understory stand contribution**: While small trees accounted for ~5% of stand biomass ($3.20\text{ Mg ha}^{-1}$ out of $63.79\text{ Mg ha}^{-1}$), their belowground-to-aboveground biomass ratio was 0.16, compared to 0.30 for mature trees ($\text{DBH} > 10\text{ cm}$).

## Implications for our pipeline

- **Understory tree detection vs. Allometry**: In [[concepts/understory-tree-detection]], airborne sensors (orthophotos, photogrammetric CHMs) typically only register the uppermost canopy layer ([[concepts/canopy-height-model]]). If understory regeneration is detected via penetrative LiDAR or open-canopy gaps, applying adult allometric models will systematically overestimate biomass.
- **Crown width parameterization in allometric estimators**: For the allometry and yield concepts ([[concepts/tree-allometry]], [[concepts/site-index-and-yield]]), crown horizontal dimensions extracted from 2D crown segmentation or bounding boxes (e.g., [[concepts/crown-ownership]]) can directly serve as independent variables to calibrate foliage and branch biomass without relying strictly on drone-derived height metrics.
- **Competition-aware allometric adjustments**: The finding that neighborhood competition (Iterative Hegyi Index) suppresses individual tree stem and root volume reinforces that spatial tree density maps produced by [[project/pipeline-overview]] or [[project/research-normal-forest]] can serve as competition covariates when deriving stand-level carbon and biomass stocks.

## Replication pseudocode

### Prerequisites

- Destructive biomass sampling data: dry weights of stems, live branches, needles, coarse roots (> 5 mm), fine roots ($\le 5$ mm).
- Field inventory variables: $\text{DBH}$ (cm), total height $H$ (m), lowest live crown height $\text{LCH}$ (m), crown width south–north $\text{CSN}$ (m), crown width east–west $\text{CEW}$ (m), age $A$ (rings).
- Local neighborhood tree positions and DBHs for competitors within a 10 m radius.

### Procedure

```text
# Step 1: Compute aboveground competition intensity (Iterative Hegyi Index)
for each sample tree i:
    identify competitor trees j within radius R = 10 m where DBH_j > 5 cm
    compute distance Dist_ij between subject tree i and competitor j
    calculate Iterative Hegyi Index CI_i based on DBH_j / (DBH_i * Dist_ij)
    differentiating active vs. passive competitors per Lee & Gadow (1997)

# Step 2: Fit log-transformed linear regression models
# Form: ln(Y) = p0 + p1*ln(X1) + p2*ln(X2) + ... + pn*ln(Xn) + epsilon
for each biomass component Y in {stem, live_branch, needle, coarse_root, fine_root, aboveground, belowground}:
    fit Model 1: ln(Y) ~ ln(DBH)
    fit Model 2: ln(Y) ~ ln(DBH) + ln(H)
    fit Model 3 (stepwise, entry p < 0.15):
        ln(Y) ~ ln(DBH) + ln(H) + ln(CL) + ln(CSN) + ln(CEW) + ln(A) + ln(CI)

# Step 3: Compute transformation bias correction factor k
for each fitted model:
    k = sum(Y_observed) / sum(exp(predicted_ln_Y))
    unbiased_prediction = k * exp(p0 + sum(p_i * ln(X_i)))

# Step 4: Evaluate performance metrics
compute R2_adj, RMSE, RMSE_pct, MPE_pct, Bias, FI, and AIC
select best parsimonious model per component
```

### Gaps / not specified in paper

- **Sample size constraint**: The whole-tree equations are parameterized on $N = 10$ harvested sample trees, which provides high explanatory power ($R^2 > 0.95$) for this specific site but limits statistical power for multi-variable regressions and generalization across diverse forest types.
- **Iterative Hegyi parameter thresholds**: Specific iterative step criteria and dynamic zone thresholds used in the local algorithm variant are referenced via external papers (Lee & Gadow 1997; Wang et al. 2011) rather than fully parameterized in the text.
- **Crown shape extraction from above**: Ground tape-measured orthogonal crown axes ($\text{CSN}$, $\text{CEW}$) were used; mapping these directly to 2D photogrammetric crown polygons requires fitting oriented bounding boxes or principal directional axes (TBD).

## Quotes

- *On the lack of utility of tree height in understory models* (p. 22):
  > "In our study, using tree height as a second independent variable did not significantly improve the estimation, except in the case of needle biomass. This is probably caused by a high collinearity between breast height diameter and tree height, due to the high correlation between these two variables (0.96)."
- *On the impact of crown dimensions* (p. 22):
  > "Additional tree crown attributes proved to be useful for estimating all biomass components except fine roots. Crown width is an important determinant of canopy biomass and our best estimates of live branch and needle biomass were both based on crown width."
- *On aboveground competition affecting allometry* (p. 22):
  > "Our findings suggest that competition intensity is a significantly negative determinant of biomass components except canopy biomass. The most likely reason for this result maybe the effects of competition on biomass partitioning of above- and below-ground components and thus on the tree biomass allometry."
- *On size-dependent allometric deviations* (p. 23):
  > "Korean pine in this study has much lower aboveground and belowground biomass values for a given DBH than the trees grown in other two places. ... it is more likely that the differences in the allometric relationships are due to the differences in tree sizes. As trees in our study were restricted to the small trees with DBH≤10 cm..."

## Related pages

- [[concepts/tree-allometry]] — Individual tree allometric models linking crown dimensions and DBH to component biomass.
- [[concepts/understory-tree-detection]] — Understory saplings shielded by upper canopy layers.
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM representation vs. understory structure.
- [[concepts/site-index-and-yield]] — Stand-level vs. tree-level biomass and yield calculations.
- [[project/pipeline-overview]] — Operational pipeline context.
