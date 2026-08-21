---
type: Source
title: "Optimizing aerial imagery collection and processing parameters for drone-based individual tree mapping in structurally complex conifer forests"
description: "Comprehensive evaluation of 7,568 combinations of flight parameters, photogrammetry settings, and ITD algorithms in a complex mixed-conifer stand."
tags: [drone, photogrammetry, structure-from-motion, canopy-height-model, individual-tree-detection, local-maxima]
status: stable
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-03-29T12:00:00Z
source_file: raw/papers/Optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests.pdf
authors: [Derek J. N. Young, Michael J. Koontz, JonahMaria Weeks]
year: 2022
replication_status: partial
related_methods:
  - methods/local-maxima
  - methods/chm-detection
sources:
  - id: primary
    resource: raw/papers/Optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests.pdf
    title: "Optimizing aerial imagery collection and processing parameters for drone-based individual tree mapping in structurally complex conifer forests"
---

# Optimizing aerial imagery collection and processing parameters for drone-based individual tree mapping in structurally complex conifer forests

## Summary

This paper presents a comprehensive, quantitative evaluation of how drone imagery collection parameters (flight altitude, camera pitch, and image overlap), photogrammetric processing configurations in Agisoft Metashape, and individual tree detection (ITD) algorithms affect the accuracy of resulting tree maps. The study was conducted in a 3.23-ha structurally complex, moderate-density mixed-conifer stand in Emerald Bay State Park, California, containing 1,916 ground-mapped trees > 5 m tall. 

The authors tested 22 imagery collection methods, 12 photogrammetry parameterizations, and 286 tree detection methods (both raster CHM-based and 3D point cloud-based), generating 7,568 unique tree maps. The optimal pipeline achieved high accuracy, particularly for canopy-dominant and overstory trees, using a high-altitude (120 m) nadir flight with at least 90% overlap, a 2-fold image upscaling (coarsening) step during photogrammetric reconstruction, and a Canopy Height Model (CHM) smoothed with a moving-window mean before applying a Variable Window Filter (VWF).

## Key claims

* **Optimal Flight Parameters:** Imagery collected at high altitude (120 m) with at least 90% forward and side overlap maximized ITD accuracy while optimizing flight efficiency.
* **Nadir vs. Oblique:** Nadir (0° pitch) imagery consistently outperformed oblique (25° pitch) and composite nadir-oblique imagery for individual tree detection.
* **Optimal Processing Parameters:** Photogrammetric processing using 2-fold image upscaling (coarsening) during both photo alignment (Metashape "medium" quality) and dense cloud generation (Metashape "high" quality), combined with moderate depth filtering, yielded the best results (Metashape Parameter Set 16).
* **Algorithm Performance:** Raster CHM-based Variable Window Filter (VWF) algorithms consistently outperformed all 58 tested 3D point cloud-based ITD algorithms.
* **CHM Smoothing:** Applying a moving-window mean smooth (5x5 or 9x9 pixels) to the CHM prior to running the VWF was critical to smoothing over photogrammetric reconstruction artifacts and maximizing accuracy.
* **Detection Accuracy:** For overstory trees > 10 m tall, the optimal pipeline achieved a sensitivity of 0.69, a precision of 0.90, and an F-score of 0.78. For dominant trees > 20 m tall, the F-score reached 0.86.
* **Height Correspondence:** Remotely measured tree heights from the CHM corresponded to ground-measured heights with $R^2 = 0.95$, a mean absolute error of 1.82 m (9%), and a slight negative bias of -0.86 m (-3%).

## Implications for our pipeline

* **CHM Resolution and Smoothing:** Our [[methods/chm-detection]] stage should evaluate downsampling or coarsening the CHM resolution to approximately 0.12 m and applying a moving-window mean smooth (5x5 or 9x9 pixels) to mitigate photogrammetric noise before running local maxima detection.
* **Local Maxima Windowing:** The strong performance of the VWF algorithm supports our use of sliding window local maxima (see [[methods/local-maxima]]). We should implement a dynamic search window where the search radius is a linear function of the focal pixel's height ($d_{max} = a \cdot h + b$).
* **Flight Specifications for Data Ingestion:** When ingesting drone orthophotos and CHMs into the **AREA** pipeline, we should prioritize datasets captured with nadir camera angles and $\ge 90\%$ forward/side overlap.
* **Precision vs. Sensitivity Bias:** The paper notes that ITD precision was consistently higher than sensitivity (0.90 vs 0.69). If our [[project/pipeline-overview]] requires higher recall, we can tune the VWF parameters to be more sensitive and rely on downstream classification filters (e.g., DINOv3 or spectral filters) to prune false positives.

## Replication pseudocode

### Prerequisites

* R environment with packages `ForestTools` (for VWF), `lidR` (for point cloud processing), and `raster`/`terra`.
* Normalized Canopy Height Model (CHM) raster at 0.12 m resolution.

### Procedure

```text
1. Load the normalized CHM raster (0.12 m resolution).
2. Apply a moving-window mean smooth filter (e.g., 5x5 or 9x9 pixels) to the CHM to remove reconstruction artifacts.
3. Define the Variable Window Filter (VWF) search radius function:
   radius = intercept + slope * height
   (where intercept and slope are calibrated parameters, e.g., intercept = 0.5, slope = 0.05)
4. Run the VWF local maxima search on the smoothed CHM:
   - For each pixel, calculate the dynamic search radius based on its height.
   - If the pixel is the maximum height within its calculated radius, flag it as a treetop.
5. Extract the height value from the original (or smoothed) CHM at each flagged treetop location.
6. Filter out detected treetops below a minimum height threshold (e.g., 5 m or 10 m).
```

### Gaps / not specified in paper

* **Specific VWF Parameters:** The paper mentions testing 76 combinations of linear intercepts and slopes for the VWF function (detailed in Supplemental Data S1), but does not explicitly print the exact optimal intercept and slope coefficients in the main text. These must be calibrated empirically or extracted from the supplemental files.
* **Wind Conditions:** While the paper notes "winds were light to moderate," it does not quantify wind speed thresholds above which canopy movement degrades SfM alignment.

## Quotes

* "We found that the accuracy of individual tree detection (ITD) and the resulting tree maps was generally maximized by collecting imagery at high altitude (120 m) with at least 90% image-to-image overlap, photogrammetrically processing images into a canopy height model (CHM) with a 2-fold upscaling (coarsening) step, and detecting trees from the CHM using a variable window filter after first applying a moving-window mean smooth to the CHM." (p. 1)
* "Interestingly, even though the 90%/80% and 80%/90% overlap image sets contained roughly the same image density, the former consistently enabled substantially greater tree mapping accuracy..." (p. 19)
* "Our tests of camera pitch revealed that oblique (25°) and oblique-nadir composite imagery, regardless of flight altitude, yielded ITD accuracy worse than nadir imagery collected at 120 m." (p. 21)
* "The small negative height bias (CHM heights < field-measured heights) generally increased with increasing tree height, suggesting either (a) disproportionate overestimation of tall tree heights during ground surveys or (b) disproportionate underestimation of tall tree heights by the photogrammetry algorithm." (p. 24)

## Related pages

* [[methods/local-maxima]] — Sliding window local maxima detection details.
* [[methods/chm-detection]] — Canopy Height Model generation and processing.
* [[concepts/canopy-height-model]] — Conceptual overview of CHM normalization and interpolation.
* [[project/pipeline-overview]] — The overall Conifervision forest area analysis pipeline.
