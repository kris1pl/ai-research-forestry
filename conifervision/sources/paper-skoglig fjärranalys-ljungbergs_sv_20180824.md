---
title: "Skoglig Fjärranalys (Forest Remote Sensing)"
type: Source
tags: [remote-sensing, forestry, lidar, photogrammetry, satellite, chm]
status: stable
updated: 2026-10-23
description: "Foundational Swedish textbook compendium covering physics, sensor platforms, photogrammetry, laser scanning, and remote sensing methods for forestry."
source_file: raw/papers/Skoglig Fjärranalys-Ljungbergs_SV_20180824.pdf
authors:
  - "Heather Reese"
  - "Håkan Olsson"
  - "Mattias Nyström"
year: 2018
replication_status: not_applicable
related_methods:
  - methods/local-maxima
  - methods/chm-detection
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-23T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Skoglig Fjärranalys-Ljungbergs_SV_20180824.pdf
    title: "Skoglig Fjärranalys"
---

# Skoglig Fjärranalys (Forest Remote Sensing)

## Summary

*Skoglig Fjärranalys* is a comprehensive educational compendium produced by the Department of Forest Resource Management at the Swedish University of Agricultural Sciences (SLU), funded by the Erik Johan Ljungbergs Educational Fund. Authored primarily by Heather Reese, Håkan Olsson, and Mattias Nyström, the textbook serves as the foundational Swedish reference for remote sensing applications in forestry.

The text covers fundamental radiation physics, sensor mechanics (push-broom CCD arrays, matrix sensors, LiDAR, and SAR), operational platforms (satellites, aircraft, UAVs, and terrestrial/mobile systems), photogrammetric point matching versus laser scanning, and methods for area-based and single-tree estimation. It outlines the operational transition in Nordic forestry from traditional aerial stereo interpretation (e.g., the LMV method) to wall-to-wall 3D measurements via Airborne Laser Scanning (ALS) and digital photogrammetry.

## Key claims

- **3D point clouds vs 2D spectral limitations**: Optical 2D remote sensing is strongly correlated with forest shadowing and canopy closure, but saturates in mature boreal stands (~300 m³/ha) and cannot directly measure height or vertical stand density without 3D structural data (p. 5, 35).
- **Photogrammetric surface models vs ALS**: While image matching from stereo aerial photography yields high-density 3D surface models (such as Lantmäteriet's *Ytmodell från flygbilder*), it primarily resolves the outer canopy surface and fails to penetrate dense canopies to measure terrain ground elevation or lower understory density as airborne LiDAR does; an external DTM from ALS is typically required (p. 5, 36).
- **Scale and resolution thresholds**: Individual tree delineation (ITD) requires spatial resolutions finer than 2 m ("many pixels per tree"), with ~0.5 m pixels being practical for individual tree identification and ~5 cm drone imagery enabling branching architecture assessment for species identification (p. 36–37).
- **Spectral behavior of boreal canopies**: Boreal optical reflectance is largely captured by two dimensions: overall darkness/shadowing (driven by canopy volume and tree height, most pronounced in SWIR) and photosynthetic vitality (NIR reflectance, which separates broadleaf/deciduous from coniferous trees) (p. 19, 35).
- **Atmospheric dispersion and blue bands**: Rayleigh scattering ($1/\lambda^4$) heavily corrupts blue band radiance at higher altitudes and satellite scales, making it noisy and unsuitable for automated processing over broad areas, while diffuse blue illumination can aid human visual interpretation into canopy shadows (p. 18).

## Implications for our pipeline

- **Terrain Normalization & CHM generation**: Confirms the necessity in [[project/pipeline-overview]] of pairing photogrammetric point clouds (ODM / UAV) with a reliable ground baseline (such as CSF ground filtering or external ALS DTMs), as optical image matching cannot map the forest floor beneath dense canopies ([[concepts/canopy-height-model]]).
- **Resolution targets for tree detection**: Aligns with the multi-layer detection design in [[project/research-normal-forest]] and [[project/research-tree-detection-ensemble]]: high-resolution drone orthophotos (<10 cm GSD) provide structural crown features well above the ~0.5 m threshold needed for single-tree crown separation.
- **Spectral separation in species classification**: Reinforces why [[methods/dinov3-classification]] benefits from high-resolution RGB/NIR canopy crops, exploiting differences in crown branch patterns, foliage texture, and reflectance profiles between spruce, pine, and deciduous species.
- **Shadowing effects**: Highlights how solar geometry and self-shadowing create intra-crown contrast, which can aid local maxima detection on CHMs but causes challenges for optical segmentation if shadow boundaries are conflated with stand gaps.

## Replication pseudocode

The compendium is a broad academic textbook rather than an empirical algorithmic paper; specific algorithmic implementations (e.g., k-NN estimation or local maxima CHM filtering) are described conceptually.

### Prerequisites

- Calibrated multispectral imagery or drone RGB orthophoto.
- 3D photogrammetric or LiDAR point cloud (`.laz`).
- Digital Terrain Model (DTM) or ground filter algorithm (e.g., CSF).

### Procedure

```text
# Conceptual workflow for forest metric extraction (Chapters 3, 5, 6)
1. Acquire multi-view aerial imagery or ALS point cloud.
2. If using photogrammetry:
    a. Extract tie points and run bundle block adjustment (SfM).
    b. Generate dense 3D point cloud via dense image matching.
    c. Normalize heights against an ALS ground elevation model (DTM) to build a CHM.
3. If using ALS point cloud:
    a. Classify ground returns vs vegetation returns.
    b. Interpolate DTM from ground returns and DSM from canopy first returns.
    c. Compute CHM = DSM - DTM.
4. Scale-dependent analysis:
    a. Stand/area-based level: Aggregate height percentiles and canopy density metrics.
    b. Tree-level (ITD): Apply local peak detection on CHM (GSD < 0.5 m) to isolate individual crowns.
```

### Gaps / not specified in paper

- Explicit hyperparameter choices for single-tree segmentation algorithms (e.g., variable window filter parameters, morphological kernels).
- Quantitative precision benchmarks for UAV photogrammetric crown models in closed-canopy boreal conditions.

## Quotes

- *On the necessity of 3D data*: "Två-dimensionella (2D) data, som t.ex. vanliga satellitbilder har en uppenbar begränsning när det gäller att ge information om skogens höjd, vilket i sin tur också är viktigt för beräkning av andra variabler som t.ex. virkesförråd." (p. 35)
- *On resolution requirements for single-tree detection*: "När upplösningen blir bättre än ca 2 m, så närmar vi oss situationen 'många pixlar per träd'. Bilder med ca 0,5 m pixlar kan vara användbara för att identifiera enstaka träd. Vid ännu bättre upplösning, t.ex. drönarbilder med ca 5 cm pixlar, så får man en avbildningssituation som motsvara 'många pixlar per gren'." (p. 36–37)
- *On image-matching point clouds*: "Dock så erhålls inte lika bra information om skogens täthet som med laserdata, så skattningarna av t.ex. virkesförråd blir sämre... marken i regel inte syns i dessa 3D modeller. Istället behöver man använda en befintlig markmodell från laserskanning som referens för marknivån." (p. 5, 36)

## Related pages

- [[project/pipeline-overview]]
- [[concepts/canopy-height-model]]
- [[concepts/site-index-and-yield]]
- [[methods/local-maxima]]
- [[methods/chm-detection]]
