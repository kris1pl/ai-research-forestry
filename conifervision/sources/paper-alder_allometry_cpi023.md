---
title: "Stem volume equations and basic density for grey alder and common alder in Sweden"
type: Source
tags: [allometry, volume, alder, biomass, basic-density, yield]
status: stable
updated: 2026-10-23
description: "Empirical stem volume models, basic wood density, and stand yield relationships for Alnus incana and Alnus glutinosa across Sweden."
source_file: raw/papers/Alder_allometry_cpi023.pdf
authors:
  - Tord Johansson
year: 2005
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-23T12:00:00Z
related_methods:
  - methods/chm-detection
  - methods/dinov3-classification
sources:
  - id: primary
    resource: raw/papers/Alder_allometry_cpi023.pdf
    title: "Stem volume equations and basic density for grey alder and common alder in Sweden"
---

# Stem volume equations and basic density for grey alder and common alder in Sweden

## Summary

This study establishes individual stem volume allometric equations and basic wood density values for natural stands of grey alder (*Alnus incana*) and common alder (*Alnus glutinosa*) across latitudinal gradients in Sweden. Based on destructive sampling and section-wise mensuration of felled trees, the author determined that grey alder stem volume is accurately predicted using diameter at breast height ($D$) and total tree height ($H$), whereas common alder volume estimates are notably improved by adding crown base height ($CH$) to account for stem taper. Additionally, basic wood density measurements revealed systematic differences between the two species, with common alder displaying denser stemwood than grey alder, while crown twig densities remained similar across both species.

## Key claims

- **Model formulation for grey alder:** For *Alnus incana*, inclusion of crown base height does not significantly improve volume prediction over models relying solely on $D$ and $H$. The chosen polynomial form (Equation 2E) yielded an $R^2 = 0.99$ with minimal residual error.
- **Model formulation for common alder:** For *Alnus glutinosa*, crown base height ($CH$) serves as an informative predictor of stem taper; the power model incorporating $D$, $H$, and $CH$ (Equation 4E) achieved the lowest root mean squared error ($R^2 = 0.99$).
- **Wood basic density disparities:** Stem basic density under bark differs considerably between the species:
  - Grey alder stemwood averages $359 \text{ kg m}^{-3}$ (range 230–440).
  - Common alder stemwood averages $427 \text{ kg m}^{-3}$ (range 370–490).
- **Branch and twig density parity:** Wood basic density in lower and lateral crown twigs was statistically indistinguishable between species, averaging roughly $415\text{--}423 \text{ kg m}^{-3}$.
- **Stand productivity and silviculture:** Naturally regenerated unmanaged or late-thinned alder stands maintain high stem density and high basal area, with mean annual volume increment averaging $12.0 \text{ m}^3\text{ ha}^{-1}\text{ a}^{-1}$ for grey alder and $8.4 \text{ m}^3\text{ ha}^{-1}\text{ a}^{-1}$ for common alder. Early thinning below $3000\text{ stems ha}^{-1}$ at height 3–4 m is recommended to maximize merchantable stem growth.

## Implications for our pipeline

- **Downstream allometry and volume estimation:** Provides standard Scandinavian volumetric models when individual tree detections are attributed as *Alnus* species by [[methods/dinov3-classification]].
- **Crown height parameters:** For common alder, crown base height ($CH$) significantly modulates stem volume. In drone pipelines leveraging [[concepts/canopy-height-model]], vertical height profiles extracted from photogrammetric or LiDAR point clouds can estimate crown base height to refine volume calculations.
- **Biomass conversion factors:** The documented basic densities ($359 \text{ kg m}^{-3}$ for *A. incana*, $427 \text{ kg m}^{-3}$ for *A. glutinosa*) enable direct conversion from detected stem volumes to dry stem biomass in broadleaf-dominated wetland or riparian buffer zones.
- **Dense stand handling:** The paper's observations on unmanaged alder stands exceeding 4000 stems ha$^{-1}$ align with challenges targeted in [[concepts/dense-stand-detection]] and pre-thinning deciduous stand monitoring.

## Replication pseudocode

### Prerequisites

- Species classification identifying *Alnus incana* vs. *Alnus glutinosa* (e.g., from [[methods/dinov3-classification]]).
- Estimated diameter at breast height ($D$, in cm) derived from crown metrics or allometric allometry.
- Total tree height ($H$, in m) extracted from the [[concepts/canopy-height-model]].
- (Optional, for common alder) Crown base height ($CH$, in m) derived from CHM vertical profiling.

### Procedure

```text
# High-level volume calculation per tree detection
1. Parse tree attributes: species, D (cm), H (m), and CH (m, if available).
2. If species == "Alnus incana" (Grey alder):
   # Model 2E parameterization (Johansson 2005, Table 2)
   # V in dm3; coefficients: b0 = 0.006090, b1 = 0.000640, b2 = 0.000065
   stem_volume_dm3 = 0.006090 + 0.000640 * (D ** 2) + 0.000065 * (D * H)
   stem_volume_m3 = stem_volume_dm3 / 1000.0
   stem_biomass_kg = stem_volume_m3 * 359.0

3. Else if species == "Alnus glutinosa" (Common alder):
   If CH is known:
       # Model 4E parameterization (Table 2)
       # coefficients: b0 = 0.000057, b1 = 1.966900, b2 = 0.829200, b3 = 0.101300
       stem_volume_dm3 = 0.000057 * (D ** 1.966900) * (H ** 0.829200) * (CH ** 0.101300)
   Else:
       # Model 3E fallback (without crown height, Table 2)
       # coefficients: b0 = 0.000049, b1 = 1.929100, b2 = 1.004000
       stem_volume_dm3 = 0.000049 * (D ** 1.929100) * (H ** 1.004000)
   stem_volume_m3 = stem_volume_dm3 / 1000.0
   stem_biomass_kg = stem_volume_m3 * 427.0

4. Return stem_volume_m3 and stem_biomass_kg.
```

### Gaps / not specified in paper

- **Remote-sensing $D$ estimation:** The equations require ground DBH ($D$); predicting $D$ from crown diameter or crown area from drone imagery requires secondary crown-to-stem allometric relationships.
- **Automated crown base height detection:** The paper measured live crown base height manually via field felling and hypsometry; automated detection of $CH$ from photogrammetric UAV point clouds in dense broadleaf stands is frequently noisy due to sub-canopy occlusion.

## Quotes

> "The adopted model for grey alder was based on diameter at breast height and height. For common alder, crown height was added to diameter and height." (p. 249)

> "In the present study, basic density for common alder stems was higher (427 kg m-3) than for grey alder (359 kg m-3). Density for twigs was at the same level for both species." (p. 259)

> "The most important operation is to thin the alder stands at an early phase, e.g. when the trees are 3–4 m high. After thinning the stem number should not exceed 3000 stems ha-1." (p. 260)

## Related pages

- [[project/pipeline-overview]]
- [[concepts/site-index-and-yield]]
- [[concepts/canopy-height-model]]
- [[concepts/dense-stand-detection]]
- [[methods/dinov3-classification]]
