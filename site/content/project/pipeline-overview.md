---
title: Pipeline — przegląd
type: project
tags: [pipeline, production]
status: active
updated: 2026-06-03
related_methods:
  - methods/local-maxima
  - methods/chm-detection
  - methods/deimv2-canopy
  - methods/merge-detections
  - methods/dinov3-classification
---

# Pipeline analizy obszarów leśnych (AREA)

**Status:** opis referencyjny — aktualizuj przy każdej zmianie metodologii w produkcji. Lint porównuje tę stronę z kodem i stronami `methods/`.

## 1. Pozyskanie danych

- Zdjęcia z dronów dla wybranych obszarów **AREA**.
- Budowa **orthophoto** dla danego AREA.

## 2. Detekcja drzew (geometria + CHM + AI)

1. **Local maxima** ze sliding window na modelu 3D — czubki drzew, wysokości.
2. **Canopy Height Model (CHM)** z modelu 3D i danych laserowych (ground model).
3. **Detekcja obiektów** modelem **DEIMv2** na kilku warstwach wysokościowych (małe / duże drzewa).
4. **Merge** detekcji local maxima + CHM → finalne detekcje drzew.

## 3. Klasyfikacja gatunków

1. **DINOv3** — detekcja obiektów, crop, wektory cech.
2. **Klastrowanie** — specjalista grupuje klastry wg przeważającego gatunku.
3. **Rejestr obiektów** (Delta Lake) — `weak_label` z klastrowania.
4. Trening klasyfikatora DINOv3 na ground truth + weak labels.
5. Klasyfikacja wykrytych drzew modelem wytrenowanym.

## Powiązania zewnętrzne

- Dane operacyjne i etykiety: **Delta Lake** (poza tym repo) — wiki linkuje metryki i wersje, nie duplikuje tabel.

## Metody (wiki)

| Etap | Strona wiki |
|------|-------------|
| Local maxima | [[methods/local-maxima]] |
| CHM + detekcja | [[methods/chm-detection]] |
| DEIMv2 | [[methods/deimv2-canopy]] |
| Merge | [[methods/merge-detections]] |
| DINOv3 | [[methods/dinov3-classification]] |
