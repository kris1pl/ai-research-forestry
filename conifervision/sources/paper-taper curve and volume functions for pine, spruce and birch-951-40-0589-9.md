---
title: "Taper Curve and Volume Functions for Pine, Spruce and Birch"
type: Source
tags: [allometry, taper-curve, volume-functions, scots-pine, norway-spruce, birch]
status: stable
updated: 2026-10-21
description: "Foundational Finnish national forest inventory models for stem taper curves and volume equations for pine, spruce, and birch across Finland."
source_file: raw/papers/TAPER CURVE AND VOLUME FUNCTIONS FOR PINE, SPRUCE AND BIRCH-951-40-0589-9.pdf
authors:
  - Jouko Laasasenaho
year: 1982
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/TAPER CURVE AND VOLUME FUNCTIONS FOR PINE, SPRUCE AND BIRCH-951-40-0589-9.pdf
    title: "Taper Curve and Volume Functions for Pine, Spruce and Birch"
---

# Taper Curve and Volume Functions for Pine, Spruce and Birch

## Summary

This work establishes the standard Finnish forest mensuration taper and volume equations developed by Jouko Laasasenaho for Scots pine (*Pinus sylvestris*), Norway spruce (*Picea abies*), and birch (*Betula pendula* and *B. pubescens*). Using representative sample datasets from National Forest Inventory (NFI) tracts across Finland comprising 2,326 pines, 1,864 spruces, and 863 birches, the study develops single-equation polynomial taper curves, simultaneous linear equation systems for predicting relative height diameters, and multiplicative logarithmic volume models conditioned on diameter at breast height ($d$), total tree height ($h$), and optional upper diameters ($d_6$).

## Key claims

- **Universal representation across Finland:** Representative sampling across roughly 100 nationwide NFI tracts enables unbiased volume and taper curves across diverse sites and age distributions.
- **Relative height standardization:** Taper variations across tree dimensions can be formulated through relative diameter ratios normalized to stem diameter at 20% of total height ($d_{0.2h}$).
- **Single-equation polynomial model:** A polynomial based on powers following Fibonacci sequence exponents effectively captures tree profiles from ground butt-swell through upper stems down to zero at tree tops.
- **Simultaneous equation modeling:** Diameters at arbitrary relative heights can be solved jointly via tridiagonal linear simultaneous equation systems with minimal loss in precision compared to full parameter matrices.
- **Multiplicative volume formulation:** Regressing logarithmic transformations of stem metrics using $d$, $h$, and $h - 1.3\text{ m}$ provides stable, homoscedastic residual structures across diverse diameter classes.

## Implications for our pipeline

- **Downstream stand inventory:** In remote sensing forest inventories where drone photogrammetry and [[concepts/canopy-height-model|CHM]] pipelines yield height ($h$) and segmented crown areas, invert allometric formulas to infer DBH ($d$) before applying Laasasenaho equations for commercial stemwood volume estimates ([[concepts/site-index-and-yield]]).
- **Species-specific calibration:** Pipeline predictions from [[methods/dinov3-classification|DINOv3]] (pine, spruce, birch) directly dictate which coefficient parameters must be chosen for taper and merchantable volume calculation.
- **Height-diameter inversion links:** Direct drone measurement captures $h$ but lacks direct stem caliper access under the canopy; empirical models converting crown diameter/height to DBH must link with these equations to achieve per-stem wood yield without field crews.

## Replication pseudocode

### Prerequisites

- Species classification (pine, spruce, birch) from [[methods/dinov3-classification]].
- Tree height $h$ (meters) derived from local maxima or CHM height rasters.
- Estimated or measured diameter at breast height $d$ (cm).

### Procedure

```text
1. Select model parameters based on detected tree species.
2. If breast-height diameter d and height h are available:
   a. Compute log-linear volume formulation:
      ln(v) = b0 + b1*ln(d) + b2*ln(h) + b3*ln(h - 1.3) + ...
   b. Apply logarithmic transformation bias correction (+ s^2 / 2) to intercept.
   c. Exponentiate to yield total stem volume in dm^3.
3. For continuous stem profiles or bucking assortment simulations:
   a. Evaluate relative diameter ratios using the polynomial taper model across relative height x = 1 - (stem_height / h).
   b. Scale basic curve relative to d_0.2h.
   c. Adjust taper profile with corrective polynomials matching measured d and h.
```

### Gaps / not specified in paper

- Remote sensing specific errors: Does not evaluate uncertainties arising when height is underestimated in photogrammetric canopy surfaces.
- Direct aerial parameterization: Requires ground-level DBH or calibrated inversion ratios not directly measurable from nadir UAV views.

## Quotes

- The study highlights that selecting sample trees across diverse regional strata is essential to ensure generalizability when computing allometric equations with fewer predictor variables (p. 8).
- The author notes that formulating taper curves through relative height and diameter terms effectively balances out wide variations attributable solely to absolute tree size (p. 19).

## Related pages

- [[project/pipeline-overview]]
- [[concepts/canopy-height-model]]
- [[concepts/site-index-and-yield]]
- [[concepts/height-diameter-inversion]]
- [[methods/dinov3-classification]]
