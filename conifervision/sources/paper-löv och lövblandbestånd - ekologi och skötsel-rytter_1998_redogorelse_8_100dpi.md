---
title: "Löv och lövblandbestånd - ekologi och skötsel"
type: Source
tags: [silviculture, broadleaves, sweden, birch, aspen, oak, mixed-stands]
status: stable
updated: 2026-10-24
description: "Comprehensive silvicultural guide on the ecology, regeneration, thinning, and yield management of Swedish broadleaves and mixed broadleaf-conifer stands."
source_file: raw/papers/Löv och lövblandbestånd - ekologi och skötsel-rytter_1998_redogorelse_8_100dpi.pdf
authors:
  - Lars Rytter
  - Urban Nilsson
  - Ulf Johansson
year: 1998
replication_status: not_applicable
related_methods:
  - methods/dinov3-classification
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Löv och lövblandbestånd - ekologi och skötsel-rytter_1998_redogorelse_8_100dpi.pdf
    title: "Löv och lövblandbestånd - ekologi och skötsel"
---

# Löv och lövblandbestånd - ekologi och skötsel

## Summary

This report (*SkogForsk Redogörelse Nr 8, 1998*) provides an authoritative synthesis of the ecology, establishment, thinning regimes, and wood production dynamics of broadleaves (*Betula pendula*, *Betula pubescens*, *Populus tremula*, *Alnus incana*, *Alnus glutinosa*, *Quercus robur*, *Fagus sylvatica*, *Fraxinus excelsior*) in pure and mixed stands in Sweden. It outlines species-specific growth dynamics, competition between broadleaves and conifers (primarily Norway spruce and Scots pine), canopy stratification across stand development, and thinning programs aimed at balancing high-value timber production with biodiversity conservation.

## Key claims

- **Canopy dynamics & light ecology:** Birch (*Betula pendula* / *B. pubescens*) and aspen (*Populus tremula*) are obligate pioneer, light-demanding species requiring high light availability for crown survival. Shading rapidly causes lower crown recession, reducing diameter increment and weakening crown stability.
- **Nurse crop dynamics in mixed stands:** Broadleaves frequently regenerate naturally in young conifer plantations. In spruce-birch mixtures, an overstory of silver birch can protect frost-sensitive young spruce seedlings; however, if birch crown closure exceeds ~30–40% or if birch crowns whip spruce tops, spruce height growth is severely inhibited.
- **Self-thinning and natural pruning:** Dense self-sown broadleaf stands exhibit extreme natural mortality and rapid self-pruning. Birch stands established at 10,000–30,000 stems/ha naturally reduce to fewer than 2,000 stems/ha before age 20–25 through intense canopy competition.
- **Thinning regimes:** Commercial timber production from birch and oak demands early, heavy crown thinnings to release dominant trees. Birch diameter growth drops rapidly if the green crown ratio falls below 40–50% of tree height.
- **Stand structure differentiation:** In mixed stands, species partition vertical space. Birch and aspen maintain dominant/co-dominant positions in upper canopy layers, while spruce tolerates intermediate or suppressed positions, forming multi-layered or two-storied structures.

## Implications for our pipeline

- **Multi-layer canopy detection:** In mixed boreal/nemoral stands (e.g., spruce-birch mixtures), photogrammetric [[concepts/canopy-height-model|CHMs]] derived from drone imagery primarily expose dominant pioneer broadleaves (birch/aspen), obscuring suppressed or understory spruce crowns ([[concepts/understory-tree-detection|understory tree detection]]). Layered height stratification (e.g. lower layer vs upper layer in [[project/pipeline-overview]]) must account for broadleaf overstories casting diffuse shadow/structure over conifer understories.
- **Crown morphology and local maxima:** Birch and oak crowns exhibit wider, more irregular branch structures and flatter, diffuse apexes compared to conifer spires (spruce/pine). Standard point-detection algorithms relying on sharp local maxima in CHMs risk over-splitting large broadleaf crowns into multiple tree detections or under-detecting flatter crowns unless morphological adaptations or contour-based instance segmentation are used.
- **Phenological and species classification:** Broadleaf species classification via [[methods/dinov3-classification]] must account for seasonal phenology (leaf-on vs leaf-off, autumn senescence), as crown spectral signatures and visible branch architecture change drastically relative to evergreen conifers.
- **Allometry and yield estimation:** Crown diameter-to-DBH ratios differ significantly between open-grown broadleaves and shade-tolerant conifers, impacting crown-area-based biomass or volume estimations ([[concepts/site-index-and-yield]]).

## Replication pseudocode

### Prerequisites

- Species-level forestry reference tables, stand yield curves, and silvicultural growth models for Swedish site indices (H100/H50).

### Procedure

```text
# Silvicultural regime simulation for mixed birch-spruce stands
1. Initialise stand model:
   - Density: 10,000–25,000 stems/ha (naturally regenerated Betula) + 2,000–2,500 stems/ha (planted Picea abies).
2. Pre-commercial thinning (cleaning) at height 2–4 m:
   - Target residual birch density: 1,500–2,500 stems/ha retained as shelter/future crop trees.
   - Remove whips and competing broadleaves directly overtopping crop spruces.
3. First commercial thinning at height 12–14 m:
   - Select 400–600 dominant birch crop trees (green crown ratio >= 40%).
   - Thin from above to release broadleaf crowns or remove birch overstory to release spruce understory.
4. Final harvesting / Rotation:
   - Silver birch target rotation: 40–60 years (target DBH: 30–35 cm).
   - Retain mixed-species biodiversity retention patches and veteran broadleaves.
```

### Gaps / not specified in paper

- The work is a silvicultural monograph and field guide; it does not specify remote sensing algorithms, photogrammetric parameters, or automated tree delineation models.

## Quotes

- *"Lövträden är i regel mera ljuskrävande än granen, och björk och asp är utpräglade pionjärträd som fordrar full belysning för att utvecklas väl."* (p. 15)
- *"För att björken skall behålla en god diametertillväxt krävs att kronan hålls väl tilltagen. Kronandelen bör inte understiga 40–50 procent av trädhöjden."* (p. 42)

## Related pages

- [[project/pipeline-overview]] — Operational drone analysis pipeline for detection and DINOv3 classification
- [[concepts/understory-tree-detection]] — Understory and multi-layered canopy detection challenges
- [[concepts/canopy-height-model]] — Photogrammetric canopy surface representation
- [[concepts/site-index-and-yield]] — Stand development and site index estimation
- [[methods/dinov3-classification]] — Species classification applied to cropped tree crowns
