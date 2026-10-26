---
title: "Airborne laser scanning data estimates for forests that are candidates for thinning cuttings - calculations of volume density"
type: Source
tags: [lidar, als, thinning, volume-density, area-based-approach, forestry-inventory, allometry]
status: stable
updated: 2026-10-24
description: "SLU thesis investigating area-based estimation of volume density (massaslutenhet), height, basal area, and stem volume from low-pulse ALS for thinning prioritization."
source_file: raw/papers/Skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet.pdf
authors:
  - "Martin Sjödin"
year: 2010
replication_status: partial
generated:
  by: agent:ingest/gemini-3.5-flash
  at: 2026-10-24T12:00:00Z
sources:
  - id: primary
    resource: "raw/papers/Skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet.pdf"
    title: "Skattningar i gallringsskog med hjälp av flygburen laserskanning -beräkningar med massaslutenhet (Airborne laser scanning data estimates for forests that are candidates for thinning cuttings - calculations of volume density)"
    last_modified: 2010-12-01
related_methods:
  - methods/chm-detection
  - project/pipeline-overview
---

# Airborne laser scanning data estimates for forests that are candidates for thinning cuttings - calculations of volume density

## Summary

This master's thesis (Swedish University of Agricultural Sciences, SLU Umeå / SCA Skog AB) develops an area-based approach (ABA) for identifying pine-dominated stands (*Pinus sylvestris* and *Pinus contorta*) candidate for first thinning in northern Sweden (Älvsbyn municipality) using low-density airborne laser scanning (ALS; 0.5–1 points/$\text{m}^2$) from Lantmäteriet's National Elevation Model (NNH).

Instead of relying on tree count or age-dependent thinning templates, the study uses the historical Nordic concept of **volume density** (*massaslutenhet*, Jonsson 1914)—the ratio between existing stand volume and the volume of a fully stocked stand of identical basal-area-weighted mean height ($H_{gy}$). Using 85 field reference plots ($r = 8\text{ m}$), multiple linear regression models predicted $H_{gy}$, dominant height ($H_{dom}$), and volume density ($M$) from height percentiles, vegetation proportions, and absolute scan angles. Volume and basal area were derived algebraically from $H_{gy}$ and $M$ using classical yield formulations and form factors. When mapped at 10 m raster resolution, areas meeting thinning criteria (e.g., $H_{dom} \in [10, 16]\text{ m}$, $M \ge 0.8$) delineated operational thinning units independently of historical stand registry boundaries.

## Key claims

1. **Volume density is predictable from low-density ALS:** Using pulse densities of only 0.5–1 returns/$\text{m}^2$, volume density was estimated with $R^2 = 79.2\%$ and $\text{RMSE} = 0.09$ (relative $\text{RMSE} = 15.5\%$) on $r=8\text{ m}$ plots (p. 20).
2. **Scan angle corrects canopy penetration bias:** Incorporating the sine of the absolute scan angle ($\sin|\theta|$) significantly improved the volume density regression ($p = 0.001$), accounting for higher apparent crown interception at off-nadir angles (p. 17, 25).
3. **Height estimation precision:** ALS height metrics accurately estimated basal-area-weighted mean height ($R^2 = 93.7\%$, $\text{RMSE} = 5.13\text{ dm}$, relative $\text{RMSE} = 5.2\%$) and dominant height ($R^2 = 91.5\%$, $\text{RMSE} = 6.34\text{ dm}$, relative $\text{RMSE} = 5.5\%$) (p. 20).
4. **Derived basal area and volume:** Deriving basal area ($G$) and stem volume ($V$) indirectly from estimated $H_{gy}$ and $M$ achieved relative RMSEs of $15.4\%$ ($2.27\text{ m}^2/\text{ha}$) and $15.9\%$ ($13.3\text{ m}^3\text{sk}/\text{ha}$), respectively (p. 20).
5. **Stand-independent boundary delineation:** High-density within-stand patches eligible for thinning ($G \ge 23\text{ m}^2/\text{ha}$) were successfully extracted from stands recorded as low-density overall ($G \approx 13\text{ m}^2/\text{ha}$), proving raster-based delineation identifies sub-stand operational units better than legacy polygon registries (p. 24).

## Implications for our pipeline

- **Stand-level volume density as an alternative to individual crown counting:** In pre-thinning young stands (such as [[concepts/dense-stand-detection]]), individual tree crown delineation often undercounts suppressed and codominant stems. Adapting Jonsson's volume density ($M$) or relative canopy closure metrics provides an area-level check on total standing biomass and stocking density without requiring individual stem allometry.
- **Off-nadir scan/view angle adjustments:** Drone photogrammetric point clouds and wide-FOV UAV orthophoto flights experience severe obliquity variations across swath edges. Equation 1 includes a scan angle term ($\sin\theta$) to correct canopy penetration fractions; a similar calibration could be applied to normalized CHM canopy cover fractions in [[project/pipeline-overview]].
- **Decoupling treatment units from legacy polygons:** High-resolution raster scoring followed by spatial grouping (aggregate if gap $< 50\text{ m}$, minimum polygon size $\ge 1\text{ ha}$) aligns with the spatial clustering steps needed to map dense forest segments for automated harvesting routes.
- **Linkage to allometry and site yield:** Links directly to [[concepts/site-index-and-yield]] and [[concepts/height-diameter-inversion]] by providing functional relationships converting top height and volume density to basal area.

## Replication pseudocode

### Prerequisites

- Normalized 3D point cloud (ALS or dense photogrammetric point cloud with ground classification; e.g., CSF-filtered as in [[concepts/canopy-height-model]]).
- Field calibration plots ($r = 8\text{ m}$) with measured DBH, height, species composition, and calculated basal-area-weighted height ($H_{gy}$).
- Known species proportions: $T$ (pine / contorta), $G$ (spruce), $L$ (deciduous).

### Procedure

```text
# 1. Point Cloud Metric Extraction (per 10 m grid cell, using returns within r = 8 m radius)
For each raster cell centered at (x, y):
    pts = filter_points_within_radius(point_cloud, center=(x, y), radius=8.0)
    
    # Exclude ground points for relative height distributions (normalized z)
    veg_pts = [p for p in pts if p.z >= 0.0]  # unclassified / canopy returns
    
    p70 = percentile(veg_pts.z, 70)
    p90 = percentile(veg_pts.z, 90)
    p95 = percentile(veg_pts.z, 95)
    p100 = max(veg_pts.z)
    
    # Vegetation proportion: ratio of canopy returns above 40% of max height to total returns
    prop40 = count(veg_pts.z >= 0.40 * p100) / count(pts)
    
    # Absolute scan angle mean
    mean_scan_angle = mean([abs(p.scan_angle) for p in pts])

# 2. Regression Estimations (Table 3, p. 17; heights in dm)
H_gy_dm = 16.3 + 5.23 * p70 + 4.50 * p95
H_dom_dm = 21.1 + 4.49 * p90 + 4.83 * p100
M = -0.244 + 0.0383 * p90 + 1.32 * prop40 - 0.231 * sin(radians(mean_scan_angle))

H_gy_m = H_gy_dm / 10.0
H_dom_m = H_dom_dm / 10.0

# 3. Volume and Basal Area Calculation (Jonsson 1914; p. 19)
# Full-stand volume per hectare (VF) based on species composition (T, G, L)
VF = (T * 6.0 * (H_gy_m ** (4/3))) + (G * 4.2 * (H_gy_m ** (3/2))) + (L * 5.7 * (H_gy_m ** (4/3)))

# Standing volume (VB in m3sk/ha)
VB = M * VF

# Form factor f (Jonsson 1911, form class 0.65; dependent on H_gy)
f = lookup_jonsson_form_factor(form_class=0.65, height=H_gy_m)

# Basal area (G in m2/ha)
G_stand = VB / (H_gy_m * f)

# 4. Thinning Candidate Segmentation (ArcGIS workflow; p. 18, 23)
mask = (H_dom_m >= 10.0) & (H_dom_m <= 16.0) & (M >= 0.8) & (species_pine_fraction >= 0.70)
polygons = raster_to_vector(mask == True)
aggregated = aggregate_polygons(polygons, max_distance=50.0, min_area_ha=1.0)
thinning_units = smooth_boundaries(aggregated)
```

### Gaps / not specified in paper

- **Form factor coefficients:** The exact lookup table or closed-form formula used for Jonsson's form factor ($f$) under form class 0.65 across varying heights is referenced (Jonsson 1911) but not explicitly printed in the text (cited on p. 19).
- **Photogrammetry suitability:** The regression relies on laser beam penetration through the canopy (`prop40` and lower return percentiles). In UAV photogrammetry (SfM/ODM point clouds), canopy penetration is markedly lower than multi-return ALS, which would require retraining the empirical coefficients.
- **Flight overlap edge artifacts:** The author notes that scan angle adjustments caused thin line artifacts along swath overlap boundaries (p. 25); no automated seam-smoothing filter was specified.

## Quotes

- **On volume density definition:**  
  *"Definitionen av massaslutenhet är enligt Jonsson (1914) kvoten mellan skogens befintliga volym i förhållande till volymen i en fullsluten skog med samma grundytevägda höjd."* (p. 19)  
  *(Translation: According to Jonsson (1914), volume density is defined as the ratio between the forest's existing volume and the volume of a fully closed forest of the same basal-area-weighted height.)*
- **On scan angle significance:**  
  *"Användningen av skanningsvinkeln i funktionen för att beräkna massaslutenhet gav ett tydligt förbättrat resultat. I teorin kan variabelns påverkan bero på att trädens grenar täcker större del av marken om den betraktas med en vidare vinkel från flygplanet."* (p. 25)
- **On ALS bypassing stand boundary limitations:**  
  *"Den heltäckande bild som laserskanningen ger är istället möjlig att använda som källa till att söka skog med en specifik beskaffenhet och efter aktuellt behov bilda tillfälliga behandlingsenheter som är väl avgränsade. Med ett sådant arbetssätt borde det vara möjligt att väsentligt höja effektiviteten i skogsbruket."* (p. 26–27)

## Related pages

- [[project/pipeline-overview]] — Operational CHM and raster preparation pipeline.
- [[concepts/site-index-and-yield]] — Dominant height, site index, and stand-level volume estimation.
- [[concepts/dense-stand-detection]] — Structural assessment in dense, unthinned stands.
- [[concepts/canopy-height-model]] — Height normalization and CHM generation from point clouds.
- [[concepts/height-diameter-inversion]] — Allometric inversion predicting stand basal area and diameter distributions.
