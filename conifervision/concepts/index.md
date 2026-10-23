# Concepts

Cross-cutting ideas referenced by multiple pipeline methods.

* [Literature map — dense ITD](/concepts/literature-map-dense-itd.md) — prioritized synthesis of ingested papers for dense detection/segmentation
* [Dense stand detection (before clearing)](/concepts/dense-stand-detection.md) — evaluation concept for dense plots
* [Understory tree detection](/concepts/understory-tree-detection.md) — a stem under another crown; a canopy-height surface does not show it
* [Normal forest](/concepts/normal-forest.md) — merchantable crowns larger than R-class, with separable tops
* [Crown ownership](/concepts/crown-ownership.md) — 800 box, one peak in the core, height floor TBD, then a fixed sample
* [Canopy height model (CHM)](/concepts/canopy-height-model.md) — DSM − DTM; LiDAR and satellite SSL links
* [Site index and stand yield](/concepts/site-index-and-yield.md) — dominant height at a reference age, then stand volume; tree-level allometry stays on the source pages
* [Point Cloud Individual Tree Segmentation](/concepts/point-cloud-individual-tree-segmentation.md) — Existing concept canopy-height-model and literature-map-dense-itd focus on raster CHMs or dense 2D imagery, leaving direct 3D point cloud clustering and bottom-up tree instance segmentation unrepresented.
* [Tree-Level Allometric Scaling](/concepts/tree-allometry.md) — Existing concept site-index-and-yield explicitly restricts coverage to stand-level site index, dominant height, basal area, and yield capacity, leaving individual tree DBH, crown width, crown base height, and stem volume relationships unrepresented.
* [Pseudo tree crown (PTC)](/concepts/pseudo-tree-crown.md) — UAV crown reprojection before species CNN input
* [Pseudo-label audit in CVAT](/concepts/pseudo-label-audit-cvat.md) — fixed-size human check; pilot on AREA 540, then 20×150; not a full dataset upload
