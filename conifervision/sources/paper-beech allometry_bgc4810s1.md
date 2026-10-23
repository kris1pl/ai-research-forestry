---
title: "Optimising profits from timber harvest and the biodiversity conservation value in a central European beech forest using a novel bioeconomic forestry model (Supplementary Material)"
type: Source
tags: [allometry, beech, dbh, crown-area, height, canopy-layering]
status: stable
updated: 2026-10-24
description: "Empirical allometric relations predicting crown area and height from DBH for European beech, hornbeam, lime, and maple."
source_file: raw/papers/Beech allometry_BGC4810s1.pdf
authors:
  - "Schorn et al."
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Beech allometry_BGC4810s1.pdf
    title: "Optimising profits from timber harvest and the biodiversity conservation value in a central European beech forest using a novel bioeconomic forestry model (Supplementary Material)"
related_methods:
  - methods/chm-detection
  - methods/dinov3-classification
---

# Optimising profits from timber harvest and the biodiversity conservation value in a central European beech forest using a novel bioeconomic forestry model (Supplementary Material)

## Summary

This supplementary document to Schorn et al. (2025) provides species- and genus-specific allometric equations linking diameter at breast height ($\text{DBH}$ in $\text{cm}$) to tree height ($H$ in $\text{m}$) and crown projected area ($\text{CA}$ in $\text{m}^2$). The parameters were fitted using non-linear least squares (`scipy.optimize.least_squares`) on an inventory dataset of 1,316 trees from Weberstedter Holz, Germany. Models cover *Fagus sylvatica* (European beech), *Carpinus betulus* (hornbeam), *Tilia* spp. (lime), and *Acer* spp. (maple), with beech parameters serving as proxies for oak (*Quercus robur*) and ash (*Fraxinus excelsior*). Additionally, the text specifies empirical recruitment rates under open ($<1$) versus closed ($\ge 1$) canopy shading and compiles structural validation metrics across multiple European old-growth beech sites.

## Key claims

- **DBH-to-crown area allometry:** Crown area ($\text{ca}$, $\text{m}^2$) follows a double-logistic curve relative to $\text{DBH}$ ($\text{cm}$):
  $$\text{ca} = \frac{a}{1 + \exp\left(\frac{c - \text{DBH}}{d}\right)} + \frac{b}{1 + \exp\left(\frac{c - \text{DBH}}{d}\right)}$$
  Parameter values fitted:
  - *Fagus sylvatica* ($n=842$): $a = 10.31$, $b = 250$, $c = 18.06$, $d = 77.06$
  - *Carpinus betulus* ($n=35$): $a = -29.13$, $b = 200$, $c = 26.56$, $d = 46.54$
  - *Tilia* spp. ($n=366$): $a = -0.50$, $b = 200$, $c = 19.00$, $d = 64.93$
  - *Acer* spp. ($n=73$): $a = -0.40$, $b = 200$, $c = 22.30$, $d = 65.58$
- **DBH-to-height allometry:** Tree height ($H$, $\text{m}$) follows a modified Mund (2004) power formulation:
  $$H = 1.3 + \left(\frac{\text{DBH}}{a + b \cdot \text{DBH}}\right)^3$$
  Parameter values fitted:
  - *Fagus sylvatica*: $a = 1.649$, $b = 0.285$
  - *Carpinus betulus*: $a = 1.538$, $b = 0.311$
  - *Tilia* spp.: $a = 1.354$, $b = 0.306$
  - *Acer* spp.: $a = 1.564$, $b = 0.304$
- **Proxy species assignments:** Beech parameters are applied to oak (*Quercus robur*) and ash (*Fraxinus excelsior*); lime (*Tilia* spp.) parameters are applied to all other deciduous species.
- **Canopy shading and recruitment:** Recruitment thresholds (trees crossing $1.3\text{ m}$ height per ha/year) vary under open canopy ($\text{shading} < 1$) versus closed canopy ($\text{shading} \ge 1$), where shading is defined as $\sum \text{crown area} / 400\text{ m}^2$.

## Implications for our pipeline

- **Inversion for DBH estimation from drone CHM and segmentations:** [[project/pipeline-overview]] extracts tree height ($H$) from the [[concepts/canopy-height-model]] and crown projected area ($\text{CA}$) from segmented crown boundaries or bounding boxes (see [[concepts/crown-ownership]] and [[concepts/normal-forest]]). By inverting the DBH–height or DBH–crown area relationships, our post-detection downstream analysis can predict single-tree DBH for broadleaf stands without field calipers.
- **Species-conditioned allometric scaling:** Downstream classification by [[methods/dinov3-classification]] provides species labels (beech, maple, hornbeam, oak, ash, lime). This enables assigning the corresponding allometric equation parameters directly in tree-level GeoJSON export layers, advancing the [[concepts/tree-allometry]] framework.
- **Validation of crown boundaries:** Predicted crown areas from instance segmentation or local maxima ellipse estimations can be plausibly bounded using the height-derived DBH; discrepancies between predicted $\text{CA}$ and modeled $\text{ca}(\text{DBH}(H))$ can flag under-segmentation or over-segmentation.
- **Canopy layer assignment:** In dense mixed deciduous canopies, calculating canopy shading ratio per unit cell ($400\text{ m}^2$) helps differentiate dominant canopy crowns from suppressed understory trees, addressing [[concepts/understory-tree-detection]].

## Replication pseudocode

### Prerequisites

- Species classification per tree hypothesis (e.g., from [[methods/dinov3-classification]]).
- Observed tree top height $H$ ($\text{m}$) extracted from raster [[concepts/canopy-height-model]] (or segmented crown area $\text{CA}_{\text{obs}}$ in $\text{m}^2$).
- Fitted parameter dictionary for target taxa.

### Procedure

```text
# Estimating DBH and expected crown area from CHM tree height

1. Define species parameter lookup table:
   PARAMS_HEIGHT = {
       "Fagus sylvatica": {"a": 1.649, "b": 0.285},
       "Carpinus betulus": {"a": 1.538, "b": 0.311},
       "Tilia":            {"a": 1.354, "b": 0.306},
       "Acer":             {"a": 1.564, "b": 0.304},
       "Quercus robur":    {"a": 1.649, "b": 0.285}, # Beech proxy
       "Fraxinus excelsior":{"a": 1.649, "b": 0.285}  # Beech proxy
   }
   
   PARAMS_CROWN = {
       "Fagus sylvatica": {"a": 10.31, "b": 250.0, "c": 18.06, "d": 77.06},
       "Carpinus betulus": {"a": -29.13, "b": 200.0, "c": 26.56, "d": 46.54},
       "Tilia":            {"a": -0.50,  "b": 200.0, "c": 19.00, "d": 64.93},
       "Acer":             {"a": -0.40,  "b": 200.0, "c": 22.30, "d": 65.58}
   }

2. For each detected tree hypothesis with height H (m) > 1.3 and predicted species:
   a. Retrieve {a, b} from PARAMS_HEIGHT for species (fallback to Tilia if missing).
   b. Invert Mund equation:
      # H = 1.3 + (DBH / (a + b * DBH))^3
      # (H - 1.3)^(1/3) = DBH / (a + b * DBH)
      Y = (H - 1.3) ** (1.0 / 3.0)
      DBH_est = (a * Y) / (1.0 - b * Y)

   c. Retrieve {a_c, b_c, c_c, d_c} from PARAMS_CROWN for species.
   d. Compute expected crown area ca_expected (m²):
      denom = 1.0 + exp((c_c - DBH_est) / d_c)
      ca_expected = (a_c / denom) + (b_c / denom)
      
   e. Compare ca_expected against segmented polygon area CA_obs:
      ratio = CA_obs / ca_expected
      Flag as potential merge/split artifact if ratio outside plausible threshold [TBD].
```

### Gaps / not specified in paper

- **Inversion stability:** The equation $H = 1.3 + (\text{DBH} / (a + b \cdot \text{DBH}))^3$ has an asymptote at $H_{\max} = 1.3 + (1/b)^3$ (e.g. for beech, $b = 0.285 \implies H \approx 44.4\text{ m}$). Heights observed in the CHM above this asymptote cannot be inverted for DBH without numerical clamping.
- **Crown area formula simplification:** In the printed text (p. 2), the double logistic equation is written with identical denominators in both terms: $\text{ca} = \frac{a}{1+\exp((c-\text{dbh})/d)} + \frac{b}{1+\exp((c-\text{dbh})/d)} = \frac{a+b}{1+\exp((c-\text{dbh})/d)}$. The paper does not clarify whether this was a typographic reduction of a two-stage logistic function or intentional parameter separation.
- **Understory detection validity:** The relationships were fitted on measured trees from Weberstedter Holz; their behavior for heavily suppressed or stunted sub-canopy trees in dense stands is not separately parameterized.

## Quotes

- *On dataset and species fitting (p. 2):* "We estimated these allometric relationships based on data on height, crown projected area and dbh from 1,316 trees in the Weberstedter Holz (Fleck et al., 2011; Holzwarth et al., 2015). For beech (Fagus sylvatica) and hornbeam (Carpinus betulus), we fit species-specific relationships based on data from 842 and 35 trees, respectively."
- *On species proxy assignment (p. 2):* "We used the parameters for beech (Fagus sylvatica) also to estimate height and crown areas of oak (Quercus robur) and ash (Fraxinus excelsior) trees and the parameters for lime (Tilia spp.) to estimate height and crown areas of all other species."
- *On diameter–height form (p. 3):* "Allometric equations for dbh - height relationships were estimated based on the form (adapted from Mund 2004): $H = 1.3 + \left(\frac{dbh}{a+ b \cdot dbh}\right)^3$"

## Related pages

- [[concepts/tree-allometry]] — Core concepts for single-tree allometric modeling (DBH, height, crown projection, volume).
- [[concepts/site-index-and-yield]] — Stand-level yield capacity and dominant height reference concepts.
- [[concepts/canopy-height-model]] — Source layer for extracting individual tree top height $H$.
- [[concepts/normal-forest]] — Application scope for individual crown segmentation in merchantable/mature stands.
- [[concepts/understory-tree-detection]] — Shading and canopy layer dynamics affecting understory detection.
- [[project/pipeline-overview]] — Forest area analysis workflow integrating detection, classification, and metric extraction.
