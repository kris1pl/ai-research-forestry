# Pipeline methods

Implementation and supporting literature for each production stage. Overview: [Pipeline overview](/project/pipeline-overview.md).

* [Local maxima](/methods/local-maxima.md) — sliding-window LM on CHM / 3D surface (Popescu 2004 literature)
* [CHM + detection](/methods/chm-detection.md) — canopy height model and geometric detection
* [DEIMv2 (height layers)](/methods/deimv2-canopy.md) — multi-layer object detection (stub)
* [EdgeCrafter ECSeg](/methods/edgecrafter-ecseg.md) — instance segmentation layer for dense stands
* [Detection merge](/methods/merge-detections.md) — fuse LM + CHM + DEIMv2 (stub)
* [DINOv3 classification](/methods/dinov3-classification.md) — species classification, weak labels, clustering
