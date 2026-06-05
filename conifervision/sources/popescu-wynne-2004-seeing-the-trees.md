---
title: "Popescu & Wynne (2004) — LiDAR, multispectral fusion, CHM, local maxima"
type: source
tags: [lidar, chm, local-maxima, multispectral, tree-height]
status: active
updated: 2026-06-05
replication_status: partial
source_file: raw/papers/Seeing_the_Trees_in_the_Forest_Using_Lidar_and_Mul.pdf
authors: [Sorin C. Popescu, Randolph H. Wynne]
year: 2004
related_methods:
  - methods/local-maxima
  - methods/chm-detection
sources: []
---

# Popescu & Wynne (2004) — Seeing the Trees in the Forest

**Citation:** Popescu, S. C., & Wynne, R. H. (2004). Seeing the Trees in the Forest: Using Lidar and Multispectral Data Fusion with Local Filtering and Variable Window Size for Estimating Tree Height. *Photogrammetric Engineering & Remote Sensing*, 70(5), 589–604. DOI: [10.14358/PERS.70.5.589](https://doi.org/10.14358/PERS.70.5.589)

**Local file:** `raw/papers/Seeing_the_Trees_in_the_Forest_Using_Lidar_and_Mul.pdf`

## Summary

Classic small-footprint airborne LiDAR study (≈0.65 m footprint, ≈0.7 m shot spacing) over pine and deciduous stands in the southeastern US. The authors build a **canopy height model (CHM)** from first-return DSM minus terrain, then estimate plot-level dominant tree height by detecting **individual tree tops** with **local maximum (LM) filtering** using **variable window size** (square vs circular). **Multispectral fusion** (ATLAS, leaf-off) separates conifer vs deciduous to tune window sizing and improves pine height models; deciduous plots often did better without forest-type-specific window calibration.

Regression on 0.017-ha plots: pine dominant height **R² ≈ 97%**; deciduous **R² ≈ 79%**. Circular LM windows fit pines better; square windows slightly better for some deciduous cases.

## Key claims

1. **CHM = DSM_tree − DTM** — terrain from slope-based ground classification; top DSM uses **max elevation per 0.25 m² cell** + kriging (0.5 m grid) to reduce apex underestimation vs using all first returns.
2. **Individual-tree LM on CHM** outperforms using all pulse heights within plot footprints for mean height estimation.
3. **Variable window LM** — window size scales with expected crown size from height–crown field relations; too small → commission, too large → omission.
4. **Circular vs square windows** — circular LM preferred for conifers (single apex); both tested systematically.
5. **LiDAR + optical fusion** — species class from multispectral image resampled to CHM grid; fusion helps pine height estimation; deciduous often better without type-specific LM calibration.
6. Small-footprint LiDAR at individual-tree scale supports **precision forestry / automated inventory** when combined with optical data for species context.

## Implications for our pipeline

| Our stage | Relevance |
|-----------|-----------|
| [[methods/chm-detection]] | Strong precedent for CHM from 3D/laser ground model; max-per-cell DSM before CHM; grid resolution matters (here 0.5 m). |
| [[methods/local-maxima]] | Direct ancestor of **variable-window local maxima on height surface** — validates sliding/window LM before modern deep detectors. |
| [[methods/merge-detections]] | Paper works at **tree-top / crown** level then plot aggregation; we merge LM with CHM/DEIMv2 — same tension between geometric peaks and model detections. |
| Multispectral / species layers | Analog to using **height strata + species context** (our DINOv3 path); fusion improved pines more than deciduous. |
| Drone orthophoto | Different sensor than airborne small-footprint LiDAR, but CHM + LM logic transfers; verify window rules on our GSD and species mix. |

## Replication pseudocode

**Status:** partial — main flow is clear; ground classification and exact window-sizing coefficients are in Popescu (2002) / field calibration, not fully in this paper.

### Prerequisites

- Small-footprint airborne LiDAR: first returns (+ optionally full waveform), georeferenced point cloud.
- Field inventory: dominant/codominant tree heights, DBH, species; height–crown relationship for window sizing.
- Optional: leaf-off multispectral imagery coregistered to LiDAR (paper: ATLAS, 4 m → resampled to 0.5 m CHM grid).
- Plot footprints ≈ 0.017 ha (FIA-style subplots) for validation.

### Procedure

```text
INPUT: lidar_points (x, y, z, return_number, ...), optional_multispectral_image, field_plots

# 1 — Terrain (DTM)
ground_points = classify_ground(lidar_points, method="slope-based iterative")  # details: Popescu 2002
DTM = interpolate_to_grid(ground_points, cell_size=0.5 m)

# 2 — Canopy surface (top DSM)
first_returns = filter(lidar_points, return == first)
for each cell c of size 0.25 m² on grid:
    z_top[c] = max(elevation of first_returns in c)
top_DSM = kriging_interpolate(z_top, target_cell=0.5 m)

# 3 — CHM
CHM = top_DSM - DTM   # per-cell canopy height

# 4 — Optional species layer for window calibration (fusion)
if multispectral_available:
    species_map = classify(maxlik, classes=[open, deciduous, conifer])
    species_map = resample(species_map, to_grid=CHM, method=nearest_neighbor)
else:
    species_map = null

# 5 — Height–crown model (from field data)
# crown_size = f(tree_height)  # linear, species-specific coefficients from inventory

# 6 — Variable-window local maxima on CHM
tree_tops = []
for each cell p in CHM:
    h_local = height_at(p)  # or neighborhood estimate
    w = window_size_from_height_crown_model(h_local, species_map[p])  # square n×n or circular radius
    if p == local_maximum(CHM, window=w, shape in {square, circular}):
        tree_tops.append((x(p), y(p), CHM[p]))

# 7 — Plot-level height (validation path in paper)
for each field_plot P:
    trees_in_P = tree_tops within geometry(P)
    h_lidar_dom = mean_or_max_height(trees_in_P matching dominant/codominant rules)
    compare h_lidar_dom to h_field_dom via regression  # report R²

OUTPUT: CHM, tree_top_locations, plot-level predicted dominant height
```

### Gaps / not specified in paper

- Full **ground-point classification** algorithm (referenced to Popescu, 2002).
- Exact **height–crown regression coefficients** and window-size lookup tables.
- Kriging variogram settings for top DSM.
- Commission/omission tuning rules beyond “window too small / too large”.
- Our stack uses **drone 3D + DEIMv2** — replace ATLAS fusion with equivalent species/height strata layers.

### Mapping to our pipeline

| Paper step | Our analogue |
|------------|----------------|
| DTM / ground model | Laser ground model in [[project/pipeline-overview]] |
| CHM | [[methods/chm-detection]], [[concepts/canopy-height-model]] |
| Variable LM on CHM | [[methods/local-maxima]] (sliding window) |
| Species-aware windows | Possible future layer; DINOv3 / forest type |
| Tree tops + merge with detectors | [[methods/merge-detections]] |

## Contradictions / gaps vs current practice

- **Sensor era:** 2004 airborne LiDAR + ATLAS — not drone RGB/DEIMv2; window and CHM parameters must be re-tuned for our data.
- **Output unit:** plot-level dominant height for inventory, not full instance segmentation masks like DEIMv2.
- **Underestimation:** authors note lidar often samples crown shoulders; max-cell DSM mitigates but does not remove bias — compare with our [[project/pipeline-overview]] height workflow.
- No conflict with using LM + CHM merge; paper **supports** LM on CHM as a defensible baseline.

## Quotes

> "The tree canopy height model was computed as the difference between tree canopy hits and the corresponding lidar-derived terrain elevation values." (CHM section, ~p. 593)

> "The second method to estimate tree heights was based on single-tree identification using a variable window technique with local maximum (LM) focal filtering." (~p. 594)

> "If the filter size is too small or too large, errors of commission or omission respectively, occur." (~p. 594)

> "Using lidar and optical data fusion to differentiate between forest types provided better results for estimating average plot height for pines." (Abstract)

## Related pages

- [[concepts/canopy-height-model]]
- [[methods/local-maxima]]
- [[methods/chm-detection]]
- [[methods/merge-detections]]
- [[project/pipeline-overview]]
