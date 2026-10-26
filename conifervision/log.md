# Wiki log

Chronological record of ingest, query, hypothesis, and lint operations.

## [2026-10-26] lint | Publish accepted concepts still marked draft

- Set `status: stable` on [[concepts/area-based-approach]], [[concepts/foundation-model-tree-delineation]], [[concepts/direct-stem-dbh-point-cloud]], [[concepts/height-diameter-inversion]], [[concepts/stem-taper-curve]]
- `make concept-gate APPLY=1` now writes new concept pages as `stable`. [[project/concept-proposals]] stays a draft review sheet.

## [2026-10-26] query | Concept accepted: Stem Taper Curve

- Added [[concepts/stem-taper-curve]] from [[project/concept-proposals]]

## [2026-10-26] query | Concept accepted: Area-Based Approach

- Added [[concepts/area-based-approach]] from [[project/concept-proposals]]

## [2026-10-26] ingest | Hartley et al. (2025) — ULS vs UAV-SfM height and crown-derived DBH modeling

- Source: `raw/papers/UAV-enabled evaluation of forestry plantations_A comprehensive assessment of laser scanning and photogrammetric approa-1-s2.0-S2666017225000513-main.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-uav-enabled evaluation of forestry plantations_a comprehensive assessment of laser scanning and photogrammetric approa-1-s2-0-s2666017225000513-main]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/height-diameter-inversion]], [[sources/index]]

## [2026-10-26] ingest | Urban et al. (2012) — Allometric scaling and site fertility effects for Douglas fir and Norway spruce

- Source: `raw/papers/Tree allometry of Douglas fir and Norway spruce on a nutrient-poor and a nutrient-rich site_urban_dg_2012.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-tree allometry of douglas fir and norway spruce on a nutrient-poor and a nutrient-rich site_urban_dg_2012]]
- Updated [[index]], [[concepts/height-diameter-inversion]], [[concepts/tree-allometry]], [[concepts/crown-ownership]], [[sources/index]]

## [2026-10-26] ingest | Petrauskas & Rupšys (2013) — Generalized H-D equations for Scots pine in Lithuania

- Source: `raw/papers/The Generalised Height-Diameter Equations of Scots Pine Trees in Lithuania-E_PetrauskasP_Rupsys.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-the generalised height-diameter equations of scots pine trees in lithuania-e_petrauskasp_rupsys]]
- Updated [[index]], [[concepts/height-diameter-inversion]], [[concepts/tree-allometry]], [[sources/index]]

## [2026-10-26] ingest | Laasasenaho (1982) — Finnish taper curve and stem volume functions

- Source: `raw/papers/TAPER CURVE AND VOLUME FUNCTIONS FOR PINE, SPRUCE AND BIRCH-951-40-0589-9.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-taper curve and volume functions for pine, spruce and birch-951-40-0589-9]]
- Updated [[index]], [[methods/dinov3-classification]], [[concepts/tree-allometry]], [[concepts/height-diameter-inversion]], [[sources/index]]

## [2026-10-26] ingest | Appel (2017) — ALS vs UAV-LiDAR single-tree detection and CHM height stratification in Finnish forestry

- Source: `raw/papers/Skogsinventering med flygburen laserskanning-Appel_Lucas.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-skogsinventering med flygburen laserskanning-appel_lucas]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[sources/index]]

## [2026-10-26] ingest | Reese et al. (2016) — remote sensing fundamentals and operational CHM generation

- Source: `raw/papers/skoglig_fjarranalys_v1_0_161211.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-skoglig_fjarranalys_v1_0_161211]]
- Updated [[index]], [[methods/chm-detection]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Reese et al. (2018) — Swedish remote sensing textbook

- Source: `raw/papers/Skoglig Fjärranalys-Ljungbergs_SV_20180824.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-skoglig fjärranalys-ljungbergs_sv_20180824]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Sjödin (2010) — ALS volume density for pre-thinning delineation

- Source: `raw/papers/Skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/site-index-and-yield]], [[concepts/dense-stand-detection]], [[sources/index]]

## [2026-10-26] ingest | Heiðarsson et al. (2023) — Sitka spruce stem volume and biomass models in Iceland

- Source: `raw/papers/Sitka_Spruce IAS-2023-6-L-Heidarsson-K-Nystrom-A-Snorrason-69-80.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-sitka_spruce ias-2023-6-l-heidarsson-k-nystrom-a-snorrason-69-80]]
- Updated [[index]], [[concepts/tree-allometry]], [[concepts/height-diameter-inversion]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Pessacg et al. (2022) — photogrammetric DTM and mission parameters

- Source: `raw/papers/Simplifying UAV-Based Photogrammetry in Forestry_How to Generate Accurate Digital Terrain Model and Assess Flight Mission Settings-forests-13-00173.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-simplifying uav-based photogrammetry in forestry_how to generate accurate digital terrain model and assess flight mission settings-forests-13-00173]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/canopy-height-model]], [[sources/index]]

## [2026-10-26] query | Concept accepted: Height-Diameter and Crown-Diameter Inversion

- Added [[concepts/height-diameter-inversion]] from [[project/concept-proposals]]

## [2026-10-26] ingest | Vallet et al. (2025) — Height-diameter allometries for 41 European species

- Source: `raw/papers/Robust height-diameter allometries for 41 European tree species - supplementary data-2025.09.29.679156v2_media-1.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-robust height-diameter allometries for 41 european tree species - supplementary data-2025-09-29-679156v2_media-1]]
- Updated [[index]], [[methods/chm-detection]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Savine et al. (2025) — generalized H-D allometries across 41 European species and stand structures

- Source: `raw/papers/Robust height-diameter allometries for 41 European tree species - stand characteristics and structure matter-2025.09.29.679156v2_full.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-robust height-diameter allometries for 41 european tree species - stand characteristics and structure matter-2025-09-29-679156v2_full]]
- Updated [[index]], [[concepts/tree-allometry]], [[methods/chm-detection]], [[concepts/site-index-and-yield]], [[sources/index]]

## [2026-10-26] ingest | Randle et al. (2014) — FC Piecewise Crown and Root Biomass Equations

- Source: `raw/papers/revised-biomass-equations-27jan2014.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-revised-biomass-equations-27jan2014]]
- Updated [[index]], [[concepts/tree-allometry]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Shupe et al. (2022) — Quercus robur DBH-only carbon allometry

- Source: `raw/papers/Quercus robur allometry_1-s2.0-S2215016122001807-main.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-quercus robur allometry_1-s2-0-s2215016122001807-main]]
- Updated [[index]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Lantmäteriet (2022) — National LiDAR Quality and DTM Error Characteristics

- Source: `raw/papers/quality_description_lidar.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-quality_description_lidar]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[sources/index]]

## [2026-10-26] ingest | Filipescu et al. (2012) — DBH prediction from height, crown area, and CAL competition

- Source: `raw/papers/Prediction of Diameter Using Height and Crown Attributes - Filipescu_etal2012WJAFDbh_ht_model.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-prediction of diameter using height and crown attributes - filipescu_etal2012wjafdbh_ht_model]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/tree-allometry]], [[sources/index]]

## [2026-10-26] ingest | Hou & Chai (2022) — Nonlinear mixed-effects crown width models with competition

- Source: `raw/papers/Predicting_crown_width_using_nonlinear_mixed-effec.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-predicting_crown_width_using_nonlinear_mixed-effec]]
- Updated [[index]], [[methods/local-maxima]], [[methods/chm-detection]], [[concepts/tree-allometry]], [[sources/index]]

## [2026-10-26] ingest | Pyataev & Vais (2019) — Scots pine DBH–crown width Gaussian allometry

- Source: `raw/papers/Pine Crown and Trunk Diameter Dependence Research-27_short_paper.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-pine crown and trunk diameter dependence research-27_short_paper]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/tree-allometry]], [[concepts/crown-ownership]], [[sources/index]]

## [2026-10-26] ingest | Song et al. (2024) — Global height–crown–DBH parameterization across PFTs

- Source: `raw/papers/Parameterization of height–diameter and crown radius-diameter relationship across the globe - rtae005.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-parameterization of height–diameter and crown radius-diameter relationship across the globe - rtae005]]
- Updated [[index]], [[methods/deimv2-canopy]], [[methods/chm-detection]], [[sources/index]]

## [2026-10-26] ingest | Brandel (1990) — Swedish national volume functions for pine, spruce, and birch

- Source: `raw/papers/Nya volymfunktioner för Tall, Gran och Björk-brandel.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-nya volymfunktioner för tall, gran och björk-brandel]]
- Updated [[index]], [[concepts/tree-allometry]], [[concepts/site-index-and-yield]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Rytter et al. (1998) — Swedish broadleaf and mixed-stand silviculture

- Source: `raw/papers/Löv och lövblandbestånd - ekologi och skötsel-rytter_1998_redogorelse_8_100dpi.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-löv och lövblandbestånd - ekologi och skötsel-rytter_1998_redogorelse_8_100dpi]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/chm-detection]], [[methods/local-maxima]], [[sources/index]]

## [2026-10-26] ingest | Buchacher & Ledermann (2020) — mixed-effects crown width models

- Source: `raw/papers/Interregional Crown Width Models for Individual Trees Growing in Pure and Mixed Stands in Austria-forests-11-00114-v3.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-interregional crown width models for individual trees growing in pure and mixed stands in austria-forests-11-00114-v3]]
- Updated [[index]], [[methods/deimv2-canopy]], [[concepts/tree-allometry]], [[concepts/crown-ownership]], [[sources/index]]

## [2026-10-26] ingest | Näslund (1947) — Swedish stem volume equations and form-factor tables

- Source: `raw/papers/FUNKTIONER OCH TABELLER FÖR KUBERING AV STAENDE TRÄD-medd_statens_skogsforskningsinst_036_03.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-funktioner och tabeller för kubering av staende träd-medd_statens_skogsforskningsinst_036_03]]
- Updated [[index]], [[concepts/tree-allometry]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] query | Concept accepted: Foundation Model Prompting for Tree Delineation

- Added [[concepts/foundation-model-tree-delineation]] from [[project/concept-proposals]]

## [2026-10-26] query | Concept accepted: Direct Stem and DBH Measurement from 3D Point Clouds

- Added [[concepts/direct-stem-dbh-point-cloud]] from [[project/concept-proposals]]

## [2026-10-26] ingest | Lindberg & Holmgren (2014) — ALS area-based vs ITD methods for Swedish forestry

- Source: `raw/papers/Flygburen laserskanning för skogliga skattningar-faktaskog_04_2014.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-flygburen laserskanning för skogliga skattningar-faktaskog_04_2014]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Erfanifard et al. (2025) — multi-angle UAV-DAP DBH and allometric modeling

- Source: `raw/papers/Estimating tree diameter at breast height (DBH) from UAV data-1-s2.0-S2666017225001373-main.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-estimating tree diameter at breast height (dbh) from uav data-1-s2-0-s2666017225001373-main]]
- Updated [[index]], [[concepts/tree-allometry]], [[concepts/point-cloud-individual-tree-segmentation]], [[methods/chm-detection]], [[sources/index]]

## [2026-10-26] ingest | Lantmäteriet (2023) — Laser Data Download, Forest product description

- Source: `raw/papers/e_pb_laserdata_nedladdning_skog.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-e_pb_laserdata_nedladdning_skog]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/canopy-height-model]], [[sources/index]]

## [2026-10-26] ingest | Nevalainen et al. (2025) — wall-to-wall UAV inventory pipelines

- Source: `raw/papers/Drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-drone imaging-based wall-to-wall processing pipelines for individual tree level inventory in boreal forest plots]]
- Updated [[index]], [[methods/local-maxima]], [[methods/chm-detection]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-26] ingest | Manso et al. (2022) — dynamic Sitka spruce allometry and volume forecasting

- Source: `raw/papers/Diameter, height and volume increment single tree models for improved Sitka spruce in Great Britain-cpab049.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-diameter, height and volume increment single tree models for improved sitka spruce in great britain-cpab049]]
- Updated [[index]], [[concepts/tree-allometry]], [[concepts/site-index-and-yield]], [[sources/index]]

## [2026-10-26] ingest | Esfahani et al. (2026) — species-specific DBH prediction from height and relative density

- Source: `raw/papers/DBH vs Height 1-s2.0-S0378112725008801-main.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-dbh vs height 1-s2-0-s0378112725008801-main]]
- Updated [[index]], [[concepts/tree-allometry]], [[methods/dinov3-classification]], [[sources/index]]

## [2026-10-23] lint | Publish reader pages that were still drafts

- Set `status: stable` so Quartz emits them: [[concepts/crown-ownership]], [[concepts/normal-forest]], [[concepts/site-index-and-yield]], [[concepts/tree-allometry]], [[concepts/understory-tree-detection]], [[concepts/point-cloud-individual-tree-segmentation]], [[project/research-normal-forest]], [[project/normal-forest-flow]], [[project/domains]], [[experiments/normal-forest/exp-005-normal-forest-ownership-smoke]]
- Left [[project/concept-proposals]] as draft (review sheet, not a reader page)
- Page prose still says ADR-003 is proposed and exp-005 has not run

## [2026-10-23] query | Concept accepted: Point Cloud Individual Tree Segmentation

- Added [[concepts/point-cloud-individual-tree-segmentation]] from [[project/concept-proposals]]

## [2026-10-23] ingest | Wang et al. (2013) — Understory Pinus koraiensis crown & root allometry

- Source: `raw/papers/Crown_and_root_biomass_equations_fo.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-crown_and_root_biomass_equations_fo]]
- Updated [[index]], [[methods/chm-detection]], [[sources/index]]

## [2026-10-23] ingest | Blanchard et al. (2016) — Invariant DBH-crown area allometry across tropical sites

- Source: `raw/papers/Blanchard_TSAF_2016.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-blanchard_tsaf_2016]]
- Updated [[index]], [[methods/chm-detection]], [[methods/edgecrafter-ecseg]], [[sources/index]]

## [2026-10-23] ingest | Zianis et al. (2005) — European tree biomass and stem volume equations compilation

- Source: `raw/papers/Biomass and stem volume_951-40-1984-9.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-biomass and stem volume_951-40-1984-9]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/chm-detection]], [[sources/index]]

## [2026-10-23] ingest | Schorn et al. (2025) — Beech & Deciduous Allometric Scaling (DBH, Height, Crown Area)

- Source: `raw/papers/Beech allometry_BGC4810s1.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-beech allometry_bgc4810s1]]
- Updated [[index]], [[methods/chm-detection]], [[methods/dinov3-classification]], [[concepts/tree-allometry]], [[sources/index]]

## [2026-10-23] query | Concept accepted: Understory tree detection

- Added [[concepts/understory-tree-detection]] from [[project/concept-proposals]]
- Holmgren et al. (2022) and Ding (2025). Separate from [[concepts/dense-stand-detection]].

## [2026-10-23] query | Concept accepted: Tree-Level Allometric Scaling

- Added [[concepts/tree-allometry]] from [[project/concept-proposals]]

## [2026-10-23] ingest | Widlowski et al. (2003) — Allometric Relationships of European Tree Species

- Source: `raw/papers/allometric relationships of selected european tree-gp_eudor_PDFA1B_EUNA20855ENC_001.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-allometric relationships of selected european tree-gp_eudor_pdfa1b_euna20855enc_001]]
- Updated [[index]], [[concepts/site-index-and-yield]], [[concepts/crown-ownership]], [[methods/deimv2-canopy]], [[sources/index]]

## [2026-10-23] ingest | Johansson (2005) — Alder stem volume equations and wood density

- Source: `raw/papers/Alder_allometry_cpi023.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-alder_allometry_cpi023]]
- Updated [[index]], [[methods/dinov3-classification]], [[concepts/site-index-and-yield]], [[sources/index]]

## [2026-10-23] ingest | Rupšys & Petrauskas (2017) — 4-variate SDE for DBH, height, crown width, and volume

- Source: `raw/papers/A_Linkage_among_Tree_Diameter_Height_Crown_Base_He.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-a_linkage_among_tree_diameter_height_crown_base_he]]
- Updated [[index]], [[methods/chm-detection]], [[methods/deimv2-canopy]], [[sources/index]]

## [2026-10-23] ingest | Vasilescu et al. (2017) — stem profile median diameter and taper allometry

- Source: `raw/papers/A rapid method for estimating the median diameter of the stem profile of Norway spruce trees-iForest_ifor1945-009_Vasilescu.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-a rapid method for estimating the median diameter of the stem profile of norway spruce trees-iforest_ifor1945-009_vasilescu]]
- Updated [[index]], [[concepts/site-index-and-yield]], [[sources/index]]

## [2026-10-23] ingest | Raptis et al. (2018) — nonlinear crown width and DBH allometry

- Source: `raw/papers/A Crown Width-Diameter Model for Natural Even-Aged Black Pine Forest Management-forests-09-00610-v2.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-a crown width-diameter model for natural even-aged black pine forest management-forests-09-00610-v2]]
- Updated [[index]], [[methods/deimv2-canopy]], [[concepts/crown-ownership]], [[concepts/dense-stand-detection]], [[sources/index]]

## [2026-10-23] query | Concept gate on the current source set

- Reviewed ingested sources against [[concepts/index]] before the next paper batch.
- Added [[concepts/site-index-and-yield]] for dominant height, site index, and stand volume (five sources). Moved those open questions off [[concepts/canopy-height-model]].
- Left GADA, Eichhorn's rule, and Heureka on their source pages. Tree-level stem measurements stay on the eucalyptus UAV-LiDAR source. The allometry row in [[project/domains]] is still not a started program.
- Later ingests print concept proposals and do not create the page.

## [2026-10-23] lint | sources index lists every ingested paper

- Replaced the short highlight list in [[sources/index]] with one bullet per source page (34).
- Later `make ingest-paper WRITE=1` prepends new papers to that list.
- Fixed the Shaheen (2025) slug (`self-supervised`, not `self_supervised`) on [[index]] and [[concepts/literature-map-dense-itd]].

## [2026-10-23] ingest | Socha et al. (2020) — GADA Site Index and Height Growth Models for Central European Species

- Source: `raw/papers/Site Index Models for Main Forest-Forming Tree Species in Poland_forests-11-00301.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-site index models for main forest-forming tree species in poland_forests-11-00301]]
- Updated [[index]], [[concepts/canopy-height-model]], [[methods/local-maxima]], [[methods/dinov3-classification]]

## [2026-10-23] ingest | Tarmu et al. (2020) — dominant vs mean height modeling under thinning

- Source: `raw/papers/Mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_Estonian_forests.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_estonian_forests]]
- Updated [[index]], [[concepts/canopy-height-model]], [[methods/local-maxima]]

## [2026-10-23] ingest | Zhou et al. (2025) — Bottom-up ITD and DBH via Ultra-High-Density UAV-LiDAR

- Source: `raw/papers/Extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost UAV-LiDAR_in_Eucalyptus_plantations.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-extraction_of_individual_tree_attributes_using_ultra-high-density_point_clouds_acquired_by_low-cost uav-lidar_in_eucalyptus_plantations]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]], [[concepts/crown-ownership]]

## [2026-10-23] ingest | Fahlvik et al. (2014) — Heureka growth model evaluation

- Source: `raw/papers/Evaluation of growth functions used in the Swedish Forest Planning System Heureka_article1013.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-evaluation of growth functions used in the swedish forest planning system heureka_article1013]]
- Updated [[index]], [[concepts/canopy-height-model]], [[concepts/dense-stand-detection]]

## [2026-10-23] ingest | Appiah Mensah et al. (2023) — bi-temporal ALS site index (SIS) mapping

- Source: `raw/papers/AppiahMensah_et_al_2023_Site_Index_SIS_RS.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-appiahmensah_et_al_2023_site_index_sis_rs]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/canopy-height-model]]

## [2026-10-23] ingest | Appiah Mensah et al. (2022) — Potential yield capacity and allometric volume modeling in Swedish conifers

- Source: `raw/papers/AppiahMensah_et _al.2022_yield capacity.pdf` (LLM: `gemini-3.8-flash` via `make ingest-paper`)
- Added [[sources/paper-appiahmensah_et _al-2022_yield capacity]]
- Updated [[index]], [[methods/dinov3-classification]], [[concepts/canopy-height-model]]

## [2026-10-22] query | normal-forest flow for discussion

- Added [[project/normal-forest-flow]]: condensed path from the ownership sample through labels, a score, a detector student, and outlines
- Does not accept ADR-003, does not sign the 0.95 bar, and does not number any experiment after exp-005
- exp-005 gate now names four locks before CVAT: height floor, precision bar, small-set count, read cap

## [2026-10-22] hypothesis | ownership sample does not certify a large pool

- Unread candidates become ground truth only on a small set, or when the lower end of a 95% Wilson interval reaches the proposed 0.95 bar. Both paths stay proposals to lock before CVAT
- A raw 0.95 on 150 boxes does not promote the rest. The small-set count and the read cap are TBD. ADR-003 stays proposed. exp-005 stays draft

## [2026-10-21] lint | experiments grouped by domain

- `experiments/exp-001-per-layer-baselines.md` → `experiments/r-class-itd/exp-001-per-layer-baselines.md`
- `experiments/exp-002-rgb-seg-backend-ceiling.md` → `experiments/r-class-itd/exp-002-rgb-seg-backend-ceiling.md`
- `experiments/exp-003-merge-fusion-v1.md` → `experiments/r-class-itd/exp-003-merge-fusion-v1.md`
- `experiments/exp-004-rgb-small-student-pseudo-v2.md` → `experiments/r-class-itd/exp-004-rgb-small-student-pseudo-v2.md`
- `experiments/exp-005-normal-forest-ownership-smoke.md` → `experiments/normal-forest/exp-005-normal-forest-ownership-smoke.md`
- Added [[project/domains]]. Ids stay global. Species classification, stand segmentation, and allometry have no folder yet

## [2026-10-21] hypothesis | ADR-003 proposed; normal-forest priority

- Proposed ADR-003: close [[experiments/exp-004-rgb-small-student-pseudo-v2]] before Phase B; park [[experiments/exp-003-merge-fusion-v1]]; current proposal is [[project/research-normal-forest]]
- Added [[concepts/normal-forest]], [[concepts/crown-ownership]], [[experiments/exp-005-normal-forest-ownership-smoke]] (draft smoke; no training)
- AREA 540 counts on exp-004 stay. Gates on exp-004 stay TBD. The 0.95 / 0.80 bar and the height floor are proposed, not signed
- 2026-10-13 sequencing note: proposed superseded by ADR-003. ADR-002 is not rewritten. ADR-003 is not accepted

## [2026-10-13] hypothesis | exp-004 locked for the coding repo

- Train COCO = weak boxes on AREAs 473–479 plus proposals kept by Round 1 FT @400 confirmed at @200. Audit does not drop the rest. 480, 481, golden, and AREA 540 stay out of that train set
- B1 inits from Round 1 FT. DINOv3 and VLM off on the first pass. Run id for the 400∪200 fallback is `B400u200` (not C1). No H4
- Two TBD bars before A0 CVAT opens: audit precision, and the margin over Round 1 `R_small` 0.252 / `AP_small` 0.157

## [2026-10-13] hypothesis | exp-004 and audit diagrams

- Mermaid on [[experiments/exp-004-rgb-small-student-pseudo-v2]] and [[concepts/pseudo-label-audit-cvat]] for the flow, the score gate, tile sampling, and the box verdict
- Skill: Mermaid for concepts; jpg/png only when a script wrote the figure

## [2026-10-13] lint | drop financial wording from research pages

- Research pages no longer frame decisions as budget, payment, or funding
- Sample-size caps stay as technical limits; paper quotes that report a source’s own cost figures are unchanged

## [2026-10-13] hypothesis | restore CVAT audit page; pilot on AREA 540

- Restored [[concepts/pseudo-label-audit-cvat]] after accidental delete
- First CVAT pass is AREA 540 (procedure only). Train-gate sample stays 20×150 on Round 1 tiles
- Tile halves ordered by weak-box count, not by eye and not by a new segmentation or height filter

## [2026-10-13] hypothesis | exp-004 CVAT pseudo-label audit procedure

- Added [[concepts/pseudo-label-audit-cvat]]: 20 tiles / 150 new boxes, no full train upload, accept/reject/accept_resize
- Linked from [[experiments/exp-004-rgb-small-student-pseudo-v2]] human gate

## [2026-10-13] hypothesis | exp-004 board-language section intros

- Added executive summary plus “for the board” / takeaway blocks on [[experiments/exp-004-rgb-small-student-pseudo-v2]], same pattern as exp-001 / exp-002

## [2026-10-13] hypothesis | exp-004 RGB small-student (pseudo v2)

- Next detection track: one DEIMv2 student, primary eval SAHI 400, train on gap-filled pseudo v2 — not more AREA of the same weak GT
- Large-tree AP on that checkpoint is out of scope; no 800∪400 bank inside the experiment
- ADR-002 note: H2 (exp-003) and H3 follow-ups wait on the exp-004 usefulness gate (H3 preliminary close stands)
- Added [[experiments/exp-004-rgb-small-student-pseudo-v2]]; updated [[project/decisions]], [[experiments/index]], [[index]], [[experiments/exp-003-merge-fusion-v1]], [[concepts/literature-map-dense-itd]]

## [2026-10-12] ingest | Sun (2025) — RefDrone benchmark and NGDINO for drone REC

- Source: `raw/papers/RefDrone_llms.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-refdrone_llms]]
- Updated [[index]], [[methods/deimv2-canopy]], [[concepts/dense-stand-detection]]

## [2026-10-12] ingest | Iwanowski (2025) — Multi-LLM/VLM consensus for object detection

- Source: `raw/papers/multi_llm_detections.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-multi_llm_detections]]
- Updated [[index]], [[methods/merge-detections]], [[concepts/literature-map-dense-itd]]

## [2026-09-28] hypothesis | exp-001 Round2 plan: small expert + SAHI bank

- Drop single-checkpoint AP_large protection; multilayer: large=`svk_full@800`, small=FT@**400**, slice **200** = bank ablation ± size-gate
- Next: Round2 more AREAs (small expert) + oracle/NMS bank eval `800∪400(∪200)` before full exp-002
- Updated [[experiments/exp-001-per-layer-baselines]], [[methods/merge-detections]], [[experiments/index]], [[index]]

## [2026-09-28] hypothesis | exp-001 scope revision v1.1 (open/dense deferred)

- Golden `kaxen_197_1` = small crowns + sparse overlap (AREA “dense” tag ≠ closed-canopy ITD)
- H1 hypothesis rewritten: size-stratified R-class ceilings + weak-FT small↔large tradeoff; open/dense deferred to data program
- Success/Kill updated; under_seg/dup de-emphasized as dense-merge signals
- Updated [[experiments/exp-001-per-layer-baselines]], [[experiments/index]], [[index]]

## [2026-09-28] hypothesis | exp-001 box + lateral-shift plots vs golden

- Rebuilt matched TP stats + charts (`plot_box_vs_gt.py`): area ratio, IoU, lateral dx/dy (LM peak-offset hypothesis)
- Lateral shift on hits is small (~1.5–1.8 px; ~3–5% GT width); Round1 slightly higher |dx|; mean slightly left
- Area ratio closer to 1 for Round1 vs baseline; LM center-bias **not** dominant on matched TPs
- Updated [[experiments/exp-001-per-layer-baselines]] with plots in `experiments/assets/exp001_*`
- Artifacts: `research/exp-001/results/box_vs_gt_plots/`

## [2026-09-28] hypothesis | exp-001 Round 1 multi-AREA weak FT golden ladder (`002`)

- Train: AREAs 473–479 / val 480 / test 481 (`r_weak_v1_a473_481`), init `svk_full`; eval golden SAHI 800/400/200
- vs `svk_full`: 800 ΔR≈+0.13 / ΔAP_small≈+0.14 / ΔAP_large≈−0.33; 400 similar pattern; 200 nearly flat
- vs smoke `001`: better small/recall at 800/400; large-AP regression is the new risk
- Conclusion: **iterate** — keep scaling AREAs, mitigate large-box drop before merge
- Updated [[experiments/exp-001-per-layer-baselines]]; artifacts `rgb_deimv2_r_weak_sahi_*_002/`, `delta_r_weak_vs_baseline_002.json`

## [2026-09-24] hypothesis | exp-001 statistical + visual box QA vs golden GT

- Question: do weak-LM labels cause smoke FT to under-size boxes vs golden?
- Stats (IoU≥0.5): median area_pred/gt ≈1.29–1.35; covGT≈1.0 (GT inside pred); covPr≈0.74; center≈3 px; small GT more oversized than large
- Visual QA: `overlays_vs_gt/` — dominant FN; hits not systematically too small
- Conclusion: shrink hypothesis **not supported** on TPs; next = multi-AREA FT / recall, not box inflation
- Updated [[experiments/exp-001-per-layer-baselines]]; artifact `box_size_vs_gt_r_weak.json`

## [2026-09-22] hypothesis | exp-001 smoke weak-GT FT positive Δ (iterate)

- Smoke FT: AREA 540 weak tiles, init `svk_full`, ~24e; golden hold-out SAHI 800/400/200
- Δ vs baseline: 800 ΔR≈+0.019 / ΔR_large≈+0.074 (P stable); 400 ΔR≈+0.021; 200 ΔAP_small≈+0.042, small ΔR
- Direction OK; absolute small gap remains — **not** H1 success. Next: multi-AREA weak FT
- Updated [[experiments/exp-001-per-layer-baselines]] Runs/Results/Conclusion; runs `rgb_deimv2_r_weak_sahi_*_001`

## [2026-09-21] hypothesis | exp-001 next: R-class weak-GT DEIMv2 FT (iterate)

- Decision: train DEIMv2 RGB R-class on weak labels from production R detections (CHM→LM→merge); init `svk_full`
- Golden `kaxen_197_1` = hold-out eval only; re-run SAHI 800/400/200 vs baseline before multi-scale RGB merge
- Updated [[experiments/exp-001-per-layer-baselines]] Conclusion / Handoff; planned run `rgb_deimv2_r_weak_*`

## [2026-09-21] hypothesis | exp-001 SAHI slice 200 smallest-tile ablation

- Same `svk_full` on golden `kaxen_197_1`: SAHI 200 vs prior 400/800 (no merge)
- 200: n_pred 1736, R≈0.349, R_small≈0.279, AP_small≈0.157, P≈0.51 (vs 400: R_small≈0.122; 800: ≈0.063)
- Updated [[experiments/exp-001-per-layer-baselines]] — tile ladder complete for H1 RGB; multi-scale merge → exp-002

## [2026-09-15] lint | exp-001 rename sahi eval package to rgb_deimv2_sahi_800_001

- Renamed result package for readability vs slice-400: `rgb_deimv2_sahi_800_001` (pair with `rgb_deimv2_sahi_400_001`)
- Layer ids remain `rgb_deimv2_sahi_800` / `rgb_deimv2_sahi_400`; preds under `preds_rgb_deimv2_sahi_{800,400}/`

## [2026-09-15] hypothesis | exp-001 SAHI slice 400 small-tree ablation

- Same `svk_full` on golden `kaxen_197_1`: SAHI 400 vs prior 800 (no merge)
- 400: n_pred 734, R≈0.199, R_small≈0.122, AP_small≈0.068 (vs 800: R_small≈0.063, AP_small≈0.03)
- Tile size helps small crowns ~2× but gap remains; updated [[experiments/exp-001-per-layer-baselines]]

## [2026-09-15] lint | exp-001 drop oracle SAM from H1 narrative

- Archived engineer eval `sam_baseline_001` → `results/_archive/sam_oracle_raw_001` (raw SAM→box oracle; not clipped; not fair detector)
- Removed from [[experiments/exp-001-per-layer-baselines]] Runs/Results tables; silver clipped kept for exp-003
- H1 primary RGB remains `rgb_deimv2_sahi`

## [2026-09-15] hypothesis | exp-001 RGB SAHI vs no-slice (iterate)

- Same `svk_full` on golden `kaxen_197_1`: SAHI (800 / conf 0.3) vs prior no-slice
- SAHI: n_pred 433, R≈0.134, AP_small≈0.03, AP_large≈0.48 (vs no-slice R≈0.012 / AP_large≈0.09)
- Updated [[experiments/exp-001-per-layer-baselines]] — SAHI is primary RGB ceiling; conclusion still **iterate**
- Small R-class gap remains the dominant H1 signal

## [2026-09-15] hypothesis | exp-001 provisional dense RGB baseline (iterate)

- Engineer return from `conifervision-ai-train` (`research/exp-001/`)
- Data: golden `kaxen_197_1` (2534 CVAT boxes, dense R); silver SAM+clip under `research/annotations/silver/`
- Run `rgb_deimv2_001`: big-trees DEIMv2 vs golden — AP_small=0, AP_large≈0.09, R≈0.012, under_seg≈0.99 (FN-dominated)
- Run `sam_baseline_001`: oracle SAM (GT-prompted) recorded as proxy only, not fair H1 ceiling
- Updated [[experiments/exp-001-per-layer-baselines]] Results / Conclusion → **iterate**; kill not triggered
- Still missing for full H1: open-stand GT, LM, CHM+DEIMv2 layers

## [2026-09-02] sync | Operational pipeline flow from processing-chain diagram

- Updated [[project/pipeline-overview]] — Mermaid overview + **full end-to-end operational diagram** + ML/R&D diagram
- Updated [[methods/merge-detections]] — production rules (under4/above4/LM, R-class merge)
- Updated [[methods/chm-detection]] — photogrammetry CHM, height bands, production parameters
- Source: `raw/assets/PROCESSING_CHAIN_DIAGRAM.md` + verified items from `raw/assets/eic_comments.md`

## [2026-08-31] ingest | Cuttano (2026) — INSID3 training-free in-context segmentation with DINOv3

- Source: `raw/papers/insid3_in_context_segmentation_dinov3.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-insid3_in_context_segmentation_dinov3]]
- Updated [[index]], [[methods/dinov3-classification]], [[concepts/pseudo-tree-crown]]

## [2026-08-24] hypothesis | Queue H1 → H3 → H2 approved (ADR-002)

- Human selected sequence: baselines → RGB seg backend ceiling → mask-aware fusion
- Updated [[experiments/exp-001-per-layer-baselines]] (H1), [[experiments/exp-003-merge-fusion-v1]] (H2)
- Added [[experiments/exp-002-rgb-seg-backend-ceiling]] (H3)
- ADR-002 accepted in [[project/decisions]]; Current focus + [[experiments/index]] updated

## [2026-08-24] lint | Visibility lift — north star on index + literature map

- Primary objective made explicit in `AGENTS.md` Purpose (dense ITD/segmentation, ensemble)
- Root [[index]]: Current focus + links to research program, hypothesis loop, experiments; OKF frontmatter only `okf_version`
- Added [[concepts/literature-map-dense-itd]] (Tier A/B/C synthesis)
- Promoted to `stable`: research program, hypothesis loop, dense-stand, edgecrafter-ecseg, exp-001, exp-002
- `wiki_update.append_index_source` no longer bumps root index frontmatter (OKF)

## [2026-08-21] ingest | Chen (2025) — Zero-shot tree detection and segmentation with SAM2

- Source: `raw/papers/ZERO-SHOT_TREE_DETECTION_AND_SEGMENTATION_FROM_AERIAL_FOREST_IMAGERY-2506.03114v1.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-zero-shot_tree_detection_and_segmentation_from_aerial_forest_imagery-2506-03114v1]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/merge-detections]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Rodríguez-Puerta (2022) — UAV LiDAR for young forest ITD and height

- Source: `raw/papers/UAV-Based_LiDAR_Scanning_for_Individual_Tree_Detection_and_Height_Measurement_in_Young_Forest-5_2021.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-uav-based_lidar_scanning_for_individual_tree_detection_and_height_measurement_in_young_forest-5_2021]]
- Updated [[index]], [[concepts/canopy-height-model]], [[methods/chm-detection]], [[methods/local-maxima]], [[methods/merge-detections]]

## [2026-08-21] ingest | Vaschetti (2025) — TreePseCo for individual tree crown segmentation

- Source: `raw/papers/TreePseCo_Scaling_Individual_Tree_Crown_Segmentation_using_Large_Vision_Models-isprs-archives-XLVIII-M-7-2025-275-2025.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-treepseco_scaling_individual_tree_crown_segmentation_using_large_vision_models-isprs-archives-xlviii-m-7-2025-275-2025]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Holmgren (2022) — 3D density models and mean-shift for understory ITD

- Source: `raw/papers/Tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-tree_crown_segmentation_in_three_dimensions_using_density_models_derived_from_airborne_laser_scanning-holmgren_j_et_al_220114]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Pucino (2025) — CHM and ITS algorithm benchmark across vegetation types

- Source: `raw/papers/The_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-XLVIII-G-2025-1223-2025.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-the_accuracy_of_image-based_individual_tree_crown_detection_and_delineation_across_vegetation_types-isprs-archives-xlviii-g-2025-1223-2025]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Shaheen (2025) — Self-supervised 3D LiDAR tree segmentation

- Source: `raw/papers/Self-Supervised_Learning_for_Precise_Individual_Tree_Segmentation_in_Airborne_LiDAR_Point_Clouds.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-self-supervised_learning_for_precise_individual_tree_segmentation_in_airborne_lidar_point_clouds]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Young et al. (2022) — Drone parameters and ITD optimization in complex conifer forests

- Source: `raw/papers/Optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-optimizing_aerial_imagery_collection_and_processing_parameters_for_drone-based_individual_tree_mapping_in_structurally_complex_conifer_forests]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]]

## [2026-08-21] ingest | Lu (2025) — DEN4 unsupervised point cloud denoising

- Source: `raw/papers/LiDAR_point_cloud_denoising_for_individual_tree_extraction_based_on_the_Noise4Denoise-fpls-15-1490660.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-lidar_point_cloud_denoising_for_individual_tree_extraction_based_on_the_noise4denoise-fpls-15-1490660]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/canopy-height-model]]

## [2026-08-21] ingest | Li (2025) — RDT hybrid tree segmentation using UAV LiDAR

- Source: `raw/papers/Individual_Tree_Segmentation_Based_on_Region-Growing_and_Density-Guided_Canopy_3-D_Morphology_Detection_Using_UAV_LiDAR_Data.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-individual_tree_segmentation_based_on_region-growing_and_density-guided_canopy_3-d_morphology_detection_using_uav_lidar_data]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/canopy-height-model]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Tong (2025) — StarDist-based tree crown delineation

- Source: `raw/papers/Individual_tree_crown_delineation_in_high_resolution_aerial_RGB_imagery_using_StarDist-based_model-1-s2.0-S0034425725000227-main.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-individual_tree_crown_delineation_in_high_resolution_aerial_rgb_imagery_using_stardist-based_model-1-s2-0-s0034425725000227-main]]
- Updated [[index]], [[methods/edgecrafter-ecseg]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Xiang (2025) — ForestFormer3D end-to-end 3D forest segmentation

- Source: `raw/papers/ForestFormer3D_A_Unified_Framework_for_End-to-End_Segmentation_of_Forest_LiDAR_3DPoint_Clouds-2506.16991v1.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-forestformer3d_a_unified_framework_for_end-to-end_segmentation_of_forest_lidar_3dpoint_clouds-2506-16991v1]]
- Updated [[index]], [[methods/chm-detection]], [[methods/merge-detections]], [[concepts/dense-stand-detection]]

## [2026-08-21] ingest | Sparks (2022) — ITD benchmark on low/high pulse density ALS

- Source: `raw/papers/Cross-comparision-of-ITD-methods-using-low-and-hight-pulse-density-ALS-2022-Sparks-et-al.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-cross-comparision-of-itd-methods-using-low-and-hight-pulse-density-als-2022-sparks-et-al]]
- Updated [[index]], [[methods/local-maxima]], [[methods/chm-detection]], [[concepts/dense-stand-detection]]

## [2026-08-21] hypothesis | Hypothesis validation loop + Experiment template

- Added [[project/hypothesis-validation-loop]] (scientist ↔ engineer handoff)
- Strengthened `.templates/experiment.md`; refreshed [[experiments/exp-001-per-layer-baselines]], [[experiments/exp-003-merge-fusion-v1]]
- ADR-001 proposed in [[project/decisions]] (ensemble v1 success structure)
- AGENTS.md Operation: Hypothesis; Cursor rule `.cursor/rules/hypothesis-from-wiki.mdc`
- Linked from [[project/index]], [[project/research-tree-detection-ensemble]], README quick reference

## [2026-08-21] ingest | Weckman (2021) — UAV-LiDAR individual tree detection comparison

- Source: `raw/papers/Comparison_of_individual_tree-twec21_public.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-comparison_of_individual_tree-twec21_public]]
- Updated [[index]], [[methods/local-maxima]], [[methods/chm-detection]], [[methods/merge-detections]]

## [2026-08-21] ingest | Mu (2020) — K-means watershed segmentation for canopy LiDAR

- Source: `raw/papers/CANOPY_LIDAR_POINT_CLOUD_DATA_K-MEANS_CLUSTERING_WATERSHED_SEGMENTATION_METHOD-isprs-annals-VI-3-W1-2020-67-2020.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-canopy_lidar_point_cloud_data_k-means_clustering_watershed_segmentation_method-isprs-annals-vi-3-w1-2020-67-2020]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[methods/merge-detections]]

## [2026-08-21] ingest | Schladebach (2025) — BorFIT LiDAR dataset & species classification

- Source: `raw/papers/BorFIT_A_Novel_LiDAR-Based_Training_Dataset_for_Individual_Tree-essd-2025-340.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-borfit_a_novel_lidar-based_training_dataset_for_individual_tree-essd-2025-340]]
- Updated [[index]], [[methods/dinov3-classification]], [[concepts/canopy-height-model]]

## [2026-08-21] ingest | Ding (2025) — bottom-up oriented search and clustering for ALS

- Source: `raw/papers/A simple oriented search and clustering method for extracting individual forest trees from ALS point clouds-1-s2.0-S157495412400520X-main.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-a simple oriented search and clustering method for extracting individual forest trees from als point clouds-1-s2-0-s157495412400520x-main]]
- Updated [[index]], [[methods/chm-detection]], [[methods/local-maxima]], [[concepts/pseudo-tree-crown]]

## [2026-08-20] ingest | Yun (2026) — LGINet text-guided diffusion for tree species generation

- Source: `raw/papers/Linguistic_guided_image_diffusion_model_for_tree_species_generation.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-linguistic_guided_image_diffusion_model_for_tree_species_generation]]
- Updated [[index]], [[methods/dinov3-classification]]

## [2026-08-20] ingest | Marcozzi (2026) — TreeFlow conditional 3D tree generation

- Source: `raw/papers/TreeFlow.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-treeflow]]
- Updated [[index]], [[methods/chm-detection]], [[concepts/canopy-height-model]], [[concepts/pseudo-tree-crown]]

## [2026-08-20] ingest | Feng (2026) — FSOD-VFM few-shot detection & graph diffusion

- Source: `raw/papers/FSOD-VFM.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-fsod-vfm]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/deimv2-canopy]], [[concepts/dense-stand-detection]]

## [2026-08-20] ingest | Yu et al. (2026) — Hybrid Ensemble Decoder and progressive fine-tuning for cross-domain FSOD

- Source: `raw/papers/Fine-Tuning_Matters_and_Parallel_Decoder_Helps.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-fine-tuning_matters_and_parallel_decoder_helps]]
- Updated [[index]], [[methods/deimv2-canopy]], [[methods/dinov3-classification]]

## [2026-08-20] ingest | Liu et al. (2026) — EdgeCrafter compact ViTs for edge dense prediction

- Source: `raw/papers/EdgeCrafter.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-edgecrafter]]
- Updated [[index]], [[methods/dinov3-classification]], [[methods/deimv2-canopy]], [[methods/edgecrafter-ecseg]]

## [2026-08-19] ingest | Huang et al. (2026) — DEIMv2 real-time object detection with DINOv3

- Source: `raw/papers/deimv2.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/paper-deimv2]]
- Updated [[index]], [[methods/deimv2-canopy]], [[methods/dinov3-classification]]

## [2026-06-09] ingest | Vo et al. (2024) — SSL data curation (hierarchical k-means)

- Source: `raw/papers/2405.15613v2.pdf` (LLM: `gemini-3.5-flash` via `make ingest-paper`)
- Added [[sources/vo-2024-automatic-data-curation]]
- Updated [[methods/dinov3-classification]], [[concepts/canopy-height-model]], [[index]]

## [2026-06-03] ingest | Miao et al. (2024) — PTC UAV species classification

- Source: `raw/papers/remotesensing-16-01849-v2.pdf`
- Added [[sources/miao-zhang-2024-ptc-uav-species]], [[concepts/pseudo-tree-crown]]
- Updated [[methods/dinov3-classification]], [[project/pipeline-overview]], [[index]], [[methods/index]]

## [2026-06-03] init | repo bootstrap

- Created LLM Wiki repository skeleton (vault `conifervision/`, Quartz, AGENTS.md).
- Seed: [[project/pipeline-overview]], [[methods/index]].

## [2026-06-03] i18n | English as primary language

- Translated vault content to English; `AGENTS.md` requires English for all new wiki pages.

## [2026-06-03] todo | code repo integration deferred

- Added [[project/code-repo-integration]] — planned link to production codebase (separate repo); not implemented yet.

## [2026-06-05] ingest | Popescu & Wynne (2004) — LiDAR CHM local maxima

- Source: `raw/papers/Seeing_the_Trees_in_the_Forest_Using_Lidar_and_Mul.pdf`
- Added [[sources/popescu-wynne-2004-seeing-the-trees]], [[concepts/canopy-height-model]]
- Updated [[methods/local-maxima]], [[methods/chm-detection]], [[index]]
- Added **Replication pseudocode** section; ingest rule in `AGENTS.md`
- **Replication notes** on [[methods/local-maxima]], [[methods/chm-detection]], [[methods/merge-detections]], [[concepts/canopy-height-model]]
