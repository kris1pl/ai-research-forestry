---
type: Source
title: "UAV-enabled evaluation of forestry plantations: A comprehensive assessment of laser scanning and photogrammetric approaches"
description: "Comparison of UAV laser scanning (ULS) and UAV structure-from-motion (UAV-SfM) for height measurement and crown-derived DBH modeling across diverse Pinus radiata plantation age classes."
tags: [uav, lidar, uls, sfm, photogrammetry, chm, height-inversion, dbh, allometry, pinus-radiata]
status: stable
source_file: raw/papers/UAV-enabled evaluation of forestry plantations_A comprehensive assessment of laser scanning and photogrammetric approa-1-s2.0-S2666017225000513-main.pdf
authors:
  - Robin J.L. Hartley
  - Sadeepa Jayathunga
  - Joane S. Elleouet
  - Benjamin S.C. Steer
  - Michael S. Watt
year: 2025
replication_status: partial
updated: 2026-10-22
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-22T10:15:00Z
sources:
  - id: primary
    resource: raw/papers/UAV-enabled evaluation of forestry plantations_A comprehensive assessment of laser scanning and photogrammetric approa-1-s2.0-S2666017225000513-main.pdf
    title: "UAV-enabled evaluation of forestry plantations: A comprehensive assessment of laser scanning and photogrammetric approaches"
related_methods:
  - methods/local-maxima
  - methods/chm-detection
---

# UAV-enabled evaluation of forestry plantations: A comprehensive assessment of laser scanning and photogrammetric approaches

## Summary

This study conducts a large-scale empirical evaluation comparing UAV laser scanning (ULS) and UAV Structure-from-Motion (UAV-SfM) photogrammetry across twelve *Pinus radiata* plantation sites in New Zealand, spanning diverse age classes from establishment (<4 years) to mature stands (26+ years). Using high-density point clouds (homogenised to ~400 points/$\text{m}^2$), individual trees were detected on a 25 cm pit-free [[concepts/canopy-height-model|Canopy Height Model (CHM)]] using local maxima filtered by known trial planting spacing and delineated via marker-controlled watershed segmentation restricted to the upper 90% of the CHM.

Rather than relying on direct below-canopy stem returns (which are largely absent in dense or unpruned canopies and photogrammetric clouds), diameter at breast height (DBH) was predicted via [[concepts/height-diameter-inversion|allometric/statistical inversion]] using extracted individual-tree crown 2D/3D metrics (convex hull volume, projected area, height percentiles) trained via Random Forest (RF), Ordinary Least Squares (OLS), and Partial Least Squares (PLS). ULS consistently outperformed UAV-SfM across all age classes for height measurement (ULS average per-site $\text{RMSE} = 0.68\text{ m}$ [5.4%] vs. UAV-SfM $\text{RMSE} = 1.21\text{ m}$ [11.59%]). DBH prediction accuracy was comparable between ULS and UAV-SfM across the pooled dataset ($R^2 = 0.74$, $\text{RMSE} = 2.13\text{ cm}$ [11%] for ULS vs. $R^2 = 0.67$, $\text{RMSE} = 2.05\text{ cm}$ [11%] for UAV-SfM), but ULS proved substantially more resilient to closed canopies, weed understorey, and logging debris. Crucially, UAV-SfM photogrammetry failed to produce reliable Digital Terrain Models (DTMs) once canopy closure occurred, requiring external ULS DTMs for accurate terrain normalisation.

## Key claims

1. **Height estimation accuracy:** ULS achieves an average per-site RMSE of 0.68 m (5.4%) with zero overall mean bias error ($\text{MBE} = 0.00\text{ m}$), whereas UAV-SfM achieves an average per-site RMSE of 1.21 m (11.59%) and exhibits systematic height underestimation ($\text{MBE} = 0.26\text{ m}$ across 82% of sites).
2. **Terrain occlusion in photogrammetry:** In dense closed canopies, UAV-SfM completely fails to resolve the ground surface; UAV-SfM height and CHM derivation for closed stands requires a DTM generated from lidar (ULS) penetration.
3. **Indirect DBH prediction from crown metrics:** Modeling DBH from 2D/3D crown geometric metrics (convex hull surface area, volume, and point density) without direct stem reconstruction achieves an overall $R^2$ of 0.74 (ULS) and 0.67 (UAV-SfM) with an RMSE around 11% (2.05–2.13 cm).
4. **Impact of stand maturity and canopy closure:** DBH model accuracy strongly correlates with stand age ($R^2 = 0.71$ for SfM, $R^2 = 0.69$ for ULS) and canopy openness ($R^2 = 0.28$ for SfM, $R^2 = 0.26$ for ULS). In young open stands, 3D crown volume (`cnx3D_vol`) and 3D area (`cnx3D_area`) dominate variable importance; in mature closed canopies, 2D projected area (`cvx2D_area`) becomes the primary predictor due to interlocking crowns.
5. **Sample size requirements:** DBH model performance plateaus rapidly; training sets of ~200 individual trees achieve prediction accuracies comparable to full census datasets (>1,000 trees).
6. **Distortion from forked trees:** Unfiltered codominant leaders / forked stems severely degrade DBH inversion accuracy, lowering $R^2$ by up to 0.10 and causing massive negative mean bias error (up to $-2.31\text{ cm}$) due to enlarged crown envelopes forking below 1.4 m.

## Implications for our pipeline

- **Photogrammetric DTM limitation:** The production [[project/pipeline-overview|AREA pipeline]] processes UAV photogrammetry (OpenDroneMap point clouds). In dense unthinned coniferous stands, photogrammetry cannot establish true ground elevations. In the absence of concurrent ULS flights, photogrammetric DTM generation using Cloth Simulation Filtering (CSF) risks floating terrain baselines and underestimating tree heights.
- **Crown segmentation boundary thresholds:** The paper restricts watershed crown delineations to the top 90% of the CHM (a 10% drop from the local maximum) to prevent segmented polygons from bleeding into adjacent crowns or incorporating understorey scrub. This matches requirements for [[concepts/crown-ownership|crown ownership]] and [[concepts/normal-forest|normal-forest crown delineation]].
- **Crown-to-DBH inversion feasibility:** For post-detection inventory and [[concepts/site-index-and-yield|site yield]] calculations, DBH can be estimated directly from 2D crown area and CHM maximum height ($z_{\max}$) without requiring costly terrestrial lidar or direct stem point cloud returns ([[concepts/direct-stem-dbh-point-cloud|direct stem DBH point clouds]]).
- **Handling multi-leader / forked crowns:** Over-segmented or forked crowns produce severe outliers in height-diameter allometry. Detection models must either detect multi-leader trees as single compound entities or apply shape morphology filters (e.g., polygon eccentricity / elongation) before feeding crown envelopes into DBH regression models.

## Replication pseudocode

### Prerequisites

- Normalised point cloud (LAZ) or photogrammetric point cloud with accurate DTM (derived from ULS or ground-surveyed benchmarks).
- Point cloud density homogenised (target ~400 points/$\text{m}^2$) via spatial thinning to remove flightline overlap artifacts.
- R environment with `lidR`, `ForestTools`, `cxhull`, and `caret` (or equivalent Python stack: `laspy`, `rasterio`, `scikit-learn`, `scipy`).

### Procedure

```text
# 1. Point Cloud Homogenisation & Normalisation
points = load_laz("raw_point_cloud.laz")
points_homo = sample_homogenise(points, res=1.0, target_density=400) # pts/m^2
dtm = generate_dtm(points_homo, method="knnidw") # or load co-registered ULS DTM
points_norm = points_homo - dtm

# 2. CHM Generation & Smoothing
# Pit-free algorithm (Khosravipour et al., 2014) at 0.25 m resolution
chm = pit_free_chm(points_norm, resolution=0.25, thresholds=[0, 2, 5, 10, 15, 20])
chm_smoothed = apply_moving_window_filter(chm, kernel_size=(3, 3), func="mean")

# 3. Individual Tree Detection (Local Maxima)
# Window size matched to planting spacing (e.g. 2.5 - 3.0 m)
spacing = 3.0 # TBD based on stand density
tree_peaks = find_local_maxima(chm_smoothed, min_distance=spacing)

# 4. Marker-Controlled Watershed Crown Delineation
# Restrict watershed basin expansion to upper 90% of CHM height
crown_polygons = marker_controlled_watershed(
    chm=chm_smoothed,
    markers=tree_peaks,
    height_threshold_factor=0.90 # exclude lower 10% and ground
)

# 5. Segment Point Cloud & Extract 2D/3D Structural Metrics
metrics_list = []
for polygon, peak in zip(crown_polygons, tree_peaks):
    tree_points = extract_points_within_polygon(points_norm, polygon)
    
    # 2D & 3D Convex Hull metrics
    hull_2d = convex_hull_2d(tree_points[:, :2])
    hull_3d = convex_hull_3d(tree_points[:, :3])
    
    metrics = {
        "zmax": np.max(tree_points[:, 2]),
        "zq95": percentile(tree_points[:, 2], 95),
        "zq90": percentile(tree_points[:, 2], 90),
        "pzabove2": count(tree_points[:, 2] > 2.0) / len(tree_points),
        "cvx2D_area": hull_2d.area,
        "cnx3D_area": hull_3d.surface_area,
        "cnx3D_vol": hull_3d.volume,
        "itot": sum(tree_points.intensity) if has_lidar else TBD,
        "n": len(tree_points)
    }
    metrics_list.append(metrics)

# 6. Predict DBH via Random Forest Inversion
# Train on ~200 ground-truth validation trees (excluding forked/damaged stems)
rf_model = train_random_forest(
    X_train=metrics_list[train_indices], 
    y_train=ground_truth_dbh[train_indices],
    tune_folds=10, 
    repeats=5
)
predicted_dbh = rf_model.predict(metrics_list)
```

### Gaps / not specified in paper

- **Exact pit-free parameters:** Specific sub-circle radius and threshold sequences used for the Khosravipour pit-free CHM generation were omitted in the text (defaults in `lidR` assumed).
- **Automated forked-tree detection:** The paper excluded forked trees from primary modeling using manual field trial records; it proposes automated detection of codominant leaders as future work but does not provide an algorithm for doing so.
- **Standalone SfM DTM generation:** The study bypassed photogrammetric DTM failure by substituting ULS DTMs across all twelve sites. Performance of pure UAV-SfM without LiDAR ground truth in closed-canopy stands remains unquantified.

## Quotes

- **On SfM ground occlusion (p. 7):**  
  > "Generating an accurate high-resolution DTM from UAV-SfM point clouds is often challenging in forest stands, particularly where SfM techniques failed to detect the ground due to occlusion caused by tree canopy. Therefore, in this study, DTMs derived from ULS and UAV-SfM point clouds were compared, revealing that the UAV-SfM-derived DTM becomes highly unreliable once canopy closure occurs. As a result, for all sites, UAV-SfM point clouds were ground normalised using ULS-derived DTMs."

- **On crown delineation height thresholds (p. 8):**  
  > "To ensure that the delineated crowns of individual trees do not merge into neighbouring tree crowns and to prevent the inclusion of low vegetation within the identified tree crowns, the crown delineation was restricted to the upper 90 % of the CHM."

- **On sample size requirements for DBH models (p. 10):**  
  > "The number of observations used in the DBH prediction training process did not have a strong effect on model performance... For most datasets, model runs with 200 individual trees yielded similar results to model runs with all available trees."

- **On forked tree errors (p. 14):**  
  > "The results of this study indicated that the model accuracy was reduced and bias (MBE) increased through the inclusion of forked trees in the dataset... This was likely due to the irregular and larger crown size of a forked tree falsely inflating the predicted value of the DBH for those trees."

## Related pages

- [[project/pipeline-overview]] — Operational AREA processing flow from photogrammetry point clouds to CHM and tree detections
- [[concepts/canopy-height-model]] — Pit-free CHM generation and terrain normalization from aerial point clouds
- [[concepts/height-diameter-inversion]] — Methodologies for predicting stem diameter and volume from remote-sensing crown and height metrics
- [[concepts/normal-forest]] — Standard merchantable coniferous stands and crown boundary definitions
- [[concepts/crown-ownership]] — Peak detection, ownership bounding boxes, and vertical cutoff logic
- [[methods/local-maxima]] — Local maxima detection on raster CHMs using fixed or variable search windows
