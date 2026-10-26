---
title: "Prediction of Diameter Using Height and Crown Attributes: A Case Study"
type: Source
tags: [dbh, allometry, crown-area, height, mixed-effects, inventory]
status: stable
updated: 2026-10-24
description: "Nonlinear mixed-effects models predicting DBH from tree height, crown area, and crown area of larger trees across three conifer species."
source_file: raw/papers/Prediction of Diameter Using Height and Crown Attributes - Filipescu_etal2012WJAFDbh_ht_model.pdf
authors: [Cosmin N. Filipescu, Arthur Groot, Dan A. MacIsaac, Mike G. Cruickshank, James D. Stewart]
year: 2012
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Prediction of Diameter Using Height and Crown Attributes - Filipescu_etal2012WJAFDbh_ht_model.pdf
    title: "Prediction of Diameter Using Height and Crown Attributes: A Case Study"
---

# Prediction of Diameter Using Height and Crown Attributes: A Case Study

## Summary

Filipescu et al. evaluate the feasibility of predicting stem diameter at breast height ($\text{DBH}$) using individual tree height ($HT$), crown projected area ($CA$), and local competition metrics. Using extensive field datasets from long-term silvicultural trials in Canada across three conifer species (black spruce, interior Douglas-fir, and lodgepole pine), the authors fit nonlinear mixed-effects models. 

While height or crown area alone yielded modest predictive accuracy ($\text{RMSE}$ between 1.65 and 4.62 cm), combining height, crown area, and a plot-level competition metric—the sum of crown area of larger trees ($\text{CAL}$, analogous to basal area of larger trees)—substantially reduced residual error. The resulting models achieved an $\text{RMSE}$ between 0.99 and 1.79 cm (10.1% to 11.3% of mean stem diameter), demonstrating a practical mathematical framework for converting remote sensing (UAV/LiDAR) derived crown and height detections into operational diameter estimates.

## Key claims

1. **Inverted base power model:** Inverting conventional height-diameter equations showed that a flexible power-form base equation, $\text{DBH} = \beta_0 (HT - 1.3)^{\beta_1} \beta_2^{(HT - 1.3)}$, outperformed or matched standard asymptotic sigmoidal curves (such as Chapman-Richards, Weibull, and Korf/Lunquist) (p. 31).
2. **Predictive synergy of height and crown area:** Height alone was a stronger single predictor for black spruce and lodgepole pine, whereas crown area alone was stronger for Douglas-fir. Combining both variables ($HT$ and $CA$) dramatically improved $R^2$ (e.g., jumping from 0.619 to 0.803 for Douglas-fir) (p. 32, Table 4).
3. **Competition metric ($\text{CAL}$) further improves accuracy:** Incorporating the cumulative crown area of larger trees ($\text{CAL}$) accounts for crown social status and light competition, dropping RMSE down to ~10% of mean tree DBH (p. 32–33).
4. **Treatment and spacing effects:** Inclusion of silvicultural treatment indicators (e.g., wide initial spacing $\ge 3\text{ m}$ for spruce, heavy thinning for lodgepole pine) was statistically significant, indicating that trees growing in wider spacing accumulate more stem diameter relative to their height and crown footprint due to increased resource access (p. 32–33).
5. **Heteroscedasticity correction:** Residual variance increased with height, which the authors successfully addressed using a power variance function $\text{Var}(\varepsilon) = \sigma^2 HT^{2\delta}$ (p. 32–33, Equation 14).

## Implications for our pipeline

- **Downstream diameter attribution:** In our production flow ([[project/pipeline-overview]]), individual tree detection yields 2D crown boxes/masks and heights (derived from the photogrammetric [[concepts/canopy-height-model]]). Incorporating Filipescu's model formulation allows us to estimate DBH and volume for detected stems without direct terrestrial stem measurements.
- **Computation of $\text{CAL}$ from ortho/CHM detections:** The competition metric $\text{CAL}$ ($\text{m}^2/\text{ha}$) can be calculated directly over any detected stand: for every tree $i$ in a plot or sliding radius, $\text{CAL}_i = \sum_{j: HT_j > HT_i} CA_j / \text{Area}$. This adds minimal computational overhead to fused detection GeoJSON outputs.
- **Normal forest crown sizing:** Relates directly to [[concepts/normal-forest]] and [[concepts/site-index-and-yield]], where merchantable tree crowns and stem taper depend on stocking density and competitive positioning.

## Replication pseudocode

### Prerequisites

- Detected tree centroids with estimated total tree height $HT$ (meters, above 1.3 m threshold) from CHM.
- Individual tree crown projected area $CA$ ($\text{m}^2$) from 2D segmentation or bounding polygon area.
- Delineated stand or plot area to calculate $\text{CAL}$ ($\text{m}^2/\text{ha}$).

### Procedure

```text
# 1. Feature Extraction per detected tree i:
#    - HT[i]: Top height extracted from local CHM peak (m)
#    - CA[i]: Crown projected area derived from segmented polygon (m^2)

# 2. Compute Competitive Metric (CAL):
for each tree i in stand of area A_ha:
    CAL[i] = sum(CA[j] for j in stand if HT[j] > HT[i]) / A_ha

# 3. Predict DBH using species-specific parameters (Fixed-effects / Population average):
# Base formulation: DBH = (beta_0 + beta_4 * CAL) * (HT - 1.3)^beta_1 * beta_2^(HT - 1.3) * CA^beta_3

if species == "Pseudotsuga menziesii":
    # Douglas-fir (Table 5, Eq 12 fixed components):
    beta_0 = 2.479
    beta_1 = 0.484
    beta_2 = 1.017
    beta_3 = 0.226
    beta_4 = -0.00026
    dbh_pred = (beta_0 + beta_4 * CAL[i]) * ((HT[i] - 1.3) ** beta_1) * (beta_2 ** (HT[i] - 1.3)) * (CA[i] ** beta_3)

elif species == "Pinus contorta":
    # Lodgepole pine (Table 5, Eq 13 fixed components without treatment):
    beta_0 = 2.622
    beta_1 = 0.458
    beta_2 = 1.028
    beta_3 = 0.159
    beta_4 = -0.0016
    dbh_pred = (beta_0 + beta_4 * CAL[i]) * ((HT[i] - 1.3) ** beta_1) * (beta_2 ** (HT[i] - 1.3)) * (CA[i] ** beta_3)

elif species == "Picea mariana":
    # Black spruce (Table 5, Eq 11 fixed components without treatment):
    beta_0 = 2.038
    beta_1 = 0.657
    beta_2 = 1.024
    beta_3 = 0.218
    dbh_pred = beta_0 * ((HT[i] - 1.3) ** beta_1) * (beta_2 ** (HT[i] - 1.3)) * (CA[i] ** beta_3)

# 4. Output: Attach predicted DBH (cm) to detection attributes
```

### Gaps / not specified in paper

- **Remote-sensing measurement error propagation:** The models were fitted on ground-measured crown dimensions; photogrammetric or LiDAR crown delineations often suffer from crown merging or under-segmentation in dense canopies.
- **Plot-boundary edge effects:** The paper does not specify how $\text{CAL}$ border edge correction was handled near plot margins.
- **Random-effect calibration:** For deployment without field plot calibration subsamples, only fixed effects can be utilized; the contribution of site-level random effects cannot be directly inferred without ground calibration trees.

## Quotes

- *On the role of competition:* "Crown area of larger trees likely reflects the competitive status (i.e., social status) and access to resources of the subject tree... resource availability during the growing season affects stem diameter to a larger extent than tree height, accounting for the need to include additional explanatory variables." (p. 33)
- *On model performance:* "Our best models provided low RMSE values between 0.99 and 1.79 cm, which is between 10.1 and 11.3% of average diameter... results presented in this case study are encouraging for the application of dbh models to a wider range of stands and conditions." (p. 33)

## Related pages

- [[concepts/canopy-height-model]] — Source layer for photogrammetric tree height estimation ($HT$).
- [[concepts/site-index-and-yield]] — Stand-level structural metrics, dominant height, and volume modeling.
- [[concepts/direct-stem-dbh-point-cloud]] — Alternative approaches estimating stem diameter directly from point cloud slices rather than crown allometry.
- [[concepts/normal-forest]] — Standard merchantable stands where crown attributes and social status drive diameter growth.
- [[project/pipeline-overview]] — Operational pipeline integrating detection, crown delineation, and downstream tree attributes.
