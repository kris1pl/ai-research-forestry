---
type: Source
title: "The accuracy of image-based individual tree crown detection and delineation across vegetation types"
description: "Evaluates combinations of 3 CHM and 4 ITS algorithms across 15 Australian vegetation classes, finding Pit-Free CHM and DalPonte segmentation yield the highest accuracy."
tags: [chm, individual-tree-detection, segmentation, lidar, benchmark]
status: stable
updated: 2026-08-21
source_file: raw/papers/The_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-XLVIII-G-2025-1223-2025.pdf
authors: [Nicolas Pucino, Tim McVicar, Shaun Levick, Albert van Dijk]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/The_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-XLVIII-G-2025-1223-2025.pdf
    title: "The accuracy of image-based individual tree crown detection and delineation across vegetation types"
related_methods:
  - methods/chm-detection
  - methods/local-maxima
---

# The accuracy of image-based individual tree crown detection and delineation across vegetation types

## Summary

This study evaluates the performance of different Canopy Height Model (CHM) and Individual Tree Segmentation (ITS) algorithms for generating large tree crown datasets using airborne LiDAR data across Australia. The authors analyzed 37 representative airborne LiDAR point clouds across 15 vegetation classes (representing a range of ecosystems from rangelands to tropical forests) and three point cloud density classes. 

By testing combinations of three CHM algorithms (Point to Raster [P2R], Pit-Free, and Triangulated Irregular Network [TIN]) and four ITS algorithms (DalPonte, Watershed, Silva, and Li), they generated 444 segmentation results. These were validated against 3,387 manually delineated tree crowns. The study concludes that the **Pit-Free CHM** algorithm combined with the **DalPonte ITS** algorithm provides the most accurate and generalizable results, particularly in sparsely vegetated areas, whereas closed-canopy forests remain highly challenging due to crown clumping.

## Key claims

- **CHM Algorithm Performance:** The Pit-Free CHM algorithm achieved the highest match ratio (29% matches) and the highest median adjusted Intersection over Union (adj_IoU = 0.16) across all tested segmentation methods (p. 1225, 1226).
- **ITS Algorithm Performance:** The DalPonte algorithm significantly outperformed other segmentation methods, achieving an 84% match rate (p. 1225) and a median adj_IoU of 0.66 (p. 1226).
- **Poorest ITS Algorithm:** The Li algorithm performed poorly, yielding only a 5% match rate due to severe oversegmentation (p. 1225) and a median adj_IoU of 0.07 (p. 1226).
- **Vegetation Type Impact:** Delineation and detection accuracies are highest in sparsely vegetated areas like low scattered trees (54% match rate) (p. 1225). Conversely, closed-canopy forests and tall open woodlands (15% match rate) suffer from undersegmentation due to crown clumping (p. 1225).
- **Point Cloud Density:** High point cloud density (>16 pts/m²) yielded the best results (e.g., median adj_IoU of 0.3 for medium scattered trees), but low-density datasets (<3 pts/m²) still returned satisfactory results in open structures (p. 1226).
- **Noisy Labels:** The authors suggest that retaining noisy labels in complex canopy environments may be beneficial for deep learning training datasets to prevent underrepresentation of complex structures (p. 1226).

## Implications for our pipeline

- **CHM Generation:** Supports our use of advanced CHM generation techniques. If we process raw LiDAR point clouds, the **Pit-Free CHM** algorithm (Khosravipour et al., 2014) should be prioritized over standard Point-to-Raster or TIN interpolation to minimize empty pixels ("pits") that degrade local maxima detection.
- **Baseline Comparison:** The combination of **Pit-Free CHM + DalPonte ITS** serves as a strong non-deep-learning baseline for our [[methods/chm-detection]] and [[methods/local-maxima]] stages.
- **Handling Crown Clumping:** Confirms that crown clumping in dense/closed-canopy forests causes severe undersegmentation. This justifies our pipeline's integration of **DEIMv2** multi-layer detection to resolve overlapping and multi-layered tree structures.
- **Weak Label Strategy:** The paper's recommendation to retain "noisy labels" to avoid underrepresenting complex canopy environments supports our weak-labeling strategy in [[methods/dinov3-classification]] where we leverage clustering and weak labels for training.

## Replication pseudocode

### Prerequisites

- Raw airborne LiDAR point cloud (LAS/LAZ format).
- Ground truth manual tree crown polygons for validation.
- Python environment with `lidR` (R package) or equivalent Python bindings (e.g., `whitebox`, `laspy`, `scipy`).

### Procedure

```text
1. CLASSIFY POINT CLOUD DENSITY
   - Calculate first-return point density.
   - Categorize into Low (<3 pts/m²), Medium (3-16 pts/m²), or High (>16 pts/m²) using Jenks Natural Breaks.

2. GENERATE PIT-FREE CHM (Khosravipour et al., 2014)
   - Define thresholds (e.g., height bins at 2m, 5m, 10m, 15m, 20m, 25m, 30m).
   - For each height threshold:
     a. Filter point cloud to keep only returns above the threshold.
     b. Triangulate the filtered points to create a partial DSM.
     c. Replace "pits" (pixels where the elevation is significantly lower than the surrounding canopy) with values from the next highest threshold layer.
   - Subtract the Digital Terrain Model (DTM) to produce the final Pit-Free CHM.

3. RUN DALPONTE ITS SEGMENTATION (Dalponte & Coomes, 2016)
   - Step 1: Find local maxima on the Pit-Free CHM using a sliding window to identify tree tops.
   - Step 2: Grow individual crowns from the local maxima seeds using a decision tree based on:
     - Maximum crown radius threshold (TBD)
     - Height threshold percentage of the tree top (TBD)
     - Distance to neighboring pixels

4. EVALUATE ACCURACY
   - For each segmented crown:
     - If 1-to-1 overlap with ground truth: Classify as MATCH. Calculate standard IoU.
     - If 1-to-many overlap: Classify as OVERSEGMENTED. Calculate adjusted IoU (adj_IoU):
       adj_IoU = IoU * (Area_Intersection_Fragment / Area_Ground_Truth)
     - If many-to-1 overlap: Classify as UNDERSEGMENTED. Calculate standard IoU.
```

### Gaps / not specified in paper

- **Specific Parameters:** The exact parameters used for the DalPonte algorithm (e.g., sliding window size, maximum crown radius, height thresholds) and the Li algorithm are not specified in the text.
- **Pit-Free Thresholds:** The specific height thresholds and grid resolution used for the Pit-Free CHM algorithm are not detailed.

## Quotes

> "The Pit-Free CHM algorithm generally outperforms others, yielding higher match rates in the delineation of tree crowns. Additionally, the DalPonte ITS algorithm provides the most accurate results, especially in sparsely vegetated areas..." (p. 1223)

> "Regarding ITS algorithms, the best detections are obtained using DalPonte (84% match) whereas the worst with Li (5%), which is very prone to oversegmentation..." (p. 1225)

> "In forested areas, the reduced delineation accuracies were primarily attributed to the phenomenon of clumping, or crown clustering, which led to higher undersegmentation ratios." (p. 1225)

> "Retaining noisy labels may be beneficial, as overly stringent quality control risks underrepresenting complex canopy environments." (p. 1226)

## Related pages

- [[concepts/canopy-height-model]]
- [[methods/chm-detection]]
- [[methods/local-maxima]]
- [[project/pipeline-overview]]
