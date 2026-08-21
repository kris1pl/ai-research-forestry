---
okf_version: "0.2"
updated: 2026-08-21
generated:
  by: agent:conifervision-wiki
  at: 2026-08-21T12:00:00Z
---
# Conifervision Research Wiki

Compiled team knowledge on tree detection and classification methodology (drones, CHM, AI models, weak labels). Maintained by an LLM agent per `AGENTS.md` at the repository root.

## Project

- [[project/pipeline-overview]] — current production pipeline
- [[project/decisions]] — methodological decisions (ADR)
- [[project/code-repo-integration]] — **TODO:** link to production code repository

## Pipeline methods

- [[methods/index]] — methods index (OKF progressive disclosure)

## Concepts

- [[concepts/canopy-height-model]] — CHM (DSM − DTM); satellite SSL curation link (Vo 2024)
- [[concepts/pseudo-tree-crown]] — PTC input reformation for species CNNs (UAV)

## Experiments

- (pages under `experiments/` — hypothesis, metrics, conclusions)

## Literature sources

- [[sources/paper-comparison_of_individual_tree-twec21_public]] — Weckman (2021) — Comparative study of local maxima, trunk detection, and point density methods for individual tree detection using high-density UAV laser scanning.
- [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020]] — Mu (2020) — Canopy Maximum Model (CMM) and seeded K-means watershed segmentation to mitigate over-segmentation.
- [[sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340]] — BorFIT — A manually segmented and species-classified boreal forest LiDAR dataset with structural and spectral metrics
- [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]] — Ding (2025) — bottom-up oriented search and clustering method for extracting individual trees from ALS point clouds
- [[sources/paper-linguistic_guided_image_diffusion_model_for_tree_species_generation]] — Yun (2026) — LGINet text-guided diffusion model for synthetic tree canopy generation and enhanced YOLOv11 species identification
- [[sources/paper-treeflow]] — TreeFlow — Conditional Flow Matching for 3D tree point cloud generation from inventory attributes
- [[sources/paper-fsod-vfm]] — FSOD-VFM — A training-free few-shot object detection framework using UPN, SAM2, and DINOv2/v3 with graph diffusion to mitigate proposal overfragmentation.
- [[sources/paper-fine-tuning_matters_and_parallel_decoder_helps]] — Yu et al. (2026) — Introduces Hybrid Ensemble Decoder (HED) and progressive fine-tuning to stabilize few-shot object detection and reduce OOD overconfidence.
- [[sources/paper-edgecrafter]] — EdgeCrafter — compact ViT framework utilizing task-specialized DINOv3 distillation for edge dense prediction
- [[sources/paper-deimv2]] — DEIMv2 — Real-time DETR-based detector integrating DINOv3 backbones via Spatial Tuning Adapters
- [[sources/popescu-wynne-2004-seeing-the-trees]] — LiDAR CHM, variable-window local maxima, multispectral fusion (2004)
- [[sources/miao-zhang-2024-ptc-uav-species]] — pseudo tree crown (PTC), UAV species classification, ResNet50/PyTorch (2024)
- [[sources/vo-2024-automatic-data-curation]] — hierarchical k-means SSL data curation, satellite canopy height (Meta FAIR, 2024)

## Navigation

- [[log]] — wiki change timeline
- Full index: see sections above; the agent updates lists on this page after each ingest.
