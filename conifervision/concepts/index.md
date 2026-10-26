# Concepts

Cross-cutting ideas referenced by multiple pipeline methods.

* [Literature map — dense ITD](/concepts/literature-map-dense-itd.md) — prioritized synthesis of ingested papers for dense detection/segmentation
* [Dense stand detection (before clearing)](/concepts/dense-stand-detection.md) — evaluation concept for dense plots
* [Understory tree detection](/concepts/understory-tree-detection.md) — a stem under another crown; a canopy-height surface does not show it
* [Normal forest](/concepts/normal-forest.md) — merchantable crowns larger than R-class, with separable tops
* [Crown ownership](/concepts/crown-ownership.md) — 800 box, one peak in the core, height floor TBD, then a fixed sample
* [Canopy height model (CHM)](/concepts/canopy-height-model.md) — DSM − DTM; LiDAR and satellite SSL links
* [Site index and stand yield](/concepts/site-index-and-yield.md) — dominant height at a reference age, then stand volume; tree-level allometry stays on the source pages
* [Stem Taper Curve](/concepts/stem-taper-curve.md) — Existing concept tree-allometry covers total stem volume and whole-tree scaling relations, leaving continuous longitudinal diameter profile functions along tree height unrepresented.
* [Area-Based Approach](/concepts/area-based-approach.md) — Existing concept literature-map-dense-itd covers individual tree detection workflows, leaving the standard plot- and grid-level statistical modeling of forest structural attributes (ABA) unrepresented.
* [Height-Diameter and Crown-Diameter Inversion](/concepts/height-diameter-inversion.md) — Existing concept tree-allometry covers forward scaling of DBH to volume/crown metrics, whereas remote sensing inventory relies on inverted allometric formulations predicting DBH from height, crown width, and stand density.
* [Foundation Model Prompting for Tree Delineation](/concepts/foundation-model-tree-delineation.md) — Existing concepts literature-map-dense-itd and dense-stand-detection focus on conventional CNN/watershed/NMS detection pipelines rather than zero-shot/few-shot prompting workflows leveraging vision foundation models (SAM/SAM2/DINOv2/v3) for crown delineation.
* [Direct Stem and DBH Measurement from 3D Point Clouds](/concepts/direct-stem-dbh-point-cloud.md) — Existing concept tree-allometry covers empirical/allometric models predicting DBH from height or crown metrics rather than direct geometric stem reconstruction, trunk detection, and diameter extraction directly from 3D point cloud slices.
* [Point Cloud Individual Tree Segmentation](/concepts/point-cloud-individual-tree-segmentation.md) — Existing concept canopy-height-model and literature-map-dense-itd focus on raster CHMs or dense 2D imagery, leaving direct 3D point cloud clustering and bottom-up tree instance segmentation unrepresented.
* [Tree-Level Allometric Scaling](/concepts/tree-allometry.md) — Existing concept site-index-and-yield explicitly restricts coverage to stand-level site index, dominant height, basal area, and yield capacity, leaving individual tree DBH, crown width, crown base height, and stem volume relationships unrepresented.
* [Pseudo tree crown (PTC)](/concepts/pseudo-tree-crown.md) — UAV crown reprojection before species CNN input
* [Pseudo-label audit in CVAT](/concepts/pseudo-label-audit-cvat.md) — fixed-size human check; pilot on AREA 540, then 20×150; not a full dataset upload
