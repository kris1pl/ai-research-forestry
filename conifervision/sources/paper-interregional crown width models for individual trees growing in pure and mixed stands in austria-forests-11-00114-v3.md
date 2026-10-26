---
type: Source
title: "Interregional Crown Width Models for Individual Trees Growing in Pure and Mixed Stands in Austria"
description: "Linear mixed-effects crown width models incorporating DBH, height, crown ratio, site physiography, and species admixture proportions based on Austrian NFI data."
tags: [allometry, crown-width, mixed-stands, national-forest-inventory, austria, linear-mixed-effects]
status: stable
updated: 2026-10-24
source_file: raw/papers/Interregional Crown Width Models for Individual Trees Growing in Pure and Mixed Stands in Austria-forests-11-00114-v3.pdf
authors:
  - Rafael Buchacher
  - Thomas Ledermann
year: 2020
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Interregional Crown Width Models for Individual Trees Growing in Pure and Mixed Stands in Austria-forests-11-00114-v3.pdf
    title: "Interregional Crown Width Models for Individual Trees Growing in Pure and Mixed Stands in Austria"
related_methods:
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/merge-detections
  - methods/dinov3-classification
---

# Interregional Crown Width Models for Individual Trees Growing in Pure and Mixed Stands in Austria

## Summary

Buchacher and Ledermann develop species-specific and generic linear mixed-effects crown width ($CW$) models for the major commercial and minor tree species across Austria. Using Austrian National Forest Inventory (ANFI) field data comprising ~8,900 measured tree crowns across 1,508 sample plots, the authors model crown diameter as a function of individual tree dimensions ($DBH$, height $H$, crown ratio $CR$, slenderness $H/D$), site descriptors (elevation, slope, aspect via Stage's transformation, and 21 growth regions), and stand species mixture. Stand composition is parameterized via relative proportions of basal area ($PS$) overall or restricted to the subject tree's crown layer ($PSL$).

The resulting models demonstrate that shade-tolerant species (such as *Picea abies* and *Abies alba*) generally increase crown width when mixed with other species (intraspecific competition restricts crown size more than interspecific competition), whereas light-demanding species (*Larix decidua*, *Pinus sylvestris*, *Quercus* spp.) exhibit smaller crown widths when mixed with shade-tolerant competitors. Conifers show less plastic crown width responses to species mixing than broadleaves.

## Key claims

1. **Tree crown width variation:** Individual crown width is strongly governed by tree size ($DBH$), but past competitive status ($CR$, $H/D$) and site factors (elevation, slope, aspect) significantly modulate the relationship across ecoregions.
2. **Species admixture impact:** Crown width models that incorporate species basal area proportions ($PS$ or layer-specific $PSL$) account for crown plasticity in mixed stands. Conifers show conditional $R^2$ between 0.72 and 0.83; broadleaves reach conditional $R^2$ between 0.76 and 0.86.
3. **Shade tolerance vs. crown plasticity:** Shade-tolerant species (*Picea abies*, *Abies alba*, *Fagus sylvatica*) react positively to admixture with wider crowns, whereas light-demanding species (*Larix decidua*, *Pinus sylvestris*, *Quercus* spp.) contract their crowns under competition with shade-tolerant neighbors.
4. **Broadleaf vs. conifer crown plasticity:** Broadleaf species respond more strongly to neighbor composition changes than conifers, driven by greater lateral branch plasticity and asymmetric crown expansion.
5. **Static competition representation:** Inclusion of past competition metrics ($CR$, $H/D$) renders distance-dependent or instantaneous stand density indices ($SDI$) redundant when predicting static crown width.

## Implications for our pipeline

- **Priors for Detection & Bounding Box Size:** [[methods/chm-detection]] and [[methods/deimv2-canopy]] rely on spatial size priors or anchor definitions. Understanding that crown width scales non-linearly with $DBH$ and height allows setting species- and elevation-aware upper and lower bounds on segmented crown areas in [[concepts/normal-forest]].
- **Over-segmentation / Under-segmentation Validation:** In [[concepts/crown-ownership]] and post-detection filtering, crown widths derived from remote sensing heights and classified species (via [[methods/dinov3-classification]]) can be sanity-checked against empirical $CW$ distributions predicted by these models.
- **Biomass and Volume Estimation from Remote Sensing:** Once crowns are delineated and height is derived from [[concepts/canopy-height-model]], allometric inversion can estimate $DBH$ from remote-sensed $CW$ and $H$, directly feeding stand inventory and yield tables in [[concepts/site-index-and-yield]].
- **Mixed Stand Canopy Packing:** In dense mixed forests, crowns interlock differently than in monocultures; segmentation post-processing must accommodate broader beech or spruce crowns when admixed, as opposed to pure stands.

## Replication pseudocode

### Prerequisites

- Tree species classification $SP$ (e.g. from [[methods/dinov3-classification]])
- Stem diameter at breast height $DBH$ (cm), total tree height $H$ (m), and height of crown base $HCB$ (m)
- Terrain parameters: elevation ($ELEV$ in hectometres, i.e., $m / 100$), slope gradient ($SL$, percentage), azimuth of aspect ($EXP$, radians)
- Geographic growth region ID (1–21 per Jelem & Kilian 1972)
- Stand species composition: relative basal area proportions ($PS_x$ or crown-layer specific $PSL_x$)

### Procedure

```text
# Crown width estimation procedure following Buchacher & Ledermann (2020)

function predict_crown_width(species, DBH, H, HCB, ELEV_hm, SL_pct, EXP_rad, region_id, basal_area_shares):
    # 1. Compute allometric indices
    CR = 1.0 - (HCB / H)
    HD_ratio = (H * 100.0) / DBH  # H in cm / DBH in cm

    # 2. Evaluate model form and parameters based on species code (Tables 3 & 5)
    match species:
        case "Picea_abies":
            # Log-linear formulation (Eq. 3)
            eta = 0.052386 + 0.486831 * ln(DBH) - 0.0031566 * HD_ratio
            eta += 0.6153011 * CR - 0.2123078 * (CR^2)
            
            # Elevation & DBH interactions
            eta += (0.0003257 * ELEV_hm * DBH) - (0.0014439 * (ELEV_hm^2)) - (0.0000151 * (ELEV_hm^2) * DBH)
            
            # Aspect & Slope (Stage's transformation)
            eta += (-0.0001333 * cos(EXP_rad) * SL_pct) + (0.0002676 * sin(EXP_rad) * SL_pct)
            
            # Regional dummies
            if region_id == 6:
                eta += -0.4215087 + (0.1416563 * ln(DBH))
            elif region_id in [11, 12, 15, 18]:
                eta += 0.046185
            elif region_id == 13:
                eta += 0.0193874 * ln(DBH)
                
            # Species composition effects (relative proportions of basal area)
            ps_spruce = basal_area_shares.get("Picea_abies", 0.0)
            ps_pine_larch = basal_area_shares.get("Pinus_Larix", 0.0)
            ps_beech = basal_area_shares.get("Fagus_sylvatica", 0.0)
            
            eta += -0.1657646 * sqrt(ps_spruce)
            eta += 0.0112108 * sqrt(ps_spruce) * ELEV_hm
            eta += 0.0046689 * sqrt(ps_pine_larch) * ELEV_hm
            eta += -0.0058753 * sqrt(ps_beech) * ELEV_hm
            
            CW = exp(eta)

        case "Pinus_sylvestris":
            # Linear formulation (Eq. 2)
            CW = 3.7155099 + 0.0898499 * DBH - 0.3717171 * sqrt(HD_ratio) + 3.0042626 * sqrt(CR)
            if region_id == 19:
                CW += 0.0194008 * DBH
            elif region_id == 20:
                CW += 0.0130925 * DBH
                
            # Layer-specific spruce proportion interaction
            psl_spruce = basal_area_shares.get("PSL_Picea_abies", 0.0)
            CW += -0.0911981 * (psl_spruce^2) * ELEV_hm

        case "Fagus_sylvatica":
            # Broadleaf log-linear formulation
            eta = 1.0910323 + 0.4036294 * ln(DBH) - 0.0029587 * HD_ratio + 0.1684201 * ln(CR)
            eta += -0.000946 * (ELEV_hm^2)
            eta += (0.00073 * cos(EXP_rad) * SL_pct) + (0.0005842 * sin(EXP_rad) * SL_pct)
            
            if region_id == 9:
                eta += -0.5924605 + 0.1551168 * ln(DBH)
            elif region_id == 10:
                eta += -0.5657388 + 0.1305651 * ln(DBH)
                
            # Admixture effects (PSL)
            eta += 0.1809567 * basal_area_shares.get("PSL_Picea_abies", 0.0)
            eta += 0.5235613 * (basal_area_shares.get("PSL_Abies_alba", 0.0)^2)
            eta += 0.6546167 * (basal_area_shares.get("PSL_Quercus", 0.0)^2)
            eta += 0.0485298 * (basal_area_shares.get("PSL_Pinus_sylvestris", 0.0)^2) * ELEV_hm
            eta += 0.0118516 * (basal_area_shares.get("PSL_Fagus_sylvatica", 0.0)^2) * ELEV_hm
            
            CW = exp(eta)

        case _:
            # Fall back to generic conifer or generic broadleaf models (Tables 3 & 5)
            CW = evaluate_generic_model(species, DBH, CR, HD_ratio, ELEV_hm, SL_pct, EXP_rad, region_id)

    return CW
```

### Gaps / not specified in paper

- **Inversion to predict DBH from CW:** The paper focuses exclusively on predicting $CW$ from $DBH$ and height; solving in reverse requires numerical root finding or refitting models with $DBH$ as the dependent variable.
- **Application to drone-only data:** In drone orthophoto pipelines, $HCB$ and crown ratio ($CR$) are difficult to extract without dense sub-canopy LiDAR returns; for photogrammetric CHMs, default species $CR$ priors must be assumed.
- **Independent Validation:** As noted by the authors, independent validation datasets from mixed forests were unavailable during model fitting (evaluation relies entirely on internal mixed-effects metrics).

## Quotes

- *Page 1:* "The crown widths of shade-tolerant species reacted mainly positively to admixture, whereas light-demanding species reacted with decreasing crown widths. Coniferous species were not as strongly affected by mixture as broadleaf species."
- *Page 3:* "Crown width (CW) was calculated by doubling the quadratic mean of the 4 measurement values per tree."
- *Page 12:* "Competition (density) measures, independent whether they are stand based or individual-tree based, distance-dependent or distance-independent, quantify the current competition load of the trees while crown parameters (CR) and tree size (DBH, H) characterize the competition that a tree had experienced in the past."
- *Page 13:* "The comparison of our CW models for broadleaf and coniferous tree species shows that broadleaf trees generally reacted stronger to a change in species composition. A possible reason is that broadleaf trees have more plastic crowns and can react with more asymmetric crown shapes to the neighboring trees."

## Related pages

- [[project/pipeline-overview]] — production pipeline where AI detections are mapped to tree-level attributes
- [[concepts/normal-forest]] — target stand structure where crown dimensions correlate with tree size
- [[concepts/crown-ownership]] — criteria for assigning horizontal crown extents to detected tree stems
- [[concepts/canopy-height-model]] — source for tree height measurements used in allometric formulations
- [[concepts/site-index-and-yield]] — stand-level metrics linking tree dimensions to volume and yield
- [[methods/dinov3-classification]] — upstream species identification enabling species-specific allometric equations
