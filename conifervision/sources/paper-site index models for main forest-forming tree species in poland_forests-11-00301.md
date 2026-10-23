---
title: "Site Index Models for Main Forest-Forming Tree Species in Poland"
type: Source
tags: [site-index, growth-models, gada, height-growth, allometry, poland]
status: stable
updated: 2026-10-24
description: "Presents dynamic GADA-derived base-age invariant site index and height growth models for eight major Polish tree species using 3,052 stem analyses."
source_file: raw/papers/Site Index Models for Main Forest-Forming Tree Species in Poland_forests-11-00301.pdf
authors:
  - Jarosław Socha
  - Luiza Tymińska-Czabańska
  - Ewa Grabska
  - Stanisław Orzeł
year: 2020
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: raw/papers/Site Index Models for Main Forest-Forming Tree Species in Poland_forests-11-00301.pdf
    title: "Site Index Models for Main Forest-Forming Tree Species in Poland"
---

# Site Index Models for Main Forest-Forming Tree Species in Poland

## Summary

This paper develops dynamic, base-age invariant site index (SI) and dominant height growth models for eight primary forest-forming species in Poland: Scots pine (*Pinus sylvestris*), European beech (*Fagus sylvatica*), black alder (*Alnus glutinosa*), European larch (*Larix decidua*), silver birch (*Betula pendula*), oak (*Quercus* sp.), Norway spruce (*Picea abies*), and silver fir (*Abies alba*). Reconstructed growth series from stem analysis of 3,052 dominant/codominant trees across Poland were fitted to five candidate generalized algebraic difference approach (GADA) formulations.

The models explained $\ge 97.5\%$ of height growth variance (adjusted $R^2 \ge 0.975$, MAE between $0.60\text{ m}$ and $0.91\text{ m}$). Comparisons against historic Central European yield tables (e.g., Schwappach, Schober, Turin) revealed substantial divergence, especially in juvenile and mature age classes. The authors attribute these discrepancies to accelerated stand growth dynamics over the past century (e.g., increased temperature, nitrogen deposition, elevated $\text{CO}_2$, and shifted silvicultural rotation/regeneration techniques).

## Key claims

- **Model formulation & selection:** Depending on species, different GADA formulations yielded the best combination of statistical goodness-of-fit (AIC, MAE, $R^2_{\text{adj}}$), unbiased residuals, and biological behavior (e.g., higher site quality culminating earlier, no crossing curves):
  - Model M1 (Cieszewski 2001 formulation): Recommended for Scots pine ($R^2_{\text{adj}} = 0.989$, $\text{MAE} = 0.60\text{ m}$), European beech (alongside M5), black alder ($R^2_{\text{adj}} = 0.985$, $\text{MAE} = 0.73\text{ m}$), and silver birch ($R^2_{\text{adj}} = 0.984$, $\text{MAE} = 0.74\text{ m}$).
  - Model M3 (Cieszewski 2004 / Bertalanffy–Richards GADA): Recommended for Norway spruce ($R^2_{\text{adj}} = 0.985$, $\text{MAE} = 0.83\text{ m}$) based on residual structure despite M1 having marginally lower AIC.
  - Model M4 (Sharma et al. 2011 rational GADA): Recommended for European larch ($R^2_{\text{adj}} = 0.983$, $\text{MAE} = 0.88\text{ m}$).
  - Model M5 (Anta et al. 2006 / McDill–Amateis GADA/ADA): Recommended for Oak ($R^2_{\text{adj}} = 0.986$, $\text{MAE} = 0.70\text{ m}$) and Silver fir ($R^2_{\text{adj}} = 0.978$, $\text{MAE} = 0.92\text{ m}$).
- **Yield table obsolescence:** Century-old yield tables poorly represent modern stand growth rates. Specifically, modern Norway spruce exhibits significantly faster juvenile height growth than predicted by historical tables, whereas silver fir maintains height growth past 100–150 years without the premature growth plateau shown in yield tables.
- **Top height definition:** Reconstructed heights correspond to top height ($H_{\text{top}}$), defined as the mean height of the 100 thickest trees per hectare, avoiding silvicultural thinning bias associated with Lorey's mean height.

## Implications for our pipeline

- **Height-to-Age / Site Productivity from [[concepts/canopy-height-model]]:** In [[project/pipeline-overview]], drone photogrammetric CHMs provide direct top height estimates ($H_{\text{top}}$). Inverting these dynamic GADA equations provides mathematical bounds for stand age or site index when species classifications from [[methods/dinov3-classification]] are available.
- **Stratification and Crown Size Constraints:** For instance segmentation and crown ownership validation ([[concepts/crown-ownership]], [[concepts/normal-forest]]), expected crown width and spacing correlate with species-specific dominant height trajectories. Modern height growth curves prevent underestimating juvenile stand heights or overestimating mature height ceilings.
- **Dominant vs. Mean Height Cross-Validation:** Like [[sources/paper-mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_estonian_forests]], this work reinforces that top height is insensitive to low thinning, confirming $H_{\text{top}}$ as the ideal metric extracted from local maxima over upper canopy layers.

## Replication pseudocode

### Prerequisites

- Species identification ($S \in \{\text{Scots pine}, \text{Norway spruce}, \text{European beech}, \dots\}$) from [[methods/dinov3-classification]].
- Stand top height $H_0$ measured at observed age $t_0$, or known site index $S_I = H_1$ at reference base age $t_1 = 100$ years.
- Model parameters $b_1, b_2, b_3$ from Table 3 for the target species GADA function.

### Procedure

```text
# Compute dominant height H1 at age t1 given measured height H0 at age t0
# Example: Scots Pine using Model M1 (Cieszewski 2001)
1. Load fitted parameters for species (e.g., Scots pine M1):
   b1 = 1.366, b2 = 5802.862, b3 = 30.581

2. Given input height H0 at stand age t0:
   Z0 = H0 - b3
   R  = Z0 + sqrt(Z0^2 + (2 * b2 * H0) / (t0^b1))

3. Predict height H1 at target age t1 (or calculate site index where t1 = 100):
   H1 = H0 * (t1^b1) * ((t0^b1 * R + b2) / (t1^b1 * R + b2))

4. Inverse evaluation (Site Index estimation):
   Set t1 = reference_base_age (e.g., 100 years).
   SI = H1 calculated from step 3.
```

### Gaps / not specified in paper

- **Regional geographic parameters:** Spatial coordinates and regional climate covariates were omitted from the final models; the models assume pan-Poland average growth conditions despite noted NE–SW climatic gradients.
- **Crown allometry:** The paper measures solely vertical stem elongation; crown radius and crown ratio curves matching these height series are not reported.
- **Conversion to mean height ($H_{\text{mean}}$):** The paper does not provide explicit regression models between top height ($H_{100}$) and stand mean height ($H_{\text{mean}}$) or Lorey's height.

## Quotes

- *"Due to the frequent occurrence of pine stands exceeding the height of Schwappach’s first class, Szymkiewicz extrapolated tables for class Ia, however, simple graphical extrapolation raises large doubts in this case... Schwappach’s tables use the mean Lorey’s height to measure the site index. Influenced by the intensity of silvicultural treatment, Lorey’s height does not represent site productivity well."* (p. 2)
- *"High values of the adjusted... coefficients of determination ($R^2_{\text{adj}}$) indicate that selected models accounted for at least 97.5% of the total variation in the data... mean absolute errors ranged between 0.60 m (Scots pine) and 0.91 m (silver fir)."* (p. 11)
- *"For most species, the two types of models showed the largest differences for either the youngest or the oldest age classes... for Norway spruce, the results show that the height growth of younger stands is considerably faster than what is found according to yield tables."* (p. 11)

## Related pages

- [[project/pipeline-overview]] — Operational pipeline using CHM and DINOv3 species identification
- [[concepts/canopy-height-model]] — Photogrammetric and LiDAR CHM surface generation
- [[concepts/normal-forest]] — Standard commercial forest stands requiring dominant height and crown modeling
- [[sources/paper-mean_height_or_dominant_height_–_what_to_prefer_for_modelling_the_site_index_of_estonian_forests]] — Dominant height vs. mean height dynamics and thinning insensitivity
