---
type: Source
title: "Drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots"
description: "Comprehensive evaluation of end-to-end UAV photogrammetric pipelines comparing RGB, multispectral, and hyperspectral data for tree detection, crown delineation, species classification, and allometric attribute estimation in boreal forests."
tags: [uav-imagery, chm, individual-tree-detection, local-maxima, watershed-segmentation, tree-allometry, species-classification, photogrammetry]
status: stable
updated: 2026-06-09
source_file: raw/papers/Drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots.pdf
authors: [Olli Nevalainen, Niko Koivumäki, Raquel Alves de Oliveira, Teemu Hakala, Roope Näsi, Xinlian Liang, Yunsheng Wang, Juha Hyyppä, Eija Honkavaara]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-06-09T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots.pdf
    title: "Drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots"
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/dinov3-classification
---

# Drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots

## Summary

This study presents a comprehensive evaluation of a wall-to-wall UAV image-based individual tree inventory pipeline across six boreal forest plots in Evo, Finland (covering pine, spruce, and birch across easy, medium, and hard difficulty classes). The authors benchmark combinations of dual-RGB, multispectral (MS, 5 bands), and hyperspectral (HS, 46 bands) camera systems across key inventory stages: CHM derivation, individual tree detection ([[methods/local-maxima]] vs. watershed segmentation), crown delineation (constant radius, variable radius, and segmentation), tree attribute estimation (height, DBH, basal area, and stem volume via allometry), and tree species classification using Random Forest models.

The study demonstrates that high-resolution RGB imagery (1.3–2 cm GSD, 1200–1400 pts/m²) outperforms MS data (7–8 cm GSD, 170–210 pts/m²) for tree detection and structural attribute estimation. LM and watershed segmentation achieve virtually identical detection performance (56–84% in plots dominated by dominant/co-dominant crowns, but dropping down to 14–17% in dense plots with suppressed understory). However, crown delineation strategy significantly impacts species classification: variable-radius circular sampling and segmented crown polygons substantially outperform constant-radius circular sampling. Spectral features from HS data yielded the highest species classification F-score (0.89), followed closely by MS spectral features (0.88), while RGB features alone achieved 0.81. While omission of suppressed trees led to significant plot-level stem density underestimation (rRMSE 74.6%), volume was accurately estimated (rRMSE 17.6%) because dominant trees contain the vast majority of stand volume.

## Key claims

1. **Detection performance parity:** Local maxima (FUSION `CanopyMaxima`) and watershed segmentation (EBImage) yielded virtually identical detection and commission rates across all forest difficulty classes.
2. **Dense understory omission:** Both detection methods degrade severely in stands with suppressed trees; detection dropped to 14–17% in dense multi-layered plots (Area 5), demonstrating the strict limitation of structure-from-motion photogrammetry for [[concepts/understory-tree-detection]].
3. **RGB point density superiority:** Higher spatial resolution RGB data (1.3 cm GSD, 1200–1400 pts/m²) produced better detection rates for co-dominant crowns and lower height estimation RMSE (0.97 m, 5.1%) than lower-resolution MS point clouds (7 cm GSD, 170–210 pts/m², RMSE 1.12 m, 5.9%).
4. **Crown delineation impact on species attribution:** Moving from constant-radius circular buffers (LMC) to variable-radius buffers (LMV) or crown segmentation (SEG) improved species classification F-scores significantly (e.g., from 68.1% to 79.3% average F-score across Cases 1–3), avoiding contamination from surrounding canopy.
5. **Species classification sensor tiering:** Spectral features from HS cameras yielded the highest species classification accuracy (maximum F-score 0.89), MS spectral features reached an F-score of 0.88, while RGB-only reached 0.81. Incorporating textural or 3D features into spectral feature sets did not improve HS/MS species classification.
6. **Allometric scaling robustness:** Individual tree DBH was estimated via linear regression ($DBH = \alpha h + \beta D + \gamma$) with an RMSE of 3.09 cm (13.9% rRMSE) using RGB segmentation, resulting in a volume rRMSE of 28.7% (RGB test set). At the plot level, despite 74.6% stem density rRMSE from missed small stems, plot volume rRMSE was preserved at 17.6%.

## Implications for our pipeline

- **Validation of CHM raster detection vs. full 3D:** Supports [[project/pipeline-overview]]'s choice of conducting 2D detection on terrain-normalised raster CHMs rather than direct point cloud detection for upper canopy crowns in managed forests.
- **Normal forest focus:** Directly corroborates the shift to [[concepts/normal-forest]] and [[project/research-normal-forest]]: drone photogrammetric CHMs reliably detect dominant and co-dominant overstory trees (56–84%), but fail completely on suppressed stems in dense, multi-layered stands without thinning.
- **Crown delineation for feature extraction:** Confirms that feeding fixed-radius bounding crops into downstream classifiers can introduce background noise; variable crown-radius sampling or instance mask boundaries improve species attribution, supporting ideas in [[concepts/crown-ownership]] and [[concepts/pseudo-tree-crown]].
- **Volume vs. detection decoupling:** Indicates that for timber and carbon volume estimation ([[concepts/tree-allometry]] and [[concepts/site-index-and-yield]]), missing intermediate and suppressed stems produces only minor volume error (7–10% volume underestimation), validating dominant height and upper-canopy detection for yield assessments.
- **Backbone sensor trade-offs:** Provides empirical proof that standard RGB cameras suffice for detection, height, DBH, and volume estimation, while multispectral bands (specifically the blue band at 475 nm and red-edge indices) provide noticeable gains for species separation if available.

## Replication pseudocode

### Prerequisites

- Calibrated UAV aerial imagery (dual RGB, MS, or HS) with high overlap (≥75% forward and side overlap at canopy height).
- Dense photogrammetric point cloud and georeferenced orthomosaic (e.g., via Agisoft Metashape / PhotoScan).
- Ground classification tools (LAStools `lasnoise`, FUSION `groundfilter`).
- Reference field plot data (species, DBH, height, tree coordinates).

### Procedure

```text
# 1. DTM and CHM Generation
points_filtered = lasnoise(raw_point_cloud, isolation=TBD)
ground_points = groundfilter(points_filtered, cell_size=TBD)
dtm = gridSurfaceCreate(ground_points, cell_size=TBD)
chm = CanopyModel(points_filtered, dtm, cell_size=TBD, smooth=TBD)

# 2. Individual Tree Detection & Crown Delineation
# Method A: Local Maxima (LM)
treetops_lm = CanopyMaxima(chm, window_size_formula=TBD)
# Method B: Watershed Segmentation (SEG)
crown_segments = watershed_segmentation(chm, min_height=TBD, smoothing=TBD)
treetops_seg = [find_max_height_coord(segment, chm) for segment in crown_segments]

# 3. Delineation & Spatial Mask Extraction
for tree in detected_trees:
    if delineation_mode == "LMC":
        mask = circle(center=tree.location, radius=1.0) # 1m fixed
    elif delineation_mode == "LMV":
        radius = tree.estimated_crown_diameter / 2.0
        mask = circle(center=tree.location, radius=radius)
    elif delineation_mode == "SEG":
        mask = tree.segment_polygon

# 4. Feature Extraction
spectral_feats = extract_band_stats(orthoimage, mask) # mean, median, vnorm
vi_feats = compute_vegetation_indices(orthoimage, mask) # NDVI, GNDVI, MCARI, etc.
texture_feats = compute_texture(grayscale_ortho, mask) # GLCM Haralick, TAS, LBP
structural_feats = extract_point_cloud_metrics(point_cloud, mask) # height percentiles

# 5. Species Classification
species_rf = RandomForestClassifier(n_estimators=100)
predicted_species = species_rf.predict(selected_features)

# 6. Tree Attribute Estimation (DBH & Volume Allometry)
# Height h directly from CHM maximum
h = tree.height
# Crown diameter D from CanopyMaxima or circle equivalent to segment area
D = 2.0 * sqrt(area(mask) / pi)

# Species-specific DBH linear model
DBH = alpha[predicted_species] * h + beta[predicted_species] * D + gamma[predicted_species]
BA = pi * (DBH / 2.0)^2

# Allometric Volume (Laasasenaho 1982 formulas)
if predicted_species == "pine":
    Vol = 0.036089 * (DBH^2.01395) * (0.99676^DBH) * (h^2.07025) * ((h - 1.3)^-1.07209)
elif predicted_species == "spruce":
    Vol = 0.022927 * (DBH^1.91505) * (0.99146^DBH) * (h^2.82541) * ((h - 1.3)^-1.53547)
elif predicted_species == "birch":
    Vol = 0.011197 * (DBH^2.10253) * (0.98600^DBH) * (h^0.98600) * ((h - 1.3)^-2.65900)

# 7. Plot-Level Aggregation
plot_stem_density = count(detected_trees) / plot_area_ha
plot_basal_area = sum(BA) / plot_area_ha
plot_volume = sum(Vol) / plot_area_ha
```

### Gaps / not specified in paper

- **Exact filtering parameters:** Specific smoothing kernel sizes, thresholds, and parameters for FUSION `groundfilter`, `gridSurfaceCreate`, and LAStools `lasnoise` are deferred to Supplement S1 (not present in main text).
- **Watershed thresholding details:** Mathematical definitions of pre-filtering, gradient calculation, and exact minima/maxima thresholds in `EBImage` segmentation are referenced in Supplement S1.2.
- **Commission boundary definitions:** The manual delineation rules for the reference areas in commission rate estimation are only illustrated visually (Fig. 1) without explicit boundary buffer formulas.

## Quotes

- **On local maxima vs. segmentation parity:**  
  *"There was no significant difference between the segmentation (SEG) and local-maxima (LM) methods, as both exhibited nearly identical tree detection and commission rates for RGB and MS data."* (p. 7)
- **On missing suppressed understory trees:**  
  *"The poorest results were observed in area 5 ('Hard'), with detection rates of 14–17 % and commission rates of 34–49 %... In contrast, the largest underestimation was observed in area 6, which contained numerous intermediate and suppressed trees, with a relative difference of −66.2 % with RGB and −77.1 % with MS."* (pp. 7, 11–12)
- **On crown delineation impact on species classification:**  
  *"Tree species classification was influenced by the tree crown delineation approach, with the LMC yielding significantly poorer results than the LMV or SEG methods. This difference was most notable when only RGB data were used. These results suggest that moving from constant-sized circles in tree crown delineation to variable-sized circles or segmentation improves tree species classification."* (p. 14)
- **On plot volume resilience despite stem density omission:**  
  *"The plot-level findings indicate that while the rRMSE for stem density estimation is high (74.55 % for RGB and 84.86 % for MS), the rRMSE for volume is significantly lower (17.6 % for RGB and 27.5 % for MS)."* (p. 13)

## Related pages

- [[project/pipeline-overview]] — Operational pipeline using 2D terrain-normalised CHMs, local maxima fusion, and DINOv3 species classification
- [[project/research-normal-forest]] — Program focused on single crown box detection and attributes in normal forest stands
- [[methods/local-maxima]] — Local maxima treetop detection on CHM
- [[methods/chm-detection]] — CHM generation and raster tree detection
- [[concepts/canopy-height-model]] — Height normalisation (DSM − DTM) and photogrammetric surface extraction
- [[concepts/understory-tree-detection]] — Structural limitations of optical remote sensing in multi-tier forest stands
- [[concepts/crown-ownership]] — Crown boundary and sampling constraints for feature extraction
- [[concepts/tree-allometry]] — DBH and volume estimation models from height and crown diameter
- [[concepts/site-index-and-yield]] — Plot-level stand metrics (basal area, stem density, volume/yield)
