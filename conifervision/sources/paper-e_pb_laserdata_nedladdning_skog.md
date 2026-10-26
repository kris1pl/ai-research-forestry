---
type: Source
title: "Laser Data Download, Forest: Product Description"
description: "Specification of Lantmäteriet open ALS point clouds (1–2 pts/m²) across Sweden in SWEREF 99 TM / RH 2000."
tags: [als, lidar, point-cloud, dtm, lantmateriet, sweden, open-data]
status: stable
updated: 2026-03-31
source_file: raw/papers/e_pb_laserdata_nedladdning_skog.pdf
authors:
  - "Lantmäteriet"
year: 2023
replication_status: not_applicable
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-03-31T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/e_pb_laserdata_nedladdning_skog.pdf
    title: "Laser data Download, forest: Product description (Document version 1.6)"
---

# Laser Data Download, Forest: Product Description

## Summary

This document describes the technical product specification for *Laser data Download, forest* (*Laserdata Nedladdning, skog*), an open ALS dataset maintained by Lantmäteriet (the Swedish National Land Survey). Data collection began in 2018 to cover approximately 75% of Sweden's land area with a target point density of 1–2 points/m². Point clouds are delivered in LAS 1.2 format (PDRF 1, compressed via LASzip to `.laz`) in 2.5 × 2.5 km index tiles referenced to SWEREF 99 TM (horizontal) and RH 2000 (vertical). Point classifications follow standard LAS classes: ground (class 2), unclassified/vegetation (class 1), low noise (class 7), water (class 9), bridges (class 17), and high noise (class 18). Deliveries include flight line metadata (`_strip.json`), tile metadata (`_tile.json`), trajectory logs (`.trj`), and survey reports.

## Key claims

- **Point density:** Nominal point density is 1–2 points/m² across scanning lines (e.g., planned minimum ~1.46 points/m² inside individual swaths) (p. 3, 5).
- **Spatial coverage and tiling:** Covers approximately 75% of Sweden, partitioned into standardized 2.5 × 2.5 km tiles (p. 3).
- **Reference systems:** Projected horizontally in SWEREF 99 TM and vertically in the national orthometric height system RH 2000 (p. 3).
- **Classification levels:**
  - *Level 1 (Automatic classification):* Delivered immediately after automated ground filtering and initial QC (p. 4).
  - *Level 3:* Refined classification featuring manual/semi-automated corrections for bridge decks (class 17), dam terrain, and ground/water boundary delineations (p. 4).
- **Point classifications used:** Unclassified (1), Ground (2), Low noise (7), Water (9), Bridges (17; Level 3 only), High noise (18) (p. 3–4).
- **Delivery format:** LAS format version 1.2, Point Data Record Format (PDRF) 1, compressed with LASzip (`.laz`), accompanied by GeoJSON metadata per strip and tile, flight trajectory (`.trj`) files, and delivery QA reports (p. 6–7).

## Implications for our pipeline

- **Ground DTM extraction:** Standard ground points (class 2) provide an accurate reference terrain surface in RH 2000 for generating external DTM rasters, helping normalize photogrammetric UAV DSMs where sub-canopy photogrammetry cannot resolve ground elevation.
- **Canopy Height Model baseline:** At 1–2 points/m², the point density is insufficient for direct individual tree detection (ITD) in dense or juvenile stands (R-class), but provides macroscopic canopy top estimates and regional dominant height benchmarks for [[concepts/canopy-height-model]] and [[concepts/site-index-and-yield]].
- **Coordinate consistency:** Production UAV photogrammetry (ODM) and GIS layers operating in Sweden should standardize on SWEREF 99 TM and RH 2000 to match national elevation datasets without vertical datum distortions.

## Replication pseudocode

### Prerequisites

- Tile boundaries or target AOI coordinates in SWEREF 99 TM.
- Access to Lantmäteriet Geotorget download service / open data portal.
- Tooling for handling LAS/LAZ formats (e.g., `pdal` or `laspy`).

### Procedure

```text
# 1. Tile query and download
query_geotorget(
    aoi_polygon=target_aoi,
    product="Laserdata Nedladdning, skog",
    include_borders=True  # Ensure adjacent boundary overlap smoothing
)

# 2. Extract classified points
for laz_tile in downloaded_tiles:
    # Filter class 2 (ground)
    ground_pts = filter_point_cloud(laz_tile, classification=2)
    
    # Rasterize DTM at 1.0 m or 0.5 m resolution
    dtm_raster = rasterize_tin(ground_pts, crs="EPSG:3006")
    
# 3. Use DTM for UAV CHM normalization
uav_dsm = load_uav_photogrammetry_dsm()
uav_chm = uav_dsm - dtm_raster
```

### Gaps / not specified in paper

- Precise absolute horizontal and vertical accuracy metrics (RMSE) are omitted from this high-level product description; readers are directed to the separate document *Quality description of laser data* (p. 3).
- Specific interpolation algorithms for generating digital terrain models from the classified ground points are not specified.

## Quotes

- *"The product contains a point cloud with a point density of 1-2 points/m2. Each point is classified as ground, water, low point (noise), high noise (for example cloud), point on bridges (only classification level 3) or unclassified."* (p. 3)
- *"Laser data Download, forest is provided in files corresponding 2,5 x 2,5 km index tiles. Reference systems: In plane: SWEREF 99 TM. In height: RH 2000."* (p. 3)
- *"When laser scanning, classification and quality control are finished for a scanning area it will be provided in classification level 1 – Automatic classification. After that every scanning area go through a new classification which means classification of points on bridges, improved ground classification of dams and improved separation between water and ground. This new classification corresponds to classification level 3."* (p. 4)
- *"Borders are not automatically included in the delivery, the user must make an active choice in Geotorget beställning to include borders in your order. Borders can be important for certain applications, for example, they provide a means of smoothing out differences between adjacent scan areas."* (p. 7)

## Related pages

- [[project/pipeline-overview]]
- [[concepts/canopy-height-model]]
- [[concepts/point-cloud-individual-tree-segmentation]]
- [[concepts/site-index-and-yield]]
