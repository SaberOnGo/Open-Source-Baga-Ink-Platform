#!/usr/bin/env python3
"""Validate Baga Ink public documentation internationalization structure.

Public, long-lived prose is localized under:

    docs/en/
    docs/zh-CN/

The historical mixed-language public directories are temporarily allowed only
as a frozen migration zone described by docs/localization/catalog.json and
locked by docs/localization/legacy-lock.json.

This script uses only the Python standard library and exits non-zero on any
violation so it can run locally and in GitHub Actions.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
CATALOG_PATH = DOCS / "localization" / "catalog.json"
LEGACY_LOCK_PATH = DOCS / "localization" / "legacy-lock.json"
TERMINOLOGY_PATH = DOCS / "localization" / "terminology.json"

EN_NAME_RE = re.compile(r"^(?P<number>\d{2})_(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
ZH_NAME_RE = re.compile(r"^(?P<number>\d{2})_(?P<name>[^_]+)\.md$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

PUBLIC_CATEGORIES = {"standards", "design", "reference-apps", "governance", "status"}
ALLOWED_STATUS = {"migration-pending", "translation-pending", "current", "stale", "superseded"}
ALLOWED_TERM_POLICIES = {"keep", "keep-or-explain"}
LEGACY_PUBLIC_DIRS = {
    DOCS / "standards",
    DOCS / "design",
    DOCS / "reference-apps",
    DOCS / "governance",
    DOCS / "status",
}
LEGACY_ROOT_INDEX = DOCS / "00_项目文档入口_Baga-Ink-Documentation-Index.md"

errors: list[str] = []


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def fail(path: Path | str, message: str) -> None:
    label = rel(path) if isinstance(path, Path) else path
    errors.append(f"{label}: {message}")


def load_json(path: Path, label: str) -> dict:
    if not path.is_file():
        fail(path, f"{label} is missing")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(path, f"invalid UTF-8/JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        fail(path, f"{label} root must be an object")
        return {}
    return data


def load_catalog() -> dict:
    data = load_json(CATALOG_PATH, "localization catalog")
    if data.get("maintained_locales") != ["en", "zh-CN"]:
        fail(CATALOG_PATH, "maintained_locales must currently be exactly ['en', 'zh-CN']")
    if set(data.get("public_categories", [])) != PUBLIC_CATEGORIES:
        fail(CATALOG_PATH, "public_categories must match the governed public category set")
    if not isinstance(data.get("documents"), list):
        fail(CATALOG_PATH, "documents must be an array")
        data["documents"] = []
    return data


def validate_terminology() -> None:
    data = load_json(TERMINOLOGY_PATH, "localization terminology catalog")
    if data.get("locale") != "zh-CN":
        fail(TERMINOLOGY_PATH, "locale must currently be zh-CN")
    if not isinstance(data.get("default_rule"), str) or not data.get("default_rule"):
        fail(TERMINOLOGY_PATH, "default_rule must be a non-empty string")

    terms = data.get("terms")
    if not isinstance(terms, list):
        fail(TERMINOLOGY_PATH, "terms must be an array")
        return

    seen: set[str] = set()
    for i, item in enumerate(terms):
        label = f"terminology.terms[{i}]"
        if not isinstance(item, dict):
            fail(label, "entry must be an object")
            continue
        term = item.get("term")
        policy = item.get("policy")
        if not isinstance(term, str) or not term:
            fail(label, "term must be a non-empty string")
            continue
        if term in seen:
            fail(label, f"duplicate term: {term}")
        seen.add(term)
        if policy not in ALLOWED_TERM_POLICIES:
            fail(label, f"policy must be one of {sorted(ALLOWED_TERM_POLICIES)}")


def validate_en_filename(path: Path, expected_number: str | None = None) -> None:
    m = EN_NAME_RE.fullmatch(path.name)
    if not m:
        fail(path, "English public doc must match NN_lowercase-kebab-case-name.md")
        return
    if expected_number is not None and m.group("number") != expected_number:
        fail(path, f"filename number must be {expected_number}")
    if CJK_RE.search(path.name):
        fail(path, "English public filename must not contain Chinese characters")


def validate_zh_filename(path: Path, expected_number: str | None = None) -> None:
    m = ZH_NAME_RE.fullmatch(path.name)
    if not m:
        fail(path, "zh-CN public doc must match NN_中文名称.md with no second underscore suffix")
        return
    if expected_number is not None and m.group("number") != expected_number:
        fail(path, f"filename number must be {expected_number}")
    if not CJK_RE.search(m.group("name")):
        fail(path, "zh-CN public filename must contain Chinese descriptive text")


def validate_target_path(path_text: str, locale: str, category: str, number: str) -> None:
    path = REPO_ROOT / path_text
    parts = Path(path_text).parts

    if len(parts) < 3 or parts[0] != "docs" or parts[1] != locale:
        fail(path_text, f"must be under docs/{locale}/")
        return

    if category == "index":
        if len(parts) != 3:
            fail(path_text, "documentation index must live directly under the locale root")
    else:
        if len(parts) != 4 or parts[2] != category:
            fail(path_text, f"must be under docs/{locale}/{category}/")

    if locale == "en":
        validate_en_filename(path, number)
    else:
        validate_zh_filename(path, number)


def walk_localized_docs(locale: str) -> set[str]:
    root = DOCS / locale
    found: set[str] = set()
    if not root.is_dir():
        fail(root, "locale root is missing")
        return found

    expected_index = "00_baga-ink-documentation-index.md" if locale == "en" else "00_项目文档入口.md"

    for entry in root.iterdir():
        if entry.is_file():
            if entry.suffix != ".md":
                fail(entry, "only Markdown index documents are allowed at a locale root")
            elif entry.name != expected_index:
                fail(entry, "unexpected locale-root document")
            else:
                (validate_en_filename if locale == "en" else validate_zh_filename)(entry)
                found.add(rel(entry))
            continue

        if not entry.is_dir():
            fail(entry, "unsupported filesystem entry")
            continue

        if entry.name not in PUBLIC_CATEGORIES:
            fail(entry, f"unexpected localized public category; allowed: {sorted(PUBLIC_CATEGORIES)}")
            continue

        for item in entry.iterdir():
            if item.is_dir():
                fail(item, "public localized categories are flat; ad-hoc subdirectories are not allowed")
                continue
            if item.suffix != ".md":
                fail(item, "only Markdown prose documents are allowed in localized public categories")
                continue
            (validate_en_filename if locale == "en" else validate_zh_filename)(item)
            found.add(rel(item))

    return found


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def validate_legacy_lock(catalog_legacy_paths: set[str], actual_legacy: set[str]) -> None:
    data = load_json(LEGACY_LOCK_PATH, "legacy documentation lock")
    files = data.get("files")
    if not isinstance(files, dict):
        fail(LEGACY_LOCK_PATH, "files must be an object mapping repo path to Git blob SHA")
        return

    lock_paths = set(files)

    if lock_paths != actual_legacy:
        for path_text in sorted(actual_legacy - lock_paths):
            fail(path_text, "legacy file exists but is not locked")
        for path_text in sorted(lock_paths - actual_legacy):
            fail(path_text, "legacy lock points to a file that no longer exists; update catalog/lock as part of migration")

    if actual_legacy != catalog_legacy_paths:
        for path_text in sorted(actual_legacy - catalog_legacy_paths):
            fail(path_text, "legacy file is not registered by catalog.json")
        for path_text in sorted(catalog_legacy_paths - actual_legacy):
            fail(path_text, "catalog legacy_path does not exist")

    for path_text, expected in files.items():
        path = REPO_ROOT / path_text
        if not path.is_file():
            continue
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{40}", expected):
            fail(LEGACY_LOCK_PATH, f"invalid Git blob SHA for {path_text}")
            continue
        actual = git_blob_sha(path)
        if actual != expected:
            fail(
                path,
                "legacy public document content changed in place; migrate it to docs/zh-CN + docs/en instead of editing the legacy file",
            )


def validate_catalog(data: dict, localized_files: set[str]) -> None:
    seen_ids: set[str] = set()
    seen_targets: set[str] = set()
    catalog_targets: set[str] = set()
    catalog_legacy_paths: set[str] = set()

    for i, doc in enumerate(data.get("documents", [])):
        label = f"catalog.documents[{i}]"
        if not isinstance(doc, dict):
            fail(label, "entry must be an object")
            continue

        required = {"id", "category", "number", "zh_cn_path", "en_path", "status", "legacy_path"}
        missing = required - set(doc)
        if missing:
            fail(label, f"missing fields: {sorted(missing)}")
            continue

        doc_id = doc["id"]
        category = doc["category"]
        number = doc["number"]
        status = doc["status"]
        zh_path = doc["zh_cn_path"]
        en_path = doc["en_path"]
        legacy = doc["legacy_path"]

        if not isinstance(doc_id, str) or not doc_id:
            fail(label, "id must be a non-empty string")
        elif doc_id in seen_ids:
            fail(label, f"duplicate document id: {doc_id}")
        else:
            seen_ids.add(doc_id)

        if category not in PUBLIC_CATEGORIES | {"index"}:
            fail(label, f"invalid category: {category}")
        if not isinstance(number, str) or not re.fullmatch(r"\d{2}", number):
            fail(label, "number must be exactly two digits")
        if status not in ALLOWED_STATUS:
            fail(label, f"invalid status: {status}")

        if isinstance(zh_path, str):
            validate_target_path(zh_path, "zh-CN", category, number)
            catalog_targets.add(zh_path)
        else:
            fail(label, "zh_cn_path must be a string")

        if isinstance(en_path, str):
            validate_target_path(en_path, "en", category, number)
            catalog_targets.add(en_path)
        else:
            fail(label, "en_path must be a string")

        for target in (zh_path, en_path):
            if isinstance(target, str):
                if target in seen_targets:
                    fail(label, f"duplicate localized target path: {target}")
                seen_targets.add(target)

        legacy_exists = False
        if legacy is not None:
            if not isinstance(legacy, str):
                fail(label, "legacy_path must be null or a string")
            else:
                catalog_legacy_paths.add(legacy)
                legacy_exists = (REPO_ROOT / legacy).is_file()

        zh_exists = isinstance(zh_path, str) and (REPO_ROOT / zh_path).is_file()
        en_exists = isinstance(en_path, str) and (REPO_ROOT / en_path).is_file()

        if status == "migration-pending":
            if legacy is None or not legacy_exists:
                fail(label, "migration-pending entry must point to an existing legacy file")
        elif status == "translation-pending":
            if not zh_exists:
                fail(label, "translation-pending entry must have an existing zh-CN edition")
        elif status == "current":
            if not zh_exists or not en_exists:
                fail(label, "current entry must have both zh-CN and English editions")
        elif status == "stale":
            if not zh_exists or not en_exists:
                fail(label, "stale entry still requires both locale editions to exist")

    uncataloged = localized_files - catalog_targets
    for path_text in sorted(uncataloged):
        fail(path_text, "localized public document is not registered in catalog.json")

    actual_legacy: set[str] = set()
    for directory in LEGACY_PUBLIC_DIRS:
        if directory.is_dir():
            for item in directory.rglob("*"):
                if item.is_file():
                    actual_legacy.add(rel(item))
    if LEGACY_ROOT_INDEX.is_file():
        actual_legacy.add(rel(LEGACY_ROOT_INDEX))

    validate_legacy_lock(catalog_legacy_paths, actual_legacy)


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
        CATALOG_PATH,
        LEGACY_LOCK_PATH,
        TERMINOLOGY_PATH,
    ]
    for path in required:
        if not path.is_file():
            fail(path, "required internationalization foundation file is missing")


def main() -> int:
    validate_root_contract()
    validate_terminology()
    data = load_catalog()

    localized_files = walk_localized_docs("en") | walk_localized_docs("zh-CN")
    validate_catalog(data, localized_files)

    if errors:
        print("Documentation i18n structure check FAILED:\n", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        print(
            "\nPublic docs must use docs/en and docs/zh-CN. Legacy mixed-language public docs are locked migration-only inputs.",
            file=sys.stderr,
        )
        return 1

    print("Documentation i18n structure check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
