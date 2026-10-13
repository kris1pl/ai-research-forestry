# Experiments

Progressive disclosure listing for research runs and evaluation results.

**Queue:** **exp-001 → exp-002 → exp-004 → exp-003**. ADR-002 remains H1 → H3 → H2; **2026-10-13 note:** H2 and H3 follow-ups **wait** on the exp-004 small-tree gate ([[project/decisions]]).

* [exp-001 per-layer baselines (size-stratified R-class)](/experiments/exp-001-per-layer-baselines.md) — **H1** — v1.1; **exp-001a closed**; bank C
* [exp-002 RGB instance-seg backend ceiling](/experiments/exp-002-rgb-seg-backend-ceiling.md) — **H3** — closed preliminary (SAM vit_h, prompt C1)
* [exp-004 RGB small-student on pseudo v2](/experiments/exp-004-rgb-small-student-pseudo-v2.md) — **next** — one DEIMv2 @ SAHI 400; teacher–student labels; no 800-merge
* [exp-003 merge / fusion v1 (segmentation-aware)](/experiments/exp-003-merge-fusion-v1.md) — **H2** — waits on exp-004 usefulness gate
