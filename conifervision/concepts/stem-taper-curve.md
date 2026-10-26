---
title: "Stem Taper Curve"
type: Concept
description: "Existing concept tree-allometry covers total stem volume and whole-tree scaling relations, leaving continuous longitudinal diameter profile functions along tree height unrepresented."
tags: [stem, taper, curve]
status: stable
updated: 2026-10-26
generated:
  by: agent:concept-gate
  at: 2026-10-26T11:10:34Z
sources:
  - sources/paper-taper curve and volume functions for pine, spruce and birch-951-40-0589-9
  - sources/paper-a rapid method for estimating the median diameter of the stem profile of norway spruce trees-iforest_ifor1945-009_vasilescu
  - sources/paper-diameter, height and volume increment single tree models for improved sitka spruce in great britain-cpab049
---

# Stem Taper Curve

Existing concept tree-allometry covers total stem volume and whole-tree scaling relations, leaving continuous longitudinal diameter profile functions along tree height unrepresented.

This page names the shared idea. It does not open an experiment folder. [[project/domains]] does not gain a new program from this page.

```mermaid
flowchart LR
  sources["Source pages"] --> concept["This concept"]
```

## What the sources describe

- [[sources/paper-taper curve and volume functions for pine, spruce and birch-951-40-0589-9]] — Foundational Finnish national forest inventory models for stem taper curves and volume equations for pine, spruce, and birch across Finland.
- [[sources/paper-a rapid method for estimating the median diameter of the stem profile of norway spruce trees-iforest_ifor1945-009_vasilescu]] — Presents empirical models demonstrating that the median diameter of the longitudinal stem profile in Norway spruce occurs at ~0.3 × height and is strongly predicted by DBH.
- [[sources/paper-diameter, height and volume increment single tree models for improved sitka spruce in great britain-cpab049]] — Climate-sensitive single-tree diameter and height difference equations coupled with stem taper integration for volume forecasting in improved Sitka spruce.

Stand dominant height, site index, and stand volume stay on [[concepts/site-index-and-yield]].

## Replication notes

Coefficients stay on the source pages. Nothing here is implemented in the detection pipeline.

| Paper | Our status |
|---|---|
| [[sources/paper-taper curve and volume functions for pine, spruce and birch-951-40-0589-9]] — Taper Curve and Volume Functions for Pine, Spruce and Birch | TBD |
| [[sources/paper-a rapid method for estimating the median diameter of the stem profile of norway spruce trees-iforest_ifor1945-009_vasilescu]] — A rapid method for estimating the median diameter of the stem profile of Norway spruce (Picea abies Karst) trees | TBD |
| [[sources/paper-diameter, height and volume increment single tree models for improved sitka spruce in great britain-cpab049]] — Diameter, height and volume increment single tree models for improved Sitka spruce in Great Britain | TBD |

## Related

- [[concepts/site-index-and-yield]] — stand site index and stand volume
- [[concepts/crown-ownership]] — a crown box is not yet a measured crown width
- [[concepts/canopy-height-model]] — tree height read from the canopy surface
- [[project/domains]] — allometry program not started
