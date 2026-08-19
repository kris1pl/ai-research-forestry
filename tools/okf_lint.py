#!/usr/bin/env python3
"""Lint (and optionally fix) OKF v0.2 conformance for conifervision/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from tools.okf_common import (
    BUNDLE_ROOT,
    OKF_VERSION,
    RESERVED_FILENAMES,
    STATUS_LEGACY_MAP,
    TYPE_LEGACY_MAP,
    VALID_OKF_STATUS,
    concept_id,
    first_description,
    iso_generated_at,
    is_concept_file,
    iter_concept_files,
    join_frontmatter,
    split_frontmatter,
)

Issue = tuple[str, str, str]  # level, path, message


def _lint_root_index(path: Path, fm: str | None) -> list[Issue]:
    issues: list[Issue] = []
    rel = str(path.relative_to(BUNDLE_ROOT))
    if fm is None:
        issues.append(("warn", rel, "root index.md should declare okf_version in frontmatter"))
        return issues
    if "okf_version:" not in fm:
        issues.append(("warn", rel, f"missing okf_version (expected {OKF_VERSION!r})"))
    elif f'okf_version: "{OKF_VERSION}"' not in fm and f"okf_version: '{OKF_VERSION}'" not in fm:
        issues.append(("warn", rel, "okf_version should be 0.2"))
    for key in ("type:", "status:", "title:"):
        if key in fm and "okf_version" in fm:
            issues.append(
                ("warn", rel, f"OKF root index should only carry okf_version, not concept field {key[:-1]}"),
            )
            break
    return issues


def _lint_log(path: Path, fm: str | None) -> list[Issue]:
    rel = str(path.relative_to(BUNDLE_ROOT))
    if fm is not None:
        return [("warn", rel, "log.md should have no YAML frontmatter per OKF §9")]
    return []


def _lint_subdirectory_index(path: Path, fm: str | None) -> list[Issue]:
    rel = str(path.relative_to(BUNDLE_ROOT))
    if fm is not None:
        return [("warn", rel, "directory index.md should have no frontmatter (OKF §8)")]
    if not path.read_text(encoding="utf-8").strip():
        return [("error", rel, "empty index.md")]
    return []


def _lint_concept(path: Path, fm: str | None, body: str) -> list[Issue]:
    rel = str(path.relative_to(BUNDLE_ROOT))
    issues: list[Issue] = []
    if fm is None:
        return [("error", rel, "concept missing YAML frontmatter")]
    if not re.search(r"^type:\s*\S", fm, re.M):
        issues.append(("error", rel, "missing required OKF field: type"))
    if "description:" not in fm:
        issues.append(("warn", rel, "missing recommended field: description"))
    status_match = re.search(r"^status:\s*(\S+)", fm, re.M)
    if status_match:
        status = status_match.group(1)
        if status in STATUS_LEGACY_MAP:
            issues.append(("warn", rel, f"legacy status {status!r} — use OKF {STATUS_LEGACY_MAP[status]!r}"))
        elif status not in VALID_OKF_STATUS:
            issues.append(("warn", rel, f"non-standard status {status!r}"))
    if "generated:" not in fm:
        issues.append(("warn", rel, "missing generated (OKF provenance/trust)"))
    return issues


def lint_bundle(bundle: Path = BUNDLE_ROOT) -> list[Issue]:
    issues: list[Issue] = []
    index_dirs: set[str] = set()

    for path in sorted(bundle.rglob("*.md")):
        if ".templates" in path.parts or ".obsidian" in path.parts:
            continue
        if path.name == "Welcome.md":
            continue

        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        rel = path.relative_to(bundle)

        if path.name in RESERVED_FILENAMES:
            if rel.as_posix() == "index.md":
                issues.extend(_lint_root_index(path, fm))
            elif rel.as_posix() == "log.md":
                issues.extend(_lint_log(path, fm))
            else:
                issues.extend(_lint_subdirectory_index(path, fm))
            parent = rel.parent.as_posix()
            if parent != ".":
                index_dirs.add(parent)
            continue

        if is_concept_file(path):
            issues.extend(_lint_concept(path, fm, body))
            parent = rel.parent.as_posix()
            if parent != ".":
                index_dirs.add(parent)

    for directory in sorted(index_dirs):
        index_path = bundle / directory / "index.md"
        if not index_path.is_file():
            issues.append(("warn", directory, "missing index.md for progressive disclosure (OKF §8)"))

    return issues


def _fix_type(fm: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(1)
        mapped = TYPE_LEGACY_MAP.get(raw.lower(), raw)
        return f"type: {mapped}"

    return re.sub(r"^type:\s*(\S+)\s*$", repl, fm, count=1, flags=re.M)


def _fix_status(fm: str) -> str:
    def repl(match: re.Match[str]) -> str:
        legacy = match.group(1)
        mapped = STATUS_LEGACY_MAP.get(legacy, legacy)
        return f"status: {mapped}"

    return re.sub(r"^status:\s*(\S+)\s*$", repl, fm, count=1, flags=re.M)


def _fix_generated(fm: str) -> str:
    if "generated:" in fm:
        return fm
    updated = re.search(r"^updated:\s*(\S+)", fm, re.M)
    at = iso_generated_at(updated.group(1) if updated else None)
    block = f'generated:\n  by: agent:conifervision-wiki\n  at: {at}'
    if updated:
        return fm.replace(updated.group(0), f"{updated.group(0)}\n{block}", 1)
    return fm.rstrip() + f"\n{block}"


def _fix_description(fm: str, body: str) -> str:
    if "description:" in fm:
        return fm
    desc = first_description(body)
    if not desc:
        return fm
    escaped = desc.replace('"', '\\"')
    type_line = re.search(r"^type:.*$", fm, re.M)
    if type_line:
        insert_at = type_line.end()
        return fm[:insert_at] + f'\ndescription: "{escaped}"' + fm[insert_at:]
    return f'description: "{escaped}"\n' + fm


def fix_concept(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    if fm is None:
        return False
    original = fm
    fm = _fix_type(fm)
    fm = _fix_status(fm)
    fm = _fix_generated(fm)
    fm = _fix_description(fm, body)
    if fm == original:
        return False
    path.write_text(join_frontmatter(fm, body), encoding="utf-8")
    return True


def fix_root_index(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    new_fm = f'okf_version: "{OKF_VERSION}"'
    if fm == new_fm:
        return False
    path.write_text(join_frontmatter(new_fm, body), encoding="utf-8")
    return True


def fix_log(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    if fm is None:
        return False
    path.write_text(body.lstrip(), encoding="utf-8")
    return True


def fix_bundle(bundle: Path = BUNDLE_ROOT) -> list[str]:
    changed: list[str] = []

    root_index = bundle / "index.md"
    if root_index.is_file() and fix_root_index(root_index):
        changed.append("index.md")

    log_path = bundle / "log.md"
    if log_path.is_file() and fix_log(log_path):
        changed.append("log.md")

    for path in iter_concept_files(bundle):
        if fix_concept(path):
            changed.append(path.relative_to(bundle).as_posix())

    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint OKF v0.2 bundle at conifervision/")
    parser.add_argument("--fix", action="store_true", help="Apply safe automatic fixes")
    args = parser.parse_args()

    if args.fix:
        changed = fix_bundle()
        for rel in changed:
            print(f"fixed: {rel}")

    issues = lint_bundle()
    errors = [i for i in issues if i[0] == "error"]
    warns = [i for i in issues if i[0] == "warn"]

    for level, rel, msg in issues:
        print(f"{level}: {rel}: {msg}")

    print(f"\n{len(errors)} error(s), {len(warns)} warning(s)")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
