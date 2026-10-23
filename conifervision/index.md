---
okf_version: "0.2"
---
# Conifervision Research Wiki

Compiled team knowledge for **individual tree detection and segmentation** from drone imagery (orthophoto + CHM/3D). Also covers the current AREA production pipeline and species classification. Current proposal (2026-10-21, ADR-003 **proposed**): normal-forest crowns in [[project/research-normal-forest]]. Dense stands before thinning remain in the vault as history ([[project/research-tree-detection-ensemble]]). Maintained by an LLM agent per `AGENTS.md` at the repository root.

## Current focus

1. **Proposed program:** [[project/research-normal-forest]] — one crown box per tree in normal forest, then outlines. Condensed path for discussion: [[project/normal-forest-flow]] (draft). ADR-003 is **proposed**. Next smoke: [[experiments/normal-forest/exp-005-normal-forest-ownership-smoke]] (draft; no training). The previous north star [[project/research-tree-detection-ensemble]] stays as history.
2. **Hypothesis loop:** [[project/hypothesis-validation-loop]] — propose → Experiment page → human gate → GPU module → validate/reject.
3. **Experiments by domain:** [[project/domains]]. Active queue: [[experiments/normal-forest/index]] (exp-005 smoke). R-class history: [[experiments/r-class-itd/index]]. H1 / H2 / H3 ids are unchanged ([[project/decisions]]).
4. **Literature map (dense ITD):** [[concepts/literature-map-dense-itd]] — background reading for the previous dense-stand program.

Production baseline (what ships today): [[project/pipeline-overview]]. Success structure for the previous ensemble: ADR-001 in [[project/decisions]] (proposed until eval numbers are locked). ADR-003 is a separate proposal and is not accepted.

## Project

- [[project/domains]] — catalog of programs and the recipe for the next one
- [[project/research-normal-forest]] — **proposed current program** (ADR-003 proposed; one crown per tree, then outlines)
- [[project/normal-forest-flow]] — condensed discussion sheet for that path; draft; does not number experiments after exp-005
- [[project/research-tree-detection-ensemble]] — previous north star; not the current priority as of 2026-10-21
- [[project/hypothesis-validation-loop]] — scientist ↔ engineer handoff for experiments
- [[project/pipeline-overview]] — current production AREA pipeline
- [[project/decisions]] — methodological ADRs (incl. ADR-001 ensemble v1)
- [[project/code-repo-integration]] — **TODO:** link to production code repository

## Pipeline methods

- [[methods/index]] — methods index (OKF progressive disclosure)

## Concepts

- [[concepts/literature-map-dense-itd]] — synthesis: priorities among ingested ITD/segmentation papers
- [[concepts/dense-stand-detection]] — evaluation concept for dense plots (before clearing)
- [[concepts/understory-tree-detection]] — a stem under another crown; the canopy surface shows only the top tree
- [[concepts/normal-forest]] — merchantable crowns larger than R-class, with separable tops
- [[concepts/crown-ownership]] — 800 box owns a crown only after one peak, a height floor, and a fixed sample
- [[concepts/canopy-height-model]] — CHM (DSM − DTM); LiDAR and satellite SSL links
- [[concepts/site-index-and-yield]] — dominant height, site index, and stand volume; not a started allometry program
- [[concepts/point-cloud-individual-tree-segmentation]] — Existing concept canopy-height-model and literature-map-dense-itd focus on raster CHMs or dense 2D imagery, leaving direct 3D point cloud clustering and bottom-up tree instance segmentation unrepresented.
- [[concepts/tree-allometry]] — Existing concept site-index-and-yield explicitly restricts coverage to stand-level site index, dominant height, basal area, and yield capacity, leaving individual tree DBH, crown width, crown base height, and stem volume relationships unrepresented.
- [[concepts/pseudo-tree-crown]] — PTC input reformation for species CNNs (UAV)
- [[concepts/pseudo-label-audit-cvat]] — fixed human precision sample; AREA 540 procedure stays; verdicts reused by crown ownership

## Experiments

- [[project/domains]] — which program is active, and how to add the next one
- [[experiments/index]] — program catalog
- [[experiments/normal-forest/index]] — **current** — exp-005 ownership smoke (draft; no training)
- [[experiments/r-class-itd/index]] — history; H1 exp-001, H3 exp-002, H2 exp-003, exp-004 closed without training

## Literature sources

- [[sources/paper-crown_and_root_biomass_equations_fo]] — demonstrates crown width utility over height and competition suppression for understory Pinus koraiensis allometry
- [[sources/paper-blanchard_tsaf_2016]] — Multi-site tropical empirical study showing DBH-crown area scaling exponents remain invariant (~1.24) across sites, but height scaling and crown expansion vary with canopy emergence.
- [[sources/paper-biomass and stem volume_951-40-1984-9]] — synthesis of 607 biomass and 230 stem volume equations across 55 European tree species with transformation corrections
- [[sources/paper-beech allometry_bgc4810s1]] — Empirical double-logistic crown area and modified Mund height-to-DBH allometric equations for European beech, hornbeam, lime, and maple.
- [[sources/paper-allometric relationships of selected european tree-gp_eudor_pdfa1b_euna20855enc_001]] — synthesizes empirical allometric equations (DBH, height, crown radius, biomass) and crown geometric primitives for spruce, pine, birch, beech, and larch to constrain crown delineation and volume inversion
- [[sources/paper-alder_allometry_cpi023]] — Stem volume equations, wood basic density, and crown base height taper relationships for Alnus incana and Alnus glutinosa in Sweden.
- [[sources/paper-a_linkage_among_tree_diameter_height_crown_base_he]] — Vasicek-type 4-variate SDE joint distribution showing that conditioning on both CHM height and crown width predicts DBH ($R^2 \approx 0.89$) and stem volume without below-canopy metrics
- [[sources/paper-a rapid method for estimating the median diameter of the stem profile of norway spruce trees-iforest_ifor1945-009_vasilescu]] — empirical stem profile models locating median diameter at 0.3H for Norway spruce stem volume and taper estimation
- [[sources/paper-a crown width-diameter model for natural even-aged black pine forest management-forests-09-00610-v2]] — nonlinear mixed-effects models relating horizontal crown width to DBH and stand density covariates with plot-level calibration
- [[sources/paper-site index models for main forest-forming tree species in poland_forests-11-00301]] — GADA-based dynamic height growth and site index equations for eight Central European tree species fitted on 3,052 stem analyses, superseding historical yield tables
- [[sources/paper-mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_estonian_forests]] — demonstrates dominant height insensitivity to low thinning and provides dominant-to-mean height regression for Estonian forests
- [[sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations]] — bottom-up stem clustering with HDBSCAN, chi-square radial distribution DBH modeling, and pseudo-waveform tree height filtering from ultra-dense low-cost UAV-LiDAR
- [[sources/paper-evaluation of growth functions used in the swedish forest planning system heureka_article1013]] — Stand vs single-tree empirical basal area and volume growth evaluation in Sweden (Heureka system)
- [[sources/paper-appiahmensah_et_al_2023_site_index_sis_rs]] — Bi-temporal ALS height percentiles, annual top-height increment, and terrain auxiliaries predicting coniferous site index across Sweden via multiple linear regression
- [[sources/paper-appiahmensah_et _al-2022_yield capacity]] — Yield capacity and stand volume models connecting CHM top height, basal area, and species to timber yield across Swedish conifer trials
- [[sources/paper-refdrone_llms]] — introduces RefDrone benchmark and Number GroundingDINO (NGDINO) for multi-target and no-target aerial referring expression comprehension
- [[sources/paper-multi_llm_detections]] — Iwanowski (2025) — Survey of multi-LLM/VLM consensus frameworks for object detection, categorizing prompt-level, reasoning, box-level, and hybrid consensus.
- [[sources/paper-insid3_in_context_segmentation_dinov3]] — INSID3 — training-free in-context segmentation using SVD-debiased DINOv3 features
- [[sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1]] — Chen (2025) — Evaluates SAM2 zero-shot tree crown segmentation prompted by DeepForest bounding boxes.
- [[sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021]] — Rodríguez-Puerta (2022) — Evaluates ITD and height extraction on young pine plantations, finding 10 cm CHM optimal and point cloud height extraction unbiased.
- [[sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025]] — TreePseCo — adapts PseCo framework using SAM and Faster R-CNN for robust individual tree crown segmentation in aerial imagery
- [[sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114]] — Holmgren et al. (2022) — Introduces 3D tree crown density models and mean-shift clustering to detect understory trees in multi-layered forest canopies.
- [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025]] — Pucino (2025) — Evaluates combinations of 3 CHM and 4 ITS algorithms across 15 Australian vegetation classes, finding Pit-Free CHM and DalPonte segmentation yield the highest accuracy.
- [[sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds]] — Shaheen (2025) — Self-supervised 3D LiDAR point cloud segmentation using transformation-invariant pretext tasks and energy-based soft clustering.
- [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests]] — Young et al. (2022) — Comprehensive evaluation of 7,568 combinations of drone flight parameters, photogrammetry settings, and ITD algorithms in a complex mixed-conifer stand.
- [[sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660]] — Lu (2025) — Introduces DEN4, an unsupervised deep learning-based point cloud denoising algorithm that improves individual tree segmentation accuracy.
- [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data]] — Li (2025) — introduces RDT, a hybrid tree segmentation framework combining CHM region-growing with point cloud density-guided vertical profile morphology analysis
- [[sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main]] — Tong (2025) — Adapts StarDist with a sparse-annotation loss function for individual tree crown delineation in dense RGB imagery.
- [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1]] — ForestFormer3D — End-to-end transformer-based 3D instance and semantic segmentation framework for forest LiDAR point clouds using ISA-guided query selection and score-based block merging.
- [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]] — Sparks (2022) — Comparative study of seven ITD methods across mixed-conifer stands using 8 and 22 ppm² ALS data, showing that stand density and parameter tuning drive accuracy more than method choice.
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
