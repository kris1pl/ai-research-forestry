---
title: "UAV-Based LiDAR Scanning for Individual Tree Detection and Height Measurement in Young Forest Permanent Trials"
type: Source
tags: [uav, lidar, itd, chm, young-forest, height-underestimation, lidr, foresttools]
status: stable
description: "Evaluates five ITD methods and three CHM resolutions on young Pinus pinaster and Pinus radiata plantations, finding that 10 cm CHM resolution is optimal and point cloud-based height extraction avoids the systematic underestimation of CHM-based methods."
source_file: raw/papers/UAV-Based_LiDAR_Scanning_for_Individual_Tree_Detection_and_Height_Measurement_in_Young_Forest-5_2021.pdf
authors: [Francisco Rodríguez-Puerta, Esteban Gómez-García, Saray Martín-García, Fernando Pérez-Rodríguez, Eva Prada]
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-03-29T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/UAV-Based_LiDAR_Scanning_for_Individual_Tree_Detection_and_Height_Measurement_in_Young_Forest-5_2021.pdf
    title: "UAV-Based LiDAR Scanning for Individual Tree Detection and Height Measurement in Young Forest Permanent Trials"
---

# UAV-Based LiDAR Scanning for Individual Tree Detection and Height Measurement in Young Forest Permanent Trials

## Summary

This paper evaluates the performance of individual tree detection (ITD) and height estimation using high-density UAV-based LiDAR scanning (ULS) in young *Pinus pinaster* and *Pinus radiata* plantations (ages 2 to 5 years, mean heights 1 to 5 m). The authors compared five ITD algorithms across three Canopy Height Model (CHM) resolutions (10 cm, 25 cm, and 50 cm) and evaluated direct point cloud-based height extraction. 

The study demonstrates that a **10 cm CHM resolution** consistently yields the highest ITD accuracy. Point cloud-based height extraction was found to be practically unbiased (mean bias error of -0.047 m), whereas CHM-based height extraction systematically underestimated tree heights (mean bias error of 0.139 m for non-smoothed CHM and 0.251 m for smoothed CHM). Both ITD and height estimation accuracy degraded significantly for trees under 1.0 m in height.

## Key claims

*   **Optimal CHM Resolution:** The best CHM resolution for identifying individual trees in young stands is **10 cm** (p. 1). Coarser resolutions (25 cm and 50 cm) significantly increase omission errors.
*   **Algorithm Performance:** The best ITD results were obtained using the `lidR` package with the Dalponte and Coomes (2016) algorithm, yielding relative errors (RE) between -13.27% and 1.47% (p. 7).
*   **Height Underestimation Bias:** Extracting tree heights from a CHM introduces systematic underestimation. Non-smoothed CHMs underestimated height by an average of 0.139 m, while smoothed CHMs underestimated height by 0.251 m (p. 8).
*   **Unbiased Point Cloud Heights:** Measuring tree heights directly from the raw LiDAR point cloud yields nearly unbiased results (mean bias of -0.047 m and RMSE of 0.137 m) (p. 8).
*   **Height Threshold for Accuracy:** Both ITD and height estimation accuracy drop sharply for trees under **1.0 m** in height. For trees taller than 1.0 m, the percentage relative error (PE) of height estimation falls below 10%, and relative detection errors drop to near 1% (p. 1, 9).
*   **Species Invariance:** No significant differences in detection or height estimation accuracy were observed between *Pinus pinaster* and *Pinus radiata* (p. 1).

## Implications for our pipeline

*   **Resolution Target:** For young or structurally simple conifer stands, our [[concepts/canopy-height-model]] generation should target a **10 cm grid resolution** to maximize local maxima detection rates.
*   **Height Extraction Strategy:** To avoid systematic underestimation in our [[project/pipeline-overview]], we should extract tree heights directly from the normalized point cloud at the detected coordinate locations rather than relying solely on the rasterized CHM values.
*   **Filtering Small Trees:** Trees under 1.0 m in height should be flagged with lower confidence or handled via specialized sub-models, as standard local maxima and CHM-based segmentation methods exhibit high omission rates (RE ~15%) in this size class.
*   **Algorithm Selection:** The Dalponte and Coomes region-growing algorithm (available in `lidR`) serves as a highly stable baseline for young conifer stands, aligning with our [[methods/chm-detection]] and [[methods/merge-detections]] stages.

## Replication pseudocode

### Prerequisites

*   High-density normalized UAV LiDAR point cloud (minimum 190 points/m²).
*   R environment with `lidR` and `raster` packages installed.

### Procedure

```text
1. Generate a high-resolution Canopy Height Model (CHM) at 10 cm resolution:
   - Use the point-to-raster or pit-free algorithm on the normalized point cloud.

2. Smooth the CHM (optional, only for treetop detection baseline):
   - Apply a small Gaussian or median filter window (e.g., 3x3 or 5x5 pixels).

3. Detect treetops using the Dalponte and Coomes (2016) algorithm:
   - Define a search window size (TWS) appropriate for young crowns (e.g., sliding window).
   - Identify local maxima on the 10 cm CHM.

4. Segment individual tree crowns:
   - Apply region-growing from the detected local maxima using the normalized point cloud and CHM.

5. Extract individual tree heights:
   - For each segmented tree crown, query the raw normalized point cloud.
   - Assign the maximum Z-coordinate value within the crown boundary as the final tree height.
   - Avoid using the smoothed CHM pixel value to prevent systematic underestimation.
```

### Gaps / not specified in paper

*   **Specific TWS/SWS Parameters:** The exact sliding window sizes (Tree Window Size and Smoothing Window Size) used for the local maxima filters across different plots were not explicitly tabulated.
*   **Point Cloud Density Thresholds:** The paper utilizes very high-density ULS data (194–357 returns/m²). The performance degradation of the point cloud-based height extraction at lower point densities (e.g., standard ALS) is not quantified.

## Quotes

*   "The best CHM resolution for identifying trees was always 10 cm." (p. 1)
*   "Regarding the estimation of tree height, we can conclude that the use of the CHM to estimate height tends to underestimate its value, while the use of the point cloud presents practically unbiased results." (p. 1)
*   "The mean PE fall below 10% when tree height categories exceed 1 m. Therefore, measure of tree height from UAV based lidar is preferable when tree height reached 1 m, and this threshold is the same as for ITD." (p. 9)

## Related pages

*   [[concepts/canopy-height-model]]
*   [[methods/local-maxima]]
*   [[methods/chm-detection]]
*   [[project/pipeline-overview]]
