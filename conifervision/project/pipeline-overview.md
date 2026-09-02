---
title: Pipeline overview
type: Project
description: "Status: reference description — update whenever production methodology changes. Lint compares this page against code and methods/ pages."
tags: [pipeline, production]
status: stable
updated: 2026-09-02
generated:
  by: agent:conifervision-wiki
  at: 2026-09-02T14:00:00Z
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/merge-detections
  - methods/dinov3-classification
---
# Forest area analysis pipeline (AREA)

**Status:** reference description — update whenever production methodology changes. Lint compares this page against code and `methods/` pages.

Production methodology is separated from the research north star in [[project/research-tree-detection-ensemble]].

## Operational flow (current)

Per **AREA**, the production chain runs **detect → fuse → classify**. Detection is **2D on terrain-normalised CHM rasters** derived from photogrammetric point clouds — not learned 3D point-cloud detection.

### Overview (5 steps)

```mermaid
flowchart LR
    A["Aerial survey\n+ photogrammetry"] --> B["CHM & height layers"]
    B --> C["AI detection\nDEIMv2 + LM fusion"]
    C --> D["Species classification\nDINOv3"]
    D --> E["Tree-level products\nGeoJSON / GCS"]

    style A fill:#ecf0f1
    style B fill:#d6eaf8
    style C fill:#fdebd0
    style D fill:#d5f5e3
    style E fill:#ebdef0
```

### End-to-end diagram (operational)

Full processing chain per AREA — upstream photogrammetry, GCS inputs, in-repo prep/detection/fusion/classification, orchestration, and outputs. Source: verified against production repo (`raw/assets/PROCESSING_CHAIN_DIAGRAM.md`).

```mermaid
flowchart TB
    subgraph UPSTREAM["Upstream (external to AI repo)"]
        UAV["UAV imagery + flight metadata"]
        ODM["Photogrammetry / ODM\n(orthophoto, LAZ point cloud)"]
        UAV --> ODM
    end

    subgraph GCS_IN["GCS project storage (conifervision-areas)"]
        ORTHO["Orthophoto TIF\nodm_orthophoto_xyshifted.tif"]
        LAZ["Point cloud LAZ\nodm_georeferenced_model.laz"]
        LM_IN["Local Maxima GeoJSON\n*-preds-local-maxima-ellipse-bboxes.json"]
        ODM --> ORTHO
        ODM --> LAZ
    end

    subgraph PREP["Data preparation (in repo)"]
        CSF["Ground filter CSF\nchm_rasterizer.py"]
        CHM["Canopy Height Model\nCHM grayscale raster"]
        LAYER["Height-stratified layers\npreprocess_2d_raster_layer.py\nlower 0.3–4 m | upper 4–30 m\nR-class band 0–7.77 m"]
        LAZ --> CSF --> CHM --> LAYER
    end

    subgraph DETECT["Tree detection (DEIMv2 + DINOv3 backbone)"]
        SAHI["SAHI tiled inference\nrun_cloud_preds_chm_skip_empty_multiprocess.py"]
        AI_LOW["AI preds — lower layer\npreds_under4.json"]
        AI_UP["AI preds — upper layer\npreds_above4.json"]
        AI_R["AI preds — R-class\n50px / 100px slices"]
        LAYER --> SAHI
        SAHI --> AI_LOW
        SAHI --> AI_UP
        SAHI --> AI_R
    end

    subgraph FUSE["Rule-based fusion"]
        MERGE["Merge AI + Local Maxima\nnms_ai_lm.py\nmerge_rclass_ai_lm.py"]
        AI_LOW --> MERGE
        AI_UP --> MERGE
        AI_R --> MERGE
        LM_IN --> MERGE
        MERGE --> PREDS["Fused tree hypotheses\nGeoJSON preds.json"]
    end

    subgraph CLASSIFY["Species attribution (downstream)"]
        CROP["Crop crown regions\nfrom orthophoto"]
        DINO["DINOv3 classifier\nreclassify_detection_crops_dinov3.py"]
        OUT["Tree-level output\nGeoJSON + category_id, score"]
        ORTHO --> CROP
        PREDS --> CROP
        CROP --> DINO --> OUT
    end

    subgraph ORCH["Orchestration (GCE)"]
        STARTUP["startup_chm_reclass_full_flow.sh"]
        PY_ORCH["orchestrate_chm_reclass_full_flow_r.py\n(parallel areas)"]
        PY_ORCH --> STARTUP
        STARTUP -.-> PREP
        STARTUP -.-> DETECT
        STARTUP -.-> FUSE
        STARTUP -.-> CLASSIFY
    end

    subgraph GCS_OUT["Outputs"]
        OUT --> GCS_PRED["gs://.../preds/preds.json"]
        OUT --> GCS_RECLASS["gs://.../preds/preds_reclassified_*.json"]
        MERGE --> GCS_STATS["stats_*.json, log_*.json"]
    end

    style UPSTREAM fill:#f5f5f5,stroke:#999
    style ORCH fill:#e8f4fc,stroke:#2980b9
    style FUSE fill:#fef9e7,stroke:#f39c12
    style CLASSIFY fill:#eafaf1,stroke:#27ae60
```

### Stages

1. **Inputs** — orthophoto, photogrammetric LAZ, and precomputed local-maxima GeoJSON in GCS per AREA.
2. **CHM prep** — CSF ground filtering, CHM rasterisation, height-stratified layers ([[methods/chm-detection]]).
3. **Detection** — DEIMv2 + SAHI on CHM tiles per height band; local maxima run in parallel ([[methods/deimv2-canopy]], [[methods/local-maxima]]).
4. **Fusion** — rule-based merge of AI predictions and local maxima ([[methods/merge-detections]]).
5. **Classification** — DINOv3 on orthophoto crops mapped from fused detection boxes ([[methods/dinov3-classification]]).

Orchestration: `startup_chm_reclass_full_flow.sh` with multi-area Python orchestrator on GCE.

## ML / R&D track (separate)

Model improvement runs as a **batch lifecycle**, not inside the per-AREA operational chain:

features → Delta Lake → clustering / weak labels → DINOv3 training → approved model deploy back to operational reclassification.

Clustering and weak-label workflows support classifier training; they are **not** part of the operational detect→fuse→classify sequence.

```mermaid
flowchart TB
    subgraph INPUTS["Inputs"]
        IMG["Orthophoto tiles / drone images"]
        DET_JSON["Detection JSON or new detections"]
    end

    subgraph FEAT["Feature extraction"]
        SLICE["TIF training slicer\ntif_training_slicer.py"]
        FP["Features pipeline\nfeatures_pipeline_dinov3.py"]
        CROPS["Object crops → GCS"]
        VEC["Feature vectors\nCNN / DINOv3 / additional"]
        IMG --> SLICE --> FP
        DET_JSON --> FP
        FP --> CROPS
        FP --> VEC
    end

    subgraph LAKE["Delta Lake (deltalake_unified)"]
        OM["objects_metadata"]
        CR["clustering_results"]
        WL["weak_labels_history"]
        VM["vae_models"]
        VEC --> OM
    end

    subgraph CLUSTER["Structural discovery"]
        KM["KMeans / HDBSCAN / DBSCAN\ncreate_clusters_for_atlas*.py"]
        VAE["CM-VAE clustering\ncmvae_cluster/"]
        PATCH["Patch delineation\nSLIC + HDBSCAN\npatch_delineation/"]
        OM --> KM
        OM --> VAE
        KM --> CR
        VAE --> CR
    end

    subgraph HUMAN["Human in the loop"]
        REV["Cluster review & naming"]
        CAT["categorization.json"]
        CR --> REV --> CAT
    end

    subgraph TRAIN["Classifier training"]
        IMP["Weak labels import\nrun_weak_labels_import.py"]
        D3T["DINOv3 training\ntrain_dinov3/"]
        MODEL["Approved classifier\n→ GCS model store"]
        CAT --> IMP --> WL
        WL --> D3T --> MODEL
    end

    MODEL -.->|"deploy to operational chain"| CLASSIFY_OP["Operational reclassification"]

    style LAKE fill:#ebf5fb,stroke:#2874a6
    style HUMAN fill:#fdedec,stroke:#c0392b
    style TRAIN fill:#eafaf1,stroke:#27ae60
```

## Not in production

See [[project/research-tree-detection-ensemble]] for the experimental program:

- RGB instance segmentation ensemble and mask-aware fusion (dense stands)
- LiDAR-assisted co-registration (external / development target)
- Automated analysis-type routing

**Literature (not in production):** [[concepts/pseudo-tree-crown]] from [[sources/miao-zhang-2024-ptc-uav-species]] — optional 3D-style crown reprojection before CNN input; tested with ResNet50 on UAV orthophoto patches, not DINOv3.

## External integrations

- Operational data and labels: **Delta Lake** (outside this repo) — the wiki links metrics and versions; it does not duplicate tables.

## Methods (wiki)

| Stage | Wiki page |
|-------|-----------|
| Local maxima | [[methods/local-maxima]] |
| CHM + detection | [[methods/chm-detection]] |
| DEIMv2 | [[methods/deimv2-canopy]] |
| Merge | [[methods/merge-detections]] |
| DINOv3 | [[methods/dinov3-classification]] |
