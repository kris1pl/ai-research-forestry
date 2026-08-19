---
title: Miao et al. (2024) — Pseudo tree crown (PTC) for UAV individual tree species classification
type: Source
description: "Citation: Miao, S.; Zhang, K.; Zeng, H.; Liu, J. Improving Artificial-Intelligence-Based Individual Tree Species Classification Using Pseudo Tree Crown Derived from Unmanned Aerial Vehicle Imagery. *…"
tags:
  - uav
  - orthophoto
  - ptc
  - species-classification
  - resnet50
  - pytorch
  - urban-trees
  - 3d
status: stable
updated: 2026-06-03
generated:
  by: agent:conifervision-wiki
  at: 2026-06-03T12:00:00Z
replication_status: partial
source_file: raw/papers/remotesensing-16-01849-v2.pdf
authors:
  - Shengjie Miao
  - Kongwen (Frank) Zhang
  - Hongda Zeng
  - Jane Liu
year: 2024
related_methods:
  - methods/dinov3-classification
sources: []
---
# Miao et al. (2024) — PTC from UAV imagery for individual tree species classification

**Citation:** Miao, S.; Zhang, K.; Zeng, H.; Liu, J. Improving Artificial-Intelligence-Based Individual Tree Species Classification Using Pseudo Tree Crown Derived from Unmanned Aerial Vehicle Imagery. *Remote Sensing* **2024**, *16*, 1849. DOI: [10.3390/rs16111849](https://doi.org/10.3390/rs16111849)

**Local file:** `raw/papers/remotesensing-16-01849-v2.pdf`

## Summary

Urban **individual tree species (ITS)** classification from **UAV orthophotos** (0.03 m GSD, Fujian Normal University campus, five species, **696** field-validated crown patches). The main contribution is **pseudo tree crown (PTC)** — a **3D-style reprojection** of each nadir crown patch (green band) to exaggerate crown structure before feeding classifiers. Compared to nadir-only green-band patches, PTC improves accuracy by **~12–14%** for deep models and **~9%** for random forest.

Four classifiers tested: **PyTorch + ResNet50** (best: **98.26%** test accuracy with PTC vs **86.7%** nadir), TensorFlow 2 + ResNet50, YOLOv5s + CSPDarknet53, and RF. PyTorch was fastest (~44 min / 50 epochs) and most stable on the test split. PTC is **robust to azimuth** (−120° / 90° / 120° at 75° elevation) and **coarser GSD** (accuracy stays >90% until ~10× downsampling vs nadir dropping to 70–80%).

**Scope note:** Urban isolated trees, not dense production forest stands; no linkage to CHM or detection merge in this paper.

## Key claims

1. **PTC** — reform nadir crown greyscale into a pseudo side/3D view (matplotlib 3D plot settings: default **azimuth −120°**, **elevation 75°**) to increase inter-species feature separability for CNNs.
2. **PTC vs nadir (green band only)** — all four classifiers gain; PyTorch: 86.7% → 98.2% (Table 9).
3. **PyTorch + ResNet50 + PTC** — recommended combination: >95% from ~40 epochs; **98.26%** overall with 64×64 inputs, 50 epochs, SGD.
4. **Angle sensitivity** — azimuth/elevation variants still >95% final accuracy (Section 4.3).
5. **Resolution sensitivity** — PTC maintains ~90%+ at 10× coarser native resolution; nadir patches degrade to 70–80% (Sections 4.4–4.5).
6. **Species difficulty** — *Archontophoenix alexandrae* easiest (distinct trunk/crown); *Ficus microcarpa* hardest (large, intertwined crowns).
7. **Future work (authors)** — fuse **UAV LiDAR** (Hesai XT32 on same platform) to relate physical crowns to PTC and DBH.

## Implications for our pipeline

| Our stage | Relevance |
|-----------|-----------|
| [[project/pipeline-overview]] §3 Species classification | Optional **input reformation** before DINOv3 crops/embeddings — not in production today. |
| [[methods/dinov3-classification]] | Analog: per-tree **crops** from orthophoto; PTC is an alternative patch representation vs raw nadir RGB. |
| [[methods/deimv2-canopy]] | Paper uses YOLOv5 for **classification** comparison only, not crown delineation; our DEIMv2 role differs. |
| Detection / CHM | **Not addressed** — assumes manual per-tree patches (ArcGIS shapefiles). |
| Weak labels | Paper uses **fully validated** field species per patch; our weak-label loop is orthogonal but shares “limited labels” motivation in conclusions. |

**Transfer hypothesis:** If species classes are confused on nadir orthophoto crops, experiment with PTC-like views on DINOv3 input tiles (after [[methods/merge-detections]] boxes). Validate on conifer/mixed forest, not urban campus species.

## Replication pseudocode

**Status:** partial — PTC rendering is described at a high level (green band, 3D projection angles); exact matplotlib/ArcGIS steps and RF feature extraction are under-specified. Code available **on request** per authors (not in repo).

### Prerequisites

- UAV orthophoto (paper: **0.03 m** GSD, RGB, CGCS2000 / Gauss–Krüger; Sony a6000, 100 m flight).
- Per-tree crown polygons or patches; species verified in field.
- Python with PyTorch / TensorFlow / YOLOv5 as needed; ArcGIS 10.2 used for initial tiling (paper).

### Procedure

```text
INPUT: orthophoto_RGB, tree_polygons_or_boxes, species_labels

# 1 — Sample preparation (paper workflow)
import_to_GIS(orthophoto)
build_image_pyramid()
for each field-validated tree:
    crop_nadir_patch(polygon)   # per-species tiles; paper: 696 total samples

# 2 — PTC generation (per patch)
band = extract_green_channel(patch)
array = raster_to_array(band)
clip_values(array, max=255)   # pixels > 255 reset per paper
configure_subplot(projection_mode=3d)
PTC_image = render_pseudo_crown(
    array,
    azimuth_deg=-120,      # paper default; also tested 90, 120
    elevation_deg=75
)
resize_or_crop(PTC_image, target=64 x 64 pixels)

# 3 — Classifier training (PyTorch + ResNet50 example)
split_data(train_fraction=TBD, test_fraction=TBD)  # paper: "1:4 testing and training" — clarify ratio
for epoch in 1..50:
    train(ResNet50, input=PTC_or_nadir_green, size=64x64, batch=4,
          optimizer=SGD, lr=1e-4, momentum=1e-3, shuffle=True)

# 4 — Evaluation
report_accuracy, confusion_matrix, precision/recall/F1 per species
compare(PTC vs nadir_green, classifiers=[PyTorch, TF2, YOLOv5, RF])
optional: sweep_azimuth_elevation; downsample_GSD(factors=[3,5,10])
```

### Gaps / not specified in paper

- Exact code for PTC 3D rendering (matplotlib parameters beyond azimuth/elevation).
- Train/test split interpretation of **1:4** (testing vs training order in text).
- RF input features (dimensionality, HOG, pixel vector, etc.).
- How patches align when crowns overlap (*Ficus microcarpa* issue) — manual clean samples only.
- Generalization beyond five urban species and single campus.
- Integration with **LiDAR** crown geometry (future work in paper).

## Quotes

> “PTC can enhance the classification results across all image classifiers tested by at least 10%.” (Introduction)

> “For the creation of our PTC, azimuth angles of −120° and an elevation angle of 75° were used.” (Section 3.1)

> “Clearly, all ML classifiers were enhanced by 12–14% and about 9% in RF.” (Section 4.3, Table 9)

> “The PyTorch classifier achieved the highest overall classification accuracy of 98.26%.” (Section 4.2)

## Related pages

- [[concepts/pseudo-tree-crown]]
- [[methods/dinov3-classification]]
- [[project/pipeline-overview]]

## Contradictions

None with [[sources/popescu-wynne-2004-seeing-the-trees]] — different sensors (UAV RGB vs airborne LiDAR) and tasks (species vs height). Complementary: both stress that **how** the 2D/3D surface is prepared strongly affects downstream ML.
