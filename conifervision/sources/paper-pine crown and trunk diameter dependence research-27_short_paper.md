---
title: "Pine Crown and Trunk Diameter Dependence Research"
type: Source
tags: [allometry, crown-width, dbh, scots-pine, dense-stands]
status: stable
updated: 2026-10-22
description: "Empirical Gaussian-basis allometric models relating trunk diameter (DBH) to crown diameter for Scots pine in high-density Siberian stands."
source_file: raw/papers/Pine Crown and Trunk Diameter Dependence Research-27_short_paper.pdf
authors:
  - "Alexey S. Pyataev"
  - "Andrey A. Vais"
year: 2019
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-22T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Pine Crown and Trunk Diameter Dependence Research-27_short_paper.pdf
    title: "Pine Crown and Trunk Diameter Dependence Research"
---

# Pine Crown and Trunk Diameter Dependence Research

## Summary

This paper investigates the allometric relationship between trunk diameter at breast height (DBH) and horizontal crown diameter for Scots pine (*Pinus sylvestris*) growing in high-density stands near Kuragino in the Krasnoyarsk Krai (Siberia, Russia). In dense canopies, interlocking and mutual crown penetration impede visual and computer vision boundary segmentation.

Using field measurements from approximately 400 trees across various diameter steps (4 cm to 56 cm), the authors model crown diameter $g(x)$ as a function of trunk diameter $x$ using Gaussian basis approximations. A piecewise two-component Gaussian function ($x \le 28$ cm and $28 < x \le 52$ cm) achieves a mean approximation error of 4.05% relative to empirical diameter class means, outperforming a single Gaussian formulation (13.11% mean error). The authors propose using this allometric relationship as a corrective prior when delineating overlapping tree crowns in computer vision and forest health assessments.

## Key claims

- **Crown interpenetration limits 2D computer vision:** In high-density plantations, optical boundary delineation fails because crown boundaries overlap significantly; crown density variations within a single sanitary class can reach 30% (p. 2).
- **Trunk-to-crown empirical scaling:** For Scots pine in dense stands, average crown diameter ranges from 1.08 m (at 4 cm DBH) to 8.19 m / 6.38 m (at 52–56 cm DBH) (Table 1, Table 3).
- **Single Gaussian approximation:** Modeling crown diameter with a single Gaussian model $g(x) = 11 e^{-\frac{(x-80)^2}{2380}} + 0.5$ (for $x \le 52$ cm) yields a mean approximation error of 13.11% (p. 3–4).
- **Two-piece Gaussian formulation:** Partitioning the trunk diameter at 28 cm into two Gaussian functions reduces mean approximation error to 4.05% (p. 4–5):
  $$g(x) = \begin{cases} 3.9 e^{-\frac{(x-30)^2}{327.68}} + 0.6, & x \le 28 \\ 3.7 e^{-\frac{(x-52)^2}{112.5}} + 4.5, & 28 < x \le 52 \end{cases}$$
- **Corrective prior for ambiguous bounds:** Known DBH distributions or stem inventory can constrain expected crown projection sizes during visual or automated crown boundary resolution (p. 5).

## Implications for our pipeline

- **Crown size prior in [[project/pipeline-overview]]:** While our operational flow detects crowns from aerial CHM and orthophoto rasters (detecting crown first, then inferring tree attributes), the inverse of Pyataev & Vais's formula provides a sanity check: an inferred crown diameter of 1.5–2.0 m corresponds to young saplings/pole timber (DBH ~8–12 cm), whereas crowns >5 m imply mature stems (DBH >36 cm).
- **Priors for [[concepts/crown-ownership]] and [[concepts/normal-forest]]:** When segmenting touching pine crowns in normal or dense forest, bounding box dimensions can be bounded by species-specific crown width expectations rather than allowing NMS or watershed algorithms to merge multiple crowns into single massive segments or over-split single mature crowns.
- **Limitation for drone-only workflows:** The paper assumes trunk diameter is measured during ground cruising (forest taxation surveys) to predict crown diameter. In aerial photogrammetry/LiDAR, we measure crown width directly to predict DBH (see [[concepts/direct-stem-dbh-point-cloud]] and [[concepts/site-index-and-yield]]). Inverting their piecewise function requires numerical inversion or solving the Gaussian quadratic exponents.

## Replication pseudocode

### Prerequisites

- Trunk diameter at breast height ($x$ in cm) within the range $[4, 52]$ cm for Scots pine (*Pinus sylvestris*).

### Procedure

```text
# Input: dbh_cm (float or ndarray)
# Output: expected_crown_diameter_m (float or ndarray)

function predict_pine_crown_diameter(dbh_cm):
    if dbh_cm < 4.0 or dbh_cm > 52.0:
        log_warning("DBH out of calibrated range [4, 52] cm")
    
    if dbh_cm <= 28.0:
        exponent = - ((dbh_cm - 30.0) ** 2) / 327.68
        crown_diam = 3.9 * exp(exponent) + 0.6
    else:
        exponent = - ((dbh_cm - 52.0) ** 2) / 112.5
        crown_diam = 3.7 * exp(exponent) + 4.5
        
    return crown_diam
```

### Gaps / not specified in paper

- **Inversion formula:** The paper only fits $g(x) = \text{crown\_diam}(x)$, not the inverse function predicting DBH from crown diameter, which is the primary operational direction for UAV remote sensing.
- **Tree height exclusion:** Tree height ($H$) was not incorporated into the regression, despite noting the geometric primitives model (Han et al. 2016) in Figure 1. In aerial CHM pipelines, height is our primary observed metric.
- **Stand density metrics:** Stand stocking density (stems/ha, basal area) is qualitatively described as "high-density plantations" / "high-full stands", but exact stocking numbers or crown competition indices for the 400 sampled trees are not tabulated.

## Quotes

- **On dense stand segmentation challenges (p. 1):**  
  > "Using computer vision methods, it is often difficult to identify the crown boundaries of a particular tree in high-density plantation, as the crowns of trees penetrate significantly into each other."
- **On model utility (p. 2):**  
  > "Thus, the crown diameters due to trunk diameters dependence assessment , specific for a certain completeness of a plantation, will help to increase the reliability of determining the crown boundaries using computer vision methods from images in high-density plantations."
- **On accuracy of the two-function approximation (p. 5):**  
  > "...using one-function approximation of the function describing the dependence the pine crown diameter from the trunk diameter shows an average approximation error of 13%, at the same time using of two-function approximation gives an average error of 4%."

## Related pages

- [[project/pipeline-overview]] — Operational pipeline from aerial CHM to detected crowns and species classification.
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM height rasters.
- [[concepts/crown-ownership]] — Allocation of crown footprint and bounding boxes in overlapping canopies.
- [[concepts/normal-forest]] — Merchantable crowns with distinct apexes.
- [[concepts/direct-stem-dbh-point-cloud]] — Methods directly measuring stem diameter from 3D points.
- [[concepts/site-index-and-yield]] — Stand-level allometry and yield modeling.
