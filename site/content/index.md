---
title: Conifervision Research Wiki
description: Knowledge base for forest area analysis methodology
type: project
tags: [index]
status: active
updated: 2026-06-09
---

# Conifervision Research Wiki

Compiled team knowledge on tree detection and classification methodology (drones, CHM, AI models, weak labels). Maintained by an LLM agent per `AGENTS.md` at the repository root.

## Project

- [[project/pipeline-overview]] — current production pipeline
- [[project/decisions]] — methodological decisions (ADR)
- [[project/code-repo-integration]] — **TODO:** link to production code repository

## Pipeline methods

- [[methods/_index]] — methods index

## Concepts

- [[concepts/canopy-height-model]] — CHM (DSM − DTM); satellite SSL curation link (Vo 2024)
- [[concepts/pseudo-tree-crown]] — PTC input reformation for species CNNs (UAV)

## Experiments

- (pages under `experiments/` — hypothesis, metrics, conclusions)

## Literature sources

- [[sources/popescu-wynne-2004-seeing-the-trees]] — LiDAR CHM, variable-window local maxima, multispectral fusion (2004)
- [[sources/miao-zhang-2024-ptc-uav-species]] — pseudo tree crown (PTC), UAV species classification, ResNet50/PyTorch (2024)
- [[sources/vo-2024-automatic-data-curation]] — hierarchical k-means SSL data curation, satellite canopy height (Meta FAIR, 2024)

## Navigation

- [[log]] — wiki change timeline
- Full index: see sections above; the agent updates lists on this page after each ingest.
