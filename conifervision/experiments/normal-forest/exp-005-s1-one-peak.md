---
title: exp-005 S1 one peak in the core
type: Note
description: "S1 count for exp-005 on stand 17568, cut from area 663: SAHI 800 boxes against local-maxima peaks at least 7 m tall. Not a CVAT sample. AREA 665 is not this count."
tags: [normal-forest, exp-005, crown-ownership]
status: draft
updated: 2026-11-02
---

# exp-005 — one peak in the core (S1)

Parent: [[experiments/normal-forest/exp-005-normal-forest-ownership-smoke]].

AREA id 663-17568. Stand 17568, class G2, about 10.4 ha, cut from area 663 (`Brännvattsliden`). Working prefix `gs://conifervision-areas/exp005-663-17568`. No training, no CVAT.

AREA 665 was the wrong cohort (R-class small trees). It is not this count.

Comparison: crowns from RGB `svk_full`, SAHI window 800 px, overlap 0.30, confidence 0.5, against local-maxima peaks. Tree height is at least 7 m. This count read that height from the peak's Z. A CHM detection is not this measurement. The core is the central half of the box: origin `(x + 0.25w, y + 0.25h)`, size `0.5w` by `0.5h`.

Detection totals:

| Layer | Detections |
|---|---:|
| Local maxima, Z ≥ 7 m, center inside the stand | 8947 |
| SAHI 800 px | 29058 |

The core count below uses the 8981 SAHI 800 boxes whose center lies inside the stand polygon.

| Peaks in the core | Boxes | Share |
|---|---:|---:|
| exactly 1 | 6047 | 67.3% |
| 2 or more | 70 | 0.8% |
| 0 | 2864 | 31.9% |
| total | 8981 | 100% |

The other 20077 SAHI 800 boxes have their center outside the stand polygon. They sit on the orthophoto around the stand. The local-maxima file is already clipped to the stand and to 7 m, so nearly all of these boxes are empty. 19 of them are centered just outside the boundary and their core still reaches a peak inside.

| Peaks in the core | Boxes outside the stand | Share |
|---|---:|---:|
| 0 | 20058 | 99.9% |
| exactly 1 | 19 | 0.1% |
| 2 or more | 0 | 0% |
| total | 20077 | 100% |

A box with one peak stays. Two peaks, or none, drop out. Peaks are separable, so this step does not end the experiment. The bar is signed: precision ≥ 0.85 and agreement ≥ 0.80. The 6047 boxes are the pool. The reading sample is on the parent page: 150 boxes, precision 0.973, agreement 0.80.

Full detection: `gs://conifervision-areas/exp005-663-17568/preds/preds_rgb_exp005-663-17568_dinov3_model_deimv2_dinov3_s_trees_svk_full_20261028_120252.json`

Viewer layer, the 6047 boxes: `gs://conifervision-areas/exp005-663-17568/preds/preds_rgb_exp005-663-17568_dinov3_model_deimv2_dinov3_s_trees_svk_full_one_peak_20261028_130401.json`
