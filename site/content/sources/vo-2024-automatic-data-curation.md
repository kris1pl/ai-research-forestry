---
title: "Automatic Data Curation for Self-Supervised Learning: A Clustering-Based Approach"
type: source
tags: [data-curation, clustering, self-supervised-learning, weak-labels, satellite-imagery]
status: active
updated: 2026-06-09
replication_status: partial
source_file: raw/papers/2405.15613v2.pdf
authors: [Huy V. Vo, Vasil Khalidov, Timothée Darcet, Théo Moutakanni, Nikita Smetanin, Marc Szafraniec, Hugo Touvron, Camille Couprie, Maxime Oquab, Armand Joulin, Hervé Jégou, Patrick Labatut, Piotr Bojanowski]
year: 2024
related_methods:
  - methods/dinov3-classification
---

# Vo et al. (2024) — Automatic SSL data curation (hierarchical k-means)

**Citation:** Vo, H. V., Khalidov, V., Darcet, T., et al. (2024). Automatic Data Curation for Self-Supervised Learning: A Clustering-Based Approach. arXiv:2405.15613v2. Code: [facebookresearch/ssl-data-curation](https://github.com/facebookresearch/ssl-data-curation)

**Local file:** `raw/papers/2405.15613v2.pdf`

## Summary

Meta FAIR paper on **unsupervised dataset curation** for self-supervised pre-training. Uncurated web/satellite/text pools have **long-tailed concept distributions**; vanilla **k-means** cannot rebalance them because centroids concentrate in dense embedding regions (dominant concepts split into many clusters). The authors propose **hierarchical k-means with resampling** (Algorithm 1): repeated k-means on centroids plus per-cluster resampling of points nearest each centroid, flattening centroid density toward **uniform over data support**. Curated subsets are built via **flat** or **hierarchical top-down sampling** from the final cluster tree.

Evaluated with **DINOv2** on web images, **SBERT** on text, and **satellite patches** for **canopy height** (Tolan et al. 2023 setup). Curated data beats raw pools everywhere; on web images rivals or beats manual curation on robustness/OOD; on satellite canopy height **avg block R² +20%** vs raw backbone (Table 7).

## Key claims

* **Vanilla $k$-means Limitation:** In high dimensions, $k$-means centroids asymptotically follow the data distribution ($p^{d/(d+2)}$), meaning it over-represents dominant concepts by splitting them into many small clusters instead of balancing them (p. 7).
* **Uniform Support Convergence:** Successive hierarchical applications of $k$-means, combined with localized resampling of points closest to centroids, mathematically flattens the density distribution of centroids, converging toward a uniform distribution over the data support (p. 8).
* **Satellite Canopy Height Improvement:** Applying this curation pipeline to a pool of 18 million satellite patches to select a balanced 9 million patch subset yielded a relative improvement of **20% in the $R^2$ metric** on average for downstream canopy height estimation (p. 19).
* **Out-of-Distribution Robustness:** Features trained on automatically curated datasets show massive gains in out-of-distribution (OOD) generalization and fairness across geographic regions/income levels compared to raw or manually curated baselines (p. 15-16).

## Implications for our pipeline

* **Weak label balancing:** Stage 3 in [[methods/dinov3-classification]] clusters per-tree embeddings for specialist weak labels. Same failure mode as the paper: dominant species occupy many k-means clusters; rare species get merged. **Hierarchical k-means + resampling** is a candidate upgrade when rebalancing weak-label pools (not yet in production).
* **Canopy Height Model (CHM) & Satellite Pre-training:** The paper's successful application to canopy height estimation (using Tolan et al. 2023's framework) directly validates using this curation method if we pre-train or fine-tune backbones on regional aerial/satellite orthophotos before running local tree-level regressions.
* **Active Learning & Data Pruning:** Instead of random sampling or vanilla $k$-means for selecting representative tree crops for manual annotation, we should use the hierarchical sampling strategy to select diverse and balanced training subsets.

## Replication pseudocode

### Prerequisites

* High-quality feature extractor (e.g., DINOv2/DINOv3 for tree crops, or SBERT for text).
* GPU-supported distributed $k$-means implementation (to handle millions of vectors).
* Input embeddings $X \in \mathbb{R}^{n \times d}$.

### Procedure

```text
Algorithm: Hierarchical k-means with Resampling and Hierarchical Sampling

Inputs:
  - X: Input embeddings of shape [N, D]
  - T: Number of hierarchical levels (e.g., T = 3)
  - K_list: List of cluster counts for each level [K_1, K_2, ..., K_T] (e.g., [500k, 50k, 10k])
  - m: Number of resampling iterations per level (e.g., m = 10)
  - r_list: Number of points to resample per cluster at each level

1. Initialize Level 1:
   - Run standard k-means++ on X to get K_1 clusters.
   - Assign each point in X to its nearest centroid to get cluster assignments L_1.

2. For t = 2 to T:
   - Let the input vectors I be the centroids C_{t-1} from the previous level.
   - Run k-means++ on I to find K_t initial centroids C_t.
   - Assign I to C_t to get initial cluster assignments L_t.
   
   # Resampling-Clustering Loop to flatten the distribution
   - For step = 1 to m:
       - Initialize an empty list R.
       - For each cluster i in L_t:
           - Select the r_t points closest to centroid C_t[i] from the cluster's members.
           - Append these selected points to R.
       - Run k-means on the resampled set R to find new centroids C_t.
       - Re-assign the entire input set I to the new centroids C_t to update L_t.

3. Hierarchical Sampling (Top-Down Selection):
   - Given a target dataset size Target_N:
   - Perform binary search to find the optimal number of samples to draw from each level T cluster.
   - Recursively propagate the sample allocations down the tree from level T to level 1.
   - At level 1, sample the allocated number of points randomly ("r" sampling) from each cluster.
```

### Gaps / not specified in paper

* **Optimal Cluster Ratios:** The paper does not provide an analytical formula for choosing the optimal number of clusters ($K_t$) at each level, relying instead on empirical intuition (p. 9).
* **Resampling Size ($r_t$):** The exact value of $r_t$ is described as "half the average cluster size in each level" (p. 10), but a systematic sensitivity analysis for this threshold is missing.

## Quotes

> "This imbalance leads to biases toward a few dominant object categories in the learned presentation. We argue that balance is a necessary property of pre-trained datasets." (p. 2)

> "In high dimension, the distribution of k-means centroids thus depends on, and stays close to, the data distribution P. It means that k-means forms significantly more clusters in higher-density areas in the embedding space, which correspond to dominant concepts. As a consequence, it is impossible to rebalance datasets with a simple k-means." (p. 7)

> "Training the backbone of our curated dataset leads to significant improvements on all benchmarks, with a relative improvement of 20% in the r2 metric on average [for canopy height estimation]." (p. 19)

## Related pages

* [[project/pipeline-overview]] — The overall forest analysis pipeline.
* [[methods/dinov3-classification]] — Our species classification stage where clustering is utilized.
* [[concepts/canopy-height-model]] — Directly related to the satellite canopy height estimation application.



