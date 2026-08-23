#!/usr/bin/env python3
"""Validate the final Baga Ink public-document localization contract.

Long-lived public prose exists only under:

    docs/en/
    docs/zh-CN/

The historical mixed-language public trees are no longer a migration surface;
they are forbidden. The localization catalog is the stable mapping between one
logical document identity and its maintained locale editions.

This validator intentionally uses only the Python standard library so it can
run locally and in GitHub Actions without bootstrap dependencies.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
CATALOG = DOCS / "localization" / "catalog.json"
TERMINOLOGY = DOCS / "localization" / "terminology.json"
LEGACY_LOCK = DOCS / "localization" / "legacy-lock.json"

PUBLIC_CATEGORIES = {"standards", "design", "reference-apps", "governance", "status"}
ALLOWED_STATUS = {"current", "translation-pending", "stale", "superseded"}
EN_NAME_RE = re.compile(r"^(?P<number>\d{2})_(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
ZH_NAME_RE = re.compile(r"^(?P<number>\d{2})_(?P<name>[^_]+)\.md$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

LEGACY_PATHS = [
    DOCS / "standards",
    DOCS / "design",
    DOCS / "reference-apps",
    DOCS / "governance",
    DOCS / "status",
    DOCS / "00_项目文档入口_Baga-Ink-Documentation-Index.md",
]

errors: list[str] = []


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def fail(path: Path | str, message: str) -> None:
    errors.append(f"{rel(path) if isinstance(path, Path) else path}: {message}")


def load_json(path: Path, label: str) -> dict:
    if not path.is_file():
        fail(path, f"{label} is missing")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(path, f"invalid UTF-8/JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(path, f"{label} root must be an object")
        return {}
    return value


def validate_en_filename(path: Path, expected_number: str | None = None) -> None:
    match = EN_NAME_RE.fullmatch(path.name)
    if not match:
        fail(path, "English public doc must match NN_lowercase-kebab-case-name.md")
        return
    if expected_number is not None and match.group("number") != expected_number:
        fail(path, f"filename number must be {expected_number}")
    if CJK_RE.search(path.name):
        fail(path, "English public filename must not contain CJK characters")


def validate_zh_filename(path: Path, expected_number: str | None = None) -> None:
    match = ZH_NAME_RE.fullmatch(path.name)
    if not match:
        fail(path, "zh-CN public doc must match NN_中文名称.md without an English suffix")
        return
    if expected_number is not None and match.group("number") != expected_number:
        fail(path, f"filename number must be {expected_number}")
    if not CJK_RE.search(match.group("name")):
        fail(path, "zh-CN public filename must contain Chinese descriptive text")


def validate_no_legacy_paths() -> None:
    for path in LEGACY_PATHS:
        if path.exists():
            fail(path, "legacy mixed-language public path is forbidden; use docs/en or docs/zh-CN")
    if LEGACY_LOCK.exists():
        fail(LEGACY_LOCK, "legacy-lock.json must not exist after migration completion")


def walk_locale(locale: str) -> set[str]:
    root = DOCS / locale
    found: set[str] = set()
    if not root.is_dir():
        fail(root, "locale root is missing")
        return found

    expected_index = "00_baga-ink-documentation-index.md" if locale == "en" else "00_项目文档入口.md"

    for entry in root.iterdir():
        if entry.is_file():
            if entry.name != expected_index:
                fail(entry, "unexpected file at locale root")
                continue
            (validate_en_filename if locale == "en" else validate_zh_filename)(entry)
            found.add(rel(entry))
            continue

        if not entry.is_dir():
            fail(entry, "unsupported filesystem entry")
            continue

        if entry.name not in PUBLIC_CATEGORIES:
            fail(entry, f"unexpected public category; allowed: {sorted(PUBLIC_CATEGORIES)}")
            continue

        for item in entry.iterdir():
            if item.is_dir():
                fail(item, "localized public categories are flat; add governance before nesting")
                continue
            if item.suffix != ".md":
                fail(item, "only Markdown prose files are allowed in localized public categories")
                continue
            (validate_en_filename if locale == "en" else validate_zh_filename)(item)
            found.add(rel(item))

    return found


def validate_target_path(path_text: str, locale: str, category: str, number: str) -> None:
    parts = Path(path_text).parts
    path = REPO_ROOT / path_text

    if category == "index":
        if len(parts) != 3 or parts[:2] != ("docs", locale):
            fail(path_text, f"index must live directly under docs/{locale}/")
    else:
        if len(parts) != 4 or parts[:3] != ("docs", locale, category):
            fail(path_text, f"must live under docs/{locale}/{category}/")

    (validate_en_filename if locale == "en" else validate_zh_filename)(path, number)


def validate_catalog(localized_files: set[str]) -> None:
    data = load_json(CATALOG, "localization catalog")
    if data.get("maintained_locales") != ["en", "zh-CN"]:
        fail(CATALOG, "maintained_locales must currently be exactly ['en', 'zh-CN']")
    if set(data.get("public_categories", [])) != PUBLIC_CATEGORIES:
        fail(CATALOG, "public_categories does not match governed category set")

    documents = data.get("documents")
    if not isinstance(documents, list):
        fail(CATALOG, "documents must be an array")
        return

    seen_ids: set[str] = set()
    seen_targets: set[str] = set()
    catalog_targets: set[str] = set()

    for index, doc in enumerate(documents):
        label = f"catalog.documents[{index}]"
        if not isinstance(doc, dict):
            fail(label, "entry must be an object")
            continue

        required = {"id", "category", "number", "legacy_path", "zh_cn_path", "en_path", "status"}
        missing = required - set(doc)
        if missing:
            fail(label, f"missing fields: {sorted(missing)}")
            continue

        doc_id = doc.get("id")
        category = doc.get("category")
        number = doc.get("number")
        status = doc.get("status")
        en_path = doc.get("en_path")
        zh_path = doc.get("zh_cn_path")

        if not isinstance(doc_id, str) or not doc_id:
            fail(label, "id must be a non-empty string")
        elif doc_id in seen_ids:
            fail(label, f"duplicate id: {doc_id}")
        else:
            seen_ids.add(doc_id)

        if category not in PUBLIC_CATEGORIES | {"index"}:
            fail(label, f"invalid category: {category}")
        if not isinstance(number, str) or not re.fullmatch(r"\d{2}", number):
            fail(label, "number must be exactly two digits")
        if status not in ALLOWED_STATUS:
            fail(label, f"invalid status: {status}")
        if doc.get("legacy_path") is not None:
            fail(label, "legacy_path must be null after migration completion")

        if isinstance(en_path, str):
            validate_target_path(en_path, "en", category, number)
            catalog_targets.add(en_path)
        else:
            fail(label, "en_path must be a string")

        if isinstance(zh_path, str):
            validate_target_path(zh_path, "zh-CN", category, number)
            catalog_targets.add(zh_path)
        else:
            fail(label, "zh_cn_path must be a string")

        for target in (en_path, zh_path):
            if not isinstance(target, str):
                continue
            if target in seen_targets:
                fail(label, f"duplicate localized target path: {target}")
            seen_targets.add(target)

        en_exists = isinstance(en_path, str) and (REPO_ROOT / en_path).is_file()
        zh_exists = isinstance(zh_path, str) and (REPO_ROOT / zh_path).is_file()

        if status in {"current", "stale", "superseded"} and (not en_exists or not zh_exists):
            fail(label, f"{status} entry must have both maintained locale editions")
        if status == "translation-pending" and not zh_exists:
            fail(label, "translation-pending entry must at least have its zh-CN working edition")

    for path_text in sorted(localized_files - catalog_targets):
        fail(path_text, "localized public document is not registered in catalog.json")

    for path_text in sorted(catalog_targets - localized_files):
        path = REPO_ROOT / path_text
        if not path.is_file():
            # translation-pending English targets may legitimately not exist yet.
            matching = next((d for d in documents if d.get("en_path") == path_text or d.get("zh_cn_path") == path_text), None)
            if not matching or matching.get("status") != "translation-pending" or matching.get("en_path") != path_text:
                fail(path_text, "catalog target does not exist")


def validate_root_contract() -> None:
    required = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "README.zh-CN.md",
        REPO_ROOT / "CONTRIBUTING.md",
        REPO_ROOT / "CONTRIBUTING.zh-CN.md",
        DOCS / "README.md",
        DOCS / "README.zh-CN.md",
        DOCS / "en" / "00_baga-ink-documentation-index.md",
        DOCS / "zh-CN" / "00_项目文档入口.md",
        DOCS / "en" / "governance" / "01_documentation-internationalization-policy.md",
        DOCS / "zh-CN" / "governance" / "01_文档国际化与本地化规范.md",
        CATALOG,
        TERMINOLOGY,
    ]
    for path in required:
        if not path.is_file():
            fail(path, "required internationalization/governance file is missing")

    # Parse terminology so malformed machine governance cannot silently land.
    load_json(TERMINOLOGY, "terminology registry")


def main() -> int:
    validate_no_legacy_paths()
    validate_root_contract()

    localized_files = walk_locale("en") | walk_locale("zh-CN")
    validate_catalog(localized_files)

    if errors:
        print("Documentation i18n structure check FAILED:\n", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        print(
            "\nPublic docs must live only in docs/en and docs/zh-CN; legacy mixed-language public paths are forbidden.",
            file=sys.stderr,
        )
        return 1

    print("Documentation i18n structure check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
