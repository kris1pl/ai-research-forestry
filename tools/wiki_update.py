"""Apply ingest side-effects to conifervision/ (log, index, methods, concepts)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from tools.llm import ChatMessage, get_llm_client
from tools.okf_common import iso_generated_at

REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT = REPO_ROOT / "conifervision"

WIKI_UPDATE_SYSTEM = """\
You maintain the Conifervision Research Wiki after a new literature source page is ingested.
Return ONLY valid JSON (no markdown fences) with this schema:

{
  "log_title": "Short Author (year) — topic for log header",
  "index_blurb": "one-line description for index (no wikilink, plain text after em dash style)",
  "pages": [
    {
      "path": "methods/example.md",
      "literature_paragraph": "[[sources/slug]] — one paragraph for ## Literature",
      "replication_rows": [["Paper step label", "Our status (TBD / aligned / not used / ...)"]],
      "open_question": "optional bullet for ## Open questions from literature or null"
    }
  ]
}

Rules:
- English only
- Include only pages that are clearly relevant (typically 1–5)
- path must be relative to conifervision/ (e.g. methods/dinov3-classification.md)
- Do not duplicate wikilinks already present in provided page excerpts
- replication_rows: short table rows only when the paper has a procedural step for that method
"""


@dataclass
class WikiUpdateResult:
    touched: list[str] = field(default_factory=list)


def _today() -> str:
    return date.today().isoformat()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def _join_frontmatter(fm: str, body: str) -> str:
    return f"---\n{fm}\n---\n{body.lstrip()}"


def _bump_updated(text: str, today: str | None = None) -> str:
    today = today or _today()
    fm, body = _split_frontmatter(text)
    if fm is None:
        return text
    if re.search(r"^updated:\s*", fm, re.M):
        fm = re.sub(r"^updated:\s*.*$", f"updated: {today}", fm, count=1, flags=re.M)
    else:
        fm = fm.rstrip() + f"\nupdated: {today}"
    # Use \g<1> — plain \1 before a digit is parsed as octal (e.g. \12026 → "P26…")
    if re.search(r"^generated:\s*$", fm, re.M):
        fm = re.sub(
            r"(^generated:\s*\n(?:  .+\n)*?  at:\s*).+$",
            rf"\g<1>{iso_generated_at(today)}",
            fm,
            count=1,
            flags=re.M,
        )
    elif "generated:" not in fm:
        fm = fm.rstrip() + (
            f"\ngenerated:\n  by: agent:conifervision-wiki\n  at: {iso_generated_at(today)}"
        )
    return _join_frontmatter(fm, body)


def _source_link(slug: str) -> str:
    return f"[[sources/{slug}]]"


def _has_link(text: str, slug: str) -> bool:
    return f"sources/{slug}" in text or f"[[sources/{slug}]]" in text


def _add_source_to_frontmatter(text: str, slug: str, today: str | None = None) -> str:
    today = today or _today()
    fm, body = _split_frontmatter(text)
    if fm is None:
        return text
    source_entry = f"  - sources/{slug}"
    if f"sources/{slug}" in fm:
        pass
    elif re.search(r"^sources:\s*\n", fm, re.M):
        fm = re.sub(
            r"(^sources:\s*\n(?:  - .+\n)*)",
            lambda m: m.group(1) + f"{source_entry}\n",
            fm,
            count=1,
            flags=re.M,
        )
    else:
        fm = fm.rstrip() + f"\nsources:\n{source_entry}"
    fm = re.sub(r"^updated:\s*.*$", f"updated: {today}", fm, count=1, flags=re.M)
    return _join_frontmatter(fm, body)


def _append_literature(body: str, paragraph: str, slug: str) -> str:
    if _has_link(body, slug):
        return body
    for heading in ("## Literature\n", "## Literature baseline\n"):
        match = re.search(rf"({re.escape(heading)})(.*?)(?=\n## |\Z)", body, re.S)
        if match:
            block = match.group(2).rstrip()
            new_block = f"{block}\n\n{paragraph}" if block else f"\n{paragraph}"
            return body[: match.start(2)] + new_block + body[match.end(2) :]
    return body.rstrip() + f"\n\n## Literature\n\n{paragraph}\n"


def _append_replication_rows(body: str, rows: list[list[str]], slug: str) -> str:
    if not rows:
        return body
    match = re.search(
        r"(## Replication notes\n.*?)(\|[^\n]+\|\n\|[-| ]+\|\n)((?:\|[^\n]+\|\n)*)",
        body,
        re.S,
    )
    if not match:
        return body
    existing = match.group(3)
    additions = ""
    for label, status in rows:
        if label in existing:
            continue
        additions += f"| {label} | {status} |\n"
    if not additions:
        return body
    pseudocode_note = (
        f"\n\nPseudocode: [[sources/{slug}#Replication pseudocode]]."
        if f"sources/{slug}#Replication" not in body
        else ""
    )
    insert_at = match.end(3)
    return body[:insert_at] + additions + pseudocode_note + body[insert_at:]


def _append_open_question(body: str, question: str | None, slug: str) -> str:
    if not question or question in body:
        return body
    match = re.search(r"(## Open questions from literature\n)(.*?)(?=\n## |\Z)", body, re.S)
    bullet = f"- {question}"
    if match:
        block = match.group(2).rstrip()
        new_block = f"{block}\n{bullet}" if block else f"\n{bullet}"
        return body[: match.start(2)] + new_block + body[match.end(2) :]
    return body.rstrip() + f"\n\n## Open questions from literature\n\n{bullet}\n"


def _log_already_has_ingest(text: str, slug: str) -> bool:
    return f"- Added [[sources/{slug}]]" in text


def prepend_log_entry(
    slug: str,
    log_title: str,
    pdf_rel: str,
    model: str,
    touched: list[str],
    *,
    today: str | None = None,
) -> bool:
    """Prepend log entry if not already present. Returns True if modified."""
    today = today or _today()
    path = VAULT / "log.md"
    text = _read(path)
    if _log_already_has_ingest(text, slug):
        return False

    touched_links = ", ".join(f"[[{p.removesuffix('.md')}]]" for p in touched[:8])
    entry = (
        f"## [{today}] ingest | {log_title}\n\n"
        f"- Source: `{pdf_rel}` (LLM: `{model}` via `make ingest-paper`)\n"
        f"- Added {_source_link(slug)}\n"
        f"- Updated {touched_links}\n\n"
    )
    # Insert before the first dated section (stable if the intro blurb changes).
    match = re.search(r"^## \[", text, re.M)
    if match:
        text = text[: match.start()] + entry + text[match.start() :]
    else:
        text = text.rstrip() + "\n\n" + entry
    # log.md has no YAML frontmatter (OKF) — do not call _bump_updated here.
    _write(path, text)
    return True


def append_index_source(slug: str, blurb: str, *, today: str | None = None) -> bool:
    """Add source line under Literature sources. Returns True if modified."""
    today = today or _today()
    path = VAULT / "index.md"
    text = _read(path)
    if _has_link(text, slug):
        return False
    line = f"- {_source_link(slug)} — {blurb}\n"
    marker = "## Literature sources\n\n"
    if marker not in text:
        raise ValueError("index.md missing ## Literature sources section")
    text = _bump_updated(text.replace(marker, marker + line, 1), today)
    _write(path, text)
    return True


def _list_candidate_pages() -> list[Path]:
    paths: list[Path] = []
    for sub in ("methods", "concepts", "project"):
        d = VAULT / sub
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            if p.name.startswith("_"):
                continue
            paths.append(p)
    return paths


def _page_excerpt(path: Path, limit: int = 2500) -> str:
    return f"--- {path.relative_to(VAULT)} ---\n{_read(path)[:limit]}"


def plan_wiki_updates(
    source_slug: str,
    source_markdown: str,
    *,
    max_pages: int = 12,
) -> dict:
    """Ask LLM which wiki pages to update and what to append."""
    candidates = _list_candidate_pages()[:max_pages]
    catalog = "\n\n".join(_page_excerpt(p) for p in candidates)
    user = f"""\
New source page (slug: {source_slug}):

{source_markdown[:12000]}

Existing wiki pages (excerpts):
{catalog}

Produce JSON updates for relevant pages only.
"""
    client = get_llm_client()
    response = client.complete(
        [ChatMessage("system", WIKI_UPDATE_SYSTEM), ChatMessage("user", user)],
        temperature=0.2,
        max_tokens=4096,
    )
    raw = (response.text or "").strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Wiki update JSON parse failed: {exc}\nRaw: {raw[:500]}") from exc
    data["_model"] = response.model
    return data


def apply_page_update(page_rel: str, update: dict, source_slug: str) -> bool:
    """Apply one page update from plan. Returns True if file changed."""
    path = VAULT / page_rel
    if not path.is_file():
        return False
    text = _read(path)
    original = text
    if update.get("add_to_sources_frontmatter", True):
        text = _add_source_to_frontmatter(text, source_slug)
    para = update.get("literature_paragraph", "")
    if para:
        text = _append_literature(text, para.strip(), source_slug)
    rows = update.get("replication_rows") or []
    text = _append_replication_rows(text, rows, source_slug)
    text = _append_open_question(text, update.get("open_question"), source_slug)
    text = _bump_updated(text)
    if text != original:
        _write(path, text)
        return True
    return False


def apply_wiki_updates(
    source_slug: str,
    source_markdown: str,
    pdf_rel: str,
    *,
    plan: dict | None = None,
) -> WikiUpdateResult:
    """Run full wiki maintenance after source page is written."""
    result = WikiUpdateResult()
    plan = plan or plan_wiki_updates(source_slug, source_markdown)
    model = plan.get("_model", "unknown")

    log_title = plan.get("log_title") or source_slug
    index_blurb = plan.get("index_blurb") or log_title

    for page in plan.get("pages") or []:
        rel = page.get("path", "").lstrip("/")
        if not rel.endswith(".md"):
            rel = f"{rel}.md" if rel else ""
        if rel and apply_page_update(rel, page, source_slug):
            result.touched.append(rel)

    if append_index_source(source_slug, index_blurb):
        result.touched.append("index.md")

    touched_for_log = list(dict.fromkeys(["index.md"] + result.touched))
    if prepend_log_entry(source_slug, log_title, pdf_rel, model, touched_for_log):
        result.touched.append("log.md")

    # methods/index.md — bump updated on method pages when methods were touched
    method_hits = [p for p in result.touched if p.startswith("methods/") and p not in {"methods/index.md"}]
    if method_hits:
        idx_path = VAULT / "methods" / "index.md"
        if idx_path.is_file():
            _write(idx_path, _bump_updated(_read(idx_path)))
            result.touched.append("methods/index.md")

    return result
