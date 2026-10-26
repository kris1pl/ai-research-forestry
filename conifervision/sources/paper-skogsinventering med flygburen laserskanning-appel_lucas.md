---
title: "Skogsinventering med flygburen laserskanning: Laserskanning och fotogrammetri inom skogsbruket"
type: Source
tags: [lidar, chm, individual-tree-detection, uav, point-cloud, forestry]
status: stable
updated: 2026-10-21
description: "Bachelor's thesis evaluating single-tree ITD and CHM generation from national low-density ALS vs. high-density UAV-LiDAR using LiForest software in Finland."
source_file: raw/papers/Skogsinventering med flygburen laserskanning-Appel_Lucas.pdf
authors:
  - Nils Lucas Appel
year: 2017
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-21T17:30:00Z
sources:
  - id: primary
    resource: raw/papers/Skogsinventering med flygburen laserskanning-Appel_Lucas.pdf
    title: "Skogsinventering med flygburen laserskanning: Laserskanning och fotogrammetri inom skogsbruket"
---

# Skogsinventering med flygburen laserskanning: Laserskanning och fotogrammetri inom skogsbruket

## Summary

This bachelor's thesis (Novia University of Applied Sciences, Vaasa, Finland) investigates airborne laser scanning (ALS) and UAV-based photogrammetry/LiDAR workflows in Finnish forestry. Appel compares low-density public ALS data from the National Land Survey of Finland (Maanmittauslaitos / LMV, ~0.43 points/m², flown May 2008) against high-density UAV-LiDAR data (named `sibbo2`, flown April 2016) over a 2.5-hectare forest plot in Sipoo (Sibbo), Finland.

Using GreenValley's **LiForest 2.1** software and **CloudCompare**, the study implements an Individual Tree Detection (ITD) / single-tree method (*enskilda-träd-metoden*) on triangulated TIN digital elevation models (DEM), digital surface models (DSM), and canopy height models (CHM = DSM − DEM). Detection at a height cutoff of $H \ge 2\text{ m}$ isolated 322 stems in LMV vs. 391 stems in UAV-LiDAR (a difference of only 69 stems). When restricting analysis to merchantable trees ($H > 8\text{ m}$), the high-density UAV data resolved 340 stems compared to 227 for LMV. Mean height across all $\ge 2\text{ m}$ detections differed by only 11 cm (14.71 m for LMV vs. 14.60 m for UAV), though LMV showed systematic upper-canopy outliers (up to 26–27 m) caused by unclassified air points (fog/birds).

## Key claims

- **Point density vs. detection yield ($H \ge 2\text{ m}$):** Despite a high point density contrast between LMV (~0.43 pts/m²) and UAV-LiDAR, the total detected stem count differed by only 69 trees across 2.5 ha (322 LMV vs. 391 UAV).
- **Merchantable canopy detection ($H > 8\text{ m}$):** In the dominant/co-dominant tier ($>8\text{ m}$), UAV-LiDAR detected substantially more stems (340 vs. 227), demonstrating that low-density ALS misses subordinate or tightly clustered overstory stems.
- **Canopy height model parity:** The average detected tree height across all stems differed by only 0.11 m between LMV (14.71 m) and UAV (14.60 m).
- **Artifact vulnerability in sparse ALS:** LMV data suffered from high noise outliers (returns at 26–27 m attributed to atmospheric reflections, birds, or cloud/fog), inflating the mean height of trees $>8\text{ m}$ in LMV to 18.76 m vs. 15.86 m for UAV (a 2.90 m discrepancy).
- **Crown segmentation mergers:** LiForest watershed/segmentation frequently clumped adjacent crowns into single large polygon areas (up to 125–141 m² crown area), skewing individual crown diameter statistics.
- **Operational forest inventory in Finland:** National Area-Based Approaches (ABA / *arealbaserade beräkningar*) through Metsäkeskus (Minskog.fi) routinely achieve $\pm 3\text{ m}^2/\text{ha}$ basal area, $\pm 3\text{ cm}$ mean diameter, $\pm 2\text{ m}$ mean height, and $\pm 20\%$ volume in development classes 02–04, but accuracy drops to ~50% stem count in young stands (T1/T2 $<2\text{ m}$).

## Implications for our pipeline

- **Noise filtering prior to CHM generation:** Low-point and high-flyer/air-point filtering is essential. As shown in LMV data, isolated aerial reflections distort local maxima and upper-envelope surfaces unless strict statistical outlier filters (e.g., SOR or LAS class 7/noise exclusion) are applied in [[project/pipeline-overview]].
- **Height stratification boundaries:** Appel uses a 2.0 m cutoff to exclude field-layer shrubs/regeneration, and an 8.0 m cutoff to isolate dominant canopies. This aligns closely with Conifervision's stratified layers (lower 0.3–4 m, upper 4–30 m, and R-class 0–7.77 m in `preprocess_2d_raster_layer.py`).
- **Crown clumping in pure raster watershed:** LiForest's raster-based crown delineation regularly suffered from under-segmentation in dense canopies (merging adjacent crowns into massive polygons $>100\text{ m}^2$). This validates the need for machine-learning-driven bounding box proposals ([[methods/deimv2-canopy]]) and multi-layer peak refinement rather than pure morphological watershed.
- **Point density requirement for crown structure:** While 0.5–1 pts/m² ALS suffices for area-based stand averages, individual tree segmentation and crown shape parameterization require $>10\text{ pts/m}^2$, supporting our use of high-resolution photogrammetric/UAV point clouds.

## Replication pseudocode

### Prerequisites

- Point cloud input (LAS/LAZ format) with return numbers (first, intermediate, last returns).
- Pre-processing tools: CloudCompare or PDAL / CSF ground filter.
- Raster modeling software: LiForest 2.1 (GreenValley International) or open-source equivalents (WhiteboxTools / lidR).

### Procedure

```text
# High-level reconstruction of Appel's LiForest ITD workflow

1. Point Cloud Preprocessing:
   - Import point cloud (UAV "sibbo2" or NLS/LMV ALS).
   - Eliminate low points (multipath/underground bounce reflections) and aerial noise (birds/mist).
   - Classify ground returns (LAS Class 2) via TIN / progressive densification.
   - Height-stratify vegetation per ICSM / LiForest specifications:
     * Low vegetation: 0.0 - 0.3 m
     * Medium vegetation: 0.3 - 2.0 m
     * High vegetation: > 2.0 m

2. Elevation & Surface Modeling:
   - Generate DTM / DEM from Class 2 ground points using TIN interpolation at 1.0 m grid resolution (Xsize=1.0, Ysize=1.0).
   - Generate DSM from low, medium, and high vegetation first returns at 1.0 m grid resolution.
   - Compute Canopy Height Model:
     CHM = DSM - DEM

3. Individual Tree Detection (ITD) & Segmentation:
   - Apply LiForest single-tree detection algorithm on the CHM:
     * Identify local canopy maxima (crown apex / tree location X, Y, Z).
     * Filter candidate peaks: height threshold >= 2.0 m (or >= 8.0 m for merchantable canopy).
     * Delineate crown boundaries around peaks using watershed / morphological boundary tracing.
     * Calculate attributes for each tree ID:
       - Coordinates (X, Y)
       - Tree height (H = Z_peak - Z_dem)
       - Crown diameter (D_crown)
       - Crown area (A_crown)

4. Stand-Level Evaluation:
   - Export detection table (ID, X, Y, H, D_crown, A_crown).
   - Filter by height thresholds (H >= 2.0 m and H > 8.0 m).
   - Compare stem count, mean height, mean crown diameter, and mean crown area between sensor sources.
```

### Gaps / not specified in paper

- **Exact LiForest segmentation kernel:** The specific window size (fixed vs. variable window) for local maxima detection and smoothing filter sigma on the CHM are not detailed.
- **UAV point density / sensor metadata:** Exact point density per m² of `sibbo2`, flight altitude, flight speed, and camera/laser sensor model on the UAV are omitted (only noted as "betydligt högre punkttäthet" collected on 2016-04-16).
- **Ground truth field validation:** No stem-mapped field inventory was conducted on the 2.5 ha Sibbo plot to establish true commission vs. omission rates; comparisons are purely relative between LMV and UAV.

## Quotes

- **On point density limits for single-tree detection (p. 18):**
  > "Om däremot enskilda träd ska analyseras behövs ett betydligt tätare punktmoln, eftersom speciellt de dominerande stammarna ger flera returer per puls. Vid enskilda trädmetoden och vid mätningar av kronform, behöver punkttätheten vara > 10 pulser per kvadratmeter för att uppnå bra resultat."
- **On stem count comparison between UAV and NLS ALS (p. 28–29):**
  > "Resultatet visar att informationen som samlats in med drönare endast identifierar 69 stammar fler än Lantmäteriverkets punktmoln på samma provyta, trots skillnaden i antal punkter per m²... Antalet stammar över 8 meter blev 340 st för sibbo2 jämfört med 227 st för LMV punktmoln."
- **On crown over-merging in dense forest (p. 29):**
  > "De stora kronareorna beror antagligen på att flera intilliggande kronor har tolkats som en enda stor trädkrona av Liforest."
- **On aerial noise distorting ALS heights (p. 29):**
  > "LMV punktmoln flera träd uppemot 26-27 m vilket är orimligt för detta bestånd. Förklaringen är att det fortfarande har funnits punkter som inte eliminerats i luften ovanför träden och antagligen uppkommit på grund av dimma, fåglar eller dylikt."

## Related pages

- [[concepts/canopy-height-model]] — CHM generation (DSM − DTM) and rasterization methods
- [[methods/local-maxima]] — Local maxima detection heuristics and window configurations
- [[methods/chm-detection]] — CHM height stratification and detection
- [[concepts/dense-stand-detection]] — Challenges with interlocking crowns and understory omission
- [[project/pipeline-overview]] — Operational AREA pipeline processing photogrammetric point clouds into CHMs
