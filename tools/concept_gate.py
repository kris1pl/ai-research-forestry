#!/usr/bin/env python3
"""Propose concept pages, then let a person accept, reject, or correct them.

`make concept-gate` writes conifervision/project/concept-proposals.md.
Edit `decision` to accept or reject, and edit name / slug / why to correct.
`make concept-gate APPLY=1` writes a concept page only for decision: accept.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timezone

from tools.llm import ChatMessage, get_llm_client
from tools.okf_common import BUNDLE_ROOT, iso_generated_at, split_frontmatter

REVIEW_PATH = BUNDLE_ROOT / "project" / "concept-proposals.md"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SYSTEM = """\
You review a research wiki after a batch of paper ingests.
Return ONLY valid JSON (no markdown fences):

{
  "proposals": [
    {
      "name": "Short concept name",
      "slug": "kebab-case",
      "why": "One sentence: which existing concept does not hold this idea",
      "sources": ["sources/slug-without-md", "sources/another-slug"]
    }
  ]
}

Rules:
- English only
- Propose a concept only when the idea is in at least two catalogued sources, or the pipeline must name it (height, site index, volume, crown, stem)
- A model family, a software system, or a single-source measurement is not a concept
- An existing concept covers an idea only when its description is about that idea
- A mention, a tag, or an open question on a page is not coverage
- Stand site index, dominant height, stand basal area, and stand volume belong to concepts/site-index-and-yield.md
- Tree-level crown width, DBH, and stem volume are not that concept
- At most 3 proposals
- Empty proposals array when nothing clears the bar
- Do not write pages
"""


def _scalar(fm: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", fm, re.M)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def _pages(folder: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    directory = BUNDLE_ROOT / folder
    for path in sorted(directory.glob("*.md")):
        if path.name == "index.md":
            continue
        fm, _body = split_frontmatter(path.read_text(encoding="utf-8"))
        if fm is None:
            continue
        rel = path.relative_to(BUNDLE_ROOT).as_posix()
        title = _scalar(fm, "title") or path.stem
        description = _scalar(fm, "description")
        rows.append((rel, title, description))
    return rows


def _catalog() -> str:
    concepts = _pages("concepts")
    sources = _pages("sources")
    concept_lines = [
        f"- {rel}: {title} — {description}" for rel, title, description in concepts
    ]
    source_lines = [
        f"- {rel.removesuffix('.md')}: {title} — {description}"
        for rel, title, description in sources
    ]
    return (
        "Existing concepts:\n"
        + "\n".join(concept_lines)
        + "\n\nIngested sources:\n"
        + "\n".join(source_lines)
    )


def _parse_llm(raw: str) -> list[dict]:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    data = json.loads(text)
    proposals = data.get("proposals") or []
    if not isinstance(proposals, list):
        raise ValueError("proposals must be a list")
    cleaned: list[dict] = []
    for item in proposals:
        if not isinstance(item, dict) or not item.get("name"):
            continue
        sources = []
        for source in item.get("sources") or []:
            slug = str(source).strip().removeprefix("[[").removesuffix("]]")
            slug = slug.removesuffix(".md")
            if not slug.startswith("sources/"):
                slug = f"sources/{slug}"
            sources.append(slug)
        cleaned.append(
            {
                "decision": "pending",
                "name": str(item["name"]).strip(),
                "slug": str(item.get("slug") or "").strip(),
                "why": " ".join(str(item.get("why") or "").split()),
                "sources": sources,
            }
        )
    return cleaned


def _read_sheet() -> list[dict]:
    if not REVIEW_PATH.is_file():
        return []
    text = REVIEW_PATH.read_text(encoding="utf-8")
    rows: list[dict] = []
    for block in re.split(r"(?m)^## ", text)[1:]:
        lines = block.splitlines()
        header = lines[0].strip()
        fields = {
            "decision": "pending",
            "name": header,
            "slug": header,
            "why": "",
            "sources": [],
        }
        mode = ""
        for line in lines[1:]:
            if line.startswith("sources:"):
                mode = "sources"
                continue
            if mode == "sources" and line.startswith("- "):
                fields["sources"].append(line[2:].strip())
                continue
            mode = ""
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            if key in {"decision", "name", "slug", "why"}:
                fields[key] = value.strip()
        rows.append(fields)
    return rows


def _write_sheet(rows: list[dict]) -> None:
    stamp = iso_generated_at()
    body = [
        "---",
        "type: Project",
        'title: "Concept proposals"',
        'description: "Review sheet for proposed concept pages. Accept, reject, or correct them here."',
        "tags: [concepts, review]",
        "status: draft",
        f"updated: {date.today().isoformat()}",
        "generated:",
        "  by: agent:concept-gate",
        f"  at: {stamp}",
        "---",
        "",
        "# Concept proposals",
        "",
        "This sheet is the decision. The terminal list is only a copy.",
        "",
        "Set `decision` to `accept` or `reject`. To correct a proposal, edit `name`, `slug`, and `why`, then set `decision` to `accept`. Leave `pending` while you are still reading.",
        "",
        "Then run `make concept-gate APPLY=1`. That writes a concept page for each `accept`. It does not open an experiment folder.",
        "",
        "```mermaid",
        "flowchart LR",
        '  run["make concept-gate"] --> sheet["This sheet"]',
        '  sheet --> accept["decision: accept"]',
        '  sheet --> reject["decision: reject"]',
        '  accept --> page["Concept page"]',
        "```",
        "",
    ]
    if not rows:
        body.append("No proposals in this batch.")
        body.append("")
    for row in rows:
        slug = row.get("slug") or "proposal"
        body.append(f"## {slug}")
        body.append("")
        body.append(f"decision: {row.get('decision') or 'pending'}")
        body.append(f"name: {row.get('name') or ''}")
        body.append(f"slug: {slug}")
        body.append(f"why: {row.get('why') or ''}")
        body.append("sources:")
        for source in row.get("sources") or []:
            body.append(f"- {source}")
        body.append("")
    REVIEW_PATH.write_text("\n".join(body), encoding="utf-8")


def _merge(existing: list[dict], fresh: list[dict]) -> list[dict]:
    by_slug = {row.get("slug"): row for row in existing if row.get("slug")}
    merged: list[dict] = []
    seen: set[str] = set()
    for row in fresh:
        slug = row.get("slug") or ""
        seen.add(slug)
        previous = by_slug.get(slug)
        if previous and previous.get("decision") not in {"", "pending"}:
            merged.append(previous)
            continue
        merged.append(row)
    for row in existing:
        slug = row.get("slug") or ""
        if slug in seen:
            continue
        if row.get("decision") in {"accept", "reject", "accepted"}:
            merged.append(row)
    return merged


def _print_rows(rows: list[dict]) -> None:
    pending = [row for row in rows if row.get("decision") == "pending"]
    if not pending:
        print("No new concept proposals.")
    for row in pending:
        print(f"Concept proposal (not created): {row.get('name')} — {row.get('why')}")
        print(f"  slug: {row.get('slug')}")
        print(f"  sources: {', '.join(row.get('sources') or [])}")
    print(f"Review: {REVIEW_PATH.relative_to(BUNDLE_ROOT.parent)}")
    print("Set decision to accept or reject, or edit name / slug / why.")
    print("Then: make concept-gate APPLY=1")


def propose() -> None:
    client = get_llm_client()
    response = client.complete(
        [
            ChatMessage("system", SYSTEM),
            ChatMessage("user", _catalog() + "\n\nPropose concepts. Do not write pages."),
        ],
        temperature=0.2,
        max_tokens=2048,
    )
    try:
        fresh = _parse_llm(response.text or "")
    except (json.JSONDecodeError, ValueError) as exc:
        preview = (response.text or "")[:500].replace("\n", "\\n")
        raise SystemExit(f"Concept gate JSON parse failed: {exc}\nRaw: {preview}") from exc
    print(f"model: {response.model or 'unknown'}")
    rows = _merge(_read_sheet(), fresh)
    _write_sheet(rows)
    _print_rows(rows)


def _source_blurb(source_id: str) -> tuple[str, str]:
    path = BUNDLE_ROOT / f"{source_id}.md"
    if not path.is_file():
        raise SystemExit(f"Source page not found: {source_id}")
    fm, _body = split_frontmatter(path.read_text(encoding="utf-8"))
    title = _scalar(fm or "", "title") or path.stem
    description = _scalar(fm or "", "description")
    return title, description


def _insert_bullet(path, marker: str, bullet: str, needle: str) -> None:
    text = path.read_text(encoding="utf-8")
    if needle in text:
        return
    if marker not in text:
        raise SystemExit(f"Missing section in {path.name}: {marker!r}")
    path.write_text(text.replace(marker, marker + bullet, 1), encoding="utf-8")


def _prepend_log(name: str, slug: str) -> None:
    path = BUNDLE_ROOT / "log.md"
    text = path.read_text(encoding="utf-8")
    entry = (
        f"## [{date.today().isoformat()}] query | Concept accepted: {name}\n\n"
        f"- Added [[concepts/{slug}]] from [[project/concept-proposals]]\n\n"
    )
    match = re.search(r"^## \[", text, re.M)
    if match:
        text = text[: match.start()] + entry + text[match.start() :]
    else:
        text = text.rstrip() + "\n\n" + entry
    path.write_text(text, encoding="utf-8")


def _write_concept(row: dict) -> None:
    slug = row["slug"]
    if not SLUG_RE.match(slug):
        raise SystemExit(f"Slug must be kebab-case: {slug!r}")
    path = BUNDLE_ROOT / "concepts" / f"{slug}.md"
    if path.is_file():
        print(f"Already exists: concepts/{slug}.md")
        return
    source_ids = row.get("sources") or []
    if len(source_ids) < 2:
        raise SystemExit(f"{slug}: need at least two sources before accept")
    blurbs = [(source_id, *_source_blurb(source_id)) for source_id in source_ids]
    source_yaml = "\n".join(f"  - {source_id}" for source_id, _title, _desc in blurbs)
    source_lines = "\n".join(
        f"- [[{source_id}]] — {description}" if description else f"- [[{source_id}]] — {title}"
        for source_id, title, description in blurbs
    )
    stamp = datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    why = row.get("why") or row["name"]
    tags = ", ".join(part for part in slug.split("-") if part)
    if "allometr" in slug or "crown" in slug:
        diagram = """```mermaid
flowchart LR
  crown["Crown width"] --> stem["Stem volume"]
  dbh["DBH"] --> stem
  height["Tree height"] --> stem
```"""
    else:
        diagram = """```mermaid
flowchart LR
  sources["Source pages"] --> concept["This concept"]
```"""
    page = f"""---
title: {json.dumps(row['name'])}
type: Concept
description: {json.dumps(why)}
tags: [{tags}]
status: stable
updated: {date.today().isoformat()}
generated:
  by: agent:concept-gate
  at: {stamp}
sources:
{source_yaml}
---

# {row['name']}

{why}

This page names the shared idea. It does not open an experiment folder. [[project/domains]] does not gain a new program from this page.

{diagram}

## What the sources describe

{source_lines}

Stand dominant height, site index, and stand volume stay on [[concepts/site-index-and-yield]].

## Replication notes

Coefficients stay on the source pages. Nothing here is implemented in the detection pipeline.

| Paper | Our status |
|---|---|
"""
    for source_id, title, _description in blurbs:
        page += f"| [[{source_id}]] — {title} | TBD |\n"
    page += """
## Related

- [[concepts/site-index-and-yield]] — stand site index and stand volume
- [[concepts/crown-ownership]] — a crown box is not yet a measured crown width
- [[concepts/canopy-height-model]] — tree height read from the canopy surface
- [[project/domains]] — allometry program not started
"""
    path.write_text(page, encoding="utf-8")
    print(f"Wrote concepts/{slug}.md")


def _link_indexes(row: dict) -> None:
    slug = row["slug"]
    blurb = row.get("why") or row["name"]
    _insert_bullet(
        BUNDLE_ROOT / "concepts" / "index.md",
        "* [Site index and stand yield](/concepts/site-index-and-yield.md) — dominant height at a reference age, then stand volume; tree-level allometry stays on the source pages\n",
        f"* [{row['name']}](/concepts/{slug}.md) — {blurb}\n",
        f"/concepts/{slug}.md",
    )
    _insert_bullet(
        BUNDLE_ROOT / "index.md",
        "- [[concepts/site-index-and-yield]] — dominant height, site index, and stand volume; not a started allometry program\n",
        f"- [[concepts/{slug}]] — {blurb}\n",
        f"[[concepts/{slug}]]",
    )


def _retarget_stand_page(slug: str) -> None:
    path = BUNDLE_ROOT / "concepts" / "site-index-and-yield.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    old = (
        "It is the only ingested source for that measurement, so it stays on the source page. "
        "A second source, or a started allometry program, would be the reason to give tree-level allometry its own concept."
    )
    new = (
        f"Tree-level crown width, DBH, height, and stem volume are [[concepts/{slug}]]. "
        "This page stays with stand site index and stand volume."
    )
    if old in text:
        text = text.replace(old, new, 1)
    needle = f"[[concepts/{slug}]]"
    if needle not in text.split("## Related", 1)[-1]:
        text = text.replace(
            "- [[project/domains]] — allometry program not started\n",
            f"- [[concepts/{slug}]] — tree-level crown, DBH, and stem\n- [[project/domains]] — allometry program not started\n",
            1,
        )
    path.write_text(text, encoding="utf-8")
    domains = BUNDLE_ROOT / "project" / "domains.md"
    domain_text = domains.read_text(encoding="utf-8")
    cell = "none yet; shared concept [[concepts/site-index-and-yield]]"
    if cell in domain_text and f"concepts/{slug}" not in domain_text:
        domains.write_text(
            domain_text.replace(
                cell,
                cell + f" and [[concepts/{slug}]]",
                1,
            ),
            encoding="utf-8",
        )


def apply_accepted() -> None:
    if not REVIEW_PATH.is_file():
        raise SystemExit("No review sheet. Run make concept-gate first.")
    rows = _read_sheet()
    accepted = [row for row in rows if row.get("decision") == "accept"]
    if not accepted:
        print("No proposal has decision: accept.")
        print(f"Edit {REVIEW_PATH.relative_to(BUNDLE_ROOT.parent)}")
        return
    for row in accepted:
        _write_concept(row)
        _link_indexes(row)
        if "allometr" in row["slug"]:
            _retarget_stand_page(row["slug"])
        _prepend_log(row["name"], row["slug"])
        row["decision"] = "accepted"
        print(f"Accepted: {row['slug']}")
    _write_sheet(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Propose or apply concept pages.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write concept pages whose decision is accept. Does not call the LLM.",
    )
    args = parser.parse_args()
    if args.apply:
        apply_accepted()
        return
    propose()


if __name__ == "__main__":
    main()
