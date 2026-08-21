---
title: "Cross-Comparison of Individual Tree Detection Methods Using Low and High Pulse Density Airborne Laser Scanning Data"
type: Source
tags: [itd, lidar, chm, local-maxima, benchmark]
status: stable
updated: 2026-08-21
description: "Comparative study of seven ITD methods across mixed-conifer stands using 8 and 22 ppm² ALS data, showing that stand density and parameter tuning drive accuracy more than method choice."
source_file: raw/papers/Cross-comparision-of-ITD-methods-using-low-and-hight-pulse-density-ALS-2022-Sparks-et-al.pdf
authors: [Aaron M. Sparks, Mark V. Corrao, Alistair M. S. Smith]
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Cross-comparision-of-ITD-methods-using-low-and-hight-pulse-density-ALS-2022-Sparks-et-al.pdf
    title: "Cross-Comparison of Individual Tree Detection Methods Using Low and High Pulse Density Airborne Laser Scanning Data"
related_methods:
  - methods/local-maxima
  - methods/chm-detection
---

# Cross-Comparison of Individual Tree Detection Methods Using Low and High Pulse Density Airborne Laser Scanning Data

## Summary

This study evaluates seven individual tree detection (ITD) methods representing point-cloud-based, raster-based, and hybrid approaches using a single benchmark forest inventory dataset in north-central Idaho, USA. The validation dataset consists of 67 mixed-conifer plots containing species with highly diverse crown shapes. The methods were tested across two airborne laser scanning (ALS) datasets: a lower pulse density dataset (average 8 $\text{ppm}^2$) and a higher pulse density dataset (average 22 $\text{ppm}^2$). 

The study demonstrates that overall ITD accuracy (F-score) varies minimally between the top-performing configurations of each method (0.47 ± 0.03 for 8 $\text{ppm}^2$ and 0.50 ± 0.02 for 22 $\text{ppm}^2$). Instead, stand density, canopy cover, and parameter tuning (specifically matching search window sizes to average crown diameters) are the primary drivers of detection performance.

## Key claims

- **Method Performance Equivalence:** When parameters are optimized, there is little variation in F-score between different ITD methods. The choice of method is secondary to stand structure and parameter tuning (p. 1).
- **Pulse Density Impact:** Higher pulse density (22 $\text{ppm}^2$ vs. 8 $\text{ppm}^2$) improves ITD F-scores. Some methods (ForestView®, SWA, watershed) showed substantial gains of 10–13%, while others (Li 2012, lidR LMF, rLiDAR LMF, VWF) showed modest gains of 1–3% (p. 1, 9).
- **Omission Errors and Canopy Position:** Omission errors are strongly driven by stand density and canopy position. Dominant trees are detected at high rates (66% for 8 $\text{ppm}^2$, 71% for 22 $\text{ppm}^2$), whereas suppressed trees are heavily occluded and rarely detected (<13% across all methods) (p. 1, 9).
- **Parameter Sensitivity:** The highest accuracies are obtained when search window sizes or spacing thresholds are equal to or less than the average crown diameter of the target forest stand (TBD, optimized at <2.5 m in this study) (p. 1, 9).
- **CHM Resolution Interaction:** For lower pulse density data (8 $\text{ppm}^2$), a finer 25 cm CHM performed slightly better. For higher pulse density data (22 $\text{ppm}^2$), a 50 cm CHM yielded the highest accuracy, likely due to a reduction in micro-surface noise (p. 9, 14).
- **Height Measurement Accuracy:** All tested ITD methods produced highly accurate height measurements for detected trees, with RMSE < 1.1 m and bias < 0.5 m (p. 1, 12).

## Implications for our pipeline

- **Local Maxima Window Tuning:** Supports our use of [[methods/local-maxima]] sliding windows. Confirms that window sizes must be dynamically or empirically tuned to match the expected crown diameter of the target forest type (e.g., <2.5 m for dense conifers) to balance commission and omission errors.
- **CHM Resolution Guidelines:** For high-density drone orthophotos and photogrammetric point clouds, we should evaluate whether ultra-fine CHM resolutions (e.g., 10 cm) introduce surface noise that degrades local maxima detection compared to slightly smoothed resolutions (e.g., 25 cm or 50 cm) as observed in the 22 $\text{ppm}^2$ dataset.
- **Occlusion Limitations:** Reinforces that top-down geometric methods (CHM local maxima) are fundamentally limited by canopy occlusion. Sub-canopy or suppressed trees cannot be reliably resolved via standard CHM local maxima, validating our integration of multi-layered deep learning detectors like [[methods/deimv2-canopy]].
- **ForestView® Hybrid Reference:** The ForestView® hybrid approach (developed by NMI) utilizes both CHM-based segmentation and point-cloud metrics to model DBH, volume, and species. This aligns with our pipeline's goal of combining geometric detection with deep-learning-based classification via [[methods/dinov3-classification]].

## Replication pseudocode

### Prerequisites

- R environment with packages `lidR`, `rLiDAR`, `ForestTools`, and `raster`/`terra`.
- Normalized ALS point cloud or a pre-calculated Canopy Height Model (CHM).

### Procedure

```text
# 1. CHM Generation (Pit-free method)
# Generate a pit-free CHM at 25 cm or 50 cm resolution using the lidR package
chm = grid_canopy(las, res = 0.25, algorithm = pitfree(thresholds = c(0, 2, 5, 10, 15, 20), subcircle = 0.3))

# 2. Fixed Local Maxima Filter (LMF) - lidR implementation
# Define search window size (must be equal to or less than average crown diameter, e.g., 2.5 m)
window_size = 2.5 
detected_trees_lmf = locate_trees(chm, lmf(ws = window_size, shape = "circular"))

# 3. Variable Window Filter (VWF) - ForestTools implementation
# Define allometric function relating tree height to crown diameter
# Default equation: crown_diameter = (0.06 * height + 0.5) * 2
allometric_fn = function(x) { (0.06 * x + 0.5) * 2 }
detected_trees_vwf = vwf(CHM = chm, winFun = allometric_fn, minHeight = 1.5)

# 4. Accuracy Assessment (Matching)
# Match detected trees to field reference stems within a 2.5 m horizontal search radius
# and a maximum 2.0 m height difference threshold.
```

### Gaps / not specified in paper

- **Point Cloud Thinning:** The paper notes that the scanning patterns (sawtooth vs. equidistant matrix) differed between the 2018 and 2021 datasets, but point cloud thinning was not performed to homogenize pulse density (p. 14).
- **Specific ForestView® Parameters:** ForestView® is a proprietary commercial tool; its internal database parameters, exact watershed thresholds, and regression models for DBH/volume are not fully disclosed (p. 6).

## Quotes

> "ITD accuracy had large intra-method variation depending on input parameters; however, the highest accuracies were obtained when parameters such as search window size and spacing thresholds were equal to or less than the average crown diameter of trees in the study area." (p. 1)

> "Like other ITD method comparison studies (e.g., [4,31]), stand density was a larger driver of method accuracy than the individual methods themselves." (p. 15)

> "The 8 ppm² ALS dataset had insufficient pulse density for producing 10 cm resolution CHMs, and thus only 25 cm and 50 cm CHMs were used." (p. 6)

## Related pages

- [[methods/local-maxima]] — Sliding window local maxima methodology
- [[concepts/canopy-height-model]] — Canopy Height Model generation and smoothing
- [[sources/popescu-wynne-2004-seeing-the-trees]] — Original paper introducing the Variable Window Filter (VWF)
- [[sources/paper-comparison_of_individual_tree-twec21_public]] — Weckman (2021) ITD benchmark study
