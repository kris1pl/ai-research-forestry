---
type: Source
title: "BorFIT: A Novel LiDAR-Based Training Dataset for Individual Tree Segmentation and Species Detection in northern boreal Forests"
description: "Introduces the BorFIT dataset containing 16,530 manually segmented and species-classified boreal trees across 384 LiDAR plots with structural and spectral metrics."
tags: [lidar, dataset, tree-segmentation, species-classification, random-forest, boreal-forest]
status: stable
updated: 2026-08-21
source_file: raw/papers/BorFIT_A_Novel_LiDAR-Based_Training_Dataset_for_Individual_Tree-essd-2025-340.pdf
authors: [Jacob Schladebach, Birgit Heim, Léa Enguehard, Mareike Wieczorek, Jakob Broers, Robert Jackisch, Josias Gloy, Kunyan Hao, James Tretton, Anna Gorshunova, Stefan Kruse]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/BorFIT_A_Novel_LiDAR-Based_Training_Dataset_for_Individual_Tree-essd-2025-340.pdf
    title: "BorFIT: A Novel LiDAR-Based Training Dataset for Individual Tree Segmentation and Species Detection in northern boreal Forests"
---

# BorFIT: A Novel LiDAR-Based Training Dataset for Individual Tree Segmentation and Species Detection in northern boreal Forests

## Summary

Schladebach et al. (2025) present **BorFIT**, a comprehensive training dataset designed for individual tree segmentation and species classification in circumboreal forests. The dataset comprises 384 high-density UAV-LiDAR point clouds (each 20 m × 20 m) extracted from 146 sites surveyed between 2021 and 2024 across East Siberia (Yakutia), northwest Canada, and Alaska. 

The authors manually segmented 16,530 individual trees using CloudCompare. To assign species labels, they trained four regional Random Forest classifiers using 11 structural metrics (derived from point geometry and concave hulls) and 2 spectral indices (NGRDI and VARI, where RGB data was available). The resulting dataset bridges the gap between small-scale individual tree assessments and global satellite-based canopy height models, providing a valuable benchmark for deep learning-based forestry pipelines.

## Key claims

* **Large-Scale Dataset:** Contains 16,530 manually segmented individual trees across 14 taxa from 384 reference plots (20 m × 20 m) representing a systematic tree density and height gradient (p. 1).
* **High-Density UAV-LiDAR:** Data acquired at 70 m altitude and 5 m/s speed, yielding a high point density of approximately 400 points/m² (p. 5).
* **Random Forest Classifiers:** Four regional classifiers (RF1–RF4) achieved a mean species classification accuracy of 82% (p. 20).
* **Importance of Spectral Features:** Models incorporating RGB-derived spectral indices (RF1, RF2) outperformed structural-only models. For example, RF1 (11 species + RGB) achieved 86% accuracy, whereas RF3 (11 species, structural only) achieved 73% accuracy (p. 20).
* **Structural Feature Extraction:** Crown shape parameters, such as the pointedness coefficient, crown relief ratio (CRR), and geometric triangle fitting (top angle, widest distance, relative height of widest part), are highly effective for distinguishing species (p. 9).

## Implications for our pipeline

* **Feature Engineering Reference:** The 11 structural metrics (especially pointedness, CRR, and fitted triangle parameters) and 2 spectral indices (NGRDI, VARI) can be directly integrated into our [[methods/dinov3-classification]] or clustering feature extraction steps to improve classification accuracy.
* **Benchmark Data:** The BorFIT dataset (available on PANGAEA) can serve as pre-training or validation data for our 3D point cloud and segmentation models.
* **Validation of Weak Labels:** The paper's supervised Random Forest approach with regional manual overrides provides a solid methodology for generating and refining weak labels before training deep neural networks, aligning with our [[project/pipeline-overview]] strategy.
* **Limitations of Structural-Only Classification:** The drop in accuracy from 86% to 73% when omitting spectral data highlights the necessity of fusing orthophoto RGB bands with CHM/LiDAR geometry in our pipeline.

## Replication pseudocode

### Prerequisites

* R environment with packages: `caret`, `alphashape3d`, and standard spatial/point cloud libraries (`lidR` or `raster`).
* Segmented individual tree point clouds with $X, Y, Z$ coordinates and optional $R, G, B$ values.

### Procedure

```text
1. For each segmented tree point cloud:
    a. Calculate spectral indices (if RGB is available):
        - NGRDI = (Green - Red) / (Green + Red)
        - VARI = (Green - Red) / (Green + Red - Blue)
    b. Calculate basic structural metrics:
        - pointedness = (max(Z) - mean(Z)) / max(Z)
        - CRR (Crown Relief Ratio) = (mean(Z) - min(Z)) / (max(Z) - min(Z))
        - CV_Z = sd(Z) / mean(Z)
        - vertical_variability = sd(Z)
        - ZQ99 = 99th percentile of Z
        - ZQ999 = 99.9th percentile of Z
    c. Calculate concave hull metrics using alphashape3d (alpha = 1):
        - vol_concave = volume of the alpha shape
        - density_concave = total_points / vol_concave
    d. Fit 2D projection triangle:
        - Project points onto 2D plane.
        - Identify the widest horizontal part of the crown.
        - Fit a triangle from the widest part to the tree top.
        - Extract: top_angle, widest_distance, and relative_height_widest.

2. Split dataset into regional subsets (e.g., North America vs. Siberia).
3. Train Random Forest classifiers using 10-fold cross-validation:
    - Tune hyperparameters: mtry (number of variables per split) and ntree (number of trees, default=500).
4. Predict species and output class probabilities.
5. Apply manual taxonomic overrides based on regional biodiversity constraints.
```

### Gaps / not specified in paper

* **Triangle Fitting Algorithm:** The exact mathematical optimization or regression method used to fit the 2D triangle from the widest crown part to the top is not fully detailed (p. 10).
* **Alpha Parameter Selection:** While Figure 5a mentions `alpha = 1` for the alpha shape, the sensitivity of the volume calculation to different alpha values across varying point densities is not discussed.
* **Ground Filtering Thresholds:** The specific parameters used in `LAStools` for ground classification are not specified (p. 5).

## Quotes

> "The predicted tree species include: Picea mariana... Picea sitchensis... Picea glauca... Pinus contorta... Abies lasiocarpa... Larix laricina... Betula papyrifera... Betula neoalaskana... Populus balsamifera... Populus tremuloides... Pinus sylvestris and Alnus glutinosa." (p. 1)

> "Notably the models with RGB (RF1, RF2) relied heavily on spectral variables; top_angle was most important for RF2 which only decided between Picea sitchensis and Betula neoalaskana, and the shape of the crown was the deciding factor." (p. 15, Figure 10 caption)

> "Segmentation based on 2D representations of the canopy tends to overlook trees when dealing with overlapping crowns (Brieger et al., 2019)." (p. 20)

## Related pages

* [[concepts/canopy-height-model]]
* [[concepts/pseudo-tree-crown]]
* [[methods/dinov3-classification]]
* [[project/pipeline-overview]]
