---
title: Detection merge
type: method
tags: [merge, nms, detection]
status: active
updated: 2026-06-05
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/deimv2-canopy
sources:
  - sources/popescu-wynne-2004-seeing-the-trees
---

# Merge local maxima + CHM

Combine detections from [[local-maxima]] and the CHM/DEIMv2 path into a final tree set per AREA.

## Rules

_(NMS, priorities, distances — align with production code)_

## Replication notes

[[sources/popescu-wynne-2004-seeing-the-trees]] does **not** describe merging LM with a second detector — it uses LM (or all pulses) per plot for height estimation only.

| Idea from literature | Our merge design |
|----------------------|----------------|
| LM commission/omission vs window size | Inform NMS distance / priority when LM vs DEIMv2 conflict |
| Plot-level dominant height after tree-top set | We need **instance-level** union per AREA |

**Replication pseudocode:** not applicable from this source. When a paper with explicit fusion rules is ingested, link its `sources/…#Replication pseudocode` here.

## Known issues

_(overlapping detections, duplicates at window boundaries)_

## Literature

[[sources/popescu-wynne-2004-seeing-the-trees]] — indirect: LM overlap errors; no dual-detector merge.
