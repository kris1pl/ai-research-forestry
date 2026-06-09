#!/usr/bin/env python3
"""Ingest a paper PDF into the wiki using the configured LLM (default: Vertex Gemini)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from tools.llm import ChatMessage, get_llm_client
from tools.wiki_update import apply_wiki_updates

REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT = REPO_ROOT / "conifervision"
TEMPLATE = VAULT / ".templates" / "source.md"

SYSTEM_PROMPT = """\
You ingest research papers into the Conifervision Research Wiki (forest area analysis:
drone orthophoto, CHM, tree detection, DINOv3 species classification).

Output a single markdown file with YAML frontmatter. Rules:
- Language: English
- type: source, status: active
- Include: title, tags, updated (today's date YYYY-MM-DD), source_file, authors, year
- Optional: replication_status, related_methods (list of methods/... paths)
- Sections: Summary, Key claims, Implications for our pipeline, Replication pseudocode
  (Prerequisites, Procedure in a ```text block, Gaps), Quotes, Related pages
- Wikilinks: [[methods/...]], [[concepts/...]], [[project/pipeline-overview]]
- Be factual; cite page numbers when quoting; use TBD for unspecified thresholds
- Slug suggestion on first line as HTML comment: <!-- slug: author-year-short-topic -->
- Do not invent metrics not in the paper
"""


def _extract_text(pdf_path: Path) -> Path:
    txt_path = pdf_path.with_suffix(".txt")
    if not txt_path.is_file() or txt_path.stat().st_mtime < pdf_path.stat().st_mtime:
        subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "extract_pdf_text.py"), str(pdf_path)],
            check=True,
        )
    return txt_path


def _wiki_context() -> str:
    paths = [
        REPO_ROOT / "AGENTS.md",
        VAULT / "index.md",
        VAULT / "project" / "pipeline-overview.md",
    ]
    parts: list[str] = []
    for path in paths:
        if path.is_file():
            parts.append(
                f"--- {path.relative_to(REPO_ROOT)} ---\n{path.read_text(encoding='utf-8')[:4000]}"
            )
    return "\n\n".join(parts)


def _parse_slug(markdown: str, pdf_path: Path) -> str:
    match = re.search(r"<!--\s*slug:\s*([a-z0-9-]+)\s*-->", markdown, re.I)
    if match:
        return match.group(1).lower()
    stem = pdf_path.stem.lower().replace(".", "-")
    return f"paper-{stem}"


def _normalize_markdown(markdown: str, pdf_path: Path) -> str:
    """Strip slug comment; fix source_file path if LLM hallucinated it."""
    text = markdown.strip()
    text = re.sub(r"^<!--\s*slug:\s*[a-z0-9-]+\s*-->\s*\n?", "", text, flags=re.I)
    rel_pdf = pdf_path.relative_to(REPO_ROOT).as_posix()
    text = re.sub(
        r"^(source_file:\s*).*$",
        rf"\1{rel_pdf}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return text


def _generate_source_markdown(pdf_path: Path, paper_text: str, max_chars: int) -> tuple[str, str]:
    context = _wiki_context()
    template = TEMPLATE.read_text(encoding="utf-8") if TEMPLATE.is_file() else ""
    txt_path = pdf_path.with_suffix(".txt")

    user_prompt = f"""\
Wiki context (excerpt):
{context}

Source template:
{template}

Paper text (from {txt_path.relative_to(REPO_ROOT)}):
{paper_text[:max_chars]}

PDF path for source_file frontmatter: {pdf_path.relative_to(REPO_ROOT)}

Produce the complete source page markdown for this paper.
"""

    client = get_llm_client()
    response = client.complete(
        [ChatMessage("system", SYSTEM_PROMPT), ChatMessage("user", user_prompt)],
        temperature=0.2,
        max_tokens=8192,
    )
    markdown = _normalize_markdown(response.text, pdf_path)
    if not markdown.startswith("---"):
        preview = markdown[:200].replace("\n", "\\n")
        raise SystemExit(
            f"LLM response missing YAML frontmatter (expected --- at start). Got: {preview!r}"
        )
    return markdown, response.model or "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a paper PDF via LLM into conifervision/")
    parser.add_argument("pdf", type=Path, help="Path to PDF under raw/")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write source page and update wiki (log, index, methods)",
    )
    parser.add_argument(
        "--no-wiki",
        action="store_true",
        help="With --write: only write source page, skip wiki side-effects",
    )
    parser.add_argument(
        "--wiki-only",
        type=Path,
        metavar="SOURCE_MD",
        help="Skip LLM source generation; update wiki from existing source markdown",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=120_000,
        help="Max paper text chars sent to LLM (default: 120000)",
    )
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    if not pdf_path.is_file():
        raise SystemExit(f"PDF not found: {pdf_path}")

    pdf_rel = pdf_path.relative_to(REPO_ROOT).as_posix()

    if args.wiki_only:
        source_path = args.wiki_only.resolve()
        if not source_path.is_file():
            raise SystemExit(f"Source markdown not found: {source_path}")
        markdown = source_path.read_text(encoding="utf-8")
        slug = source_path.stem
        model = "wiki-only"
    else:
        txt_path = _extract_text(pdf_path)
        paper_text = txt_path.read_text(encoding="utf-8")
        markdown, model = _generate_source_markdown(pdf_path, paper_text, args.max_chars)
        slug = _parse_slug(markdown, pdf_path)

    out_path = VAULT / "sources" / f"{slug}.md"

    if not args.write:
        print(markdown)
        print(f"\n# slug: {slug} -> conifervision/sources/{slug}.md", file=sys.stderr)
        print(f"# model: {model}", file=sys.stderr)
        print("# dry-run: pass --write to save source + update wiki", file=sys.stderr)
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")

    if not args.no_wiki:
        wiki_result = apply_wiki_updates(slug, markdown, pdf_rel)
        for rel in sorted(set(wiki_result.touched)):
            print(f"Updated conifervision/{rel}")

    print(f"model: {model}")


if __name__ == "__main__":
    main()
