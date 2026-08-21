---
type: Source
title: "Individual tree crown delineation in high resolution aerial RGB imagery using StarDist-based model"
description: "Adapts the StarDist cell segmentation model using star-convex polygons and a modified sparse-annotation loss function to achieve over 92% tree crown delineation accuracy in mixed forests."
tags: [tree-detection, instance-segmentation, stardist, u-net, rgb-imagery]
status: stable
updated: 2026-08-21
source_file: raw/papers/Individual_tree_crown_delineation_in_high_resolution_aerial_RGB_imagery_using_StarDist-based_model-1-s2.0-S0034425725000227-main.pdf
authors: [Fei Tong, Yun Zhang]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-08-21T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Individual_tree_crown_delineation_in_high_resolution_aerial_RGB_imagery_using_StarDist-based_model-1-s2.0-S0034425725000227-main.pdf
    title: "Individual tree crown delineation in high resolution aerial RGB imagery using StarDist-based model"
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/merge-detections
---

# Individual tree crown delineation in high resolution aerial RGB imagery using StarDist-based model

## Summary

This paper introduces the first application of the **StarDist** model (originally developed for cell nuclei segmentation in microscopy) to individual tree crown delineation (ITCD) in complex mixed forests. Instead of using standard axis-aligned bounding boxes (like Mask R-CNN) which struggle with overlapping crowns, StarDist models tree crowns as **star-convex polygons** predicted via a U-Net architecture. 

To address the challenge of incomplete forest annotations (where only dominant/distinguishable trees are labeled), the authors modify the standard StarDist loss function with a **sparse-annotation constraint** ($p > 0$). This prevents unlabeled trees in the background from being treated as negative samples, stabilizing training. Tested on 15 cm aerial RGB imagery in the Acadia Research Forest (Canada), the model achieved a delineation accuracy exceeding 92%, outperforming Mask R-CNN by over 6%, particularly on smaller-sized tree crowns.

## Key claims

* **Star-Convex Representation:** Tree crowns are represented by a center probability $p(i, j)$ and $n = 32$ radial distances $\{d_k(i, j)\}_{k=1}^n$ to the boundary, which naturally fits the roundish geometry of tree crowns (p. 4).
* **Sparse Annotation Loss:** Modifying the binary cross-entropy loss to only calculate object probability loss on annotated pixels ($p > 0$) prevents the model from penalizing unannotated co-dominant or intermediate trees in the background (p. 6).
* **Superiority over Mask R-CNN:** StarDist achieved delineation accuracies of **92.95%** (Testing Area 1) and **92.48%** (Testing Area 2), outperforming Mask R-CNN by 8.46% and 6.90% respectively (p. 9).
* **Small Tree Performance:** StarDist significantly reduces omission errors for smaller tree crowns (area < 1000 pixels / ~22.5 m²) compared to Mask R-CNN and U-Net+Watershed (p. 10).
* **Resolution Sensitivity:** Delineation accuracy is highly sensitive to spatial resolution. Dropping resolution from 15 cm to 30 cm decreased accuracy by 5–8%, while dropping to 60 cm caused a dramatic drop of 18–30% (p. 12).

## Implications for our pipeline

* **Alternative to Bounding Boxes:** Our current pipeline uses [[methods/deimv2-canopy]] (DETR-based) which relies on bounding boxes. For dense canopy delineation, integrating a star-convex polygon head or a StarDist-like post-processing step could resolve overlapping crown errors.
* **Sparse Label Training:** The $p > 0$ constraint is highly relevant to our weak-label and clustering workflow in [[project/pipeline-overview]]. It provides a mathematical mechanism to train deep learning models on incomplete ground-truth datasets without treating unannotated trees as background noise.
* **Resolution Requirements:** The paper confirms that high-resolution UAV orthophotos (typically $\le 15\text{ cm}$) are critical for accurate geometric delineation. If satellite imagery is integrated, standard 1 m or 50 cm resolutions will likely degrade delineation performance.

## Replication pseudocode

### Prerequisites

* PyTorch or TensorFlow (the paper uses TensorFlow 2.10.0)
* `stardist` Python package
* High-resolution RGB orthophoto and corresponding sparse polygon vector labels (converted to raster masks)

### Procedure

```text
1. Preprocess Input Data:
   - Tile the 15 cm RGB orthophoto into 256 x 256 pixel patches.
   - Generate corresponding instance masks where each annotated tree has a unique integer ID.
   - Compute normalized Euclidean distance transform for each instance to get reference probability maps.
   - Compute radial distances along 32 equidistant angles from each pixel to its instance boundary.

2. Define Modified Loss Function (Sparse Constraint):
   - For object probability loss (BCE):
     Only compute loss on pixels belonging to annotated tree crowns (where ground-truth p > 0).
     Exclude background pixels (p = 0) from the BCE calculation to handle sparse annotations.
   - For radial distance loss (MAE):
     Weight the Mean Absolute Error of the 32 radial directions by the ground-truth object probability.

3. Train U-Net Backbone:
   - Input: 256 x 256 x 3 RGB patches.
   - Output heads: 
     - Probability map: 256 x 256 x 1 (Sigmoid activation)
     - Radial distances: 256 x 256 x 32 (Linear activation)
   - Optimize using Adam (learning rate = 0.0003) for 100 epochs.

4. Inference & Post-Processing (NMS):
   - Predict probability map and radial distances.
   - Filter out pixels with probability < T_crown (threshold = 0.5).
   - Reconstruct star-convex polygons from the remaining radial distances.
   - Apply Polygon Non-Maximum Suppression (NMS):
     - Sort candidate polygons by predicted center probability.
     - Iteratively save the highest-probability polygon and remove overlapping candidates with IoU > T_IoU (threshold = 0.3).
```

### Gaps / not specified in paper

* **Registration of CHM:** The authors mention using a LiDAR-derived Canopy Height Model (CHM) to assist manual annotation but only use RGB bands for model training. They note that combining RGB and CHM would improve accuracy but leave the complex spatial registration of the two modalities as an unresolved challenge (p. 12).
* **Backbone Scaling:** The paper uses a standard, relatively shallow U-Net. It does not explore whether modern vision backbones (like ViT or DINOv3) would improve the feature extraction stage of StarDist.

## Quotes

* "In instance segmentation methods like MASK R-CNN, the Non-Maximum Suppression (NMS) process is adopted to suppress redundant detections. However, because NMS relies on axis-aligned bounding boxes that do not accurately reflect the true shapes of tree crowns, it can result in incorrect delineation, especially when tree crowns overlap." (p. 2)
* "To optimize the object probability map, a constraint $p > 0$ was added to the probability loss $L_{obj}$, which means the loss function is exclusively computed based on annotated tree crowns ($p > 0$), with background pixels ($p = 0$) excluded from consideration." (p. 6)
* "Compared with the delineation maps generated by MASK R-CNN, the proposed StarDist-based model generated more accurate delineations for overlapping and densely connected tree crowns, highlighting the advantages of star-convex polygons over axis-aligned bounding boxes." (p. 9)

## Related pages

* [[concepts/canopy-height-model]] — CHM generation and integration
* [[methods/deimv2-canopy]] — Our current DETR-based canopy detection method
* [[methods/merge-detections]] — Merging local maxima and geometric detections
