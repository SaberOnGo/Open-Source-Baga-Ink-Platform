#!/usr/bin/env python3
"""Validate repository README language switch consistency.

The language registry lives at:

    docs/localization/readme-languages.json

Every current README locale must exist and expose the same language switch set.
This keeps the repository home page scalable when additional translations are
added later.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "docs" / "localization" / "readme-languages.json"
LOCALE_RE = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")
ALLOWED_STATUS = {"current", "planned", "retired"}

errors: list[str] = []


def fail(label: str | Path, message: str) -> None:
    if isinstance(label, Path):
        try:
            label = label.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            label = label.as_posix()
    errors.append(f"{label}: {message}")


def load_registry() -> dict:
    if not REGISTRY.is_file():
        fail(REGISTRY, "README language registry is missing")
        return {}
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(REGISTRY, f"invalid UTF-8/JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        fail(REGISTRY, "registry root must be an object")
        return {}
    return data


def main() -> int:
    data = load_registry()
    languages = data.get("languages", [])
    rules = data.get("rules", {})
    default_locale = data.get("default_locale")

    if not isinstance(languages, list) or not languages:
        fail(REGISTRY, "languages must be a non-empty array")
        languages = []

    start_marker = rules.get("switch_start_marker")
    end_marker = rules.get("switch_end_marker")
    if not isinstance(start_marker, str) or not start_marker:
        fail(REGISTRY, "switch_start_marker must be a non-empty string")
    if not isinstance(end_marker, str) or not end_marker:
        fail(REGISTRY, "switch_end_marker must be a non-empty string")

    seen_locales: set[str] = set()
    seen_readmes: set[str] = set()
    current: list[dict] = []

    for i, entry in enumerate(languages):
        label = f"languages[{i}]"
        if not isinstance(entry, dict):
            fail(label, "entry must be an object")
            continue
        for key in ("locale", "label", "readme", "status"):
            if not isinstance(entry.get(key), str) or not entry[key]:
                fail(label, f"{key} must be a non-empty string")
        locale = entry.get("locale", "")
        readme = entry.get("readme", "")
        status = entry.get("status", "")

        if locale and not LOCALE_RE.fullmatch(locale):
            fail(label, f"invalid locale tag: {locale}")
        if locale in seen_locales:
            fail(label, f"duplicate locale: {locale}")
        seen_locales.add(locale)

        if readme in seen_readmes:
            fail(label, f"duplicate README path: {readme}")
        seen_readmes.add(readme)

        if status not in ALLOWED_STATUS:
            fail(label, f"invalid status: {status}")
        if status == "current":
            current.append(entry)

    if default_locale not in {entry.get("locale") for entry in current}:
        fail(REGISTRY, "default_locale must refer to a current language")

    default_entry = next((e for e in current if e.get("locale") == default_locale), None)
    if default_entry and default_entry.get("readme") != "README.md":
        fail(REGISTRY, "default locale README must be README.md")

    current_readmes = {entry["readme"] for entry in current if "readme" in entry}

    # Every current language README must exist and expose all current language
    # labels inside the managed switch block. Other locales must be clickable;
    # the active locale may be rendered as text/badge without a self-link.
    for entry in current:
        readme_path = REPO_ROOT / entry["readme"]
        if not readme_path.is_file():
            fail(readme_path, "current language README is missing")
            continue
        try:
            text = readme_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            fail(readme_path, f"README must be UTF-8: {exc}")
            continue

        if text.count(start_marker) != 1 or text.count(end_marker) != 1:
            fail(readme_path, "must contain exactly one managed language-switch marker pair")
            continue
        start = text.index(start_marker) + len(start_marker)
        end = text.index(end_marker)
        if start >= end:
            fail(readme_path, "language-switch markers are out of order")
            continue
        block = text[start:end]

        for language in current:
            if language["label"] not in block:
                fail(readme_path, f"language switch is missing label: {language['label']}")
            if language["locale"] != entry["locale"] and language["readme"] not in block:
                fail(readme_path, f"language switch is missing README target: {language['readme']}")

        if "Add a language" not in block and "增加一种语言" not in block:
            fail(readme_path, "language switch must include a translation contribution entry")

    # Prevent unregistered translated README files from appearing at repo root.
    for path in REPO_ROOT.glob("README.*.md"):
        if path.name not in current_readmes:
            fail(path, "translated README is not registered as a current language")

    if errors:
        print("README language switch check FAILED:\n", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("README language switch check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
