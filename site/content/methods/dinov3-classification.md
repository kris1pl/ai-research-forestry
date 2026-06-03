---
title: DINOv3 — klasyfikacja gatunków
type: method
tags: [dinov3, classification, weak-labels]
status: active
updated: 2026-06-03
---

# DINOv3 klasyfikacja

1. Detekcja obiektów modelem DINOv3, crop, wektory cech.
2. Klastrowanie + etykiety od specjalisty → **weak labels** w Delta Lake.
3. Trening klasyfikatora na ground truth + weak labels.
4. Klasyfikacja wykrytych drzew.

## Powiązane koncepty

- Weak labels: strona `concepts/weak-labels` _(do utworzenia przy ingest)_

## Literatura / źródła

_(po ingest)_
