---
title: "Skoglig fjärranalys (Forest Remote Sensing)"
type: Source
tags: [forestry, remote-sensing, lidar, photogrammetry, inventory, uav]
status: stable
updated: 2026-10-24
description: Comprehensive educational compendium by SLU covering physical foundations, airborne LiDAR, digital photogrammetry, satellite observation, and forest inventory methods.
source_file: raw/papers/skoglig_fjarranalys_v1_0_161211.pdf
authors:
  - Heather Reese
  - Håkan Olsson
  - Björn Nilsson
  - Jonas Bohlin
  - Eva Lindberg
  - Johan Holmgren
  - Karin Nordkvist
  - Kenneth Olofsson
  - Henrik Persson
  - Jörgen Wallerman
  - Mats Nilsson
year: 2016
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/skoglig_fjarranalys_v1_0_161211.pdf
    title: "Skoglig fjärranalys (Version 1.0)"
---

# Skoglig fjärranalys (Forest Remote Sensing)

## Summary

*Skoglig fjärranalys* is a textbook and educational compendium published by the Swedish University of Agricultural Sciences (SLU) Department of Forest Resource Management. It synthesizes the physical and methodological foundations of forest remote sensing, bridging optical imagery, aerial photogrammetry, airborne and terrestrial laser scanning (ALS/TLS), radar, and operational forest management.

The text details the operational integration of remote sensing within Nordic forestry, contrasting area-based approaches (ABA) with individual tree detection (ITD). It also describes the creation and operational usage of elevation models, canopy height models (CHM), and orthophotos, including drone-based platforms (multirotors vs. fixed-wing) and point clouds generated via dense image matching.

## Key claims

- **Evolution of 3D Data Sources:** Modern operational forestry relies heavily on 3D structure; while airborne laser scanning provides superior canopy penetration and ground surface modeling, digital stereophotogrammetry produces dense surface models (matching point clouds) suitable for canopy height extraction at lower costs.
- **Scale and Resolution Frameworks:** Forest remote sensing operates across two primary regimes: high-resolution ($H$-resolution), where individual crown components span multiple pixels requiring segmentation, and low-resolution ($L$-resolution), where pixels aggregate multiple stems and shadows requiring sub-pixel modeling.
- **Influence of Canopy Shadowing:** In northern boreal forests with low solar elevation, shadows cast by crowns strongly affect optical reflectance, producing an inverse correlation between volume/basal area and reflectance in red and SWIR wavelengths.
- **Role of UAV Systems:** Small UAV platforms (fixed-wing and multirotor) are increasingly practical for stand-level inventory, offering ultra-high spatial resolution and photogrammetric 3D reconstructions, balanced by operational tradeoffs such as battery endurance and visual line-of-sight regulations.

## Implications for our pipeline

- **Raster vs. Point Cloud Fusion:** Reenforces our architectural split in [[project/pipeline-overview]]: using normalized 2D raster representations (such as a [[concepts/canopy-height-model]]) derived via ground filtering algorithms (e.g., CSF) for scalable 2D detection networks (DEIMv2), alongside high-resolution RGB crops for species identification.
- **Handling Multi-Scale Crowns:** Connects directly to the shift from small regeneration detection toward merchantable crown handling in [[concepts/normal-forest]] and crown delimitation via [[concepts/crown-ownership]], where pixel sizes are much finer than crown diameter ($H$-resolution regime).
- **Illumination and Shadow Effects:** Boreal lighting conditions demand careful consideration of shadowed canopy sections during crop extraction for vision backbones like DINOv3, as shadow fractions alter the spectral signature significantly compared to illuminated foliage.

## Replication pseudocode

### Prerequisites

- Stereo aerial image pairs or raw LiDAR point clouds (LAS/LAZ format).
- Calibrated sensor positions, camera parameters, and terrain reference models (DTM/DEM).
- Image processing or photogrammetry software suite (e.g., Structure-from-Motion/Stereo matching engines).

### Procedure

```text
# General operational flow for photogrammetric CHM and orthophoto generation
1. Ingest raw aerial or UAV survey exposures alongside positional/IMU telemetry.
2. Execute aerial triangulation and bundle block adjustment to align exposures.
3. Compute a dense 3D point cloud using multi-view stereo or semi-global matching.
4. If ALS data exists:
     Align photogrammetric surface to the ALS-derived digital terrain model (DTM).
   Else:
     Filter ground points from stereo point cloud using morphological or progressive TIN filtering.
5. Derive digital surface model (DSM) from top elevation returns.
6. Compute canopy height model (CHM) by subtracting DTM from DSM:
     CHM = DSM - DTM
7. Orthorectify aerial imagery onto the surface model to generate true orthophotos.
8. Tile and export raster layers for downstream individual tree detection and crown segmentation.
```

### Gaps / not specified in paper

- Deep learning detection architectures (e.g., modern transformer detectors) are not covered, as the text predates recent vision foundation model developments.
- Specific hyperparameter values (e.g., cell sizes, search radii for local maxima, and confidence thresholds) depend on particular commercial flight specifications and are treated generally.

## Quotes

> "Denna typ av definitioner blir ganska allomfattande. De vanligaste typerna av fjärranalystekniker har dock varit skannrar som kan registrera reflekterat solljus, samt radar och lasersensorer." (p. 1)

> "In boreal forests, areas with high stem volume will appear as dark in most wavelength bands when analyzing optical satellite images... fraction of shadows is an important factor for the brightness of a forest pixel, in particular at our northern latitudes." (p. 20)

> "L-resolution where the objects are smaller than the image pixels... H-resolution may translate to 'several pixels per tree', while L-resolution translates to 'many trees per pixel.'" (p. 37)

## Related pages

- [[project/pipeline-overview]]
- [[concepts/canopy-height-model]]
- [[concepts/normal-forest]]
- [[concepts/crown-ownership]]
- [[concepts/dense-stand-detection]]
- [[concepts/literature-map-dense-itd]]
