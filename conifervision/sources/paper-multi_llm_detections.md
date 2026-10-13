---
title: "Multiple Large AI Models' Consensus for Object Detection—A Survey"
type: Source
tags: [ensemble, object-detection, consensus-learning, late-fusion, vlm, llm]
status: stable
updated: 2026-03-10
description: "A comprehensive survey of multi-LLM/VLM consensus frameworks for object detection, categorizing methods into prompt-level, reasoning-to-detection, box-level, and hybrid consensus."
source_file: raw/papers/multi_llm_detections.pdf
authors: [Marcin Iwanowski, Marcin Gahbler]
year: 2025
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-03-10T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/multi_llm_detections.pdf
    title: "Multiple Large AI Models' Consensus for Object Detection—A Survey"
---

# Multiple Large AI Models' Consensus for Object Detection—A Survey

## Summary

This paper provides a systematic survey of the emerging paradigm of "multiple large AI models' consensus" for object detection. It bridges the gap between text-domain LLM ensembling (e.g., Mixture-of-Agents, Multi-Agent Debate) and spatial computer vision ensembling (e.g., Non-Maximum Suppression, Weighted Boxes Fusion, Probabilistic Ensembling). The authors formalize a four-level taxonomy of consensus designs (prompt-level, reasoning-to-detection, box-level, and hybrid) and analyze how combining heterogeneous predictions from LLMs, VLMs, and MLLMs improves spatial accuracy, semantic correctness, and calibration while mitigating hallucinations.

## Key claims

1. **Four-Level Consensus Taxonomy**:
   - **Prompt-level**: Models agree on semantic classes or queries textually before any detection is executed (e.g., using Self-Consistency, Mixture-of-Agents, or Multi-Agent Debate).
   - **Reasoning-to-detection**: Heterogeneous VLMs/MLLMs generate structured reasoning traces or category lists from both text and image inputs, which are then executed by open-vocabulary detectors.
   - **Box-level**: Spatial bounding boxes, classes, and confidence scores from independent models are merged geometrically or probabilistically.
   - **Hybrid**: Multi-stage pipelines combining semantic alignment, reasoning-to-detection, and spatial box-level fusion.
2. **Quantifiable Performance Gains**:
   - For box-level late fusion, ensembling via **Weighted Boxes Fusion (WBF)** consistently outperforms single-model baselines (e.g., ensembling two EfficientDet models on MS COCO increased mAP from 0.521 to 0.5344) (p. 19).
   - **Probabilistic Ensembling (ProbEn)** significantly reduces the Log-Average Miss Rate (LAMR) on multimodal datasets (e.g., reducing LAMR on the KAIST pedestrian dataset from 6.48% to 5.14%, a relative improvement of over 13%) (p. 19).
   - In LLM/VLM reasoning, the **Iterative Consensus Ensemble (ICE)** framework using three models improved overall accuracy on complex multiple-choice datasets from 60.2% to 74.03% (p. 19).
3. **Diminishing Returns of Scaling**: Performance gains from scaling the number of agents typically saturate beyond 3 to 5 heterogeneous models, after which computational cost and latency dominate the benefits (p. 14, 20).
4. **Heuristic vs. Probabilistic Fusion**: Traditional spatial fusion methods like NMS, Soft-NMS, and WBF are heuristic and do not preserve probability semantics. In contrast, ProbEn operates in logit space (summing logits) and models coordinates as Gaussian distributions to preserve Bayesian probability semantics, though it requires well-calibrated confidence scores (p. 16).

## Implications for our pipeline

- **Ensemble Strategy for Dense Stands**: Our research north star [[project/research-tree-detection-ensemble]] can directly leverage this taxonomy. Instead of simple rule-based fusion, we should evaluate a **hybrid consensus** approach:
  1. **Prompt/Reasoning Level**: Align semantic definitions of tree classes (e.g., species, health status) across different backbones.
  2. **Box-Level Fusion**: Transition from simple NMS in `nms_ai_lm.py` to **Weighted Boxes Fusion (WBF)** or **Probabilistic Ensembling (ProbEn)** to merge predictions from the local maxima, CHM/DEIMv2, and RGB detection layers.
- **Uncertainty Calibration**: Since our pipeline merges highly heterogeneous layers (geometric local maxima vs. deep learning DEIMv2/DINOv3), implementing proper score calibration (e.g., temperature scaling or isotonic regression) is a prerequisite before applying probabilistic fusion like ProbEn.
- **Efficiency Constraints**: To keep our orchestration pipeline (`orchestrate_chm_reclass_full_flow_r.py`) computationally viable, we should limit our active ensemble layers to 3–5 highly diverse experts (e.g., one CHM geometric expert, one RGB instance segmentation expert, and one open-vocabulary grounding expert) to avoid the diminishing returns of scaling.

## Replication pseudocode

### Prerequisites

- Python 3.10+
- `ensemble-boxes` library (for WBF) or a custom implementation of ProbEn.
- Calibrated confidence scores from upstream detectors (DEIMv2, Local Maxima, RGB detector).

### Procedure

```text
1. Extract bounding boxes, class labels, and confidence scores from:
   - Layer A: CHM Local Maxima (converted to bounding boxes)
   - Layer B: DEIMv2 Canopy Detector
   - Layer C: RGB Instance Segmentation (bounding box projections)
2. Normalize all coordinates to the shared orthophoto pixel coordinate system.
3. Harmonize labels (e.g., map all variations of "conifer" or "pine" to canonical class IDs).
4. Apply score calibration (e.g., Isotonic Regression) to normalize confidence scales across layers.
5. Execute Weighted Boxes Fusion (WBF) or Probabilistic Ensembling (ProbEn) to merge overlapping detections.
```

```python
# Conceptual implementation of Box-Level Fusion using WBF
import numpy as np
from ensemble_boxes import weighted_boxes_fusion

def fuse_tree_detections(predictions_by_layer, iou_thr=0.5, skip_box_thr=0.05):
    """
    predictions_by_layer: List of dicts containing 'boxes', 'scores', and 'labels' for each layer.
    Each box is normalized [x1, y1, x2, y2] in range [0, 1].
    """
    boxes_list = [pred['boxes'] for pred in predictions_by_layer]
    scores_list = [pred['scores'] for pred in predictions_by_layer]
    labels_list = [pred['labels'] for pred in predictions_by_layer]
    
    # Assign weights to layers (e.g., RGB detector has higher weight than Local Maxima)
    weights = [1.0, 1.5, 0.8] 
    
    fused_boxes, fused_scores, fused_labels = weighted_boxes_fusion(
        boxes_list, 
        scores_list, 
        labels_list, 
        weights=weights, 
        iou_thr=iou_thr, 
        skip_box_thr=skip_box_thr
    )
    
    return fused_boxes, fused_scores, fused_labels
```

### Gaps / not specified in paper

- **Open-Vocabulary Metrics for Forestry**: The paper notes a lack of systematic empirical studies quantifying the benefits of multi-agent LLM/VLM consensus using traditional object detection metrics (like mAP) on specialized open-vocabulary datasets (p. 19).
- **Non-Maximum Suppression Thresholds**: Specific optimal IoU thresholds ($IoU_{thr}$) for WBF and ProbEn are highly dataset-dependent and are left as TBD for custom domains.
- **Computational Overhead of ProbEn**: While the paper outlines the mathematical formulation of ProbEn, it does not provide concrete execution times or GPU memory footprints when scaling to thousands of dense objects (such as trees in a dense forest orthophoto).

## Quotes

> "Instead of relying on a single large AI model, LLM, VLM or MLLM, several models process the same image and prompt in parallel, each producing an independent prediction in a standardized format... These structured outputs are then merged using consensus algorithms..." (p. 2)

> "For geometry fusion, ProbEn models bounding box coordinates as a Gaussian distribution. It determines the final coordinate by calculating a weighted average based on the inverse of the variance (uncertainty) of each prediction." (p. 16)

> "They find that improvements follow a diminishing, return pattern—typically saturating beyond 3–5 diverse agents, consistent with classical ensemble theory." (p. 14)

## Related pages

- [[project/research-tree-detection-ensemble]] — Our multi-layer ensemble research target.
- [[project/pipeline-overview]] — The current production AREA pipeline.
- [[methods/merge-detections]] — Details on our current rule-based fusion (`nms_ai_lm.py`).
- [[concepts/dense-stand-detection]] — Context on dense forest stands before thinning.
