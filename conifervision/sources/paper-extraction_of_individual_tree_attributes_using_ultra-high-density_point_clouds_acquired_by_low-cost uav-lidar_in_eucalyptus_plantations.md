---
title: "Extraction of Individual Tree Attributes Using Ultra-High-Density Point Clouds Acquired by Low-Cost UAV-LiDAR in Eucalyptus Plantations"
type: Source
tags: [lidar, uav, individual-tree-detection, stem-detection, dbh, tree-height, point-cloud]
status: stable
updated: 2026-06-09
description: "Bottom-up individual tree extraction using HDBSCAN trunk clustering, chi-square distribution stem DBH measurement, and pseudo-waveform tree height estimation from ultra-high-density low-cost UAV-LiDAR."
source_file: raw/papers/Extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost UAV-LiDAR_in_Eucalyptus_plantations.pdf
authors:
  - Mei Zhou
  - Chungan Li
  - Zhen Li
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-06-09T12:00:00Z
sources:
  - id: primary
    resource: "raw/papers/Extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost UAV-LiDAR_in_Eucalyptus_plantations.pdf"
    title: "Extraction of individual tree attributes using ultra-high-density point clouds acquired by low-cost UAV-LiDAR in Eucalyptus plantations"
---

# Extraction of Individual Tree Attributes Using Ultra-High-Density Point Clouds Acquired by Low-Cost UAV-LiDAR in Eucalyptus Plantations

## Summary

This paper presents an automated bottom-up framework to extract single-tree attributes (tree count, stem base location, DBH, stem lean, tree height, and stem volume) from ultra-high-density point clouds (~19,230 pts/m²) acquired with a low-cost UAV-LiDAR system (DJI Matrice 300 RTK + Zenmuse L1) over an intensively managed *Eucalyptus urophylla* plantation.

Due to the ~10 cm horizontal positional uncertainty inherent to low-cost UAV-LiDAR systems, trunk cross-sections appear as solid circular clusters rather than the hollow rings/arcs typical of terrestrial laser scanning (TLS). Consequently, standard circle-fitting methods fail catastrophically (overestimating DBH with an RMSE of 53.92% / 8.19 cm). To solve this, the authors model radial point distances from the stem center using a $\chi^2$-distribution PDF, achieving a DBH RMSE of 14.37% (2.18 cm). Trunk base detection using HDBSCAN across multiple vertical slices (2–4 m height) achieves an F-score of 0.916. Tree heights are extracted by vector-projecting the stem lean from 1.3 m and 7.0 m slices up into the [[concepts/canopy-height-model|CHM]], clipping a 0.75 m cylinder around the crown apex, and identifying the highest convex extremum using a 10th-order polynomial pseudo-waveform (RMSE 2.69% / 0.31 m).

## Key claims

- **Failure of standard circle-fitting on low-cost UAV-LiDAR:** Low-cost IMU/GNSS sensor noise creates a solid-disk radial distribution in trunk cross-sections rather than a thin annular wall; circle fitting produced a severe bias of -50.30% (-7.64 cm) and an RMSE of 53.92% (8.19 cm).
- **$\chi^2$-distribution modeling of stem cross-sections:** Radial point distance frequencies from the estimated stem center follow a $\chi^2$ distribution with 9–12 degrees of freedom. Peak probability density directly reflects the trunk radius, yielding a DBH RMSE of 14.37% (2.18 cm) and bias of -1.70% (-0.26 cm).
- **Robust trunk detection via multi-slice HDBSCAN:** Clustering point clouds across four vertical bins between 2 m and 4 m (2.0–2.5 m, 2.5–3.0 m, 3.0–3.5 m, 3.5–4.0 m) and tracking vertical continuity within a 50 cm horizontal window achieved Recall = 0.920, Precision = 0.911, and F-score = 0.916 for tree stem detection (413 ground-truth trees).
- **Leaning stem apex projection:** Slender plantation eucalyptus trees frequently lean by >1 m between trunk base and crown top. Tracking stem centers at 1.3 m and 7.0 m allows 3D vector extrapolation to intersect the [[concepts/canopy-height-model|CHM]] surface, correctly centering crown point extraction.
- **Pseudo-waveform tree height filtering:** Fitting a 10th-order polynomial to the crown vertical point density histogram and taking the highest convex extremum eliminates spurious canopy noise and high outliers (e.g. birds, stray multipath points), matching post-felling ground-truth heights with an RMSE of 2.69% (0.31 m) and $R^2 = 0.79$.

## Implications for our pipeline

- **Bottom-up stem detection vs. top-down raster detection:** Our current production AREA workflow ([[project/pipeline-overview]]) relies strictly on 2D CHM rasters and RGB orthophotos with local maxima and DEIMv2 detectors. While top-down raster approaches struggle in interlocking crowns, bottom-up trunk extraction requires ultra-high point density (>15,000–20,000 pts/m²), which photogrammetric UAV point clouds or sparse regional ALS cannot provide under dense canopy cover.
- **Crown apex displacement from stem base:** The paper illustrates that tall slender stems have apex-to-base horizontal shifts exceeding 1.0 m. In [[concepts/normal-forest]] and [[concepts/crown-ownership]], matching top-down CHM local maxima / crown bounding boxes to true stem locations requires accounting for tree lean, especially on steep slopes or stand edges.
- **Pseudo-waveform filtering on photogrammetric CHMs:** The 10th-order polynomial pseudo-waveform technique demonstrates the value of discarding the absolute single highest point $z_{\text{max}}$ in favor of the densest topmost foliage layer when validating drone-derived heights against field inventory or post-felling data.

## Replication pseudocode

### Prerequisites

- Normalized 3D point cloud (points classified into ground and height-above-ground normalized via 0.5 m DTM). Point density ideally $>15,000 \text{ pts/m}^2$.
- DTM and raster [[concepts/canopy-height-model|CHM]] at matching spatial resolution (e.g., 0.5 m).
- Clustering library supporting HDBSCAN and optimization tools for $\chi^2$ and polynomial fitting (e.g., `scipy.optimize`, `hdbscan`, `numpy`).

### Procedure

```text
# 1. Stem Trunk Detection via Layered HDBSCAN
crop point cloud to normalized height interval [2.0 m, 4.0 m]
define 4 height slices: [2.0-2.5], [2.5-3.0], [3.0-3.5], [3.5-4.0]
for each slice h in 1..4:
    clusters[h] = HDBSCAN(points_in_slice)
    for each cluster C in clusters[h]:
        fit chi-square distribution to radial distances -> filter noise
        calculate geometric horizontal center (x_h, y_h) and preliminary diameter D_h

reference_centers = centers from slice 1 (2.0-2.5 m)
for each ref_center in reference_centers:
    match clusters in slices 2, 3, 4 where 2D Euclidean distance <= 0.50 m
    if at least 2 of the 4 matched slices have 5 cm <= D_h <= 35 cm:
        confirm candidate as valid tree stem
        store stem base coordinate (x0, y0) from slice 1

# 2. Direct Stem Diameter (DBH) Extraction via Chi-Square Filtering
for each confirmed tree stem:
    extract cylinder buffer (radius = 0.5 m, height interval = [1.05 m, 1.55 m] for 1.3 m DBH)
    repeat:
        (x0, y0) = mean(x_i, y_i) of retained cylinder points
        distances d_i = sqrt((x_i - x0)^2 + (y_i - y0)^2)
        build histogram of d_i over [0, max(d_i)] using 50 uniform bins
        fit chi-square PDF f(x; v)
        reject outliers at significance level alpha = 0.05
    until convergence (no further points rejected, typically 2-5 iterations)
    
    stem_radius R = argmax(f(x; v))
    DBH = 2 * R
    if DBH < 5 cm or DBH > 20 cm:
        shift vertical search window up (+0.5 m) or down (-0.5 m) within [0.8 m, 2.3 m]
        if no slice yields valid DBH: assign plot mean DBH
    repeat same procedure at 7.0 m height to obtain stem center (x7, y7, 7.0)

# 3. Crown Apex Search and Pseudo-Waveform Height Extraction
for each tree:
    vector_dir = (x7 - x1.3, y7 - y1.3)
    trace 3D ray along vector_dir from stem base up to intersection with CHM surface
    find crown apex coordinates (xtop, ytop, ztop) via geometric projection (Equations 2-5)
    
    clip vertical point cylinder centered at (xtop, ytop) with radius = 0.75 m
    bin cylinder points into 100 vertical bins from ground (0) to max_height
    fit 10th-order univariate polynomial f(z) to bin fractional frequencies via least squares
    find inflection points where second derivative f''(z) == 0
    identify convex intervals (f''(z) < 0)
    
    in highest convex interval:
        if exactly one inflection point lies above peak:
            tree_height = z of local maximum
        else:
            tree_height = z of minimum in the overlying concave interval
    
    calculate vertical stem volume VOL using allometric equation (Eq. 1)
```

### Gaps / not specified in paper

- **HDBSCAN hyperparameter tuning:** Minimum cluster size (`min_cluster_size`) and minimum samples (`min_samples`) for the HDBSCAN algorithm on 0.5 m vertical slices are not explicitly reported; values depend heavily on local point density.
- **Handling multi-stem / coppice clumps:** The plantation was a second-rotation coppice with multi-stem stump sprouts; the authors note proximity to budding trees caused omissions, but explicit criteria for splitting touching twin stems are not specified beyond the 50 cm centroid threshold.
- **Sensitivity to lower point density:** The authors hypothesize a requirement of $\ge 20,000\text{ pts/m}^2$ for this bottom-up workflow to succeed, but do not provide an empirical decimation curve evaluating at what lower threshold (e.g. 1,000–5,000 pts/m²) the $\chi^2$ diameter fitting breaks down.

## Quotes

- *"Due to the distinct clustering of point clouds, trunk detection tends to be more accurate. However, it needs a high point cloud density."* (p. 3)
- *"We proposed that the primary cause of the reduced accuracy in direct tree diameter measurements obtained by low-cost UAV-LiDAR... stemmed from the fact that the point clouds generated by such systems exhibited a solid-circle distribution in the trunk cross-section rather than a hollow circle or arcs... This deviation led to an absence of a mathematical foundation for employing the circle-fitting method to measure tree diameters."* (p. 17)
- *"The bias and RMSE observed in the DBH measurements obtained using the circle-fitting method were much larger than those extracted using the $\chi^2$-filtering method, which were −50.30% (−7.64 cm) and 53.92% (8.19 cm), respectively... Such a large error is unacceptable in practical application."* (p. 13)
- *"The result indicated a precision of 91.1% for individual tree detection, with an F-score of 0.916. The root mean square errors (RMSEs) for direct measurements of diameter at breast height (DBH) and tree height were 14.60% (2.18 cm) and 2.69% (0.31 m), respectively."* (p. 1)

## Related pages

- [[project/pipeline-overview]] — Operational AREA processing flow using photogrammetric CHM rasters and DEIMv2 detection.
- [[concepts/canopy-height-model]] — Principles of terrain-normalized height models (DSM − DTM).
- [[concepts/literature-map-dense-itd]] — Literature priorities for individual tree detection in dense and planted stands.
- [[concepts/normal-forest]] — Definition and attribute requirements for merchantable single-tree crowns.
- [[concepts/crown-ownership]] — Peak attribution and crown ownership principles linking tops to base extents.
