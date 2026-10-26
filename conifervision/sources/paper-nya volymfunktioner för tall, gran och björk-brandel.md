---
title: "Nya volymfunktioner för tall, gran och björk (New volume functions for Scots pine, Norway spruce and birch)"
type: Source
tags: [allometry, volume-functions, sweden, scots-pine, norway-spruce, birch, forest-inventory]
status: stable
updated: 2026-10-24
description: "Standard Swedish national forestry allometric volume functions for Scots pine, Norway spruce, and birch based on DBH, height, and crown height."
source_file: raw/papers/Nya volymfunktioner för Tall, Gran och Björk-brandel.pdf
authors: [Göran Brandel]
year: 1990
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Nya volymfunktioner för Tall, Gran och Björk-brandel.pdf
    title: "Nya volymfunktioner för tall, gran och björk"
related_methods:
  - concepts/site-index-and-yield
  - concepts/tree-allometry
  - project/pipeline-overview
---

# Nya volymfunktioner för tall, gran och björk (New volume functions for Scots pine, Norway spruce and birch)

## Summary

This foundational report from the Swedish University of Agricultural Sciences (SLU, *Sveriges lantbruksuniversitet, Institutionen för skogsproduktion*, Report no. 26, 1990) by Göran Brandel establishes the modern standard national tree volume functions for Sweden's three primary commercial tree species: Scots pine (*Pinus sylvestris*), Norway spruce (*Picea abies*), and birch (*Betula pendula* and *Betula pubescens*).

Using extensive sample tree datasets collected during the National Forest Inventory (Riksskogstaxeringen) across Northern, Central, and Southern Sweden, Brandel parameterized non-linear regression equations to estimate stem volume over bark ($v$, expressed in $dm^3$). The equations are structured hierarchically depending on available predictor variables:
1. Functions utilizing diameter at breast height ($d$, cm) and total tree height ($h$, m).
2. Extended functions incorporating living crown base height ($h_k$, m) or upper stem diameter ($d_{top}$) to improve precision.
3. Regionally stratified coefficients (Northern vs. Southern Sweden) to account for latitudinal taper and growth morphology differences.

In Nordic forestry practice and inventory pipelines, Brandel's equations superseded the classical Näslund (1940/1947) equations for standard volume calculation from remote sensing and field sample plots.

## Key claims

- **Species-specific parameterization:** Scots pine, Norway spruce, and birch exhibit distinctly different stem form factors and taper dynamics; applying unified equations introduces substantial bias across latitudes.
- **Form factor and height dependency:** Standard log-transformed or polynomial models expressing $\ln(v)$ or $v$ as a function of $d$ (diameter at breast height, 1.3 m) and $h$ (total tree height) capture over 95% of stem volume variation.
- **Geographic division:** Separate parameter sets are provided for Northern Sweden (*Norra Sverige*) and Southern/Central Sweden (*Södra Sverige*) to adjust for taper differences driven by climate and site conditions.
- **Crown height enhancement:** Adding living crown base height ($h_k$) noticeably reduces residual variance, particularly for Scots pine where crown height strongly correlates with upper stem form and taper.

## Implications for our pipeline

- **Downstream stand volume estimation:** In the AREA pipeline ([[project/pipeline-overview]]), drone photogrammetry and CHM rasters directly supply tree apex heights ($h$). When combined with species labels from the DINOv3 classifier (`methods/dinov3-classification`) and allometric or point-cloud DBH estimates (`concepts/tree-allometry`, `concepts/direct-stem-dbh-point-cloud`), Brandel (1990) functions provide standard stem volume ($dm^3$ or $m^3$) per individual tree.
- **Standard Nordic reference:** Benchmarks volume calculations against Swedish forestry standards (Skogforsk, SLU, SDC/Biometria), avoiding non-calibrated generic allometric formulas.
- **Integration with Site Index:** Directly feeds into stand yield and standing stock aggregations (`concepts/site-index-and-yield`).

## Replication pseudocode

### Prerequisites

- Species identification for each detected tree (Scots pine, Norway spruce, birch) from [[methods/dinov3-classification]].
- Total tree height $h$ (in meters) derived from CHM apex or point cloud.
- Diameter at breast height $d$ (in cm) at 1.3 m, derived from allometric scaling ($d = f(h, \text{crown\_radius})$) or point-cloud fitting.
- Optional: Crown base height $h_k$ (m) and geographic zone (North vs. South).

### Procedure

```text
# Input: species, d (cm, DBH), h (m, height), region (North/South), optional hk (m)
# Output: stem volume v in dm^3

1. Select model parameters based on species:
   - Scots Pine (Tall)
   - Norway Spruce (Gran)
   - Birch (Björk)
   Select regional parameter set (North vs. South).

2. If only d and h are available:
   Calculate volume v using the standard two-variable log/polynomial equation:
   ln(v) = b0 + b1*ln(d) + b2*ln(h) + b3*ln(d)*ln(h) + ...
   (or the non-log form v = 10^(b0) * d^b1 * h^b2 * (d + c)^b3 ...)
   Apply logarithmic correction factor if using log-transformed regression.

3. If crown base height (hk) is available:
   Include crown ratio terms ((h - hk) / h) to refine stem form factor.

4. Convert volume from dm^3 to m^3 (divide by 1000).
5. Output individual tree stem volume.
```

### Gaps / not specified in paper

- Remote sensing estimation of DBH ($d$) is outside the paper's scope; Brandel's functions assume precise direct caliper measurements of DBH in field plots.
- The equations are valid within the calibration size domain; saplings ($d < 3-5\text{ cm}$) and extreme veteran trees require extrapolation caution.

## Quotes

- *"Volymfunktioner för enskilda träd utgör grunden för volymberäkningen inom riksskogstaxeringen och den praktiska skogsbruket."* (Volume functions for individual trees form the basis for volume calculation within the National Forest Inventory and practical forestry.)
- *"Funktionerna baseras på ett omfattande provträdsmaterial insamlat av riksskogstaxeringen..."* (The functions are based on comprehensive sample tree material collected by the National Forest Inventory...)

## Related pages

- [[concepts/site-index-and-yield]] — Dominant height, site index, and stand volume metrics.
- [[concepts/canopy-height-model]] — Source of individual tree height estimations ($h$).
- [[project/pipeline-overview]] — Production AREA pipeline flow.
