"""Shared OKF v0.2 helpers for the conifervision knowledge bundle."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

OKF_VERSION = "0.2"
BUNDLE_ROOT = Path(__file__).resolve().parents[1] / "conifervision"
RESERVED_FILENAMES = frozenset({"index.md", "log.md"})
STATUS_LEGACY_MAP = {
    "active": "stable",
    "superseded": "deprecated",
    "candidate": "draft",
}
VALID_OKF_STATUS = frozenset({"draft", "stable", "deprecated"})
TYPE_LEGACY_MAP = {
    "method": "Method",
    "concept": "Concept",
    "source": "Source",
    "project": "Project",
    "experiment": "Experiment",
}


def concept_id(path: Path, bundle: Path = BUNDLE_ROOT) -> str:
    rel = path.relative_to(bundle).as_posix()
    if rel.endswith(".md"):
        rel = rel[:-3]
    return rel


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def join_frontmatter(fm: str, body: str) -> str:
    return f"---\n{fm.rstrip()}\n---\n{body.lstrip()}"


def is_concept_file(path: Path) -> bool:
    return path.suffix == ".md" and path.name not in RESERVED_FILENAMES


def iter_concept_files(bundle: Path = BUNDLE_ROOT) -> list[Path]:
    skip = {".templates", ".obsidian"}
    files: list[Path] = []
    for path in sorted(bundle.rglob("*.md")):
        if any(part in skip for part in path.parts):
            continue
        if path.name == "Welcome.md":
            continue
        if is_concept_file(path):
            files.append(path)
    return files


def parse_simple_yaml_block(block: str) -> dict[str, str]:
    """Parse flat key: value and simple list lines from frontmatter."""
    data: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def iso_generated_at(date_str: str | None = None) -> str:
    if date_str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return f"{date_str}T12:00:00Z"
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def first_description(body: str, max_len: int = 200) -> str | None:
    lines = body.splitlines()
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            continue
        text = line.strip()
        if not text or text.startswith("|") or text.startswith("-"):
            continue
        text = re.sub(r"\[\[([^|\]]+)(?:\|[^\]]+)?\]\]", r"\1", text)
        text = re.sub(r"\*\*|__|`", "", text)
        if len(text) > max_len:
            text = text[: max_len - 1].rstrip() + "…"
        return text
    return None
