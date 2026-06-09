---
title: Production code repo integration (TODO)
type: project
tags: [todo, integration]
status: active
updated: 2026-06-03
---

# Production code repository — integration (TODO)

**Status:** not started. The production pipeline codebase lives in a **separate, advanced Git repository** (another folder). This research repo (`ai-research-forestry`) is intentionally standalone for now.

## Planned later (do not implement yet)

- [ ] Document sibling repo path / GitHub URL in this page
- [ ] Map each pipeline stage → code modules (`methods/*` → *Implementation* sections)
- [ ] Link experiments to `code_git_sha`, MLflow run IDs, Delta Lake snapshots
- [ ] Optional: `docs/research.md` in the code repo pointing to this wiki (GitHub Pages)
- [ ] Optional: Cursor multi-root workspace or cross-repo lint (wiki vs code paths)
- [ ] PR checklist in code repo: update ADR / `pipeline-overview` when methodology changes

## Principles (when we do it)

- **Two repos** — wiki compiles knowledge; code executes; Delta Lake holds operational data
- **Bridge with metadata**, not a monorepo merge
- See team discussion / architecture notes from 2026-06 for rationale

## Related

- [[project/pipeline-overview]] — methodology reference (may drift from code until integration)
- Root [`AGENTS.md`](../../AGENTS.md) in this repository
