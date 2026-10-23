---
name: conifervision-wiki-voice
description: >-
  Writes Conifervision wiki pages so a non-technical reader can follow each
  section, with Mermaid diagrams for flows and script-produced jpg/png for
  measured results. Keeps the vault technical rather than financial. Use when
  creating or editing pages under conifervision/ (experiments, concepts,
  project, methods), especially experiment write-ups, audit procedures,
  hypotheses, and board-facing summaries.
---

# Conifervision wiki voice

Vault prose stays **English** (`AGENTS.md`). This skill is how those pages are shaped.

## When a page needs the plain-language layer

Add it on **experiments** and on **procedure concepts** a non-technical reader will open (audit, labelling, decision gates). Skip it on paper-source pages and on one-line index bullets.

Match the pattern already used in `conifervision/experiments/r-class-itd/exp-004-rgb-small-student-pseudo-v2.md` and `exp-002-rgb-seg-backend-ceiling.md`.

1. After the status line, add `## Executive summary (for the board)` — a few short paragraphs: what we already know, what this page decides, what is not started, what the result does **not** prove.
2. For every later `##` section, in this order:
   - `#### For the board` — plain sentences, no model IDs required
   - the existing technical body (hypothesis sentence, tables, pseudocode, links)
   - `#### Takeaway` — one or two sentences
3. Do not delete the technical body to make the page shorter. The plain text sits **above** it.

Plain words in the board blocks: photo model, rough labels, human-checked test site, small trees, large trees, window size, crown outline. Put checkpoint names, SAHI sizes, IoU, and AREA ids in the technical body.

## Pictures

Add a figure when it makes the assumption, the flow, or a result easier to see. One picture per idea.

- **Mermaid** in the page for flows, gates, and what is in or out of the score. No invented numbers on the diagram.
- **jpg or png** when a script already wrote the figure (overlays, histograms). Link it the way exp-001 does (`![[...png]]` under `experiments/assets/` or the path the page already uses). Do not redraw those plots in Mermaid.
- Skip a figure that repeats a short table.

## Research, not finance

This repository records methods, data, and results. It does not estimate money.

Do not write: budget, cost as money, pay, fund, spend, price, licence fees, or “buying” data or compute.

Say the limit in technical terms: number of runs, number of tiles, number of boxes, sample caps, agreed effort.

Leave a **quoted** figure that a paper itself reports (API price, GPU hours, FLOPs) inside that source page. Do not turn it into a project plan.

## Scope habits from the current program

When editing detection experiments, keep these unless the user changes them:

- The human-checked site `kaxen_197_1` is small crowns with space between them. Do not describe it as closed-canopy dense forest.
- A human check of new labels is a **fixed sample** in CVAT, not an upload of the whole training set and not a search for “missing trees.” Procedure: `conifervision/concepts/pseudo-label-audit-cvat.md`.
- Do not invent pass/fail numbers. Use `TBD` or “agreed before the run” until a result page already states the number.
- Large-tree scores on a small-tree model are diagnostic unless the page explicitly makes them the gate.

## Do not

- Add a financial appendix because a section mentions the board.
- Restate the whole research program inside the skill or inside every page.
