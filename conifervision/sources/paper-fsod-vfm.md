---
type: Source
title: "FSOD-VFM: Few-Shot Object Detection with Vision Foundation Models and Graph Diffusion"
description: "A training-free few-shot object detection framework integrating UPN, SAM2, and DINOv2/v3 with a graph diffusion-based confidence reweighting mechanism to eliminate proposal overfragmentation."
tags: [few-shot-detection, foundation-models, graph-diffusion, sam2, dinov2, dinov3, training-free]
status: stable
updated: 2026-03-03
source_file: raw/papers/FSOD-VFM.pdf
authors: [Chen-Bin Feng, Youyang Sha, Longfei Liu, Yongjun Yu, Chi Man Vong, Xuanlong Yu, Xi Shen]
year: 2026
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-03-03T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/FSOD-VFM.pdf
    title: "FSOD-VFM: Few-Shot Object Detection with Vision Foundation Models and Graph Diffusion"
related_methods:
  - methods/dinov3-classification
  - methods/deimv2-canopy
---

# FSOD-VFM: Few-Shot Object Detection with Vision Foundation Models and Graph Diffusion

## Summary

**FSOD-VFM** is a training-free, few-shot object detection framework presented at ICLR 2026. It leverages a combination of three vision foundation models (VFMs): a **Universal Proposal Network (UPN)** for category-agnostic bounding box generation, **Segment Anything Model 2 (SAM2)** for precise mask extraction, and **DINOv2/DINOv3** for feature extraction. 

To solve the critical issue of **proposal overfragmentation**—where class-agnostic proposal networks generate multiple small, false-positive bounding boxes covering only partial regions of an object—the authors introduce a **graph diffusion-based confidence reweighting mechanism**. Bounding boxes are modeled as nodes in a directed graph, and confidence scores are propagated using mask-level spatial overlaps. This suppresses fragmented local parts while preserving or boosting scores for complete, coherent objects.

## Key claims

- **Training-Free SOTA:** Achieves state-of-the-art performance on Pascal-5i, COCO-20i, and CD-FSOD benchmarks without requiring any fine-tuning or training steps.
- **Graph Diffusion for Overfragmentation:** Successfully mitigates proposal overfragmentation by modeling spatial overlaps as directed edges and running a PageRank-style diffusion process to penalize partial detections.
- **VFM Synergy:** Demonstrates that combining specialized foundation models (UPN for proposals, SAM2 for masks, and DINO for features) yields a highly robust, zero-shot/few-shot detector.
- **CD-FSOD Performance:** On the challenging Cross-Domain Few-Shot Object Detection (CD-FSOD) benchmark, FSOD-VFM achieves **31.6 AP** in the 10-shot setting, significantly outperforming the previous training-free baseline of 21.4 AP.

## Implications for our pipeline

- **Mitigating Tree Crown Fragmentation:** In our [[project/pipeline-overview]], tree detection models (such as [[methods/deimv2-canopy]]) or sliding-window local maxima can suffer from overfragmentation (e.g., detecting multiple branches or sub-crowns of a single large conifer). The **graph diffusion** algorithm could be adapted to reweight and merge overlapping tree crown proposals using mask-level overlaps from SAM2.
- **Training-Free Species Prototyping:** The method of extracting DINO features masked by SAM2 to build class prototypes (Equation 1) can be directly integrated into our [[methods/dinov3-classification]] stage to classify tree species using very few ground-truth reference crops.
- **DINOv3 Backbone Validation:** The paper provides ablation results for DINOv3 backbones (Table 6), confirming that DINOv3-B and DINOv3-L are highly competitive feature extractors for zero-shot matching tasks.

## Replication pseudocode

### Prerequisites

- Pre-trained Universal Proposal Network (UPN)
- Pre-trained SAM2 (e.g., SAM2-L)
- Pre-trained DINOv2 or DINOv3 backbone (e.g., DINOv2-L)
- Support set $S$ containing $K$ annotated bounding boxes per target species.

### Procedure

```text
# Stage 1: Build Class Prototypes
For each support annotation s_i in Support Set S:
    1. Generate binary foreground mask M_i using SAM2 with the annotated bounding box as a prompt.
    2. Extract dense feature map F_img using DINOv2/v3.
    3. Downsample and interpolate M_i to match the DINO feature map resolution -> M_down.
    4. Perform masked RoI pooling (Eq. 1):
       F_s = Sum(F_img[:, u, v] * M_down[u, v]) / Sum(M_down[u, v])
       
For each target class c in {1, ..., C}:
    1. Collect all pooled support features F_c belonging to class c.
    2. Compute the mean prototype: p_c = Mean(F_c)
    3. L2-normalize the prototype: p_c_hat = p_c / ||p_c||_2

# Stage 2: Query Proposal Matching
For a query image I_q:
    1. Generate up to 500 class-agnostic bounding box proposals using UPN.
    2. For each proposal j:
       a. Extract mask M_j using SAM2.
       b. Extract DINO feature vector F_q_j using masked RoI pooling.
       c. Compute cosine similarity with all class prototypes:
          similarity_c = cos(F_q_j, p_c_hat)
       d. Predict class: c_j_hat = argmax(similarity_c)
       e. Store proposal quadruple: (F_q_j, c_j_hat, score_upn_j, M_j)

# Stage 3: Graph Diffusion for Score Refinement
For each class c in {1, ..., C}:
    1. Filter proposals belonging to class c. Let N be the number of proposals.
    2. Construct an N x N directed adjacency matrix E:
       For each pair (i, j):
           If score_upn_i > score_upn_j:
               E[i, j] = 0
           Else:
               E[i, j] = Area(M_i INTERSECT M_j) / Area(M_i)
    3. Row-normalize E to obtain transition matrix P.
    4. Initialize prior weights w_i = max_j(E[i, j]) for each node i.
    5. Initialize diffusion vector pi_0 = [1/N, ..., 1/N]^T.
    6. Run PageRank-style diffusion for t = 1 to 30 steps (or until ||pi_t+1 - pi_t|| < 1e-6):
       pi_t+1 = alpha * (P * pi_t) + (1 - alpha) * w   # (where alpha = 0.3)
    7. Compute penalty-adjusted scores for each proposal j (Eq. 6):
       refined_score_j = (1 - pi_stationary_j)^lambda * max_c(cos(F_q_j, p_c_hat)) # (where lambda = 0.5)

Return top 100 proposals ranked by refined_score.
```

### Gaps / not specified in paper

- **UPN Architecture Details:** The exact configuration of the Universal Proposal Network (UPN) text prompts is simplified to "coarse" mode, but specific anchor settings or layer configurations are omitted.
- **Downsampling Interpolation:** The exact interpolation method (bilinear vs. nearest neighbor) used to downsample the SAM2 binary mask to match the DINO feature map resolution is not explicitly specified.

## Quotes

> "The bounding boxes generated by UPN often suffer from overfragmentation, covering only partial object regions and leading to numerous small, false-positive proposals rather than accurate, complete object detections." (Page 1)

> "Nodes with higher UPN scores are treated as high-quality proposals and thus retain their energy without diffusion. In contrast, nodes with lower UPN scores diffuse their energy toward more confident nodes." (Page 5)

> "Graph diffusion, in contrast, does not remove boxes based on thresholds. Instead, it refines proposal scores by propagating information between proposals using mask-level relationships from SAM2, which capture object boundaries much more accurately than bounding boxes." (Page 6)

## Related pages

- [[project/pipeline-overview]]
- [[methods/dinov3-classification]]
- [[methods/deimv2-canopy]]
- [[concepts/canopy-height-model]]
