---
title: "Technical Specification for the Biomass Equations Developed for the 2011 Forecast"
type: Source
tags: [biomass, allometry, crown-biomass, root-biomass, dbh, mensuration]
status: stable
updated: 2026-10-24
description: "Forestry Commission mensuration specification defining DBH-driven power and linear piecewise equations for crown and root biomass across British tree species."
source_file: raw/papers/revised-biomass-equations-27jan2014.pdf
authors:
  - Tim Randle
  - Robert Matthews
  - Tom Jenkins
year: 2014
replication_status: full
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/revised-biomass-equations-27jan2014.pdf
    title: "Technical Specification for the Biomass Equations Developed for the 2011 Forecast"
---

# Technical Specification for the Biomass Equations Developed for the 2011 Forecast

## Summary

This technical specification details revised allometric equations developed by Forest Research (Mensuration branch) for estimating the crown and root biomass (in oven-dry tonnes, ODT) of tree species grown in Great Britain. The revisions address known issues in legacy equations that substantially overestimated the biomass of larger mature trees.

All equations operate strictly as piecewise functions of stem diameter at breast height (DBH, measured at 1.3 m). Crown biomass is separated across three DBH tiers: below 7 cm (total above-ground biomass including small stem), 7 cm to 50 cm (power function of DBH excluding merchantable stem volume), and above 50 cm (linear function of DBH to prevent runaway power estimates). Root biomass is calculated across two tiers: DBH $\le$ 30 cm (power function with fixed exponent 2.5) and DBH > 30 cm (linear function). Comprehensive lookup tables map over 80 broadleaf and conifer taxa onto calibrated species groups.

## Key claims

- **Correction of overestimation:** Legacy power models produced unrealistically high crown and root biomass for mature stands; piecewise formulation with linear transitions for large trees stabilizes estimates (p. 2).
- **Sub-merchantable integration (< 7 cm DBH):** Because stems below 7 cm DBH are non-merchantable in standard British mensuration (Forest Yield / M1), the equation below 7 cm estimates total above-ground biomass (stem + branches + foliage) (p. 2).
- **Merchantable separation (7–50 cm & > 50 cm DBH):** Equations for stems $\ge$ 7 cm DBH estimate only crown biomass (tip, branches, twigs, and foliage), deliberately excluding the merchantable stem volume (pp. 3–4).
- **Root biomass partitioning:** Root biomass equations estimate total below-ground biomass (undifferentiated coarse and fine roots) in oven-dry tonnes (pp. 4–5).
- **Species grouping and mapping:** Due to limited empirical calibration data across all species, calibration was performed on core species clusters, and uncalibrated taxa are systematically mapped to groups based on silvicultural/morphological similarity (pp. 6–10).

## Implications for our pipeline

- **Downstream yield and carbon estimation:** While [[project/pipeline-overview]] outputs 2D crown detections and [[methods/dinov3-classification]] assigns species labels, turning segmented trees into carbon or biomass metrics requires allometric translation via [[concepts/site-index-and-yield]].
- **DBH inference dependency:** The equations require DBH in cm. When extracting tree features from UAV photogrammetry / [[concepts/canopy-height-model]], DBH must either be predicted indirectly from crown area and height (allometry) or measured via point cloud stem fitting ([[concepts/direct-stem-dbh-point-cloud]]).
- **Separation of stem and crown:** In standing drone surveys, CHM volume encompasses crown plus stem. To calculate total tree biomass for trees $\ge$ 7 cm DBH, crown biomass from these tables must be combined with merchantable stem volume estimates (e.g., from Forest Yield or regional volume tariff tables).
- **Lookups by species:** Provides ready-to-use parameter tables for Scots pine, Corsican pine, Sitka spruce, Norway spruce, Douglas fir, larches, oak, beech, and birch once categorized by [[methods/dinov3-classification]].

## Replication pseudocode

### Prerequisites

- Species classification (e.g., mapped from [[methods/dinov3-classification]] to FC codes).
- Diameter at breast height ($DBH$, in cm, measured at 1.3 m).

### Procedure

```text
def calculate_tree_biomass(dbh_cm, species_name):
    # 1. Lookup species mappings (Tables 6 and 7)
    crown_group = map_species_to_crown_group(species_name)
    root_group = map_species_to_root_group(species_name)
    
    # 2. Compute Crown / Above-ground Biomass (oven-dry tonnes)
    if dbh_cm < 7.0:
        # Eq 1: Total above-ground biomass (including stem)
        # Above-ground biomass = b * (dbh ** p)
        b, p = get_table_1_params(crown_group)
        crown_or_agb = b * (dbh_cm ** p)
        is_total_agb = True
    elif 7.0 <= dbh_cm <= 50.0:
        # Eq 2: Crown biomass only (excluding merchantable stem)
        # Crown biomass = b * (dbh ** p)
        b, p = get_table_2_params(crown_group)
        crown_or_agb = b * (dbh_cm ** p)
        is_total_agb = False
    else: # dbh_cm > 50.0
        # Eq 3: Crown biomass linear model
        # Crown biomass = a + b * dbh
        a, b = get_table_3_params(crown_group)
        crown_or_agb = a + (b * dbh_cm)
        is_total_agb = False

    # 3. Compute Root Biomass (oven-dry tonnes)
    if dbh_cm <= 30.0:
        # Eq 4: Root biomass power model (exponent fixed to 2.5)
        # Root biomass = b * (dbh ** 2.5)
        b = get_table_4_params(root_group)
        root_biomass = b * (dbh_cm ** 2.5)
    else: # dbh_cm > 30.0
        # Eq 5: Root biomass linear model
        # Root biomass = a + b * dbh
        a, b = get_table_5_params(root_group)
        root_biomass = a + (b * dbh_cm)

    return {
        "crown_or_agb_odt": crown_or_agb,
        "is_total_agb": is_total_agb,
        "root_biomass_odt": root_biomass
    }
```

### Gaps / not specified in paper

- **Stem volume equations:** The paper explicitly omits merchantable stem volume equations for trees $\ge$ 7 cm DBH, directing users to external systems ("M1 and/or Forest Yield in the Forecast System").
- **Height and crown diameter inputs:** Equations do not include tree height ($H$) or crown radius as co-predictors; height variation within a DBH class is absorbed into average site calibration.
- **Empirical sample sizes:** The specific sample sizes, site conditions, and harvest plot locations used to fit parameters $a$, $b$, and $p$ are not documented in this specification document.

## Quotes

- **Motivation for revision:** *"Existing crown and root biomass equations overestimate the biomass content of larger trees. Revised equations have therefore been prepared for estimating the crown and root biomass, in oven-dry tonnes, of tree species grown in Great Britain."* (p. 2)
- **Definition of crown biomass:** *"Crown biomass includes the tip, branches, twigs and foliage."* (p. 2)
- **Sub-merchantable definition:** *"A tree of less than 7 cm dbh is assumed to contain no merchantable stem volume. The output of the crown biomass equation for trees of less than 7 cm dbh therefore incorporates the biomass, in oven-dry tonnes, contained in the tree stem in addition to the biomass contained in the crown (i.e. all above-ground tree biomass)."* (p. 2)
- **Merchantable stem exclusion:** *"The output of the crown biomass equation for trees between 7 cm and 50 cm dbh gives an estimate of the biomass, in oven-dry tonnes, contained in the above-ground parts of the tree, excluding the merchantable tree stem biomass (i.e. excluding the part of the stem accounted for in M1 and/or Forest Yield in the Forecast System)."* (p. 3)
- **Root definition:** *"The output of the root biomass equation... estimates the total biomass, in oven-dry tonnes, contained in tree roots (i.e. not differentiated into biomass estimates of coarse and fine roots)."* (p. 4)

## Related pages

- [[concepts/site-index-and-yield]] — Stand yield, dominant height, and volume forecasting context.
- [[concepts/direct-stem-dbh-point-cloud]] — Direct 3D measurement of DBH required to feed these biomass equations.
- [[methods/dinov3-classification]] — Upstream classification pipeline that maps crowns to species codes.
- [[project/pipeline-overview]] — Operational workflow from drone data to tree-level attributes.
