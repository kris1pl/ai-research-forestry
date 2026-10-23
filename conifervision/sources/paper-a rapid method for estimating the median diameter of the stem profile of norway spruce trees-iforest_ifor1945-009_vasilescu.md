---
title: "A rapid method for estimating the median diameter of the stem profile of Norway spruce (Picea abies Karst) trees"
type: Source
tags: [allometry, stem-profile, stem-volume, norway-spruce, picea-abies, dendrometry]
status: stable
updated: 2026-10-24
description: "Presents empirical models demonstrating that the median diameter of the longitudinal stem profile in Norway spruce occurs at ~0.3 × height and is strongly predicted by DBH."
source_file: raw/papers/A rapid method for estimating the median diameter of the stem profile of Norway spruce trees-iForest_ifor1945-009_Vasilescu.pdf
authors:
  - Maria Magdalena Vasilescu
  - Cornel Cristian Teresneu
  - Florin Dinulica
year: 2017
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/A rapid method for estimating the median diameter of the stem profile of Norway spruce trees-iForest_ifor1945-009_Vasilescu.pdf
    title: "A rapid method for estimating the median diameter of the stem profile of Norway spruce (Picea abies Karst) trees"
---

# A rapid method for estimating the median diameter of the stem profile of Norway spruce (Picea abies Karst) trees

## Summary

This paper presents an empirical analysis of longitudinal stem profiles based on historical dendrometric measurements of 5,403 Norway spruce (*Picea abies* Karst.) trees across 200 plots in the Romanian Carpathians (grouped into 218 height-diameter classes). The authors evaluate Mathiesen's formula for stem volume, which relies on the total area of the stem longitudinal section ($A$) and its median diameter ($D_M$, the diameter dividing the longitudinal stem area into two equal parts). 

Because calculating $D_M$ classically requires labor-intensive taper measurements at narrow intervals along the bole, the authors model $D_M$ and its position along the stem. They establish two main findings:
1. $D_M$ can be predicted directly from diameter at breast height ($\text{DBH}$) with high precision ($R^2 = 0.9985$): $D_M = 0.7061 \cdot \text{DBH} + 3.235$ (or simplified as $0.7 \cdot \text{DBH} + 3$).
2. Across all tree size classes, the height at which this median diameter occurs ($H_{DM}$) is located almost invariantly at approximately $0.3 \times H$ ($H_{DM\text{rel}} \approx 0.2987$, coefficient of variation 4.88%).

The paper discusses how stem profile descriptors like $D_M$ and the ratio $D_M / H$ relate to stem taper, mechanical wind stability, and stand competition.

## Key claims

- **Mathiesen's stem volume method:** The volume of a tree stem can be derived from longitudinal section area $A$ and median diameter $D_M$ via $V = \frac{3}{4} \cdot D_M \cdot A$ (Mathiesen 1925).
- **Strong linear coupling between DBH and median stem diameter:** Diameter at breast height is the primary predictor for $D_M$ ($R^2 = 0.9985$, $F = 143871.1$):
  $$D_M = 0.7061 \cdot \text{DBH} + 3.235$$
  A bivariate regression adding height ($H$) improves the fit marginally ($R^2 = 0.9991$):
  $$D_M = 2.716099 + 0.688689 \cdot \text{DBH} + 0.041612 \cdot H$$
- **Invariance of relative height of median diameter:** Across 218 diameter-height classes spanning DBH 12–60 cm and total height 10–42 m, the relative height of $D_M$ ($H_{DM\text{rel}} = H_{DM} / H$) shows an arithmetic mean of $0.2978$ to $0.2987$ ($\approx 0.3 \times H$) with an extremely low coefficient of variation ($1.99\%$ to $4.88\%$).
- **Model estimation error:** Differences between $D_M$ calculated by discrete 2 m sectional integration and $D_M$ predicted by the linear DBH model were less than 2% in 86.24% of tested cases, with a maximum absolute error of 0.88 cm.
- **Biomechanical significance of $0.3 \times H$:** Approximately 50% of the stem volume and profile area is concentrated below $0.3 \times H$. The $D_M / H$ ratio is proposed as a relevant metric for stem breakage strength and resistance to overturning.

## Implications for our pipeline

- **Secondary mensuration / timber volume estimation:** While [[project/pipeline-overview]] currently prioritizes 2D detection, segmentation, and species classification, post-processing downstream products linked to [[concepts/site-index-and-yield]] require volume and biomass estimation. If canopy height models ([[concepts/canopy-height-model]]) provide tree height ($H$) and crown width / DBH allometry provides estimated DBH, this paper provides a lightweight, parameter-efficient formulation to infer upper-stem taper ($D_{0.3H}$) and volume without full 3D point cloud reconstruction of the stem.
- **Crown-to-stem allometry handoff:** In high-resolution drone photogrammetry and LiDAR, only the canopy and upper bole are typically visible. Knowing that stem profile median properties align at $0.3 \times H$ allows bounding lower-bole volume assumptions from UAV-derived crown metrics and top heights.
- **Stability and wind risk assessment:** Stand structure attributes derived from drone detections (such as dominant height and predicted taper $D_M / H$) could feed post-inventory risk models for windthrow or snow breakage in coniferous stands.

## Replication pseudocode

### Prerequisites

- Input tree metrics: Diameter at breast height ($\text{DBH}$, in cm) and total tree height ($H$, in m).
- Calibration tables or local coefficients for Norway spruce (*Picea abies*).

### Procedure

```text
# Estimating Stem Profile Median Diameter and Position (Vasilescu et al. 2017)

def estimate_norway_spruce_stem_median(dbh_cm: float, height_m: float, model_type: str = "simple"):
    # 1. Estimate height along stem where median diameter occurs
    # Across diameter classes, HDM_rel is approximately 0.3 * H
    h_dm_m = 0.3 * height_m
    
    # 2. Estimate median diameter (DM) of the longitudinal stem section
    if model_type == "quick":
        # Simplified operational formula (eqn 12)
        dm_cm = 0.7 * dbh_cm + 3.0
    elif model_type == "linear_dbh":
        # Univariate linear model (eqn 6, R^2 = 0.9985)
        dm_cm = 0.7061 * dbh_cm + 3.235
    elif model_type == "bivariate":
        # Multiple regression model (Table 1, R^2 = 0.9991)
        dm_cm = 2.716099 + 0.688689 * dbh_cm + 0.041612 * height_m
    else:
        raise ValueError("Unknown model_type")
        
    # 3. Compute taper / stability ratio
    taper_ratio = dm_cm / (height_m * 100.0) # dimensionless ratio
    
    return {
        "median_diameter_cm": dm_cm,
        "height_of_median_diameter_m": h_dm_m,
        "dm_h_ratio": taper_ratio
    }
```

### Gaps / not specified in paper

- **Direct remote sensing tie-in:** The paper operates entirely on ground-truth inventory tables from felled/measured trees; it provides no direct methodology for inferring DBH from crown diameter or UAV orthophoto metrics.
- **Mathiesen section area computation ($A$):** The paper provides the formula $V = \frac{3}{4} \cdot D_M \cdot A$, but estimating total longitudinal profile area $A$ without detailed taper measurements is not fully operationalized without integrating an assumed geometric profile form.
- **Stand density and thinning interaction:** The data originate from historical Carpathian yield tables prior to 1950; specific impacts of modern thinning regimes, initial planting spacing, or stand density on the $0.3 \times H$ constant are noted as needing further study.

## Quotes

- **On the invariant height of median diameter:**  
  *"Statistical analysis revealed that the height of the median diameter on the stem profile was 0.3 × H (tree height)."* (p. 328)
- **On DBH as the primary predictor:**  
  *"The strongest predictor of the median diameter for the stem profile was the diameter at breast height (R2 = 0.9985)."* (p. 328)
- **On Mathiesen's formula:**  
  *"If the median diameter value of the stem profile is known, the stem volume may be computed using the Mathiesen’s formula (Mathiesen 1925 – eqn. 1): $V = \frac{3}{4} \cdot D_M \cdot A$ ... However, because laborious calculation is required, Mathiesen’s formula is avoided in practice..."* (p. 328)
- **On mechanical stability and stem taper:**  
  *"The ratio defined by the median diameter of the stem profile and tree height (DM/H) helps to determine the breaking strength of the stem and, hence, tree resistance to overturning."* (p. 332)

## Related pages

- [[concepts/site-index-and-yield]] — Stand-level metrics, dominant height, and volume calculation.
- [[concepts/canopy-height-model]] — CHM extraction supporting tree height ($H$) inputs.
- [[concepts/normal-forest]] — Application scope for mature merchantable coniferous stands.
- [[project/pipeline-overview]] — Operational tree detection and classification baseline.
