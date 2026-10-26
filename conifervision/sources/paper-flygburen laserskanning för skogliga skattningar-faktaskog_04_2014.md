---
type: Source
title: "Flygburen laserskanning för skogliga skattningar"
description: "SLU review of area-based and individual tree detection (ITD) methods from airborne laser scanning (ALS) for Swedish forest inventory."
tags: [als, lidar, itd, chm, forestry, sweden, area-based]
status: stable
updated: 2026-06-09
source_file: raw/papers/Flygburen laserskanning för skogliga skattningar-faktaskog_04_2014.pdf
authors:
  - Eva Lindberg
  - Johan Holmgren
year: 2014
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-06-09T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Flygburen laserskanning för skogliga skattningar-faktaskog_04_2014.pdf
    title: "Flygburen laserskanning för skogliga skattningar"
related_methods:
  - methods/local-maxima
  - methods/chm-detection
---

# Flygburen laserskanning för skogliga skattningar

## Summary

This publication from the Swedish University of Agricultural Sciences (SLU *Fakta Skog* series, No. 4, 2014) provides an overview of airborne laser scanning (ALS) applications in Swedish forest inventory. It contrasts **area-based approaches (ABA)**, which predict stand metrics across raster grids (e.g., 10×10 m or 12.5×12.5 m) using height percentiles and regression/kNN, with **individual tree detection (ITD)** methods that require higher point densities (> 5 points/m²).

The authors detail ITD workflows starting from raster surface models (CHM) constructed either from raw binning or via 3D geometric crown templates (ellipsoids). They discuss the structural limits of 2.5D surface models (inability to detect understory trees and under-segmentation in dense canopies) and review full 3D point-cloud clustering techniques developed at SLU to delineate understory and intermediate canopy strata.

## Key claims

- **Point density trade-off:** Area-based methods function effectively with low point densities (~0.5 points/m²), whereas individual tree detection (ITD) requires high-density ALS (> 5 points/m²) (p. 3).
- **Area-based requirements:** Parametric multiple regression models require a minimum of ~30 field plots, whereas non-parametric techniques (Random Forests, kNN, k-MSN) require ≥ 100 field plots across representative forest conditions (p. 3).
- **CHM from 3D templates:** Fitting 3D geometric ellipsoids directly to point clouds creates a correlation-based surface model that outperforms basic highest-return binning (e.g., 0.5×0.5 m cells) by incorporating structural prior knowledge (p. 3).
- **Canopy model limitation:** Surface models (2.5D CHMs) only represent the outermost top canopy layer. Detecting sub-canopy or suppressed trees requires 3D point cloud clustering directly in point space (p. 3–4).
- **Crown segmentation errors:** Over-segmentation and under-segmentation occur frequently in dense stands where crowns interlock. Connecting segments statistically to field inventory data allows modeling zero, one, or multiple stems per segment using geometric metrics like width-to-height ratio (p. 4).
- **Species identification:** Individual tree segments allow species classification based on structural crown geometry and return intensity distributions (e.g., separating Scots pine and Norway spruce) (p. 4).

## Implications for our pipeline

- **Limits of 2D CHM detection:** Corroborates why our 2D terrain-normalized CHM pipeline ([[project/pipeline-overview]], [[concepts/canopy-height-model]]) struggles with intermediate and suppressed trees ([[concepts/understory-tree-detection]]). A 2D CHM cannot represent stems obscured beneath upper canopy crowns.
- **Ellipsoid modeling prior:** Holmgren & Lindberg's method of fitting ellipsoid templates to raw returns provides theoretical justification for combining morphological assumptions with peak finding, relevant to [[methods/local-maxima]] and crown boundary reasoning in [[concepts/crown-ownership]].
- **Segment-to-stem mapping:** When handling dense plots where crowns coalesce, evaluating one detection box/segment as potentially harboring multiple trees (or adjusting diameter distributions via crown width/height ratios) aligns with challenges addressed in [[concepts/dense-stand-detection]] and [[project/research-normal-forest]].

## Replication pseudocode

### Prerequisites

- High-density point cloud (`.las` / `.laz`) with ALS pulse density > 5 pts/m².
- Classified ground returns for DTM normalization.
- Calibrated field plot measurements (stem positions, DBH, species, height).

### Procedure

```text
# Area-based Approach (ABA)
1. Normalize ALS point elevations by subtracting DTM: Z_norm = Z_pts - DTM.
2. Bin points into regular grid cells (e.g., 12.5 x 12.5 m).
3. Compute height percentiles (e.g., H20, H50, H95, H100) and density metrics (ratio of returns > height threshold).
4. Fit regression / k-MSN models using N >= 30 (parametric) or N >= 100 (non-parametric) field plots.
5. Predict stand volume, basal area, and mean diameter across target grid.

# Individual Tree Detection (ITD) - CHM / Geometric Template
1. Generate CHM:
   a. Standard: Highest return within 0.5 x 0.5 m cells.
   b. Geometric: Fit 3D ellipsoid models across local point neighborhoods and compute correlation surface.
2. Detect local maxima (tree tops) on the surface model.
3. Delineate crown boundaries around peaks (watershed or region growing).
4. Compute segment morphology (width, height, width-to-height ratio).
5. (Optional 3D refinement): Seed 3D clusters from 2D peaks and cluster sub-canopy returns in 3D point space.
6. Extract intensity and crown shape features per segment for species classification.
```

### Gaps / not specified in paper

- Exact mathematical parameters for the crown ellipsoid model (semi-axes ratios, fitting cost functions; referenced to Holmgren & Lindberg 2013).
- Specific height cutoff thresholds separating ground/understory noise from tree canopy.
- Quantitative classification accuracy rates for tree species separation.

## Quotes

- **Page 3 (ITD vs. ABA density requirements):**  
  > "Med täta laserdata (> 5 punkter/m2) kan även enskilda träd urskiljas. Med hjälp av automatiserade metoder liknande bildanalys kan träden ringas in, så kallad segmentering."
- **Page 3 (Limitation of surface models):**  
  > "Ytmodeller beskriver endast det högsta skiktet i skogen. Täta laserdata innehåller även mätningar från träd och buskar under det högsta skiktet och därför har metoder utvecklats för att avgränsa trädkronor i tre dimensioner direkt från laserreturerna."
- **Page 4 (Dense stand crown fusion):**  
  > "I idealfallet ska varje träd ge upphov till ett segment. I praktiken omfattar dock en del av segmenten flera träd. Det kan vara träd som står tätt intill varandra och vars kronor går in i varandra."

## Related pages

- [[concepts/canopy-height-model]] — Construction of DSM/DTM height surfaces from point clouds.
- [[concepts/understory-tree-detection]] — Structural limitations of top-down elevation models.
- [[concepts/point-cloud-individual-tree-segmentation]] — Direct 3D clustering vs. 2.5D CHM approaches.
- [[concepts/dense-stand-detection]] — Challenges of overlapping and interlocked crowns.
- [[methods/local-maxima]] — Canopy surface peak detection.
- [[project/pipeline-overview]] — Production pipeline using photogrammetric CHM rasters and DEIMv2/LM.
