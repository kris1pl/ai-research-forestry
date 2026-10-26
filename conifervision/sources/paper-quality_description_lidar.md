---
type: Source
title: "Lantmäteriet: Quality Description — Laser Data (v1.6)"
description: Technical quality description and error characterization of national airborne LiDAR datasets in Sweden (Laser data Download, NH and Forest).
tags: [lidar, lantmateriet, dtm, chm, ground-filtering, point-cloud, sweden]
status: stable
updated: 2026-10-21
source_file: raw/papers/quality_description_lidar.pdf
authors:
  - "Lantmäteriet"
year: 2022
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/quality_description_lidar.pdf
    title: "Quality Description Laser Data (Document Version 1.6)"
related_methods:
  - methods/chm-detection
  - methods/local-maxima
---

# Lantmäteriet: Quality Description — Laser Data (v1.6)

## Summary

This official technical quality report from Lantmäteriet (the Swedish National Land Survey) details the specifications, error modes, and operational characteristics of Sweden's national airborne laser scanning (ALS) data products: *Laser data Download, NH* (national elevation model) and *Laser data Download, forest* (Laserdata Skog). The document assesses data quality under ISO 19157:2013 across completeness, positional accuracy, classification accuracy, and seasonal variation.

The document systematically catalogues known systematic failure modes in ALS classification and ground surface extraction—specifically in dense brushwood/regeneration stands, steep rocky terrain, and multi-temporal flight line boundaries. These specifications provide critical reference parameters for ground elevation reference data (DTM) used when normalising UAV photogrammetric point clouds into a [[concepts/canopy-height-model]].

## Key claims

- **Point density standards**:
  - *Laser data Download, NH*: Mean point density $\ge 0.5\text{ points/m}^2$ (last return, 10 m cells) across $\ge 95\%$ of scanned surface ($0.25\text{ points/m}^2$ in bare mountain regions). Altitude 1,700–2,300 m, footprint 0.4–0.9 m, side overlap 10–20%.
  - *Laser data Download, forest*: Mean point density 1.0–2.0 points/m$^2$ ($\ge 1.0\text{ points/m}^2$ across $\ge 95\%$ of surface). Altitude $\sim 3,000\text{ m}$, footprint $< 0.75\text{ m}$, side overlap $\ge 20\%$. Instrument pulse returns with $>1$ return must reach $\ge 30\%$ in forest.
- **Positional accuracy**:
  - Absolute horizontal error (open flat hard surfaces): standard error $< 0.3\text{ m}$ in plane.
  - Absolute vertical error (open flat hard surfaces): standard error $< 0.1\text{ m}$ in height.
  - Relative vertical error between adjacent flight lines: standard error $< 0.15\text{ m}$.
  - Planar accuracy degrades terrain height accuracy on steep slopes.
- **Pulse dead zone / instrument separation**: Sensor technology cannot record returns occurring within $\sim 2\text{ m}$ of a preceding return along the same pulse path.
- **Vegetation penetration failures (elevation bias)**:
  - In dense deciduous brushwood, young regeneration clearings, crops, or reeds, pulses cannot penetrate to the true ground. Combined with the 2 m sensor dead zone, the automated ground classification routinely misclassifies the canopy/shrub surface as ground.
  - Observed ground elevation overestimation of **2 to 3 metres** above actual bare ground in thickets and clearings.
- **Steep terrain omissions**: On vertical cliffs, rock cuts, and boulder fields, automatic ground algorithms frequently reject ground points as vegetation or buildings, causing artificial smoothing or missing terrain slices.
- **Tall and narrow tree crowns**: The highest crown peak is frequently missing in point clouds due to low density (0.5–2 pts/m$^2$) and narrow beam footprints.

## Implications for our pipeline

- **Reference DTM quality for [[concepts/canopy-height-model]] (CHM)**: In [[project/pipeline-overview]], normalizing photogrammetric UAV surface models (DSM) with Lantmäteriet DTMs can introduce 2–3 m vertical underestimation of tree height in dense young regeneration stands (R-class) where the historical ALS failed to penetrate shrub layers.
- **Crown height clipping**: Because low-density ALS misses thin apical leaders of coniferous trees, heights derived purely from Lantmäteriet laser data underestimate maximum crown height compared to dense UAV photogrammetry or high-density UAV-LiDAR.
- **Ground filtering validation**: Highlights that cloth simulation filtering (CSF) or TIN-densification in dense stands requires awareness of false ground surfaces; if no returns penetrate the lower 2 m, any algorithm will latch onto the brushwood layer.

## Replication pseudocode

### Prerequisites

- National ALS LAS/LAZ tiles (`Laser data Download, forest` or `NH`) in SWEREF 99 TM / RH 2000.
- Companion metadata including flight date, scanning system, and season.

### Procedure

```text
# Evaluation of national ALS ground model quality for DTM/CHM production
1. Load LAS 1.2 tile containing returns and classification codes.
2. Filter points by return type:
     - Count last returns per 10 x 10 m cell.
     - Validate completeness against requirement (>= 1.0 pts/m2 in forest).
3. Extract Class 2 (Ground) points:
     - Identify data voids where point density on ground drops to 0.
4. Flag potential ground overestimation zones:
     - Check flight metadata season (summer flights in non-coniferous zones).
     - Cross-reference with external vegetation masks or high-resolution UAV orthophotos.
     - In dense brush/reeds, expect ground elevation bias between +0.5 m and +3.0 m.
5. Apply relative flight-line equalization check across overlap zones (threshold: standard error < 0.15 m).
6. Interpolate validated ground points into DTM raster for DSM subtraction:
     CHM = DSM_photogrammetry - DTM_ALS
```

### Gaps / not specified in paper

- Specific parameter sets used for the three national automatic classification zones (TBD).
- Algorithmic implementation details of the automatic classification filter (described only as "automatic methods" supplemented by GGD database masks).
- Quantitative penetration probabilities across specific Swedish conifer vs. broadleaf canopy cover densities.

## Quotes

- **On dense vegetation ground bias (p. 9–10):**
  > "Firstly, technological limitations with laser scanning entail that returns from a short distance (about 2 metres) following a preceding return cannot be registered, and secondly, the vegetation is sometimes so dense, e.g. cereals or shrubbery, that no laser pulses can penetrate to the ground... the terrain model has registered 2-3 m above the actual ground surface."
- **On missing tree tops (p. 6):**
  > "Tall and narrow objects are not always complete depicted in the laser point cloud, highest peak may be missing. This depends on the scanning angle and point density."
- **On absolute accuracy specifications (p. 4):**
  > "On open flat hard surfaces, the standard error < 0,1 m in height, < 0.3 m in plane."

## Related pages

- [[concepts/canopy-height-model]] — Production and error bounds of CHM surfaces derived from photogrammetry and DTMs.
- [[concepts/understory-tree-detection]] — Challenges where upper canopy occludes lower vegetation layers.
- [[project/pipeline-overview]] — Operational pipeline utilizing ground filtering and CHM generation.
