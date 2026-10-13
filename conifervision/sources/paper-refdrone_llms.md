---
type: Source
title: "RefDrone: A Challenging Benchmark for Referring Expression Comprehension in Drone Scenes"
description: "Introduces the RefDrone benchmark, the RDAnnotator semi-automated labeling pipeline, and Number GroundingDINO (NGDINO) to handle multi-target and no-target scenarios in aerial imagery."
tags: [drone-imagery, object-detection, referring-expression-comprehension, multi-target, annotation-pipeline]
status: stable
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-03-29T12:00:00Z
source_file: raw/papers/RefDrone_llms.pdf
authors: [Zhichao Sun, Yepeng Liu, Zhiling Su, Huachao Zhu, Yuliang Gu, Yuda Zou, Zelong Liu, Gui-Song Xia, Bo Du, Yongchao Xu]
year: 2025
replication_status: partial
related_methods:
  - methods/chm-detection
  - methods/merge-detections
sources:
  - id: primary
    resource: raw/papers/RefDrone_llms.pdf
    title: "RefDrone: A Challenging Benchmark for Referring Expression Comprehension in Drone Scenes"
---

# RefDrone: A Challenging Benchmark for Referring Expression Comprehension in Drone Scenes

## Summary

The paper addresses Referring Expression Comprehension (REC) in drone-captured imagery, which presents unique challenges such as multi-target/no-target scenarios, small-scale objects, and complex environmental contexts. The authors introduce **RefDrone**, a benchmark dataset containing 17,900 referring expressions across 8,536 images with 63,679 object instances. To construct this dataset efficiently, they develop **RDAnnotator**, a semi-automated annotation framework combining Large Vision-Language Models (LVLMs) and human-in-the-loop verification. 

Furthermore, they propose **Number GroundingDINO (NGDINO)**, which extends GroundingDINO by explicitly modeling target object counts. NGDINO incorporates a number prediction head, learnable number-queries, and a number cross-attention module to improve performance on multi-target and no-target cases.

## Key claims

* **RefDrone Dataset Complexity:** RefDrone contains a high proportion of multi-target (11,362) and no-target (847) expressions, with target counts ranging from 0 to 242 (Page 4). Small objects (< 1024 pixels) make up 31.1% of the dataset (Page 2, Table 1).
* **RDAnnotator Efficiency:** RDAnnotator reduces human annotation time by 85% (from 7 minutes to under 1 minute per expression) and achieves a low API cost of $0.0539 per expression using GPT-4o (Page 4).
* **NGDINO Superiority:** NGDINO-B achieves state-of-the-art fine-tuning performance on RefDrone with 72.51% $F1_{inst.}$ and 57.22% $Acc_{inst.}$, outperforming the baseline GDINO-B by 2.76% and 3.27% respectively (Page 6, Table 3).
* **Explicit Number Modeling:** Incorporating an auxiliary number prediction task and fusing number-queries with detection queries significantly improves grounding performance in multi-target and no-target scenarios (Page 5).

## Implications for our pipeline

* **Multi-Target and No-Target Handling:** Our [[project/research-tree-detection-ensemble]] deals with dense stands where a single query or local region can contain dozens of trees (multi-target) or zero trees (no-target). The explicit numerical reasoning concepts from NGDINO could be adapted to our detection heads to reduce false positives in empty canopy gaps.
* **Small-Object Detection:** The paper highlights that standard LVLMs struggle with small objects in drone imagery (Page 6). This reinforces our reliance on high-resolution local tiling (e.g., SAHI in our [[project/pipeline-overview]]) and specialized backbones rather than zero-shot general-purpose vision-language models.
* **Semi-Automated Labeling (RDAnnotator):** The multi-step feedback loop (scene understanding $\rightarrow$ color categorization $\rightarrow$ expression generation $\rightarrow$ quality evaluation $\rightarrow$ human verification) can serve as a template for generating weak labels or synthetic training data for our [[concepts/pseudo-tree-crown]] and species classification pipelines.

## Replication pseudocode

### Prerequisites

* PyTorch and MMDetection framework.
* Pre-trained GroundingDINO (GDINO) weights.
* Discretized target count bins: $C = \{0, 1, 2, 3, 4+\}$.

### Procedure

```text
1. Initialize NGDINO with pre-trained GDINO weights.
2. Append a lightweight Number Prediction Head (FFN + MeanPool + Softmax) to the decoder.
3. Define learnable number-queries Q_num of shape [Batch, Ln, Dimension] where Ln = 50 (5 bins * 10 queries).
4. Stage 1 (Pre-training):
   a. Freeze all backbone and detection components.
   b. Train only the Number Prediction Head for 5 epochs on the target dataset.
   c. Loss function: Cross-Entropy loss on the discretized target bins.
5. Stage 2 (End-to-end Fine-tuning):
   a. Unfreeze the entire model.
   b. For each forward pass:
      i. Predict target count distribution N_prob from detection queries Q_det.
      ii. Select the corresponding slice of number-queries Q_sel based on N_pred = argmax(N_prob).
      iii. Pass Q_det (as Query) and Q_sel (as Key/Value) through the Number Cross-Attention module.
      iv. Add the cross-attention output to the self-attention output of the decoder.
   c. Train end-to-end for 50 epochs using combined loss:
      Loss = Loss_GDINO_box + Loss_GDINO_class + Loss_Number_CE
   d. Disable random crop data augmentation to preserve spatial context.
```

### Gaps / not specified in paper

* **Learning Rate Schedule:** The exact learning rate and optimizer parameters for the two-stage training process are not fully detailed.
* **Discretization Thresholds:** While the bins are defined as $\{0, 1, 2, 3, 4+\}$, the exact regression-to-classification mapping during training for counts higher than 4 is not explicitly formulated beyond the bin assignment.

## Quotes

> "RDAnnotator reduces human annotation effort by 85%, decreasing the average time per expression from 7 minutes to 1 minute." (Page 4)

> "Our key insight is that explicitly modeling the number of referred objects significantly enhances handling of these scenarios." (Page 2)

> "We disable random crop data augmentation. This is because random cropping can remove crucial spatial context or the target objects themselves in our position-sensitive referring expressions..." (Page 12)

## Related pages

* [[project/pipeline-overview]] — Current production pipeline utilizing SAHI and local detection.
* [[project/research-tree-detection-ensemble]] — Research north star for dense stand tree detection.
* [[concepts/canopy-height-model]] — Context on drone-based photogrammetry and height layers.
