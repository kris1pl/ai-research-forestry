---
title: DINOv3 — species classification
type: Method
description: "1. Object detection with DINOv3, crops, feature vectors."
tags: [dinov3, classification, weak-labels, orthophoto, species]
status: stable
updated: 2026-08-31
generated:
  by: agent:conifervision-wiki
  at: 2026-08-31T12:00:00Z
related_methods:
  - methods/merge-detections
sources:
  - sources/miao-zhang-2024-ptc-uav-species
  - sources/paper-deimv2
  - sources/paper-edgecrafter
  - sources/vo-2024-automatic-data-curation
  - sources/paper-fine-tuning_matters_and_parallel_decoder_helps
  - sources/paper-fsod-vfm
  - sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340
  - sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1
  - sources/paper-insid3_in_context_segmentation_dinov3
  - sources/paper-linguistic_guided_image_diffusion_model_for_tree_species_generation
---
# DINOv3 classification

1. Object detection with DINOv3, crops, feature vectors.
2. Clustering + specialist labels → **weak labels** in Delta Lake.
3. Train classifier on ground truth + weak labels.
4. Classify detected trees.

## In the pipeline

Stage 3 in [[project/pipeline-overview]] — runs on per-tree crops after detection/merge.

## Literature

[[sources/miao-zhang-2024-ptc-uav-species]] — urban UAV study; **not DINOv3** but directly relevant to **per-tree orthophoto patches** and species separability. Shows that **input reformation (PTC)** before a CNN can outperform nadir green-band patches by >10%; best reported setup PyTorch + ResNet50 (~98% on 5 species, 696 patches). Our backbone differs; the lesson is patch geometry/view, not a specific framework.

[[sources/vo-2024-automatic-data-curation]] — Meta FAIR (DINOv2 authors). **Hierarchical k-means + resampling** to build balanced SSL pre-training sets from long-tailed pools; explains why **vanilla k-means fails** to balance dominant vs rare visual concepts. Directly relevant to our **clustering → weak labels** step (same embedding-space pathology, different goal). Satellite experiment: curated 9M / 18M patch pool improved **canopy height R² ~20%** vs raw pre-training — indirect support for balanced aerial/satellite representation learning before tree-level tasks.

## Replication notes

| Paper step | Our implementation |
|------------|---------------------|
| Manual / GIS tree patches | Automated crops from detections + orthophoto |
| PTC 3D reprojection of crown | **Not used** — candidate experiment ([[concepts/pseudo-tree-crown]]) |
| ResNet50 64×64, 50 epochs | DINOv3 pipeline (architecture TBD in code repo) |
| Field-validated species labels | Ground truth + weak labels (Delta Lake) |
| Hierarchical k-means curation (Vo 2024) | **Not used** — we use plain clustering for weak labels; candidate improvement |
| DINOv3 feature extraction | aligned |
| Teacher Preparation (Stage 1) | TBD |
| Knowledge Distillation (Stage 2) | TBD |
| Downstream Task Adaptation (Stage 3) | TBD |
| Progressive Fine-Tuning (Stage 1: frozen backbone; Stage 2: unfrozen) | TBD |
| Plateau-aware learning rate scheduler trigger | TBD |
| Build Class Prototypes (Masked RoI Pooling) | aligned |
| Query Proposal Matching (Cosine Similarity) | aligned |
| Text Embedding Generation | not used |
| Forward Diffusion (Noise Injection) | not used |
| Reverse Diffusion (Denoising with LGINet) | not used |
| Downstream Training | aligned (candidate for rare species augmentation) |
| Calculate spectral indices (NGRDI, VARI) | TBD |
| Calculate structural metrics (pointedness, CRR, CV_Z, vertical_variability, ZQ99, ZQ999) | TBD |
| Calculate concave hull metrics via alphashape3d | TBD |
| Fit 2D projection triangle (top_angle, widest_distance, relative_height_widest) | TBD |
| Train Random Forest classifiers with 10-fold cross-validation | TBD |
| Apply manual taxonomic overrides based on regional constraints | TBD |
| DeepForest bounding box prediction | aligned |
| SAM2 mask generation from box prompts | TBD |
| Post-processing to remove disconnected regions | TBD |
| Polygon-based Non-Maximum Suppression (IoU = 0.05) | TBD |
| Estimate positional subspace via SVD on noise image | TBD |
| Project features onto orthogonal complement of positional subspace | TBD |
| Fine-grained agglomerative clustering on target features | TBD |
| Seed-cluster selection via debiased cross-image similarity | TBD |
| Cluster aggregation using original and debiased prototypes | TBD |


Pseudocode: [[sources/paper-insid3_in_context_segmentation_dinov3#Replication pseudocode]].

Pseudocode: [[sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1#Replication pseudocode]].

Pseudocode: [[sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340#Replication pseudocode]].

Pseudocode: [[sources/paper-linguistic_guided_image_diffusion_model_for_tree_species_generation#Replication pseudocode]].

Pseudocode: [[sources/paper-fsod-vfm#Replication pseudocode]].

Pseudocode: [[sources/paper-fine-tuning_matters_and_parallel_decoder_helps#Replication pseudocode]].

Pseudocode: [[sources/paper-edgecrafter#Replication pseudocode]].

Pseudocode: [[sources/paper-deimv2#Replication pseudocode]].
Full PTC pseudocode: [[sources/miao-zhang-2024-ptc-uav-species#Replication pseudocode]]. **Replication focus for us:** only the *idea* of non-nadir patch views until we run an internal A/B.

## Production parameters

_(model version, crop size, augmentations — link when code repo integrated)_

## Related concepts

- [[concepts/pseudo-tree-crown]] — optional input transform from literature
- Weak labels: Delta Lake / clustering — see [[sources/vo-2024-automatic-data-curation#Implications for our pipeline]] for balancing theory

## Open questions from literature

- Would PTC-style views help conifer species confused on nadir orthophoto crops?
- Paper patches are pre-segmented urban crowns; do overlapping crowns in production negate PTC gains?
- Can we adapt hierarchical k-means with resampling to balance highly skewed species distributions in our weak-label generation pipeline?
- Can we adapt the hierarchical k-means + resampling pipeline to balance our weak-label species pools in Delta Lake?
- Can we use hierarchical k-means with resampling to resolve the dominant-species cluster splitting issue in our weak-label generation pipeline?
- Can we share a single DINOv3 backbone instance between the DEIMv2 detector and the downstream species classifier to minimize redundant forward passes?
- How does the performance of a compact student distilled from a task-specialized DINOv3 teacher compare to direct fine-tuning of a generic DINOv3 student on our species classification task?
- Can the progressive fine-tuning framework stabilize DINOv3 species classification when adapting to highly distinct geographic forest domains with limited labeled samples?
- Can we adapt the masked RoI pooling mechanism using SAM2 masks and DINOv3 features to build robust, training-free species prototypes for rare conifer species?
- Can low-resolution ($32 \times 32$) synthetic canopy patches generated by LGINet be effectively upscaled or integrated into high-resolution DINOv3 feature extraction pipelines without losing critical morphological details?
- How does the inclusion of BorFIT's 11 structural metrics and 2 spectral indices as auxiliary features alongside DINOv3 embeddings affect classification accuracy for overlapping boreal conifer species?
- Can prompting SAM2 with DEIMv2 canopy bounding boxes reliably isolate individual tree crowns in dense conifer stands to eliminate background noise before DINOv3 feature extraction?
- Can the SVD-based debiasing projection from INSID3 be applied to DINOv3 feature extraction in our species classification pipeline to improve cross-orthophoto matching and reduce spatial coordinate bias?