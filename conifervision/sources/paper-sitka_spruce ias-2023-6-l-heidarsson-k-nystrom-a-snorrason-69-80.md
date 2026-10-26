---
title: "Stem volume and above ground biomass models for Sitka spruce (Picea sitchensis (Bong.) Carr.) in Iceland"
type: Source
tags: [allometry, sitka-spruce, stem-volume, aboveground-biomass, iceland, forestry-inventory]
status: stable
updated: 2026-10-24
description: "Updated non-linear allometric power models for total aboveground biomass and stem volume of Sitka spruce in Iceland using DBH and total height."
source_file: raw/papers/Sitka_Spruce IAS-2023-6-L-Heidarsson-K-Nystrom-A-Snorrason-69-80.pdf
authors:
  - Lárus Heiðarsson
  - Kenneth Nyström
  - Arnór Snorrason
year: 2023
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Sitka_Spruce IAS-2023-6-L-Heidarsson-K-Nystrom-A-Snorrason-69-80.pdf
    title: "Stem volume and above ground biomass models for Sitka spruce (Picea sitchensis (Bong.) Carr.) in Iceland"
---

# Stem volume and above ground biomass models for Sitka spruce (Picea sitchensis (Bong.) Carr.) in Iceland

## Summary

This study by Heiðarsson et al. (2023) establishes updated empirical allometric models for estimating total aboveground dry biomass ($BM$, kg) and total stem volume above stump ($V$, $\text{dm}^3$ / liters) for Sitka spruce (*Picea sitchensis*) and hybrid Lutzii spruce (*Picea $\times$ lutzii*) in Iceland. The dataset comprises destructive sampling and sectional measurements from 48 even-aged plantation locations across Iceland planted between 1942 and 1983.

The authors demonstrate that older national models (Snorrason & Einarsson 2006) underestimate stem volume and aboveground biomass when extrapolated to older, larger stands (DBH up to 36 cm and heights up to 22.7 m). They fit non-linear allometric power functions of the form $Y = a \cdot DBH^b \cdot H^c$ using weighted non-linear regression (weighting by the inverse of initial unweighted predictions to control heteroscedasticity). In the biomass formulation, Sitka spruce and white spruce (*Picea glauca*) were statistically pooled ($n=57, R^2=0.952$), whereas stem volume required a species-specific Sitka spruce parameterisation ($n=204, R^2=0.992$).

## Key claims

- **Model formulations and parameters**:
  - Total Aboveground Biomass ($BM$, in kg):
    $$BM = 0.1128 \cdot DBH^{1.7531} \cdot H^{0.6634}$$
    ($R^2 = 0.952$, $\text{SEE} = 16.50\text{ kg}$, $\text{Bias} = 0.004\text{ kg}$, $n=57$; Sitka spruce and white spruce pooled).
  - Total Stem Volume ($V$, in $\text{dm}^3$ / liters):
    $$V = 0.0615 \cdot DBH^{1.7612} \cdot H^{1.0953}$$
    ($R^2 = 0.992$, $\text{SEE} = 11.91\text{ dm}^3$, $\text{Bias} = -0.07\text{ dm}^3$, $n=204$; Sitka spruce only).
- **Need for country-specific and age-updated models**: Older Icelandic equations (Snorrason & Einarsson 2006) underestimate volume and biomass when applied to stands reaching mature timber dimensions. Furthermore, foreign equations (e.g. Bauger 1995 for western Norway Sitka spruce, and Yarie & Van Cleve 1983 for Alaskan white spruce) overestimate biomass and underestimate stem volume for larger trees under Icelandic growing conditions (p. 76–77).
- **Inclusion of height**: Tree height ($H$) as a second explanatory variable significantly reduces model error across geographically dispersed stands with varying height-to-diameter ($H/D$) ratios (p. 70, 77).
- **Stand random effects**: Linear mixed-effects testing revealed no significant plot- or site-level random effects once $DBH$ and $H$ were included (p. 73).
- **Weighting against heteroscedasticity**: Heteroscedastic error variance was eliminated by weighting observations by the reciprocal of the predicted value from an initial unweighted non-linear fit ($w_i = 1 / \hat{y}_i$) (p. 73–74).

## Implications for our pipeline

- **Downstream timber and biomass estimation**: In [[project/pipeline-overview]], detected tree crowns classified as spruce by [[methods/dinov3-classification]] have direct height estimates extracted from the photogrammetric [[concepts/canopy-height-model]]. While direct DBH is not measured by 2D orthophotos/CHMs, these equations provide the foundational forward link from DBH and $H$ to cubic timber volume ($V$) and carbon metrics.
- **Inversion for remote sensing inventory**: To apply these allometric equations in our aerial pipeline, they must be coupled with [[concepts/height-diameter-inversion]] or crown-diameter-to-DBH models calibrated for Icelandic or sub-boreal plantation spruce.
- **Merchantable volume sizing in normal forest**: The volume equation provides ground truth conversion targets when evaluating single-crown merchantable timber in [[concepts/normal-forest]] and validating stand-level accumulation against yield tables in [[concepts/site-index-and-yield]].
- **Differentiation between species**: Because the volume model demonstrated a statistically significant divergence between Sitka spruce and white spruce (requiring Sitka-specific fitting), reliable crown-level classification (e.g. via DINOv3) is critical prior to volumetric inventory roll-up.

## Replication pseudocode

### Prerequisites

- Tree-level attribute table with columns: `tree_id`, `species`, `dbh_cm` ($DBH \ge 1.3\text{ m}$), and `height_m` (total tree height $H$).
- Parameter thresholds verified within data range: $DBH \in [2.8, 36.0]\text{ cm}$, $H \in [2.6, 22.7]\text{ m}$.

### Procedure

```text
# Input: Single tree records with DBH (cm) and Height (m)
# Output: Total stem volume (dm^3) and Total aboveground biomass (kg)

FOR EACH tree IN tree_records:
    ASSERT tree.height_m > 0
    ASSERT tree.dbh_cm > 0

    # Model 2: Total Aboveground Biomass (Picea sitchensis & Picea glauca)
    # Range check: DBH 4.8 - 32.9 cm, H 4.8 - 18.8 m
    biomass_kg = 0.1128 * (tree.dbh_cm ** 1.7531) * (tree.height_m ** 0.6634)

    # Model 3: Total Stem Volume (Picea sitchensis)
    # Range check: DBH 2.8 - 36.0 cm, H 2.6 - 22.7 m
    IF tree.species == "Picea sitchensis":
        volume_dm3 = 0.0615 * (tree.dbh_cm ** 1.7612) * (tree.height_m ** 1.0953)
    ELSE:
        # White spruce or other species require alternate allometry (TBD)
        volume_dm3 = TBD

    EMIT tree.id, biomass_kg, volume_dm3
```

### Gaps / not specified in paper

- **Direct remote-sensing predictors**: The paper exclusively models $DBH$ and $H$. It does not provide direct equations linking crown diameter (CD) or crown projection area (CPA) from drone orthophotos to $DBH$ or stem volume.
- **Stand density interactions**: Stand density is acknowledged as an influential factor altering taper and crown dynamics (planting densities dropped from 4,000 to 2,500 trees/ha in Iceland), but density metrics were not incorporated as explicit predictors in the published equations.
- **Root/belowground biomass**: Only aboveground biomass ($BM$) is modelled; root-to-shoot conversions or coarse root models are omitted.

## Quotes

- *On the necessity of allometry for emerging remote sensing:* "Despite recent advances in remote sensing and other survey instruments, single tree allometric models are still fundamental to biomass and stem volume prediction and for calibrating emerging technologies and new approaches to earlier estimates (Asner & Mascaro 2014, Ferraz & Saatchi 2016)." (p. 70)
- *On species combination for biomass vs. volume:* "In the updated aboveground biomass models, Sitka spruce and white spruce data were combined after testing if they belonged to the same population. A species indicator (dummy) variable was added to the new allometric model and was not found to be significant... A species indicator (dummy) variable was added to the new allometric model and was found to be significant, indicating that species was a relevant factor regarding stem volume prediction within the dataset." (p. 71)
- *On weighting to correct heteroscedasticity:* "To eliminate the bias effect of the error variance for volume and biomass models, which generally increases with tree size, and to reduce the effect of heteroscedasticity in the nonlinear models, the final model parameters were estimated with weighted nonlinear regression. The observations were weighted with the reciprocal of the prediction from a first unweighted model fit" (p. 73)
- *On geographic transferability:* "The foreign reference studies overestimated the total aboveground biomass and underestimated the stem volume, especially for larger trees... The difference was small but clearly shows the necessity to develop specific biomass and volume equations for Icelandic conditions." (p. 77)

## Related pages

- [[project/pipeline-overview]] — Operational pipeline producing height layers, bounding boxes, and DINOv3 species attributions.
- [[concepts/canopy-height-model]] — Photogrammetric height rasters providing tree height ($H$) estimates.
- [[concepts/normal-forest]] — Stand condition with merchantable timber volumes derived via allometric models.
- [[concepts/site-index-and-yield]] — Stand-level growth curves, site index, and cumulative volume metrics.
- [[concepts/height-diameter-inversion]] — Inversion formulations deriving DBH from height and crown width.
- [[methods/dinov3-classification]] — Species classification distinguishing Sitka spruce from adjacent species.
