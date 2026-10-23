---
type: Source
title: "Biomass and stem volume equations for tree species in Europe"
description: "Comprehensive European meta-compilation of 607 tree biomass and 230 stem volume allometric equations across 55 species."
tags: [allometry, biomass, stem-volume, carbon-accounting, europe, inventory]
status: stable
updated: 2026-10-21
source_file: raw/papers/Biomass and stem volume_951-40-1984-9.pdf
authors:
  - "Dimitris Zianis"
  - "Petteri Muukkonen"
  - "Raisa Mäkipää"
  - "Maurizio Mencuccini"
year: 2005
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T17:35:00Z
sources:
  - id: primary
    resource: raw/papers/Biomass and stem volume_951-40-1984-9.pdf
    title: "Biomass and Stem Volume Equations for Tree Species in Europe"
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/dinov3-classification
---

# Biomass and Stem Volume Equations for Tree Species in Europe

## Summary

This monograph compiles and synthesizes empirical tree allometry equations across the European continent. It provides parameter values, mathematical formulations, sample sizes, and valid dimension ranges for 607 tree biomass equations (spanning 39 species) and 230 stem volume equations (covering 55 species). Explanatory variables are consistently diameter at breast height ($D$, measured at 1.3 m above ground) and/or tree height ($H$).

The monograph addresses methodological challenges in converting raw inventory metrics into biomass and carbon estimates, including logarithmic transformation bias (requiring Sprugel's correction factors), non-additivity of component models, multicollinearity between $D$ and $H$, and definitional discrepancies regarding merchantable versus total stem volume across European national forest inventories.

## Key claims

- **Compiled equation scale**: Assembles 607 biomass equations (aboveground, stem wood, stem bark, branches, foliage, roots) and 230 stem volume equations across European forestry literature (p. 7, 11).
- **Dominant model structures**: Most biomass models follow the linearized power relationship $\log(M) = A + B \times \log(D)$ (127 models), power functions $a \cdot D^b$, or combined height-diameter formulations such as $a \cdot D^b \cdot H^c$ and polynomial expansions (p. 7, 18–39).
- **Geographic and taxonomic imbalance**: Most equations represent coniferous species (*Picea abies* with 159 biomass models, *Pinus sylvestris* with 191 models) in Northern and Central Europe (Sweden, Finland, Germany), with sparse coverage in Southern/Mediterranean Europe (82 models) and limited root biomass data (p. 7–9).
- **Volume definition disparities**: Nordic equations generally estimate total stemwood from root collar to tip, whereas other European nations restrict volume to merchantable stem wood up to a top diameter limit (e.g., 7 cm), rendering direct cross-regional aggregations biased without harmonized expansion factors (p. 11, 14).
- **Transformation and additivity issues**: Applying log-transformed regressions induces systematic underestimation unless corrected by Sprugel's correction factor ($CF = \exp(SEE^2 / 2)$), and separate component regressions often fail additivity checks against total aboveground equations (p. 14–15).

## Implications for our pipeline

- **Downstream tree product attribution**: Bridges the gap from individual tree detections (crown location via [[methods/local-maxima]], crown dimensions via [[methods/chm-detection]], and species via [[methods/dinov3-classification]]) to per-tree stem volume and biomass estimation in [[project/pipeline-overview]].
- **Expansion of allometry concepts**: Complements [[concepts/site-index-and-yield]] by anchoring individual tree allometry ([[concepts/tree-allometry]]), connecting UAV-derived height ($H$) and inferred crown diameter/DBH directly to wood volume.
- **Biomass error awareness**: For pipeline reporting, species-specific biomass functions must be applied strictly within their documented $D$ and $H$ ranges (e.g., Marklund 1987/1988 functions for boreal Scots pine and Norway spruce) to avoid unbounded extrapolation errors.
- **Log-transformation bias corrections**: Any logarithmic allometric curve embedded in production reporting modules must include Sprugel's correction factor when predicting back to arithmetic scale.

## Replication pseudocode

### Prerequisites

- Tree species classification output (e.g., *Picea abies*, *Pinus sylvestris*, *Betula pendula*) from [[methods/dinov3-classification]].
- Tree height $H$ (in meters) extracted from [[concepts/canopy-height-model]].
- DBH ($D$, in cm) measured directly, or estimated from crown diameter via species-specific crown-width-to-DBH models.

### Procedure

```text
# Biomass and Stem Volume Estimation per Detected Tree

1. Load detected tree record:
   - species = detection.species
   - H = detection.height_m
   - D = detection.dbh_cm

2. Match species and regional domain to compiled equation set:
   - For Boreal / Nordic Scots pine:
       Marklund (1988) stem biomass:
         ln(ST) = a + b * [D / (D + 13)] + c * H + d * ln(H)
       Or Swedish stem volume (Appendix C, TBD species-specific formula):
         V = f(D, H)
   - For Norway spruce:
       Marklund (1987) aboveground biomass or stem biomass:
         ln(ST) = -2.2052 + 7.4361 * [D / (D + 14)] + 0.0186 * H + 0.7595 * ln(H)

3. Verify diameter and height validity ranges:
   - Assert D_min <= D <= D_max, else flag extrapolation warning.

4. Evaluate log-linear equation:
   - y_pred_log = a + b * [D / (D + param)] + c * H + d * ln(H)

5. Apply transformation bias correction (Sprugel 1983):
   - SEE = equation.standard_error_of_estimate
   - CF = exp((SEE^2) / 2)
   - ST_biomass_kg = exp(y_pred_log) * CF

6. Compute stem volume:
   - Evaluate species-specific volume function V = VolumeEquation(D, H)
   - Adjust for merchantable vs. total trunk definition (e.g., 7 cm top threshold).

7. Output tree-level metrics:
   - detection.stem_biomass_kg = ST_biomass_kg
   - detection.stem_volume_m3 = V
```

### Gaps / not specified in paper

- **Crown diameter to DBH regressions**: The paper focuses purely on $D$ (DBH) and $H$ (height). Remote sensing pipelines acquiring data from UAV photogrammetry typically measure crown spread or area rather than stem DBH; external crown-width-to-DBH models must be supplied.
- **Tabular error estimates**: Standard errors of parameter estimates (SEE) and Sprugel correction factors are omitted from the Appendix tables due to inconsistent reporting in primary publications (p. 6, 14–15).
- **Additive constraint enforcement**: Simultaneous estimation techniques (e.g., SUR) ensuring crown + stem + root = total biomass are discussed conceptually (Parresol 2001) but not harmonized across the compiled individual models.

## Quotes

- *"The vast majority of the reviewed biomass equations (127 in total) took the simple linear form Log (M) = A + B × Log(D)..."* (p. 7)
- *"However, there is no straightforward, commonly accepted definition for stem volume in Europe. In general, the volume of stemwood extending from root collar up to the top of the stems is accounted in the equations developed in the Nordic countries. For some of the reviewed regressions, the stem is the part of the main trunk up to a minimum diameter of 7 cm..."* (p. 11)
- *"It should be noticed that when a logarithmic or any other transformation is applied to the raw data, biomass and stem volume predictions are biased (Baskerville 1972, Sprugel 1983)."* (p. 15)
- *"Reliability of the national carbon inventories can be improved by applying biomass equations directly to tree-scale measurements of diameter (D)... Consequently, the additional source of error introduced by conversion or expansion factors can be avoided."* (p. 14)

## Related pages

- [[concepts/tree-allometry]] — Theoretical basis for individual-tree allometric power laws ($Y = a X^b$).
- [[concepts/site-index-and-yield]] — Stand-level dominant height, site fertility, and yield models.
- [[concepts/canopy-height-model]] — Photogrammetric source for per-tree height ($H$) inputs.
- [[methods/dinov3-classification]] — Upstream species attribution determining the applicable parameter set.
- [[project/pipeline-overview]] — Forest area analysis workflow integrating detection, classification, and volumetric valuation.
