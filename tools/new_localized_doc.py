#!/usr/bin/env python3
"""Create a paired English + zh-CN public documentation skeleton.

Example:

    python3 tools/new_localized_doc.py \
        standards 14 标准扩展示例 baga-ink-example-standard standards.14

Creates:

    docs/zh-CN/standards/14_标准扩展示例.md
    docs/en/standards/14_baga-ink-example-standard.md

and appends a `current` pair to docs/localization/catalog.json.

This tool is for *new* public documents. Existing legacy documents must follow
the migration plan instead of being silently duplicated by this command.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
CATALOG = DOCS / "localization" / "catalog.json"
PUBLIC_CATEGORIES = {"standards", "design", "reference-apps", "governance", "status"}
NUMBER_RE = re.compile(r"^\d{2}$")
EN_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def die(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def validate_args(category: str, number: str, zh_name: str, en_name: str, doc_id: str) -> None:
    if category not in PUBLIC_CATEGORIES:
        die(f"category must be one of: {sorted(PUBLIC_CATEGORIES)}")
    if not NUMBER_RE.fullmatch(number):
        die("number must be exactly two digits, e.g. 07 or 14")
    if "_" in zh_name or "/" in zh_name or "\\" in zh_name:
        die("Chinese descriptive name must not contain '_', '/' or '\\'")
    if not CJK_RE.search(zh_name):
        die("Chinese descriptive name must contain Chinese text")
    if not EN_RE.fullmatch(en_name):
        die("English descriptive name must be lowercase kebab-case")
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", doc_id):
        die("document id must use lowercase ASCII letters/numbers/dots/hyphens")


def load_catalog() -> dict:
    try:
        return json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        die(f"cannot load localization catalog: {exc}")


def write_new(path: Path, content: str) -> None:
    if path.exists():
        die(f"refusing to overwrite existing path: {path.relative_to(REPO_ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"created {path.relative_to(REPO_ROOT)}")


def zh_template(doc_id: str, category: str, number: str, zh_name: str, en_path: str) -> str:
    return f"""# {zh_name}

> **Document ID:** `{doc_id}`  
> **Category:** `{category}`  
> **Number:** `{number}`  
> **Language:** `zh-CN`  
> **English counterpart:** `{en_path}`  
> **Status:** Draft

---

## 目的

TBD

## 内容

TBD
"""


def en_template(doc_id: str, category: str, number: str, en_name: str, zh_path: str) -> str:
    title = en_name.replace("-", " ").title()
    return f"""# {title}

> **Document ID:** `{doc_id}`  
> **Category:** `{category}`  
> **Number:** `{number}`  
> **Language:** `en`  
> **Simplified Chinese counterpart:** `{zh_path}`  
> **Status:** Draft

---

## Purpose

TBD

## Content

TBD
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category")
    parser.add_argument("number")
    parser.add_argument("zh_name")
    parser.add_argument("en_name")
    parser.add_argument("doc_id")
    args = parser.parse_args()

    validate_args(args.category, args.number, args.zh_name, args.en_name, args.doc_id)

    zh_path = f"docs/zh-CN/{args.category}/{args.number}_{args.zh_name}.md"
    en_path = f"docs/en/{args.category}/{args.number}_{args.en_name}.md"
    zh_file = REPO_ROOT / zh_path
    en_file = REPO_ROOT / en_path

    data = load_catalog()
    docs = data.get("documents")
    if not isinstance(docs, list):
        die("catalog documents must be an array")

    for item in docs:
        if item.get("id") == args.doc_id:
            die(f"document id already exists in catalog: {args.doc_id}")
        if item.get("zh_cn_path") == zh_path or item.get("en_path") == en_path:
            die("target path already registered in catalog")
        if item.get("category") == args.category and item.get("number") == args.number:
            die(f"document number {args.number} is already used in category {args.category}")

    write_new(zh_file, zh_template(args.doc_id, args.category, args.number, args.zh_name, en_path))
    write_new(en_file, en_template(args.doc_id, args.category, args.number, args.en_name, zh_path))

    docs.append(
        {
            "id": args.doc_id,
            "category": args.category,
            "number": args.number,
            "legacy_path": None,
            "zh_cn_path": zh_path,
            "en_path": en_path,
            "status": "current",
        }
    )
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {CATALOG.relative_to(REPO_ROOT)}")

    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "check_docs_i18n.py")],
        cwd=REPO_ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
