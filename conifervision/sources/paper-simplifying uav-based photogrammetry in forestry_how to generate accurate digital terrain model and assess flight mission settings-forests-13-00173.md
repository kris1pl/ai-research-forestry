---
title: "Simplifying UAV-Based Photogrammetry in Forestry: How to Generate Accurate Digital Terrain Model and Assess Flight Mission Settings"
type: Source
tags: [photogrammetry, uav, dtm, chm, ransac, odm, flight-planning]
status: stable
updated: 2026-10-24
description: Evaluates UAV flight settings via Unity simulation and presents a RANSAC plane-fitting and gap-filling method for photogrammetric DTM/CHM generation in dense forest.
source_file: raw/papers/Simplifying UAV-Based Photogrammetry in Forestry_How to Generate Accurate Digital Terrain Model and Assess Flight Mission Settings-forests-13-00173.pdf
authors:
  - Facundo Pessacg
  - Francisco Gómez-Fernández
  - Matías Nitsche
  - Nicolás Chamo
  - Sebastián Torrella
  - Rubén Ginzburg
  - Pablo De Cristóforis
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Simplifying UAV-Based Photogrammetry in Forestry_How to Generate Accurate Digital Terrain Model and Assess Flight Mission Settings-forests-13-00173.pdf
    title: "Simplifying UAV-Based Photogrammetry in Forestry: How to Generate Accurate Digital Terrain Model and Assess Flight Mission Settings"
---

# Simplifying UAV-Based Photogrammetry in Forestry: How to Generate Accurate Digital Terrain Model and Assess Flight Mission Settings

## Summary

This paper investigates how UAV flight mission parameters (overlap, camera tilt, flight pattern, and altitude) affect photogrammetric Structure-from-Motion (SfM) point cloud reconstruction in forested areas, using both a realistic Unity-based synthetic simulator with ground-truth reference geometry and real-world UAV flights. Standard SfM ground filtering tools (such as SMRF in OpenDroneMap or progressive densification in Agisoft Metashape) frequently misclassify dense tree canopy points as ground because optical sensors cannot penetrate continuous foliage, leading to warped Digital Terrain Models (DTMs) and truncated Canopy Height Models (CHMs).

To solve this, the authors propose an iterative post-processing pipeline for SfM point clouds: (1) partition the initial ground point cloud (using median-based or boundary-surrounded partitioning), (2) fit local planes using RANSAC to prune misclassified canopy points, and (3) synthesize equidistant ground points over planar surfaces across large canopy occlusion gaps before rasterizing the DTM with PDAL. Experimental evaluation demonstrates that optimal survey settings for forestry involve high frontal overlap ($95\%$), moderate lateral overlap ($85\%$), nadir angles for single grids ($90^\circ$) or combined nadir/oblique passes ($90^\circ$ and $60^\circ$) in double grids, and that the proposed DTM correction cuts RMSE relative to reference ground models by more than half.

## Key claims

- **Canopy occlusion failure in standard DTM algorithms:** Conventional ground segmentation algorithms (e.g. SMRF in OpenDroneMap / WebODM) assume ground points are visible throughout the surveyed scene. Under dense tree cover, they systematically classify dense crown sections as ground, severely distorting the terrain model and degrading CHM quality (p. 2, 9).
- **Asymmetric point cloud evaluation metrics ($RMSE_{12}$ vs $RMSE_{21}$):** Evaluating reconstructed clouds ($M_2$) against ground-truth surface meshes ($M_1$) requires distinguishing directional metrics. $RMSE_{21}$ (reconstruction to mesh) indicates individual point precision but fails to penalize massive missing geometry. $RMSE_{12}$ (mesh to reconstruction) correctly captures coverage voids and missing canopy/ground structure (p. 9, 12).
- **Optimal flight acquisition settings for forest SfM:**
  - **Overlap:** Frontal overlap is the primary driver of point cloud completeness; $95\%$ frontal and $85\%$ lateral overlap achieve the best trade-off between reconstruction accuracy and flight distance/battery budget (p. 13–14). Overlap below $85\%$ yields unusable reconstructions in dense forest.
  - **Camera angle:** For single-grid flights, a nadir angle ($90^\circ$) produces higher point density and lower error than oblique single runs. For double-grid flights, combining one nadir flight line ($\alpha_1 = 90^\circ$) with an oblique flight line ($\alpha_2 = 60^\circ$) produces superior reconstructions ($RMSE_{12} = 0.91\text{ m}$) compared to nadir-only double grids ($RMSE_{12} = 0.94\text{ m}$) (p. 14–15).
  - **Flight altitude:** Lower altitudes improve GSD and point density. In double-grid workflows, combining two different altitudes ($h_1 = 50\text{ m}$ and $h_2 = 150\text{ m}$) gave the lowest point cloud error ($RMSE_{12} = 1.42\text{ m}$) (p. 15).
- **Partitioned RANSAC ground reclassification and extension:**
  - Pruning misclassified ground points via RANSAC plane fitting on median-divided spatial partitions reduces DTM $RMSE_{12}$ from $2.653\text{ m}$ to $1.701\text{ m}$ (p. 16–18).
  - Closing canopy occlusions by synthesizing equidistant points on RANSAC planes fitted to boundary-surrounded partitions brings the final DTM $RMSE_{12}$ down to $1.843\text{ m}$ compared to $4.287\text{ m}$ for raw ODM output (p. 18).
- **Downstream impact on forestry metrics:** The corrected DTM halved errors in canopy cover estimation (improving coverage from $36.56\%$ to $40.86\%$ against $46.80\%$ ground truth) and enabled automated selective logging change detection from temporal CHM differencing (p. 20–24).

## Implications for our pipeline

- **Photogrammetry and CHM generation preprocessing:** In [[project/pipeline-overview]], the production AREA workflow currently ingests LAZ point clouds generated by OpenDroneMap (ODM) and runs cloth simulation filtering (CSF via `chm_rasterizer.py`) to derive CHMs. Pessacg et al. demonstrate that standard morphological/filtering methods in ODM and photogrammetry packages fail under dense canopy cover, mislabeling dense crown bottoms as terrain. Adding a RANSAC plane reclassification and gap-closing extension step for large data voids before height normalization directly supports more accurate CHM heights in [[concepts/canopy-height-model]].
- **Dense stand height floors and understory:** For dense stands before thinning ([[concepts/dense-stand-detection]]), photogrammetric points rarely reach bare earth. When the derived DTM artificially floats upward into the lower canopy, low trees and lower crown limits are clipped or erased in stratification bands (e.g. `lower 0.3–4 m` vs `upper 4–30 m`). Planar ground extension across canopy gaps prevents artificial truncation of small stems.
- **Flight mission specifications for drone acquisitions:** Field flight guidelines for forestry mapping should enforce $\ge 90\text{--}95\%$ frontal overlap and $\ge 85\%$ lateral overlap. For 3D crown modeling and high-density plots, double-grid flight profiles combining nadir ($90^\circ$) with oblique ($60^\circ$) passes should be preferred to preserve lateral branch structure.

## Replication pseudocode

### Prerequisites

- Dense photogrammetric point cloud ($X, Y, Z$) exported from Structure-from-Motion (e.g. OpenDroneMap / Agisoft Metashape).
- Initial coarse ground classification filter (e.g. SMRF via PDAL/ODM or CSF).
- Point cloud processing library supporting RANSAC plane fitting (e.g., PDAL, Open3D, or PyVista).

### Procedure

```text
# Pessacg et al. 2022: Photogrammetric DTM Ground Reclassification and Gap Closing

1. INITIAL FILTERING:
   - Run SMRF (or CSF) on raw photogrammetric cloud to extract initial GroundCloud and NonGroundCloud.

2. GROUND POINT RECLASSIFICATION (Algorithm 1):
   - Spatial partitioning: Divide GroundCloud in X-Y plane using Median Division (recursively splitting
     along median point coordinates until point count or quadrant area falls below threshold TBD).
   - For each partition P_i:
       a. Fit best plane Plane_i using RANSAC (with inlier distance threshold TBD).
       b. For each point p in P_i:
            if Height(p) > Height(Plane_i at X(p), Y(p)) + threshold_elevation:
                Remove p from GroundCloud
                Add p to NonGroundCloud

3. GAP CLOSING & GROUND EXTENSION (Algorithm 2):
   - Identify spatial voids (canopy gaps lacking ground returns) using boundary perimeter search ("Surrounded" method).
   - For each void partition V_k:
       a. Collect ground points surrounding void perimeter.
       b. Fit best-fitting plane Plane_k using RANSAC.
       c. Synthesize synthetic ground points at regular equidistant grid spacing (step = 5.0 m) across Plane_k.
       d. Add synthetic points to GroundCloud.

4. DTM & CHM RASTERIZATION:
   - Construct DTM raster from augmented GroundCloud using Delaunay triangulation / IDW interpolation in PDAL.
   - Construct DSM raster from all cloud points (highest returns).
   - Generate CHM = DSM - DTM.
   - Apply stratum thresholding or morphological filtering as needed for downstream detection.
```

### Gaps / not specified in paper

- **RANSAC distance thresholds:** Exact elevation threshold values above the RANSAC plane for classifying outliers as vegetation during Median partitioning are not explicitly tabulated (noted generally as user-defined, around $0.15\text{--}0.5\text{ m}$; use `TBD` in production implementation).
- **Void boundary extraction parameters:** The spatial boundary extraction algorithm ("Surrounded" method) lacks exact alpha-shape radius or grid buffer distance parameters for detecting empty canopy pockets.
- **Rugged / non-planar terrain limitation:** Both Algorithms 1 and 2 rely on planar RANSAC approximations within local partitions. While effective for rolling topography, performance in steep, complex mountainous terrain with sharp breaks-of-slope was not rigorously tested against high-density LiDAR DTMs.

## Quotes

- *"However, optical sensors are only poorly capable of penetrating the tree canopy, causing raw image-based point clouds unable to reliably collect and classify ground points in woodlands, which is essential for further data processing."* (Abstract, p. 1)
- *"However, since both approaches assume that there are detectable ground points throughout the surveyed area (and this cannot be granted when employing photogrammetry), canopy points are commonly misclassified as ground points. This drawback limits their use in forest environments."* (Section 1, p. 2)
- *"From all of these combinations we found that using 85% lateral overlap gives good results overall. In particular, combining this value with 95% frontal overlap gives the best trade off in terms of accuracy and number of points/images and flight distance."* (Section 3.1.1, p. 13)
- *"The capability to generate the DTM in forested environments using only the point cloud from SfM is the key for UAS-based photogrammetry in cases where there is no other source available, or it is not possible to use LiDAR due to their high cost or operational difficulty."* (Section 4, p. 25)

## Related pages

- [[project/pipeline-overview]] — Operational pipeline detailing upstream ODM point cloud ingestion, CSF rasterization, and height-stratified layer prep.
- [[concepts/canopy-height-model]] — Canopy Height Model generation principles, normalization challenges over bare ground, and photogrammetric error mitigation.
- [[concepts/dense-stand-detection]] — Challenges of dense canopy coverage where ground penetration fails and understory trees are obscured.
- [[methods/chm-detection]] — Tree detection pipelines utilizing normalized elevation models derived from photogrammetry.
- [[concepts/literature-map-dense-itd]] — Literature map covering SfM/photogrammetry vs LiDAR workflows in dense forest structures.
