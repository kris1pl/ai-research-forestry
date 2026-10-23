---
title: "Allometric Relationships of Selected European Tree Species"
type: Source
tags: [allometry, crown-shape, tree-architecture, radiative-transfer, biometrics, biomass]
status: stable
updated: 2026-10-21
description: "Compendium of allometric equations for crown radius, tree height, crown base height, LAI, and biomass for five European commercial species (birch, beech, larch, Norway spruce, Scots pine)."
source_file: raw/papers/allometric relationships of selected european tree-gp_eudor_PDFA1B_EUNA20855ENC_001.pdf
authors:
  - Jean-Luc Widlowski
  - Michel Verstraete
  - Bernard Pinty
  - Nadine Gobron
year: 2003
replication_status: direct
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/allometric relationships of selected european tree-gp_eudor_PDFA1B_EUNA20855ENC_001.pdf
    title: "Allometric Relationships of Selected European Tree Species: Parametrizations of tree architecture for the purpose of 3-D canopy reflectance models used in the interpretation of remote sensing data"
---

# Allometric Relationships of Selected European Tree Species

## Summary

This European Commission Joint Research Centre (JRC) report compiles empirical allometric equations and architectural parameterizations for five key European tree species: European beech (*Fagus sylvatica*), birch (*Betula pubescens* and *Betula pendula*), European larch (*Larix decidua*), Norway spruce (*Picea abies*), and Scots pine (*Pinus sylvestris*).

Designed to support realistic 3D radiation transfer simulations (e.g., Raytran) and look-up-table (LUT) inversion schemes for satellite and airborne remote sensing, the report gathers equations linking trunk diameter at breast height ($DBH$) to tree height ($H$), height to crown base ($H_t$), height to maximum crown width ($H_{cr}$), maximum crown radius ($C_r$), bottom crown radius ($R_c$), Leaf Area Index ($LAI$), and above-ground biomass components ($W_s, W_b, W_f, W_t$). It also synthesizes general canopy architecture principles, such as crown geometrical primitives, leaf normal distributions (LND), vertical foliage profiles, interior foliage-free dead zones, and stem spatial distributions.

## Key claims

- **Parametrization from DBH and H:** Individual tree geometry can be largely parameterized using $DBH$ as the driving variable, or inverted from height $H$ to predict crown dimensions.
- **Geometric primitives for crown envelopes:**
  - *Birch:* Obloid top connected to a hemispherical base via a central cylinder.
  - *European Beech:* Hemispherical top joined to a conical bottom at $H_{cr}$ ($H_{cr} \approx H_t + \frac{3}{5}H_c$).
  - *European Larch:* Two conical elements touching at their bases ($H_{cr} \approx H_t + \frac{1}{3}H_c$).
  - *Norway Spruce:* Two conical elements meeting at maximum width ($H_{cr} = H_t + \frac{1}{3}H_c$, with $R_c \approx C_r / 2$).
  - *Scots Pine:* Two conical elements meeting at maximum width ($H_{cr} = H_t + \frac{1}{2}H_c$, with $R_c \approx C_r / 3$).
- **Crown radius ($C_r$) relationships:**
  - *Norway spruce:* Linear model $C_r = 0.6122 + 0.0536 \cdot DBH$ (Nagel et al., 2002) or exponential formulation from SILVA (Pretzsch et al., 2002):
    $$C_r = \frac{1}{2} \exp\left(-0.2195 + 0.2545 \ln(DBH) + 0.009 H - 0.6735 \ln\left(\frac{H}{DBH}\right)\right)$$
  - *Scots pine:* $C_r = \exp(-0.5515 + 0.6468 \ln(H) - 0.0062 H + 0.1904 \ln(DBH))$ (Pretzsch et al., 2002) or $C_r = \frac{1}{2}(0.641 DBH + 0.548)$ (Čermák et al., 1998).
- **Crown base height ($H_t$):** For both spruce and pine, relative crown height varies with stand density and competition; standard stand formulations (e.g., Pretzsch et al., 2002) predict $H_t$ as a function of total tree height $H$ and slenderness ($H/DBH$).
- **Foliage distribution:** Conifer foliage is strongly upward-skewed, peaking around 70–80% of crown height, with an inner foliage-free zone resulting from self-shading.
- **Spatial patterns:** Natural, unmanaged forest stands generally conform to a random Poisson distribution of stems, whereas managed plantations approach regular spacing, transitioning towards clustered distributions only under specific gap-phase disturbance dynamics.

## Implications for our pipeline

- **Prior constraints for crown delineation:** When segmenting individual tree crowns from drone orthophotos and [[concepts/canopy-height-model|CHM rasters]], the documented height-to-crown-radius ($H \leftrightarrow C_r$) ratios provide rigorous prior bounds. Outlines or bounding boxes that deviate significantly from species-specific empirical bounds can be flagged during validation or post-processing.
- **Ownership box scaling in normal forest:** Supports [[concepts/crown-ownership|crown ownership]] and [[concepts/normal-forest|normal forest]] logic by specifying expected lateral crown spread ($2 C_r$) for given CHM peak heights.
- **Biomass and yield estimation:** Directly provides the mathematical formulations needed to scale detected tree crowns and height measurements into merchantable stem volume, above-ground dry biomass, and standing timber yield (linking into [[concepts/site-index-and-yield|site index and yield]] workflows).
- **Synthetic scene generation & digital twins:** For forward-modeling photogrammetric point clouds or validation datasets, the geometric primitive equations and vertical foliage profiles enable realistic 3D tree crown reconstruction.

## Replication pseudocode

### Prerequisites

- Species classification label (e.g., from [[methods/dinov3-classification|DINOv3]] or field call: spruce, pine, birch, beech, larch).
- Observed tree top height ($H$) from CHM / local maxima.
- (Optional) Estimated or inverted $DBH$ in cm.

### Procedure

```text
# Estimating crown envelope and biomass from height and species
1. Given species and measured top height H (meters):
   a. Invert species height curve to solve for DBH:
      - For Norway spruce (Kindermann 1998):
        solve H = 1.3 + (DBH / (0.165 + 0.030 * DBH))^2 for DBH
      - Or for Scots pine (Čermák et al. 1998):
        DBH = -14.4 * ln(1 - (H / 24.8)^(1 / 0.758))

2. Calculate maximum crown radius (Cr) and crown base height (Ht):
   - For Norway spruce:
     Ht = H * (1 - exp(0.537 - 0.781 * (H / DBH) - 0.015 * DBH))
     Cr = 0.5 * exp(-0.2195 + 0.2545*ln(DBH) + 0.009*H - 0.6735*ln(H / DBH))
     Hcr = Ht + (H - Ht) / 3.0
     Rc = Cr / 2.0
   - For Scots pine:
     Ht = H * (1 - exp(0.376 - 0.9963 * (H / DBH) - 0.0218 * DBH))
     Cr = exp(-0.5515 + 0.6468*ln(H) - 0.0062*H + 0.1904*ln(DBH))
     Hcr = Ht + (H - Ht) / 2.0
     Rc = Cr / 3.0

3. Compute expected vertically downward projected crown diameter (CD = 2 * Cr):
   - Compare CD with predicted bounding box width from DEIMv2 / edge segmentation.
   - If predicted crown box width deviates by > TBD_TOLERANCE from CD, mark for audit.

4. Compute tree dry biomass (Wt):
   - For spruce: Wt = 0.105196 * DBH^2.310 + 0.011350 * DBH^2.570 + 0.027669 * DBH^2.226 + 0.029174 * DBH^2.292
   - For pine: Wt = 0.0943 * DBH^2 - 0.950
```

### Gaps / not specified in paper

- **Dense stand suppression:** The paper notes that dense stands alter the crown ratio drastically ($H_t$ approaches $H$ under competition), but does not provide dynamic, continuous density-dependent modifier functions across all species.
- **Inversion instability:** Inverting empirical non-linear height equations (such as asymptotic exponential forms) becomes ill-conditioned near asymptotic heights ($H_{max}$).
- **Stem defect rates:** Dead wood and snag fractions are reported broadly (10–18% of stems), but local decay class transitions are not parameterized.

## Quotes

- **Scope and modeling premise:** *"The purpose of this document is thus to compile allometric relationships, that are based on field observations and that describe the structural properties of an individual tree, for the subsequent generation of credible surface structure solutions (forest canopies) over spatial scales that are comparable to the IFOV of most current medium spatial resolution instruments."* (p. 3)
- **Primary structural variable:** *"In traditional forestry most structural properties, like tree height, crown width, crown length, etc, have been related by allometric relationships to an easily measurable primary variable. In most cases this variable is the Diameter-at-Breast-Height, DBH..."* (p. 3–4)
- **Norway spruce crown shape:** *"The crown shape of the Norway spruce is predominantly conical, with broad crowns occurring in lower altitudes of central Europe and tall and pointy crowns at higher elevations or further to the north. Pretzsch (1992) represents the crown shape of the Norway Spruce using two conical elements..."* (p. 30)
- **Scots pine crown morphology:** *"As the trees mature the crown form often becomes more rounded because elongation of the main stem is reduced relative to the laterals... represented using two conical elements, as outlined by Pretzsch (1992)..."* (p. 38)

## Related pages

- [[project/pipeline-overview]]
- [[concepts/canopy-height-model]]
- [[concepts/normal-forest]]
- [[concepts/crown-ownership]]
- [[concepts/site-index-and-yield]]
- [[methods/dinov3-classification]]
